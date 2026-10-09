from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import operation_relations as relations
import operation_tags as tags


class RelationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.vocab = tags.vocabulary()
        patch = mock.patch.object(relations, 'vocabulary', return_value=self.vocab)
        patch.start(); self.addCleanup(patch.stop)
        self.actor = relations.Relator(self.root / 'state', output=self.root / 'relations.json')

    def answer(self, report, value):
        q = report['next_action']['request']
        return self.actor.answer({'contract_version':'element-answer/v1', **{k:q[k] for k in ('run_id','element_id','attempt')}, 'value':value})

    def test_choice_reason_resume_and_symmetric_projection(self):
        report = self.actor.next()
        self.assertEqual('choice', report['next_action']['request']['answer_format']['type'])
        report = self.answer(report, 'decide-in-action')
        self.assertEqual('text', report['next_action']['request']['answer_format']['type'])
        self.assertEqual(report, self.actor.next())
        self.assertFalse(self.actor.output.exists())
        report = self.answer(report, '条件が整うまで決定を後に回すことと、行為を進めながら次の判断をその場で決めることは時点が対比になる。')
        doc = json.loads(self.actor.output.read_text())
        relations.validate_relations(doc, self.vocab, complete=False)
        self.assertEqual(['defer'], doc['edges']['contrast']['decide-in-action'])
        self.assertNotIn('decide-in-action', report['next_action']['request']['answer_format']['choices'])

    def test_incomplete_and_tampered_projection_or_receipts_fail(self):
        doc = relations.validate_relations()
        for change in ('incomplete', 'symmetry', 'self', 'reason', 'receipt', 'vocabulary'):
            bad = deepcopy(doc)
            if change == 'incomplete': bad['selections'].pop(); bad['edges'] = relations.edges(bad['selections'])
            elif change == 'symmetry': bad['edges']['contrast']['defer'] = []
            elif change == 'self': bad['selections'][0]['target_id'] = 'defer'
            elif change == 'reason': bad['selections'][0]['reason'] = '条件が整うまで決定を後に回す。'
            elif change == 'vocabulary': bad['vocabulary_sha256'] = '0'*64
            else: bad['selections'][0]['history'][0]['value_sha256'] = '0'*64
            with self.assertRaises(ValueError, msg=change): relations.validate_relations(bad)

    def test_invalid_reason_retries_same_element_and_blocks_at_five(self):
        report = self.answer(self.actor.next(), 'decide-in-action')
        identifier = report['next_action']['request']['element_id']
        for n in range(5):
            report = self.answer(report, '条件が整うまで決定を後に回す。')
            if n < 4:
                self.assertEqual(identifier, report['next_action']['request']['element_id'])
                self.assertEqual(n+2, report['next_action']['request']['attempt'])
        self.assertEqual('BLOCKED', report['status'])
        self.assertIsNone(report['next_action'])
        self.assertFalse(self.actor.output.exists())

    def test_shared_words_multisentence_and_identity_do_not_pass(self):
        self.assertFalse(relations.reason_valid('素材が共通する。', '素材を削って形を作る。', '素材を盛って形を作る。'))
        self.assertFalse(relations.reason_valid('条件が整うまで待つ。行為を進める。', self.vocab['operations'][0]['definition'], self.vocab['operations'][-6]['definition']))
        report = self.actor.next();q=report['next_action']['request']
        with self.assertRaisesRegex(ValueError, 'identity'):
            self.actor.answer({'contract_version':'element-answer/v1','run_id':'wrong','element_id':q['element_id'],'attempt':1,'value':'decide-in-action'})
        self.assertEqual(report, self.actor.next())

    def test_drift_stops_before_mutation(self):
        self.actor.next(); self.actor.vocab = deepcopy(self.vocab)
        self.actor.vocab['operations'][0]['definition'] = '条件を待つ。'
        with self.assertRaisesRegex(ValueError, 'changed'): self.actor.next()

    def test_conflicting_pair_and_export_are_checked(self):
        doc = relations.validate_relations()
        bad = deepcopy(doc)
        row = next(r for r in bad['selections'] if r['operation_id']=='decide-in-action' and r['relation']=='complement')
        row['target_id']='defer'
        with self.assertRaisesRegex(ValueError, 'both contrast'): relations.validate_relations(bad)
        exported = relations.export_edges()
        self.assertEqual(doc['edges'], exported['edges'])
        self.assertEqual(tags.digest(doc), exported['source_sha256'])
        self.assertNotIn('selections', exported)


class ExtensionTests(unittest.TestCase):
    def test_append_only_bundle_preserves_old_tags_and_receipts(self):
        _, records = tags.load_entities()
        original = json.loads(tags.TAGS.read_text())
        result = tags.validated_bundle(records)
        self.assertEqual(185, len(result['records']))
        for entity, row in original['records'].items():
            merged = result['records'][entity]
            self.assertEqual(row['tags'], merged['tags'][:len(row['tags'])])
            self.assertEqual(row['history'], merged['history'])
        self.assertEqual(original, json.loads(tags.TAGS.read_text()))
        self.assertGreater(sum(len(row['tags']) for row in result['records'].values()), sum(len(row['tags']) for row in original['records'].values()))

    def test_extension_base_hash_and_scope_drift_fail(self):
        _, records = tags.load_entities()
        scope = json.loads((tags.ROOT/'config/operation-tag-extension.json').read_text())
        for change in ('base', 'scope'):
            bad = deepcopy(scope)
            if change=='base': bad['base_tags_sha256']='0'*64
            else: bad['added_operation_ids'].pop()
            native_read = Path.read_text
            def read(path, *args, **kwargs):
                return json.dumps(bad) if path.name=='operation-tag-extension.json' else native_read(path,*args,**kwargs)
            with mock.patch.object(Path,'read_text',read), self.assertRaisesRegex(ValueError, 'extension'):
                tags.validated_bundle(records)

    def test_old_definitions_cannot_change_under_extension(self):
        _, records = tags.load_entities()
        vocab = tags.vocabulary();vocab['operations'][0]['definition']='決定を後に回す。'
        with mock.patch.object(tags,'vocabulary',return_value=vocab), self.assertRaisesRegex(ValueError,'changed'):
            tags.validated_bundle(records)
