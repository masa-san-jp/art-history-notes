#!/usr/bin/env python3
"""Verbatim card excerpts for phase A v2 (agentic-art-orchestration design 4.1-4.2).

    python tools/card_excerpts.py next --state-root <absolute path outside Git>
    python tools/card_excerpts.py answer --state-root <same root> < one-answer.json
    python tools/card_excerpts.py run --state-root <same root> [--limit N]
    python tools/card_excerpts.py check [--commit SHA]

Items with operation tags use the tag evidence as their card text. Items with a
body but no tags get one inference per element (K1): a verbatim excerpt, then a
second, separate element for "one more place or これ以上なし". Items with neither are
listed, never filled from names. The harness starts no model itself; `run` only
pipes each request to an external adapter, one request at a time.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from kb import ROOT, load_entities
    from agent_support import is_immutable_archive
    import operation_tags
    from export_signals import entity_content
except ModuleNotFoundError:
    from tools.kb import ROOT, load_entities
    from tools.agent_support import is_immutable_archive
    from tools import operation_tags
    from tools.export_signals import entity_content

STORE = ROOT / 'config/card-excerpts.json'
SCHEMAS = ROOT / 'schemas'
CONTRACT = 'card-excerpts/v1'
RUN_ID = 'card-excerpts'
STOP = 'これ以上なし'
BODY_MAX_BYTES = 3000
MIN_CHARS, MAX_CHARS, MAX_ATTEMPTS = 12, 120, 5
INSTRUCTION_FIRST = 'この本文から、この美術がどんな作り方・考え方をするかを最もよく表す部分を、一字も変えずに抜き書きしてください。'
INSTRUCTION_SECOND = ('この本文から、すでに選んだ部分とは別の一箇所を、一字も変えずに抜き書きしてください。'
                      f'無ければ「{STOP}」と答えてください。')

# Design 4.1 fixed display rule: quote marks, link syntax, URLs and IDs are removed;
# a line break between Japanese characters is closed up, between ASCII letters it
# becomes one space. Excerpts are checked after this same rule is applied.
_LINK = re.compile(r'!?\[([^\]]*)\]\([^)\s]*\)')
_URL = re.compile(r"https?://[A-Za-z0-9\-._~:/?#\[\]@!$&'*+,;=%]+")
_ID = re.compile(r'(?<![A-Za-z0-9])[PQ]\d{2,}(?![A-Za-z0-9])'
                 r'|(?<![A-Za-z0-9/])(?:movement|person|place|concept|event|org|work|source)/[a-z0-9][a-z0-9-]*'
                 r'|urn:[a-z]+:\S+')
_EMPTY_BRACKETS = re.compile(r'[（(]\s*[）)]')
_REFERENCE_WORDS = ('未確認', '出典')


def normalize_text(text: str) -> str:
    text = _LINK.sub(r'\1', text)
    joined = ''
    for line in text.split('\n'):
        line = re.sub(r'^\s*(?:>\s*)+', '', line).strip()
        if not line:
            continue
        if joined and joined[-1].isascii() and line[0].isascii():
            joined += ' '
        joined += line
    for pattern in (_URL, _ID, _EMPTY_BRACKETS):
        joined = pattern.sub('', joined)
    return re.sub(r' {2,}', ' ', joined).strip()


def normalized_paragraphs(text: str) -> list[str]:
    return [p for p in (normalize_text(part) for part in re.split(r'\n\s*\n', text)) if p]


def excerpt_in(excerpt: str, paragraphs: list[str]) -> bool:
    return bool(excerpt) and '\n' not in excerpt and any(excerpt in p for p in paragraphs)


def reference_problem(text: str) -> str | None:
    if _URL.search(text) or _ID.search(text) or '](' in text or text.startswith('>'):
        return 'URL・ID・リンク記法・引用記号を含んでいます'
    if any(word in text for word in _REFERENCE_WORDS):
        return '出典メモや未確認の注記になっています'
    return None


digest = operation_tags.digest


def body_items(meta: dict, body: str) -> list[dict]:
    """The owner's cited body (entity_content), displayed under the fixed rule, cut by paragraph."""
    items, size = [], 0
    for item in entity_content(meta, body):
        text = normalize_text(item['text'])
        # 出典メモだけの段落（「典拠: Wikidata／Getty AAT …」など）と、抜き書きの最小字数に満たない段落は本文として扱わない。
        if len(text) < MIN_CHARS or text.lstrip('*_ ').startswith(('未確認', '典拠', '出典')):
            continue
        size += len(text.encode()) + (2 if items else 0)
        if size > BODY_MAX_BYTES:
            if not items:
                raise ValueError(f'First body paragraph exceeds {BODY_MAX_BYTES} bytes: {meta["id"]}')
            break
        items.append({'text': text, 'source_locator': item['source_locator']})
    return items


def pool(records, bundle) -> dict[str, list[dict]]:
    """Entities that need an inferred excerpt: in the tag inventory, no tags, with a body."""
    tagged = {key for key, value in bundle['records'].items() if value['tags']}
    wanted = set(operation_tags.targets(records)) - tagged
    out = {}
    for _, meta, body in records:
        if meta['id'] in wanted and (items := body_items(meta, body)):
            out[meta['id']] = items
    return dict(sorted(out.items()))


# --- contract (schemas copied from the parent, see schemas/element-contract-provenance.json) ---

def _validate(value, schema, path='$'):
    kind = schema.get('type')
    checks = {'object': dict, 'array': list, 'string': str, 'boolean': bool, 'null': type(None)}
    if kind == 'integer':
        if type(value) is not int:
            raise ValueError(f'{path}: integer expected')
    elif kind in checks and not isinstance(value, checks[kind]):
        raise ValueError(f'{path}: {kind} expected')
    if 'const' in schema and value != schema['const']:
        raise ValueError(f'{path}: must be {schema["const"]!r}')
    if 'oneOf' in schema:
        passed = 0
        for option in schema['oneOf']:
            try:
                _validate(value, option, path)
                passed += 1
            except ValueError:
                pass
        if passed != 1:
            raise ValueError(f'{path}: does not match exactly one allowed form')
    if isinstance(value, str):
        if len(value) < schema.get('minLength', 0) or len(value) > schema.get('maxLength', 1 << 30):
            raise ValueError(f'{path}: bad length')
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            raise ValueError(f'{path}: bad pattern')
    if type(value) is int and value < schema.get('minimum', value):
        raise ValueError(f'{path}: below minimum')
    if isinstance(value, dict):
        missing = set(schema.get('required', [])) - set(value)
        if missing:
            raise ValueError(f'{path}: missing {sorted(missing)}')
        properties = schema.get('properties', {})
        if schema.get('additionalProperties') is False and set(value) - set(properties):
            raise ValueError(f'{path}: unexpected {sorted(set(value) - set(properties))}')
        for key, sub in properties.items():
            if key in value:
                _validate(value[key], sub, f'{path}.{key}')
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            raise ValueError(f'{path}: too few items')
        if schema.get('uniqueItems') and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            raise ValueError(f'{path}: duplicate items')
        for index, item in enumerate(value):
            if 'items' in schema:
                _validate(item, schema['items'], f'{path}[{index}]')


def validate_contract(kind: str, value) -> None:
    _validate(value, json.loads((SCHEMAS / f'element-{kind}.schema.json').read_text()))


# --- store ---

def _fresh(items, commit):
    return {'content_sha256': digest(items), 'source_commit': commit, 'excerpts': [], 'completed': False, 'history': []}


def element_id(entity: str, number: int) -> str:
    return f'K1.card.{entity.replace("/", ".")}.{number}'


def validate_store(pool_, document, *, complete=True):
    if set(document) != {'contract_version', 'records'} or document['contract_version'] != CONTRACT:
        raise ValueError('Invalid card excerpt contract')
    if (complete and set(document['records']) != set(pool_)) or not set(document['records']) <= set(pool_):
        raise ValueError('Card excerpt coverage differs from the untagged body inventory')
    for entity, record in document['records'].items():
        if set(record) != {'content_sha256', 'source_commit', 'excerpts', 'completed', 'history'}:
            raise ValueError(f'Invalid card record: {entity}')
        if record['content_sha256'] != digest(pool_[entity]):
            raise ValueError(f'Stale card excerpts: {entity}')
        if (complete and record['completed'] is not True) or not isinstance(record['completed'], bool):
            raise ValueError(f'Unfinished card excerpts: {entity}')
        if not re.fullmatch(r'[0-9a-f]{40}', record['source_commit']) or len(record['excerpts']) > 2:
            raise ValueError(f'Invalid card record: {entity}')
        for row in record['history']:
            if (set(row) != {'element_id', 'attempt', 'value_sha256', 'accepted', 'failed_checks'}
                    or type(row['attempt']) is not int or not 1 <= row['attempt'] <= MAX_ATTEMPTS
                    or not isinstance(row['accepted'], bool) or not isinstance(row['failed_checks'], list)
                    or not re.fullmatch(r'[0-9a-f]{64}', row['value_sha256'])):
                raise ValueError(f'Invalid answer history: {entity}')
        for excerpt in record['excerpts']:
            if (set(excerpt) != {'text', 'source_locator'} or not MIN_CHARS <= len(excerpt['text']) <= MAX_CHARS
                    or reference_problem(excerpt['text'])
                    or not any(excerpt['text'] in item['text'] and '\n' not in excerpt['text']
                               and item['source_locator'] == excerpt['source_locator'] for item in pool_[entity])):
                raise ValueError(f'Excerpt is not verbatim body text: {entity}')
        texts = [row['text'] for row in record['excerpts']]
        if len(texts) == 2 and (texts[0] in texts[1] or texts[1] in texts[0]):
            raise ValueError(f'Overlapping excerpts: {entity}')
        if record['completed']:
            expected = [(element_id(entity, n), digest(row['text'])) for n, row in enumerate(record['excerpts'], 1)]
            if len(texts) == 1:
                expected.append((element_id(entity, 2), digest(STOP)))
            actual = [(row['element_id'], row['value_sha256']) for row in record['history'] if row['accepted']]
            if not texts or actual != expected:
                raise ValueError(f'Excerpts differ from the accepted answers: {entity}')
    return document


def load_store(path=STORE):
    return json.loads(path.read_text()) if path.exists() else {'contract_version': CONTRACT, 'records': {}}


def check_answer(request: dict, value) -> list[dict]:
    """Programmatic checks only; returns the failed ones as previous_failure rows."""
    if not isinstance(value, str) or not value.strip():
        return [{'check': 'non_empty', 'reason': '空でない文字列を返してください。'}]
    second = 'already_chosen' in request['inputs']
    if second and value == STOP:
        return []
    failures = []
    body = request['inputs']['body']
    if not MIN_CHARS <= len(value) <= MAX_CHARS:
        failures.append({'check': 'length', 'reason': f'{MIN_CHARS}〜{MAX_CHARS}字で抜き書きしてください。'})
    if value != value.strip() or '\n' in value or value not in body:
        failures.append({'check': 'exact_input_excerpt:body',
                         'reason': '本文の一つの段落にある文字列を、一字も変えず改行なしで抜いてください。'})
    if problem := reference_problem(value):
        failures.append({'check': 'no_reference_tokens', 'reason': problem + '。'})
    if second and (value in request['inputs']['already_chosen'] or request['inputs']['already_chosen'] in value):
        failures.append({'check': 'not_overlapping:already_chosen', 'reason': '選んだ部分と重ならない別の箇所にしてください。'})
    return failures


def atomic(path, value):
    operation_tags.atomic(path, value)


class Cards:
    def __init__(self, state_root, *, output=STORE, records=None, bundle=None):
        self.root = Path(state_root)
        if not self.root.is_absolute() or any((p / '.git').exists() for p in [self.root.resolve(), *self.root.resolve().parents]):
            raise ValueError('Use an absolute Git-external state root')
        self.path = self.root / 'card-state.json'
        self.output = output
        if records is None:
            _, records = load_entities()
        self.records = records
        self.bundle = bundle or operation_tags.validated_bundle(records)
        self.pool = pool(records, self.bundle)

    def next(self):
        state = json.loads(self.path.read_text()) if self.path.exists() else None
        if state and state['inventory_sha256'] != digest(self.pool):
            if state['pending'] is not None or state['blocked']:
                raise ValueError('Card input changed during a run')
            state = None  # finished run on older text: only changed items are redone below
        if state is None:
            commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
            stored = load_store(self.output)
            kept = {entity: record for entity, record in stored['records'].items()
                    if entity in self.pool and record['content_sha256'] == digest(self.pool[entity])}
            document = {'contract_version': CONTRACT, 'records': kept}
            validate_store(self.pool, document, complete=False)
            state = {'run_id': RUN_ID, 'inventory_sha256': digest(self.pool), 'source_commit': commit,
                     'document': document, 'pending': None, 'attempt': 1, 'failure': None, 'blocked': False}
        if state['pending'] is None and not state['blocked']:
            self._request(state)
        atomic(self.path, state)
        atomic(self.output, state['document'])
        return self.report(state)

    def _request(self, state):
        for entity, items in self.pool.items():
            record = state['document']['records'].setdefault(entity, _fresh(items, state['source_commit']))
            if record['completed']:
                continue
            second = bool(record['excerpts'])
            inputs = {'body': '\n\n'.join(item['text'] for item in items)}
            if second:
                inputs['already_chosen'] = record['excerpts'][0]['text']
            request = {
                'contract_version': 'element-request/v1', 'run_id': state['run_id'],
                'element_id': element_id(entity, 2 if second else 1), 'attempt': state['attempt'],
                'instruction': INSTRUCTION_SECOND if second else INSTRUCTION_FIRST,
                'inputs': inputs,
                'answer_format': {'type': 'text', 'min_chars': 6 if second else MIN_CHARS, 'max_chars': MAX_CHARS},
                'checks': ['exact_input_excerpt:body', 'no_reference_tokens']
                          + [f'min_chars:{MIN_CHARS}', 'not_overlapping:already_chosen', f'allow_stop:{STOP}'][:3 if second else 1],
                'previous_failure': state['failure']}
            validate_contract('request', request)
            if len(json.dumps(request, ensure_ascii=False).encode()) > 4096:
                raise ValueError(f'Request exceeds 4096 bytes: {request["element_id"]}')
            state['pending'] = request
            return
        state['pending'] = None

    def report(self, state):
        done = sum(row['completed'] for row in state['document']['records'].values())
        return {'status': 'BLOCKED' if state['blocked'] else 'WAITING' if state['pending'] else 'COMPLETED',
                'completed_count': done, 'target_count': len(self.pool),
                **({'blocked': {'element_id': state['pending']['element_id'], 'attempt': state['pending']['attempt'],
                                'last_failure': state['failure']}} if state['blocked'] else {}),
                'next_action': {'kind': 'element', 'request': state['pending']}
                               if state['pending'] and not state['blocked'] else None}

    def answer(self, answer):
        validate_contract('answer', answer)
        state = json.loads(self.path.read_text())
        if state['inventory_sha256'] != digest(self.pool):
            raise ValueError('Card input changed during a run')
        request = state['pending']
        if request is None or state['blocked']:
            raise ValueError('No pending card element')
        if any(answer[key] != request[key] for key in ('run_id', 'element_id', 'attempt')):
            raise ValueError('Answer identity mismatch')
        value = answer['value']
        entity = next(key for key in self.pool if request['element_id'] in (element_id(key, 1), element_id(key, 2)))
        record = state['document']['records'][entity]
        failures = check_answer(request, value)
        record['history'].append({'element_id': request['element_id'], 'attempt': request['attempt'],
                                  'value_sha256': digest(value), 'accepted': not failures,
                                  'failed_checks': [row['check'] for row in failures]})
        if failures:
            state['failure'] = failures
            state['attempt'] += 1
            if state['attempt'] > MAX_ATTEMPTS:
                state['blocked'] = True
            else:
                self._request(state)
        else:
            if value == STOP and 'already_chosen' in request['inputs']:
                record['completed'] = True
            else:
                locator = next(item['source_locator'] for item in self.pool[entity] if value in item['text'])
                record['excerpts'].append({'text': value, 'source_locator': locator})
                record['completed'] = len(record['excerpts']) == 2
            state.update(pending=None, attempt=1, failure=None)
            self._request(state)
        atomic(self.path, state)
        atomic(self.output, state['document'])
        return self.report(state)


# --- export ---

def read_blob(commit: str, path: str) -> bytes:
    try:
        return subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{commit}:{path}'])
    except subprocess.CalledProcessError:
        if not is_immutable_archive(ROOT):
            raise
        return (ROOT / path).read_bytes()


class CardSourceMismatch(ValueError):
    pass


def build_cards(records, bundle, commit, *, read=read_blob, store=None):
    """(cards by entity id, entity ids with neither tags nor body).

    Every excerpt is re-checked against the pinned blob under the fixed display rule.
    """
    inventory = pool(records, bundle)
    document = validate_store(inventory, load_store() if store is None else store)
    cards, missing = {}, []
    inventory_ids = set(operation_tags.targets(records))
    for _, meta, _body in records:
        entity = meta['id']
        if entity not in inventory_ids:
            continue
        tags = bundle['records'].get(entity, {}).get('tags') or []
        if tags:
            excerpts = [(normalize_text(tag['evidence']), tag['source_locator']) for tag in tags]
        elif entity in document['records']:
            excerpts = [(row['text'], row['source_locator']) for row in document['records'][entity]['excerpts']]
        else:
            missing.append(entity)
            continue
        blob = read(commit, meta['path'])
        paragraphs = normalized_paragraphs(blob.decode('utf-8'))
        sha = hashlib.sha256(blob).hexdigest()
        card = []
        for text, locator in excerpts:
            if not locator.startswith(meta['path'] + '#') or not excerpt_in(text, paragraphs):
                raise CardSourceMismatch(f'CARD_SOURCE_MISMATCH: {entity} {locator}')
            if not any(row['text'] == text and row['source_locator'] == locator for row in card):
                card.append({'text': text, 'source_locator': locator, 'source_sha256': sha})
        cards[entity] = card
    return cards, sorted(missing)


# --- command line ---

def run_loop(cards: Cards, adapter, limit=0, log=lambda message: None):
    report, answered = cards.next(), 0
    while report['status'] == 'WAITING' and (not limit or answered < limit):
        request = report['next_action']['request']
        value = adapter(request)
        report = cards.answer({'contract_version': 'element-answer/v1', 'run_id': request['run_id'],
                               'element_id': request['element_id'], 'attempt': request['attempt'], 'value': value})
        answered += 1
        log(f'{request["element_id"]} attempt={request["attempt"]} -> {report["completed_count"]}/{report["target_count"]}')
    return report


def subprocess_adapter(command):
    def adapter(request):
        result = subprocess.run(command, input=json.dumps(request, ensure_ascii=False), text=True,
                                capture_output=True, check=False)
        if result.returncode:
            raise RuntimeError(f'adapter failed: {result.stderr.strip()[-300:]}')
        return result.stdout
    return adapter


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['next', 'answer', 'run', 'check'])
    parser.add_argument('--state-root', type=Path)
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--commit')
    parser.add_argument('--adapter', default=str(Path(__file__).with_name('haiku_adapter.py')))
    args = parser.parse_args()
    try:
        _, records = load_entities()
        bundle = operation_tags.validated_bundle(records)
        if args.command == 'check':
            commit = args.commit or subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
            cards, missing = build_cards(records, bundle, commit)
            excerpts = sum(len(card) for card in cards.values())
            print(json.dumps({'commit': commit, 'entities_with_cards': len(cards), 'excerpts': excerpts,
                              'entities_without_cards': missing}, ensure_ascii=False))
            return 0
        if args.state_root is None:
            raise ValueError('--state-root required')
        cards = Cards(args.state_root, records=records, bundle=bundle)
        cards.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        with (cards.root / 'card-excerpts.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if args.command == 'answer':
                report = cards.answer(json.load(sys.stdin))
            elif args.command == 'run':
                report = run_loop(cards, subprocess_adapter([sys.executable, args.adapter]), args.limit,
                                  lambda message: print(message, file=sys.stderr, flush=True))
            else:
                report = cards.next()
        print(json.dumps(report, ensure_ascii=False))
        return 2 if report['status'] == 'BLOCKED' else 0
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
