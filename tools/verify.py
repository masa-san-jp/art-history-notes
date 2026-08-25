#!/usr/bin/env python3
"""Run the repository's complete deterministic verification sequence.

The command is intentionally small and ordered. It is the single entry point
used by local development, the git hook, and CI:

    uv run --locked python tools/verify.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def steps() -> list[list[str]]:
    """Return commands in the order required to validate and regenerate the KB."""
    python = sys.executable
    return [
        [python, "tools/build_graph.py", "--check"],
        [python, "tools/build_context_vectors.py", "--check"],
        [python, "-m", "unittest", "discover", "-s", "tests", "-p", "test*.py"],
        [python, "tools/build_graph.py"],
        [python, "tools/audit.py"],
        [python, "tools/build_context_vectors.py"],
        ["git", "diff", "--exit-code", "--", "data/", "overviews/coverage.md"],
    ]


def main() -> int:
    for command in steps():
        try:
            result = subprocess.run(command, cwd=ROOT, check=False)
        except OSError as exc:
            print(f"verify: command failed to start: {' '.join(command)}: {exc}", file=sys.stderr)
            return 1
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
