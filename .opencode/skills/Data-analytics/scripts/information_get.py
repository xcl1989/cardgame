#!/usr/bin/env python3
"""
数据和指标信息获取 - 步骤 1

调用 API 获取企业的数据模型和指标库信息，带日志记录功能。

用法:
    python3 information_get.py

输出:
    - 在控制台显示数据模型和指标库摘要
    - 日志保存到 logs/{session_id}/
"""

import sys
import json
import time
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

sys.path.insert(0, str(Path(__file__).parent))
from call_api_get_models import get_api_key
from logger import QueryLogger

try:
    from mcp.client.sse import sse_client
    from mcp import ClientSession

    HAS_MCP = True
except ImportError:
    HAS_MCP = False


class CredentialExpiredError(Exception):
    """凭证过期异常"""

    pass


class APIKeyInvalidError(Exception):
    """API Key 失效异常"""

    pass


def _get_mcp_base_url() -> str:
    config_path = Path(__file__).parent.parent / "api_config.json"
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            return config.get("mcpBaseUrl", "https://mcp-dev.cloud.hecom.cn")
    except Exception:
        return "https://mcp-dev.cloud.hecom.cn"


MCP_BASE_URL = _get_mcp_base_url()


async def _call_mcp_list_model_infos(api_key: str) -> Optional[Dict[str, Any]]:
    """
    通过 MCP 调用 listModelInfos_v0 获取数据模型

    Args:
        api_key: API 密钥

    Returns:
        MCP 响应数据
    """
    async with sse_client(f"{MCP_BASE_URL}/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "listModelInfos_v0",
                arguments={"header": {"apiKey": api_key}},
            )

            if result.isError:
                print(f"ERROR: MCP 调用错误：{result}")
                return None

            # 解析 MCP 响应结果
            for item in result.content:
                if item.type == "text":
                    try:
                        response = json.loads(item.text)
                        if isinstance(response, dict):
                            text = response.get("text", "") or str(response)
                            if "UID is missing" in text or "invalid" in text.lower():
                                raise APIKeyInvalidError(
                                    "APIKey 失效，请联系管理员更新 hecomapiKey 配置"
                                )
                        return response
                    except json.JSONDecodeError:
                        if "UID is missing" in item.text:
                            raise APIKeyInvalidError(
                                "APIKey 失效，请联系管理员更新 hecomapiKey 配置"
                            )
                        return {"data": item.text}
            return None


def call_api_get_models(model_name: str = "") -> Optional[Dict[str, Any]]:
    """
    调用 API 获取数据模型（使用 MCP）

    Args:
        model_name: 模型名称，为空时获取所有模型

    Returns:
        API 响应数据，失败返回 None
    """
    if not HAS_MCP:
        print("ERROR: mcp 库未安装，请运行 pip install mcp")
        return None

    try:
        api_key = get_api_key()
    except ValueError as e:
        print(f"ERROR: {e}")
        return None

    try:
        result = asyncio.run(_call_mcp_list_model_infos(api_key))
        print(f"DEBUG: MCP 调用返回")
        return result
    except Exception as e:
        print(f"ERROR: MCP 请求异常：{e}")
        return None


async def _call_mcp_query_indicators(
    api_key: str, question: str = ""
) -> Optional[Dict[str, Any]]:
    """
    通过 MCP 调用 queryIndicatorByBossAssist_v0 获取指标库

    Args:
        api_key: API 密钥
        question: 查询问题

    Returns:
        MCP 响应数据
    """
    async with sse_client(f"{MCP_BASE_URL}/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "queryIndicatorByBossAssist_v0",
                arguments={
                    "header": {"apiKey": api_key},
                    "param": {"question": question},
                },
            )

            if result.isError:
                print(f"ERROR: MCP 指标库调用错误：{result}")
                return None

            for item in result.content:
                if item.type == "text":
                    try:
                        response = json.loads(item.text)
                        if isinstance(response, dict):
                            text = response.get("text", "") or str(response)
                            if "UID is missing" in text or "invalid" in text.lower():
                                raise APIKeyInvalidError(
                                    "APIKey 失效，请联系管理员更新 hecomapiKey 配置"
                                )
                        return response
                    except json.JSONDecodeError:
                        if "UID is missing" in item.text:
                            raise APIKeyInvalidError(
                                "APIKey 失效，请联系管理员更新 hecomapiKey 配置"
                            )
                        return {"data": item.text}
            return None


def call_api_get_indicators(question: str = "") -> Optional[Dict[str, Any]]:
    """
    调用 API 获取指标库信息（使用 MCP）

    Args:
        question: 查询问题，用于获取相关指标

    Returns:
        API 响应数据，失败返回 None
    """
    if not HAS_MCP:
        print("ERROR: mcp 库未安装，请运行 pip install mcp")
        return None

    try:
        api_key = get_api_key()
    except ValueError as e:
        print(f"ERROR: {e}")
        return None

    try:
        result = asyncio.run(_call_mcp_query_indicators(api_key, question))
        print(f"DEBUG: MCP 指标库调用返回")
        return result
    except Exception as e:
        print(f"ERROR: MCP 指标库请求异常：{e}")
        return None


def parse_models_from_response(response_data: dict) -> list:
    """
    从 API 响应中解析模型数据

    Args:
        response_data: API 响应数据

    Returns:
        模型列表
    """
    if not response_data:
        return []

    result_code = response_data.get("result", "")
    if result_code != "0":
        print(f"WARNING: API 返回结果码：{result_code}")
        return []

    data = response_data.get("data", [])
    return data


def parse_indicators_from_response(response_data: dict) -> list:
    """
    从 API 响应中解析指标数据

    Args:
        response_data: API 响应数据

    Returns:
        指标列表
    """
    if not response_data:
        return []

    result_code = response_data.get("result", "")
    if result_code != "0":
        print(f"WARNING: 指标库 API 返回结果码：{result_code}")
        return []

    data = response_data.get("data", "")

    # 如果 data 是字符串，按行解析
    if isinstance(data, str):
        indicators = []
        lines = [line.strip() for line in data.split("\n") if line.strip()]
        for line in lines:
            # 解析格式：1.【指标名称】：xxx；【取值逻辑】：xxx
            if "【指标名称】" in line:
                try:
                    # 提取指标名称
                    start = line.find("【指标名称】：") + 6
                    end = line.find("；", start)
                    if end == -1:
                        end = len(line)
                    name = line[start:end].strip()
                    # 去除前导冒号
                    if name.startswith("："):
                        name = name[1:].strip()

                    # 提取取值逻辑
                    desc = ""
                    if "【取值逻辑】" in line:
                        start = line.find("【取值逻辑】：") + 6
                        desc = line[start:].strip()
                        if desc.endswith("。"):
                            desc = desc[:-1]
                        # 去除前导冒号
                        if desc.startswith("："):
                            desc = desc[1:].strip()

                    indicators.append(
                        {"name": name, "description": desc, "category": "指标库"}
                    )
                except Exception as e:
                    print(f"WARNING: 解析指标行失败：{line}, 错误：{e}")
        return indicators
    elif isinstance(data, list):
        return data
    elif isinstance(data, dict):
        return [data]
    else:
        print(f"WARNING: 指标库数据格式异常：{type(data)}")
        return []


def print_models_summary(models: list, session_dir: str = ""):
    """打印模型摘要（包含完整字段列表）

    Args:
        models: 模型列表
        session_dir: 会话日志目录路径
    """
    print()
    print("=" * 60)
    print("📊 数据模型信息")
    print("=" * 60)
    print(f"共发现 {len(models)} 个数据模型")
    print()

    for i, model in enumerate(models, 1):
        table_name = model.get("tableName", "N/A")
        desc = model.get("description", "") or "无描述"
        columns = model.get("columns", [])
        print(f"{i}. {table_name}  ({len(columns)} 个字段)")
        print(f"模型说明：{i}. {desc} ")
        print(f"   完整字段列表（步骤 2 请直接复制 columnName）:")
        for col in columns:
            col_name = col.get("columnName", "N/A")
            col_label = col.get("label", "")
            col_type = col.get("type", "")
            col_desc = col.get("description", "")
            desc_text = f" - {col_desc}" if col_desc else ""
            print(f"     - {col_name} ({col_label}, {col_type}){desc_text}")
        print()

    print("=" * 60)
    print()
    print("⚠️  重要提示：")
    print("   步骤 2 选择模型时，必须直接复制上面的完整 columnName（带表前缀）")
    print(f"   完整数据已保存到：{session_dir}/step1-get-all-models-models.json")
    print("=" * 60)


def print_indicators_summary(indicators: list):
    """打印指标摘要"""
    print()
    print("=" * 60)
    print("📈 指标库信息")
    print("=" * 60)
    print(f"共发现 {len(indicators)} 个指标")
    print()

    for i, indicator in enumerate(indicators, 1):
        name = indicator.get("name", indicator.get("indicatorName", "N/A"))
        desc = indicator.get("description", "") or "无描述"
        category = indicator.get(
            "category", indicator.get("indicatorCategory", "未分类")
        )
        print(f"{i}. {name} - {category}")
        if desc:
            print(f"   描述：{desc}")

    print("=" * 60)


def main():
    logger = QueryLogger()
    session_id = logger.create_session(reuse_existing=False)

    print()
    print("=" * 60)
    print("步骤 1: 获取数据模型和指标库信息")
    print("=" * 60)
    print(f"会话 ID: {session_id}")
    print()

    models = []
    indicators = []

    print("【1/2】正在调用 API 获取数据模型...")
    print()
    try:
        response_data = call_api_get_models()
    except APIKeyInvalidError as e:
        print(f"\n❌ 错误：{str(e)}")
        print()
        sys.exit(1)
    except CredentialExpiredError as e:
        print(f"\n❌ 错误：{str(e)}")
        print()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误：{str(e)}")
        print()
        sys.exit(1)

    if response_data:
        logger.log_api_call(
            step="1",
            description="get-all-models",
            api_type="get_models",
            question="获取所有数据模型",
            additional_params={"raw_response": response_data},
        )

    models = parse_models_from_response(response_data if response_data else {})

    if not models:
        print("WARNING: 未获取到数据模型信息")
    else:
        logger.log_models_info("1", "get-all-models", models)
        logger.log_api_response(
            step="1",
            description="get-all-models",
            api_type="get_models",
            response_data={"success": True, "model_count": len(models)},
        )
        print_models_summary(models, session_dir=str(logger.get_session_dir()))

    print()
    print("【2/2】正在调用 API 获取指标库信息...")
    print()

    try:
        indicator_response = call_api_get_indicators(question="")
    except APIKeyInvalidError as e:
        print(f"\n❌ 错误：{str(e)}")
        print()
        sys.exit(1)
    except CredentialExpiredError as e:
        print(f"\n❌ 错误：{str(e)}")
        print()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误：{str(e)}")
        print()
        sys.exit(1)

    if indicator_response:
        logger.log_api_call(
            step="1",
            description="get-indicators",
            api_type="get_indicators",
            question="获取指标库信息",
            additional_params={"raw_response": indicator_response},
        )

    indicators = parse_indicators_from_response(
        indicator_response if indicator_response else {}
    )

    if not indicators:
        print("WARNING: 未获取到指标库信息")
    else:
        logger.log_api_response(
            step="1",
            description="get-indicators",
            api_type="get_indicators",
            response_data={"success": True, "indicator_count": len(indicators)},
        )
        print_indicators_summary(indicators)

    print()
    print("=" * 60)
    print("✅ 步骤 1 完成：已获取数据模型和指标库信息")
    print("=" * 60)
    print()
    print("提示：现在可以进行步骤 2，由大模型根据具体问题选择相关模型和指标")
    print("=" * 60)
    print()

    print(f"日志已保存到：{logger.get_session_dir()}")
    print()


if __name__ == "__main__":
    main()
