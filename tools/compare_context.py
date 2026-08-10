#!/usr/bin/env python3
"""context IDを指定し、説明可能な類似候補を表示する。"""

from __future__ import annotations

import argparse
import json
import sys

from build_context_vectors import (CONFIG_PATH, CONTEXTS_DIR, SIMILARITY_PATH, VECTORS_PATH,
                                   load_context_config)
from context_kb import compute_input_digest, load_contexts
from kb import ROOT


NOTICE = "類似は調査候補であり、同一性・影響・因果の証拠ではない"


def fail(message):
    print(message, file=sys.stderr)
    return 2


def axis_detail(axis_id, target_id, other_id, vectors, contexts, pair):
    pair_axis = next(item for item in pair["dimensions"] if item["id"] == axis_id)
    target_dimension = vectors[target_id]["dimensions"][axis_id]
    other_dimension = vectors[other_id]["dimensions"][axis_id]
    sources = []
    for context_id in (target_id, other_id):
        for signal in contexts[context_id].get("signals") or []:
            if signal.get("dimension") == axis_id and signal.get("source") not in sources:
                sources.append(signal["source"])
    return {
        "id": axis_id,
        "axis_similarity": pair_axis["axis_similarity"],
        "target": target_dimension,
        "candidate": other_dimension,
        "sources": sources,
    }


def candidate_object(target_id, pair, vectors, contexts):
    other_id = pair["b"] if pair["a"] == target_id else pair["a"]
    return {
        "id": other_id,
        "label_ja": vectors[other_id]["label_ja"],
        "similarity": pair["similarity"],
        "comparable_dimension_count": pair["comparable_dimension_count"],
        "scope": vectors[other_id]["scope"],
        "status": vectors[other_id]["status"],
        "aligned": [axis_detail(axis_id, target_id, other_id, vectors, contexts, pair)
                    for axis_id in pair["aligned"]],
        "divergent": [axis_detail(axis_id, target_id, other_id, vectors, contexts, pair)
                      for axis_id in pair["divergent"]],
    }


def render_axis(axis):
    target, candidate = axis["target"], axis["candidate"]
    return (
        f"  - `{axis['id']}`（軸類似度 {axis['axis_similarity'] * 100:.1f}%）\n"
        f"    - 対象: 方向 {target['value']}, 顕著性 {target['salience']}, "
        f"分極 {target['polarization']}, 信頼度 {target['confidence']}\n"
        f"    - 候補: 方向 {candidate['value']}, 顕著性 {candidate['salience']}, "
        f"分極 {candidate['polarization']}, 信頼度 {candidate['confidence']}\n"
        f"    - 根拠: {', '.join(axis['sources'])}"
    )


def render_markdown(target_id, vectors, candidates):
    lines = [f"# {vectors[target_id]['label_ja']} — 時代文脈の比較候補"]
    for candidate in candidates:
        lines.extend([
            "",
            f"## {candidate['label_ja']} (`{candidate['id']}`)",
            "",
            f"- 類似度: {candidate['similarity'] * 100:.1f}%",
            f"- 比較軸数: {candidate['comparable_dimension_count']}",
            f"- scope: `{json.dumps(candidate['scope'], ensure_ascii=False, sort_keys=True)}`",
            f"- status: `{candidate['status']}`",
            "- 類似上位3軸:",
        ])
        lines.extend(render_axis(axis) for axis in candidate["aligned"])
        lines.append("- 相違上位3軸:")
        lines.extend(render_axis(axis) for axis in candidate["divergent"])
    lines.extend(["", f"> {NOTICE}"])
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("context_id")
    parser.add_argument("--kind", choices=("historical", "current"))
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--format", choices=("md", "json"), default="md")
    args = parser.parse_args(argv)
    if not 1 <= args.top <= 100:
        return fail("--top は1〜100にする")
    if not VECTORS_PATH.exists() or not SIMILARITY_PATH.exists():
        return fail("生成物がない。python3 tools/build_context_vectors.py を実行してください")
    try:
        vectors_payload = json.loads(VECTORS_PATH.read_text(encoding="utf-8"))
        similarity_payload = json.loads(SIMILARITY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"生成物を読めない: {exc}")
    current_digest = compute_input_digest(CONFIG_PATH, CONTEXTS_DIR)
    if similarity_payload.get("input_digest") != current_digest \
            or vectors_payload.get("input_digest") != current_digest:
        return fail("生成物が入力と一致しない。python3 tools/build_context_vectors.py を実行してください")
    vectors = vectors_payload["contexts"]
    if args.context_id not in vectors:
        return fail(f"未知の context ID: {args.context_id}")
    contexts = load_contexts(CONTEXTS_DIR, ROOT)
    pairs = [pair for pair in similarity_payload["pairs"]
             if args.context_id in (pair["a"], pair["b"])]
    if not pairs:
        return fail(f"{args.context_id} は比較可能軸が4未満で、比較候補を生成できない")
    candidates = [candidate_object(args.context_id, pair, vectors, contexts) for pair in pairs]
    if args.kind:
        candidates = [candidate for candidate in candidates if vectors[candidate["id"]]["kind"] == args.kind]
    candidates.sort(key=lambda candidate: (-candidate["similarity"], candidate["id"]))
    candidates = candidates[:args.top]
    if args.format == "json":
        output = {
            "target": args.context_id,
            "candidates": candidates,
            "notice": NOTICE,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=False))
    else:
        print(render_markdown(args.context_id, vectors, candidates), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
