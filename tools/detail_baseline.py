"""13文化圏の詳細解説baselineを選定・検証する共通ロジック。"""

from __future__ import annotations

from pathlib import Path

import yaml

from kb import ROOT, load_region_history, read_frontmatter, regions_of


BASELINE_PATH = ROOT / "config" / "detail-baseline-v1.yaml"
PD_LICENSES = {"public-domain", "cc0", "pdm"}
SOURCE_COMMIT = "1c0c1734e97f3c56c58a90ba93bc02638a62b947"


def work_targets(entities, movement_id):
    """movementに直接belongs_toされるwork、またはmovementから直接張られたwork。"""
    targets = set()
    movement = entities.get(movement_id) or {}
    for relation in movement.get("relations") or []:
        target = relation.get("target")
        if target in entities and entities[target].get("type") == "work":
            targets.add(target)
    for entity_id, meta in entities.items():
        if meta.get("type") != "work":
            continue
        if any(relation.get("target") == movement_id
               for relation in meta.get("relations") or []):
            targets.add(entity_id)
    return sorted(targets)


def has_pd_image(meta):
    return any(
        isinstance(image, dict)
        and image.get("license") in PD_LICENSES
        and image.get("url")
        and image.get("source_page")
        for image in meta.get("images") or []
    )


def select_baseline(entities, config, region_history=None):
    """Issue #361の決定順でregionごとのmovementを1件ずつ選ぶ。"""
    history = region_history if region_history is not None else load_region_history()
    movements = [
        (entity_id, meta) for entity_id, meta in entities.items()
        if meta.get("type") == "movement" and meta.get("status") != "stub"
    ]
    selected = {}
    for region in config.get("buckets") or {}:
        candidates = []
        for entity_id, meta in movements:
            if region not in regions_of(entity_id, entities, history):
                continue
            targets = work_targets(entities, entity_id)
            score = (
                1 if targets else 0,
                1 if has_pd_image(meta) else 0,
                len(meta.get("sources") or []),
            )
            candidates.append((score, entity_id))
        if candidates:
            candidates.sort(key=lambda row: (-row[0][0], -row[0][1], -row[0][2], row[1]))
            selected[region] = candidates[0]
    return {region: value[1] for region, value in selected.items()}


def validate_manifest(entities, config, path=BASELINE_PATH, region_history=None):
    """manifestの形式・選定結果・代表work接続を検証する。"""
    errors = []
    path = Path(path)
    if not path.exists():
        return [f"{path.relative_to(ROOT)}: manifestがない"]
    try:
        manifest = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        return [f"{path.relative_to(ROOT)}: manifestを読めない: {exc}"]
    if manifest.get("source_commit") != SOURCE_COMMIT:
        errors.append(f"{path.relative_to(ROOT)}: source_commitは基準commit {SOURCE_COMMIT} にする")
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return errors + [f"{path.relative_to(ROOT)}: entriesは配列が必要"]
    expected = select_baseline(entities, config, region_history)
    actual_regions = []
    for index, entry in enumerate(entries, start=1):
        prefix = f"{path.relative_to(ROOT)}: entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix}はmapが必要")
            continue
        region = entry.get("region")
        movement = entry.get("movement")
        work = entry.get("work")
        actual_regions.append(region)
        if region not in (config.get("buckets") or {}):
            errors.append(f"{prefix}: 未知のregion {region}")
        elif expected.get(region) != movement:
            errors.append(f"{prefix}: 選定結果は {expected.get(region)}（今: {movement}）")
        movement_meta = entities.get(movement)
        if not movement_meta or movement_meta.get("type") != "movement":
            errors.append(f"{prefix}: movementは存在するmovement IDが必要")
        elif region not in regions_of(movement, entities, region_history):
            errors.append(f"{prefix}: movementがregionに属さない: {region}")
        work_meta = entities.get(work)
        if not work_meta or work_meta.get("type") != "work":
            errors.append(f"{prefix}: workは存在するwork IDが必要")
        elif work not in work_targets(entities, movement):
            errors.append(f"{prefix}: workとmovementの既存relationがない")
        elif "## どう成立しているか" not in read_frontmatter(ROOT / work_meta["path"])[1]:
            errors.append(f"{prefix}: work本文に ## どう成立しているか がない")
    if sorted(actual_regions) != sorted(set(actual_regions)):
        errors.append(f"{path.relative_to(ROOT)}: regionが重複している")
    if set(actual_regions) != set(config.get("buckets") or {}):
        errors.append(f"{path.relative_to(ROOT)}: 13regionを各1件で埋める")
    return errors
