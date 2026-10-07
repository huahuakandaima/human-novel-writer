#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zhuque_check.py — 朱雀 AIGC 文本检测在线门禁（腾讯云 EdgeOne Makers @makers/zhuque-text）

接口文档：https://cloud.tencent.com/document/product/1552/137539
开通步骤：腾讯云 EdgeOne 控制台 → Makers → Models → API Key 页面 → 创建 API Key。
计费：每月免费 50 万 token；实际扣减量以响应 makers_models_usage.total_tokens 为准
（一章 ~3000 字约 3-5k token，免费额度约够 100+ 章/月）。

用法：
    python scripts/zhuque_check.py 正文/第005章-xxx.md
    python scripts/zhuque_check.py 稿件.md --threshold 0.5 --top 10
    echo 一段文字 | python scripts/zhuque_check.py --stdin
    ZHUQUE_API_KEY=xxxx python scripts/zhuque_check.py 稿件.md

API Key 读取顺序：--key 参数 → 环境变量 ZHUQUE_API_KEY → scripts/zhuque_api_key.txt
（key 文件已列入 .gitignore，严禁提交到仓库）。

判定口径（对齐 SKILL.md 特殊规则「朱雀 AIGC>0.5 且人工读感确认才触发删除重写制」）：
    AI 占比    labels_ratio["1"] + 疑似占比 labels_ratio["2"] = AIGC 合计，对照阈值
    硬阈值     --threshold（默认 0.5）：AIGC 合计超过 → exit 1，按删除重写制处理
               （先人工读感确认"确实 AI"；技法化写法的密度类高分区不触发）
    逐段置信度 默认 is_merge=false 逐段输出，label 1/2 的高分区片段清单即
               「已通过片段一律不动，只重写未过片段」的定位依据
首次使用建议：拿几章已过稿的旧文跑一遍，和朱雀网页版（matrix.tencent.com/ai-detect）
的分数对一次，偏差大就调 --threshold 校准。

退出码：0 = AIGC 合计 ≤ 阈值；1 = 超阈值（走删除重写制判定）；2 = 调用错误
（无 Key / 网络失败 / API 报错 / 文本为空）。

注意：文档未给出单次文本长度上限；若 API 报长度类错误，把章节按场景手动分片重试。
markdown 默认做轻量清洗（去 YAML frontmatter/代码块/标题#/强调*/水平线）后发送，
--raw 关闭清洗原样发送。
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://ai-gateway.edgeone.link/v1/providers/zhuque-text/classify"
KEY_FILE = Path(__file__).resolve().parent / "zhuque_api_key.txt"
LABEL_NAME = {"0": "人工", "1": "AI", "2": "疑似AI"}


def find_key(cli_key):
    if cli_key:
        return cli_key.strip()
    env = os.environ.get("ZHUQUE_API_KEY", "").strip()
    if env:
        return env
    if KEY_FILE.is_file():
        saved = KEY_FILE.read_text(encoding="utf-8-sig").strip()
        if saved:
            return saved
    return None


def strip_markdown(text):
    # YAML frontmatter
    text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, flags=re.S)
    # 围栏代码块
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    # 标题标记、水平线、强调符号
    lines = []
    for line in text.splitlines():
        if re.fullmatch(r"\s*(:?-{3,}|\*{3,}|={3,})\s*", line):
            continue
        lines.append(line)
    text = "\n".join(lines)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.M)
    text = re.sub(r"\*\*?|__?|`", "", text)
    return text.strip()


def call_api(text, key, merge):
    body = json.dumps({"text": text, "is_merge": merge}).encode("utf-8")
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
    })
    # 国内端点，直连优先；失败再试系统代理（clash 等可能拦截）
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        return opener.open(req, timeout=60)
    except (urllib.error.URLError, OSError):
        return urllib.request.build_opener().open(req, timeout=60)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="朱雀 AIGC 检测在线门禁（EdgeOne Makers）")
    ap.add_argument("file", nargs="?", help="待检测稿件（.md/.txt）")
    ap.add_argument("--stdin", action="store_true", help="从标准输入读取文本")
    ap.add_argument("--threshold", type=float, default=0.5,
                    help="AIGC 合计（AI+疑似）硬阈值，默认 0.5")
    ap.add_argument("--top", type=int, default=10, help="列出未过片段条数，默认 10")
    ap.add_argument("--merge", action="store_true",
                    help="is_merge=true（整篇合并置信度，不逐段）")
    ap.add_argument("--raw", action="store_true", help="不做 markdown 清洗，原样发送")
    ap.add_argument("--key", help="API Key（一般不用，走环境变量或 key 文件）")
    args = ap.parse_args()

    if args.stdin:
        text = sys.stdin.read()
    elif args.file:
        path = Path(args.file)
        if not path.is_file():
            print(f"[错误] 文件不存在：{path}")
            sys.exit(2)
        text = path.read_text(encoding="utf-8-sig")
    else:
        ap.print_help()
        sys.exit(2)

    if not args.raw:
        text = strip_markdown(text)
    text = text.strip()
    if not text:
        print("[错误] 待检测文本为空（清洗后无内容？加 --raw 试试）")
        sys.exit(2)

    key = find_key(args.key)
    if not key:
        print("[错误] 未找到 API Key。三选一：")
        print(f"  1. 环境变量：set ZHUQUE_API_KEY=你的Key")
        print(f"  2. 写入文件：{KEY_FILE}（已 gitignore，勿提交）")
        print("  3. EdgeOne 控制台 → Makers → Models → API Key 创建，见文档")
        print("     https://cloud.tencent.com/document/product/1552/137539")
        sys.exit(2)

    try:
        with call_api(text, key, args.merge) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        print(f"[错误] API 返回 HTTP {e.code}：{detail or e.reason}")
        if e.code in (401, 403):
            print("       Key 无效或未开通朱雀模型：检查 EdgeOne 控制台 Makers → API Key")
        sys.exit(2)
    except Exception as e:
        print(f"[错误] 请求失败：{e}")
        print("       已尝试直连与系统代理两条线路；检查网络后重试")
        sys.exit(2)

    if data.get("status") != "success":
        print(f"[错误] API 推理失败：status={data.get('status')} msg={data.get('msg')}")
        sys.exit(2)

    ratio = data.get("labels_ratio") or {}
    human = float(ratio.get("0", 0))
    ai = float(ratio.get("1", 0))
    suspect = float(ratio.get("2", 0))
    total = ai + suspect
    softmax = float(data.get("softmax_confidence", 0))
    usage = (data.get("makers_models_usage") or {}).get("total_tokens", "?")

    src = "stdin" if args.stdin else args.file
    mode = "merge" if args.merge else "per-segment"
    print("── 朱雀 AIGC 检测（EdgeOne Makers @makers/zhuque-text）──")
    print(f"稿件：{src}（发送 {len(text)} 字，is_merge={mode}）")
    print(f"人工 {human:.2%} ｜ AI {ai:.2%} ｜ 疑似AI {suspect:.2%}")
    print(f"AIGC 合计（AI+疑似）{total:.2%} ｜ softmax {softmax:.4f} ｜ ratio_conf "
          f"{float(data.get('ratio_confidence', 0)):.4f}")
    print(f"本次扣减额度：{usage} token")

    segments = data.get("segment_labels") or []
    bad = [s for s in segments if str(s.get("label")) in ("1", "2")]
    bad.sort(key=lambda s: s.get("conf", 0), reverse=True)
    if segments:
        n1 = sum(1 for s in segments if str(s.get("label")) == "1")
        n2 = len(bad) - n1
        print(f"分段：共 {len(segments)} 段，AI {n1} 段 / 疑似 {n2} 段 / 人工 "
              f"{len(segments) - len(bad)} 段")

    if total > args.threshold:
        print(f"判定：FAIL（AIGC 合计 {total:.2%} > 阈值 {args.threshold:.0%}）")
        print("       按「删除重写制」处理：先人工读感确认'确实 AI'再触发；")
        print("       已通过片段（conf<0.5 的 AI/疑似段除外）一律不动，只重写未过片段。")
        verdict = 1
    else:
        print(f"判定：PASS（AIGC 合计 {total:.2%} ≤ 阈值 {args.threshold:.0%}）")
        if softmax > 0.5:
            print("       softmax 整体置信度偏高，建议人工冷读复核")
        verdict = 0

    if bad and not args.merge:
        print(f"未过片段（label 1/2，按置信度降序，top {args.top}）：")
        for s in bad[: args.top]:
            label = LABEL_NAME.get(str(s.get("label")), "?")
            excerpt = str(s.get("text", "")).replace("\n", " ")[:40]
            print(f"  #{s.get('order')}  conf={s.get('conf'):.4f}  {label}  「{excerpt}…」"
                  f"（position {s.get('position')}）")
    sys.exit(verdict)


if __name__ == "__main__":
    main()
