#!/usr/bin/env python3
"""申论手写稿纸字数推算。

手写作答的字数必须按格纸格数推算，不能用转写文本的字符数代替
（连笔、行书会导致字符数系统性偏低，用字符数判"字数不足"会冤判）。

用法：
  python count_grid.py --cols 25 --lines 11,25,25,25,25,25,25,25,25,25,11 --limit 300
  python count_grid.py --cols 25 --rows 11.4 --limit 300 --chars 278
  python count_grid.py --cols 25 --lines "25 x 10, 11" --limit 300 --json

参数：
  --cols    每行格数（标准申论稿纸 25）
  --lines   逐行实际占用格数，逗号分隔
  --rows    等价于 lines 的简写：行数（可含小数，如 11.4 表示 11 整行 + 0.4 行）
  --note    旁注补充字数（行间/页边插入，计入作答但不占格）
  --limit   题干字数限制，用于超字判定
  --chars   转写文本的字符数，用于双通道校验
  --json    输出 JSON
"""

import argparse
import json
import sys
from typing import List, Optional


def parse_lines(spec: str) -> List[int]:
    """解析 '11,25,25' 或 '25 x 10, 11' 形式。"""
    counts: List[int] = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "x" in chunk.lower():
            left, right = chunk.lower().split("x", 1)
            n = int(right.strip())
            v = int(float(left.strip()))
            counts.extend([v] * n)
        else:
            counts.append(int(float(chunk)))
    return counts


def compute(cols: int, lines: List[int], note: int = 0) -> dict:
    if cols <= 0:
        raise ValueError("cols 必须为正整数")
    if any(x < 0 or x > cols for x in lines):
        raise ValueError(f"每行占用格数必须在 0..{cols} 之间")

    grid_total = sum(lines) + note
    full_lines = sum(1 for x in lines if x == cols)
    partial = [x for x in lines if 0 < x < cols]
    blank = sum(1 for x in lines if x == 0)

    return {
        "cols": cols,
        "line_count": len(lines),
        "full_lines": full_lines,
        "partial_lines": len(partial),
        "blank_lines": blank,
        "grid_chars": grid_total,
        "note_chars": note,
    }


def judge_limit(chars: int, limit: Optional[int]) -> dict:
    if limit is None or limit <= 0:
        return {"limit": None, "verdict": "未提供字数限制"}
    ratio = chars / limit
    over = chars - limit
    if over <= 0:
        return {
            "limit": limit,
            "ratio": round(ratio, 4),
            "over": over,
            "verdict": f"未超限（{chars}/{limit}，占用 {ratio:.1%}）",
        }
    if over / limit <= 0.10:
        verdict = f"超出 {over} 字（{ratio:.1%}），轻微超限；未提供扣分依据，不自动扣分"
    else:
        verdict = f"超出 {over} 字（{ratio:.1%}），明显超限；未提供扣分依据，不自动扣分，须给删减方案"
    return {"limit": limit, "ratio": round(ratio, 4), "over": over, "verdict": verdict}


def cross_check(grid_chars: int, transcript_chars: Optional[int]) -> dict:
    """双通道校验：格数推算值 vs 转写字符数。格数推算值永远优先。"""
    if not transcript_chars or transcript_chars <= 0:
        return {"transcript_chars": None, "note": "未提供转写字符数，跳过校验"}
    if grid_chars == 0:
        return {"transcript_chars": transcript_chars, "note": "格数为 0，无法校验"}
    dev = abs(grid_chars - transcript_chars) / grid_chars
    if dev <= 0.10:
        level = "正常"
        action = "取格数推算值"
    elif dev <= 0.25:
        level = "偏差偏大"
        action = "取格数推算值，报告中标注偏差（疑转写漏字或涂改误计）"
    else:
        level = "转写不可靠"
        action = "取格数推算值，且不判超字/字数不足，只提示复核"
    return {
        "transcript_chars": transcript_chars,
        "deviation": round(dev, 4),
        "level": level,
        "action": action,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="申论手写稿纸字数推算")
    p.add_argument("--cols", type=int, default=25, help="每行格数，默认 25")
    p.add_argument("--lines", type=str, default=None, help="逐行占用格数，逗号分隔")
    p.add_argument("--rows", type=float, default=None, help="行数简写（可含小数）")
    p.add_argument("--note", type=int, default=0, help="旁注补充字数")
    p.add_argument("--limit", type=int, default=None, help="题干字数限制")
    p.add_argument("--chars", type=int, default=None, help="转写文本字符数")
    p.add_argument("--json", action="store_true", help="输出 JSON")
    args = p.parse_args()

    if args.cols <= 0:
        print("错误：--cols 必须为正整数", file=sys.stderr)
        return 2
    if args.note < 0:
        print("错误：--note 不能为负数", file=sys.stderr)
        return 2
    if args.limit is not None and args.limit <= 0:
        print("错误：--limit 必须为正整数", file=sys.stderr)
        return 2
    if args.chars is not None and args.chars < 0:
        print("错误：--chars 不能为负数", file=sys.stderr)
        return 2
    if args.rows is not None and args.rows <= 0:
        print("错误：--rows 必须大于 0", file=sys.stderr)
        return 2

    if args.lines:
        lines = parse_lines(args.lines)
    elif args.rows is not None:
        whole = int(args.rows)
        frac = args.rows - whole
        lines = [args.cols] * whole
        if frac > 0:
            lines.append(round(frac * args.cols))
    else:
        print("错误：需要 --lines 或 --rows", file=sys.stderr)
        return 2

    try:
        base = compute(args.cols, lines, args.note)
    except ValueError as e:
        print(f"错误：{e}", file=sys.stderr)
        return 2

    result = {
        **base,
        "limit_check": judge_limit(base["grid_chars"], args.limit),
        "cross_check": cross_check(base["grid_chars"], args.chars),
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(f"每行格数      : {result['cols']}")
    print(f"作答行数      : {result['line_count']}（满行 {result['full_lines']}，未满 {result['partial_lines']}，空行 {result['blank_lines']}）")
    print(f"格数推算字数  : {result['grid_chars']}")
    if result["note_chars"]:
        print(f"  其中旁注    : {result['note_chars']}")
    print()
    cc = result["cross_check"]
    if cc.get("transcript_chars"):
        print(f"转写字符数    : {cc['transcript_chars']}")
        print(f"偏差          : {cc['deviation']:.1%}  → {cc['level']}")
        print(f"处理          : {cc['action']}")
    else:
        print(f"校验          : {cc['note']}")
    print()
    lc = result["limit_check"]
    print(f"字数判定      : {lc['verdict']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
