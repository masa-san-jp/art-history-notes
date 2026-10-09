#!/usr/bin/env python3
"""One choice or one verbatim evidence answer at a time; no model or bulk tagging."""
from __future__ import annotations
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import os
import re
import fcntl

try:
    from kb import ROOT, load_entities, normalize_sources
    from export_signals import entity_content, _method
except ModuleNotFoundError:
    from tools.kb import ROOT, load_entities, normalize_sources
    from tools.export_signals import entity_content, _method

VOCABULARY = ROOT / 'config/operation-vocabulary.json'
TAGS = ROOT / 'config/operation-tags.json'
STOP = 'これ以上なし'


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n'


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def vocabulary(path=VOCABULARY):
    value = json.loads(path.read_text())
    if set(value) != {'contract_version', 'operations'} or value['contract_version'] != 'operation-vocabulary/v1':
        raise ValueError('Invalid operation vocabulary')
    seen = set()
    for row in value['operations']:
        if set(row) != {'id', 'label', 'definition'} or any(not isinstance(v, str) or not v.strip() for v in row.values()):
            raise ValueError('Invalid operation definition')
        if not re.fullmatch(r'[a-z][a-z0-9-]*', row['id']) or row['id'] in seen or row['id'] == STOP or row['definition'].count('。') != 1 or not row['definition'].endswith('。'):
            raise ValueError('Duplicate operation or non-sentence definition')
        seen.add(row['id'])
    if not 1 <= len(seen) <= 40:
        raise ValueError('Vocabulary must contain 1 to 40 operations')
    return value


def tagging_content(meta, body):
    # The owner text is the evidence, not a newly researched external claim.
    # Keep method fields and every definition/method section plus lead prose;
    # operational tagging does not infer methods from history, names or relations.
    content = entity_content(meta, '')
    refs = sorted({source['url'] for source in normalize_sources(meta.get('sources') or [])})
    parts = re.split(r'(?m)^#{1,6}\s+([^\n]+)\n', body)
    for index in range(1, len(parts), 2):
        heading, prose = parts[index:index + 2]
        is_lead = index == 1
        if not is_lead and not re.match(r'定義|方法|手法|技法|態度|特徴|実装例|手つき|どう成立|使える手', heading):
            continue
        for paragraph in re.split(r'\n\s*\n', prose.strip()):
            if paragraph and not paragraph.startswith('**未確認**'):
                content.append({'text': paragraph, 'source_locator': meta['path'] + '#' + ('lead' if is_lead else heading),
                                'source_refs': refs})
    return content


def targets(records):
    return {meta['id']: tagging_content(meta, body) for _, meta, body in records
            if meta['type'] == 'movement' or _method(meta) is not None}


def validate_tags(records, document=None, vocab=None, *, complete=True):
    vocab = vocab or vocabulary()
    if document is None:
        document = json.loads(TAGS.read_text())
        # Preserve old receipts only when an exact prefix of definitions matches.
        for size in range(1, len(vocab['operations']) + 1):
            prefix = {**vocab, 'operations': vocab['operations'][:size]}
            if digest(prefix) == document['vocabulary_sha256']:
                vocab = prefix
                break
    if set(document) != {'contract_version', 'vocabulary_sha256', 'records'} or document['contract_version'] != 'operation-tags/v1':
        raise ValueError('Invalid operation tags contract')
    if document['vocabulary_sha256'] != digest(vocab):
        raise ValueError('Operation vocabulary changed; retag explicitly')
    pool = targets(records)
    if (complete and set(document['records']) != set(pool)) or not set(document['records']) <= set(pool):
        raise ValueError('Operation tag coverage differs from movement/method inventory')
    ids = {row['id'] for row in vocab['operations']}
    for entity, record in document['records'].items():
        if set(record) != {'content_sha256', 'tags', 'completed', 'source_commit', 'history'}:
            raise ValueError('Invalid entity tagging record')
        content = pool[entity]
        if record['content_sha256'] != digest(content):
            raise ValueError(f'Stale operation tags: {entity}')
        if complete and record['completed'] is not True:
            raise ValueError(f'Unfinished operation tags: {entity}')
        if not isinstance(record['completed'], bool) or not re.fullmatch(r'[0-9a-f]{40}', record['source_commit']):
            raise ValueError('Invalid completion or source commit')
        if not isinstance(record['history'], list):
            raise ValueError('Invalid answer history')
        for answer in record['history']:
            if (set(answer) != {'element_id', 'attempt', 'value_sha256', 'accepted'}
                    or not isinstance(answer['accepted'], bool)
                    or type(answer['attempt']) is not int or not 1 <= answer['attempt'] <= 5
                    or not re.fullmatch(r'[0-9a-f]{64}', answer['value_sha256'])):
                raise ValueError('Invalid individual answer history')
        if record['completed']:
            expected = []
            prefix = entity.replace('/', '.')
            for number, tag in enumerate(record['tags'], 1):
                expected.extend([(f'{prefix}.operation.{number}', digest(tag['operation_id'])),
                                 (f'{prefix}.evidence.{number}', digest(tag['evidence']))])
            expected.append((f'{prefix}.operation.{len(record['tags']) + 1}', digest(STOP)))
            actual = [(row['element_id'], row['value_sha256']) for row in record['history'] if row['accepted']]
            if actual != expected:
                raise ValueError('Tags differ from the individual accepted answers')
        seen = set()
        for tag in record['tags']:
            if set(tag) != {'operation_id', 'evidence', 'source_locator', 'source_refs'} or tag['operation_id'] not in ids or tag['operation_id'] in seen:
                raise ValueError('Unknown or duplicate operation tag')
            seen.add(tag['operation_id'])
            if not isinstance(tag['evidence'], str) or len(tag['evidence']) > 600 or not tag['evidence'].strip() or not any(tag['evidence'] in item['text'] and tag['source_locator'] == item['source_locator'] and tag['source_refs'] == item['source_refs'] for item in content):
                raise ValueError(f'Operation evidence is not verbatim sourced content: {entity}')
    return document



def validated_bundle(records):
    base = validate_tags(records)
    scope_path = ROOT / 'config/operation-tag-extension.json'
    if not scope_path.exists():
        return base
    scope = json.loads(scope_path.read_text())
    full = vocabulary()
    old_count = len(full['operations']) - len(scope['added_operation_ids'])
    if (set(scope) != {'contract_version', 'base_tags_sha256', 'added_operation_ids', 'target_ids'}
            or scope['contract_version'] != 'operation-tag-extension/v1'
            or scope['base_tags_sha256'] != digest(base)
            or scope['added_operation_ids'] != [row['id'] for row in full['operations'][old_count:]]
            or digest({**full, 'operations': full['operations'][:old_count]}) != base['vocabulary_sha256']
            or len(scope['target_ids']) != len(set(scope['target_ids']))):
        raise ValueError('Invalid append-only operation extension')
    added_vocab = {**full, 'operations': full['operations'][old_count:]}
    additions = validate_tags(records, json.loads((ROOT / 'config/operation-tag-additions.json').read_text()), added_vocab, complete=False)
    if set(additions['records']) != set(scope['target_ids']) or any(not row['completed'] for row in additions['records'].values()):
        raise ValueError('Unfinished extension coverage')
    result = deepcopy(base)
    result['vocabulary_sha256'] = digest(full)
    for entity, row in additions['records'].items():
        existing = {tag['operation_id'] for tag in result['records'][entity]['tags']}
        if any(tag['operation_id'] in existing for tag in row['tags']):
            raise ValueError('Duplicate extension tag')
        result['records'][entity]['tags'].extend(deepcopy(row['tags']))
    return result

def atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, mode='w', encoding='utf-8', delete=False) as handle:
        temporary = Path(handle.name)
        try:
            handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n')
            handle.flush()
            os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)


class Tagger:
    def __init__(self, state_root, *, output=TAGS, entities=None, allowed_ids=None):
        self.root = Path(state_root).resolve() if Path(state_root).is_absolute() else Path(state_root)
        if not self.root.is_absolute() or any((p / '.git').exists() for p in [self.root, *self.root.parents]):
            raise ValueError('Use an absolute Git-external state root')
        self.path = self.root / 'operation-tag-state.json'
        self.output = output
        self.vocab = vocabulary()
        if allowed_ids is not None:
            if not set(allowed_ids) <= {row['id'] for row in self.vocab['operations']}:
                raise ValueError('Unknown extension operation')
            self.vocab['operations'] = [row for row in self.vocab['operations'] if row['id'] in allowed_ids]
        _, self.records = load_entities()
        self.pool = targets(self.records)
        if entities is not None:
            if not set(entities) <= set(self.pool):
                raise ValueError('Unknown extension target')
            self.pool = {key: self.pool[key] for key in entities}

    def next(self):
        if self.path.exists():
            state = json.loads(self.path.read_text())
            if state['vocabulary_sha256'] != digest(self.vocab) or state['inventory_sha256'] != digest(self.pool):
                raise ValueError('Tagging input changed')
        else:
            commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
            document = json.loads(self.output.read_text()) if self.output.exists() else {
                'contract_version': 'operation-tags/v1', 'vocabulary_sha256': digest(self.vocab), 'records': {}}
            validate_tags(self.records, document, self.vocab, complete=False)
            state = {'run_id': 'operation-tags', 'vocabulary_sha256': digest(self.vocab),
                     'inventory_sha256': digest(self.pool), 'source_commit': commit,
                     'document': document, 'pending': None, 'attempt': 1, 'failure': None,
                     'selected': None, 'blocked': False}
        if state['pending'] is None and not state['blocked']:
            self._request(state)
        atomic(self.path, state)
        return self.report(state)

    def _request(self, state):
        unfinished = [entity for entity in sorted(self.pool) if not state['document']['records'].get(entity, {}).get('completed')]
        if not unfinished:
            state['pending'] = None
            return
        entity = unfinished[0]
        record = state['document']['records'].setdefault(entity, {
            'content_sha256': digest(self.pool[entity]), 'tags': [], 'completed': False,
            'source_commit': state['source_commit'], 'history': []})
        content = self.pool[entity]
        used = {tag['operation_id'] for tag in record['tags']}
        selected = state['selected']
        state['pending'] = {
            'contract_version': 'element-request/v1', 'run_id': state['run_id'],
            'element_id': entity.replace('/', '.') + ('.evidence' if selected else '.operation') + f'.{len(used) + 1}',
            'attempt': state['attempt'], 'previous_failure': state['failure'],
            'instruction': ('選んだ操作の根拠を本文から一箇所そのまま抜き書きしてください。' if selected else
                            '本文だけを根拠に操作を一つ選んでください。根拠がない、または残る操作がなければ「これ以上なし」を選んでください。'),
            'inputs': {'entity_id': entity,
                       **({'body': '\n\n'.join(item['text'] for item in content)} if selected else
                          {'content': [{'text': item['text']} for item in content]}),
                       'operations': {row['id']: row['definition'] for row in self.vocab['operations']
                                      if row['id'] == selected or not selected and row['id'] not in used}},
            'answer_format': {'type': 'text', 'max_chars': 600} if selected else
                             {'type': 'choice', 'choices': [row['id'] for row in self.vocab['operations'] if row['id'] not in used] + [STOP]},
            'checks': ['non_empty', 'exact_input_excerpt:body'] if selected else ['non_empty']}

    def report(self, state):
        return {'status': 'BLOCKED' if state['blocked'] else 'WAITING' if state['pending'] else 'COMPLETED',
                'completed_count': sum(row['completed'] for row in state['document']['records'].values()),
                'target_count': len(self.pool),
                **({'blocked': {'element_id': state['pending']['element_id'],
                                'attempt': state['pending']['attempt'], 'last_failure': state['failure']}} if state['blocked'] else {}),
                'next_action': {'kind': 'element', 'request': state['pending']} if state['pending'] and not state['blocked'] else None}

    def answer(self, answer):
        state = json.loads(self.path.read_text())
        # Resumption validates the fixed source body and vocabulary before mutation.
        if state['inventory_sha256'] != digest(self.pool) or state['vocabulary_sha256'] != digest(self.vocab):
            raise ValueError('Tagging input changed')
        request = state['pending']
        if request is None or state['blocked']:
            raise ValueError('No pending tagging element')
        if set(answer) != {'contract_version', 'run_id', 'element_id', 'attempt', 'value'} or answer['contract_version'] != 'element-answer/v1' or any(answer[k] != request[k] for k in ('run_id', 'element_id', 'attempt')):
            raise ValueError('Answer identity mismatch')
        entity = request['inputs']['entity_id']
        value = answer['value']
        record = state['document']['records'][entity]
        content = self.pool[entity]
        selected = state['selected']
        valid = isinstance(value, str) and bool(value.strip())
        evidence = next((item for item in content if valid and value in item['text']), None)
        valid = valid and (len(value) <= 600 and evidence is not None if selected else value in request['answer_format']['choices'])
        record['history'].append({'element_id': request['element_id'], 'attempt': request['attempt'],
                                  'value_sha256': digest(value), 'accepted': valid})
        if not valid:
            state['failure'] = [{'check': 'exact_excerpt' if selected else 'choice', 'reason': 'Return one listed choice or a verbatim passage as requested.'}]
            state['attempt'] += 1
            if state['attempt'] > 5:
                state['blocked'] = True
            else:
                self._request(state)
        else:
            if selected:
                record['tags'].append({'operation_id': selected, 'evidence': value,
                                       'source_locator': evidence['source_locator'], 'source_refs': evidence['source_refs']})
                state['selected'] = None
            elif value == STOP:
                record['completed'] = True
            else:
                state['selected'] = value
            state.update(pending=None, attempt=1, failure=None)
            atomic(self.output, state['document'])
            self._request(state)
        atomic(self.path, state)
        return self.report(state)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['next', 'answer', 'check'])
    parser.add_argument('--state-root', type=Path)
    parser.add_argument('--extension', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'check':
            _, records = load_entities()
            validated_bundle(records)
            print('Operation vocabulary, coverage and verbatim evidence verified')
            return 0
        if args.state_root is None:
            raise ValueError('--state-root required')
        scope = json.loads((ROOT / 'config/operation-tag-extension.json').read_text()) if args.extension else None
        tagger = Tagger(args.state_root, output=ROOT / 'config/operation-tag-additions.json',
                        entities=scope['target_ids'], allowed_ids=scope['added_operation_ids']) if scope else Tagger(args.state_root)
        tagger.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        with (tagger.root / 'operation-tags.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            report = tagger.answer(json.load(sys.stdin)) if args.command == 'answer' else tagger.next()
        print(json.dumps(report, ensure_ascii=False))
        return 2 if report['status'] == 'BLOCKED' else 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
