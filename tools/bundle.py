#!/usr/bin/env python3
"""知識のまとまりを1文書として取り出す。ばらばらのファイルを読み歩かずに済むようにするため。

    python3 tools/bundle.py movement/neo-impressionism            # 1件とその周辺（1ホップ）
    python3 tools/bundle.py movement/neo-impressionism --depth 2  # 2ホップまで
    python3 tools/bundle.py --region asia-east-japan              # 文化圏でまとめて
    python3 tools/bundle.py --century 19                          # 世紀でまとめて
    python3 tools/bundle.py movement/... -o /tmp/bundle.md        # ファイルへ

出力は markdown 1本。中心エンティティの本文をそのまま入れ、周辺は要約行＋関係で示し、
出典URLを最後に集約する。
"""

import argparse
import sys
from pathlib import Path

from kb import (ROOT, alias_map, build_edges, century_of_year, edtf_year_range, load_entities, log_query,
                load_region_history, read_frontmatter, regions_of, resolve, search_entities)


def summarize(meta):
    t = meta.get("time") or {}
    span = "–".join(str(x) for x in (t.get("start"), t.get("end")) if x) or "年代未確認"
    kind = f"／{meta['kind']}" if meta.get("kind") else ""
    return f"{meta.get('label_ja')}（{meta.get('type')}{kind}・{span}・{meta.get('status')}）"


def neighbors(center, edges, depth):
    seen, frontier = {center}, {center}
    for _ in range(depth):
        nxt = set()
        for e in edges:
            if e["from"] in frontier and e["to"] not in seen:
                nxt.add(e["to"])
            if e["to"] in frontier and e["from"] not in seen:
                nxt.add(e["from"])
        seen |= nxt
        frontier = nxt
    return seen


def render(centers, entities, edges, title):
    lines = [f"# 知識バンドル: {title}", "",
             "生成物（`tools/bundle.py`）。編集しても KB には戻らない。正は `entities/` 側。", ""]
    sources = []
    for cid in centers:
        meta = entities.get(cid)
        if not meta:
            lines.append(f"- （見つからない: {cid}）")
            continue
        body = read_frontmatter(ROOT / meta["path"])[1].strip()
        lines += [f"## {summarize(meta)}", f"`{cid}` — {meta['path']}", ""]
        if meta.get("naming"):
            n = meta["naming"]
            bits = ["自称あり" if n.get("self_identified") else "自称なし（後付けの命名）"]
            if n.get("named_by"):
                bits.append(f"命名者 {n['named_by']}")
            if n.get("named_when"):
                bits.append(f"命名 {n['named_when']}")
            if n.get("original_label"):
                bits.append(f"原語 {n['original_label']}")
            lines.append("命名: " + "／".join(bits))
        if meta.get("evidence"):
            lines += ["", "証拠接続:"] + [
                f"- `{item.get('target')}`（supports: {', '.join(item.get('supports') or [])}）"
                for item in meta["evidence"]
            ]
        out_edges = [e for e in edges if e["from"] == cid and not e.get("derived")]
        in_edges = [e for e in edges if e["to"] == cid and not e.get("derived")]
        sources += [e["source"] for e in out_edges + in_edges if e.get("source")]
        if out_edges:
            lines += ["", "関係（この節から出る）:"] + [
                f"- {e['type']} → {summarize(entities[e['to']]) if e['to'] in entities else e['to']}"
                + (f"（{e['certainty']}）" if e.get("certainty") else "")
                + (f"  根拠: {e['source']}" if e.get("source") else "") for e in out_edges]
        if in_edges:
            lines += ["", "関係（この節へ入る）:"] + [
                f"- {summarize(entities[e['from']]) if e['from'] in entities else e['from']}"
                f" — {e['type']} →" for e in in_edges]
        lines += ["", body, ""]
        sources += meta.get("sources") or []
    if sources:
        lines += ["## 出典（このバンドル全体）", ""] + [f"- {s}" for s in dict.fromkeys(sources)]
    return "\n".join(lines) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("center", nargs="?", help="中心にする id（例 movement/neo-impressionism）")
    p.add_argument("--depth", type=int, default=1)
    p.add_argument("--region", help="文化圏バケットでまとめる")
    p.add_argument("--century", type=int, help="起点の世紀でまとめる（19 = 1800年代）")
    p.add_argument("--search", help="語で探す（label と本文を見る）。1件なら束を出し、複数なら一覧を出す")
    p.add_argument("-o", "--out")
    a = p.parse_args()

    entities, _ = load_entities()
    edges = build_edges(entities)
    region_history = load_region_history()

    if a.search:
        hits = search_entities(a.search, entities)
        log_query(a.search, len(hits))
        if not hits:
            print(f"該当なし: {a.search}\n（overviews/coverage.md の空欄も見る——まだ無い領域かもしれない）",
                  file=sys.stderr)
            return 1
        if len(hits) > 1:
            print(f"「{a.search}」に触れているもの {len(hits)} 件:")
            for eid in hits:
                m = entities[eid]
                print(f"  {eid}  — {summarize(m)}")
            print("\n1件に絞って束で読む: python3 tools/bundle.py <id>")
            return 0
        a.center = hits[0]
        print(f"（1件だけ該当: {a.center}）\n", file=sys.stderr)

    if a.center:
        a.center = resolve(a.center, entities, alias_map(entities))
        if a.center not in entities:
            print(f"✗ そんな id は無い: {a.center}", file=sys.stderr)
            return 1
        ids = [a.center] + sorted(neighbors(a.center, edges, a.depth) - {a.center})
        title = f"{entities[a.center]['label_ja']}（{a.depth}ホップ）"
    elif a.region:
        ids = sorted(i for i, m in entities.items()
                     if m.get("type") == "movement"
                     and a.region in regions_of(i, entities, region_history))
        title = f"文化圏 {a.region}"
    elif a.century:
        ids = []
        for i, m in entities.items():
            if m.get("type") != "movement":
                continue
            lo, _ = edtf_year_range((m.get("time") or {}).get("start"))
            if lo is not None and century_of_year(lo) == a.century:
                ids.append(i)
        ids.sort()
        title = f"{a.century}世紀に始まる movement"
    else:
        p.error("center か --region か --century のどれかを指定する")

    text = render(ids, entities, edges, title)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"✓ {a.out}（{len(ids)} エンティティ）")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
