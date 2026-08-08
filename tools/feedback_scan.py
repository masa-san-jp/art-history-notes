#!/usr/bin/env python3
"""公開物 → KB の還り線。どの記述が外に出て、どう受けたかを KB 側に戻す。

系が一方通行だと、KB は「探された語」までしか需要を知れない。実際に外に出て反応があったかどうかは
公開側にしかない。その台帳を読んで突き合わせるのがこのスクリプト。

    python3 tools/feedback_scan.py            # 突き合わせて data/citations.json を書く
    python3 tools/feedback_scan.py --dry-run  # 書かずに表示だけ

台帳（読むだけ・こちらからは書かない）:
  Agent-team/tools/note-metrics/articles.jsonl（note 公開の SSOT・aiko-pr 管理）

突き合わせ方は2段。
  1. `kb_refs` — 記事側が使った KB の id を書いていればそれを使う（確実。※台帳への項目追加は要相談）
  2. 表題の照合 — `kb_refs` が無い記事は、表題に KB のラベルが出ているかだけ見る（弱い代替）

**本文は取りに行かない。** 48件を毎回 fetch するのは重く、外部への負荷にもなる。確実さが要るなら
記事側が id を書く方が安く、正確。

**2026-08-08 の初回実行の結果**: 48件中、id 明記は0件、表題一致は2件（どちらも「京都」を含む記事で、
KB を引いた記事ではない＝偽陽性）。つまり**線は繋いだが、まだ信号が流れていない**。
表題照合は代替として弱い。`kb_refs` が入るまで、この出力を根拠に優先順位を動かさない。
"""

import argparse
import json
import sys
from pathlib import Path

from kb import ROOT, load_entities

LEDGER = Path.home() / "dev/Agent-Lab/Agent-team/tools/note-metrics/articles.jsonl"
OUT = ROOT / "data" / "citations.json"


def read_ledger(path):
    if not path.exists():
        return None
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ledger", default=str(LEDGER))
    a = ap.parse_args()

    articles = read_ledger(Path(a.ledger))
    if articles is None:
        print(f"台帳が無い: {a.ledger}\n（aiko-pr 側の置き場が変わった可能性。確認してから直す）",
              file=sys.stderr)
        return 1

    entities, _ = load_entities()
    labels = {}
    for eid, meta in entities.items():
        for key in ("label_ja", "label_en"):
            v = (meta.get(key) or "").strip()
            if len(v) >= 2:
                labels.setdefault(v, eid)

    cited, explicit, guessed = {}, 0, 0
    for art in articles:
        refs = art.get("kb_refs") or []
        if refs:
            explicit += 1
        else:
            title = art.get("title") or ""
            refs = sorted({eid for label, eid in labels.items() if label in title})
            if refs:
                guessed += 1
        for eid in refs:
            row = cited.setdefault(eid, {"articles": [], "likes_total": 0})
            row["articles"].append({"title": art.get("title"), "url": art.get("url"),
                                    "likes_24h": art.get("likes_24h"),
                                    "matched_by": "kb_refs" if art.get("kb_refs") else "title"})
            try:
                row["likes_total"] += int(art.get("likes_24h") or 0)
            except (TypeError, ValueError):
                pass

    result = {
        "ledger": str(a.ledger),
        "articles_scanned": len(articles),
        "matched_by_kb_refs": explicit,
        "matched_by_title": guessed,
        "cited": cited,
    }

    print(f"記事 {len(articles)} 件を見た — id 明記 {explicit} 件 / 表題一致 {guessed} 件")
    if cited:
        for eid, row in sorted(cited.items(), key=lambda x: -x[1]["likes_total"]):
            print(f"  {eid} — 記事 {len(row['articles'])}本 / スキ計 {row['likes_total']}")
    else:
        print("  KB を引いた記事はまだ無い（表題照合では拾えていないだけの可能性もある）")
        print("  確実にするには、公開台帳に kb_refs（使った KB の id）を1項目足すのが安い。要相談。")

    if not a.dry_run:
        OUT.parent.mkdir(exist_ok=True)
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
