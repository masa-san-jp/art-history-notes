#!/usr/bin/env python3
"""One element request on stdin -> the answer value only on stdout, via Claude Haiku 5.5.

Each call is an independent `claude -p` run with no tools, no project settings and
no session, so the answerer sees only this one request. The value is written
exactly as returned (trailing newline removed); the harness checks it.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile

MODEL = 'claude-haiku-5-5'
EFFORT = 'max'
TIMEOUT_SECONDS = 600
TRANSIENT_RETRIES = 3
SYSTEM_PROMPT = ('あなたは1つの依頼に対して、答えの値だけを返す答え手です。'
                 '説明・前置き・引用符・コードブロックは付けず、値そのものだけを出力します。')
CHECK_NOTES = {
    'exact_input_excerpt': '入力の本文にある文字列を、一字も変えず（句読点・記号・改行の扱いも含めて）そのままコピーしてください。要約や言い換えは不可です。',
    'no_reference_tokens': 'URL・ID・出典メモ・「未確認」の注記を含めないでください。',
    'not_overlapping': '先に選んだ部分と重ならない別の箇所にしてください。',
    'allow_stop': '該当する別の箇所が本文に無い場合に限り、指定された終了の言葉だけを返してください。',
}


def build_prompt(request: dict) -> str:
    fmt = request['answer_format']
    notes = [CHECK_NOTES[name.split(':')[0]] for name in request['checks'] if name.split(':')[0] in CHECK_NOTES]
    parts = [request['instruction'], '', '## 入力', json.dumps(request['inputs'], ensure_ascii=False, indent=2), '',
             '## 答えの形', json.dumps(fmt, ensure_ascii=False)]
    if notes:
        parts += ['', '## 守ること', *[f'- {note}' for note in notes]]
    if request['previous_failure']:
        parts += ['', '## 前回の答えが確認に通らなかった理由',
                  *[f'- {row["check"]}: {row["reason"]}' for row in request['previous_failure']]]
    parts += ['', '答えの値だけを出力してください。']
    return '\n'.join(parts)


def ask(prompt: str, runner=subprocess.run) -> str:
    command = ['claude', '-p', '--model', MODEL, '--effort', EFFORT, '--output-format', 'text',
               '--no-session-persistence', '--disable-slash-commands', '--tools', '',
               '--strict-mcp-config', '--setting-sources', '', '--system-prompt', SYSTEM_PROMPT]
    error = ''
    for _ in range(TRANSIENT_RETRIES):
        with tempfile.TemporaryDirectory() as cwd:  # outside any project, so no CLAUDE.md is picked up
            try:
                result = runner(command, input=prompt, text=True, capture_output=True, cwd=cwd,
                                timeout=TIMEOUT_SECONDS, check=False)
            except subprocess.TimeoutExpired:
                error = 'timeout'
                continue
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.rstrip('\n')
        error = (result.stderr or 'empty output').strip()[-300:]
    raise RuntimeError(f'claude call failed: {error}')


def main() -> int:
    try:
        request = json.load(sys.stdin)
        sys.stdout.write(ask(build_prompt(request)))
        return 0
    except (OSError, ValueError, KeyError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
