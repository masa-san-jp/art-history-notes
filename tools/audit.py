#!/usr/bin/env python3
"""体系の食い違いと偏りを検査して、次に調べることを KB 自身に出させる。

`build_graph.py --check` が見ているのは**壊れているか**（必須項目・参照先・語彙）。それだけだと、
形は正しいが中身が食い違っている状態を誰も指摘しない。人が読んで気づくしかない＝知識が増えても
次の問いが出てこない。ここはその穴を埋める。

    python3 tools/audit.py            # 検査して data/audit.json を書き、被覆マップに反映
    python3 tools/audit.py --dry-run  # 表示だけ

検査するもの（すべて美術史の構造そのものに関するもの）:
  1. 時間の逆行 — 派生元より先に始まっている／後付けの命名年が対象の開始より前
  2. 型の食い違い — grouped_as の先が retrospective でない（後付けの括りでないものに括られている）
  3. kind の地域偏り — ある文化圏の movement が1種類の kind だけ。kind が地域の言い換えに堕ちている疑い
  4. 仮説の未検証 — 俯瞰が挙げた反証先の文化圏が空のまま（＝崩しに行っていない）
  5. 片側だけの継承 — derives_from の先が stub のまま（辿れる先が空）
  6. 文化圏を跨ぐ関係の欠如 — 他の文化圏の movement と1本も繋がっていない（島として扱っている）

これらは commit を止めない（壊れてはいないので）。**次に何を調べるかの材料として出す。**
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

from kb import ROOT, build_edges, edtf_year_range, load_config, load_entities, load_region_history, regions_of

OVERVIEWS = ROOT / "overviews"
OUT = ROOT / "data" / "audit.json"
COVERAGE = OVERVIEWS / "coverage.md"
MARK_START = "<!-- generated:audit:start -->"
MARK_END = "<!-- generated:audit:end -->"


def start_year(meta):
    return edtf_year_range((meta.get("time") or {}).get("start"))[0]


def check_time_order(entities, edges, findings):
    """派生・後続の関係が時間と矛盾していないか。"""
    for e in edges:
        if e.get("derived") or e["type"] not in ("derives_from", "precedes"):
            continue
        a, b = entities.get(e["from"]), entities.get(e["to"])
        if not a or not b:
            continue
        ya, yb = start_year(a), start_year(b)
        if ya is None or yb is None:
            continue
        if e["type"] == "derives_from" and ya < yb:
            findings.append({"kind": "time-order", "about": e["from"],
                             "text": f"{a['label_ja']}（{ya}）が派生元 {b['label_ja']}（{yb}）より先に始まっている"})
        if e["type"] == "precedes" and ya > yb:
            findings.append({"kind": "time-order", "about": e["from"],
                             "text": f"{a['label_ja']}（{ya}）が後続とした {b['label_ja']}（{yb}）より後に始まっている"})

    for eid, meta in entities.items():
        naming = meta.get("naming") or {}
        named = edtf_year_range(naming.get("named_when"))[0]
        start = start_year(meta)
        # self-declared は、名称を作った後に宣言・制度化されることがある。
        # 例: 民藝は1925年に語が生まれ、1926年に設立趣意書で公表された。
        # 後付けの括り（retrospective）だけを、対象開始後の命名という時間順で監査する。
        if named and start and named < start and meta.get("kind") == "retrospective":
            findings.append({"kind": "time-order", "about": eid,
                             "text": f"{meta['label_ja']}: 命名年 {named} が対象の開始 {start} より前"})


def check_grouped_as(entities, edges, findings):
    """後付けの括りへの所属先が、本当に後付けの括りか。"""
    for e in edges:
        if e.get("derived") or e["type"] != "grouped_as":
            continue
        target = entities.get(e["to"])
        if target and target.get("kind") != "retrospective":
            findings.append({"kind": "type-mismatch", "about": e["from"],
                             "text": f"{entities[e['from']]['label_ja']} が grouped_as で指す "
                                     f"{target['label_ja']} の kind が {target.get('kind')}"
                                     "（後付けの括りは retrospective のはず。part_of の誤用か、相手の kind が誤り）"})


def check_kind_bias(entities, cfg, findings, region_history):
    """kind が文化圏の言い換えになっていないか（非西洋＝lineage-school だけ、等）。"""
    by_region = defaultdict(list)
    for eid, meta in entities.items():
        if meta.get("type") != "movement":
            continue
        for r in regions_of(eid, entities, region_history):
            by_region[r].append(meta.get("kind"))
    for region, kinds in sorted(by_region.items()):
        if len(kinds) >= 2 and len(set(kinds)) == 1:
            findings.append({"kind": "kind-bias", "about": region,
                             "text": f"{region} の movement {len(kinds)}件が全部 {kinds[0]}。"
                                     "kind が地域の言い換えになっていないか、別の kind の例を1件探す"})


def check_hypotheses(entities, cfg, findings, region_history):
    """俯瞰が挙げた反証先の文化圏に、まだ1件も入っていないもの。"""
    counts = defaultdict(int)
    for eid, meta in entities.items():
        if meta.get("type") == "movement":
            for r in regions_of(eid, entities, region_history):
                counts[r] += 1
    for path in sorted(OVERVIEWS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        meta = yaml.safe_load(text.split("---\n", 2)[1]) or {}
        # 既に試した先は指さない（org で試した場合など、movement が増えないこともある）
        tested = {row.get("region") for row in (meta.get("tested") or []) if isinstance(row, dict)}
        for region in meta.get("tests_regions") or []:
            if region not in cfg["buckets"]:
                findings.append({"kind": "hypothesis", "about": path.name,
                                 "text": f"tests_regions に未知の文化圏 {region}"})
            elif region in tested:
                continue
            elif counts.get(region, 0) == 0:
                findings.append({"kind": "hypothesis", "about": path.name,
                                 "text": f"{path.name} の仮説を崩しにいく先 {region} が空のまま"
                                         "（反証を試していないので仮説のまま止まっている）"})


def check_dangling_lineage(entities, edges, findings):
    """継承をたどった先が stub のまま（＝辿れない）。"""
    for e in edges:
        if e.get("derived") or e["type"] not in ("derives_from", "taught_by", "grouped_as"):
            continue
        target = entities.get(e["to"])
        if target and target.get("status") == "stub":
            findings.append({"kind": "dead-end", "about": e["to"],
                             "text": f"{entities[e['from']]['label_ja']} の {e['type']} 先 "
                                     f"{target['label_ja']} が stub のまま（辿れない）"})


def check_cross_region_links(entities, edges, findings, region_history):
    """他の文化圏の movement と1本も繋がっていない movement。

    時間軸だけでなく空間的な広がりと関連性を体系化するのが目的なので、どの文化圏とも繋がっていない
    ものは「その文化圏を孤立した島として扱っている」状態を意味する。影響・伝播・反発を調べていない
    可能性が高い。壊れてはいないので commit は止めず、次に何を調べるかの材料として出す。
    """
    total, isolated = 0, defaultdict(list)
    for eid, meta in sorted(entities.items()):
        if meta.get("type") != "movement" or meta.get("status") == "stub":
            continue
        own = set(regions_of(eid, entities, region_history))
        if not own:
            continue
        total += 1
        linked = set()
        for e in edges:
            other = e["to"] if e["from"] == eid else (e["from"] if e["to"] == eid else None)
            if not other or (entities.get(other) or {}).get("type") != "movement":
                continue
            linked |= set(regions_of(other, entities, region_history))
        if not (linked - own):
            for r in own:
                isolated[r].append(meta["label_ja"])
    if not isolated:
        return
    n = sum(len(v) for v in isolated.values())
    # 1件ずつ並べると全件が並んで読めなくなるので、文化圏ごとの件数に畳む。
    findings.append({"kind": "no-cross-region", "about": "all",
                     "text": f"他の文化圏の movement と1本も繋がっていない movement が {n}/{total} 件。"
                             "時間だけでなく空間の広がりを体系化するので、影響・伝播・反発を調べる余地"})
    for region, names in sorted(isolated.items(), key=lambda x: -len(x[1])):
        findings.append({"kind": "no-cross-region", "about": region,
                         "text": f"{region}: {len(names)}件（{'、'.join(names[:4])}"
                                 f"{' ほか' if len(names) > 4 else ''}）"})


def render(findings):
    if not findings:
        return "食い違い・偏りの指摘はなし。"
    order = ["time-order", "type-mismatch", "kind-bias", "hypothesis", "dead-end", "no-cross-region"]
    label = {"time-order": "時間の矛盾", "type-mismatch": "型の食い違い", "kind-bias": "kind の地域偏り",
             "hypothesis": "仮説が未検証", "dead-end": "辿れない先",
             "no-cross-region": "文化圏を跨ぐ関係が無い"}
    lines = []
    for k in order:
        rows = [f for f in findings if f["kind"] == k]
        if rows:
            lines.append(f"**{label[k]}**")
            lines += [f"- {f['text']}" for f in rows]
            lines.append("")
    return "\n".join(lines).rstrip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    cfg = load_config()
    entities, _ = load_entities()
    region_history = load_region_history()
    edges = build_edges(entities)
    findings = []

    check_time_order(entities, edges, findings)
    check_grouped_as(entities, edges, findings)
    check_kind_bias(entities, cfg, findings, region_history)
    check_hypotheses(entities, cfg, findings, region_history)
    check_dangling_lineage(entities, edges, findings)
    check_cross_region_links(entities, edges, findings, region_history)

    print(render(findings))
    if not a.dry_run:
        OUT.parent.mkdir(exist_ok=True)
        OUT.write_text(json.dumps({"findings": findings}, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
        text = COVERAGE.read_text(encoding="utf-8")
        if MARK_START in text and MARK_END in text:
            head, rest = text.split(MARK_START, 1)
            _old, tail = rest.split(MARK_END, 1)
            COVERAGE.write_text(f"{head}{MARK_START}\n{render(findings)}\n{MARK_END}{tail}",
                                encoding="utf-8")
        else:
            print("overviews/coverage.md に監査の生成ブロックが無い", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
