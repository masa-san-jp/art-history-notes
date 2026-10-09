#!/usr/bin/env python3
"""Individual choice and definition-grounded reason elements; symmetric projection."""
import argparse
import fcntl
import json
import re
from pathlib import Path
import sys
try:
    from operation_tags import ROOT, atomic, digest, vocabulary
except ModuleNotFoundError:
    from tools.operation_tags import ROOT, atomic, digest, vocabulary

RELATIONS = ROOT / 'config/operation-relations.json'
KINDS = ('contrast', 'complement')


def terms(definition):
    # Keep written Japanese words with their inflection; remove final particles.
    # Shared words cannot alone demonstrate use of both definitions.
    chunks = re.findall(r'[一-龯]+[ぁ-ゖ]*|[ァ-ヺー]{2,}|[A-Za-z]{3,}', definition)
    return {word for chunk in chunks if (word := re.sub(r'(?:ながら|まで|から|より|として|[はがをにやとのかで])+$', '', chunk))}


def reason_valid(reason, left, right):
    a, b = terms(left), terms(right)
    return (isinstance(reason, str) and 0 < len(reason) <= 400 and reason.count('。') == 1
            and reason.endswith('。') and '\n' not in reason
            and any(term in reason for term in a - b)
            and any(term in reason for term in b - a))


def edges(selections):
    result = {kind: {} for kind in KINDS}
    for row in selections:
        a, b = row['operation_id'], row['target_id']
        result[row['relation']].setdefault(a, set()).add(b)
        result[row['relation']].setdefault(b, set()).add(a)
    return {kind: {key: sorted(values) for key, values in sorted(rows.items())} for kind, rows in result.items()}


def validate_relations(document=None, vocab=None, *, complete=True):
    vocab = vocab or vocabulary()
    document = document if document is not None else json.loads(RELATIONS.read_text())
    defs = {row['id']: row['definition'] for row in vocab['operations']}
    if set(document) != {'contract_version', 'vocabulary_sha256', 'selections', 'edges'} or document['contract_version'] != 'operation-relations/v1' or document['vocabulary_sha256'] != digest(vocab):
        raise ValueError('Invalid relation vocabulary contract')
    seen, pairs = set(), {}
    for row in document['selections']:
        if set(row) != {'operation_id', 'relation', 'target_id', 'reason', 'history'}:
            raise ValueError('Invalid relation selection')
        a, b, kind = row['operation_id'], row['target_id'], row['relation']
        if a not in defs or b not in defs or a == b or kind not in KINDS or (a, kind) in seen:
            raise ValueError('Invalid or duplicate relation selection')
        seen.add((a, kind))
        pair = tuple(sorted((a, b)))
        if pair in pairs and pairs[pair] != kind:
            raise ValueError('Pair is both contrast and complement')
        pairs[pair] = kind
        if not reason_valid(row['reason'], defs[a], defs[b]):
            raise ValueError('Reason must use distinct terms from both definitions in one sentence')
        prefix = a + '.' + kind
        expected = [(prefix + '.choice', digest(b)), (prefix + '.reason', digest(row['reason']))]
        for receipt in row['history']:
            if set(receipt) != {'element_id', 'attempt', 'accepted', 'value_sha256'} or type(receipt['accepted']) is not bool or type(receipt['attempt']) is not int or not 1 <= receipt['attempt'] <= 5:
                raise ValueError('Invalid relation receipt')
        if [(r['element_id'], r['value_sha256']) for r in row['history'] if r['accepted']] != expected:
            raise ValueError('Relation differs from accepted individual answers')
    if complete and seen != {(a, kind) for a in defs for kind in KINDS}:
        raise ValueError('Every operation needs one choice of each relation')
    if document['edges'] != edges(document['selections']):
        raise ValueError('Relation edges must be the symmetric projection of selections')
    return document


def export_edges(vocab=None):
    document = validate_relations(vocab=vocab)
    return {'contract_version': 'operation-relation-edges/v1',
            'vocabulary_sha256': document['vocabulary_sha256'],
            'source_sha256': digest(document), 'edges': deepcopy_edges(document['edges'])}


def deepcopy_edges(value):
    return json.loads(json.dumps(value))


class Relator:
    def __init__(self, state_root, *, output=RELATIONS):
        self.root = Path(state_root)
        if not self.root.is_absolute() or any((p / '.git').exists() for p in (self.root, *self.root.parents)):
            raise ValueError('Use a Git-external absolute state root')
        self.path = self.root / 'operation-relation-state.json'
        self.output = output
        self.vocab = vocabulary()
        self.defs = {row['id']: row['definition'] for row in self.vocab['operations']}

    def next(self):
        if self.path.exists():
            state = json.loads(self.path.read_text())
            if state['document']['vocabulary_sha256'] != digest(self.vocab):
                raise ValueError('Relation vocabulary changed')
        else:
            doc = json.loads(self.output.read_text()) if self.output.exists() else {
                'contract_version': 'operation-relations/v1', 'vocabulary_sha256': digest(self.vocab), 'selections': [], 'edges': edges([])}
            validate_relations(doc, self.vocab, complete=False)
            state = {'document': doc, 'pending': None, 'selected': None, 'history': [], 'attempt': 1, 'failure': None, 'blocked': False}
        if not state['blocked']:
            self.request(state)
        atomic(self.path, state)
        return self.report(state)

    def request(self, state):
        done = {(row['operation_id'], row['relation']) for row in state['document']['selections']}
        todo = [(row['id'], kind) for row in self.vocab['operations'] for kind in KINDS if (row['id'], kind) not in done]
        if not todo:
            state['pending'] = None
            return
        a, kind = todo[0]
        selected = state['selected']
        other = 'contrast' if kind == 'complement' else 'complement'
        forbidden = set(edges(state['document']['selections'])[other].get(a, [])) | {a}
        choices = [b for b in self.defs if b not in forbidden]
        state['pending'] = {'contract_version': 'element-request/v1', 'run_id': 'operation-relations',
            'element_id': a + '.' + kind + ('.reason' if selected else '.choice'),
            'attempt': state['attempt'], 'previous_failure': state['failure'],
            'instruction': '両方の定義の固有の語を含む理由を1文で答えてください。' if selected else '定義だけを根拠に、' + ('対比' if kind == 'contrast' else '補い合う') + '操作を一覧から一つ選んでください。',
            'inputs': {'operation_id': a, 'relation': kind, 'definition': self.defs[a],
                       'definitions': {b: self.defs[b] for b in ([selected] if selected else choices)}},
            'answer_format': {'type': 'text', 'max_chars': 400} if selected else {'type': 'choice', 'choices': choices},
            'checks': ['non_empty', 'both_definition_terms', 'one_sentence'] if selected else ['non_empty']}

    def report(self, state):
        return {'status': 'BLOCKED' if state['blocked'] else 'WAITING' if state['pending'] else 'COMPLETED',
                'completed_count': len(state['document']['selections']), 'target_count': len(self.defs) * 2,
                'next_action': {'kind': 'element', 'request': state['pending']} if state['pending'] and not state['blocked'] else None}

    def answer(self, answer):
        state = json.loads(self.path.read_text())
        if state['document']['vocabulary_sha256'] != digest(self.vocab):
            raise ValueError('Relation vocabulary changed')
        request = state['pending']
        if not request or state['blocked']:
            raise ValueError('No pending relation element')
        if set(answer) != {'contract_version', 'run_id', 'element_id', 'attempt', 'value'} or answer['contract_version'] != 'element-answer/v1' or any(answer[k] != request[k] for k in ('run_id', 'element_id', 'attempt')):
            raise ValueError('Relation answer identity mismatch')
        a, kind = request['inputs']['operation_id'], request['inputs']['relation']
        value, selected = answer['value'], state['selected']
        valid = reason_valid(value, self.defs[a], self.defs[selected]) if selected else isinstance(value, str) and value in request['answer_format']['choices']
        state['history'].append({'element_id': request['element_id'], 'attempt': request['attempt'], 'accepted': valid, 'value_sha256': digest(value)})
        if valid:
            if selected:
                state['document']['selections'].append({'operation_id': a, 'relation': kind, 'target_id': selected, 'reason': value, 'history': state['history']})
                state['document']['edges'] = edges(state['document']['selections'])
                validate_relations(state['document'], self.vocab, complete=False)
                atomic(self.output, state['document'])
                state.update(selected=None, history=[])
            else:
                state['selected'] = value
            state.update(attempt=1, failure=None)
        else:
            state['failure'] = [{'check': 'both_definition_terms' if selected else 'choice', 'reason': 'Return a listed choice or one sentence grounded in both definitions.'}]
            if state['attempt'] == 5:
                state['blocked'] = True
            else:
                state['attempt'] += 1
        if not state['blocked']:
            self.request(state)
        atomic(self.path, state)
        return self.report(state)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['next', 'answer', 'check'])
    parser.add_argument('--state-root', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'check':
            result = validate_relations()
            print(f"Verified {len(result['selections'])} individual relation selections and symmetric edges")
            return 0
        actor = Relator(args.state_root)
        actor.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        with (actor.root / 'operation-relations.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            result = actor.answer(json.load(sys.stdin)) if args.command == 'answer' else actor.next()
        print(json.dumps(result, ensure_ascii=False))
        return 2 if result['status'] == 'BLOCKED' else 0
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
