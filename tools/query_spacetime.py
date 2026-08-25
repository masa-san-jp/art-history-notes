#!/usr/bin/env python3
"""時間×空間でエンティティを問い合わせる（graph.jsonは読み取り専用）。

    uv run --locked python tools/query_spacetime.py --at 1885
    uv run --locked python tools/query_spacetime.py --from 1880 --to 1890 \
        --regions europe-west asia-east-japan
    uv run --locked python tools/query_spacetime.py --at 1885 \
        --near place/paris --radius-km 500 --format json

この結果は同時代の候補を返すだけで、因果関係や類似性を主張せず、graph.jsonにもedgeを追加しない。
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from kb import (ROOT, TYPES, edtf_year_range, load_config, load_region_history)


EARTH_RADIUS_KM = 6371.0088
SPACE_ROLES_BY_TYPE = {
    "movement": {"originated_in"},
    "person": {"active_in", "born_in", "died_in"},
    "work": {"created_in"},
    "org": {"active_in", "sited_in"},
    "concept": {"active_in"},
    "event": {"held_at"},
    "source": {"active_in", "held_at", "sited_in"},
}


def load_graph(path=None):
    """生成済みgraph.jsonからentity mapだけを読む。"""
    graph_path = Path(path) if path else ROOT / "data" / "graph.json"
    payload = json.loads(graph_path.read_text(encoding="utf-8"))
    entities = payload.get("entities")
    if not isinstance(entities, dict):
        raise ValueError("graph.json の entities がmapではない")
    return entities


def haversine_km(first, second):
    """緯度経度2点間の大円距離をkmで返す。"""
    lat1, lon1 = first
    lat2, lon2 = second
    lat1, lon1, lat2, lon2 = map(math.radians, (lat1, lon1, lat2, lon2))
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    value = (math.sin(delta_lat / 2) ** 2
             + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2)
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(value))


def _coordinates(meta):
    coordinates = meta.get("coordinates")
    if not isinstance(coordinates, list) or len(coordinates) != 2:
        return None
    if any(isinstance(value, bool) or not isinstance(value, (int, float))
           or not math.isfinite(value) for value in coordinates):
        return None
    return coordinates


def _entity_time_range(meta):
    """entityのtimeを、既知の包含範囲として返す。不明端はNone。"""
    time = meta.get("time")
    if not isinstance(time, dict):
        return None
    start_lo, _start_hi = edtf_year_range(time.get("start"))
    if start_lo is None:
        return None
    if time.get("end") == "..":
        return start_lo, None
    _end_lo, end_hi = edtf_year_range(time.get("end"))
    if end_hi is None:
        return None
    return start_lo, end_hi


def _overlaps(entity_range, query_range):
    entity_start, entity_end = entity_range
    query_start, query_end = query_range
    return entity_start <= query_end and (entity_end is None or query_start <= entity_end)


def _regions_for_place(place_id, query_range, entities, region_history):
    place = entities.get(place_id) or {}
    query_start, query_end = query_range
    found = []
    for entry in (region_history or {}).get(place_id) or []:
        entry_start, _ = edtf_year_range(entry.get("start"))
        _entry_end_start, entry_end = edtf_year_range(entry.get("end"))
        if entry_start is None:
            continue
        if query_end < entry_start:
            continue
        if entry_end is not None and query_start >= entry_end:
            continue
        region = entry.get("region")
        if region and region not in found:
            found.append(region)
    if found:
        return found
    region = place.get("region")
    return [region] if region else [None]


def _space_candidates(meta, entities):
    """対象型に応じたspace roleから place targetを返す。"""
    if meta.get("type") == "place":
        return [{"place_id": meta.get("id"), "space_role": "self"}]
    allowed_roles = SPACE_ROLES_BY_TYPE.get(meta.get("type"), set())
    candidates = []
    for space in meta.get("space") or []:
        if not isinstance(space, dict) or space.get("role") not in allowed_roles:
            continue
        candidates.append({"place_id": space.get("target"), "space_role": space.get("role")})
    return candidates


def query_entities(entities, query_range, entity_type="movement", regions=None,
                   near=None, radius_km=None, region_history=None):
    """entitiesを問い合わせ、JSON/Markdown共通のpayloadを返す。"""
    if query_range[0] > query_range[1]:
        raise ValueError("問い合わせのfromはto以下にする")
    if entity_type not in TYPES:
        raise ValueError(f"未知のtype: {entity_type}")
    regions = sorted(set(regions or []))
    if radius_km is not None and radius_km < 0:
        raise ValueError("radius-kmは0以上が必要")
    if (near is None) != (radius_km is None):
        raise ValueError("nearとradius-kmはセットで指定する")
    near_coordinates = None
    if near is not None:
        near_meta = entities.get(near)
        if not near_meta or near_meta.get("type") != "place":
            raise ValueError(f"nearは存在するplace IDが必要: {near}")
        near_coordinates = _coordinates(near_meta)
        if near_coordinates is None:
            raise ValueError(f"nearのplaceに有効なcoordinatesがない: {near}")

    results = []
    exclusions = {}
    for entity_id, meta in sorted(entities.items()):
        if meta.get("type") != entity_type:
            continue
        entity_range = _entity_time_range(meta)
        if entity_range is None:
            exclusions[entity_id] = {"unknown-time"}
            continue
        if not _overlaps(entity_range, query_range):
            continue

        candidates = _space_candidates(meta, entities)
        if not candidates:
            exclusions[entity_id] = {"unknown-place"}
            continue
        accepted = []
        candidate_reasons = set()
        for candidate in candidates:
            place_id = candidate["place_id"]
            place = entities.get(place_id)
            coordinates = _coordinates(place or {})
            if not place or place.get("type") != "place" or coordinates is None:
                candidate_reasons.add("unknown-place")
                continue
            distance = None
            if near_coordinates is not None:
                distance = haversine_km(near_coordinates, coordinates)
                if distance > radius_km:
                    candidate_reasons.add("outside-radius")
                    continue
            place_regions = _regions_for_place(place_id, query_range, entities, region_history)
            matching_regions = [region for region in place_regions
                                if not regions or region in regions]
            if not matching_regions:
                candidate_reasons.add("region-filter")
                continue
            for region in matching_regions:
                result = {
                    "id": entity_id,
                    "label": meta.get("label_ja") or meta.get("label_en") or entity_id,
                    "type": meta.get("type"),
                    "time": {
                        "start": (meta.get("time") or {}).get("start"),
                        "end": (meta.get("time") or {}).get("end"),
                    },
                    "place_id": place_id,
                    "region": region,
                    "space_role": candidate["space_role"],
                }
                if distance is not None:
                    result["distance_km"] = round(distance, 3)
                accepted.append(result)
        if accepted:
            results.extend(accepted)
        else:
            exclusions[entity_id] = candidate_reasons or {"unknown-place"}

    def result_key(result):
        start, _ = edtf_year_range(result["time"].get("start"))
        return (start if start is not None else math.inf,
                result.get("region") or "", result["id"],
                result.get("place_id") or "", result["space_role"])

    results.sort(key=result_key)
    excluded = [
        {"id": entity_id, "reasons": sorted(reasons)}
        for entity_id, reasons in sorted(exclusions.items())
    ]
    return {
        "query": {
            "type": entity_type,
            "from": query_range[0],
            "to": query_range[1],
            "regions": regions,
            "near": near,
            "radius_km": radius_km,
        },
        "count": len(results),
        "entity_count": len({result["id"] for result in results}),
        "results": results,
        "excluded_count": len(excluded),
        "excluded": excluded,
    }


def render_json(payload):
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def _markdown_cell(value):
    return str(value if value is not None else "—").replace("|", "\\|").replace("\n", " ")


def render_markdown(payload):
    query = payload["query"]
    if query["from"] == query["to"]:
        period = str(query["from"])
    else:
        period = f"{query['from']}–{query['to']}"
    lines = [
        "# 時空間クエリ結果",
        "",
        f"- 対象: `{query['type']}`",
        f"- 年: `{period}`",
        f"- 地域: `{', '.join(query['regions']) if query['regions'] else '指定なし'}`",
        f"- 採用: {payload['count']}行 / {payload['entity_count']}entity",
        "",
        "> 注意: これは時間・空間条件に合う候補の生成であり、類似性・影響・因果関係の証拠ではない。",
        "",
        "## 結果",
        "",
        "| entity | label | time | place | region | role | distance km |",
        "|---|---|---|---|---|---|---:|",
    ]
    for result in payload["results"]:
        time = f"{result['time'].get('start')}–{result['time'].get('end')}"
        lines.append("| " + " | ".join([
            f"`{_markdown_cell(result['id'])}`",
            _markdown_cell(result["label"]),
            _markdown_cell(time),
            f"`{_markdown_cell(result['place_id'])}`",
            _markdown_cell(result["region"]),
            _markdown_cell(result["space_role"]),
            _markdown_cell(result.get("distance_km")),
        ]) + " |")
    if not payload["results"]:
        lines.append("| （該当なし） |  |  |  |  |  |  |")
    lines += ["", "## 除外", ""]
    if payload["excluded"]:
        for excluded in payload["excluded"]:
            lines.append(f"- `{excluded['id']}`: {', '.join(excluded['reasons'])}")
    else:
        lines.append("- なし")
    lines += ["", "生成元: `data/graph.json`。問い合わせはgraphにedgeを追加しない。", ""]
    return "\n".join(lines)


def _year(value):
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError("天文学的年番号の整数が必要") from exc


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--at", type=_year, help="1年を指定（BCEは天文学的年番号で負数）")
    parser.add_argument("--from", dest="from_year", type=_year)
    parser.add_argument("--to", dest="to_year", type=_year)
    parser.add_argument("--type", choices=sorted(TYPES), default="movement")
    parser.add_argument("--regions", nargs="+", default=[])
    parser.add_argument("--near", help="中心にするplace ID")
    parser.add_argument("--radius-km", type=float)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)
    if args.at is not None and (args.from_year is not None or args.to_year is not None):
        parser.error("--at と --from/--to は同時に指定できない")
    if args.at is None and (args.from_year is None or args.to_year is None):
        parser.error("--at または --from と --to の両方が必要")
    if args.at is not None:
        args.from_year = args.to_year = args.at
    elif args.from_year > args.to_year:
        parser.error("--from は --to 以下にする")
    if args.radius_km is not None and args.radius_km < 0:
        parser.error("--radius-km は0以上が必要")
    if (args.near is None) != (args.radius_km is None):
        parser.error("--near と --radius-km は必ずセットで指定する")
    return parser, args


def main(argv=None):
    try:
        parser, args = parse_args(argv)
        entities = load_graph()
        config = load_config()
        known_regions = set((config.get("buckets") or {}).keys())
        unknown_regions = sorted(set(args.regions) - known_regions)
        if unknown_regions:
            parser.error(f"未知のregion: {', '.join(unknown_regions)}")
        if args.near is not None:
            near_meta = entities.get(args.near)
            if not near_meta or near_meta.get("type") != "place":
                parser.error(f"--near は存在するplace IDが必要: {args.near}")
        payload = query_entities(
            entities,
            (args.from_year, args.to_year),
            entity_type=args.type,
            regions=args.regions,
            near=args.near,
            radius_km=args.radius_km,
            region_history=load_region_history(),
        )
        output = render_json(payload) if args.format == "json" else render_markdown(payload)
        print(output, end="")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"✗ 時空間クエリを実行できない: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
