#!/usr/bin/env python3
"""構造化出典への移行残数を型別に決定論的に監査する。

    uv run --locked python tools/audit_source_migration.py
    uv run --locked python tools/audit_source_migration.py --format markdown
    uv run --locked python tools/audit_source_migration.py --check-type movement

``--check-type`` は指定型にlegacy URL文字列が残っていれば非0で終了する。
通常の正準検証は互換期間中もlegacyを読み込めるため、この監査を移行完了時のゲートにする。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
TYPE_DIRS = {
    "movement": ROOT / "entities" / "movements",
    "context": ROOT / "contexts",
    "person": ROOT / "entities" / "persons",
    "work": ROOT / "entities" / "works",
}
TYPE_ORDER = ("movement", "context", "person", "work")


def _parse(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("frontmatter がない")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("frontmatter の終端 --- がない")
    value = yaml.safe_load(parts[1]) or {}
    if not isinstance(value, dict):
        raise ValueError("frontmatter はマッピングにする")
    return value


def _paths(entity_type: str) -> list[Path]:
    directory = TYPE_DIRS[entity_type]
    paths = sorted(directory.glob("*.md"))
    if entity_type == "context":
        paths = [path for path in paths if path.name != "README.md"]
    return paths


def _source_url(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return value.get("url")
    return None


def report(entity_type: str) -> dict:
    files = []
    legacy_files = []
    parse_errors = []
    source_count = 0
    legacy_count = 0
    reference_count = 0
    missing_references = []
    for path in _paths(entity_type):
        try:
            relative = path.relative_to(ROOT).as_posix()
        except ValueError:
            # fixture/testでTYPE_DIRSだけ差し替えられた場合も決定的な名前を出す。
            relative = f"{entity_type}/{path.name}"
        files.append(relative)
        try:
            meta = _parse(path)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            parse_errors.append({"path": relative, "error": str(exc)})
            continue
        sources = meta.get("sources")
        if not isinstance(sources, list):
            continue
        source_count += len(sources)
        strings = sum(isinstance(source, str) for source in sources)
        if strings:
            legacy_files.append(relative)
            legacy_count += strings
        source_urls = {_source_url(source) for source in sources}
        for field in ("claims", "relations", "signals"):
            for index, item in enumerate(meta.get(field) or [], start=1):
                if not isinstance(item, dict) or not item.get("source"):
                    continue
                reference_count += 1
                if item["source"] not in source_urls:
                    missing_references.append({
                        "path": relative,
                        "field": field,
                        "index": index,
                        "source": item["source"],
                    })
    return {
        "type": entity_type,
        "file_count": len(files),
        "source_count": source_count,
        "legacy_file_count": len(legacy_files),
        "legacy_item_count": legacy_count,
        "reference_count": reference_count,
        "missing_reference_count": len(missing_references),
        "files": files,
        "legacy_files": legacy_files,
        "missing_references": missing_references,
        "parse_errors": parse_errors,
    }


def build_report(types: list[str] | None = None) -> dict:
    selected = types or [entity_type for entity_type in TYPE_ORDER if entity_type in TYPE_DIRS]
    return {"schema_version": 1, "reports": [report(entity_type) for entity_type in selected]}


def render_markdown(payload: dict) -> str:
    lines = ["# 構造化出典の移行監査", "", "| 型 | ファイル | source項目 | legacyファイル | legacy項目 |", "|---|---:|---:|---:|---:|"]
    for item in payload["reports"]:
        lines.append(
            f"| {item['type']} | {item['file_count']} | {item['source_count']} | "
            f"{item['legacy_file_count']} | {item['legacy_item_count']} |"
        )
    for item in payload["reports"]:
        lines += ["", f"## {item['type']} 対象ファイル", ""]
        lines.extend(f"- `{path}`" for path in item["files"])
        if item["legacy_files"]:
            lines += ["", "legacyを含むファイル:", ""]
            lines.extend(f"- `{path}`" for path in item["legacy_files"])
        for error in item["parse_errors"]:
            lines.append(f"- **読み込みエラー** `{error['path']}`: {error['error']}")
        if item["missing_references"]:
            lines += ["", "親sourcesにない根拠参照:", ""]
            lines.extend(
                f"- `{row['path']}` {row['field']}[{row['index']}]: `{row['source']}`"
                for row in item["missing_references"]
            )
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-type", choices=sorted(TYPE_DIRS), action="append",
                        help="指定型にlegacyが残っていれば非0（複数指定可）")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", help="出力先。省略時は標準出力")
    parser.add_argument("--quiet", action="store_true", help="check-typeのゲート用途でレポートを表示しない")
    args = parser.parse_args(argv)
    payload = build_report(args.check_type)
    text = (render_markdown(payload) if args.format == "markdown"
            else json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n")
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    elif not args.quiet:
        sys.stdout.write(text)
    failed = any(item["legacy_file_count"] or item["parse_errors"] or item["missing_reference_count"]
                 for item in payload["reports"])
    return 1 if args.check_type and failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
