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
  6. 文化圏間接続 — movement relation / diffused_to / active_in / exhibited_at→location の4経路を監査し、
     connected / reviewed-no-documented-link / unreviewed の3区分にする

これらは commit を止めない（壊れてはいないので）。**次に何を調べるかの材料として出す。**
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

from detail_baseline import BASELINE_PATH
from cross_region import (
    audit_cross_region,
    load_baseline,
    load_reviews,
    render_overview,
    validate_baseline,
    validate_reviews,
)
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


def check_cross_region_links(entities, edges, findings, region_history, cross_region=None):
    """4経路監査のunreviewed件数を既存audit findingsへ反映する。"""
    cross_region = cross_region or audit_cross_region(entities, region_history)
    unreviewed = cross_region["unreviewed"]
    if unreviewed:
        findings.append({"kind": "no-cross-region", "about": "all",
                         "text": f"4経路でconnectedにもreviewedにもなっていないmovementが "
                                 f"{len(unreviewed)}/{cross_region['movement_total']} 件"})


def check_detail_baseline(entities, findings):
    """baselineの代表movementにperson/workの証拠接続があるか監査する。"""
    if not BASELINE_PATH.exists():
        findings.append({"kind": "evidence-missing", "about": str(BASELINE_PATH),
                         "text": "詳細baseline manifestがない"})
        return
    try:
        manifest = yaml.safe_load(BASELINE_PATH.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        findings.append({"kind": "evidence-missing", "about": str(BASELINE_PATH),
                         "text": f"詳細baseline manifestを読めない: {exc}"})
        return
    for entry in manifest.get("entries") or []:
        movement_id = entry.get("movement") if isinstance(entry, dict) else None
        meta = entities.get(movement_id) or {}
        evidence = meta.get("evidence") or []
        if not evidence:
            findings.append({"kind": "evidence-missing", "about": movement_id,
                             "text": f"baseline movement {movement_id} にevidenceがない"})
            continue
        for item in evidence:
            if not isinstance(item, dict) or not item.get("target") or not item.get("supports"):
                findings.append({"kind": "evidence-missing", "about": movement_id,
                                 "text": f"baseline movement {movement_id} のevidenceが未充足"})


def render(findings, cross_region=None, baseline=None):
    if not findings:
        return "食い違い・偏りの指摘はなし。"
    order = ["time-order", "type-mismatch", "kind-bias", "hypothesis", "dead-end",
             "evidence-missing", "no-cross-region"]
    label = {"time-order": "時間の矛盾", "type-mismatch": "型の食い違い", "kind-bias": "kind の地域偏り",
             "hypothesis": "仮説が未検証", "dead-end": "辿れない先",
             "evidence-missing": "baselineの証拠不足",
             "no-cross-region": "文化圏を跨ぐ関係が無い"}
    lines = []
    for k in order:
        rows = [f for f in findings if f["kind"] == k]
        if rows:
            lines.append(f"**{label[k]}**")
            lines += [f"- {f['text']}" for f in rows]
            lines.append("")
    if cross_region is not None:
        lines += [render_overview(cross_region, baseline), ""]
    return "\n".join(lines).rstrip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    cfg = load_config()
    entities, _ = load_entities()
    region_history = load_region_history()
    edges = build_edges(entities)
    reviews, review_errors = load_reviews()
    baseline, baseline_errors = load_baseline()
    cross_region = audit_cross_region(entities, region_history, reviews)
    review_errors.extend(validate_reviews(reviews, entities, cross_region))
    baseline_errors.extend(validate_baseline(baseline, entities, cross_region))
    config_errors = review_errors + baseline_errors
    if config_errors:
        print("✗ cross-region audit config:", file=sys.stderr)
        for error in config_errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    baseline_report = dict(baseline)
    baseline_ids = set(baseline["movement_ids"])
    baseline_report["remaining_unreviewed"] = sorted(
        baseline_ids.intersection(cross_region["unreviewed"])
    )
    baseline_report["current_unreviewed"] = cross_region["unreviewed"]
    findings = []

    check_time_order(entities, edges, findings)
    check_grouped_as(entities, edges, findings)
    check_kind_bias(entities, cfg, findings, region_history)
    check_hypotheses(entities, cfg, findings, region_history)
    check_dangling_lineage(entities, edges, findings)
    check_detail_baseline(entities, findings)
    check_cross_region_links(entities, edges, findings, region_history, cross_region)

    print(render(findings, cross_region, baseline_report))
    if not a.dry_run:
        OUT.parent.mkdir(exist_ok=True)
        OUT.write_text(json.dumps({"schema_version": 1, "findings": findings,
                                   "cross_region": cross_region,
                                   "cross_region_baseline": baseline_report},
                                  ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
        text = COVERAGE.read_text(encoding="utf-8")
        if MARK_START in text and MARK_END in text:
            head, rest = text.split(MARK_START, 1)
            _old, tail = rest.split(MARK_END, 1)
            COVERAGE.write_text(
                f"{head}{MARK_START}\n{render(findings, cross_region, baseline_report)}\n{MARK_END}{tail}",
                                encoding="utf-8")
        else:
            print("overviews/coverage.md に監査の生成ブロックが無い", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
