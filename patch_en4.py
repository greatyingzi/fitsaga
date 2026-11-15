#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
s = P.read_text(encoding="utf-8")
# cards append 分lang
old = 'cards.append('
# 简单方案: cards.append行前加 lang 判断跳过en
line_mark = "        cards.append("
i = s.find(line_mark)
if i > 0:
    guard = "        if t.get("lang") != "en":
            cards.append("
    s = s.replace(line_mark, guard, 1)
    # en索引单独写
    add = '''
    en_cards = [c for c in []]
    '''
    P.write_text(s, encoding="utf-8")
    print("guard added")
