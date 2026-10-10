#!/usr/bin/env python3
"""境界へ出すための研究信号を書き出す（正準グラフは複製しない）。

    python3 tools/export_signals.py --purpose artistic-research
    python3 tools/export_signals.py --purpose artistic-research --entity movement/mannerism
    python3 tools/export_signals.py --purpose artistic-research --limit 5 --output signals.json

正準グラフ（graph.json のノード・エッジ本体）は複製しない。
出典付きの method concept は、候補の種に必要な method 記述と source_refs も境界へ出す。
親の `tools/adapters.py::adapt_art_history_signal` が受け取る境界DTOの形に合わせてある。

**関係は解釈を含むものだけを出す。** `influenced_by` / `derives_from` / `responds_to` / `reacts_against` /
`grouped_as` / `diffused_to` / `patronized_by` / `uses_method` は、このKBが `certainty` と `source` を必須にしている
関係で、根拠と確度がそのまま境界へ運べる。構造的な関係（`created_by` 等）は確度の概念を持たないので
出さない——**「解釈を事実に変換しない」** という cross-repository-contract の禁止事項に当たるため。
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from kb import ROOT, is_http_url, load_entities, normalize_reference, normalize_sources
    from agent_support import is_immutable_archive, resolve_code_commit
except ModuleNotFoundError:  # tools.export_signals として読まれた場合
    from tools.kb import ROOT, is_http_url, load_entities, normalize_reference, normalize_sources
    from tools.agent_support import is_immutable_archive, resolve_code_commit

CONTRACT = "research-signal-export/v1"
ADAPTER_VERSION = "1.1.0"
CONTENT_MAX_CHARS = 2400
SOURCE_REPOSITORY = "art-history"

# このKBが certainty と source を必須にしている関係（docs/schema.md「relations」）。
INTERPRETIVE = {
    "influenced_by", "derives_from", "responds_to", "reacts_against",
    "grouped_as", "diffused_to", "patronized_by", "uses_method",
}

# KB の certainty → 境界の certainty.level
CERTAINTY_LEVEL = {"attested": "observed", "scholarly": "inferred", "hypothesis": "inferred"}

# 美術史の事実は腐りにくいが、「腐らない」ではない。典拠IDの改訂・撤回・URL の消滅がある。
REVALIDATE_DAYS = 365


def _head_commit() -> str:
    status_result = subprocess.run(
        ["git", "-C", str(ROOT), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    )
    status = status_result.stdout.strip()
    if status:
        raise RuntimeError(
            "作業ツリーが dirty のため、HEAD を入力データの provenance として使えない"
        )
    if status_result.returncode and not is_immutable_archive(ROOT):
        raise RuntimeError(status_result.stderr.strip() or "git status failed")
    return resolve_code_commit(ROOT)


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


def _method(meta: dict) -> dict | None:
    """出典付きの draft 以上の method concept だけを境界へ出す。"""
    if meta.get("type") != "concept" or meta.get("status") not in {"draft", "verified"}:
        return None
    method = meta.get("method")
    if not isinstance(method, dict):
        return None
    for field in ("fixes", "varies", "requires"):
        values = method.get(field)
        if not isinstance(values, list) or not values or any(
            not isinstance(value, str) or not value.strip() for value in values
        ):
            return None
    origin = method.get("origin_domain")
    if not isinstance(origin, str) or not origin.strip():
        return None
    if not any(is_http_url(source.get("url"))
               for source in normalize_sources(meta.get("sources") or [])):
        return None
    return {field: list(method[field]) for field in ("fixes", "varies", "requires")} | {"origin_domain": origin}


def entity_content(meta: dict, body: str = "") -> list[dict]:
    """Bounded verbatim excerpts, never a generated summary or an uncited section.

    Prose paragraphs need their own explicit URL in the entity's sources. A
    directly following quotation inherits that paragraph's citation. Method
    fields use the existing owner contract's declared source_refs.
    """
    sources = sorted({s["url"] for s in normalize_sources(meta.get("sources") or [])
                      if is_http_url(s.get("url"))})
    remaining = CONTENT_MAX_CHARS
    content = []

    def append(text, refs, locator):
        nonlocal remaining
        if remaining and text and refs:
            text = text[:remaining]
            content.append({"text": text, "source_refs": refs, "source_locator": locator})
            remaining -= len(text)

    method = _method(meta)
    if method:
        for field in ("fixes", "varies", "requires"):
            for text in method[field]:
                append(text, sources, f"{meta['path']}#method.{field}")
    sections = re.split(r"(?m)^#{1,6}\s+([^\n]+)\n", body)
    for index in range(1, len(sections), 2):
        heading, prose = sections[index:index + 2]
        if not re.match(r"定義|方法|手法|技法|態度|特徴|実装例", heading):
            continue
        citation = []
        for paragraph in re.split(r"\n\s*\n", prose.strip()):
            urls = set(re.findall(r'\]\((https?://[^\s]+?)\)', paragraph))
            urls.update(re.findall(r'https?://[^\s<>()]+', paragraph))
            refs = sorted(set(sources) & urls)
            if refs:
                citation = refs
            elif not paragraph.startswith(">"):
                citation = []
            append(paragraph, refs or citation, f"{meta['path']}#{heading}")
    return content


def build_record(meta: dict, entities: dict, commit: str, now: datetime, purpose: str,
                 body: str = "", *, operation_tags: list | None = None,
                 operation_vocabulary: dict | None = None, card: list | None = None) -> dict | None:
    """既存の関係信号、または出典付き method concept を境界DTOへ変換する。"""
    method = _method(meta)
    if meta.get("type") == "concept" and "method" in meta and method is None:
        return None  # 宣言された方法が未記入・無出典なら関係経路へ迂回しない
    relations = _relations(meta)
    content = entity_content(meta, body)
    if not relations and method is None and not content and not operation_tags and not card:
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

    record = {
        "signal_id": f"art-history:method:{slug}" if method else f"art-history:{slug}",
        "repository": SOURCE_REPOSITORY,
        "commit": commit,
        "entity_id": meta["id"],
        "entity_labels": [value for value in (meta.get('label_ja'), meta.get('label_en'))
                          if isinstance(value, str) and value.strip()],
        "source_locator": meta["path"],
        "evidence_locator": f"{meta['path']}#sources",
        "sources": sources,
        "evidence_sources": evidence_sources,
        "images": [dict(image) for image in meta.get("images") or [] if isinstance(image, dict)],
        # 出典の種類。このKBの本文は大半を「二次情報」と明記しており、一次資料への到達は
        # 各ファイルの「未着手」に残っている状態なので、既定は secondary にする。
        # 一次・二次を frontmatter で機械可読に持っていないため、ここで個別判定はしない。
        "evidence_kind": "secondary",
        "statement": (f"{meta.get('label_ja')}（{meta.get('label_en')}）は出典付きの方法記述を持つ"
                      if method else f"{meta.get('label_ja')}（{meta.get('label_en')}）は "
                      f"{len(relations)} 件の解釈的関係を根拠付きで持つ"),
        "certainty": {
            "level": "observed" if verified else "inferred",
            "basis": f"kind={meta.get('kind')} / status={meta.get('status')}。"
                     + ("方法記述の根拠は source_refs にある。美術への適用・歴史的影響は認定しない"
                        if method else "関係ごとの根拠は relations[].evidence_refs にある"),
        },
        "unknowns": unknowns or ["この括りの未着手事項は本文の「未着手」節にある"],
        "constraints": [
            f"{purpose} の目的内でのみ利用する",
            "解釈を含む関係を事実の関係へ変換しない",
            ("正準グラフや出典本文は複製せず、方法記述と安定IDと locator で参照する"
             if method else "正準グラフは複製せず、安定IDと locator で参照する"),
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
        "entity_kind": "concept" if method else meta.get("kind") or "movement",
        "time": _time_display(meta),
        "geo": _geo(meta, entities),
        "relations": relations,
        "canonical_graph_locator": f"data/graph.json#{meta['id']}",
    }
    if content:
        record["content"] = content
    if operation_vocabulary is not None:
        record["operation_vocabulary"] = operation_vocabulary
        record["operation_tags"] = operation_tags or []
    if card is not None:
        record["card"] = card
    if method:
        record["method"] = method
        record["source_refs"] = sorted({source["url"] for source in sources
                                        if is_http_url(source.get("url"))})
        # evidence_sources は関係の根拠。方法の出典は source_refs に分けて保持する。
        record["constraints"].append("方法の起源領域は美術への適用・歴史的影響の証明ではない")
    return record


def main() -> int:
    ap = argparse.ArgumentParser(description="境界へ出す研究信号を書き出す")
    ap.add_argument("--purpose", required=True)
    ap.add_argument("--entity", help="1件だけ出す（例: movement/mannerism）")
    ap.add_argument("--limit", type=int, default=0, help="0 なら全件")
    ap.add_argument("--output", help="書き出し先。省略時は標準出力")
    ap.add_argument("--knowledge-store-root", type=Path)
    ap.add_argument("--creator")
    ap.add_argument("--collection")
    ap.add_argument("--code-commit")
    ap.add_argument("--knowledge-commit")
    ap.add_argument("--query", default="")
    ap.add_argument("--at")
    ap.add_argument("--access-scope", choices=["public", "creator-private"], default="creator-private")
    args = ap.parse_args()

    if args.knowledge_store_root:
        from research_knowledge_intake import KnowledgeStore
        try:
            if not all((args.creator, args.collection, args.code_commit, args.knowledge_commit, args.at)):
                raise ValueError("explicit creator, collection, code/knowledge commits and time required")
            at = datetime.fromisoformat(args.at.replace("Z", "+00:00"))
            if at.tzinfo is None: raise ValueError("timezone required")
            store = KnowledgeStore(args.knowledge_store_root, args.creator, args.collection, args.code_commit)
            result = store.retrieve(args.knowledge_commit, args.query, args.access_scope, at)
            result.update(contract_version="art-history-knowledge-export/v1", purpose=args.purpose,
                          code_commit=args.code_commit, knowledge_commit=args.knowledge_commit)
            text = json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n"
            if args.output: Path(args.output).write_text(text, encoding="utf-8")
            else: sys.stdout.write(text)
            return 0
        except (OSError, ValueError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

    entities, source_records = load_entities()
    bodies = {meta["id"]: body for _path, meta, body in source_records}
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
        meta for meta in entities.values()
        if meta.get("type") == "movement" or _method(meta) is not None
    ]

    from operation_tags import vocabulary, validated_bundle
    from card_excerpts import build_cards
    vocab = vocabulary()
    tags = validated_bundle(source_records)
    try:
        cards, card_missing = build_cards(source_records, tags, commit)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:  # CARD_SOURCE_MISMATCH などは黙って捨てず止める
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    records = []
    # 既存の --limit は movement の ID 順を保ち、その後に方法を追加する。
    for meta in sorted(targets, key=lambda m: (m.get("type") != "movement", m["id"])):
        record = build_record(meta, entities, commit, now, args.purpose, bodies.get(meta["id"], ""),
                              operation_tags=tags["records"].get(meta["id"], {}).get("tags"),
                              operation_vocabulary=vocab if meta["id"] in tags["records"] else None,
                              card=cards.get(meta["id"], [] if meta["id"] in card_missing else None))
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
        # 本文もタグも無くカードを作れない項目。名前だけで埋めず ID を残す。
        "card_missing": sorted(set(card_missing) & {r["entity_id"] for r in records}),
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
