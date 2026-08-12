#!/usr/bin/env python3
"""frontmatter を検証し、グラフと被覆集計を生成する。

    python3 tools/build_graph.py            # 検証 + data/graph.json + data/coverage.json + 被覆マップ更新
    python3 tools/build_graph.py --check    # 検証のみ（CI 用・書き込みなし）

検証で落ちるもの: 必須項目の欠落／id・uri とパスの不一致／id 重複／存在しない参照／語彙外の型・関係・役割／
EDTF 違反／解釈系の関係で certainty・source の欠落／verified なのに項目ごとの根拠がない／
place の region 欠落／俯瞰の依存先が更新されたのに as_of が古い（STALE）。
"""

import json
import sys
import yaml

import re

from kb import (CERTAINTIES, CLAIM_FIELDS_FOR_VERIFIED, DIR_FOR_TYPE, ENTITIES, FOUNDING_CONTROL,
                IMAGE_LICENSES,
                INTERPRETIVE_RELATIONS, MOVEMENT_KINDS, RELATION_TARGET_TYPES, RELATIONS, ROOT,
                SPACE_ROLES, SPACE_TARGET_TYPES, STATUSES, TYPES, URI_PREFIX, alias_map,
                build_edges, century_of_year, edtf_ok, edtf_year_range, load_config, load_entities,
                load_coverage_reviews, load_region_history,
                read_frontmatter, read_queries, regions_of, search_entities)

OVERVIEWS = ROOT / "overviews"
MARK_START = "<!-- generated:coverage:start -->"
MARK_END = "<!-- generated:coverage:end -->"


def validate(entities, records, cfg, errors):
    seen = {}
    for path, meta, _body in records:
        rel = meta["path"]

        def err(msg):
            errors.append(f"{rel}: {msg}")

        for key in ("id", "uri", "type", "label_ja", "sources", "status", "updated"):
            if not meta.get(key):
                err(f"必須項目 {key} が空")
        if any("TODO" in str(s) for s in meta.get("sources") or []):
            err("sources に TODO が残っている（出典URLを入れる）")

        etype = meta.get("type")
        if etype not in TYPES:
            err(f"未知の type: {etype}")
        else:
            expected = f"{etype}/{path.stem}"
            if meta.get("id") != expected:
                err(f"id とパスが不一致（id={meta.get('id')} / 期待={expected}）")
            if meta.get("uri") != URI_PREFIX + expected:
                err(f"uri は {URI_PREFIX}{expected} にする（今: {meta.get('uri')}）")
            if path.parent.name != DIR_FOR_TYPE[etype]:
                err(f"type={etype} は entities/{DIR_FOR_TYPE[etype]}/ に置く")

        if meta.get("id") in seen:
            err(f"id が重複: {meta.get('id')}（既出: {seen[meta['id']]}）")
        seen[meta.get("id")] = rel

        for key, value in meta.items():
            if isinstance(value, str) and "TODO" in value:
                err(f"{key} に TODO が残っている（雛形のまま）")

        if meta.get("status") not in STATUSES:
            err(f"status は {sorted(STATUSES)} のどれか（今: {meta.get('status')}）")

        if etype == "movement":
            if meta.get("kind") not in MOVEMENT_KINDS:
                err(f"movement は kind が必須（{sorted(MOVEMENT_KINDS)}／今: {meta.get('kind')}）")
            naming = meta.get("naming")
            if not isinstance(naming, dict) or "self_identified" not in naming:
                err("movement は naming.self_identified が必須（後付けの命名と自己認識の区別）")
            elif naming.get("self_identified") is False and not naming.get("named_by") \
                    and not (naming.get("note") or "").strip():
                err("naming.self_identified=false なら named_by か note で命名の経緯を書く")
            if naming and "rejected_by" in naming:
                rb = naming.get("rejected_by")
                if not isinstance(rb, list) or not rb:
                    err("naming.rejected_by は「誰が拒んだか」の配列にする（空なら項目を消す）")

        if meta.get("founding_control") and meta["founding_control"] not in FOUNDING_CONTROL:
            err(f"founding_control は {sorted(FOUNDING_CONTROL)} のどれか（今: {meta['founding_control']}）")

        for ch in meta.get("control_changes") or []:
            if not edtf_ok(ch.get("year")):
                err(f"control_changes の year が EDTF に合わない: {ch.get('year')!r}")
            if ch.get("to") not in FOUNDING_CONTROL:
                err(f"control_changes の to は {sorted(FOUNDING_CONTROL)} のどれか（今: {ch.get('to')}）")
            if not (ch.get("trigger") or "").strip():
                err("control_changes には trigger が必須（何が決定者を入れ替えたか）")
        if meta.get("control_changes") and not meta.get("founding_control"):
            err("control_changes を書くなら founding_control（成立時点の値）も要る")

        for img in meta.get("images") or []:
            if not img.get("url"):
                err("images の各項目に url が要る")
            if img.get("license") not in IMAGE_LICENSES:
                err(f"images の license は {sorted(IMAGE_LICENSES)} のどれか"
                    f"（パブリックドメイン相当のみ／今: {img.get('license')}）")
            if not img.get("source_page"):
                err("images の各項目に source_page（所蔵館の作品ページ）が要る")

        for fn in meta.get("former_names") or []:
            if not fn.get("name"):
                err("former_names の各項目に name が要る")
            if not edtf_ok(fn.get("from")) or not edtf_ok(fn.get("until")):
                err(f"former_names の from/until が EDTF に合わない: {fn}")

        if etype == "place" and not meta.get("region"):
            err("place は region が必須（被覆集計のキー。config/regions.yaml のバケット名）")
        if etype == "place" and meta.get("region") and meta["region"] not in cfg["buckets"]:
            err(f"未知の region: {meta['region']}")

        t = meta.get("time") or {}
        for field in ("start", "end"):
            if not edtf_ok(t.get(field)):
                err(f"time.{field} が EDTF Level 1 サブセットに合わない: {t.get(field)!r}")

        auth = meta.get("authority") or {}
        if not any(auth.get(k) for k in ("wikidata", "aat", "ndl", "jpsearch")) \
                and not auth.get("none_reason"):
            err("典拠が1つも無いときは authority.none_reason に理由を書く")

        for a in meta.get("aliases") or []:
            if a in entities:
                err(f"alias {a} が既存の id と衝突している")

        for r in meta.get("relations") or []:
            rtype = r.get("type")
            if rtype not in RELATIONS:
                err(f"未知の関係 type: {rtype}")
                continue
            allowed = RELATION_TARGET_TYPES.get(rtype)
            target = entities.get(r.get("target"))
            if allowed and target and target.get("type") not in allowed:
                err(f"{rtype} が指せるのは {sorted(allowed)}。今: {r.get('target')}"
                    f"（{target.get('type')}）")
            if rtype in INTERPRETIVE_RELATIONS:
                if r.get("certainty") not in CERTAINTIES:
                    err(f"{rtype} は certainty が必須（{sorted(CERTAINTIES)}／今: {r.get('certainty')}）")
                if not r.get("source"):
                    err(f"{rtype} は source が必須（解釈を含む関係）")
        for s in meta.get("space") or []:
            role = s.get("role")
            if role not in SPACE_ROLES:
                err(f"未知の space role: {role}")
                continue
            allowed = SPACE_TARGET_TYPES.get(role)
            target = entities.get(s.get("target"))
            if allowed and target and target.get("type") not in allowed:
                err(f"{role} が指せるのは {sorted(allowed)}。今: {s.get('target')}"
                    f"（{target.get('type')}）")

        if meta.get("status") == "verified":
            need = CLAIM_FIELDS_FOR_VERIFIED.get(etype, set())
            have = {c.get("field") for c in meta.get("claims") or []}
            for field in sorted(need - have):
                err(f"verified を名乗るには claims に {field} の根拠が要る")
        for c in meta.get("claims") or []:
            if not c.get("source"):
                err(f"claims の {c.get('field')} に source が無い")
            if c.get("certainty") not in CERTAINTIES:
                err(f"claims の {c.get('field')} の certainty が語彙外: {c.get('certainty')}")

    aliases = alias_map(entities)
    for edge in build_edges(entities):
        if edge.get("derived"):
            continue
        if edge["to"] not in entities and edge["to"] not in aliases:
            errors.append(f"{edge['from']}: 存在しない参照先 {edge['to']}（{edge['type']}）")

    # 本文の相対リンクが実在するか（slug を変えたときに黙って切れるのを防ぐ）
    link_re = re.compile(r"\]\((\.[^)\s]+\.md)\)")
    for path, _meta, body in records:
        for rel_link in link_re.findall(body):
            if not (path.parent / rel_link).resolve().exists():
                errors.append(f"{path.relative_to(ROOT)}: 本文のリンク先が無い {rel_link}")

    history = load_region_history()
    for place_id, entries in history.items():
        place = entities.get(place_id)
        if not place or place.get("type") != "place":
            errors.append(f"place-region-history: 存在しない place {place_id}")
            continue
        previous = []
        for entry in entries or []:
            start = entry.get("start")
            end = entry.get("end")
            region = entry.get("region")
            if not edtf_ok(start) or start == "..":
                errors.append(f"place-region-history {place_id}: start が不正: {start!r}")
            if not edtf_ok(end):
                errors.append(f"place-region-history {place_id}: end が不正: {end!r}")
            if region not in cfg["buckets"]:
                errors.append(f"place-region-history {place_id}: 未知の region: {region}")
            start_year, _ = edtf_year_range(start)
            end_year, _ = edtf_year_range(end)
            if start_year is not None and end_year is not None and start_year >= end_year:
                errors.append(f"place-region-history {place_id}: start が end 以後: {entry}")
            for old in previous:
                old_start, _ = edtf_year_range(old.get("start"))
                old_end, _ = edtf_year_range(old.get("end"))
                overlaps = ((old_end is None or start_year is None or start_year < old_end)
                            and (end_year is None or old_start is None or end_year > old_start))
                if overlaps:
                    errors.append(f"place-region-history {place_id}: 区間が重複: {old} / {entry}")
            previous.append(entry)


def check_overview_freshness(entities, errors):
    """俯瞰の depends_on が as_of より後に更新されていたら STALE として落とす。"""
    for path in sorted(OVERVIEWS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        meta = yaml.safe_load(text.split("---\n", 2)[1]) or {}
        as_of = str(meta.get("as_of") or "")
        for dep in meta.get("depends_on") or []:
            target = entities.get(dep)
            if target is None:
                errors.append(f"overviews/{path.name}: depends_on に存在しない {dep}")
            elif as_of and str(target.get("updated")) > as_of:
                errors.append(
                    f"overviews/{path.name}: STALE — {dep} が {target['updated']} に更新（as_of={as_of}）")


def validate_coverage_reviews(reviews, cfg, cov, errors):
    """被覆表の空セルに対する調査済み記録を検証する。"""
    seen = set()
    for index, row in enumerate(reviews, start=1):
        prefix = f"config/coverage-reviews.yaml: cells[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix} はマップで書く")
            continue
        region = row.get("region")
        century = row.get("century")
        status = row.get("status")
        if region not in cfg["buckets"]:
            errors.append(f"{prefix}: 未知の region: {region}")
        century = str(century) if century is not None else ""
        if century != "unknown":
            try:
                century_number = int(century)
            except (TypeError, ValueError):
                century_number = 0
            if century_number == 0:
                errors.append(f"{prefix}: century は正の世紀、負の紀元前世紀、unknown のいずれか")
        if status != "no-known-grouping":
            errors.append(f"{prefix}: status は no-known-grouping のみ（今: {status}）")
        if not isinstance(row.get("note"), str) or not row["note"].strip():
            errors.append(f"{prefix}: note が必要")
        sources = row.get("sources")
        if not isinstance(sources, list) or not sources or any(
                not isinstance(source, str) or not source.startswith(("http://", "https://"))
                for source in sources):
            errors.append(f"{prefix}: sources に http(s) URL が1つ以上必要")
        key = (region, century)
        if key in seen:
            errors.append(f"{prefix}: 同じセルが重複している: {region} / {century}")
        seen.add(key)
        if cov["grid"].get(region, {}).get(century, 0):
            errors.append(f"{prefix}: movement が存在するセルは no-known-grouping にできない: {region} / {century}")


def coverage(entities, cfg):
    """movement × 文化圏 × 世紀 の被覆と、受け入れ条件の達成度。

    **stub は実績に数えない。** 枠だけのファイルで件数を満たせてしまうと、受け入れ条件が意味を失う。
    起源が複数あるものは、どのバケットにも代表させずに「複数起源」として別に数える——
    最初の1つで代表させると地域比率が歪む。
    """
    movements = {i: m for i, m in entities.items() if m.get("type") == "movement"}
    counted = {i: m for i, m in movements.items() if m.get("status") in ("draft", "verified")}
    buckets = cfg["buckets"]
    grid, per_bucket = {}, {b: 0 for b in buckets}
    unknown_origin, multi_origin, pre1800, isolated = [], [], 0, []
    all_edges = build_edges(entities)
    region_history = load_region_history()
    edge_ends = {e["from"] for e in all_edges} | {e["to"] for e in all_edges}
    reviews = load_coverage_reviews()

    for mid, meta in counted.items():
        regions = regions_of(mid, entities, region_history)
        lo, _hi = edtf_year_range((meta.get("time") or {}).get("start"))
        century = str(century_of_year(lo)) if lo is not None else "unknown"
        if lo and lo < 1800:
            pre1800 += 1
        if not regions:
            key = "origin-unknown"
            unknown_origin.append(mid)
        elif len(regions) > 1:
            key = "origin-multiple"
            multi_origin.append({"id": mid, "regions": regions})
        else:
            key = regions[0]
            per_bucket[key] += 1
        grid.setdefault(key, {}).setdefault(century, 0)
        grid[key][century] += 1
        if mid not in edge_ends:
            isolated.append(mid)

    total = len(counted)
    non_west = sum(n for b, n in per_bucket.items() if not buckets[b]["west"])
    th = cfg["thresholds"]
    # as_of は「今日」ではなく、反映しているデータの最新日にする。
    # 今日を入れると生成物が走らせた日ごとに変わり、CI の「生成物が最新か」が時差だけで落ちる。
    return {
        "as_of": max((str(m.get("updated") or "") for m in entities.values()), default=""),
        "movement_total": total,
        "movement_stub_excluded": len(movements) - total,
        "by_status": {s: sum(1 for m in movements.values() if m.get("status") == s)
                      for s in sorted(STATUSES)},
        "grid": grid,
        "per_bucket": per_bucket,
        "origin_unknown": unknown_origin,
        "origin_multiple": multi_origin,
        "isolated": isolated,
        "no_known_grouping": reviews,
        "progress": {
            "movement_total": f"{total}/{th['movement_total']}（stub {len(movements) - total}件は不算入）",
            "non_west_ratio": f"{(non_west / total if total else 0):.2f}/{th['non_west_ratio']}",
            "per_bucket_min": f"{sum(1 for n in per_bucket.values() if n >= th['per_bucket_min'])}"
                              f"/{len(buckets)} バケットが {th['per_bucket_min']}件以上",
            "pre_1800_ratio": f"{(pre1800 / total if total else 0):.2f}/{th['pre_1800_ratio']}",
            "isolated_ratio": f"{(len(isolated) / total if total else 0):.2f}"
                              f"（上限 {th['isolated_max_ratio']}）",
        },
    }


def render_coverage(cov, cfg, entities):
    buckets = cfg["buckets"]
    reviewed = {(str(row.get("region")), str(row.get("century"))): row
                for row in cov["no_known_grouping"]}
    centuries = {c for row in cov["grid"].values() for c in row if c != "unknown"}
    centuries |= {str(row.get("century")) for row in cov["no_known_grouping"]
                  if str(row.get("century")) != "unknown"}
    centuries = sorted(centuries, key=int)
    cols = [(c, f"{abs(int(c))}BCE" if int(c) < 0 else f"{c}C") for c in centuries]
    cols += [("unknown", "年代不明")]
    header = "| 文化圏 | " + " | ".join(label for _k, label in cols) + " | 計 |"
    sep = "|---" * (len(cols) + 2) + "|"
    lines = [f"データの最新日: {cov['as_of']} — `python3 tools/build_graph.py` が生成（手で書き換えない）", "",
             f"movement **{cov['movement_total']}** 件（stub {cov['movement_stub_excluded']}件は不算入）"
             f"／内訳 {cov['by_status']}", "", header, sep]
    for b, conf in buckets.items():
        row = cov["grid"].get(b, {})
        cells = " | ".join("∅" if (b, k) in reviewed else str(row.get(k, 0) or "")
                           for k, _label in cols)
        mark = "" if conf["west"] else " ※非西洋"
        lines.append(f"| {b}（{conf['label_ja']}）{mark} | {cells} | {cov['per_bucket'].get(b, 0)} |")
    for key, label in (("origin-unknown", "**発生地未確認**"), ("origin-multiple", "**複数起源**")):
        if cov["grid"].get(key):
            row = cov["grid"][key]
            cells = " | ".join(str(row.get(k, 0) or "") for k, _label in cols)
            n = len(cov["origin_unknown"] if key == "origin-unknown" else cov["origin_multiple"])
            lines.append(f"| {label} | {cells} | {n} |")
    if cov["origin_multiple"]:
        lines += ["", "複数起源（どのバケットにも代表させていない）:"] + [
            f"- {m['id']} — {' / '.join(m['regions'])}" for m in cov["origin_multiple"]]
    if cov["no_known_grouping"]:
        lines += ["", "**調査済み・該当する movement なし**（`no-known-grouping`）:", ""]
        for row in cov["no_known_grouping"]:
            century = str(row["century"])
            label = "年代不明" if century == "unknown" else (
                f"{abs(int(century))}BCE" if int(century) < 0 else f"{century}C")
            lines.append(f"- {row['region']} / {label}: {row['note']}（出典: {'、'.join(row['sources'])}）")
    # 空振りの記録は残すが、**いま当たる語は出さない**。KB が空だった頃に探された語をそのまま
    # 「無い」と出し続けると、既に入っているものを調べに行かせてしまう。
    asked = {}
    for q in read_queries():
        if q.get("hits") == 0:
            asked[q["term"]] = asked.get(q["term"], 0) + 1
    misses = {t: n for t, n in asked.items() if not search_entities(t, entities)}
    if misses:
        lines += ["", "**探されたが無かった語**（需要のシグナル。多い順）:", ""]
        lines += [f"- {term} — {n}回" for term, n in sorted(misses.items(), key=lambda x: -x[1])]
    filled = sorted(set(asked) - set(misses))
    if filled:
        lines += ["", f"探された当時は無く、いまは入っている語: {', '.join(filled)}"]

    lines += ["", "受け入れ条件の達成度:", ""]
    lines += [f"- {k}: {v}" for k, v in cov["progress"].items()]
    if cov["isolated"]:
        lines += ["", f"関係を持たない movement: {', '.join(cov['isolated'])}"]
    return "\n".join(lines)


def warn_if_hook_off():
    """clone 直後はフックが無効。気づかないまま検証なしで commit できてしまうので、走る度に言う。"""
    import subprocess
    try:
        got = subprocess.run(["git", "-C", str(ROOT), "config", "core.hooksPath"],
                             capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception:
        return
    if got != ".githooks":
        print("⚠ commit 前の検証フックが無効です。1回だけ実行してください: "
              "git config core.hooksPath .githooks", file=sys.stderr)


def main():
    check_only = "--check" in sys.argv
    warn_if_hook_off()
    cfg = load_config()
    errors = []
    try:
        entities, records = load_entities()
    except Exception as exc:
        print(f"✗ 読み込み失敗: {exc}", file=sys.stderr)
        return 1

    validate(entities, records, cfg, errors)
    check_overview_freshness(entities, errors)

    if errors:
        print(f"✗ {len(errors)} 件:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    edges = build_edges(entities)
    cov = coverage(entities, cfg)
    validate_coverage_reviews(cov["no_known_grouping"], cfg, cov, errors)
    if errors:
        print(f"✗ {len(errors)} 件:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    if check_only:
        print(f"✓ {len(entities)} エンティティ / {len(edges)} 関係 — 問題なし")
        return 0

    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "graph.json").write_text(
        json.dumps({"entities": entities, "edges": edges}, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8")
    (ROOT / "data" / "coverage.json").write_text(
        json.dumps(cov, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")

    cmap = OVERVIEWS / "coverage.md"
    text = cmap.read_text(encoding="utf-8")
    if MARK_START in text and MARK_END in text:
        head, rest = text.split(MARK_START, 1)
        _old, tail = rest.split(MARK_END, 1)
        cmap.write_text(f"{head}{MARK_START}\n{render_coverage(cov, cfg, entities)}\n{MARK_END}{tail}",
                        encoding="utf-8")
    else:
        errors.append("overviews/coverage.md に生成ブロックのマーカーが無い")

    print(f"✓ {len(entities)} エンティティ / {len(edges)} 関係")
    print(f"  movement {cov['movement_total']} 件 / " + " / ".join(f"{k}={v}" for k, v in cov["progress"].items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
