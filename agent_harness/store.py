"""SQLite-backed append-only run ledger and state machine."""

from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import sqlite3
import threading
import time
from typing import Any, Iterator

from .ids import new_run_id, utc_now
from .models import (
    ALLOWED_TRANSITIONS,
    ActiveRunExistsError,
    InvalidTransitionError,
    Run,
    RunState,
    RunNotFoundError,
    StateConflictError,
)


SCHEMA_VERSION = 1
_ACTIVE_SQL = "state NOT IN ('succeeded', 'blocked', 'failed', 'cancelled')"
_INITIALIZE_LOCK = threading.Lock()


class RunStore:
    """Own the local state database for one repository."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 30000")
        try:
            yield connection
        finally:
            connection.close()

    def _initialize(self) -> None:
        with _INITIALIZE_LOCK:
            for attempt in range(30):
                try:
                    with self._connection() as connection:
                        connection.execute("PRAGMA journal_mode = WAL")
                        connection.execute("PRAGMA synchronous = FULL")
                        connection.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)")
                        current = connection.execute("SELECT COALESCE(MAX(version), 0) FROM schema_migrations").fetchone()[0]
                        if current < 1:
                            connection.executescript(
                    """
                    BEGIN IMMEDIATE;
                        CREATE TABLE IF NOT EXISTS runs (
                            run_id TEXT PRIMARY KEY,
                            repository TEXT NOT NULL,
                            issue_number INTEGER NOT NULL CHECK (issue_number > 0),
                            contract_hash TEXT NOT NULL,
                            base_sha TEXT NOT NULL,
                            branch TEXT NOT NULL,
                            worktree TEXT NOT NULL,
                            backend TEXT NOT NULL,
                            state TEXT NOT NULL,
                            attempt INTEGER NOT NULL DEFAULT 0 CHECK (attempt >= 0),
                            heartbeat_at TEXT,
                            lease_expires_at TEXT,
                            reason_code TEXT,
                            reason_detail TEXT,
                            pr_number INTEGER,
                            cancel_requested INTEGER NOT NULL DEFAULT 0 CHECK (cancel_requested IN (0, 1)),
                            created_at TEXT NOT NULL,
                            updated_at TEXT NOT NULL
                        );
                        CREATE UNIQUE INDEX IF NOT EXISTS one_active_run_per_issue
                            ON runs(repository, issue_number) WHERE state NOT IN ('succeeded', 'blocked', 'failed', 'cancelled');
                        CREATE INDEX IF NOT EXISTS runs_by_state ON runs(state, created_at, run_id);
                        CREATE TABLE IF NOT EXISTS attempts (
                            run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
                            attempt INTEGER NOT NULL CHECK (attempt > 0),
                            state TEXT NOT NULL,
                            started_at TEXT NOT NULL,
                            ended_at TEXT,
                            failure_code TEXT,
                            failure_detail TEXT,
                            PRIMARY KEY (run_id, attempt)
                        );
                        CREATE TABLE IF NOT EXISTS events (
                            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
                            event_type TEXT NOT NULL,
                            from_state TEXT,
                            to_state TEXT,
                            attempt INTEGER NOT NULL,
                            occurred_at TEXT NOT NULL,
                            payload_json TEXT NOT NULL
                        );
                        CREATE INDEX IF NOT EXISTS events_by_run ON events(run_id, event_id);
                        CREATE TABLE IF NOT EXISTS artifacts (
                            artifact_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
                            attempt INTEGER NOT NULL,
                            kind TEXT NOT NULL,
                            path TEXT NOT NULL,
                            sha256 TEXT,
                            byte_count INTEGER,
                            created_at TEXT NOT NULL,
                            UNIQUE(run_id, attempt, kind, path)
                        );
                        CREATE TABLE IF NOT EXISTS leases (
                            repository TEXT NOT NULL,
                            issue_number INTEGER NOT NULL CHECK (issue_number > 0),
                            run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
                            owner_id TEXT NOT NULL,
                            token_hash TEXT NOT NULL,
                            acquired_at TEXT NOT NULL,
                            heartbeat_at TEXT NOT NULL,
                            expires_at TEXT NOT NULL,
                            PRIMARY KEY(repository, issue_number)
                        );
                    INSERT INTO schema_migrations(version, applied_at) VALUES (1, '""" + utc_now() + """');
                    COMMIT;
                    """
                            )
                        elif current != SCHEMA_VERSION:
                            raise RuntimeError(f"unsupported state database version: {current}")
                    return
                except sqlite3.OperationalError as exc:
                    if "locked" not in str(exc).lower() or attempt == 29:
                        raise
                    time.sleep(0.05)

    @staticmethod
    def hash_contract(normalized_contract: str) -> str:
        return hashlib.sha256(normalized_contract.encode("utf-8")).hexdigest()

    def create_run(
        self,
        *,
        repository: str,
        issue_number: int,
        contract_hash: str,
        base_sha: str,
        branch: str,
        worktree: str,
        backend: str,
        run_id: str | None = None,
    ) -> Run:
        run_id = run_id or new_run_id()
        now = utc_now()
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                connection.execute(
                    """INSERT INTO runs
                    (run_id, repository, issue_number, contract_hash, base_sha, branch, worktree, backend, state,
                     attempt, heartbeat_at, lease_expires_at, reason_code, reason_detail, pr_number,
                     cancel_requested, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, NULL, NULL, NULL, NULL, NULL, 0, ?, ?)""",
                    (run_id, repository, issue_number, contract_hash, base_sha, branch, worktree, backend, RunState.DISCOVERED.value, now, now),
                )
                self._insert_event(connection, run_id, "run.created", None, RunState.DISCOVERED, 0, now, {"issue_number": issue_number})
                connection.execute("COMMIT")
            except sqlite3.IntegrityError as exc:
                connection.execute("ROLLBACK")
                if "one_active_run_per_issue" in str(exc) or "UNIQUE constraint failed: runs.repository, runs.issue_number" in str(exc):
                    raise ActiveRunExistsError(f"active run already exists for {repository} issue #{issue_number}") from exc
                raise
            except Exception:
                connection.execute("ROLLBACK")
                raise
        return self.get_run(run_id)

    def get_run(self, run_id: str) -> Run:
        with self._connection() as connection:
            row = connection.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
        if row is None:
            raise RunNotFoundError(run_id)
        return Run.from_row(row)

    def list_runs(self, state: RunState | str | None = None) -> list[Run]:
        with self._connection() as connection:
            if state is None:
                rows = connection.execute("SELECT * FROM runs ORDER BY created_at, run_id").fetchall()
            else:
                value = RunState(state).value
                rows = connection.execute("SELECT * FROM runs WHERE state = ? ORDER BY created_at, run_id", (value,)).fetchall()
        return [Run.from_row(row) for row in rows]

    def transition(
        self,
        run_id: str,
        to_state: RunState | str,
        *,
        expected_state: RunState | str | None = None,
        reason_code: str | None = None,
        reason_detail: str | None = None,
        event_type: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> Run:
        target = RunState(to_state)
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                row = connection.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
                if row is None:
                    raise RunNotFoundError(run_id)
                current = RunState(row["state"])
                if expected_state is not None and current != RunState(expected_state):
                    raise StateConflictError(f"expected {expected_state}, found {current.value}")
                if target not in ALLOWED_TRANSITIONS[current]:
                    raise InvalidTransitionError(f"cannot transition {current.value} -> {target.value}")
                now = utc_now()
                connection.execute(
                    """UPDATE runs SET state = ?, reason_code = ?, reason_detail = ?, updated_at = ?,
                       cancel_requested = CASE WHEN ? = 'cancelled' THEN 0 ELSE cancel_requested END
                       WHERE run_id = ?""",
                    (target.value, reason_code, reason_detail, now, target.value, run_id),
                )
                self._insert_event(connection, run_id, event_type or f"run.{target.value}", current, target, row["attempt"], now, payload or {})
                connection.execute("COMMIT")
            except Exception:
                connection.execute("ROLLBACK")
                raise
        return self.get_run(run_id)

    def start_attempt(self, run_id: str, *, state: RunState = RunState.RUNNING) -> Run:
        if state not in {RunState.PREPARING, RunState.RUNNING}:
            raise InvalidTransitionError("attempt must start in preparing or running")
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                row = connection.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
                if row is None:
                    raise RunNotFoundError(run_id)
                current = RunState(row["state"])
                if state not in ALLOWED_TRANSITIONS[current]:
                    raise InvalidTransitionError(f"cannot start attempt from {current.value} -> {state.value}")
                attempt = row["attempt"] + 1
                now = utc_now()
                connection.execute("UPDATE runs SET state = ?, attempt = ?, updated_at = ? WHERE run_id = ?", (state.value, attempt, now, run_id))
                connection.execute("INSERT INTO attempts(run_id, attempt, state, started_at) VALUES (?, ?, ?, ?)", (run_id, attempt, state.value, now))
                self._insert_event(connection, run_id, "attempt.started", current, state, attempt, now, {})
                connection.execute("COMMIT")
            except Exception:
                connection.execute("ROLLBACK")
                raise
        return self.get_run(run_id)

    def finish_attempt(self, run_id: str, *, failure_code: str | None = None, failure_detail: str | None = None) -> Run:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                row = connection.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
                if row is None:
                    raise RunNotFoundError(run_id)
                now = utc_now()
                connection.execute(
                    "UPDATE attempts SET ended_at = ?, failure_code = ?, failure_detail = ? WHERE run_id = ? AND attempt = ?",
                    (now, failure_code, failure_detail, run_id, row["attempt"]),
                )
                connection.execute("UPDATE runs SET updated_at = ? WHERE run_id = ?", (now, run_id))
                self._insert_event(connection, run_id, "attempt.finished", RunState(row["state"]), RunState(row["state"]), row["attempt"], now, {"failure_code": failure_code} if failure_code else {})
                connection.execute("COMMIT")
            except Exception:
                connection.execute("ROLLBACK")
                raise
        return self.get_run(run_id)

    def heartbeat(self, run_id: str, *, lease_expires_at: str | None = None) -> Run:
        with self._connection() as connection:
            now = utc_now()
            changed = connection.execute(
                "UPDATE runs SET heartbeat_at = ?, lease_expires_at = COALESCE(?, lease_expires_at), updated_at = ? WHERE run_id = ? AND state NOT IN ('succeeded', 'blocked', 'failed', 'cancelled')",
                (now, lease_expires_at, now, run_id),
            ).rowcount
        if not changed:
            run = self.get_run(run_id)
            raise StateConflictError(f"cannot heartbeat terminal run {run.state.value}")
        return self.get_run(run_id)

    def request_cancel(self, run_id: str, reason: str) -> Run:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                row = connection.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
                if row is None:
                    raise RunNotFoundError(run_id)
                current = RunState(row["state"])
                if current in {RunState.SUCCEEDED, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED}:
                    connection.execute("COMMIT")
                    return Run.from_row(row)
                now = utc_now()
                connection.execute("UPDATE runs SET cancel_requested = 1, updated_at = ? WHERE run_id = ?", (now, run_id))
                self._insert_event(connection, run_id, "run.cancel_requested", current, current, row["attempt"], now, {"reason": reason})
                connection.execute("COMMIT")
            except Exception:
                connection.execute("ROLLBACK")
                raise
        return self.get_run(run_id)

    def cancel(self, run_id: str, reason: str) -> Run:
        run = self.get_run(run_id)
        if run.state in {RunState.SUCCEEDED, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED}:
            return run
        return self.transition(run_id, RunState.CANCELLED, expected_state=run.state, reason_code="cancelled", reason_detail=reason)

    def resume(self, run_id: str, reason: str) -> Run:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                row = connection.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
                if row is None:
                    raise RunNotFoundError(run_id)
                current = RunState(row["state"])
                if current not in {RunState.BLOCKED, RunState.FAILED}:
                    raise InvalidTransitionError(f"only blocked or failed runs can resume, found {current.value}")
                now = utc_now()
                connection.execute(
                    "UPDATE runs SET state = 'preparing', reason_code = 'resumed', reason_detail = ?, cancel_requested = 0, updated_at = ? WHERE run_id = ?",
                    (reason, now, run_id),
                )
                self._insert_event(connection, run_id, "run.resumed", current, RunState.PREPARING, row["attempt"], now, {"reason": reason})
                connection.execute("COMMIT")
            except Exception:
                connection.execute("ROLLBACK")
                raise
        return self.get_run(run_id)

    def record_artifact(self, run_id: str, *, kind: str, path: str, attempt: int | None = None, content: bytes | None = None) -> None:
        run = self.get_run(run_id)
        attempt = attempt if attempt is not None else run.attempt
        digest = hashlib.sha256(content).hexdigest() if content is not None else None
        byte_count = len(content) if content is not None else None
        with self._connection() as connection:
            connection.execute(
                """INSERT INTO artifacts(run_id, attempt, kind, path, sha256, byte_count, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(run_id, attempt, kind, path) DO UPDATE SET sha256=excluded.sha256, byte_count=excluded.byte_count""",
                (run_id, attempt, kind, path, digest, byte_count, utc_now()),
            )

    def set_pr_number(self, run_id: str, pr_number: int) -> Run:
        if pr_number <= 0:
            raise ValueError("pr number must be positive")
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                row = connection.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
                if row is None:
                    raise RunNotFoundError(run_id)
                if row["pr_number"] == pr_number:
                    connection.execute("COMMIT")
                    return Run.from_row(row)
                now = utc_now()
                connection.execute("UPDATE runs SET pr_number = ?, updated_at = ? WHERE run_id = ?", (pr_number, now, run_id))
                self._insert_event(connection, run_id, "delivery.pr_linked", RunState(row["state"]), RunState(row["state"]), row["attempt"], now, {"pr_number": pr_number})
                connection.execute("COMMIT")
            except Exception:
                connection.execute("ROLLBACK")
                raise
        return self.get_run(run_id)

    def record_lease(self, run_id: str, *, owner_id: str, token_hash: str, acquired_at: str, heartbeat_at: str, expires_at: str) -> None:
        run = self.get_run(run_id)
        with self._connection() as connection:
            connection.execute(
                """INSERT INTO leases(repository, issue_number, run_id, owner_id, token_hash, acquired_at, heartbeat_at, expires_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(repository, issue_number) DO UPDATE SET run_id=excluded.run_id, owner_id=excluded.owner_id,
                     token_hash=excluded.token_hash, acquired_at=excluded.acquired_at, heartbeat_at=excluded.heartbeat_at,
                     expires_at=excluded.expires_at""",
                (run.repository, run.issue_number, run_id, owner_id, token_hash, acquired_at, heartbeat_at, expires_at),
            )

    def heartbeat_lease(self, run_id: str, *, heartbeat_at: str, expires_at: str) -> None:
        with self._connection() as connection:
            connection.execute("UPDATE leases SET heartbeat_at = ?, expires_at = ? WHERE run_id = ?", (heartbeat_at, expires_at, run_id))

    def release_lease(self, run_id: str, *, owner_id: str, token_hash: str) -> None:
        with self._connection() as connection:
            connection.execute("DELETE FROM leases WHERE run_id = ? AND owner_id = ? AND token_hash = ?", (run_id, owner_id, token_hash))

    def recover_run(self, run_id: str, *, reason: str) -> Run:
        """Move a stale non-terminal run back to preparation without changing its ID."""
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                row = connection.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
                if row is None:
                    raise RunNotFoundError(run_id)
                current = RunState(row["state"])
                if current in {RunState.SUCCEEDED, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED}:
                    connection.execute("COMMIT")
                    return Run.from_row(row)
                now = utc_now()
                connection.execute("UPDATE runs SET state = 'preparing', reason_code = 'crash_recovered', reason_detail = ?, updated_at = ? WHERE run_id = ?", (reason, now, run_id))
                self._insert_event(connection, run_id, "run.crash_recovered", current, RunState.PREPARING, row["attempt"], now, {"reason": reason})
                connection.execute("COMMIT")
            except Exception:
                connection.execute("ROLLBACK")
                raise
        return self.get_run(run_id)

    def events(self, run_id: str) -> list[dict[str, Any]]:
        with self._connection() as connection:
            rows = connection.execute("SELECT * FROM events WHERE run_id = ? ORDER BY event_id", (run_id,)).fetchall()
        return [
            {
                "event_id": row["event_id"],
                "run_id": row["run_id"],
                "event_type": row["event_type"],
                "from_state": row["from_state"],
                "to_state": row["to_state"],
                "attempt": row["attempt"],
                "occurred_at": row["occurred_at"],
                "payload": json.loads(row["payload_json"]),
            }
            for row in rows
        ]

    def record_event(self, run_id: str, event_type: str, payload: dict[str, Any] | None = None) -> None:
        """Append an observational event without changing run state."""
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                row = connection.execute("SELECT state, attempt FROM runs WHERE run_id = ?", (run_id,)).fetchone()
                if row is None:
                    raise RunNotFoundError(run_id)
                now = utc_now()
                state = RunState(row["state"])
                self._insert_event(connection, run_id, event_type, state, state, row["attempt"], now, payload or {})
                connection.execute("COMMIT")
            except Exception:
                connection.execute("ROLLBACK")
                raise

    @staticmethod
    def _insert_event(
        connection: sqlite3.Connection,
        run_id: str,
        event_type: str,
        from_state: RunState | None,
        to_state: RunState | None,
        attempt: int,
        occurred_at: str,
        payload: dict[str, Any],
    ) -> None:
        connection.execute(
            """INSERT INTO events(run_id, event_type, from_state, to_state, attempt, occurred_at, payload_json)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                run_id,
                event_type,
                from_state.value if from_state else None,
                to_state.value if to_state else None,
                attempt,
                occurred_at,
                json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
            ),
        )
