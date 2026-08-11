#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
density_check.py — 朱雀密度红线检查器（第八版检测器同文对照实证）

用法：
    python scripts/density_check.py 稿件.md
    python scripts/density_check.py 稿件.md --forbidden 突然 忽然 只见

对照红线（来自《读条》第 1 章同文实测：人工段 vs AI 段差异量化）：
    破折号  人工每 ~268 字 1 个 / AI 每 ~136 字 1 个 → 每 250 字 ≤1 个
    对话    人工每 ~67 字 1 个引号 → 每 120 字 ≥1 个引号（低于此即叙述堆砌）
    推测词  叙述层 0 容忍（似乎/显然/仿佛/大概/略显）——口语吐槽语境人工判断
    三连排比 全禁（不是X不是Y不是Z / 没有A没有B没有C / 记得X记得Y记得Z）
    省略号  留白利器，鼓励 ≥2 个（悬停/拖音，替代破折号）
    数字    具体化鼓励：数字出现次数是人工特征（AI 段 5 个 vs 人工段 26 个）

退出码：0 = 全部通过；1 = 存在 FAIL（禁词/三连排比/破折号超限）
"""

import re
import sys
from pathlib import Path

# ── 红线参数 ────────────────────────────────────────────────
DASH_LIMIT = 250          # 每 N 字允许 1 个破折号
DIALOG_MIN = 120          # 每 N 字至少 1 个对话引号
DEFAULT_FORBIDDEN = ["突然", "忽然", "只见", "紧接着", "话音刚落", "就在这时", "下一秒", "不由得", "霎时间", "良久", "微微一笑", "淡淡地说", "沉声道",
                     # 2026-08-08 合并 story-deslop 一级禁用词（oh-story-claudecode）
                     "仿佛", "犹如", "宛若", "一丝", "一抹", "些许", "隐约", "深吸一口气", "缓缓", "不禁", "微微", "轻轻", "淡淡",
                     "眼中闪过", "嘴角勾起", "眉头微皱", "瞳孔微缩", "心中一动", "心头一震", "心下了然", "心中暗道", "心底泛起",
                     "不容置疑", "不易察觉", "显而易见", "毫无疑问", "不可否认", "闪烁着光芒", "凛冽",
                     "不由自主", "情不自禁", "自然而然"]
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

    # 1. 破折号密度
    dashes = body.count("——")
    if dashes:
        density = total / dashes
        ok = density >= DASH_LIMIT
        mark = "✓" if ok else "✗ FAIL"
        if not ok:
            issues.append("FAIL")
        print(f"破折号: {dashes} 个 (每 {density:.0f} 字 1 个, 红线每 {DASH_LIMIT} 字) {mark}")
        if not ok:
            print(f"  提示: 需砍到 ≤{total // DASH_LIMIT} 个，停顿用句号，悬停用省略号")
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

    # 5. 省略号（留白鼓励）
    ellipsis = body.count("……")
    if ellipsis >= 2:
        print(f"省略号: {ellipsis} 个 ✓ (留白利器)")
    else:
        print(f"省略号: {ellipsis} 个 ! 建议 ≥2（台词拖音/悬停用省略号，别用破折号顶替）")

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

    print()
    if not issues:
        print("结论: 全部通过 ✓")
        sys.exit(0)
    print(f"结论: {len(issues)} 项需处理 (FAIL=必须修, !=建议)")
    sys.exit(1)


if __name__ == "__main__":
    main()
