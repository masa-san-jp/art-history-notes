#!/usr/bin/env python3
"""Validate entity frontmatter and emit data/graph.json.

The markdown files are the source of truth. This turns their frontmatter into one
graph so the collection can be queried by time, space, or relation instead of only
being read file by file.

    python3 tools/build_graph.py            # validate + write data/graph.json
    python3 tools/build_graph.py --check    # validate only, exit 1 on any error
"""

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "entities"
OUT = ROOT / "data" / "graph.json"

TYPES = {"artist", "work", "movement", "place", "concept", "event"}
DIR_FOR_TYPE = {
    "artist": "artists",
    "work": "works",
    "movement": "movements",
    "place": "places",
    "concept": "concepts",
    "event": "events",
}
RELATIONS = {
    "created_by", "belongs_to", "taught_by", "influenced_by", "responds_to",
    "depicts", "member_of", "exhibited_at", "part_of", "precedes", "documented_in",
}
SPACE_ROLES = {"created_in", "held_at", "active_in", "born_in", "died_in", "sited_in"}
STATUSES = {"stub", "draft", "verified"}
INVERSE = {
    "created_by": "created", "belongs_to": "has_member", "taught_by": "taught",
    "influenced_by": "influenced", "responds_to": "answered_by", "depicts": "depicted_in",
    "member_of": "has_member", "exhibited_at": "exhibited", "part_of": "has_part",
    "precedes": "follows", "documented_in": "documents",
}


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("frontmatter がない（先頭が --- で始まっていない）")
    _, block, _ = text.split("---\n", 2)
    return yaml.safe_load(block) or {}


def validate(meta, path, errors):
    rel = path.relative_to(ROOT)
    def err(msg):
        errors.append(f"{rel}: {msg}")

    for key in ("id", "type", "label_ja", "sources", "status", "updated"):
        if not meta.get(key):
            err(f"必須項目 {key} が空")

    etype = meta.get("type")
    if etype not in TYPES:
        err(f"未知の type: {etype}")
    elif meta.get("id"):
        expected_id = f"{etype}/{path.stem}"
        if meta["id"] != expected_id:
            err(f"id とパスが不一致（id={meta['id']} / 期待={expected_id}）")
        if path.parent.name != DIR_FOR_TYPE[etype]:
            err(f"type={etype} は entities/{DIR_FOR_TYPE[etype]}/ に置く")

    if meta.get("status") not in STATUSES:
        err(f"status は {sorted(STATUSES)} のどれか（今: {meta.get('status')}）")

    for r in meta.get("relations") or []:
        if r.get("type") not in RELATIONS:
            err(f"未知の関係 type: {r.get('type')}")
    for s in meta.get("space") or []:
        if s.get("role") not in SPACE_ROLES:
            err(f"未知の space role: {s.get('role')}")


def main():
    check_only = "--check" in sys.argv
    entities, edges, errors = {}, [], []

    for path in sorted(ENTITIES.rglob("*.md")):
        try:
            meta = read_frontmatter(path)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        validate(meta, path, errors)
        eid = meta.get("id")
        if eid in entities:
            errors.append(f"{path.relative_to(ROOT)}: id が重複: {eid}")
        entities[eid] = {**meta, "path": str(path.relative_to(ROOT))}
        for r in meta.get("relations") or []:
            edges.append({"from": eid, "type": r.get("type"), "to": r.get("target")})
        for s in meta.get("space") or []:
            edges.append({"from": eid, "type": s.get("role"), "to": s.get("target")})

    for edge in edges:
        if edge["to"] not in entities:
            errors.append(f"{edge['from']}: 存在しない参照先 {edge['to']}（{edge['type']}）")

    if errors:
        print(f"✗ {len(errors)} 件:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    edges += [
        {"from": e["to"], "type": INVERSE[e["type"]], "to": e["from"], "derived": True}
        for e in edges if e["type"] in INVERSE
    ]

    if check_only:
        print(f"✓ {len(entities)} エンティティ / {len(edges)} 関係 — 問題なし")
        return 0

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(
        # default=str: YAML の日付は date 型で入ってくる
        json.dumps({"entities": entities, "edges": edges}, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    by_status = {}
    for e in entities.values():
        by_status[e.get("status")] = by_status.get(e.get("status"), 0) + 1
    print(f"✓ {OUT.relative_to(ROOT)} を書いた — {len(entities)} エンティティ / {len(edges)} 関係")
    print(f"  status: {by_status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
