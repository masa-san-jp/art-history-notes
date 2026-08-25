#!/usr/bin/env python3
"""119 movementのverified化を、固定manifestと段階gateで監査する。"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from kb import is_http_url, regions_of

ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "config" / "verified-movement-baseline-v1.yaml"
SCHEMA_VERSION = 1
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
TARGET_FIELDS = ("time", "originated_in", "origin_unknown", "kind")
ORIGIN_FIELDS = {"originated_in", "origin_unknown"}
EVIDENCE_KINDS = {"primary", "scholarly", "institutional"}


def load_manifest(path=BASELINE_PATH):
    path = Path(path)
    if not path.exists():
        return {}, [f"{path}: verified movement baselineがない"]
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        return {}, [f"{path}: verified movement baselineを読めない: {exc}"]
    if not isinstance(data, dict):
        return {}, [f"{path}: baselineはobjectが必要"]
    return data, []


def _is_wikidata(url):
    return "wikidata.org" in (url or "").lower()


def _source_index(meta):
    return {
        item.get("url"): item
        for item in (meta.get("sources") or [])
        if isinstance(item, dict) and item.get("url")
    }


def _claim_errors(movement_id, meta):
    prefix = movement_id
    errors = []
    claims = meta.get("claims") or []
    by_field = {field: [] for field in TARGET_FIELDS}
    source_index = _source_index(meta)
    for claim in claims:
        if isinstance(claim, dict) and claim.get("field") in by_field:
            by_field[claim["field"]].append(claim)

    for field in ("time", "kind"):
        if not by_field[field]:
            errors.append(f"{prefix}: {field} claimがない")
    origins = [claim for field in ORIGIN_FIELDS for claim in by_field[field]]
    if len(origins) != 1:
        errors.append(f"{prefix}: originated_in / origin_unknown claimは排他的に1件必要")
    if by_field["origin_unknown"] and any(
            item.get("role") == "originated_in" for item in (meta.get("space") or [])):
        errors.append(f"{prefix}: origin_unknownとspace.originated_inを併記できない")
    if by_field["originated_in"] and not any(
            item.get("role") == "originated_in" for item in (meta.get("space") or [])):
        errors.append(f"{prefix}: originated_in claimにはspace.originated_inが必要")

    for field in TARGET_FIELDS:
        for claim in by_field[field]:
            source = claim.get("source")
            if not is_http_url(source) or source not in source_index:
                errors.append(f"{prefix}: {field} claimのsourceが親sourcesにない: {source}")
                continue
            if claim.get("certainty") == "hypothesis":
                errors.append(f"{prefix}: {field} claimにhypothesisを使えない")
            if _is_wikidata(source):
                errors.append(f"{prefix}: {field} claimをWikidataだけにできない")
            if source_index[source].get("kind") not in EVIDENCE_KINDS:
                errors.append(
                    f"{prefix}: {field} claimのsource kindはprimary/scholarly/institutionalが必要: "
                    f"{source}"
                )
    return errors


def _manifest_shape_errors(manifest, entities):
    errors = []
    prefix = "config/verified-movement-baseline-v1.yaml"
    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"{prefix}: schema_versionは{SCHEMA_VERSION}固定")
    commit = manifest.get("source_commit")
    if not isinstance(commit, str) or not COMMIT_RE.fullmatch(commit):
        errors.append(f"{prefix}: source_commitは40桁の小文字hexが必要")
    if not isinstance(manifest.get("enforce_complete"), bool):
        errors.append(f"{prefix}: enforce_completeはboolが必要")
    ids = manifest.get("movement_ids")
    if not isinstance(ids, list) or any(not isinstance(item, str) for item in ids):
        errors.append(f"{prefix}: movement_idsは文字列配列が必要")
        ids = []
    if manifest.get("movement_count") != len(ids):
        errors.append(f"{prefix}: movement_countとmovement_idsの件数が不一致")
    if len(set(ids)) != len(ids):
        errors.append(f"{prefix}: movement_idsに重複がある")
    if ids != sorted(ids):
        errors.append(f"{prefix}: movement_idsは辞書順で固定する")
    for movement_id in ids:
        if (entities.get(movement_id) or {}).get("type") != "movement":
            errors.append(f"{prefix}: 存在しないmovement_id: {movement_id}")
    return errors


def audit_manifest(manifest, entities):
    """manifestを検証し、段階進捗と未完了IDを返す。"""
    errors = _manifest_shape_errors(manifest, entities)
    ids = [item for item in manifest.get("movement_ids") or [] if isinstance(item, str)]
    verified = []
    incomplete = []
    for movement_id in ids:
        meta = entities.get(movement_id) or {}
        if meta.get("status") == "verified":
            verified.append(movement_id)
            errors.extend(_claim_errors(movement_id, meta))
        else:
            incomplete.append(movement_id)
    if manifest.get("enforce_complete") is True and incomplete:
        errors.append(
            "config/verified-movement-baseline-v1.yaml: enforce_complete=trueだが未完了: "
            + ", ".join(incomplete)
        )
    by_region = {}
    for movement_id in ids:
        for region in regions_of(movement_id, entities):
            by_region[region] = by_region.get(region, 0) + 1
    return {
        "schema_version": SCHEMA_VERSION,
        "source_commit": manifest.get("source_commit"),
        "movement_total": len(ids),
        "verified": len(verified),
        "incomplete": incomplete,
        "enforce_complete": manifest.get("enforce_complete"),
        "by_region": dict(sorted(by_region.items())),
    }, errors


def validate_transition(previous, current):
    """完了gateを一度trueにしたmanifestをfalseへ戻さない。"""
    if previous.get("enforce_complete") is True and current.get("enforce_complete") is not True:
        return ["verified movement baseline: enforce_complete=trueからの退行は禁止"]
    return []


def render_progress(report):
    lines = [
        "基準movementの根拠付きverified化:",
        f"- verified: {report['verified']}/{report['movement_total']}",
        f"- enforce_complete: {str(report['enforce_complete']).lower()}",
    ]
    if report["incomplete"]:
        lines.append("- 未完了: " + ", ".join(f"`{item}`" for item in report["incomplete"]))
    return "\n".join(lines)
