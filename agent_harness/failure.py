"""Closed failure taxonomy and finite retry policy."""

from __future__ import annotations

from enum import StrEnum


class FailureCode(StrEnum):
    TASK_INVALID = "task_invalid"
    DEPENDENCY_BLOCKED = "dependency_blocked"
    POLICY_VIOLATION = "policy_violation"
    SECRET_DETECTED = "secret_detected"
    LEASE_LOST = "lease_lost"
    BACKEND_TRANSIENT = "backend_transient"
    GITHUB_TRANSIENT = "github_transient"
    INFRA_TRANSIENT = "infra_transient"
    BACKEND_FAILED = "backend_failed"
    TASK_CHECK_FAILED = "task_check_failed"
    CANONICAL_VERIFY_FAILED = "canonical_verify_failed"
    TIMEOUT = "timeout"
    OUTPUT_LIMIT = "output_limit"
    CANCELLED = "cancelled"
    INTERNAL_ERROR = "internal_error"


NO_RETRY = frozenset({
    FailureCode.TASK_INVALID,
    FailureCode.DEPENDENCY_BLOCKED,
    FailureCode.POLICY_VIOLATION,
    FailureCode.SECRET_DETECTED,
    FailureCode.LEASE_LOST,
    FailureCode.CANCELLED,
    FailureCode.INTERNAL_ERROR,
})


def retry_allowed(code: FailureCode | str, *, attempt: int, max_attempts: int) -> bool:
    """Return whether the failure may produce another bounded attempt."""

    code = FailureCode(code)
    if attempt >= max_attempts or code in NO_RETRY:
        return False
    return True


def retry_delay_seconds(attempt: int, *, base: float = 2.0, maximum: float = 120.0) -> float:
    if attempt < 1:
        raise ValueError("attempt must be positive")
    return min(maximum, base * (2 ** (attempt - 1)))
