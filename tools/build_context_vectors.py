#!/usr/bin/env python3
"""contextを検証し、決定論的なベクトルと類似度を生成する。"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import tempfile
from pathlib import Path

import yaml

from context_kb import (compare_vectors, compute_context_vector, compute_input_digest,
                        load_contexts, validate_contexts)
from kb import ROOT, load_entities


CONFIG_PATH = ROOT / "config" / "context-dimensions.yaml"
CONTEXTS_DIR = ROOT / "contexts"
VECTORS_PATH = ROOT / "data" / "context-vectors.json"
SIMILARITY_PATH = ROOT / "data" / "context-similarity.json"


def load_context_config():
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
    regions = yaml.safe_load((ROOT / "config" / "regions.yaml").read_text(encoding="utf-8")) or {}
    config["regions"] = list((regions.get("buckets") or {}).keys())
    return config


def atomic_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                         prefix=f".{path.name}.", suffix=".tmp",
                                         delete=False) as handle:
            handle.write(payload)
            temporary = Path(handle.name)
        temporary.replace(path)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


def build_payloads(contexts, config, input_digest):
    order = [item["id"] for item in sorted(config["dimensions"], key=lambda item: item["index"])]
    vectors = {
        "schema_version": 1,
        "input_digest": input_digest,
        "dimension_order": order,
        "contexts": {
            context_id: compute_context_vector(contexts[context_id], config)
            for context_id in sorted(contexts)
        },
    }
    pairs = []
    for a_id, b_id in itertools.combinations(sorted(contexts), 2):
        pair = compare_vectors(contexts[a_id], contexts[b_id], config)
        if pair is not None:
            pairs.append(pair)
    similarity = {
        "schema_version": 1,
        "input_digest": input_digest,
        "pairs": pairs,
    }
    return vectors, similarity


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="読み込みと検証だけ行い、書き込まない")
    args = parser.parse_args(argv)
    try:
        config = load_context_config()
        entities, _records = load_entities()
        contexts = load_contexts(CONTEXTS_DIR, ROOT)
    except Exception as exc:
        print(f"✗ 読み込み失敗: {exc}", file=sys.stderr)
        return 1
    errors = validate_contexts(contexts, entities, config)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.check:
        print(f"✓ {len(contexts)} contexts — 問題なし")
        return 0
    input_digest = compute_input_digest(CONFIG_PATH, CONTEXTS_DIR)
    vectors, similarity = build_payloads(contexts, config, input_digest)
    atomic_json(VECTORS_PATH, vectors)
    atomic_json(SIMILARITY_PATH, similarity)
    print(f"✓ {len(contexts)} contexts / {len(similarity['pairs'])} comparisons")
    return 0


if __name__ == "__main__":
    sys.exit(main())
