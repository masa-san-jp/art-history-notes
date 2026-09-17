#!/usr/bin/env python3
"""テーマ起点の調査を1回まとめる — 「実行のたびに調査が回り、使うたびに厚くなる」の入口。

    python3 tools/theme_research.py --theme "ムガル絵画"
    python3 tools/theme_research.py --theme "ムガル絵画" --json

このスクリプト自体は調べ物をしない（Web検索・出典評価はエージェントの仕事）。やることは3つだけ:

1. 検索して当たりを報告する（`bundle.py --search` と同じ検索・ログ経路を使う）
2. その検索を `data/queries.jsonl` に記録する（該当なしも記録する——探されたのに無かった、
   という需要を消さないため）
3. 現在の被覆グリッド（`data/coverage.json` の `grid`）をそのまま出す

当たりが薄い（stub/draft で出典が少ない）、または無い場合に何をするかは
`docs/agent/theme-research-task.md` の手順に従う。判断（このテーマにとって
どのregion×世紀の空白が関係するか、どの資料を信頼するか）は常にエージェント側に残す——
このKBの他のツール（build_graph.py の検証 と audit.py の指摘）と同じ、
「機械的チェックと判断を混ぜない」原則に従う。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from kb import ROOT, load_entities, log_query, search_entities

COVERAGE_PATH = ROOT / "data" / "coverage.json"


def hit_summary(hit_id, entities):
    meta = entities.get(hit_id) or {}
    return {
        "id": hit_id,
        "label_ja": meta.get("label_ja"),
        "type": meta.get("type"),
        "status": meta.get("status"),
        "n_sources": len(meta.get("sources") or []),
    }


def load_grid():
    if not COVERAGE_PATH.exists():
        return None
    data = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    return data.get("grid")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--theme", required=True, help="調べたい語（人名・movement名・地域名など、自由記述）")
    p.add_argument("--json", action="store_true", help="JSON で出す（他ツール・エージェントからの呼び出し用）")
    a = p.parse_args()

    entities, _ = load_entities()
    hit_ids = search_entities(a.theme, entities)
    log_query(a.theme, len(hit_ids))
    hits = [hit_summary(h, entities) for h in hit_ids]
    grid = load_grid()

    report = {
        "theme": a.theme,
        "hits": hits,
        "hit_count": len(hits),
        "coverage_grid": grid,
        "next_step": (
            "当たりが無い、または全件 stub/draft で出典が少なければ調査対象。"
            "docs/agent/theme-research-task.md の手順に従う。"
        ),
    }

    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(f"テーマ: {a.theme}")
    if not hits:
        print("該当なし。data/queries.jsonl に記録した。既存の空白かどうかは coverage_grid を見て判断する。")
    else:
        print(f"{len(hits)} 件ヒット:")
        for h in hits:
            print(f"  - {h['id']} （{h['label_ja']}／{h['status']}／出典{h['n_sources']}件）")
    print()
    print("被覆グリッド（region → {世紀: 件数}）:")
    for region, counts in sorted((grid or {}).items()):
        print(f"  {region}: {counts}")
    print()
    print("次にやること: docs/agent/theme-research-task.md を読み、このテーマに関係する")
    print("region×世紀の空白があれば調査対象にする。無理に埋めない——このテーマに")
    print("本当に関係する空白が無ければ、記録した検索ログだけが今回の成果でよい。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
