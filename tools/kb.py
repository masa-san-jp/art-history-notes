#!/usr/bin/env python3
"""KB の共通部品 — frontmatter の読み込み、スキーマ定義、EDTF、グラフ組み立て。

各ツール（build_graph / bundle / new_entity）はここを import する。スキーマの定義はこの1箇所。
"""

import re
from urllib.parse import urlparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "entities"
CONFIG = ROOT / "config"

# --- スキーマ -----------------------------------------------------------------

DIR_FOR_TYPE = {
    "person": "persons", "work": "works", "org": "orgs", "place": "places",
    "movement": "movements", "concept": "concepts", "event": "events", "source": "sources",
}
TYPES = set(DIR_FOR_TYPE)

MOVEMENT_KINDS = {"self-declared", "retrospective", "lineage-school", "period-style"}
AUTHORITY_KEYS = {"wikidata", "aat", "ulan", "tgn", "ndl", "jpsearch", "none_reason"}
AUTHORITY_ID_PATTERNS = {
    "wikidata": re.compile(r"^Q[1-9][0-9]*$"),
    "aat": re.compile(r"^[0-9]{9}$"),
    "ulan": re.compile(r"^[0-9]{9}$"),
    "tgn": re.compile(r"^[0-9]{7,8}$"),
    "ndl": re.compile(r"^[0-9]{8}$"),
}
# 設立・所有・意思決定に、対象文化の外部者が構造的に含まれていたか（任意項目）
FOUNDING_CONTROL = {"internal", "shared", "external"}
# 画像は「パブリックドメイン相当のものだけ」を参照する。再配布はしない（リンクのみ）
IMAGE_LICENSES = {"public-domain", "cc0", "pdm"}
STATUSES = {"stub", "draft", "verified"}
CERTAINTIES = {"attested", "scholarly", "hypothesis"}

# 出典は移行期間中、URL文字列と構造化objectの両方を読む。新形式のkindは
# ここだけで定義し、validator・bundle・exportがそれぞれ独自の変換を持たない。
SOURCE_KINDS = {"primary", "scholarly", "institutional", "authority", "reference"}
SOURCE_KEYS = {"url", "kind", "note"}

# 構造的な関係（出典なしで書ける）
STRUCTURAL_RELATIONS = {
    "created_by": "created", "belongs_to": "has_member", "member_of": "has_member",
    "part_of": "has_part", "depicts": "depicted_in", "exhibited_at": "exhibited",
    "precedes": "follows", "taught_by": "taught", "documented_in": "documents",
}
# 解釈を含む関係（certainty と source を必須にする）
INTERPRETIVE_RELATIONS = {
    "influenced_by": "influenced", "responds_to": "answered_by", "derives_from": "derived_into",
    "reacts_against": "reacted_against_by", "grouped_as": "groups", "diffused_to": "received",
    "patronized_by": "patronized",
}
RELATIONS = {**STRUCTURAL_RELATIONS, **INTERPRETIVE_RELATIONS}

SPACE_ROLES = {"originated_in", "created_in", "held_at", "active_in", "born_in", "died_in", "sited_in"}

# 関係が指してよい相手の型。意味的に壊れた配線（created_by が場所を指す等）を落とすため。
RELATION_TARGET_TYPES = {
    "created_by": {"person", "org"}, "taught_by": {"person"},
    "belongs_to": {"movement"}, "grouped_as": {"movement"},
    "derives_from": {"movement"}, "reacts_against": {"movement", "concept"},
    "precedes": {"movement", "event"}, "diffused_to": {"place"},
    "patronized_by": {"org", "person"}, "member_of": {"org", "movement", "event"},
    "exhibited_at": {"event", "org"}, "documented_in": {"source"},
    "depicts": {"concept", "place", "person", "work"},
    "influenced_by": None, "responds_to": None, "part_of": None,  # None = 型を限定しない
}
SPACE_TARGET_TYPES = {
    "originated_in": {"place"}, "created_in": {"place"}, "active_in": {"place"},
    "born_in": {"place"}, "died_in": {"place"},
    "held_at": {"org", "place"}, "sited_in": {"place"},
}

# verified を名乗るとき、項目ごとの根拠が要る field（claims ブロック）
CLAIM_FIELDS_FOR_VERIFIED = {"movement": {"time", "originated_in", "kind"}}

URI_PREFIX = "urn:ahn:"

# --- EDTF（ISO 8601-2 Level 1 サブセット）--------------------------------------
# 受ける形: 1884 / 0000 / -0899 / 1884-05 / 146X / 18XX / -08XX / 1503~ / 1884? / 1884%
#          .. （開いた端）/ null（不明）
EDTF_RE = re.compile(
    r"^(?:\.\.|(?P<year>-?(?:\d{4}|\d{3}X|\d{2}XX|\dXXX))"
    r"(?:-\d{2}(?:-\d{2})?)?[?~%]?)$"
)


def edtf_ok(value):
    return value is None or (isinstance(value, str) and bool(EDTF_RE.match(value)))


def edtf_year_range(value):
    """EDTF 値から (最小年, 最大年) を返す。開いた端・不明は None。ソートと集計に使う。"""
    if not isinstance(value, str) or not value or value == "..":
        return (None, None)
    match = EDTF_RE.fullmatch(value)
    if not match:
        return (None, None)
    year = match.group("year")
    sign = -1 if year.startswith("-") else 1
    digits = year.lstrip("-")
    if "X" not in digits:
        exact = sign * int(digits)
        return (exact, exact)
    lo = int(digits.replace("X", "0"))
    hi = int(digits.replace("X", "9"))
    if sign < 0:
        # 紀元前は数値が小さいほど後なので、範囲の順序を暦年の順に戻す。
        return (-hi, -lo)
    return (lo, hi)


def century_of_year(year):
    """暦年をcoverage/bundle用の世紀番号にする（天文学的年番号）。"""
    if year is None:
        return None
    if year <= 0:
        # year 0 = 1 BCE。BCEの人間向け年へ直してから世紀を求める。
        bce_year = 1 - year
        return -((bce_year + 99) // 100)
    return year // 100 + 1


def astronomical_year_to_label(year):
    """天文学的年番号を表示用の ``N BCE`` / ``N CE`` に変換する。"""
    if not isinstance(year, int) or isinstance(year, bool):
        raise TypeError("year は整数が必要")
    if year <= 0:
        return f"{1 - year}BCE"
    return f"{year}CE"


def human_year_to_astronomical(year, era):
    """人間向けのBCE/CE年を天文学的年番号へ変換する。"""
    if not isinstance(year, int) or isinstance(year, bool) or year < 1:
        raise ValueError("year は1以上の整数が必要")
    normalized = str(era).upper()
    if normalized == "BCE":
        return 1 - year
    if normalized == "CE":
        return year
    raise ValueError("era は BCE または CE が必要")


def bce_year_to_astronomical(year):
    """人間向けのBCE年を天文学的年番号へ変換する短縮形。"""
    return human_year_to_astronomical(year, "BCE")


# --- 出典 --------------------------------------------------------------------

def is_http_url(value):
    """scheme と host を持つ http(s) URLだけを受け入れる。ネットワークには接続しない。"""
    if not isinstance(value, str) or not value.strip() or any(char.isspace() for char in value):
        return False
    parsed = urlparse(value)
    return parsed.scheme.lower() in {"http", "https"} and bool(parsed.netloc)


def normalize_source(value):
    """legacy URLまたは構造化sourceを共通の内部表現にする。"""
    if isinstance(value, str):
        return {"url": value, "kind": "reference"}
    if isinstance(value, dict):
        normalized = {key: value[key] for key in ("url", "kind", "note") if key in value}
        return normalized
    return {}


def normalize_sources(values):
    """source配列を正規化する（入力を変更しない）。"""
    if not isinstance(values, list):
        return []
    return [normalize_source(value) for value in values]


def sources_are_structured(values):
    """source配列が空でなく、全件新形式objectかを返す。"""
    return isinstance(values, list) and bool(values) and all(isinstance(value, dict) for value in values)


def source_urls(values):
    """source配列からURLだけを決定的な順序で取り出す。"""
    return [source["url"] for source in normalize_sources(values) if source.get("url")]


def source_validation_errors(values, prefix, *, allow_legacy=True):
    """source配列の構造・URL・kindを検証する。旧文字列は互換期間中許可する。"""
    errors = []
    if not isinstance(values, list):
        return [f"{prefix}: sources は配列が必要"]
    structured_urls = []
    for index, value in enumerate(values, start=1):
        item_prefix = f"{prefix}: sources[{index}]"
        if isinstance(value, str):
            if not allow_legacy:
                errors.append(f"{item_prefix} は構造化objectが必要")
            if not is_http_url(value):
                errors.append(f"{item_prefix}.url はscheme/hostを持つhttp(s) URLが必要: {value!r}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{item_prefix} はURL文字列またはobjectが必要")
            continue
        unknown = set(value) - SOURCE_KEYS
        if unknown:
            errors.append(f"{item_prefix} に未知のkey: {sorted(unknown)}")
        url = value.get("url")
        kind = value.get("kind")
        if not is_http_url(url):
            errors.append(f"{item_prefix}.url はscheme/hostを持つhttp(s) URLが必要: {url!r}")
        if kind not in SOURCE_KINDS:
            errors.append(f"{item_prefix}.kind が語彙外: {kind!r}")
        note = value.get("note")
        if note is not None and (not isinstance(note, str) or not note.strip()):
            errors.append(f"{item_prefix}.note は空でない文字列または省略が必要")
        if kind == "primary" and (not isinstance(note, str) or not note.strip()):
            errors.append(f"{item_prefix}: primary には資料種別を説明するnoteが必要")
        structured_urls.append(url)
    if all(isinstance(value, dict) for value in values):
        duplicates = sorted({url for url in structured_urls if structured_urls.count(url) > 1})
        for url in duplicates:
            errors.append(f"{prefix}: sources のURLが重複: {url}")
    return errors


def normalized_meta(meta):
    """生成物用のentity mapを共通内部表現にする。"""
    output = dict(meta)
    if isinstance(meta.get("sources"), list):
        output["sources"] = normalize_sources(meta["sources"])
    return output


# --- 読み込み -----------------------------------------------------------------

def read_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("frontmatter がない（先頭が --- で始まっていない）")
    _, block, body = text.split("---\n", 2)
    return yaml.safe_load(block) or {}, body


def load_config():
    return yaml.safe_load((CONFIG / "regions.yaml").read_text(encoding="utf-8"))


def load_region_history():
    """場所ごとの期間付き文化圏辞書を読む。未導入の checkout では空辞書にする。"""
    path = CONFIG / "place-region-history.yaml"
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data.get("places") or {}


def load_coverage_reviews():
    """被覆表の「調査済み・該当なし」セルを読む。"""
    path = CONFIG / "coverage-reviews.yaml"
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data.get("cells") or []


def load_entities():
    """{id: meta} と、id 順の (path, meta, body) を返す。検証はしない。"""
    entities, records = {}, []
    for path in sorted(ENTITIES.rglob("*.md")):
        meta, body = read_frontmatter(path)
        meta["path"] = str(path.relative_to(ROOT))
        records.append((path, meta, body))
        if meta.get("id"):
            entities[meta["id"]] = meta
    return entities, records


def edges_of(meta):
    """1エンティティの frontmatter から出るエッジを列挙する。"""
    out = []
    for r in meta.get("relations") or []:
        out.append({"from": meta.get("id"), "type": r.get("type"), "to": r.get("target"),
                    "certainty": r.get("certainty"), "source": r.get("source")})
    for s in meta.get("space") or []:
        out.append({"from": meta.get("id"), "type": s.get("role"), "to": s.get("target")})
    return out


def build_edges(entities):
    edges = [e for meta in entities.values() for e in edges_of(meta)]
    derived = [
        {"from": e["to"], "type": RELATIONS[e["type"]], "to": e["from"], "derived": True}
        for e in edges if e["type"] in RELATIONS and e["to"] in entities
    ]
    return edges + derived


QUERY_LOG = ROOT / "data" / "queries.jsonl"


def log_query(term, hits):
    """検索を記録する。**該当なしこそ残す**——探されたのに無かった、という需要が消えないように。

    これが無いと系が一方通行になる（書く→読まれる→何も返らない）。記録した語は被覆マップに出て、
    次に何を埋めるかの判断材料になる。
    """
    import datetime, json
    QUERY_LOG.parent.mkdir(exist_ok=True)
    row = {"ts": datetime.datetime.now().isoformat(timespec="seconds"), "term": term, "hits": hits}
    with QUERY_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_queries():
    import json
    if not QUERY_LOG.exists():
        return []
    return [json.loads(l) for l in QUERY_LOG.read_text(encoding="utf-8").splitlines() if l.strip()]


def search_entities(term, entities):
    """語で当たる id を返す（label と本文を見る）。bundle の --search と被覆マップで同じ結果を使う。"""
    hits = []
    needle = term.lower()
    for eid, meta in sorted(entities.items()):
        body = read_frontmatter(ROOT / meta["path"])[1]
        haystack = " ".join(str(meta.get(k) or "") for k in ("label_ja", "label_en", "id")) + body
        if needle in haystack.lower():
            hits.append(eid)
    return hits


def _region_history_matches(year_range, entries):
    """movement の開始年範囲と、[start, end) 区間が重なる辞書項目を返す。"""
    lo, hi = year_range
    if lo is None or hi is None:
        return []
    matches = []
    for entry in entries or []:
        start, _ = edtf_year_range(entry.get("start"))
        end, _ = edtf_year_range(entry.get("end"))
        if start is not None and hi < start:
            continue
        if end is not None and lo >= end:
            continue
        matches.append(entry)
    return matches


def regions_of(entity_id, entities, region_history=None):
    """発生地の文化圏を**全部**返す。

    起源が複数・論争中のものを最初の1つで代表させない。場所に期間辞書がある場合は、
    movement の開始時期と重なる区間の region を使う。時期不明・該当区間なしは place の
    現在の region に戻す。
    """
    meta = entities.get(entity_id) or {}
    year_range = edtf_year_range((meta.get("time") or {}).get("start"))
    out = []
    for s in meta.get("space") or []:
        if s.get("role") == "originated_in":
            place_id = s.get("target")
            place = entities.get(place_id) or {}
            entries = (region_history or {}).get(place_id) or []
            matches = _region_history_matches(year_range, entries)
            regions = [e.get("region") for e in matches if e.get("region")]
            if not regions:
                regions = [place.get("region")]
            for r in regions:
                if r and r not in out:
                    out.append(r)
    return out


def region_of(entity_id, entities, region_history=None):
    """後方互換。複数あるときは最初の1つ（集計には regions_of を使う）。"""
    rs = regions_of(entity_id, entities, region_history)
    return rs[0] if rs else None


def resolve(ref, entities, alias_map):
    """id か alias を id に解決する。slug を変えても参照が切れないようにするため。"""
    return ref if ref in entities else alias_map.get(ref, ref)


def alias_map(entities):
    out = {}
    for eid, meta in entities.items():
        for a in meta.get("aliases") or []:
            out[a] = eid
    return out
