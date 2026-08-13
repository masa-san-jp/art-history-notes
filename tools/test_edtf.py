#!/usr/bin/env python3
"""EDTF の受け入れと年の展開のテスト。

    python3 tools/test_edtf.py

紀元前を入れたときに壊れやすいのは3か所——正規表現が符号を弾く、マスクの最小・最大が
符号で入れ替わる、西暦0年が `if year` で falsy になって落ちる。ここはその退行を止める。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from kb import century_label, edtf_ok, edtf_year_range  # noqa: E402

ACCEPT = ["1884", "1884-05", "1884-05-20", "146X", "18XX", "1503~", "1884?", "..",
          "-0899", "-08XX", "-0001", "0000", None]
REJECT = ["184", "18845", "abcd", "18X4", "--0899", "1884-", ""]

RANGES = [
    ("1884", (1884, 1884)),
    ("146X", (1460, 1469)),
    ("18XX", (1800, 1899)),
    ("1503~", (1503, 1503)),
    # 符号付きはここが本題。-09XX は -999〜-900 で、正のときと最小・最大が入れ替わる。
    ("-0899", (-899, -899)),
    ("-09XX", (-999, -900)),
    ("-0XXX", (-999, 0)),
    ("0000", (0, 0)),
    ("..", (None, None)),
    (None, (None, None)),
]

CENTURIES = [
    (1884, "19"),
    (1900, "20"),
    (1, "1"),
    (0, "1"),          # 西暦0年＝紀元前1年。falsy だが "unknown" に落としてはいけない
    (-899, "-9"),      # 天文学的 -0899 ＝ 紀元前900年 → 前9世紀
    (-1, "-1"),
    (None, "unknown"),
]


def main():
    failures = []

    for v in ACCEPT:
        if not edtf_ok(v):
            failures.append(f"受けるべき値を弾いた: {v!r}")
    for v in REJECT:
        if edtf_ok(v):
            failures.append(f"弾くべき値を受けた: {v!r}")

    for v, expected in RANGES:
        got = edtf_year_range(v)
        if got != expected:
            failures.append(f"年の展開が違う: {v!r} -> {got} (期待 {expected})")

    for year, expected in CENTURIES:
        got = century_label(year)
        if got != expected:
            failures.append(f"世紀のキーが違う: {year} -> {got!r} (期待 {expected!r})")

    if failures:
        print(f"✗ {len(failures)} 件:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"✓ {len(ACCEPT) + len(REJECT) + len(RANGES) + len(CENTURIES)} 件 — 問題なし")
    return 0


if __name__ == "__main__":
    sys.exit(main())
