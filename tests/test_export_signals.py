import contextlib
import copy
import io
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import export_signals


def movement(status="draft", space=None):
    return {
        "id": "movement/example",
        "path": "entities/movements/example.md",
        "type": "movement",
        "kind": "retrospective",
        "label_ja": "例",
        "label_en": "Example",
        "status": status,
        "time": {"start": "1900", "end": ".."},
        "space": space or [{"role": "originated_in", "target": "place/a"}],
        "relations": [{
            "type": "influenced_by",
            "target": "movement/other",
            "certainty": "scholarly",
            "source": "https://example.test/source",
        }],
    }


class ExportSignalsTests(unittest.TestCase):
    def test_content_keeps_only_cited_definition_paragraphs_and_adjacent_quote(self):
        meta = movement()
        meta['sources'] = [{'url': 'https://example.test/source', 'kind': 'primary'}]
        body = ('## 定義と範囲\n\n無出典の説明。\n\n'
                '操作を遅らせる（[資料](https://example.test/source)）。\n\n'
                '> Delay execution.\n\n出典なしの追記。\n\n'
                '## 未確認\n[資料](https://example.test/source) 未確認の仮説。\n')
        content = export_signals.entity_content(meta, body)
        self.assertEqual(['操作を遅らせる（[資料](https://example.test/source)）。', '> Delay execution.'],
                         [item['text'] for item in content])
        self.assertTrue(all(item['source_refs'] == ['https://example.test/source'] for item in content))
        self.assertTrue(all(item['source_locator'].endswith('#定義と範囲') for item in content))

    def test_uncited_or_unregistered_source_is_never_content(self):
        meta = movement()
        meta['sources'] = [{'url': 'https://example.test/source', 'kind': 'primary'}]
        for body in ('## 定義\n本文だけ。', '## 定義\nhttps://other.test/source 本文。',
                     '## 定義\nhttps://example.test/source-unrelated 本文。',
                     '## 未着手\nhttps://example.test/source 仮説。'):
            self.assertEqual([], export_signals.entity_content(meta, body))

    def test_cli_uses_loaded_markdown_body_for_movement_content(self):
        meta = movement()
        meta['sources'] = [{'url': 'https://example.test/source', 'kind': 'primary'}]
        body = '## 定義\n操作を待つ [資料](https://example.test/source)'
        stdout = io.StringIO()
        with mock.patch.object(export_signals, 'load_entities', return_value=(
            {meta['id']: meta}, [(ROOT / meta['path'], meta, body)])), \
             mock.patch.object(export_signals, '_head_commit', return_value='a' * 40), \
             mock.patch.object(sys, 'argv', ['export_signals.py', '--purpose', 'test']), \
             contextlib.redirect_stdout(stdout):
            self.assertEqual(0, export_signals.main())
        import json
        record = json.loads(stdout.getvalue())['signals'][0]
        self.assertEqual('操作を待つ [資料](https://example.test/source)', record['content'][0]['text'])
        self.assertEqual([meta['label_ja'], meta['label_en']], record['entity_labels'])

    def test_content_limit_is_per_entity_and_preserves_native_prefix(self):
        meta = movement()
        meta['sources'] = [{'url': 'https://example.test/source', 'kind': 'primary'}]
        paragraph = 'https://example.test/source ' + '操作' * 2000
        content = export_signals.entity_content(meta, '## 定義\n' + paragraph)
        self.assertEqual(export_signals.CONTENT_MAX_CHARS, sum(len(item['text']) for item in content))
        self.assertEqual(paragraph[:export_signals.CONTENT_MAX_CHARS], content[0]['text'])

    def test_content_only_movement_exports_without_inventing_relations(self):
        meta = movement()
        meta['relations'] = []
        meta['sources'] = [{'url': 'https://example.test/source', 'kind': 'primary'}]
        record = export_signals.build_record(meta, {}, 'a' * 40,
            datetime(2026, 8, 14, tzinfo=timezone.utc), 'test',
            '## 定義\n操作を遅らせる https://example.test/source')
        self.assertEqual([], record['relations'])
        self.assertTrue(record['content'])
        self.assertEqual('unknown', record['validity']['status'])

    def test_method_content_preserves_fixed_varied_and_required_values_with_sources(self):
        meta = self.method_concept()
        record = self.export(meta)
        self.assertEqual(['repeat', 'initial condition', 'classify result'],
                         [item['text'] for item in record['content']])
        self.assertTrue(all(item['source_refs'] == record['source_refs'] for item in record['content']))

    def method_concept(self):
        return {
            "id": "concept/example-method", "type": "concept", "status": "draft",
            "path": "entities/concepts/example-method.md", "label_ja": "方法例",
            "label_en": "Example method", "relations": [],
            "method": {"fixes": ["repeat"], "varies": ["initial condition"],
                       "requires": ["classify result"], "origin_domain": "computation"},
            "sources": [{"url": "https://example.test/method", "kind": "primary", "note": "fixture"}],
        }

    def export(self, meta):
        return export_signals.build_record(meta, {}, "a" * 40,
                                          datetime(2026, 8, 14, tzinfo=timezone.utc), "artistic-research")

    def test_sourced_method_exports_without_a_historical_relation(self):
        meta = self.method_concept()
        original = copy.deepcopy(meta)
        record = self.export(meta)
        self.assertEqual(original, meta)
        self.assertEqual(meta["method"], record["method"])
        self.assertEqual([meta["sources"][0]["url"]], record["source_refs"])
        self.assertEqual([], record["relations"])
        self.assertEqual("concept", record["entity_kind"])
        self.assertEqual("unknown", record["validity"]["status"])
        self.assertEqual("inferred", record["certainty"]["level"])
        self.assertEqual("art-history:method:example-method", record["signal_id"])

    def test_method_requires_sources_complete_description_and_draft_status(self):
        for field in ("fixes", "varies", "requires", "origin_domain"):
            with self.subTest(field=field):
                meta = self.method_concept()
                del meta["method"][field]
                self.assertIsNone(self.export(meta))
        for status in ("stub", "unknown", None):
            meta = self.method_concept()
            meta["status"] = status
            self.assertIsNone(self.export(meta))
        for sources in ([], [{"url": "", "kind": "primary"}]):
            meta = self.method_concept()
            meta["sources"] = sources
            meta["relations"] = movement()["relations"]
            self.assertIsNone(self.export(meta))

    def test_default_cli_exports_methods_alongside_movements(self):
        method = self.method_concept()
        metas = {method["id"]: method, "movement/example": movement()}
        stdout = io.StringIO()
        with mock.patch.object(export_signals, "load_entities", return_value=(metas, [])), \
             mock.patch.object(export_signals, "_head_commit", return_value="a" * 40), \
             mock.patch.object(sys, "argv", ["export_signals.py", "--purpose", "artistic-research"]), \
             contextlib.redirect_stdout(stdout):
            self.assertEqual(0, export_signals.main())
        import json
        payload = json.loads(stdout.getvalue())
        self.assertEqual(2, payload["signal_count"])
        self.assertEqual({"concept", "retrospective"}, {r["entity_kind"] for r in payload["signals"]})

    def test_uses_method_relation_retains_source_and_certainty(self):
        meta = movement()
        meta["relations"][0].update(type="uses_method", target="concept/example-method", certainty="hypothesis")
        record = self.export(meta)
        relation = record["relations"][0]
        self.assertEqual("uses_method", relation["relation"])
        self.assertEqual("inferred", relation["certainty"]["level"])
        self.assertEqual([meta["relations"][0]["source"]], relation["evidence_refs"])

    def test_limit_preserves_movement_order_before_methods(self):
        method = self.method_concept()
        first = movement()
        second = movement()
        second["id"] = "movement/z-example"
        metas = {meta["id"]: meta for meta in (method, second, first)}
        import json
        for limit in (1, 2):
            with self.subTest(limit=limit):
                stdout = io.StringIO()
                with mock.patch.object(export_signals, "load_entities", return_value=(metas, [])), \
                     mock.patch.object(export_signals, "_head_commit", return_value="a" * 40), \
                     mock.patch.object(sys, "argv", ["export_signals.py", "--purpose", "test", "--limit", str(limit)]), \
                     contextlib.redirect_stdout(stdout):
                    self.assertEqual(0, export_signals.main())
                records = json.loads(stdout.getvalue())["signals"]
                self.assertEqual([first["id"], second["id"]][:limit], [r["entity_id"] for r in records])

    def test_explicit_concept_without_method_keeps_relation_export(self):
        entities, _records = export_signals.load_entities()
        meta = entities["concept/hurufiyya"]
        self.assertNotIn("method", meta)
        stdout = io.StringIO()
        with mock.patch.object(export_signals, "_head_commit", return_value="a" * 40), \
             mock.patch.object(sys, "argv", ["export_signals.py", "--purpose", "test", "--entity", meta["id"]]), \
             contextlib.redirect_stdout(stdout):
            self.assertEqual(0, export_signals.main())
        import json
        payload = json.loads(stdout.getvalue())
        self.assertEqual(1, payload["signal_count"])
        record = payload["signals"][0]
        self.assertEqual("art-history:hurufiyya", record["signal_id"])
        self.assertEqual(export_signals._relations(meta), record["relations"])
        self.assertNotIn("method", record)
        self.assertNotIn("source_refs", record)

    def test_method_sources_do_not_replace_relation_evidence_sources(self):
        meta = self.method_concept()
        meta["relations"] = movement()["relations"]
        relation_source = meta["relations"][0]["source"]
        meta["sources"].append({"url": relation_source, "kind": "secondary", "note": "relation fixture"})
        record = self.export(meta)
        self.assertEqual([relation_source], [s["url"] for s in record["evidence_sources"]])
        self.assertEqual(meta["sources"], record["sources"])
        self.assertEqual(sorted(s["url"] for s in meta["sources"]), record["source_refs"])

    def test_computation_method_from_398_is_exportable_as_an_unverified_seed(self):
        entities, _records = export_signals.load_entities()
        meta = entities["concept/iterated-boundary-generation"]
        record = self.export(meta)
        self.assertEqual("computation", record["method"]["origin_domain"])
        self.assertIn("https://sohl-dickstein.github.io/2024/02/12/fractal.html", record["source_refs"])
        self.assertEqual([], record["relations"])
        self.assertEqual("unknown", record["validity"]["status"])

    def test_unverified_status_is_preserved_as_unknown_validity(self):
        record = export_signals.build_record(
            movement("draft"),
            {"place/a": {"region": "europe-west"}},
            "a" * 40,
            datetime(2026, 8, 14, tzinfo=timezone.utc),
            "artistic-research",
        )
        self.assertEqual("unknown", record["validity"]["status"])
        self.assertTrue(any("draft" in item for item in record["unknowns"]))

    def test_multiple_origin_regions_are_not_reduced_to_first(self):
        record = export_signals.build_record(
            movement(space=[
                {"role": "originated_in", "target": "place/a"},
                {"role": "originated_in", "target": "place/b"},
            ]),
            {
                "place/a": {"region": "europe-west"},
                "place/b": {"region": "asia-east-japan"},
            },
            "a" * 40,
            datetime(2026, 8, 14, tzinfo=timezone.utc),
            "artistic-research",
        )
        self.assertEqual("europe-west,asia-east-japan", record["geo"])
        self.assertTrue(any("place/a" in item and "place/b" in item for item in record["unknowns"]))

    def test_image_rights_source_is_preserved(self):
        source = "https://example.test/work"
        meta = movement()
        meta["images"] = [{"url": "https://example.test/image.jpg", "source_page": source,
                            "rights_source": source, "license": "cc0"}]
        record = export_signals.build_record(
            meta,
            {"place/a": {"region": "europe-west"}},
            "a" * 40,
            datetime(2026, 8, 14, tzinfo=timezone.utc),
            "artistic-research",
        )
        self.assertEqual(source, record["images"][0]["rights_source"])

    def test_unknown_entity_returns_clean_error(self):
        stderr = io.StringIO()
        with mock.patch.object(sys, "argv", ["export_signals.py", "--purpose", "test", "--entity", "movement/missing"]), contextlib.redirect_stderr(stderr):
            self.assertEqual(1, export_signals.main())
        self.assertIn("そのIDは無い", stderr.getvalue())

    def test_dirty_checkout_is_not_used_as_commit_provenance(self):
        with mock.patch.object(export_signals.subprocess, "run") as run:
            run.return_value = mock.Mock(stdout=" M entities/example.md\n")
            with self.assertRaisesRegex(RuntimeError, "dirty"):
                export_signals._head_commit()
        self.assertEqual(1, run.call_count)


if __name__ == "__main__":
    unittest.main()
