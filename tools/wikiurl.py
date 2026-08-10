#!/usr/bin/env python3
"""ウィキペディアのURLを手で組み立てないための道具。

    python3 tools/wikiurl.py ja 狩野元信
    python3 tools/wikiurl.py zh "王鑑 (畫家)"

漢字やキリル文字の記事URLを読みから percent-encoding で書き起こすと、実在しないURLが
できあがる（2026-08-10 実測: 王鑑を王鑒と1字取り違えて 404 を作った）。引用文は本物なのに
URLだけ偽物という状態は、linkcheck が 404 を返すまで気づけない。

先に repo 内に同じ記事のURLが既にあればそれを返し、無ければ MediaWiki API に解決させる。
どちらも「実在が確認できたURL」だけを出力する。
"""

import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "art-history-notes/0.1"


def existing_in_repo(lang, title):
    """repo 内に同じ記事を指すURLが既にあれば返す（表記ゆれ対策の第一手）。"""
    quoted = urllib.parse.quote(title.replace(" ", "_"))
    pattern = f"https://{lang}.wikipedia.org/wiki/"
    hits = subprocess.run(
        ["grep", "-rho", f"{re.escape(pattern)}[^ )\"'\\]]*", str(ROOT / "entities")],
        capture_output=True, text=True,
    ).stdout.split()
    for url in dict.fromkeys(hits):
        tail = url[len(pattern):]
        if urllib.parse.unquote(tail) == title.replace(" ", "_") or tail == quoted:
            return url
    return None


def resolve(lang, title):
    """MediaWiki API に正規のタイトルを返させる。リダイレクトもここで解決される。"""
    api = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "query", "titles": title, "redirects": "1", "format": "json"})
    req = urllib.request.Request(api, headers={"User-Agent": UA})
    pages = json.load(urllib.request.urlopen(req, timeout=30))["query"]["pages"]
    page = next(iter(pages.values()))
    if "missing" in page:
        return None, page.get("title")
    canonical = page["title"]
    return f"https://{lang}.wikipedia.org/wiki/" + urllib.parse.quote(canonical.replace(" ", "_")), canonical


def main():
    if len(sys.argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    lang, title = sys.argv[1], sys.argv[2]

    found = existing_in_repo(lang, title)
    if found:
        print(found)
        print(f"# repo 内に既出（そのまま使う）", file=sys.stderr)
        return 0

    url, canonical = resolve(lang, title)
    if not url:
        print(f"# 記事が見つからない: {lang}:{title}", file=sys.stderr)
        return 1
    print(url)
    if canonical != title:
        print(f"# リダイレクト/正規化: {title} -> {canonical}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
