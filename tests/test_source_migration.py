import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(ROOT / "tools"))

import audit_source_migration
import bundle
import new_entity
from kb import (normalize_source, normalize_sources, normalized_meta,
                source_validation_errors)


class SourceNormalizationTests(unittest.TestCase):
    def test_legacy_and_object_share_url_internal_representation(self):
        legacy = normalize_source("https://example.org/source")
        structured = normalize_source({"url": "https://example.org/source", "kind": "primary",
                                       "note": "同時代資料"})
        self.assertEqual(legacy["url"], structured["url"])
        self.assertEqual("reference", legacy["kind"])
        self.assertEqual("primary", structured["kind"])

    def test_new_source_rejects_unknown_kind_invalid_url_and_duplicate(self):
        sources = [
            {"url": "https://example.org/source", "kind": "unknown"},
            {"url": "not-a-url", "kind": "reference"},
            {"url": "https://example.org/source", "kind": "reference"},
        ]
        errors = "\n".join(source_validation_errors(sources, "fixture"))
        self.assertIn("kind が語彙外", errors)
        self.assertIn("scheme/host", errors)
        self.assertIn("URLが重複", errors)

    def test_primary_requires_note(self):
        errors = source_validation_errors([{"url": "https://example.org/source", "kind": "primary"}], "fixture")
        self.assertTrue(any("primary" in error and "note" in error for error in errors))

    def test_normalized_meta_does_not_modify_input(self):
        meta = {"sources": ["https://example.org/source"]}
        normalized = normalized_meta(meta)
        self.assertEqual("https://example.org/source", meta["sources"][0])
        self.assertEqual({"url": "https://example.org/source", "kind": "reference"}, normalized["sources"][0])


class ConsumerTests(unittest.TestCase):
    def test_bundle_keeps_kind_and_note(self):
        entities = {
            "movement/example": {"id": "movement/example", "path": "entities/movements/example.md",
                                 "type": "movement", "label_ja": "例", "status": "draft",
                                 "sources": [{"url": "https://example.org/source", "kind": "primary", "note": "同時代資料"}]},
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "entities" / "movements" / "example.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\nid: movement/example\n---\n\n本文\n", encoding="utf-8")
            with mock.patch.object(bundle, "ROOT", root):
                text = bundle.render(["movement/example"], entities, [], "例")
        self.assertIn("kind: primary", text)
        self.assertIn("同時代資料", text)

    def test_new_entity_template_uses_object_source(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.md"
            with mock.patch.object(new_entity, "ENTITIES", Path(directory)), \
                    mock.patch.object(new_entity, "DIR_FOR_TYPE", {"movement": "."}), \
                    mock.patch.object(new_entity, "URI_PREFIX", "urn:ahn:"):
                # mainの出力先だけを一時ディレクトリへ向けるため、argparseを直接差し替える。
                with mock.patch.object(sys, "argv", ["new_entity.py", "movement", "example", "--ja", "例"]):
                    self.assertEqual(0, new_entity.main())
            text = path.read_text(encoding="utf-8")
        self.assertIn("url: https://example.org/source", text)
        self.assertIn("kind: reference", text)


class AuditTests(unittest.TestCase):
    def test_audit_counts_fixture_files_and_check_type_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            movements = root / "movements"
            contexts = root / "contexts"
            movements.mkdir()
            contexts.mkdir()
            frontmatter = "---\nid: movement/example\nsources:\n  - https://example.org/legacy\n---\n"
            (movements / "example.md").write_text(frontmatter, encoding="utf-8")
            (contexts / "example.md").write_text(
                "---\nid: context/example\nsources:\n  - url: https://example.org/new\n    kind: institutional\n---\n",
                encoding="utf-8",
            )
            with mock.patch.object(audit_source_migration, "TYPE_DIRS",
                                   {"movement": movements, "context": contexts}):
                payload = audit_source_migration.build_report()
                self.assertEqual(1, payload["reports"][0]["legacy_item_count"])
                self.assertEqual(0, payload["reports"][1]["legacy_item_count"])
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(1, audit_source_migration.main(["--check-type", "movement"]))
                self.assertIn("legacy_item_count", output.getvalue())


if __name__ == "__main__":
    unittest.main()
