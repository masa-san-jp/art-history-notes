from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import operation_tags as tags
from test_export_signals import movement


class OperationTagTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        meta = movement(); meta['sources'] = [{'url': 'https://example.test/source', 'kind': 'primary'}]
        self.records = [(Path(meta['path']), meta, '## 定義\n条件を待ち決定を後に回す。')]
        self.vocab = {'contract_version':'operation-vocabulary/v1', 'operations':[
            {'id':'defer', 'label':'決定の先送り', 'definition':'条件が整うまで決定を後に回す。'}]}
        self.patches = [mock.patch.object(tags, 'load_entities', return_value=({}, self.records)),
                        mock.patch.object(tags, 'vocabulary', return_value=self.vocab)]
        for patch in self.patches: patch.start(); self.addCleanup(patch.stop)
        self.tagger = tags.Tagger(self.root / 'state', output=self.root / 'tags.json')

    def answer(self, report, value):
        request = report['next_action']['request']
        return self.tagger.answer({'contract_version':'element-answer/v1',
            **{key:request[key] for key in ('run_id','element_id','attempt')}, 'value':value})

    def finished(self):
        report = self.tagger.next()
        report = self.answer(report, 'defer')
        report = self.answer(report, '決定を後に回す')
        return self.answer(report, tags.STOP)

    def test_choice_and_evidence_are_separate_and_resume_same_request(self):
        report = self.tagger.next()
        self.assertEqual('choice', report['next_action']['request']['answer_format']['type'])
        report = self.answer(report, 'defer')
        self.assertEqual('text', report['next_action']['request']['answer_format']['type'])
        self.assertEqual(report, self.tagger.next())
        document = json.loads(self.tagger.output.read_text())
        self.assertEqual([], document['records']['movement/example']['tags'])

    def test_wrong_evidence_retries_selected_operation_without_normalization(self):
        report = self.answer(self.tagger.next(), 'defer')
        report = self.answer(report, '決定を 後に回す')
        self.assertEqual(2, report['next_action']['request']['attempt'])
        report = self.answer(report, '決定を後に回す')
        self.assertNotIn('defer', report['next_action']['request']['answer_format']['choices'])
        self.assertEqual('COMPLETED', self.answer(report, tags.STOP)['status'])

    def test_unknown_choice_and_identity_are_rejected(self):
        report = self.answer(self.tagger.next(), 'unknown')
        self.assertEqual(2, report['next_action']['request']['attempt'])
        request = report['next_action']['request']
        with self.assertRaisesRegex(ValueError, 'identity'):
            self.tagger.answer({'contract_version':'element-answer/v1','run_id':'other',
                'element_id':request['element_id'],'attempt':2,'value':tags.STOP})

    def test_stop_completes_empty_tags_without_inventing_evidence(self):
        report = self.answer(self.tagger.next(), tags.STOP)
        self.assertEqual('COMPLETED', report['status'])
        self.assertEqual([], json.loads(self.tagger.output.read_text())['records']['movement/example']['tags'])

    def test_validation_checks_coverage_vocabulary_body_and_verbatim_source(self):
        self.finished(); document = json.loads(self.tagger.output.read_text())
        tags.validate_tags(self.records, document, self.vocab)
        for change in ('coverage','vocabulary','body','evidence','locator','refs','duplicate','unfinished'):
            bad = deepcopy(document); record = bad['records']['movement/example']
            if change == 'coverage': bad['records'] = {}
            elif change == 'vocabulary': bad['vocabulary_sha256'] = '0'*64
            elif change == 'body': record['content_sha256'] = '0'*64
            elif change == 'unfinished': record['completed'] = False
            elif change == 'duplicate': record['tags'].append(deepcopy(record['tags'][0]))
            elif change == 'evidence': record['tags'][0]['evidence'] = '決定を 後に回す'
            elif change == 'locator': record['tags'][0]['source_locator'] = 'other'
            else: record['tags'][0]['source_refs'] = ['https://example.test/other']
            with self.assertRaises(ValueError, msg=change): tags.validate_tags(self.records, bad, self.vocab)

    def test_body_and_vocabulary_drift_stop_resume(self):
        self.tagger.next()
        self.tagger.pool['movement/example'][0]['text'] += '変更'
        with self.assertRaisesRegex(ValueError, 'changed'): self.tagger.next()

    def test_retry_budget_blocks_only_failed_element(self):
        report = self.answer(self.tagger.next(), 'defer')
        for _ in range(5): report = self.answer(report, 'not in body')
        self.assertEqual('BLOCKED', report['status'])
        self.assertIsNone(report['next_action'])
        self.assertEqual('movement.example.evidence.1', report['blocked']['element_id'])
        self.assertEqual([], json.loads(self.tagger.output.read_text())['records']['movement/example']['tags'])

    def test_owner_lead_text_is_available_without_changing_cited_export(self):
        from export_signals import entity_content
        meta = self.records[0][1]; body = self.records[0][2]
        self.assertEqual([], entity_content(meta, body))
        self.assertEqual('条件を待ち決定を後に回す。', tags.tagging_content(meta, body)[0]['text'])
