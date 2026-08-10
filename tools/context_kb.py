#!/usr/bin/env python3
"""時代文脈スナップショットの読み込み、検証、ベクトル化、比較。"""

from __future__ import annotations

import hashlib
import math
import re
from pathlib import Path

import yaml

from kb import edtf_ok


CONTEXT_KINDS = {"historical", "current"}
CONTEXT_STATUSES = {"draft", "verified"}
SIGNAL_ID_RE = re.compile(r"^s\d{3}$")
HTTP_RE = re.compile(r"^https?://", re.IGNORECASE)
FIXED_HEADINGS = ("範囲", "根拠の読み方", "反対証拠・内部差", "未確認")


class ContextCollection(dict):
    """dict APIを保ったまま、読み込み時の複数エラーも保持する。"""

    def __init__(self):
        super().__init__()
        self.load_errors = []


def _relative(path, root):
    try:
        return path.resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("frontmatter がない")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("frontmatter の終端 --- がない")
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"frontmatter YAML が不正: {exc}") from exc
    if not isinstance(meta, dict):
        raise ValueError("frontmatter はマッピングにする")
    return meta, parts[2]


def load_contexts(contexts_dir, root):
    """contexts直下を読み、context IDをキーとするdictを返す。"""
    contexts = ContextCollection()
    contexts_dir = Path(contexts_dir)
    root = Path(root)
    if not contexts_dir.exists():
        return contexts
    for path in sorted(contexts_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        rel = _relative(path, root)
        try:
            meta, body = _parse_frontmatter(path)
        except (OSError, ValueError) as exc:
            contexts.load_errors.append(f"{rel}: {exc}")
            continue
        meta = dict(meta)
        meta["_path"] = path
        meta["_relative_path"] = rel
        meta["_body"] = body
        context_id = meta.get("id")
        key = context_id if isinstance(context_id, str) and context_id else f"__invalid__/{path.stem}"
        if key in contexts:
            contexts.load_errors.append(f"{rel}: id が重複: {key}")
            continue
        contexts[key] = meta
    return contexts


def _public_context(context):
    return {k: v for k, v in context.items() if not k.startswith("_")}


def _body_section(body, heading):
    match = re.search(rf"^## {re.escape(heading)}\s*$", body, re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^## \S.*$", body[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(body)
    return body[start:end]


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def validate_contexts(contexts, entities, config):
    """全contextを検証し、ファイル・signal ID付きのエラー文字列を返す。"""
    errors = list(getattr(contexts, "load_errors", []))
    dimensions = sorted(config.get("dimensions") or [], key=lambda d: d.get("index", 999))
    dimension_ids = {d.get("id") for d in dimensions}
    certainty_weights = config.get("certainty_weights") or {}
    holder_roles = set(config.get("holder_roles") or [])
    regions = set(config.get("regions") or config.get("_regions") or [])

    for context in contexts.values():
        path = context.get("_path")
        rel = context.get("_relative_path") or (path.as_posix() if path else "<context>")
        body = context.get("_body") or ""

        def err(message, signal_id=None):
            prefix = f"{rel}:"
            if signal_id:
                prefix += f" {signal_id}:"
            errors.append(f"{prefix} {message}")

        required = ("id", "label_ja", "kind", "scope", "about", "signals", "sources", "status", "updated")
        for field in required:
            if field not in context or context.get(field) is None:
                err(f"必須フィールド {field} がない")

        if not isinstance(context.get("label_ja"), str) or not context.get("label_ja", "").strip():
            err("label_ja は空でない文字列にする")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(context.get("updated", ""))):
            err("updated は YYYY-MM-DD にする")

        context_id = context.get("id")
        if path and context_id != f"context/{path.stem}":
            err(f"id とファイル名が一致しない（id={context_id!r}）")
        if context.get("kind") not in CONTEXT_KINDS:
            err(f"kind が語彙外: {context.get('kind')!r}")
        if context.get("status") not in CONTEXT_STATUSES:
            err(f"status が語彙外: {context.get('status')!r}")

        scope = context.get("scope") or {}
        if not isinstance(scope, dict):
            err("scope はマッピングにする")
            scope = {}
        if scope.get("domain") != "art":
            err("scope.domain は art 固定")
        for field in ("start", "end"):
            if field not in scope or scope.get(field) is None:
                err(f"scope.{field} は必須")
        scope_regions = scope.get("regions")
        if not isinstance(scope_regions, list) or not scope_regions:
            err("scope.regions は1件以上にする")
        else:
            for region in scope_regions:
                if region not in regions:
                    err(f"未知の region: {region}")
        for field in ("start", "end"):
            if not edtf_ok(scope.get(field)):
                err(f"scope.{field} が EDTF に合わない: {scope.get(field)!r}")
        topics = scope.get("topics")
        if not isinstance(topics, list) or not topics:
            err("scope.topics は1件以上にする")
        else:
            for topic in topics:
                if not isinstance(topic, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", topic):
                    err(f"scope.topics は kebab-case: {topic!r}")

        about = context.get("about")
        if not isinstance(about, list):
            err("about は配列にする")
            about = []
        if context.get("kind") == "historical" and not about:
            err("historical context は about が1件以上必要")
        for entity_id in about:
            if entity_id not in entities:
                err(f"about の参照先が存在しない: {entity_id}")

        sources = context.get("sources")
        if not isinstance(sources, list):
            err("sources は配列にする")
            sources = []
        signals = context.get("signals")
        if not isinstance(signals, list):
            err("signals は配列にする")
            signals = []
        if context.get("status") in CONTEXT_STATUSES and not signals:
            err(f"{context.get('status')} は signal が1件以上必要")
        if context.get("status") in CONTEXT_STATUSES and not sources:
            err(f"{context.get('status')} は source が1件以上必要")

        seen_ids = set()
        seen_claims = set()
        dimensions_to_signals = {}
        all_holders = set()
        all_signal_sources = set()
        hypothesis_count = 0
        for signal in signals:
            if not isinstance(signal, dict):
                err("signal はマッピングにする")
                continue
            signal_id = signal.get("id")
            shown_id = signal_id if isinstance(signal_id, str) else "<signal>"
            if not isinstance(signal_id, str) or not SIGNAL_ID_RE.fullmatch(signal_id):
                err(f"signal id は s + 3桁数字: {signal_id!r}", shown_id)
            if signal_id in seen_ids:
                err("signal id が重複", shown_id)
            seen_ids.add(signal_id)

            dimension = signal.get("dimension")
            if dimension not in dimension_ids:
                err(f"dimension が語彙外: {dimension!r}", shown_id)
            dimensions_to_signals.setdefault(dimension, []).append(signal)
            direction = signal.get("direction")
            if not _is_int(direction) or direction not in range(-2, 3):
                err(f"direction は整数 -2〜2: {direction!r}", shown_id)
            salience = signal.get("salience")
            if not _is_int(salience) or salience not in range(1, 4):
                err(f"salience は整数 1〜3: {salience!r}", shown_id)
            certainty = signal.get("certainty")
            if certainty not in certainty_weights:
                err(f"certainty が語彙外: {certainty!r}", shown_id)
            if certainty == "hypothesis":
                hypothesis_count += 1
            holders = signal.get("holders")
            if not isinstance(holders, list) or not holders:
                err("holders は1件以上にする", shown_id)
                holders = []
            for holder in holders:
                if holder not in holder_roles:
                    err(f"holder が語彙外: {holder!r}", shown_id)
                all_holders.add(holder)
            for field in ("claim", "note"):
                if not isinstance(signal.get(field), str) or not signal.get(field).strip():
                    err(f"{field} は空でない文章にする", shown_id)
            source = signal.get("source")
            source_valid = isinstance(source, str) and (
                HTTP_RE.match(source)
                or (source in entities and entities[source].get("type") == "source")
            )
            if not source_valid:
                err(f"source は既存 source ID または http/https URL: {source!r}", shown_id)
            if source not in sources:
                err("signal.source が context の sources にない", shown_id)
            all_signal_sources.add(source)
            duplicate_key = (dimension, source, signal.get("claim"))
            if duplicate_key in seen_claims:
                err("dimension・source・claim が同一の signal が重複", shown_id)
            seen_claims.add(duplicate_key)

        for heading in FIXED_HEADINGS:
            if not re.search(rf"^## {re.escape(heading)}\s*$", body, re.MULTILINE):
                err(f"本文の固定見出しがない: ## {heading}")
        if "TODO" in yaml.safe_dump(_public_context(context), allow_unicode=True) or "TODO" in body:
            err("TODO が残っている")

        if context.get("status") == "verified":
            populated_dimensions = {d for d, items in dimensions_to_signals.items() if d in dimension_ids and items}
            unique_sources = {s for s in all_signal_sources if s}
            if len(signals) < 12:
                err("verified は signal が12件以上必要")
            if len(populated_dimensions) < 8:
                err("verified は8軸以上必要")
            if len(unique_sources) < 6:
                err("verified は一意な source が6件以上必要")
            if len(all_holders) < 3:
                err("verified は holders が3役割以上必要")
            if hypothesis_count:
                err("verified に hypothesis signal は置けない")
            counter_section = _body_section(body, "反対証拠・内部差")
            for dimension, items in dimensions_to_signals.items():
                positive = [s for s in items if _is_int(s.get("direction")) and s["direction"] > 0]
                negative = [s for s in items if _is_int(s.get("direction")) and s["direction"] < 0]
                if positive and negative:
                    positive_noted = any(isinstance(s.get("id"), str) and s["id"] in counter_section
                                          for s in positive)
                    negative_noted = any(isinstance(s.get("id"), str) and s["id"] in counter_section
                                          for s in negative)
                    if not positive_noted or not negative_noted:
                        err(f"verified の反対証拠節に {dimension} の正負 signal ID が揃っていない")
    return errors


def _dimension_order(config):
    return [d["id"] for d in sorted(config["dimensions"], key=lambda d: d["index"])]


def compute_context_vector(context, config):
    """1 context分の説明可能な固定軸ベクトルを計算する。"""
    order = _dimension_order(config)
    certainty_weights = config["certainty_weights"]
    signals = sorted(context.get("signals") or [], key=lambda signal: signal["id"])
    dimensions = {}
    vector = []
    populated = 0
    for dimension_id in order:
        items = [signal for signal in signals if signal.get("dimension") == dimension_id]
        if not items:
            dimensions[dimension_id] = None
            vector.append(None)
            continue
        populated += 1
        weighted = []
        for signal in items:
            certainty = certainty_weights[signal["certainty"]]
            weight = signal["salience"] * certainty
            value = signal["direction"] / 2
            weighted.append((signal, certainty, weight, value))
        weight_sum = sum(item[2] for item in weighted)
        value = sum(weight * x for _signal, _certainty, weight, x in weighted) / weight_sum
        salience_sum = sum(item[0]["salience"] for item in weighted)
        certainty_mean = sum(item[0]["salience"] * item[1] for item in weighted) / salience_sum
        source_count = len({item[0]["source"] for item in weighted})
        holders = {holder for item in weighted for holder in item[0]["holders"]}
        holder_count = len(holders)
        salience = min(1, salience_sum / 9)
        polarization = math.sqrt(sum(weight * (x - value) ** 2 for _s, _c, weight, x in weighted) / weight_sum)
        confidence = min(1, source_count / 3) * min(1, holder_count / 2) * certainty_mean
        rounded_value = round(value, 6)
        dimensions[dimension_id] = {
            "value": rounded_value,
            "salience": round(salience, 6),
            "polarization": round(polarization, 6),
            "confidence": round(confidence, 6),
            "signal_count": len(items),
            "source_count": source_count,
            "holder_count": holder_count,
            "signal_ids": [item[0]["id"] for item in weighted],
        }
        vector.append(rounded_value)
    return {
        "label_ja": context["label_ja"],
        "kind": context["kind"],
        "status": context["status"],
        "scope": context["scope"],
        "about": context.get("about") or [],
        "coverage": round(populated / len(order), 6),
        "vector": vector,
        "dimensions": dimensions,
    }


def compare_vectors(context_a, context_b, config):
    """2 contextを比較する。比較可能軸4未満ならNone。"""
    a_id, b_id = context_a["id"], context_b["id"]
    if a_id == b_id:
        return None
    a, b = compute_context_vector(context_a, config), compute_context_vector(context_b, config)
    rows = []
    index = {dimension_id: i for i, dimension_id in enumerate(_dimension_order(config))}
    for dimension_id in _dimension_order(config):
        da, db = a["dimensions"][dimension_id], b["dimensions"][dimension_id]
        if da is None or db is None or da["confidence"] < 0.25 or db["confidence"] < 0.25:
            continue
        axis_weight = min(da["salience"], db["salience"]) * min(da["confidence"], db["confidence"])
        direction_similarity = 1 - abs(da["value"] - db["value"]) / 2
        polarization_similarity = 1 - abs(da["polarization"] - db["polarization"])
        axis_similarity = 0.8 * direction_similarity + 0.2 * polarization_similarity
        rows.append({
            "id": dimension_id,
            "axis_weight": round(axis_weight, 6),
            "direction_similarity": round(direction_similarity, 6),
            "polarization_similarity": round(polarization_similarity, 6),
            "axis_similarity": round(axis_similarity, 6),
        })
    if len(rows) < 4:
        return None
    weight_sum = sum(row["axis_weight"] for row in rows)
    raw_similarity = sum(row["axis_weight"] * row["axis_similarity"] for row in rows) / weight_sum
    coverage_factor = min(1, len(rows) / 8)
    aligned = sorted(rows, key=lambda row: (-(row["axis_weight"] * row["axis_similarity"]), index[row["id"]]))
    divergent = sorted(rows, key=lambda row: (-(row["axis_weight"] * (1 - row["axis_similarity"])), index[row["id"]]))
    first, second = sorted((a_id, b_id))
    return {
        "a": first,
        "b": second,
        "similarity": round(raw_similarity * coverage_factor, 6),
        "raw_similarity": round(raw_similarity, 6),
        "coverage_factor": round(coverage_factor, 6),
        "comparable_dimension_count": len(rows),
        "dimensions": rows,
        "aligned": [row["id"] for row in aligned[:3]],
        "divergent": [row["id"] for row in divergent[:3]],
    }


def compute_input_digest(config_path, contexts_dir):
    """configとcontexts直下のraw bytesから決定論的SHA-256を作る。"""
    config_path = Path(config_path).resolve()
    contexts_dir = Path(contexts_dir).resolve()
    root = config_path.parent.parent
    files = [config_path] + sorted(contexts_dir.glob("*.md"))
    digest = hashlib.sha256()
    for path in sorted(files, key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()
