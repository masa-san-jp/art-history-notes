#!/usr/bin/env python3
"""KB の共通部品 — frontmatter の読み込み、スキーマ定義、EDTF、グラフ組み立て。

各ツール（build_graph / bundle / new_entity）はここを import する。スキーマの定義はこの1箇所。
"""

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "entities"
CONFIG = ROOT / "config"

# --- スキーマ -----------------------------------------------------------------

DIR_FOR_TYPE = {
    "person": "persons", "work": "works", "org": "orgs", "place": "places",
    "movement": "movements", "concept": "concepts", "event": "events", "source": "sources",
}
TYPES = set(DIR_FOR_TYPE)

MOVEMENT_KINDS = {"self-declared", "retrospective", "lineage-school", "period-style"}
STATUSES = {"stub", "draft", "verified"}
CERTAINTIES = {"attested", "scholarly", "hypothesis"}

# 構造的な関係（出典なしで書ける）
STRUCTURAL_RELATIONS = {
    "created_by": "created", "belongs_to": "has_member", "member_of": "has_member",
    "part_of": "has_part", "depicts": "depicted_in", "exhibited_at": "exhibited",
    "precedes": "follows", "taught_by": "taught", "documented_in": "documents",
}
# 解釈を含む関係（certainty と source を必須にする）
INTERPRETIVE_RELATIONS = {
    "influenced_by": "influenced", "responds_to": "answered_by", "derives_from": "derived_into",
    "reacts_against": "reacted_against_by", "grouped_as": "groups", "diffused_to": "received",
    "patronized_by": "patronized",
}
RELATIONS = {**STRUCTURAL_RELATIONS, **INTERPRETIVE_RELATIONS}

SPACE_ROLES = {"originated_in", "created_in", "held_at", "active_in", "born_in", "died_in", "sited_in"}

# verified を名乗るとき、項目ごとの根拠が要る field（claims ブロック）
CLAIM_FIELDS_FOR_VERIFIED = {"movement": {"time", "originated_in", "kind"}}

URI_PREFIX = "urn:ahn:"

# --- EDTF（ISO 8601-2 Level 1 サブセット）--------------------------------------
# 受ける形: 1884 / 1884-05 / 1884-05-20 / 146X / 18XX / 1503~ / 1884? / 1884%
#          .. （開いた端）/ null（不明）
EDTF_RE = re.compile(r"^(?:\.\.|(\d{4}|\d{3}X|\d{2}XX|\dXXX)(?:-\d{2}(?:-\d{2})?)?[?~%]?)$")


def edtf_ok(value):
    return value is None or (isinstance(value, str) and bool(EDTF_RE.match(value)))


def edtf_year_range(value):
    """EDTF 値から (最小年, 最大年) を返す。開いた端・不明は None。ソートと集計に使う。"""
    if not value or value == "..":
        return (None, None)
    head = value.split("-")[0].rstrip("?~%")
    if "X" not in head:
        return (int(head), int(head))
    lo = int(head.replace("X", "0"))
    hi = int(head.replace("X", "9"))
    return (lo, hi)


# --- 読み込み -----------------------------------------------------------------

def read_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("frontmatter がない（先頭が --- で始まっていない）")
    _, block, body = text.split("---\n", 2)
    return yaml.safe_load(block) or {}, body


def load_config():
    return yaml.safe_load((CONFIG / "regions.yaml").read_text(encoding="utf-8"))


def load_entities():
    """{id: meta} と、id 順の (path, meta, body) を返す。検証はしない。"""
    entities, records = {}, []
    for path in sorted(ENTITIES.rglob("*.md")):
        meta, body = read_frontmatter(path)
        meta["path"] = str(path.relative_to(ROOT))
        records.append((path, meta, body))
        if meta.get("id"):
            entities[meta["id"]] = meta
    return entities, records


def edges_of(meta):
    """1エンティティの frontmatter から出るエッジを列挙する。"""
    out = []
    for r in meta.get("relations") or []:
        out.append({"from": meta.get("id"), "type": r.get("type"), "to": r.get("target"),
                    "certainty": r.get("certainty"), "source": r.get("source")})
    for s in meta.get("space") or []:
        out.append({"from": meta.get("id"), "type": s.get("role"), "to": s.get("target")})
    return out


def build_edges(entities):
    edges = [e for meta in entities.values() for e in edges_of(meta)]
    derived = [
        {"from": e["to"], "type": RELATIONS[e["type"]], "to": e["from"], "derived": True}
        for e in edges if e["type"] in RELATIONS and e["to"] in entities
    ]
    return edges + derived


QUERY_LOG = ROOT / "data" / "queries.jsonl"


def log_query(term, hits):
    """検索を記録する。**該当なしこそ残す**——探されたのに無かった、という需要が消えないように。

    これが無いと系が一方通行になる（書く→読まれる→何も返らない）。記録した語は被覆マップに出て、
    次に何を埋めるかの判断材料になる。
    """
    import datetime, json
    QUERY_LOG.parent.mkdir(exist_ok=True)
    row = {"ts": datetime.datetime.now().isoformat(timespec="seconds"), "term": term, "hits": hits}
    with QUERY_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_queries():
    import json
    if not QUERY_LOG.exists():
        return []
    return [json.loads(l) for l in QUERY_LOG.read_text(encoding="utf-8").splitlines() if l.strip()]


def region_of(entity_id, entities):
    """エンティティの発生地から文化圏バケットを引く。辿れなければ None。"""
    meta = entities.get(entity_id) or {}
    for s in meta.get("space") or []:
        if s.get("role") == "originated_in":
            place = entities.get(s.get("target")) or {}
            return place.get("region")
    return None
