#!/usr/bin/env python3
"""
获取模型列表和详细信息，供大模型分析使用
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

from auth import get_base_url, load_headers, post
from bi_utils import get_model_info


def get_cache_dir() -> Path:
    """获取缓存目录路径"""
    script_dir = Path(__file__).parent
    cache_dir = script_dir / ".cache"
    cache_dir.mkdir(exist_ok=True)
    return cache_dir


def get_model_list(base_url: str = "") -> List[Dict[str, Any]]:
    base_url = base_url or get_base_url()
    headers = load_headers()

    url = f"{base_url}/biserver/paas/app/dataModel/operation/list"
    payload = {"modelName": "", "pageNo": 1, "pageSize": 500}
    response = post(url, json=payload, headers=headers)
    data = response.json()

    if data.get("result") == "0":
        return data.get("data", {}).get("list", [])
    else:
        raise Exception(f"获取模型列表失败：{data.get('desc')}")


def list_models_to_json(
    output_file: Optional[Union[str, Path]] = None,
) -> List[Dict[str, Any]]:
    """保存模型列表到 JSON 文件"""
    if output_file is None:
        output_file = get_cache_dir() / "model_list.json"
    models = get_model_list()
    simple_models = [{"id": m.get("id"), "name": m.get("name")} for m in models]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(simple_models, f, ensure_ascii=False, indent=2)

    print(f"已保存 {len(simple_models)} 个模型到 {output_file}")
    return simple_models


def get_models_info(model_ids: List[int]) -> List[Dict[str, Any]]:
    """批量获取模型详细信息"""
    models_info = []
    for model_id in model_ids:
        try:
            info = get_model_info(model_id)
            models_info.append(info)
            print(f"✓ 已获取模型 {model_id} 的详细信息")
        except Exception as e:
            print(f"✗ 获取模型 {model_id} 失败：{e}")

    return models_info


def format_model_info_for_llm(
    model_info: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """格式化模型信息供 LLM 分析"""
    if not model_info:
        return None

    model_name = model_info.get("modelDTO", {}).get("name", "Unknown")
    model_id = model_info.get("modelDTO", {}).get("id")

    fields_summary = {
        "date_fields": [],
        "category_fields": [],
        "amount_fields": [],
        "other_fields": [],
    }

    for ds in model_info.get("modelDatasetDTOList", []):
        for field in ds.get("fields", []):
            field_type = field.get("fieldType", "")
            field_name = field.get("fieldName", "")
            field_label = field.get("fieldLabel", "")

            field_info = {
                "name": field_name,
                "label": field_label,
                "type": field_type,
                "dataset": ds.get("datasetName"),
            }

            if field_type == "Time":
                fields_summary["date_fields"].append(field_info)
            elif field_type == "Number" and any(
                kw in field_name.lower()
                for kw in ["amount", "money", "price", "sum", "金额"]
            ):
                fields_summary["amount_fields"].append(field_info)
            elif field_type in ["Text", "Join"]:
                fields_summary["category_fields"].append(field_info)
            else:
                fields_summary["other_fields"].append(field_info)

    return {"id": model_id, "name": model_name, "fields_summary": fields_summary}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="获取模型信息供大模型分析")
    parser.add_argument("--list", action="store_true", help="列出所有模型")
    parser.add_argument(
        "--model-ids", type=int, nargs="+", help="获取指定模型的详细信息"
    )
    parser.add_argument(
        "--output", default=None, help="输出文件路径（默认保存到 .cache/ 目录）"
    )
    parser.add_argument("--base-url", default=get_base_url(), help="API 基础 URL")
    parser.add_argument(
        "--env",
        default="dev",
        choices=["dev", "test", "prod"],
        help="环境 (默认 dev，与 --base-url 二选一)",
    )

    args = parser.parse_args()
    base_url = args.base_url if args.base_url else get_base_url(args.env)

    if args.list:
        models = list_models_to_json()
        print(f"\n前 20 个模型:")
        for m in models[:20]:
            print(f"  ID: {m['id']}, 名称：{m['name']}")

    elif args.model_ids:
        models_info = []
        for model_id in args.model_ids:
            try:
                info = get_model_info(model_id, base_url=base_url)
                formatted = format_model_info_for_llm(info)
                if formatted:
                    models_info.append(formatted)
                    print(f"✓ 已获取模型 {model_id} 的详细信息")
            except Exception as e:
                print(f"✗ 获取模型 {model_id} 失败：{e}")

        # 如果未指定输出文件，保存到 .cache 目录
        if args.output is None:
            output_file = get_cache_dir() / f"model_info_{args.model_ids[0]}.json"
        else:
            output_file = Path(args.output)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(models_info, f, ensure_ascii=False, indent=2)

        print(f"\n已保存 {len(models_info)} 个模型的详细信息到 {output_file}")

    else:
        parser.print_help()
