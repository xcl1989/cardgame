#!/usr/bin/env python3
"""
获取节点数据的脚本

使用方法:
    python3 scripts/get_nodes.py --list                    # 获取节点列表
    python3 scripts/get_nodes.py --node-ids 123 456        # 获取节点详情
    python3 scripts/get_nodes.py --search "项目"           # 搜索节点
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
        "app": "biapp",
        "clientTag": "web",
    }


def ensure_cache_dir():
    """确保缓存目录存在"""
    CACHE_DIR.mkdir(exist_ok=True)


def get_nodes_list() -> list:
    """获取所有节点列表"""
    headers = load_headers()
    url = "https://dev.cloud.hecom.cn/biserver//paas/bi-app/dataset/list"

    all_nodes = []

    # 获取表格类型节点
    for dataset_type in ["TABLE", "BIZ_TYPE", "OPTION"]:
        response = requests.post(
            url, headers=headers, json={"datasetType": dataset_type}, timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            # 响应可能没有 code 字段，直接取 data
            nodes = data.get("data", [])
            if nodes:
                all_nodes.extend(nodes)

    return all_nodes


def get_node_detail(node_id: int) -> dict:
    """获取单个节点详情"""
    nodes_list = get_nodes_list()
    for node in nodes_list:
        # 节点可能使用 datasourceId 或 datasetId
        if node.get("datasourceId") == node_id or node.get("datasetId") == node_id:
            return node
    return {}


def cmd_list(args):
    """列出所有节点"""
    print("📡 正在获取节点列表...")

    try:
        nodes = get_nodes_list()
    except FileNotFoundError as e:
        print(f"❌ 错误：{e}")
        return

    ensure_cache_dir()

    # 保存到缓存
    cache_file = CACHE_DIR / "nodes_list.json"
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(nodes, f, ensure_ascii=False, indent=2)

    print(f"✓ 已保存 {len(nodes)} 个节点到 {cache_file}")

    if args.search:
        nodes = [
            n
            for n in nodes
            if args.search.lower() in n.get("datasetName", "").lower()
            or args.search in n.get("datasetLabel", "")
        ]
        print(f"🔍 搜索结果：'{args.search}' - 找到 {len(nodes)} 个节点")

    # 显示前 20 个
    print(f"\n=== 节点列表 (共 {len(nodes)} 个) ===")
    print("ID              名称                              类型        字段数")
    print("-" * 90)

    for node in nodes[:20]:
        node_id = str(node.get("datasetId", ""))
        name = f"{node.get('datasetLabel', '')} ({node.get('datasetName', '')})"
        dtype = node.get("datasetType", "")
        field_count = len(node.get("fields", []))

        print(f"{node_id:<15} {name:<35} {dtype:<12} {field_count}")

    if len(nodes) > 20:
        print(f"... 还有 {len(nodes) - 20} 个节点")


def cmd_detail(args):
    """获取节点详情"""
    ensure_cache_dir()

    try:
        headers = load_headers()
    except FileNotFoundError as e:
        print(f"❌ 错误：{e}")
        return

    url = "https://dev.cloud.hecom.cn/biserver//paas/bi-app/dataset/list"

    for node_id in args.node_ids:
        print(f"📡 正在获取节点 {node_id} 的详细信息...")

        # 获取所有节点并查找
        all_nodes = get_nodes_list()
        node = None
        for n in all_nodes:
            # 节点可能使用 datasourceId 或 datasetId
            if n.get("datasourceId") == node_id or n.get("datasetId") == node_id:
                node = n
                break

        if not node:
            print(f"⚠️  未找到节点 {node_id}")
            continue

        # 保存到缓存
        if args.output:
            output_file = Path(args.output)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = CACHE_DIR / f"nodes_info_{node_id}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(node, f, ensure_ascii=False, indent=2)

        node_name = node.get("datasetName", "")
        node_label = node.get("datasetLabel", "")
        field_count = len(node.get("fields", []))
        print(f"✓ 已获取节点 {node_id} 的详细信息")
        print(f"   名称：{node_label} ({node_name})")
        print(f"   字段数：{field_count}")
        print(f"   已保存到：{output_file}")


def main():
    parser = argparse.ArgumentParser(description="获取节点数据")
    subparsers = parser.add_subparsers(dest="command", help="命令类型")

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有节点")
    list_parser.add_argument("--search", help="搜索节点（模糊匹配）")
    list_parser.set_defaults(func=cmd_list)

    # detail 命令
    detail_parser = subparsers.add_parser("detail", help="获取节点详情")
    detail_parser.add_argument(
        "--node-ids", type=int, nargs="+", required=True, help="节点 ID 列表"
    )
    detail_parser.add_argument("--output", help="输出文件路径")
    detail_parser.set_defaults(func=cmd_detail)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
