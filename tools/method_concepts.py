#!/usr/bin/env python3
"""共有する手法 concept の判定・構造検証。

`theme_research.py` の候補生成と `build_graph.py` / research intake の検証が
別々の判定を持つと、同じ候補が movement と concept の間を揺れる。このモジュール
は版付き config を唯一のルールとして読み、判定理由と必須フィールドを共通化する。
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from kb import CONFIG, ROOT


CONFIG_PATH = CONFIG / "method-concepts.yaml"
CONTRACT = "method-concepts/v1"
REQUIRED_METHOD_FIELDS = ("fixes", "varies", "requires", "origin_domain")


def load_method_config(path: Path = CONFIG_PATH) -> dict:
    """版付きの判定規則を読み、機械判定に必要な shape を検証する。"""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if data.get("contract_version") != CONTRACT:
        raise ValueError(f"{path}: contract_version は {CONTRACT} でなければならない")
    rules = data.get("classification")
    if not isinstance(rules, dict):
        raise ValueError(f"{path}: classification が無い")
    for key in ("default_entity_type", "method_entity_kind", "method_entity_type",
                "method_term_patterns", "style_term_exclusions", "origin_domains",
                "required_method_fields", "enforced_statuses"):
        if key not in rules:
            raise ValueError(f"{path}: classification.{key} が無い")
    if rules["default_entity_type"] != "movement":
        raise ValueError(f"{path}: movement が既定でなければならない")
    if rules["method_entity_kind"] != "method" or rules["method_entity_type"] != "concept":
        raise ValueError(f"{path}: method は concept として宣言する")
    if tuple(rules["required_method_fields"]) != REQUIRED_METHOD_FIELDS:
        raise ValueError(f"{path}: required_method_fields が {REQUIRED_METHOD_FIELDS} と一致しない")
    if not rules["origin_domains"] or not rules["enforced_statuses"]:
        raise ValueError(f"{path}: origin_domains / enforced_statuses は空にできない")
    return data


def _nonempty_string_list(value, field: str) -> list[str]:
    if not isinstance(value, list) or not value:
        return [f"method.{field} は1件以上の配列が必要"]
    if any(not isinstance(item, str) or not item.strip() for item in value):
        return [f"method.{field} は空でない文字列の配列が必要"]
    return []


def method_validation_errors(method, *, config: dict | None = None) -> list[str]:
    """方法記述の閉じた構造を検証する。空の殻は通さない。"""
    config = config or load_method_config()
    rules = config["classification"]
    if not isinstance(method, dict):
        return ["method はmapが必要"]
    expected = set(rules["required_method_fields"])
    unknown = set(method) - expected
    missing = expected - set(method)
    errors = []
    if unknown:
        errors.append(f"method に未知のkey: {sorted(unknown)}")
    if missing:
        errors.append(f"method に必須keyが無い: {sorted(missing)}")
    for field in ("fixes", "varies", "requires"):
        errors.extend(_nonempty_string_list(method.get(field), field))
    if method.get("origin_domain") not in rules["origin_domains"]:
        errors.append(f"method.origin_domain は {rules['origin_domains']} のどれか")
    return errors


def _exact_type(recon_result: dict, exact_ids: list[str]) -> str | None:
    for hit in recon_result.get("hits") or []:
        if hit.get("id") in exact_ids:
            return hit.get("type")
    # candidate_template の旧呼び出しは exact_label_hits だけを渡すため、IDの
    # namespace も決定根拠として読む。既存完全一致を movement に戻さない。
    for entity_id in exact_ids:
        if isinstance(entity_id, str) and "/" in entity_id:
            return entity_id.split("/", 1)[0]
    return None


def classify(term: str, recon_result: dict, *, declaration: dict | None = None,
             config: dict | None = None) -> dict:
    """movement/concept を決定し、再現可能な理由を返す。

    優先順は「既存の完全一致」→「candidate の method 宣言」→「版付き config の
    語規則」→「movement 既定」。既存 entity を別型へ移動させないことを優先する。
    """
    config = config or load_method_config()
    rules = config["classification"]
    exact_ids = list(recon_result.get("exact_label_hits") or [])
    exact_type = _exact_type(recon_result, exact_ids)
    if exact_ids:
        entity_type = exact_type or rules["default_entity_type"]
        exact_hit = next((hit for hit in recon_result.get("hits") or []
                          if hit.get("id") in exact_ids), None)
        return {"entity_type": entity_type,
                "is_method": bool(exact_hit and exact_hit.get("is_method")),
                "reason": "existing-exact-label", "rule_version": CONTRACT,
                "conflict": None}

    declaration = declaration or {}
    declared_kind = declaration.get("entity_kind")
    if declared_kind == rules["method_entity_kind"]:
        method = declaration.get("method")
        return {"entity_type": rules["method_entity_type"], "is_method": True,
                "reason": "candidate-declared-method", "rule_version": CONTRACT,
                "conflict": None, "method_errors": method_validation_errors(method, config=config)}
    if declared_kind and declared_kind != rules["method_entity_kind"]:
        return {"entity_type": rules["default_entity_type"], "is_method": False,
                "reason": "candidate-declared-movement", "rule_version": CONTRACT,
                "conflict": None}

    normalized = term.strip().casefold()
    if normalized in {str(value).casefold() for value in rules["style_term_exclusions"]}:
        return {"entity_type": rules["default_entity_type"], "is_method": False,
                "reason": "style-name-exclusion", "rule_version": CONTRACT,
                "conflict": None}
    for pattern in rules["method_term_patterns"]:
        if re.search(pattern, term, flags=re.IGNORECASE):
            return {"entity_type": rules["method_entity_type"], "is_method": True,
                    "reason": "configured-method-term", "rule_version": CONTRACT,
                    "conflict": None, "method_errors": [
                        "candidate.entity_kind=method と method.* を埋める"]}
    return {"entity_type": rules["default_entity_type"], "is_method": False,
            "reason": "default-movement", "rule_version": CONTRACT, "conflict": None}


def method_concept_ids(entities: dict) -> set[str]:
    """方法記述を宣言した concept の集合（legacy concept は除外）。"""
    return {eid for eid, meta in entities.items()
            if meta.get("type") == "concept" and meta.get("method") is not None}
