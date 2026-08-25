#!/usr/bin/env python3
"""movementの文化圏間接続を4つの明示的な経路だけで監査する。"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import yaml

from kb import edtf_year_range, is_http_url, regions_of

REVIEW_PATH = Path(__file__).resolve().parents[1] / "config" / "cross-region-reviews.yaml"
REVIEW_STATUS = "no-documented-cross-region-relation"
ROUTE_KINDS = {
    "movement-relation",
    "diffused-to-place",
    "active-in-place",
    "exhibited-at-place",
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _period_matches(year_range, entries):
    lo, hi = year_range
    if lo is None or hi is None:
        return []
    matches = []
    for entry in entries or []:
        start, _ = edtf_year_range(entry.get("start"))
        end, _ = edtf_year_range(entry.get("end"))
        if start is not None and hi < start:
            continue
        if end is not None and lo >= end:
            continue
        matches.append(entry)
    return matches


def place_regions(place_id, at_meta, entities, region_history):
    """場所を、対象movementの開始時点に対応するregionへ解決する。"""
    place = entities.get(place_id) or {}
    entries = (region_history or {}).get(place_id) or []
    matches = _period_matches(
        edtf_year_range((at_meta.get("time") or {}).get("start")),
        entries,
    )
    regions = [entry.get("region") for entry in matches if entry.get("region")]
    if not regions and place.get("region"):
        regions = [place["region"]]
    return list(dict.fromkeys(regions))


def _edge(from_id, edge_type, target, **extra):
    edge = {"from": from_id, "type": edge_type, "to": target}
    for key, value in extra.items():
        if value is not None:
            edge[key] = value
    return edge


def _route(kind, edges, destination_regions):
    return {
        "kind": kind,
        "edges": edges,
        "destination_regions": sorted(set(destination_regions)),
    }


def _movement_routes(movement_id, movement, entities, region_history):
    """1 movementから到達する4経路のうち、originと異なるものだけを返す。"""
    origin_regions = set(regions_of(movement_id, entities, region_history))
    routes = []

    # 1. movement -> movement relation
    for relation in movement.get("relations") or []:
        target_id = relation.get("target")
        target = entities.get(target_id) or {}
        if target.get("type") != "movement":
            continue
        destination = regions_of(target_id, entities, region_history)
        if set(destination) - origin_regions:
            routes.append(_route(
                "movement-relation",
                [_edge(movement_id, relation.get("type"), target_id,
                       certainty=relation.get("certainty"), source=relation.get("source"))],
                destination,
            ))

    # 2. movement -> place diffused_to
    for relation in movement.get("relations") or []:
        if relation.get("type") != "diffused_to":
            continue
        place_id = relation.get("target")
        if (entities.get(place_id) or {}).get("type") != "place":
            continue
        destination = place_regions(place_id, movement, entities, region_history)
        if set(destination) - origin_regions:
            routes.append(_route(
                "diffused-to-place",
                [_edge(movement_id, "diffused_to", place_id,
                       certainty=relation.get("certainty"), source=relation.get("source"))],
                destination,
            ))

    # 3. movement.space.active_in
    for space in movement.get("space") or []:
        if space.get("role") != "active_in":
            continue
        place_id = space.get("target")
        if (entities.get(place_id) or {}).get("type") != "place":
            continue
        destination = place_regions(place_id, movement, entities, region_history)
        if set(destination) - origin_regions:
            routes.append(_route(
                "active-in-place",
                [_edge(movement_id, "active_in", place_id)],
                destination,
            ))

    # 4. movement -> event/org exhibited_at -> held_at/sited_in place
    for relation in movement.get("relations") or []:
        if relation.get("type") != "exhibited_at":
            continue
        venue_id = relation.get("target")
        venue = entities.get(venue_id) or {}
        if venue.get("type") not in {"event", "org"}:
            continue
        location_role = "held_at" if venue.get("type") == "event" else "sited_in"
        for location in venue.get("space") or []:
            if location.get("role") != location_role:
                continue
            place_id = location.get("target")
            if (entities.get(place_id) or {}).get("type") != "place":
                continue
            destination = place_regions(place_id, movement, entities, region_history)
            if set(destination) - origin_regions:
                routes.append(_route(
                    "exhibited-at-place",
                    [
                        _edge(movement_id, "exhibited_at", venue_id,
                              certainty=relation.get("certainty"), source=relation.get("source")),
                        _edge(venue_id, location_role, place_id),
                    ],
                    destination,
                ))

    routes.sort(key=lambda route: (
        route["kind"],
        [(edge.get("from"), edge.get("type"), edge.get("to")) for edge in route["edges"]],
        route["destination_regions"],
    ))
    return routes


def load_reviews(path=REVIEW_PATH):
    path = Path(path)
    if not path.exists():
        return [], [f"{path}: review configがない"]
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        return [], [f"{path}: review configを読めない: {exc}"]
    reviews = data.get("reviews")
    if not isinstance(reviews, list):
        return [], [f"{path}: reviewsは配列が必要"]
    return reviews, []


def audit_cross_region(entities, region_history=None, reviews=None):
    movements = {
        entity_id: meta for entity_id, meta in entities.items()
        if meta.get("type") == "movement"
    }
    review_by_id = {
        item.get("movement_id"): item for item in (reviews or [])
        if isinstance(item, dict) and item.get("movement_id")
    }
    rows = []
    for movement_id in sorted(movements):
        movement = movements[movement_id]
        origin_regions = sorted(set(regions_of(movement_id, entities, region_history)))
        routes = _movement_routes(movement_id, movement, entities, region_history)
        if routes:
            status = "connected"
            reason = [f"{len(routes)}経路で起源region外へ到達"]
            review = None
        elif movement_id in review_by_id:
            status = "reviewed-no-documented-link"
            review = review_by_id[movement_id]
            reason = [review["note"]]
        else:
            status = "unreviewed"
            review = None
            reason = ["4経路に起源region外への到達がなく、cross-region reviewもない"]
        rows.append({
            "movement_id": movement_id,
            "status": status,
            "origin_regions": origin_regions,
            "routes": routes,
            "reasons": reason,
            "review": review,
        })

    groups = {
        status: [row["movement_id"] for row in rows if row["status"] == status]
        for status in ("connected", "reviewed-no-documented-link", "unreviewed")
    }
    return {
        "schema_version": 1,
        "movement_total": len(rows),
        "counts": {status: len(groups[status]) for status in groups},
        "connected": groups["connected"],
        "reviewed_no_documented_link": groups["reviewed-no-documented-link"],
        "unreviewed": groups["unreviewed"],
        "movements": rows,
    }


def validate_reviews(reviews, entities, audit):
    errors = []
    movement_ids = {entity_id for entity_id, meta in entities.items()
                    if meta.get("type") == "movement"}
    connected = set(audit.get("connected") or [])
    seen = set()
    for index, review in enumerate(reviews, start=1):
        prefix = f"config/cross-region-reviews.yaml: reviews[{index}]"
        if not isinstance(review, dict):
            errors.append(f"{prefix}はobjectが必要")
            continue
        movement_id = review.get("movement_id")
        if movement_id in seen:
            errors.append(f"{prefix}: movement_idが重複: {movement_id}")
        seen.add(movement_id)
        if movement_id not in movement_ids:
            errors.append(f"{prefix}: 存在しないmovement_id: {movement_id}")
        if review.get("status") != REVIEW_STATUS:
            errors.append(f"{prefix}: statusは{REVIEW_STATUS}固定")
        checked = review.get("checked")
        valid_checked = False
        if isinstance(checked, str) and DATE_RE.fullmatch(checked):
            try:
                date.fromisoformat(checked)
                valid_checked = True
            except ValueError:
                pass
        if not valid_checked:
            errors.append(f"{prefix}: checkedはYYYY-MM-DDが必要")
        note = review.get("note")
        if not isinstance(note, str) or not note.strip():
            errors.append(f"{prefix}: noteは空でない文字列が必要")
        sources = review.get("sources")
        if not isinstance(sources, list) or len(sources) < 2:
            errors.append(f"{prefix}: sourcesはhttp(s) URL 2件以上が必要")
        elif any(not is_http_url(source) for source in sources):
            errors.append(f"{prefix}: sourcesはhttp(s) URLだけが必要")
        if movement_id in connected:
            errors.append(f"{prefix}: 既にconnectedなmovementはreviewできない: {movement_id}")
    return errors


def render_overview(audit):
    counts = audit["counts"]
    lines = [
        "**文化圏間接続監査（4経路）**",
        f"- connected: {counts['connected']}件",
        f"- reviewed-no-documented-link: {counts['reviewed-no-documented-link']}件",
        f"- unreviewed: {counts['unreviewed']}件",
    ]
    if audit["unreviewed"]:
        lines.append("- unreviewed ID: " + ", ".join(f"`{item}`" for item in audit["unreviewed"]))
    return "\n".join(lines)
