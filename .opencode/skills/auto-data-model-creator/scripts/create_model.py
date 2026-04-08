#!/usr/bin/env python3
"""
自动创建/更新数据模型的 Python 脚本

使用方法:
    python3 scripts/create_model.py create --name "模型名称" --nodes "节点 1:字段 1，字段 2;节点 2:字段 1，字段 2" --relation "节点 1.字段：节点 2.字段"

示例:
    python3 scripts/create_model.py create \
      --name "项目收款模型" \
      --nodes "project3X:name,code,version;collectionReg3X:project,amount,date" \
      --relation "project3X.code:collectionReg3X.project"
"""

import json
import argparse
import requests
import os
from typing import Dict, List, Optional
from pathlib import Path

# 脚本目录
SCRIPT_DIR = Path(__file__).parent
HEADER_FILE = SCRIPT_DIR / "header.json"
CACHE_DIR = SCRIPT_DIR / ".cache"


def load_headers() -> dict:
    """从 header.json 加载认证信息"""
    if not HEADER_FILE.exists():
        raise FileNotFoundError(
            f"认证文件不存在：{HEADER_FILE}\n请先创建该文件并填入认证信息"
        )

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


def load_datasets() -> dict:
    """从 API 加载所有可用节点信息"""
    headers = load_headers()
    url = "https://dev.cloud.hecom.cn/biserver//paas/bi-app/dataset/list"

    datasets = {}

    # 获取表格类型节点
    response = requests.post(
        url, headers=headers, json={"datasetType": "TABLE"}, timeout=30
    )
    if response.status_code == 200:
        data = response.json()
        # 响应可能没有 code 字段，直接取 data
        for dataset in data.get("data", []):
            datasets[dataset["datasetName"]] = dataset

    # 获取业务类型节点
    response = requests.post(
        url, headers=headers, json={"datasetType": "BIZ_TYPE"}, timeout=30
    )
    if response.status_code == 200:
        data = response.json()
        for dataset in data.get("data", []):
            datasets[dataset["datasetName"]] = dataset

    # 获取选项类型节点
    response = requests.post(
        url, headers=headers, json={"datasetType": "OPTION"}, timeout=30
    )
    if response.status_code == 200:
        data = response.json()
        for dataset in data.get("data", []):
            datasets[dataset["datasetName"]] = dataset

    return datasets


def build_field_object(
    dataset_id: int, dataset_name: str, field_name: str, field_info: dict, ent_code: str
) -> dict:
    """构建字段配置对象"""
    return {
        "customVal": False,
        "datasetId": dataset_id,
        "datasetMetaId": dataset_id,
        "datasetName": dataset_name,
        "disabled": 0,
        "entCode": ent_code,
        "fieldLabel": field_info["fieldLabel"],
        "fieldMetaId": dataset_id,
        "fieldName": field_name,
        "fieldType": field_info["fieldType"],
        "id": field_info["id"],
        "nativeType": field_info["nativeType"],
        "objId": field_info["id"],
        "status": 0,
        "vector": 0,
    }


def build_dataset_object(dataset_info: dict, ent_code: str) -> dict:
    """构建数据集对象（用于关联关系）"""
    dataset_id = dataset_info.get("datasourceId", dataset_info.get("datasetId"))
    return {
        "datasetId": dataset_id,
        "datasetLabel": dataset_info.get("datasetLabel", dataset_info["datasetName"]),
        "datasetName": dataset_info["datasetName"],
        "datasetType": dataset_info.get("datasetType", "TABLE"),
        "modelTableType": "FACTS_TABLE",
        "entCode": ent_code,
        "key": dataset_info["datasetName"],
        "name": dataset_info["datasetName"],
        "label": dataset_info.get("datasetLabel", dataset_info["datasetName"]),
    }


def build_field_ref_object(field_info: dict, field_name: str, ent_code: str) -> dict:
    """构建字段引用对象（用于关联关系）"""
    return {
        "id": field_info["id"],
        "fieldLabel": field_info["fieldLabel"],
        "fieldName": field_name,
        "nativeType": field_info["nativeType"],
        "fieldType": field_info["fieldType"],
        "entCode": ent_code,
    }


def create_model_config(
    name: str,
    nodes: Dict[str, List[str]],
    datasets: dict,
    relation: Optional[Dict],
    ent_code: str,
) -> dict:
    """
    创建数据模型配置

    Args:
        name: 模型名称
        nodes: 节点字典 {节点名：[字段列表]}
        datasets: 所有节点信息
        relation: 关联关系 {from_node, from_field, to_node, to_field}
        ent_code: 企业编码

    Returns:
        完整的模型配置 JSON 对象
    """
    model_config = {
        "modelDTO": {"name": name, "entCode": ent_code, "std": 0},
        "modelRelationDTOList": [],
        "modelDatasetDTOList": [],
    }

    # 构建节点列表
    for node_name, field_names in nodes.items():
        if node_name not in datasets:
            print(f"⚠️  警告：节点 {node_name} 不在可用节点列表中")
            continue

        dataset_info = datasets[node_name]

        # 构建字段查找字典：{fieldName: field_info}
        fields_dict = {}
        for f in dataset_info.get("fields", []):
            field_name = f.get("fieldName")
            if field_name:
                fields_dict[field_name] = f

        # 构建字段列表
        fields = []
        for field_name in field_names:
            if field_name not in fields_dict:
                print(f"⚠️  警告：字段 {field_name} 不在节点 {node_name} 中")
                continue

            field_obj = build_field_object(
                dataset_info.get("datasourceId", dataset_info.get("datasetId")),
                node_name,
                field_name,
                fields_dict[field_name],
                ent_code,
            )
            fields.append(field_obj)

        if not fields:
            print(f"⚠️  警告：节点 {node_name} 没有有效的字段")
            continue

        dataset_id = dataset_info.get("datasourceId", dataset_info.get("datasetId"))

        # 构建 displayFields - 使用字段名数组而不是对象数组
        display_fields = [f["fieldName"] for f in fields]

        # 构建节点配置
        node_config = {
            "modelTableType": "FACTS_TABLE",
            "datasetType": "TABLE",
            "datasetLabel": dataset_info.get("datasetLabel", node_name),
            "datasetName": node_name,
            "fields": fields,
            "metaId": dataset_id,
            "metaName": node_name,
            "entCode": ent_code,
            "datasetId": dataset_id,
            "name": node_name,
            "label": dataset_info.get("datasetLabel", node_name),
            "displayFields": display_fields,
            "unionDataSets": [],
        }
        model_config["modelDatasetDTOList"].append(node_config)

    # 构建关联关系
    if relation:
        from_node = relation["from_node"]
        from_field = relation["from_field"]
        to_node = relation["to_node"]
        to_field = relation["to_field"]

        if from_node in datasets and to_node in datasets:
            from_dataset = datasets[from_node]
            to_dataset = datasets[to_node]

            # 构建字段查找字典
            from_fields_dict = {
                f.get("fieldName"): f for f in from_dataset.get("fields", [])
            }
            to_fields_dict = {
                f.get("fieldName"): f for f in to_dataset.get("fields", [])
            }

            if from_field in from_fields_dict and to_field in to_fields_dict:
                relation_config = {
                    "sourceModelDataset": build_dataset_object(from_dataset, ent_code),
                    "targetModelDataset": build_dataset_object(to_dataset, ent_code),
                    "sourceField": build_field_ref_object(
                        from_fields_dict[from_field], from_field, ent_code
                    ),
                    "targetField": build_field_ref_object(
                        to_fields_dict[to_field], to_field, ent_code
                    ),
                    "relationType": "LEFT_JOIN",
                    "to": to_node,
                    "from": from_node,
                    "entCode": ent_code,
                }
                model_config["modelRelationDTOList"].append(relation_config)
            else:
                print(
                    f"⚠️  警告：关联字段不存在 - {from_node}.{from_field} 或 {to_node}.{to_field}"
                )
        else:
            print(f"⚠️  警告：关联节点不存在 - {from_node} 或 {to_node}")

    return model_config


def save_model(model_config: dict) -> dict:
    """调用 API 保存模型"""
    headers = load_headers()
    url = (
        "https://dev.cloud.hecom.cn/biserver//paas/app/dataModel/operation/saveModelAll"
    )

    response = requests.post(url, headers=headers, json=model_config, timeout=30)

    if response.status_code != 200:
        raise Exception(f"API 请求失败：{response.status_code}\n{response.text}")

    result = response.json()
    # 检查是否成功
    if "data" in result and result.get("data"):
        return result
    else:
        raise Exception(
            f"保存失败：{result.get('desc', result.get('message', '未知错误'))}"
        )


def parse_nodes(nodes_str: str) -> Dict[str, List[str]]:
    """
    解析节点字符串

    格式："节点 1:字段 1，字段 2;节点 2:字段 1，字段 2"
    """
    nodes = {}
    node_parts = nodes_str.split(";")
    for node_part in node_parts:
        if ":" in node_part:
            node_name, fields_str = node_part.split(":", 1)
            fields = [f.strip() for f in fields_str.split(",")]
            nodes[node_name.strip()] = fields
    return nodes


def parse_relation(relation_str: str) -> Optional[Dict]:
    """
    解析关联关系字符串

    格式："节点 1.字段 1：节点 2.字段 2"
    """
    if not relation_str or ":" not in relation_str:
        return None

    left, right = relation_str.split(":")
    from_part = left.strip().split(".")
    to_part = right.strip().split(".")

    if len(from_part) != 2 or len(to_part) != 2:
        return None

    return {
        "from_node": from_part[0].strip(),
        "from_field": from_part[1].strip(),
        "to_node": to_part[0].strip(),
        "to_field": to_part[1].strip(),
    }


def cmd_create(args):
    """创建模型命令"""
    print(f"🚀 开始创建模型：{args.name}")

    # 加载认证信息
    try:
        headers = load_headers()
        ent_code = args.ent_code or headers.get("entCode", "")
    except FileNotFoundError as e:
        print(f"❌ 错误：{e}")
        return

    # 加载节点信息
    print("📡 正在获取可用节点列表...")
    datasets = load_datasets()
    print(f"✓ 已加载 {len(datasets)} 个节点")

    # 解析参数
    nodes = parse_nodes(args.nodes)
    relation = parse_relation(args.relation) if args.relation else None

    print(f"📋 模型配置:")
    print(f"   名称：{args.name}")
    print(f"   节点：{len(nodes)} 个")
    for node_name, fields in nodes.items():
        print(f"      - {node_name}: {len(fields)} 个字段")
    if relation:
        print(
            f"   关联：{relation['from_node']}.{relation['from_field']} → {relation['to_node']}.{relation['to_field']}"
        )

    # 构建模型配置
    print("🔧 正在构建模型配置...")
    model_config = create_model_config(
        name=args.name,
        nodes=nodes,
        datasets=datasets,
        relation=relation,
        ent_code=ent_code,
    )

    # 保存模型
    print("💾 正在保存模型...")
    try:
        result = save_model(model_config)
        model_id = result.get("data", {}).get("modelDTO", {}).get("id", "未知")
        print(f"✅ 模型创建成功！")
        print(f"   模型 ID: {model_id}")
        print(f"   包含节点：{len(model_config['modelDatasetDTOList'])} 个")
        if model_config["modelRelationDTOList"]:
            print(f"   关联关系：{len(model_config['modelRelationDTOList'])} 个")
    except Exception as e:
        print(f"❌ 保存失败：{e}")


def main():
    parser = argparse.ArgumentParser(description="创建数据模型配置")
    subparsers = parser.add_subparsers(dest="command", help="命令类型")

    # create 命令
    create_parser = subparsers.add_parser("create", help="创建新模型")
    create_parser.add_argument("--name", required=True, help="模型名称")
    create_parser.add_argument(
        "--nodes",
        required=True,
        help="节点和字段配置，格式：'节点 1:字段 1，字段 2;节点 2:字段 1，字段 2'",
    )
    create_parser.add_argument(
        "--relation", help="关联关系，格式：'节点 1.字段 1：节点 2.字段 2'"
    )
    create_parser.add_argument("--ent-code", help="企业编码（默认从 header.json 读取）")
    create_parser.set_defaults(func=cmd_create)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
