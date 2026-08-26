#!/usr/bin/env python3
"""Run the repository-local external-agent readiness suite."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_agent_*.py"],
        cwd=ROOT,
        check=False,
    )
    if tests.returncode:
        return tests.returncode
    canonical = subprocess.run(
        ["uv", "run", "--locked", "python", "tools/verify.py"],
        cwd=ROOT,
        check=False,
    )
    return canonical.returncode


if __name__ == "__main__":
    raise SystemExit(main())
