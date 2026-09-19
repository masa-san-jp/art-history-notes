#!/usr/bin/env python3
"""テーマ起点の調査を1回まとめる — 「実行のたびに調査が回り、使うたびに厚くなる」の入口（recon）。

    python3 tools/theme_research.py --theme "ムガル絵画"
    python3 tools/theme_research.py --theme "ムガル絵画" --theme "Mughal painting" --json
    python3 tools/theme_research.py --theme "ムガル絵画" --json --budget config/theme-research.yaml

仕様: docs/theme-research-cycle.md（theme-research-cycle/v1）§5 R1。出力契約は
theme-research-recon/v1。

このスクリプト自体は調べ物をしない（Web検索・出典評価・candidate起票はエージェントの仕事）。
やることは3つだけ:

1. 検索して当たりを報告する（`bundle.py --search` と同じ検索・ログ経路を使う）
2. その検索を `data/queries.jsonl` に記録する（該当なしも記録する——探されたのに無かった、
   という需要を消さないため）。テーマ語ごとに1行
3. 現在の被覆グリッド（`data/coverage.json` の `grid`）と、予算（`config/theme-research.yaml`）を
   そのまま出す

判断（このテーマにとってどのregion×世紀の空白が関係するか、どの資料を信頼するか、
既存hitが「主題そのもの」か本文中の言及に過ぎないか）は常にエージェント側に残す——
このKBの他のツール（build_graph.py の検証 と audit.py の指摘）と同じ、
「機械的チェックと判断を混ぜない」原則に従う。exit code は常に 0。該当なしは失敗ではない。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

from kb import ROOT, load_entities, log_query, search_entities

CONTRACT = "theme-research-recon/v1"
BUDGET_CONTRACT = "theme-research-budget/v1"
COVERAGE_PATH = ROOT / "data" / "coverage.json"
BUDGET_PATH = ROOT / "config" / "theme-research.yaml"
BUDGET_KEYS = {"max_passes", "max_theme_terms", "max_candidates", "max_source_fetches", "wall_clock_seconds"}
NEXT_STEP = ("当たりが無い、または主題そのものの entity が無く stub/draft の言及だけなら調査対象。"
             "docs/agent/theme-research-task.md の手順（経路A: run内 intake／経路B: 手動昇格）に従う。"
             "予算（budget）を超えたら捏造せず止め、no-new-evidence を選ぶ。")


def hit_summary(hit_id, entities):
    meta = entities.get(hit_id) or {}
    return {
        "id": hit_id,
        "label_ja": meta.get("label_ja"),
        "label_en": meta.get("label_en"),
        "type": meta.get("type"),
        "status": meta.get("status"),
        "n_sources": len(meta.get("sources") or []),
    }


def exact_label_hits(term, hits):
    """label がテーマ語そのものである hit の id。本文中の言及だけの hit と区別するための補助。"""
    needle = term.strip().lower()
    return [h["id"] for h in hits
            if needle and needle in {str(h.get("label_ja") or "").lower(), str(h.get("label_en") or "").lower()}]


def load_grid():
    if not COVERAGE_PATH.exists():
        return None
    data = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    return data.get("grid")


def load_budget(path=BUDGET_PATH):
    """予算は有限の整数だけを許す。欠落・非整数・0以下は設定エラー（推測で補わない）。"""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if data.get("contract_version") != BUDGET_CONTRACT:
        raise ValueError(f"{path}: contract_version は {BUDGET_CONTRACT} でなければならない")
    per_run = data.get("per_run") or {}
    missing = BUDGET_KEYS - set(per_run)
    if missing:
        raise ValueError(f"{path}: per_run に {sorted(missing)} が無い")
    for k in BUDGET_KEYS:
        v = per_run[k]
        if isinstance(v, bool) or not isinstance(v, int) or v <= 0:
            raise ValueError(f"{path}: per_run.{k} は正の整数でなければならない（{v!r}）")
    if data.get("on_exhausted") != "stop":
        raise ValueError(f"{path}: on_exhausted は stop でなければならない")
    return data


def recon(term, entities):
    hit_ids = search_entities(term, entities)
    log_query(term, len(hit_ids))
    hits = [hit_summary(h, entities) for h in hit_ids]
    return {
        "theme": term,
        "hits": hits,
        "hit_count": len(hits),
        "exact_label_hits": exact_label_hits(term, hits),
    }


def build_report(terms, entities, grid, budget):
    results = [recon(t, entities) for t in terms]
    return {
        "contract_version": CONTRACT,
        "themes": [r["theme"] for r in results],
        "results": results,
        # 後方互換: 単一テーマ呼び出しの旧field（最初のテーマの値）
        "theme": results[0]["theme"],
        "hits": results[0]["hits"],
        "hit_count": results[0]["hit_count"],
        "coverage_grid": grid,
        "budget": budget,
        "next_step": NEXT_STEP,
    }


SAFE_ID = re.compile(r"[^a-z0-9]+")


def slug(term):
    """テーマ語から安全な id 断片を作る。非ASCIIは落ちるので、その場合は 'theme-<sha8>' にする。"""
    import hashlib
    s = SAFE_ID.sub("-", term.strip().lower()).strip("-")
    return s or "theme-" + hashlib.sha256(term.encode("utf-8")).hexdigest()[:8]


def candidate_template(term, recon_result, *, creator, collection, project_id, origin_instance_id,
                       run_id, code_commit, record_id=None, now=None):
    """spec §5 R3: candidate.json の骨格。statement / source_reads / entity はエージェントが埋める。

    envelope の固定 field と payload_ref / content_sha256 は既存 intake の同じ関数で計算する。
    出典・hash・主張は一切推測しない——埋まっていない箇所は missing に列挙する。
    """
    from datetime import datetime, timezone
    from research_knowledge_intake import OWNER, POLICY, canonical, digest, key

    exact = recon_result.get("exact_label_hits") or []
    target_id = exact[0] if exact else "movement/" + slug(term)
    payload = {
        "classification": "historical",
        "target_id": target_id,
        "project_id": project_id,
        "statement": "",
        "entity": None,
        "source_reads": [],
        "context_body": None,
    }
    record = {
        "contract_version": "artifact-record/v1",
        "record_id": record_id or slug(term),
        "revision": 1,
        "origin_instance_id": origin_instance_id,
        "creator_id": creator,
        "owner_repository": OWNER,
        "collection_id": collection,
        "kind": "art-history-knowledge",
        "payload_schema": POLICY,
        "payload_ref": None,
        "content_sha256": digest(canonical(payload)),
        "sources": [],
        "derived_from": [],
        "epistemic_status": "externally-supported",
        "lifecycle": "candidate",
        "applicability": {"theme": term},
        "rights": {"knowledge_write": True, "redistribute": False},
        "access_scope": "creator-private",
        "consent_ref": None,
        "created_at": (now or datetime.now(timezone.utc)).isoformat(),
        "reviewed_at": None,
        "valid_until": None,
        "producer": {"kind": "agent", "generator_version": "theme_research.py/" + CONTRACT,
                     "code_commit": code_commit, "run_id": run_id},
        "supersedes": [],
        "invalidates": [],
    }
    record["payload_ref"] = "contexts/research-memory/payloads/" + key(record) + ".json"
    missing = [
        "payload.statement: 固有の観測または解釈（空のままでは intake が拒否する）",
        "payload.source_reads: 実際に読んだ出典の snapshot hash（--source-snapshots と対で必要）",
        "payload.entity: canonical 候補なら既存 schema の frontmatter、本人解釈なら null のまま",
        "record.consent_ref: access_scope=creator-private のとき必須",
        "record.content_sha256: payload を編集したら canonical JSON の sha256 を再計算する",
    ]
    if not exact:
        missing.insert(0, f"payload.target_id: 既存 id が無いため新 id 案 '{target_id}'——dedupe（entities/ 全型の grep）を先に行う")
    return {"candidate": {"record": record, "payload": payload},
            "existing_target": exact[0] if exact else None, "missing": missing}


def validate_candidate_file(candidate_path, snapshots_path=None):
    """spec §4 [D] の前段: store 無しで既存 intake の validate_candidate を掛ける（read-only）。

    creator / collection は candidate 自身の record から取る（ここで見るのは内部整合だけ。
    store との照合は intake の prepare/commit が行う）。戻り値は {"ok": bool, ...}。
    """
    from research_knowledge_intake import IntakeError, validate_candidate
    candidate = json.loads(Path(candidate_path).read_text(encoding="utf-8"))
    snapshots = json.loads(Path(snapshots_path).read_text(encoding="utf-8")) if snapshots_path else None
    record = candidate.get("record") if isinstance(candidate, dict) else None
    if not isinstance(record, dict):
        return {"ok": False, "errors": ["candidate must contain record and payload"]}
    try:
        validate_candidate(candidate, creator=record.get("creator_id"), collection=record.get("collection_id"),
                           snapshots=snapshots)
    except (IntakeError, KeyError, TypeError, ValueError, OSError) as exc:
        return {"ok": False, "errors": [str(exc) or type(exc).__name__]}
    return {"ok": True, "target_id": candidate["payload"]["target_id"],
            "classification": candidate["payload"]["classification"],
            "n_source_reads": len(candidate["payload"]["source_reads"])}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--validate-candidate", type=Path, metavar="CANDIDATE_JSON",
                   help="candidate.json を既存 intake の validate_candidate に掛けて {ok, errors} を出す（store 不要・read-only）。"
                        "invalid なら exit 1")
    p.add_argument("--source-snapshots", type=Path, metavar="MAP_JSON",
                   help="--validate-candidate 用: URL→snapshot file の対応 JSON")
    p.add_argument("--theme", action="append",
                   help="調べたい語（人名・movement名・地域名など、自由記述）。複数回指定できる")
    p.add_argument("--json", action="store_true", help="JSON で出す（他ツール・エージェントからの呼び出し用）")
    p.add_argument("--budget", type=Path, default=BUDGET_PATH, help="予算ファイル（theme-research-budget/v1）")
    p.add_argument("--emit-candidate-template", action="store_true",
                   help="spec §5 R3: 各テーマの candidate.json 骨格を report.candidate_templates に含める（要 --creator 等）")
    p.add_argument("--creator"); p.add_argument("--collection"); p.add_argument("--project-id")
    p.add_argument("--origin-instance-id"); p.add_argument("--run-id")
    a = p.parse_args()

    if a.validate_candidate:
        result = validate_candidate_file(a.validate_candidate, a.source_snapshots)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1

    terms = [t for t in (a.theme or []) if t and t.strip()]
    if not terms:
        p.error("--theme が空（または --validate-candidate を指定する）")
    budget = load_budget(a.budget)
    limit = budget["per_run"]["max_theme_terms"]
    truncated = terms[limit:]
    terms = terms[:limit]

    entities, _ = load_entities()
    grid = load_grid()
    report = build_report(terms, entities, grid, budget)
    if truncated:
        report["truncated_themes"] = truncated

    if a.emit_candidate_template:
        needed = {"creator": a.creator, "collection": a.collection, "project_id": a.project_id,
                  "origin_instance_id": a.origin_instance_id, "run_id": a.run_id}
        absent = [k for k, v in needed.items() if not v]
        if absent:
            p.error("--emit-candidate-template には次が要る: " + ", ".join("--" + k.replace("_", "-") for k in absent))
        import subprocess
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
        code_commit = head.stdout.strip() if head.returncode == 0 else ""
        max_c = budget["per_run"]["max_candidates"]
        report["candidate_templates"] = [
            candidate_template(r["theme"], r, code_commit=code_commit, **needed)
            for r in report["results"][:max_c]
        ]
        a.json = True

    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    for r in report["results"]:
        print(f"テーマ: {r['theme']}")
        if not r["hits"]:
            print("  該当なし。data/queries.jsonl に記録した。既存の空白かどうかは coverage_grid を見て判断する。")
        else:
            print(f"  {r['hit_count']} 件ヒット（主題そのもの: {len(r['exact_label_hits'])} 件）:")
            for h in r["hits"]:
                mark = "*" if h["id"] in r["exact_label_hits"] else " "
                print(f"  {mark} {h['id']} （{h['label_ja']}／{h['status']}／出典{h['n_sources']}件）")
    if truncated:
        print(f"\n予算 max_theme_terms={limit} を超えたテーマ語は扱わなかった: {truncated}")
    print()
    print("被覆グリッド（region → {世紀: 件数}）:")
    for region, counts in sorted((grid or {}).items()):
        print(f"  {region}: {counts}")
    print()
    print("予算:", json.dumps(budget["per_run"], ensure_ascii=False))
    print()
    print("次にやること:", NEXT_STEP)
    return 0


if __name__ == "__main__":
    sys.exit(main())
