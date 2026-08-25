#!/usr/bin/env python3
"""frontmatter を検証し、グラフと被覆集計を生成する。

    uv run --locked python tools/build_graph.py            # 検証 + data/graph.json + data/coverage.json + 被覆マップ更新
    uv run --locked python tools/build_graph.py --check    # 検証のみ（CI 用・書き込みなし）

検証で落ちるもの: 必須項目の欠落／id・uri とパスの不一致／id 重複／存在しない参照／語彙外の型・関係・役割／
EDTF 違反／解釈系の関係で certainty・source の欠落／verified なのに項目ごとの根拠がない／
place の region 欠落／俯瞰の依存先が更新されたのに as_of が古い（STALE）。
"""

import json
import math
import sys
import yaml

import re
from datetime import date

from kb import (AUTHORITY_ID_PATTERNS, AUTHORITY_KEYS, CERTAINTIES, CLAIM_FIELDS_FOR_VERIFIED,
                DIR_FOR_TYPE, ENTITIES, FOUNDING_CONTROL, IMAGE_LICENSES,
                INTERPRETIVE_RELATIONS, MOVEMENT_KINDS, RELATION_TARGET_TYPES, RELATIONS, ROOT,
                SPACE_ROLES, SPACE_TARGET_TYPES, STATUSES, TYPES, URI_PREFIX, alias_map,
                build_edges, century_of_year, edtf_ok, edtf_year_range, load_config, load_entities,
                load_coverage_reviews, load_region_history,
                is_http_url, normalized_meta, read_frontmatter, read_queries, regions_of,
                search_entities, source_urls, source_validation_errors)
from detail_baseline import validate_manifest

OVERVIEWS = ROOT / "overviews"
MARK_START = "<!-- generated:coverage:start -->"
MARK_END = "<!-- generated:coverage:end -->"
OVERVIEW_LINK_RE = re.compile(r"\]\((\.\./entities/[^)\s]+\.md)(?:#[^)]*)?\)")
OVERVIEW_ASSERTION_KEYS = {"subject", "field", "equals", "relation", "target", "space_role"}
EVIDENCE_SUPPORTS = {"kind", "time", "origin", "naming", "relation", "visual-character"}


def validate(entities, records, cfg, errors):
    seen = {}
    seen_aliases = {}
    for path, meta, _body in records:
        rel = meta["path"]

        def err(msg):
            errors.append(f"{rel}: {msg}")

        for key in ("id", "uri", "type", "label_ja", "sources", "status", "updated"):
            if not meta.get(key):
                err(f"必須項目 {key} が空")
        if any("TODO" in str(s) for s in meta.get("sources") or []):
            err("sources に TODO が残っている（出典URLを入れる）")
        errors.extend(source_validation_errors(meta.get("sources"), rel))
        normalized_source_urls = set(source_urls(meta.get("sources")))

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
            elif not isinstance(naming.get("self_identified"), bool):
                err("naming.self_identified はboolが必要")
            else:
                if naming.get("self_identified") is False and not naming.get("named_by") \
                        and not (naming.get("note") or "").strip():
                    err("naming.self_identified=false なら named_by か note で命名の経緯を書く")
                if "original_label" not in naming:
                    err("naming.original_label が必須")
                elif naming.get("original_label") is None:
                    if not (naming.get("note") or "").strip():
                        err("naming.original_label=null なら note に未確認理由が必要")
                elif not isinstance(naming.get("original_label"), str) \
                        or not naming["original_label"].strip():
                    err("naming.original_label は空でない文字列またはnullが必要")
                named_when = naming.get("named_when")
                if named_when is not None and not edtf_ok(named_when):
                    err(f"naming.named_when がEDTFに合わない: {named_when!r}")
                named_by = naming.get("named_by")
                if named_by is not None:
                    named_by_meta = entities.get(named_by)
                    if not named_by_meta or named_by_meta.get("type") not in {"person", "org"}:
                        err("naming.named_by は存在するpersonまたはorg IDが必要")
            if isinstance(naming, dict) and "rejected_by" in naming:
                rb = naming.get("rejected_by")
                if not isinstance(rb, list) or not rb:
                    err("naming.rejected_by は「誰が拒んだか」の配列にする（空なら項目を消す）")

            evidence = meta.get("evidence")
            if evidence is not None:
                if not isinstance(evidence, list):
                    err("evidence は配列が必要")
                else:
                    for index, item in enumerate(evidence, start=1):
                        prefix = f"evidence[{index}]"
                        if not isinstance(item, dict):
                            err(f"{prefix} はmapが必要")
                            continue
                        target_id = item.get("target")
                        target = entities.get(target_id)
                        if not target or target.get("type") not in {"person", "work"}:
                            err(f"{prefix}.target は存在するperson/work IDが必要: {target_id}")
                        else:
                            direct = any(
                                relation.get("target") == target_id
                                for relation in meta.get("relations") or []
                            )
                            reverse = any(
                                relation.get("target") == meta.get("id")
                                for relation in target.get("relations") or []
                            )
                            if not (direct or reverse):
                                err(f"{prefix}.targetへの既存relationが必要: {target_id}")
                        supports = item.get("supports")
                        if not isinstance(supports, list) or not supports:
                            err(f"{prefix}.supports は1件以上の配列が必要")
                            supports = []
                        if len(supports) != len({repr(support) for support in supports}):
                            err(f"{prefix}.supports に重複がある")
                        for support in supports:
                            if support not in EVIDENCE_SUPPORTS:
                                err(f"{prefix}.supports の語彙外: {support}")
                        if target and target.get("type") == "work" \
                                and "visual-character" in supports:
                            try:
                                target_body = read_frontmatter(ROOT / target["path"])[1]
                            except (OSError, ValueError) as exc:
                                err(f"{prefix}.target work本文を読めない: {exc}")
                            else:
                                if not re.search(r"^## どう成立しているか\s*$", target_body, re.MULTILINE):
                                    err(f"{prefix}.visual-characterにはwork本文の ## どう成立しているか が必要")

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

        for index, img in enumerate(meta.get("images") or [], start=1):
            prefix = f"images[{index}]"
            if not isinstance(img, dict):
                err(f"{prefix} はobjectが必要")
                continue
            for field in ("url", "source_page", "rights_source"):
                if not is_http_url(img.get(field)):
                    err(f"{prefix}.{field} はhttp(s) URLが必要")
            if img.get("license") not in IMAGE_LICENSES:
                err(f"{prefix}.license は {sorted(IMAGE_LICENSES)} のどれか"
                    f"（パブリックドメイン相当のみ／今: {img.get('license')}）")

        for fn in meta.get("former_names") or []:
            if not fn.get("name"):
                err("former_names の各項目に name が要る")
            if not edtf_ok(fn.get("from")) or not edtf_ok(fn.get("until")):
                err(f"former_names の from/until が EDTF に合わない: {fn}")

        if etype == "place" and not meta.get("region"):
            err("place は region が必須（被覆集計のキー。config/regions.yaml のバケット名）")
        if etype == "place" and meta.get("region") and meta["region"] not in cfg["buckets"]:
            err(f"未知の region: {meta['region']}")
        if etype == "place":
            coordinates = meta.get("coordinates")
            if not isinstance(coordinates, list) or len(coordinates) != 2:
                err("place.coordinates は [latitude, longitude] の2要素配列が必須")
            else:
                for index, value in enumerate(coordinates):
                    axis = "latitude" if index == 0 else "longitude"
                    if isinstance(value, bool) or not isinstance(value, (int, float)) \
                            or not math.isfinite(value):
                        err(f"place.coordinates.{axis} は有限の数値が必要")
                    elif (index == 0 and not -90 <= value <= 90) \
                            or (index == 1 and not -180 <= value <= 180):
                        err(f"place.coordinates.{axis} が範囲外: {value}")

        time = meta.get("time")
        if not isinstance(time, dict):
            err("time はstart/endを持つマップが必須")
            time = {}
        for field in ("start", "end"):
            if field not in time:
                err(f"time.{field} が必須（不明ならnull）")
            elif not edtf_ok(time.get(field)):
                err(f"time.{field} が EDTF Level 1 サブセットに合わない: {time.get(field)!r}")
        if time.get("start") == "..":
            err("time.start に開いた端 '..' は使えない（開いた端はendだけ）")
        start_lo, _start_hi = edtf_year_range(time.get("start"))
        _end_lo, end_hi = edtf_year_range(time.get("end"))
        if start_lo is not None and end_hi is not None and start_lo > end_hi:
            err(f"time.start がtime.endより後: {time.get('start')!r} > {time.get('end')!r}")

        auth = meta.get("authority")
        if not isinstance(auth, dict):
            err("authority は典拠keyを持つマップが必須")
            auth = {}
        unknown_authority_keys = set(auth) - AUTHORITY_KEYS
        if unknown_authority_keys:
            err(f"authority に未知のkey: {sorted(unknown_authority_keys)}")
        authority_ids = []
        for key, pattern in AUTHORITY_ID_PATTERNS.items():
            value = auth.get(key)
            if value is None or value == "":
                continue
            if isinstance(value, bool) or not pattern.fullmatch(str(value)):
                err(f"authority.{key} の形式が不正: {value!r}")
            else:
                authority_ids.append(key)
        jpsearch = auth.get("jpsearch")
        if jpsearch is not None and (not isinstance(jpsearch, str) or not jpsearch.strip()):
            err(f"authority.jpsearch は空でない文字列またはURLが必要: {jpsearch!r}")
        if jpsearch:
            authority_ids.append("jpsearch")
        none_reason = auth.get("none_reason")
        if authority_ids and none_reason not in (None, ""):
            err("authorityにIDがある場合、none_reasonはnullにする")
        if not authority_ids and (not isinstance(none_reason, str) or not none_reason.strip()):
            err("典拠が1つも無いときはauthority.none_reasonに理由を書く")

        updated = meta.get("updated")
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(updated)):
                raise ValueError
            date.fromisoformat(str(updated))
        except ValueError:
            err(f"updated は実在するYYYY-MM-DDが必要: {updated!r}")

        aliases = meta.get("aliases") or []
        if not isinstance(aliases, list):
            err("aliases は文字列の配列が必要")
            aliases = []
        for alias in aliases:
            if not isinstance(alias, str) or not alias.strip():
                err(f"alias は空でない文字列が必要: {alias!r}")
                continue
            if alias in entities:
                err(f"alias {alias} が既存の id と衝突している")
            if alias in seen_aliases:
                err(f"alias {alias} が重複している（{seen_aliases[alias]} と {meta.get('id')}）")
            else:
                seen_aliases[alias] = meta.get("id")
            if "/" in alias:
                alias_type, _, alias_slug = alias.partition("/")
                if alias_type not in TYPES or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", alias_slug):
                    err(f"型付きaliasの形式が不正: {alias}")

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
            if r.get("source"):
                if not is_http_url(r.get("source")):
                    err(f"{rtype}.source はhttp(s) URLが必要: {r.get('source')!r}")
                elif r["source"] not in normalized_source_urls:
                    err(f"{rtype}.source がsourcesにない: {r['source']}")
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
        claim_keys = set()
        for c in meta.get("claims") or []:
            if not isinstance(c, dict):
                err(f"claims の各項目はマップが必要: {c!r}")
                continue
            field = c.get("field")
            if not isinstance(field, str) or not field.strip():
                err("claims の field が無い")
            if not c.get("source"):
                err(f"claims の {field} に source が無い")
            else:
                if not is_http_url(c.get("source")):
                    err(f"claims の {field}.source はhttp(s) URLが必要: {c.get('source')!r}")
                elif c["source"] not in normalized_source_urls:
                    err(f"claims の {field}.source がsourcesにない: {c['source']}")
            if c.get("certainty") not in CERTAINTIES:
                err(f"claims の {field} の certainty が語彙外: {c.get('certainty')}")
            claim_key = json.dumps(c, ensure_ascii=False, sort_keys=True, default=str)
            if claim_key in claim_keys:
                err(f"claims に完全重複がある: {c}")
            claim_keys.add(claim_key)

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


def _scalar_field(meta, field):
    value = meta
    for part in field.split("."):
        if not isinstance(value, dict) or part not in value:
            return False, None
        value = value[part]
    if isinstance(value, (dict, list)):
        return False, value
    return True, value


def _overview_link_ids(path, body, entities):
    path_to_id = {
        str((ROOT / meta["path"]).resolve()): entity_id
        for entity_id, meta in entities.items() if meta.get("path")
    }
    ids = set()
    for relative in OVERVIEW_LINK_RE.findall(body):
        target = (path.parent / relative).resolve()
        entity_id = path_to_id.get(str(target))
        if entity_id:
            ids.add(entity_id)
    return ids


def validate_overviews(entities, errors):
    """Validate machine-readable overview assertions and dependency closure."""
    latest_updated = max((str(meta.get("updated") or "") for meta in entities.values()), default="")
    for path in sorted(OVERVIEWS.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
            if not text.startswith("---\n"):
                errors.append(f"overviews/{path.name}: frontmatter がない")
                continue
            meta = yaml.safe_load(text.split("---\n", 2)[1]) or {}
            body = text.split("---\n", 2)[2]
        except Exception as exc:
            errors.append(f"overviews/{path.name}: frontmatterを読めない: {exc}")
            continue

        as_of = str(meta.get("as_of") or "")
        try:
            date.fromisoformat(as_of)
        except ValueError:
            errors.append(f"overviews/{path.name}: as_of は実在するYYYY-MM-DDが必要: {as_of!r}")

        depends_on = meta.get("depends_on")
        if not isinstance(depends_on, list):
            errors.append(f"overviews/{path.name}: depends_on は配列が必要")
            depends_on = []
        dependency_ids = []
        for index, entity_id in enumerate(depends_on, start=1):
            if not isinstance(entity_id, str):
                errors.append(f"overviews/{path.name}: depends_on[{index}] はentity ID文字列が必要")
                continue
            dependency_ids.append(entity_id)
        if len(dependency_ids) != len(set(dependency_ids)):
            errors.append(f"overviews/{path.name}: depends_on に重複がある")
        for entity_id in dependency_ids:
            if entity_id not in entities:
                errors.append(f"overviews/{path.name}: depends_on に存在しない {entity_id}")

        if path.name == "coverage.md":
            generated = re.search(r"データの最新日: (\d{4}-\d{2}-\d{2})", body)
            if as_of != latest_updated:
                errors.append(f"overviews/{path.name}: as_of={as_of} がentityの最新日 {latest_updated} と不一致")
            if not generated or generated.group(1) != latest_updated:
                errors.append(f"overviews/{path.name}: 生成ブロックの最新日がentityの最新日 {latest_updated} と不一致")
            continue

        assertions = meta.get("assertions")
        if not isinstance(assertions, list):
            errors.append(f"overviews/{path.name}: assertions は配列が必要")
            assertions = []
        required = set()
        for index, assertion in enumerate(assertions, start=1):
            prefix = f"overviews/{path.name}: assertions[{index}]"
            if not isinstance(assertion, dict):
                errors.append(f"{prefix} はマップで書く")
                continue
            unknown = set(assertion) - OVERVIEW_ASSERTION_KEYS
            if unknown:
                errors.append(f"{prefix}: 未知のキー {sorted(unknown)}")
            subject = assertion.get("subject")
            if subject not in entities:
                errors.append(f"{prefix}: subjectが存在しない {subject}")
            else:
                required.add(subject)
            kinds = [key for key in ("field", "relation", "space_role") if key in assertion]
            if len(kinds) != 1:
                errors.append(f"{prefix}: field/relation/space_roleのいずれか1つが必要")
                continue
            kind = kinds[0]
            if kind == "field":
                field = assertion.get("field")
                if not isinstance(field, str) or not field:
                    errors.append(f"{prefix}: fieldは空でない文字列が必要")
                    continue
                if "equals" not in assertion or isinstance(assertion.get("equals"), (dict, list)):
                    errors.append(f"{prefix}: scalar fieldにはscalarのequalsが必要")
                    continue
                if subject in entities:
                    exists, actual = _scalar_field(entities[subject], field)
                    if not exists:
                        errors.append(f"{prefix}: scalar fieldが存在しない {field}")
                    elif actual != assertion["equals"]:
                        errors.append(f"{prefix}: {subject}.{field}={actual!r}（期待値 {assertion['equals']!r}）")
            else:
                relation_or_role = assertion.get(kind)
                target = assertion.get("target")
                if not isinstance(relation_or_role, str):
                    errors.append(f"{prefix}: {kind}は文字列が必要")
                elif kind == "relation" and relation_or_role not in RELATIONS:
                    errors.append(f"{prefix}: 未知のrelation {relation_or_role}")
                elif kind == "space_role" and relation_or_role not in SPACE_ROLES:
                    errors.append(f"{prefix}: 未知のspace_role {relation_or_role}")
                if target not in entities:
                    errors.append(f"{prefix}: targetが存在しない {target}")
                else:
                    required.add(target)
                if subject in entities and isinstance(relation_or_role, str):
                    if kind == "relation":
                        found = any(r.get("type") == relation_or_role and r.get("target") == target
                                    for r in entities[subject].get("relations") or [])
                    else:
                        found = any(s.get("role") == relation_or_role and s.get("target") == target
                                    for s in entities[subject].get("space") or [])
                    if not found:
                        errors.append(f"{prefix}: entityに対応する{kind}がない")

        for index, row in enumerate(meta.get("tested") or [], start=1):
            if not isinstance(row, dict):
                errors.append(f"overviews/{path.name}: tested[{index}] はマップで書く")
                continue
            tested_by = row.get("by")
            if tested_by not in entities:
                errors.append(f"overviews/{path.name}: tested[{index}].byが存在しない {tested_by}")
            else:
                required.add(tested_by)

        required |= _overview_link_ids(path, body, entities)
        missing = sorted(required - set(dependency_ids))
        if missing:
            errors.append(f"overviews/{path.name}: depends_onに参照先が不足 {', '.join(missing)}")


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
        if lo is not None and lo < 1800:
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
    lines = [f"データの最新日: {cov['as_of']} — `uv run --locked python tools/build_graph.py` が生成（手で書き換えない）", "",
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
    validate_overviews(entities, errors)
    errors.extend(validate_manifest(entities, cfg))

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
    graph_entities = {entity_id: normalized_meta(meta) for entity_id, meta in entities.items()}
    (ROOT / "data" / "graph.json").write_text(
        json.dumps({"entities": graph_entities, "edges": edges}, ensure_ascii=False, indent=2, default=str) + "\n",
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
