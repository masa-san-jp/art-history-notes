"""Identifiers and timestamps used by the durable run ledger."""

from __future__ import annotations

from datetime import datetime, timezone
import random
import uuid


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def new_run_id(now_ms: int | None = None, rand: random.Random | None = None) -> str:
    """Create an RFC 9562 UUIDv7 without an extra dependency."""

    if now_ms is None:
        now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    generator = rand or random.SystemRandom()
    timestamp = now_ms & ((1 << 48) - 1)
    random_a = generator.getrandbits(12)
    random_b = generator.getrandbits(62)
    value = timestamp << 80
    value |= 0x7 << 76
    value |= random_a << 64
    value |= 0b10 << 62
    value |= random_b
    return str(uuid.UUID(int=value))
