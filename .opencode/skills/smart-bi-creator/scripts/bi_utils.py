#!/usr/bin/env python3
"""BI 大屏工具函数 - 被多个脚本共享"""

from typing import Dict, List, Optional

from auth import get, post, load_headers, get_base_url


def get_model_info(
    model_id: int, base_url: str = "", headers: Optional[Dict] = None
) -> Dict:
    """获取模型详情

    Args:
        model_id: 模型 ID
        base_url: API 基础 URL（可选，默认从环境变量读取）
        headers: 请求头（可选，默认从 header.json 加载）

    Returns:
        模型详情 dict

    Raises:
        Exception: API 返回错误
    """
    if base_url is None or base_url == "":
        base_url = get_base_url()
    if headers is None:
        headers = load_headers()

    url = f"{base_url}/biserver/paas/app/dataModel/operation/listModelAll/{model_id}"
    response = post(url, json={"id": model_id}, headers=headers)
    data = response.json()
    if data.get("result") == "0":
        return data.get("data", {})
    raise Exception(f"获取模型信息失败：{data.get('desc')}")


def build_model_fields(model_info: Dict, ent_code: str = "") -> List[Dict]:
    """构建模型字段数组

    Args:
        model_info: 模型详情 dict
        ent_code: 企业编码（从请求头中获取）

    Returns:
        字段对象列表
    """
    all_fields = []
    datasets = model_info.get("modelDatasetDTOList", [])
    for ds in datasets:
        for field in ds.get("fields", []):
            field_obj = {
                "customVal": False,
                "datasetId": ds["datasetId"],
                "datasetMetaId": ds["datasetId"],
                "datasetName": ds["datasetName"],
                "disabled": 0,
                "entCode": ent_code,
                "fieldLabel": field.get("fieldLabel", ""),
                "fieldMetaId": field.get("fieldMetaId", field.get("id")),
                "fieldName": field.get("fieldName", ""),
                "fieldType": field.get("fieldType", ""),
                "id": field.get("id"),
                "nativeType": field.get("nativeType", ""),
                "objId": field.get("objId"),
                "status": 0,
                "vector": 0,
                "fieldId": field.get("id"),
            }
            all_fields.append(field_obj)
    return all_fields
