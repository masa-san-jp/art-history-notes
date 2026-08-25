#!/usr/bin/env python3
"""境界へ出すための研究信号を書き出す（正準グラフは複製しない）。

    python3 tools/export_signals.py --purpose artistic-research
    python3 tools/export_signals.py --purpose artistic-research --entity movement/mannerism
    python3 tools/export_signals.py --purpose artistic-research --limit 5 --output signals.json

出すのは **安定IDと locator だけ** で、正準グラフ（graph.json のノード・エッジ本体）は複製しない。
親の `tools/adapters.py::adapt_art_history_signal` が受け取る境界DTOの形に合わせてある。

**解釈を含む関係だけを出す。** `influenced_by` / `derives_from` / `responds_to` / `reacts_against` /
`grouped_as` / `diffused_to` / `patronized_by` は、このKBが `certainty` と `source` を必須にしている
関係で、根拠と確度がそのまま境界へ運べる。構造的な関係（`created_by` 等）は確度の概念を持たないので
出さない——**「解釈を事実に変換しない」** という cross-repository-contract の禁止事項に当たるため。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from kb import ROOT, load_entities, normalize_reference, normalize_sources
except ModuleNotFoundError:  # tools.export_signals として読まれた場合
    from tools.kb import ROOT, load_entities, normalize_reference, normalize_sources

CONTRACT = "research-signal-export/v1"
ADAPTER_VERSION = "1.0.0"
SOURCE_REPOSITORY = "art-history"

# このKBが certainty と source を必須にしている関係（docs/schema.md「relations」）。
INTERPRETIVE = {
    "influenced_by", "derives_from", "responds_to", "reacts_against",
    "grouped_as", "diffused_to", "patronized_by",
}

# KB の certainty → 境界の certainty.level
CERTAINTY_LEVEL = {"attested": "observed", "scholarly": "inferred", "hypothesis": "inferred"}

# 美術史の事実は腐りにくいが、「腐らない」ではない。典拠IDの改訂・撤回・URL の消滅がある。
REVALIDATE_DAYS = 365


def _head_commit() -> str:
    status = subprocess.run(
        ["git", "-C", str(ROOT), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    if status:
        raise RuntimeError(
            "作業ツリーが dirty のため、HEAD を入力データの provenance として使えない"
        )
    return subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def _iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def _time_display(meta: dict) -> str:
    """時間軸は EDTF をそのまま渡す。表示用の原表記は落とす（境界では機械可読側だけ使う）。"""
    time = meta.get("time") or {}
    start, end = time.get("start"), time.get("end")
    if not start and not end:
        return "unspecified-time"
    return f"{start or 'unknown'}/{end or 'unknown'}"


def _origin_targets(meta: dict) -> list[str]:
    return [
        space["target"]
        for space in meta.get("space") or []
        if space.get("role") == "originated_in" and space.get("target")
    ]


def _geo(meta: dict, entities: dict) -> str:
    regions = []
    for target in _origin_targets(meta):
        place = entities.get(target) or {}
        region = place.get("region")
        if region and region not in regions:
            regions.append(region)
    return ",".join(regions) if regions else "unspecified-region"


def _relations(meta: dict) -> list[dict]:
    out = []
    for rel in meta.get("relations") or []:
        if rel.get("type") not in INTERPRETIVE:
            continue
        source = rel.get("source")
        if not source:
            continue  # 検証が通っていれば起きないが、根拠の無い解釈は出さない
        out.append({
            "target_entity_id": rel["target"],
            "relation": rel["type"],
            "certainty": {
                "level": CERTAINTY_LEVEL.get(rel.get("certainty"), "inferred"),
                "basis": f"このKBは解釈を含む関係に certainty と source を必須にしている（{rel.get('certainty')}）",
            },
            "evidence_refs": [source],
        })
    return out


def _source_details(meta: dict, relations: list[dict]) -> tuple[list[dict], list[dict]]:
    """source URLを正規化し、relationの参照にもkind/noteを添える。"""
    sources = normalize_sources(meta.get("sources") or [])
    by_url = {source.get("url"): source for source in sources if source.get("url")}
    evidence_sources = []
    for relation in relations:
        for url in relation.get("evidence_refs") or []:
            evidence_sources.append(by_url.get(url, normalize_reference(url)))
    return sources, evidence_sources


def build_record(meta: dict, entities: dict, commit: str, now: datetime, purpose: str) -> dict | None:
    """1つの movement を境界DTOへ変換する。解釈関係が無いものは None（出さない）。"""
    relations = _relations(meta)
    if not relations:
        return None
    sources, evidence_sources = _source_details(meta, relations)

    slug = meta["id"].split("/", 1)[1]
    unknowns = []
    if not (meta.get("time") or {}).get("start"):
        unknowns.append("開始時期を単一のEDTF値に確定できていない（time.display に幅と根拠がある）")
    verified = meta.get("status") == "verified"
    if not verified:
        unknowns.append(f"status は {meta.get('status')} であり、verified ではない（項目ごとの根拠付けが未完）")
    origin_targets = _origin_targets(meta)
    if not origin_targets:
        unknowns.append("発生地を特定できていない")
    elif len(origin_targets) > 1:
        unknowns.append(
            "発生地が複数あるため、起源entityを保持する: "
            + ", ".join(origin_targets)
        )

    return {
        "signal_id": f"art-history:{slug}",
        "repository": SOURCE_REPOSITORY,
        "commit": commit,
        "entity_id": meta["id"],
        "source_locator": meta["path"],
        "evidence_locator": f"{meta['path']}#sources",
        "sources": sources,
        "evidence_sources": evidence_sources,
        # 出典の種類。このKBの本文は大半を「二次情報」と明記しており、一次資料への到達は
        # 各ファイルの「未着手」に残っている状態なので、既定は secondary にする。
        # 一次・二次を frontmatter で機械可読に持っていないため、ここで個別判定はしない。
        "evidence_kind": "secondary",
        "statement": f"{meta.get('label_ja')}（{meta.get('label_en')}）は "
                     f"{len(relations)} 件の解釈的関係を根拠付きで持つ",
        "certainty": {
            "level": "observed" if verified else "inferred",
            "basis": f"kind={meta.get('kind')} / status={meta.get('status')}。"
                     "関係ごとの根拠は relations[].evidence_refs にある",
        },
        "unknowns": unknowns or ["この括りの未着手事項は本文の「未着手」節にある"],
        "constraints": [
            f"{purpose} の目的内でのみ利用する",
            "解釈を含む関係を事実の関係へ変換しない",
            "正準グラフは複製せず、安定IDと locator で参照する",
        ],
        "validity": {
            "status": "valid" if verified else "unknown",
            "checked_at": _iso(now),
        },
        "freshness": {
            "status": "current",
            "retrieved_at": _iso(now),
            "revalidate_at": _iso(now + timedelta(days=REVALIDATE_DAYS)),
        },
        "generated_at": _iso(now),
        "adapter_version": ADAPTER_VERSION,
        "entity_kind": meta.get("kind") or "movement",
        "time": _time_display(meta),
        "geo": _geo(meta, entities),
        "relations": relations,
        "canonical_graph_locator": f"data/graph.json#{meta['id']}",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="境界へ出す研究信号を書き出す")
    ap.add_argument("--purpose", required=True)
    ap.add_argument("--entity", help="1件だけ出す（例: movement/mannerism）")
    ap.add_argument("--limit", type=int, default=0, help="0 なら全件")
    ap.add_argument("--output", help="書き出し先。省略時は標準出力")
    args = ap.parse_args()

    entities, _records = load_entities()
    if args.entity and args.entity not in entities:
        print(f"ERROR: そのIDは無い: {args.entity}", file=sys.stderr)
        return 1

    try:
        commit = _head_commit()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    now = datetime.now(timezone(timedelta(hours=9))).replace(microsecond=0)

    targets = [entities[args.entity]] if args.entity else [
        meta for meta in entities.values() if meta.get("type") == "movement"
    ]

    records = []
    for meta in sorted(targets, key=lambda m: m["id"]):
        record = build_record(meta, entities, commit, now, args.purpose)
        if record:
            records.append(record)
        if args.limit and len(records) >= args.limit:
            break

    payload = {
        "contract_version": CONTRACT,
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": commit,
        "purpose": args.purpose,
        "generated_at": _iso(now),
        "signal_count": len(records),
        "signals": records,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"{len(records)} 件を書き出した -> {args.output}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
