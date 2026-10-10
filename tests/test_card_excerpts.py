from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import card_excerpts as cards
import export_signals
import haiku_adapter
from test_export_signals import movement

SOURCE = 'https://example.test/source'
BODY_A = ('## 定義と範囲\n\n'
          f'制作の前に条件を決め、あとは手順に任せる。\n作者は結果を選ばない。 [資料]({SOURCE})\n\n'
          f'> 偶然に出た形を、そのまま作品として残す。 {SOURCE}\n')
BODY_B = f'## 定義と範囲\n\n素材の重さを画面に写し取る。 {SOURCE}\n'
STOP = cards.STOP


def entity(slug, body):
    meta = movement()
    meta.update(id=f'movement/{slug}', path=f'entities/movements/{slug}.md', sources=[{'url': SOURCE, 'kind': 'primary'}])
    return (Path(meta['path']), meta, body)


class CardTestCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.output = self.root / 'cards.json'
        self.records = [entity('a', BODY_A), entity('b', BODY_B)]
        self.bundle = {'records': {'movement/a': {'tags': []}, 'movement/b': {'tags': []}}}

    def make(self, records=None, bundle=None):
        return cards.Cards(self.root / 'state', output=self.output, records=records or self.records,
                           bundle=bundle or self.bundle)

    def answer(self, tracker, report, value):
        request = report['next_action']['request']
        return tracker.answer({'contract_version': 'element-answer/v1',
                               **{key: request[key] for key in ('run_id', 'element_id', 'attempt')}, 'value': value})


class NormalizationTests(unittest.TestCase):
    def test_fixed_display_rule(self):
        self.assertEqual('日本語の改行は詰める', cards.normalize_text('日本語の\n改行は詰める'))
        self.assertEqual('two english words', cards.normalize_text('two english\nwords'))
        self.assertEqual('引用を外す', cards.normalize_text('> > 引用を\n> 外す'))
        self.assertEqual('資料を読む', cards.normalize_text(f'[資料]({SOURCE})を読む'))
        self.assertEqual('前後', cards.normalize_text(f'前（{SOURCE}）後'))
        self.assertEqual('前後', cards.normalize_text('前P571後'))
        self.assertEqual('前後', cards.normalize_text('前movement/gutai後'))

    def test_excerpt_must_sit_inside_one_paragraph(self):
        paragraphs = cards.normalized_paragraphs('一つ目。\n\n二つ目。')
        self.assertTrue(cards.excerpt_in('一つ目。', paragraphs))
        self.assertFalse(cards.excerpt_in('一つ目。二つ目。', paragraphs))
        self.assertFalse(cards.excerpt_in('一つ目。\n\n二つ目。', paragraphs))

    def test_contract_copy_matches_recorded_parent_hashes(self):
        record = json.loads((ROOT / 'schemas/element-contract-provenance.json').read_text())
        for name, expected in record['sha256'].items():
            self.assertEqual(expected, hashlib.sha256((ROOT / 'schemas' / name).read_bytes()).hexdigest())


class ElementFlowTests(CardTestCase):
    def test_requests_follow_the_contract_one_value_at_a_time(self):
        tracker = self.make()
        report = tracker.next()
        request = report['next_action']['request']
        cards.validate_contract('request', request)
        self.assertEqual('K1.card.movement.a.1', request['element_id'])
        self.assertNotIn('already_chosen', request['inputs'])
        self.assertIn('偶然に出た形を、そのまま作品として残す。', request['inputs']['body'])
        self.assertNotIn('http', request['inputs']['body'])
        self.assertNotIn('>', request['inputs']['body'])
        self.assertEqual({'type': 'text', 'min_chars': 12, 'max_chars': 120}, request['answer_format'])
        self.assertEqual(report, tracker.next())
        second = self.answer(tracker, report, '制作の前に条件を決め、あとは手順に任せる。')['next_action']['request']
        self.assertEqual('K1.card.movement.a.2', second['element_id'])
        self.assertEqual('制作の前に条件を決め、あとは手順に任せる。', second['inputs']['already_chosen'])
        self.assertEqual(STOP, 'これ以上なし')
        self.assertIn(STOP, second['instruction'])

    def test_two_excerpts_or_explicit_stop_complete_an_item(self):
        tracker = self.make()
        report = tracker.next()
        report = self.answer(tracker, report, '制作の前に条件を決め、あとは手順に任せる。')
        report = self.answer(tracker, report, '偶然に出た形を、そのまま作品として残す。')
        self.assertEqual('K1.card.movement.b.1', report['next_action']['request']['element_id'])
        report = self.answer(tracker, report, '素材の重さを画面に写し取る。')
        report = self.answer(tracker, report, STOP)
        self.assertEqual('COMPLETED', report['status'])
        document = json.loads(self.output.read_text())
        a, b = document['records']['movement/a'], document['records']['movement/b']
        self.assertEqual(['制作の前に条件を決め、あとは手順に任せる。', '偶然に出た形を、そのまま作品として残す。'],
                         [row['text'] for row in a['excerpts']])
        self.assertEqual(1, len(b['excerpts']))
        self.assertEqual('entities/movements/a.md#定義と範囲', a['excerpts'][0]['source_locator'])
        self.assertEqual([True] * 2, [row['accepted'] for row in b['history']])
        cards.validate_store(cards.pool(self.records, self.bundle), document)

    def test_stop_is_not_an_answer_for_the_first_excerpt(self):
        tracker = self.make()
        report = self.answer(tracker, tracker.next(), STOP)
        self.assertEqual(2, report['next_action']['request']['attempt'])
        self.assertIn('exact_input_excerpt:body', [row['check'] for row in report['next_action']['request']['previous_failure']])

    def test_failed_checks_retry_the_same_element_with_reason(self):
        tracker = self.make()
        report = tracker.next()
        bad = {'non_empty': '', 'length': '短い', 'exact_input_excerpt:body': '制作の前に条件を決めて、あとは手順に任せる。',
               'no_reference_tokens': f'制作の前に条件を決め、あとは手順に任せる。 {SOURCE}'}
        for name, value in bad.items():
            failed = self.answer(tracker, report, value)
            request = failed['next_action']['request']
            self.assertEqual('K1.card.movement.a.1', request['element_id'], name)
            self.assertIn(name, [row['check'] for row in request['previous_failure']])
            report = failed
        self.assertEqual(5, report['next_action']['request']['attempt'])
        spanning = self.answer(tracker, report, '制作の前に条件を決め、あとは手順に任せる。作者は結果を選ばない。偶然に出た形')
        self.assertEqual('BLOCKED', spanning['status'])
        self.assertEqual('K1.card.movement.a.1', spanning['blocked']['element_id'])
        self.assertIsNone(spanning['next_action'])
        document = json.loads(self.output.read_text())
        self.assertEqual([], document['records']['movement/a']['excerpts'])
        self.assertEqual(5, len(document['records']['movement/a']['history']))

    def test_second_excerpt_must_not_overlap_the_first(self):
        tracker = self.make()
        report = self.answer(tracker, tracker.next(), '制作の前に条件を決め、あとは手順に任せる。')
        report = self.answer(tracker, report, '制作の前に条件を決め、あとは手順に任せる。')
        self.assertIn('not_overlapping:already_chosen',
                      [row['check'] for row in report['next_action']['request']['previous_failure']])

    def test_identity_and_malformed_answers_are_rejected(self):
        tracker = self.make()
        request = tracker.next()['next_action']['request']
        good = {'contract_version': 'element-answer/v1', 'run_id': request['run_id'],
                'element_id': request['element_id'], 'attempt': 1, 'value': 'x'}
        with self.assertRaisesRegex(ValueError, 'identity'):
            tracker.answer({**good, 'element_id': 'K1.card.movement.b.1'})
        with self.assertRaises(ValueError):
            tracker.answer({**good, 'extra': 1})
        with self.assertRaises(ValueError):
            tracker.answer({**good, 'attempt': 0})

    def test_resume_returns_the_same_request_from_a_new_process(self):
        tracker = self.make()
        report = self.answer(tracker, tracker.next(), '制作の前に条件を決め、あとは手順に任せる。')
        self.assertEqual(report, self.make().next())

    def test_only_items_with_changed_body_are_redone(self):
        tracker = self.make()
        report = tracker.next()
        for value in ('制作の前に条件を決め、あとは手順に任せる。', STOP, '素材の重さを画面に写し取る。', STOP):
            report = self.answer(tracker, report, value)
        self.assertEqual('COMPLETED', report['status'])
        before = json.loads(self.output.read_text())
        changed = [entity('a', BODY_A), entity('b', BODY_B.replace('写し取る', '写して残す'))]
        again = self.make(changed).next()
        self.assertEqual('K1.card.movement.b.1', again['next_action']['request']['element_id'])
        after = json.loads(self.output.read_text())
        self.assertEqual(before['records']['movement/a'], after['records']['movement/a'])
        self.assertEqual([], after['records']['movement/b']['excerpts'])
        self.assertNotEqual(before['records']['movement/b']['content_sha256'], after['records']['movement/b']['content_sha256'])

    def test_input_change_during_a_run_is_refused(self):
        tracker = self.make()
        tracker.next()
        with self.assertRaisesRegex(ValueError, 'changed'):
            self.make([entity('a', BODY_A.replace('任せる', '預ける')), self.records[1]]).next()

    def test_state_root_inside_git_is_refused(self):
        with self.assertRaisesRegex(ValueError, 'Git-external'):
            cards.Cards(ROOT / '.agent-local-test', output=self.output, records=self.records, bundle=self.bundle)

    def test_tagged_entities_and_unsourced_bodies_are_not_inferred(self):
        bundle = {'records': {'movement/a': {'tags': [{'operation_id': 'x'}]}, 'movement/b': {'tags': []}}}
        self.assertEqual(['movement/b'], list(cards.pool(self.records, bundle)))
        bare = [entity('c', '## 定義と範囲\n\n出典URLの無い説明。\n')]
        self.assertEqual({}, cards.pool(bare, {'records': {'movement/c': {'tags': []}}}))

    def test_run_loop_feeds_each_request_to_the_adapter_one_at_a_time(self):
        calls = []
        replies = iter(['制作の前に条件を決め、あとは手順に任せる。', STOP, '素材の重さを画面に写し取る。', STOP])

        def adapter(request):
            calls.append(request['element_id'])
            return next(replies)
        report = cards.run_loop(self.make(), adapter)
        self.assertEqual('COMPLETED', report['status'])
        self.assertEqual(['K1.card.movement.a.1', 'K1.card.movement.a.2', 'K1.card.movement.b.1', 'K1.card.movement.b.2'], calls)

    def test_validate_store_rejects_tampering(self):
        tracker = self.make()
        report = tracker.next()
        for value in ('制作の前に条件を決め、あとは手順に任せる。', STOP, '素材の重さを画面に写し取る。', STOP):
            report = self.answer(tracker, report, value)
        document = json.loads(self.output.read_text())
        inventory = cards.pool(self.records, self.bundle)
        for change in ('coverage', 'stale', 'unfinished', 'excerpt', 'locator', 'history'):
            bad = deepcopy(document)
            record = bad['records']['movement/a']
            if change == 'coverage':
                del bad['records']['movement/b']
            elif change == 'stale':
                record['content_sha256'] = '0' * 64
            elif change == 'unfinished':
                record['completed'] = False
            elif change == 'excerpt':
                record['excerpts'][0]['text'] = '制作の前に条件を決めて、あとは手順に任せる。'
            elif change == 'locator':
                record['excerpts'][0]['source_locator'] = 'other'
            else:
                record['history'][0]['value_sha256'] = '1' * 64
            with self.assertRaises(ValueError, msg=change):
                cards.validate_store(inventory, bad)


class ExportCardTests(CardTestCase):
    def finished_store(self):
        tracker = self.make()
        report = tracker.next()
        for value in ('制作の前に条件を決め、あとは手順に任せる。', STOP, '素材の重さを画面に写し取る。', STOP):
            report = self.answer(tracker, report, value)
        return json.loads(self.output.read_text())

    def reader(self, mapping):
        return lambda commit, path: mapping[path].encode()

    def test_cards_use_tag_evidence_k1_excerpts_and_list_items_without_either(self):
        store = self.finished_store()
        raw = {'entities/movements/a.md': BODY_A, 'entities/movements/b.md': BODY_B,
               'entities/movements/t.md': '---\n---\n\n## 定義と範囲\n\n紙を重ねて擦る手順を固定し、\n下に置く面を可変要素とする。\n',
               'entities/movements/z.md': '# z\n'}
        tagged = entity('t', raw['entities/movements/t.md'])
        bare = entity('z', raw['entities/movements/z.md'])
        records = self.records + [tagged, bare]
        tag = {'operation_id': 'x', 'evidence': '紙を重ねて擦る手順を固定し、\n下に置く面を可変要素とする。',
               'source_locator': 'entities/movements/t.md#定義と範囲', 'source_refs': []}
        bundle = {'records': {**self.bundle['records'], 'movement/t': {'tags': [tag]}, 'movement/z': {'tags': []}}}
        with mock.patch.object(cards.operation_tags, 'targets', return_value={r[1]['id']: [] for r in records}):
            found, missing = cards.build_cards(records, bundle, 'a' * 40, read=self.reader(raw), store=store)
        self.assertEqual(['movement/z'], missing)
        self.assertEqual(['紙を重ねて擦る手順を固定し、下に置く面を可変要素とする。'], [c['text'] for c in found['movement/t']])
        self.assertEqual(['制作の前に条件を決め、あとは手順に任せる。'], [c['text'] for c in found['movement/a']])
        card = found['movement/b'][0]
        self.assertEqual({'text', 'source_locator', 'source_sha256'}, set(card))
        self.assertEqual(hashlib.sha256(BODY_B.encode()).hexdigest(), card['source_sha256'])
        self.assertNotIn('movement/z', found)

    def test_excerpt_missing_from_pinned_blob_stops_instead_of_dropping(self):
        store = self.finished_store()
        raw = {'entities/movements/a.md': BODY_A, 'entities/movements/b.md': BODY_B.replace('重さ', '厚み')}
        with mock.patch.object(cards.operation_tags, 'targets', return_value={'movement/a': [], 'movement/b': []}):
            with self.assertRaisesRegex(cards.CardSourceMismatch, 'CARD_SOURCE_MISMATCH: movement/b'):
                cards.build_cards(self.records, self.bundle, 'a' * 40, read=self.reader(raw), store=store)

    def test_build_record_carries_card_and_tags_without_relation_table(self):
        meta = movement()
        card = [{'text': 't', 'source_locator': 'l', 'source_sha256': '0' * 64}]
        record = export_signals.build_record(meta, {}, 'a' * 40, datetime(2026, 10, 10, tzinfo=timezone.utc), 'test',
                                             operation_tags=[], operation_vocabulary={'operations': []}, card=card)
        self.assertEqual(card, record['card'])
        self.assertEqual([], record['operation_tags'])
        self.assertNotIn('operation_relations', record)
        self.assertEqual([], export_signals.build_record(meta, {}, 'a' * 40, datetime(2026, 10, 10, tzinfo=timezone.utc),
                                                         'test', card=[])['card'])

    def test_cli_exports_card_and_lists_items_without_card(self):
        meta = movement()
        meta['sources'] = [{'url': SOURCE, 'kind': 'primary'}]
        found = {'movement/example': [{'text': 't', 'source_locator': 'l', 'source_sha256': '0' * 64}]}
        for cards_result, expected_missing in ((found, []), ({}, ['movement/example'])):
            stdout = __import__('io').StringIO()
            with mock.patch.object(export_signals, 'load_entities', return_value=({meta['id']: meta}, [(Path(meta['path']), meta, '')])), \
                 mock.patch.object(export_signals, '_head_commit', return_value='a' * 40), \
                 mock.patch('operation_tags.validated_bundle', return_value={'records': {meta['id']: {'tags': []}}}), \
                 mock.patch('card_excerpts.build_cards', return_value=(cards_result, expected_missing)), \
                 mock.patch.object(sys, 'argv', ['export_signals.py', '--purpose', 'test']), \
                 __import__('contextlib').redirect_stdout(stdout):
                self.assertEqual(0, export_signals.main())
            payload = json.loads(stdout.getvalue())
            self.assertEqual(expected_missing, payload['card_missing'])
            self.assertEqual(cards_result.get('movement/example', []), payload['signals'][0]['card'])


class RealRepositoryTests(unittest.TestCase):
    def test_every_entity_with_a_body_has_cards_that_appear_verbatim_in_its_source(self):
        from kb import load_entities
        import operation_tags
        _, records = load_entities()
        bundle = operation_tags.validated_bundle(records)
        found, missing = cards.build_cards(records, bundle, 'worktree',
                                           read=lambda commit, path: (ROOT / path).read_bytes())
        inventory = operation_tags.targets(records)
        self.assertEqual(set(inventory), set(found) | set(missing))
        # 設計書の6件に、本文が出典メモ（「典拠: …」）だけの4件を加えた10件。
        self.assertEqual(['movement/an-gyeon-school', 'movement/bagan-art', 'movement/barbizon-school',
                          'movement/gothic-art', 'movement/hudson-river-school', 'movement/kano-school',
                          'movement/nanga', 'movement/neoclassicism', 'movement/renaissance',
                          'movement/rococo'], missing)
        for entity_id, card in found.items():
            self.assertTrue(card, entity_id)
            for row in card:
                self.assertTrue(row['text'].strip() and '\n' not in row['text'])
        tagged = {key for key, value in bundle['records'].items() if value['tags']}
        self.assertEqual(111, len(tagged))
        self.assertEqual(len(inventory) - len(missing), len(found))


class AdapterTests(unittest.TestCase):
    REQUEST = {'instruction': '抜き書きしてください。', 'inputs': {'body': '本文です。'},
               'answer_format': {'type': 'text', 'min_chars': 3, 'max_chars': 10},
               'checks': ['exact_input_excerpt:body', 'no_reference_tokens'],
               'previous_failure': [{'check': 'length', 'reason': '短すぎます。'}]}

    def test_prompt_contains_only_this_request(self):
        prompt = haiku_adapter.build_prompt(self.REQUEST)
        for needle in ('抜き書きしてください。', '本文です。', 'length: 短すぎます。', '一字も変えず', '答えの値だけ'):
            self.assertIn(needle, prompt)

    def test_ask_uses_haiku_with_max_effort_and_returns_only_the_value(self):
        runner = mock.Mock(return_value=subprocess.CompletedProcess([], 0, stdout='答え\n', stderr=''))
        self.assertEqual('答え', haiku_adapter.ask('p', runner))
        command = runner.call_args.args[0]
        self.assertEqual(['claude', '-p'], command[:2])
        self.assertEqual('claude-haiku-5-5', command[command.index('--model') + 1])
        self.assertEqual('max', command[command.index('--effort') + 1])
        self.assertEqual('p', runner.call_args.kwargs['input'])

    def test_ask_retries_transient_failures_then_reports(self):
        runner = mock.Mock(return_value=subprocess.CompletedProcess([], 1, stdout='', stderr='boom'))
        with self.assertRaisesRegex(RuntimeError, 'boom'):
            haiku_adapter.ask('p', runner)
        self.assertEqual(haiku_adapter.TRANSIENT_RETRIES, runner.call_count)


if __name__ == '__main__':
    unittest.main()
