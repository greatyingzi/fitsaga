#!/usr/bin/env python3
"""inject_examples.py - 给各专题json批量注入examples(引用刚生成的图)"""
import json, pathlib

ROOT = pathlib.Path("/Users/liheng/work/self/fitsaga/collector")

EX = {
  "hanfu-prompt-guide": [
    {"slug":"form","title":"对照 1 · 形制分层","good_cap":"✓ 明制马面+交领右衽+步摇+园林窗光——形制三层齐","bad_cap":"✗ 只写 hanfu dress——影楼混搭感"},
    {"slug":"dynasty","title":"对照 2 · 朝代差异","good_cap":"✓ 唐制齐胸+披帛+舞姿+风吹布料——唐制飘逸","bad_cap":"✗ 只写 tang costume——影楼租赁感"},
    {"slug":"snow","title":"对照 3 · 红衣雪景","good_cap":"✓ 红墙雪+梅+冷暖对比——流量密码构图","bad_cap":"✗ 平铺直叙的红衣雪景"},
  ],
  "lighting-prompt-guide": [
    {"slug":"golden","title":"对照 1 · 黄金时刻","good_cap":"✓ rim light 发丝光+长软影","bad_cap":"✗ nice lighting 废词出图"},
    {"slug":"window","title":"对照 2 · 窗光","good_cap":"✓ Rembrandt 三角光+光尘+衰减","bad_cap":"✗ indoor lighting 泛词"},
    {"slug":"blue","title":"对照 3 · 蓝调时刻","good_cap":"✓ 深蓝天+灯初亮的城市","bad_cap":"✗ 夜晚+霓虹(缺蓝调时段)"},
  ],
  "fabric-texture-prompt": [
    {"slug":"velvet","title":"对照 1 · 丝绒哑光","good_cap":"✓ light-absorbing folds 微距质感","bad_cap":"✗ 泛写 velvet 的亮面"},
    {"slug":"satin","title":"对照 2 · 缎面流光","good_cap":"✓ liquid sheen 顺褶流光","bad_cap":"✗ 泛写 satin"},
    {"slug":"tulle","title":"对照 3 · 纱的分层","good_cap":"✓ layered transparency+逆光","bad_cap":"✗ 单写 sheer 的塑料感"},
  ],
  "nikki-art-reference": [
    {"slug":"concept","title":"对照 1 · 原画感","good_cap":"✓ concept art+painterly+matte backdrop","bad_cap":"✗ 泛写 digital art"},
    {"slug":"palette","title":"对照 2 · 借色法","good_cap":"✓ 深蓝银金+不对称剪裁——设计血脉","bad_cap":"✗ 只说 blue and silver dress"},
  ],
  "cyberpunk-vs-miami": [
    {"slug":"neon","title":"对照 1 · 赛博霓虹","good_cap":"✓ 全域霓虹+全息+蒸汽——世界规则","bad_cap":"✗ 用 miami 词却想赛博"},
    {"slug":"miami","title":"对照 2 · 迈阿密","good_cap":"✓ 渐变天+棕榈+pastel 霓虹点缀","bad_cap":"✗ cyberpunk 词入镜跑偏"},
  ],
  "jk-lolita-ai-guide": [
    {"slug":"petticoat","title":"对照 1 · 裙撑铁律","good_cap":"✓ 钟形轮廓+糖果印花+咖啡馆窗光","bad_cap":"✗ 无裙撑=蓬蓬裙万圣感"},
    {"slug":"jk","title":"对照 2 · JK 场景","good_cap":"✓ 水手领+格裙+樱花街+午后光","bad_cap":"✗ 泛写 school uniform"},
  ],
  "wedding-dress-ai-guide": [
    {"slug":"lace","title":"对照 1 · 蕾丝花园","good_cap":"✓ 刺绣+头纱+金色 bokeh","bad_cap":"✗ 泛写 wedding dress"},
    {"slug":"tullewind","title":"对照 2 · 海边轻纱","good_cap":"✓ wind-blown 头纱+逆光","bad_cap":"✗ 无风的海边婚纱"},
  ],
  "photo-to-prompt-method": [
    {"slug":"layered","title":"对照 1 · 六层转译","good_cap":"✓ 六层齐(主体/服装/姿态/场景/光/媒介)","bad_cap":"✗ 一句话直译——气质全无"},
  ],
  "cny-hanfu-ai": [
    {"slug":"scene","title":"对照 1 · 场景符号","good_cap":"✓ 灯笼+雪+石板街——三要素齐","bad_cap":"✗ 只有红灯笼(缺场景叙事)"},
    {"slug":"modern","title":"对照 2 · 新中式","good_cap":"✓ 立领+红色点缀+极简棚拍","bad_cap":"✗ 红裙堆砌"},
  ],
}

n = 0
for slug, examples in EX.items():
    for suffix in ["", ]:
        p = ROOT / f"_topic_{slug}.json"
        if not p.exists(): continue
        t = json.loads(p.read_text(encoding="utf-8"))
        t["examples"] = examples
        P2 = ROOT / f"_topic_{slug}.json"
        P2.write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
        n += 1
print("injected into", n, "topics")
