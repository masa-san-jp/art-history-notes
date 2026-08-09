#!/usr/bin/env python3
"""出典URLが本当に在るかを確かめる。

このKBの主張はほぼ全て本文中のURLに寄りかかっている。**存在しないURLが1本混ざると、
その主張は検証不能になる**——形の上では出典があるように見えるので、読む側からは区別が付かない。
実測（2026-08-09・719本）で、実在するオランダ語ページから英語版のURLを組み立てた（`_ned_` →
`_eng_`）ものが1本見つかった。ページは無いが、引用文そのものは実在した。この型は目で追えない。

検証（build_graph.py）とは別に置く。ネットワークに出るので遅く、落ちたからといって commit を
止めるべきものでもない（サイト側の一時的な不調と、URLの誤りを機械は区別できない）。

    python3 tools/linkcheck.py                 # 全部
    python3 tools/linkcheck.py entities/movements/pita-maha.md   # 指定ファイルだけ
    python3 tools/linkcheck.py --json          # 機械可読

**403 と 429 は「無い」ではない。** bot 避けとレート制限で、ブラウザでは開く。分けて出す。
"""
import argparse
import concurrent.futures
import glob
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; art-history-notes/0.1 link-check)"
# 括弧の組は URL の一部として飲み込む（Wikipedia の曖昧さ回避 …_(painting) を切らないため）。
# `(` を文字クラスから外さないと、開き括弧だけが単独で食われて閉じ括弧の手前で切れる。
# カンマは URL の一部として認める（Commons の File:…, 1913 bronze… や『0,10』展のように
# タイトルにカンマを含む項目が実在し、除外すると生きている URL が 404 として報告される）。
# 散文中の「URL, つぎの文」は空白で切れ、末尾のカンマは下の rstrip が落とす。
URL_RE = re.compile(r'https?://(?:[^\s"\'<>\]()]|\([^\s()]*\))+')
BLOCKED = {403, 429, 999}   # bot 避け・レート制限。存在しないことの証拠にならない


def collect(paths):
    """{url: [出てくるファイル…]} を返す。"""
    found = {}
    for path in paths:
        text = open(path, encoding="utf-8").read()
        for m in URL_RE.finditer(text):
            url = m.group(0).rstrip(".,;:")
            found.setdefault(url, [])
            if path not in found[url]:
                found[url].append(path)
    return found


def encode(url):
    """非ASCIIを含むパス（日本語版Wikipedia・百度百科）は percent-encode しないと送れない。"""
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((
        parts.scheme, parts.netloc.encode("idna").decode("ascii"),
        urllib.parse.quote(parts.path, safe="/%:@&=+$,~!*'()"),
        urllib.parse.quote(parts.query, safe="/?:@&=+$,%"),
        urllib.parse.quote(parts.fragment, safe="/?:@&=+$,%")))


def status(url):
    try:
        url = encode(url)
    except Exception:
        return 0
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status
    except urllib.error.HTTPError as e:
        # HEAD を受け付けないサーバがある。GET で確かめ直す。
        # 404 も同じ扱いにする——HEAD にだけ 404 を返して GET には 200 を返すサーバが実在し
        # （mmcaresearch.kr・tongilnews.com で実測）、そのまま信じると生きた出典を殺すことになる。
        if e.code in (400, 404, 405, 501):
            try:
                get = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(get, timeout=25) as r:
                    return r.status
            except urllib.error.HTTPError as e2:
                return e2.code
            except Exception:
                return 0
        return e.code
    except Exception:
        # HEAD に答えないまま繋ぎっぱなしにするサーバがある（大きな PDF を置いた IIS で実測）。
        # 先頭1バイトだけ要求して生死を分ける。ここも駄目なら本当に到達できていない。
        try:
            rng = urllib.request.Request(
                url, headers={"User-Agent": UA, "Range": "bytes=0-0"})
            with urllib.request.urlopen(rng, timeout=25) as r:
                return 200 if r.status in (200, 206) else r.status
        except urllib.error.HTTPError as e3:
            return e3.code
        except Exception:
            return 0   # DNS・TLS・タイムアウト。到達できなかった、であって 404 ではない


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", help="省略時は entities/ 配下すべて")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--workers", type=int, default=16)
    a = ap.parse_args()

    paths = a.paths or sorted(glob.glob("entities/**/*.md", recursive=True))
    found = collect(paths)
    if not found:
        print("URL が1本も見つからない。パスを確かめる。")
        return 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
        codes = dict(zip(found, pool.map(status, found)))

    dead = {u: c for u, c in codes.items() if c == 404}
    unreachable = {u: c for u, c in codes.items() if c == 0}
    blocked = {u: c for u, c in codes.items() if c in BLOCKED}
    ok = len(codes) - len(dead) - len(unreachable) - len(blocked)

    if a.json:
        print(json.dumps({"total": len(codes), "ok": ok,
                          "dead": {u: found[u] for u in dead},
                          "unreachable": {u: found[u] for u in unreachable},
                          "blocked": sorted(blocked)}, ensure_ascii=False, indent=2))
        return 1 if dead else 0

    print(f"{len(codes)} 本 — 生きている {ok} / 404 {len(dead)} / "
          f"到達できず {len(unreachable)} / bot避け・レート制限 {len(blocked)}")
    for label, group in (("404（ページが無い。URLを組み立てていないか疑う）", dead),
                         ("到達できず（サイト側の不調かもしれない。時間を置いて再実行）", unreachable)):
        if not group:
            continue
        print(f"\n**{label}**")
        for url in sorted(group):
            print(f"- {url}\n  ← {'、'.join(found[url])}")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
