#!/usr/bin/env python3
"""
获取模型列表的脚本

使用方法:
    python3 scripts/list_models.py --list                  # 获取模型列表
    python3 scripts/list_models.py --search "收款"         # 搜索模型
"""

import json
import requests
import argparse
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
HEADER_FILE = SCRIPT_DIR / "header.json"
CACHE_DIR = SCRIPT_DIR / ".cache"


def load_headers() -> dict:
    """从 header.json 加载认证信息"""
    if not HEADER_FILE.exists():
        raise FileNotFoundError(f"认证文件不存在：{HEADER_FILE}")

    with open(HEADER_FILE, "r", encoding="utf-8") as f:
        headers_data = json.load(f)

    return {
        "Content-Type": "application/json",
        "accessToken": headers_data.get("accessToken", ""),
        "empCode": headers_data.get("empCode", ""),
        "entCode": headers_data.get("entCode", ""),
        "uid": headers_data.get("uid", ""),
        "app": "dataModel",
        "act": "operation",
        "clientTag": "web",
    }


def ensure_cache_dir():
    """确保缓存目录存在"""
    CACHE_DIR.mkdir(exist_ok=True)


def get_models_list() -> list:
    """获取所有模型列表"""
    headers = load_headers()
    url = "https://dev.cloud.hecom.cn/biserver//paas/app/dataModel/operation/list"

    response = requests.post(
        url,
        headers=headers,
        json={"modelName": "", "pageNo": 1, "pageSize": 9999},
        timeout=30,
    )

    if response.status_code != 200:
        raise Exception(f"API 请求失败：{response.status_code}")

    data = response.json()
    # 响应可能没有 code 字段
    return data.get("data", {}).get("list", [])


def get_model_detail(model_id: int) -> dict:
    """获取模型详情"""
    headers = load_headers()
    url = f"https://dev.cloud.hecom.cn/biserver/paas/app/dataModel/operation/getModelDetail/{model_id}"

    response = requests.post(
        url, headers=headers, json={"id": str(model_id)}, timeout=30
    )

    if response.status_code != 200:
        raise Exception(f"API 请求失败：{response.status_code}")

    data = response.json()
    # 响应可能没有 code 字段
    return data.get("data", {})


def cmd_list(args):
    """列出所有模型"""
    print("📡 正在获取模型列表...")

    try:
        models = get_models_list()
    except FileNotFoundError as e:
        print(f"❌ 错误：{e}")
        return
    except Exception as e:
        print(f"❌ 错误：{e}")
        return

    ensure_cache_dir()

    # 保存到缓存
    cache_file = CACHE_DIR / "models_list.json"
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(models, f, ensure_ascii=False, indent=2)

    print(f"✓ 已保存 {len(models)} 个模型到 {cache_file}")

    if args.search:
        if args.exact:
            models = [m for m in models if args.search == m.get("name", "")]
        else:
            models = [
                m for m in models if args.search.lower() in m.get("name", "").lower()
            ]
        print(f"🔍 搜索结果：'{args.search}' - 找到 {len(models)} 个模型")

    # 显示
    print(f"\n=== 模型列表 (共 {len(models)} 个) ===")
    print(
        "ID              名称                                      节点数        更新时间"
    )
    print("-" * 100)

    for model in models[:20]:
        model_id = str(model.get("id", ""))
        name = model.get("name", "")
        node_count = len(model.get("modelDatasetDTOList", []))
        updated = model.get("updatedOn", "")
        if updated:
            updated = datetime.fromtimestamp(updated / 1000).strftime("%Y-%m-%d")

        print(f"{model_id:<15} {name:<40} {node_count:<12} {updated}")

    if len(models) > 20:
        print(f"... 还有 {len(models) - 20} 个模型")


def cmd_detail(args):
    """获取模型详情"""
    ensure_cache_dir()

    try:
        model = get_model_detail(args.model_id)
    except FileNotFoundError as e:
        print(f"❌ 错误：{e}")
        return
    except Exception as e:
        print(f"❌ 错误：{e}")
        return

    if not model:
        print(f"⚠️  未找到模型 {args.model_id}")
        return

    # 显示详情
    print(f"\n=== 模型详情 ===")
    print(f"ID: {model.get('id', '')}")
    print(f"名称：{model.get('name', '')}")
    print(f"企业编码：{model.get('entCode', '')}")
    print(f"版本：{model.get('version', '')}")
    print(f"状态：{model.get('status', '')}")
    print(
        f"创建时间：{datetime.fromtimestamp(model.get('createdOn', 0) / 1000).strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print(
        f"更新时间：{datetime.fromtimestamp(model.get('updatedOn', 0) / 1000).strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # 显示节点
    print(f"\n包含节点 ({len(model.get('modelDatasetDTOList', []))} 个):")
    for node in model.get("modelDatasetDTOList", []):
        dataset_name = node.get("datasetName", "")
        dataset_label = node.get("datasetLabel", "")
        fields = node.get("fields", [])
        print(f"  - {dataset_label} ({dataset_name}): {len(fields)} 个字段")
        for field in fields[:5]:
            print(
                f"      • {field.get('fieldLabel', '')} ({field.get('fieldName', '')})"
            )
        if len(fields) > 5:
            print(f"      ... 还有 {len(fields) - 5} 个字段")

    # 显示关联关系
    relations = model.get("modelRelationDTOList", [])
    if relations:
        print(f"\n关联关系 ({len(relations)} 个):")
        for rel in relations:
            from_node = rel.get("from", "")
            to_node = rel.get("to", "")
            source_field = rel.get("sourceField", {}).get("fieldName", "")
            target_field = rel.get("targetField", {}).get("fieldName", "")
            relation_type = rel.get("relationType", "")
            print(
                f"  - {from_node}.{source_field} → {to_node}.{target_field} ({relation_type})"
            )

    # 保存到缓存
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = CACHE_DIR / f"model_info_{args.model_id}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(model, f, ensure_ascii=False, indent=2)

    print(f"\n✓ 已保存到：{output_file}")


def main():
    parser = argparse.ArgumentParser(description="获取模型数据")
    subparsers = parser.add_subparsers(dest="command", help="命令类型")

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有模型")
    list_parser.add_argument("--search", help="搜索模型（模糊匹配）")
    list_parser.add_argument("--exact", action="store_true", help="精确匹配名称")
    list_parser.set_defaults(func=cmd_list)

    # detail 命令
    detail_parser = subparsers.add_parser("detail", help="获取模型详情")
    detail_parser.add_argument("--model-id", type=int, required=True, help="模型 ID")
    detail_parser.add_argument("--output", help="输出文件路径")
    detail_parser.set_defaults(func=cmd_detail)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
