#!/usr/bin/env python3
"""
DSL 查询执行脚本 - 合并 DSL 改写和数据查询

用法:
    python3 execute_dsl_query.py <dsl_json_string>

示例:
    python3 execute_dsl_query.py '{"modelName":"收款登记模型","type":"chart",...}'
"""

import sys
import json
import time
import asyncio
import os
import requests
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from call_api_get_models import get_api_key
from logger import QueryLogger

try:
    from mcp.client.sse import sse_client
    from mcp import ClientSession

    HAS_MCP = True
except ImportError:
    HAS_MCP = False


def _get_mcp_base_url() -> str:
    config_path = Path(__file__).parent.parent / "api_config.json"
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            return config.get("mcpBaseUrl", "https://mcp-dev.cloud.hecom.cn")
    except Exception:
        return "https://mcp-dev.cloud.hecom.cn"


MCP_BASE_URL = _get_mcp_base_url()


def change_dsl(text: str) -> dict:
    """
    DSL 改写函数 - 验证和修正 DSL

    Args:
        text: DSL JSON 字符串

    Returns:
        {"dsl": "<改写后的 DSL JSON 字符串>"}
    """
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        data = {}

    if isinstance(data, dict):
        # 去掉 modelName 中的空格
        if "modelName" in data and isinstance(data["modelName"], str):
            data["modelName"] = data["modelName"].replace(" ", "")

        # 验证 filter 操作符
        allowed_ops = {"eq", "bte", "gt", "gte", "lt", "lte", "ne", "in", "isNull"}
        filters = data.get("filters", [])
        if isinstance(filters, list):
            for f in filters:
                if isinstance(f, dict) and f.get("op") not in allowed_ops:
                    f["op"] = "in"

        # 验证 metrics 中的指标计算 type
        allowed_metric_types = {"SUM", "AVERAGE", "MAX", "MIN", "COUNT", "CARDINALITY"}
        metric_type_mapping = {"AVG": "AVERAGE"}  # 常见别名映射
        metrics = data.get("metrics", [])
        if isinstance(metrics, list):
            for m in metrics:
                if isinstance(m, dict):
                    metric_type = m.get("type", "")
                    if metric_type in metric_type_mapping:
                        print(f"INFO: 指标 type '{metric_type}' 已转换为 'AVERAGE'")
                        m["type"] = metric_type_mapping[metric_type]
                    elif metric_type and metric_type not in allowed_metric_types:
                        print(
                            f"WARNING: 指标 type '{metric_type}' 不合法，已自动替换为 'SUM'"
                        )
                        m["type"] = "SUM"

        # 如果维度字段>=2 且 type 不是 table，自动改为 table
        if data.get("type") != "table":
            dims = data.get("dimensions")
            if isinstance(dims, list) and len(dims) >= 2:
                data["type"] = "table"

    return {"dsl": json.dumps(data, ensure_ascii=False)}


async def _call_mcp_process_dsl(api_key: str, dsl_str: str) -> Optional[Dict[str, Any]]:
    """
    通过 MCP 调用 processDsl_v0 进行 DSL 改写

    Args:
        api_key: API 密钥
        dsl_str: DSL JSON 字符串

    Returns:
        MCP 响应数据
    """
    async with sse_client(f"{MCP_BASE_URL}/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "processDsl_v0",
                arguments={"header": {"apiKey": api_key}, "param": {"dsl": dsl_str}},
            )

            if result.isError:
                print(f"ERROR: MCP DSL 改写调用错误：{result}")
                return None

            for item in result.content:
                if item.type == "text":
                    try:
                        return json.loads(item.text)
                    except json.JSONDecodeError:
                        return {"data": item.text}
            return None


async def _call_mcp_query_by_agent(
    api_key: str, dsl_str: str
) -> Optional[Dict[str, Any]]:
    """
    通过 MCP 调用 queryByAgent_v0 执行数据查询

    Args:
        api_key: API 密钥
        dsl_str: DSL JSON 字符串

    Returns:
        MCP 响应数据
    """
    async with sse_client(f"{MCP_BASE_URL}/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "queryByAgent_v0",
                arguments={"header": {"apiKey": api_key}, "param": {"dsl": dsl_str}},
            )

            if result.isError:
                print(f"ERROR: MCP 数据查询调用错误：{result}")
                return None

            for item in result.content:
                if item.type == "text":
                    try:
                        return json.loads(item.text)
                    except json.JSONDecodeError:
                        return {"data": item.text}
            return None


def prepare_query_data(dsl_response: dict) -> dict:
    """
    准备查询数据 - 从 DSL 改写响应中提取数据并补充字段

    Args:
        dsl_response: DSL 改写 API 的响应数据

    Returns:
        {"dsl": "<查询用的 DSL JSON 字符串>"}
    """
    # 安全地获取 data 字段
    first = dsl_response.get("data", {}) if dsl_response else {}

    # 补充两个新增字段
    first["question"] = ""
    first["summary"] = False

    return {"dsl": json.dumps(first, ensure_ascii=False)}


def execute_dsl_query(
    dsl_json: str,
    logger: Optional[QueryLogger] = None,
    step: str = "4",
    description: str = "execute-query",
) -> Optional[Dict[str, Any]]:
    """
    执行完整的 DSL 查询流程（DSL 改写 + 数据查询）

    Args:
        dsl_json: DSL JSON 字符串
        logger: 日志记录器实例
        step: 步骤编号
        description: 步骤描述

    Returns:
        查询结果数据，失败返回 None
    """
    # 步骤 1: DSL 改写（使用 MCP）
    print("步骤 1: DSL 改写...")

    if not HAS_MCP:
        print("ERROR: mcp 库未安装")
        return None

    try:
        api_key = get_api_key()
    except ValueError as e:
        print(f"ERROR: {e}")
        return None

    try:
        params = change_dsl(dsl_json)
        dsl_str = params.get("dsl", dsl_json)
        dsl_response = asyncio.run(_call_mcp_process_dsl(api_key, dsl_str))

        if dsl_response is None:
            raise Exception("MCP DSL 改写返回为空")

        print("DSL 改写完成")

        if logger:
            logger.log_api_call(
                step=step,
                description=description,
                api_type="dsl_change",
                question="DSL 改写",
                additional_params={
                    "request": params,
                    "response": dsl_response,
                },
            )
    except Exception as e:
        print(f"ERROR: DSL 改写失败：{e}")
        if logger:
            logger.log_api_response(
                step=step,
                description=description,
                api_type="dsl_change",
                response_data={"error": str(e)},
                status="error",
            )
        return None

    # 步骤 2: 数据查询（使用 MCP）
    print("步骤 2: 执行数据查询...")

    try:
        query_params = prepare_query_data(dsl_response)
        dsl_for_query = query_params.get("dsl", "")
        result = asyncio.run(_call_mcp_query_by_agent(api_key, dsl_for_query))

        if result is None:
            raise Exception("MCP 数据查询返回为空")

        print("数据查询完成")

        if logger:
            logger.log_dsl_only(step, description, dsl_response)
            logger.log_query_data_only(step, description, result)
            logger.log_api_response(
                step=step,
                description=description,
                api_type="query_by_agent",
                response_data=result,
                status="success",
            )

        return result
    except Exception as e:
        error_msg = str(e)
        if "UID is missing in user info rebuildHeaderWithApiKey" in error_msg:
            print()
            print("=" * 60)
            print("⚠️  API 认证失败")
            print("=" * 60)
            print("您的 API 密钥已失效，请更新 api_config.json 中的 hecomapiKey")
            print()
        else:
            print(f"ERROR: 数据查询失败：{e}")
        if logger:
            logger.log_api_response(
                step=step,
                description=description,
                api_type="query_by_agent",
                response_data={"error": error_msg},
                status="error",
            )
        return None


def main():
    if len(sys.argv) < 2:
        print("用法：python3 execute_dsl_query.py <dsl_json_string>")
        print(
            '示例：python3 execute_dsl_query.py \'{"modelName":"收款登记模型","type":"chart",...}\''
        )
        sys.exit(1)

    dsl_json = sys.argv[1]

    # 初始化日志记录器
    logger = QueryLogger()
    session_id = logger.create_session(reuse_existing=True)

    print()
    print("=" * 60)
    print("执行 DSL 查询")
    print("=" * 60)
    print(f"会话 ID: {session_id}")
    print()

    result = execute_dsl_query(
        dsl_json, logger=logger, step="4", description="execute-query"
    )

    if result:
        print()
        print("=" * 60)
        print("查询成功")
        print("=" * 60)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print()
        print(f"日志已保存到：{logger.get_session_dir()}")
    else:
        print()
        print("=" * 60)
        print("查询失败")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
