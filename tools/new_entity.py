#!/usr/bin/env python3
"""必須項目が埋まった雛形を作る。調査する側が「何を書くか」を思い出さなくて済むようにするため。

    uv run --locked python tools/new_entity.py movement kano-school --ja 狩野派 --en "Kano School"
    uv run --locked python tools/new_entity.py place kyoto --ja 京都 --en Kyoto --region asia-east-japan

TODO: が1つでも残っていると build_graph.py が落ちる（必須項目が空だから）。埋めれば通る。
"""

import argparse
import sys
from datetime import date

from kb import DIR_FOR_TYPE, ENTITIES, MOVEMENT_KINDS, URI_PREFIX

COMMON = """---
id: {eid}
uri: {uri}
type: {etype}
label_ja: {ja}
label_en: {en}
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null      # 典拠が1つも無いときだけ理由を書く
time:
  start: null            # EDTF: 1884 / 0000 (1 BCE) / -0899 (900 BCE) / 146X / 1503~ / null
  end: null              # 継続中は ".."
  display: null          # 原表記（元号など）をそのまま残す
{extra}space: []
relations: []
sources:
  - TODO: 出典URLを1本以上
status: stub
updated: {today}
---

# {ja}

TODO: 本文。型ごとの見出しは docs/schema.md の「本文の型」に従う。
"""

MOVEMENT_EXTRA = """kind: TODO             # {kinds}
naming:
  self_identified: TODO  # 当事者がこの名で名乗ったか（true / false）
  named_by: null         # 後付けなら命名者（person/org の id）
  named_when: null       # EDTF
  original_label: {ja}
  note: null
claims: []               # verified を名乗るとき time / originated_in / kind の根拠が要る
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("type", choices=sorted(DIR_FOR_TYPE))
    p.add_argument("slug")
    p.add_argument("--ja", required=True)
    p.add_argument("--en", default="null")
    p.add_argument("--region", help="place のとき必須（config/regions.yaml のバケット名）")
    a = p.parse_args()

    extra = ""
    if a.type == "movement":
        extra = MOVEMENT_EXTRA.format(ja=a.ja, kinds=" / ".join(sorted(MOVEMENT_KINDS)))
    if a.type == "place":
        if not a.region:
            p.error("place は --region が必須")
        extra = f"region: {a.region}\ncoordinates: [TODO, TODO]\n"

    eid = f"{a.type}/{a.slug}"
    path = ENTITIES / DIR_FOR_TYPE[a.type] / f"{a.slug}.md"
    if path.exists():
        print(f"✗ もうある: {path}", file=sys.stderr)
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(COMMON.format(eid=eid, uri=URI_PREFIX + eid, etype=a.type, ja=a.ja, en=a.en,
                                 extra=extra, today=date.today().isoformat()), encoding="utf-8")
    print(f"✓ {path.relative_to(path.parents[2])} を作った。TODO を埋めて "
          f"`uv run --locked python tools/build_graph.py --check` を通す")
    return 0


if __name__ == "__main__":
    sys.exit(main())
