"""Bounded subprocess execution without a shell."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import selectors
import signal
import subprocess
import time
import threading
import tempfile

from .policy import ExecutionPolicy, PolicyViolation, Redactor


@dataclass(frozen=True)
class ProcessResult:
    argv: tuple[str, ...]
    returncode: int | None
    stdout: bytes
    stderr: bytes
    timed_out: bool
    cancelled: bool
    output_limited: bool
    duration_seconds: float


def _stop(process: subprocess.Popen[bytes]) -> None:
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGTERM)
            return
        except (ProcessLookupError, PermissionError):
            process.terminate()
            return
    process.terminate()


def _kill(process: subprocess.Popen[bytes]) -> None:
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL)
            return
        except (ProcessLookupError, PermissionError):
            process.kill()
            return
    process.kill()


def run_argv(
    argv: list[str] | tuple[str, ...],
    *,
    cwd: Path,
    timeout_seconds: int,
    max_output_bytes: int,
    policy: ExecutionPolicy | None = None,
    env: dict[str, str] | None = None,
    redactor: Redactor | None = None,
    cancel_event: threading.Event | None = None,
    stdin_data: bytes | None = None,
) -> ProcessResult:
    policy = policy or ExecutionPolicy(max_output_bytes=max_output_bytes)
    policy.validate_argv(list(argv))
    policy.validate_timeout(timeout_seconds)
    if max_output_bytes < 1:
        raise PolicyViolation("max_output_bytes must be positive")
    started = time.monotonic()
    stdin_stream = None
    if stdin_data is not None:
        stdin_stream = tempfile.TemporaryFile()
        stdin_stream.write(stdin_data)
        stdin_stream.seek(0)
    try:
        process = subprocess.Popen(
            list(argv),
            cwd=cwd,
            env=env,
            shell=False,
            stdin=stdin_stream if stdin_stream is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=os.name == "posix",
        )
    except Exception:
        if stdin_stream is not None:
            stdin_stream.close()
        raise
    selector = selectors.DefaultSelector()
    assert process.stdout is not None
    assert process.stderr is not None
    selector.register(process.stdout, selectors.EVENT_READ, "stdout")
    selector.register(process.stderr, selectors.EVENT_READ, "stderr")
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    timed_out = False
    cancelled = False
    output_limited = False
    try:
        while selector.get_map():
            remaining = timeout_seconds - (time.monotonic() - started)
            if cancel_event is not None and cancel_event.is_set():
                cancelled = True
                _stop(process)
            if remaining <= 0 and process.poll() is None:
                timed_out = True
                _stop(process)
            events = selector.select(timeout=min(0.1, max(0.0, remaining)))
            for key, _ in events:
                data = os.read(key.fileobj.fileno(), 65536)
                if not data:
                    selector.unregister(key.fileobj)
                    continue
                total = len(buffers["stdout"]) + len(buffers["stderr"])
                room = max_output_bytes - total
                if room <= 0:
                    output_limited = True
                    continue
                if len(data) > room:
                    buffers[key.data].extend(data[:room])
                    output_limited = True
                else:
                    buffers[key.data].extend(data)
            if (timed_out or cancelled or output_limited) and process.poll() is None:
                _stop(process)
            if process.poll() is not None and not events:
                for key in list(selector.get_map().values()):
                    try:
                        data = os.read(key.fileobj.fileno(), 65536)
                    except OSError:
                        data = b""
                    if data:
                        total = len(buffers["stdout"]) + len(buffers["stderr"])
                        room = max_output_bytes - total
                        if room > 0:
                            buffers[key.data].extend(data[:room])
                        if len(data) > room:
                            output_limited = True
                    else:
                        selector.unregister(key.fileobj)
        returncode = process.wait(timeout=5)
    finally:
        selector.close()
        if process.poll() is None:
            _kill(process)
            process.wait(timeout=5)
        if process.stdout is not None:
            process.stdout.close()
        if process.stderr is not None:
            process.stderr.close()
        if stdin_stream is not None:
            stdin_stream.close()
    redactor = redactor or Redactor()
    return ProcessResult(
        argv=tuple(argv),
        returncode=returncode,
        stdout=redactor.bytes(bytes(buffers["stdout"])),
        stderr=redactor.bytes(bytes(buffers["stderr"])),
        timed_out=timed_out,
        cancelled=cancelled,
        output_limited=output_limited,
        duration_seconds=time.monotonic() - started,
    )
