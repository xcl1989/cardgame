#!/usr/bin/env python3
"""
数据分析 - 安全计算器

用于在步骤 5 中执行准确的数值计算，避免大模型计算错误。

功能：
1. 安全的数学表达式计算（支持加减乘除、括号等）
2. 批量执行计算任务
3. 返回精确的计算结果

使用示例：
    # 命令行调用
    python3 calculator.py "[['计算总和','100+200+300'],['转换万元','500000/10000']]"

    # 返回结果
    ["600", "50"]
"""

import json
import re
import sys
from typing import List, Tuple
import operator


# 安全的数学运算符映射
SAFE_OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
    "**": operator.pow,
}


def tokenize(expression: str) -> List[str]:
    """将表达式拆分为 tokens"""
    tokens = []
    i = 0
    while i < len(expression):
        if expression[i].isspace():
            i += 1
            continue

        # 检查多位运算符
        if i + 1 < len(expression) and expression[i : i + 2] in ["//", "**"]:
            tokens.append(expression[i : i + 2])
            i += 2
            continue

        if expression[i] in "+-*/%()":
            tokens.append(expression[i])
            i += 1
        elif expression[i].isdigit() or expression[i] == ".":
            j = i
            while j < len(expression) and (
                expression[j].isdigit() or expression[j] == "."
            ):
                j += 1
            tokens.append(expression[i:j])
            i = j
        else:
            raise ValueError(f"非法字符：{expression[i]}")

    return tokens


def evaluate_expression(expression: str) -> float:
    """
    安全地计算数学表达式

    Args:
        expression: 数学表达式字符串，如 "100+200*3"

    Returns:
        计算结果（浮点数）
    """
    # 只允许数字、运算符和括号
    if not re.match(r"^[\d\s\+\-\*\/\%\(\)\.]+$", expression):
        raise ValueError(f"表达式包含非法字符：{expression}")

    try:
        # 使用 eval 但已经通过正则表达式限制了字符范围
        result = eval(expression)
        return float(result)
    except Exception as e:
        raise ValueError(f"计算失败：{expression} - {str(e)}")


def calculate(tasks: List[List[str]]) -> List[str]:
    """
    批量执行计算任务

    Args:
        tasks: 计算任务列表，格式为 [[描述，表达式], [描述，表达式], ...]
               例如：[['计算 Q1+Q2', '308000+197990'], ['转换万元', '505990/10000']]

    Returns:
        计算结果列表，格式为 [结果 1, 结果 2, ...]
        例如：['505990.0', '50.599']
    """
    results = []

    for i, task in enumerate(tasks):
        if len(task) != 2:
            results.append(f"错误：任务{i + 1}格式不正确，应为 [描述，表达式]")
            continue

        description, expression = task

        try:
            result = evaluate_expression(expression)

            # 格式化结果：如果是整数则去掉小数部分
            if result == int(result):
                results.append(str(int(result)))
            else:
                # 保留最多 4 位小数，去掉末尾的 0
                formatted = f"{result:.4f}".rstrip("0").rstrip(".")
                results.append(formatted)

        except Exception as e:
            results.append(f"错误：{description} - {str(e)}")

    return results


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print('使用方法：python3 calculator.py "[[描述，表达式], [描述，表达式], ...]"')
        print("\n示例：")
        print(
            "  python3 calculator.py \"[['计算总和','100+200+300'],['转换万元','500000/10000']]\""
        )
        print("\n返回结果：")
        print('  ["600", "50"]')
        sys.exit(1)

    try:
        # 解析 JSON 格式的输入
        input_str = sys.argv[1]
        tasks = json.loads(input_str)

        if not isinstance(tasks, list):
            raise ValueError("输入必须是列表格式")

        # 执行计算
        results = calculate(tasks)

        # 返回 JSON 格式结果
        print(json.dumps(results, ensure_ascii=False))

    except json.JSONDecodeError as e:
        print(json.dumps(["错误：JSON 解析失败 - " + str(e)]), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps(["错误：" + str(e)]), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
