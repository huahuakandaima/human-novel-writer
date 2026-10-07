#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
density_check.py — 密度红线检查器（朱雀实测 + 小说ai行文规范 2026-10-07 合并版）

用法：
    python scripts/density_check.py 稿件.md
    python scripts/density_check.py 稿件.md --forbidden 突然 忽然 只见

红线对照（2026-10-07 起：与《小说ai行文规范》冲突处一律以该规范为准）：
    破折号  行文规范改为「用途纪律」：插入语吐槽/对话打断/场景跳转合法，装饰性滥用才砍
            → 不再按个数 FAIL；密度异常（<150 字/个）仅提示人工判断
            （朱雀参考数据：人工段每 ~268 字 1 个，AI 段每 ~136 字 1 个）
    对话    每 120 字 ≥1 个引号（低于此即叙述堆砌，建议项）
    推测词  叙述层 0 容忍（似乎/显然/仿佛/大概/略显）——口语吐槽语境人工判断
    三连排比 同构三连全禁（不是X不是Y不是Z / 没有A没有B没有C / 记得X记得Y记得Z）；
            行文规范豁免「意象对仗收尾三连」（独立短段、末项反转落点），本检查不覆盖该形态
    省略号  留白利器，鼓励 ≥2 个；「……」与「......」（行文规范的吐槽六点）均统计
    数字    具体化鼓励：数字出现次数是人工特征（AI 段 5 个 vs 人工段 26 个）
    套语    行文规范 39 条零频套语（一抹浅笑/瞳孔地震/空气仿佛凝固…）：硬项命中即 FAIL，
            词族易误伤的搭配降为提示（判断标准是搭配与密度，不是单词本身）
    短段    行文规范：动作句不得独占 10 字以内段落（五例外），脚本仅列出供人工判断
    禁词    DEFAULT_FORBIDDEN 命中即 FAIL

退出码：0 = 全部通过；1 = 存在 FAIL（禁词/三连排比/零频套语硬项）
"""

import re
import sys
from pathlib import Path

# ── 红线参数 ────────────────────────────────────────────────
DASH_LIMIT = 250          # 朱雀参考值：每 N 字 1 个为人工段密度（2026-10-07 起不再按此 FAIL，仅作密度异常参考，见 DASH_DENSE）
DASH_DENSE = 150          # 密度低于每 N 字 1 个 = 异常，提示人工判断（正当插入语/跳转不限量）
DIALOG_MIN = 120          # 每 N 字至少 1 个对话引号
DEFAULT_FORBIDDEN = ["突然", "忽然", "只见", "紧接着", "话音刚落", "就在这时", "下一秒", "不由得", "霎时间", "良久", "微微一笑", "淡淡地说", "沉声道",
                     # 2026-08-08 合并 story-deslop 一级禁用词（oh-story-claudecode）
                     "仿佛", "犹如", "宛若", "一丝", "一抹", "些许", "隐约", "深吸一口气", "缓缓", "不禁", "微微", "轻轻", "淡淡",
                     "眼中闪过", "嘴角勾起", "眉头微皱", "瞳孔微缩", "心中一动", "心头一震", "心下了然", "心中暗道", "心底泛起",
                     "不容置疑", "不易察觉", "显而易见", "毫无疑问", "不可否认", "闪烁着光芒", "凛冽",
                     "不由自主", "情不自禁", "自然而然"]
# 2026-10-07 行文规范 39 条零频套语：硬项（搭配明确，命中即一眼假，FAIL）
# 与 DEFAULT_FORBIDDEN 有少量重叠（一丝/一抹/仿佛），重复命中无副作用
XINGWEN_CLICHE_HARD = [
    "一抹浅笑", "一丝苦笑", "红了一瞬", "瞳孔骤然一缩", "瞳孔地震",
    "百感交集", "五味杂陈", "心猛地一沉", "心头一颤", "涌上心口", "涌上心头",
    "不禁红了眼眶", "泪如雨下", "说不出的", "莫名的情绪",
    "空气仿佛凝固", "凝固了空气", "时间仿佛凝固", "空气中飘荡着", "氛围感", "画面感",
    "构成了一幅", "难以捉摸的", "意味深长地", "从这一刻起", "标志着",
]
# 行文规范零频套语：提示项（单词/搭配单独看可能无辜，词族别整族拉黑，人工判断）
XINGWEN_CLICHE_SOFT = [
    "轮廓分明", "轮廓柔和", "指节分明", "描绘着", "跃动着", "守候着", "铭记着",
    "一丝凉意", "悄然地", "看不透", "嗓音低沉", "退后了半步", "折了开来", "人生将",
]
# 二级：升华/总结句式（出现即提示，人工判断；命中即计入升华腔）
UPGRADE_PATTERNS = [
    r"这一刻", r"他终于明白", r"她终于明白", r"他终于意识到", r"她终于意识到",
    r"这才意识到", r"这就是[^。！？]{2,10}的意义", r"一切[^。！？]{2,10}都(?:变得|化为|归于)",
]
GUESS_WORDS = ["似乎", "显然", "仿佛", "大概", "略显"]
TRIPLE_PATTERNS = [
    r"不是[^，。]{2,12}，不是[^，。]{2,12}，不是",   # 不是X，不是Y，不是Z
    r"没有[^，。]{2,12}，没有[^，。]{2,12}，没有",   # 没有A，没有B，没有C
    r"记得[^，。]{2,12}，记得[^，。]{2,12}，记得",   # 记得X，记得Y，记得Z
]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("用法: python density_check.py 稿件.md [--forbidden 词 词 ...]")
        sys.exit(2)

    path = Path(args[0])
    if not path.is_file():
        print(f"文件不存在: {path}")
        sys.exit(2)

    forbidden = DEFAULT_FORBIDDEN
    if "--forbidden" in sys.argv:
        i = sys.argv.index("--forbidden")
        forbidden = sys.argv[i + 1:]

    text = path.read_text(encoding="utf-8")
    body = re.sub(r"\s", "", text)
    total = len(body)

    print(f"=== 朱雀密度红线检查: {path.name} ({total} 字) ===")
    issues = []

    # 1. 破折号（2026-10-07 行文规范：用途纪律，不再按个数 FAIL）
    dashes = body.count("——")
    if dashes:
        density = total / dashes
        if density < DASH_DENSE:
            print(f"破折号: {dashes} 个 (每 {density:.0f} 字 1 个) ! 密度异常，人工判断")
            print("  提示: 插入语吐槽/对话打断/场景跳转分隔为正当用途不限量；装饰性堆叠（无功能解释、连续插语）才砍。悬停可用省略号")
            issues.append("DASH")
        else:
            print(f"破折号: {dashes} 个 (每 {density:.0f} 字 1 个) ✓ (朱雀参考: 人工段每 ~268 字 1 个)")
    else:
        print(f"破折号: 0 个 ✓")

    # 2. 对话密度（兼容直角引号「」与弯引号“”，取配对对数近似）
    quotes = min(body.count("“"), body.count("”")) + body.count("「")
    if quotes:
        density = total / quotes
        ok = density <= DIALOG_MIN
        mark = "✓" if ok else "! 建议"
        if not ok:
            issues.append("DIALOG")
        print(f"对话引号: {quotes} 个 (每 {density:.0f} 字 1 次, 人工段约每 67 字) {mark}")
        if not ok:
            print(f"  提示: 连续叙述过长，把信息塞进对话")
    else:
        print(f"对话引号: 0 个 ✗ 本章无对话？")
        issues.append("FAIL")

    # 3. 推测词
    guess_hits = {w: body.count(w) for w in GUESS_WORDS if body.count(w) > 0}
    if guess_hits:
        print(f"推测词: {guess_hits} ! 叙述层应删除（吐槽口语可留，人工判断）")
    else:
        print(f"推测词: 0 个 ✓")

    # 4. 三连排比
    trip_hits = []
    for pat in TRIPLE_PATTERNS:
        for m in re.finditer(pat, body):
            trip_hits.append(m.group(0)[:30])
    if trip_hits:
        print(f"三连排比: {len(trip_hits)} 处 ✗ FAIL: {trip_hits}")
        issues.append("FAIL")
    else:
        print(f"三连排比: 0 处 ✓")

    # 5. 省略号（留白鼓励；「……」与行文规范吐槽六点「......」均统计）
    ellipsis = body.count("……") + body.count("......")
    if ellipsis >= 2:
        print(f"省略号: {ellipsis} 个 ✓ (留白利器；吐槽六点「......」计入)")
    else:
        print(f"省略号: {ellipsis} 个 ! 建议 ≥2（台词拖音/悬停用省略号）")

    # 6. 数字具体化
    nums = len(re.findall(r"[0-9０-９]", body))
    print(f"数字: {nums} 个 (人工段约 26 个/1600 字，具体数字是人工特征)")

    # 7. 禁词
    fb_hits = {w: body.count(w) for w in forbidden if body.count(w) > 0}
    if fb_hits:
        print(f"禁词: {fb_hits} ✗ FAIL")
        issues.append("FAIL")
    else:
        print(f"禁词: 全清零 ✓")

    # 7.5 升华/总结句式（二级，出现即提示人工判断）
    up_hits = {}
    for pat in UPGRADE_PATTERNS:
        m = re.search(pat, body)
        if m:
            up_hits[pat] = m.group(0)
    if up_hits:
        print(f"升华腔: {up_hits} ! 总结/点题句式（'这一刻/他终于明白/这就是…的意义'），人工判断是否删除")

    # 8. 行文规范零频套语（2026-10-07 并入；硬项 FAIL，词族易误伤的搭配为提示）
    hard_hits = {w: body.count(w) for w in XINGWEN_CLICHE_HARD if body.count(w) > 0}
    if hard_hits:
        print(f"零频套语(硬): {hard_hits} ✗ FAIL（行文规范 12-cliche-substitution.md：写了就是一眼假，按替换方向改写）")
        issues.append("FAIL")
    else:
        print(f"零频套语(硬): 0 处 ✓")
    soft_hits = {w: body.count(w) for w in XINGWEN_CLICHE_SOFT if body.count(w) > 0}
    if soft_hits:
        print(f"零频套语(软): {soft_hits} ! 人工判断（搭配与密度定罪，单词可能无辜；对照 xingwen/12 替换方向）")

    # 9. 行文规范 10 字以内段落（动作句独占短段不合法，五例外人工判断）
    short_paras = []
    for para in re.split(r"\n\s*\n", text):
        clean = re.sub(r"[>\s#*_-]", "", para)
        han_len = len(re.findall(r"[\u4e00-\u9fff0-9０-９]", clean))
        if 0 < han_len <= 10:
            short_paras.append(clean[:14])
    if short_paras:
        print(f"10 字以内段落: {len(short_paras)} 个 {short_paras[:6]} ! 人工判断（五例外合法：时间数字/拟声/否定反问顿/意象对仗三连/标签清单+完整行为句；其余不合法）")
    else:
        print(f"10 字以内段落: 0 个 ✓")

    print()
    if not issues:
        print("结论: 全部通过 ✓")
        sys.exit(0)
    print(f"结论: {len(issues)} 项需处理 (FAIL=必须修, !=建议)")
    sys.exit(1)


if __name__ == "__main__":
    main()
