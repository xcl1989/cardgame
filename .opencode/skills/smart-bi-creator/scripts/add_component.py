#!/usr/bin/env python3
"""
向已有大屏添加新组件
使用方式：
1. 获取大屏现有配置
2. 创建新组件的配置（复制现有组件或新建）
3. 添加新组件到 layers、layouts、componentMap
4. 提交更新
"""

import json
import uuid
import time
import requests
import sys
from pathlib import Path
from typing import Dict, Optional, List

from auth import load_headers, get_preview_url, get_base_url, get, post
from bi_utils import (
    get_model_info as _get_model_info,
    build_model_fields as _build_model_fields,
)


class BiComponentAdder:
    """BI 大屏组件添加器"""

    def __init__(self, base_url: str = "https://dev.cloud.hecom.cn"):
        self.base_url = base_url
        self.headers = load_headers()

    def get_screen(self, screen_id: int) -> Dict:
        """获取大屏配置"""
        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/get/{screen_id}"
        response = get(url, headers=self.headers)
        data = response.json()
        if data.get("result") == "0":
            return data.get("data", {})
        raise Exception(f"获取大屏失败：{data.get('desc')}")

    def update_screen(self, screen_id: int, config: Dict) -> bool:
        """更新大屏配置"""
        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/update/{screen_id}"
        response = post(url, json=config, headers=self.headers)
        data = response.json()
        if data.get("result") == "0":
            return True
        raise Exception(f"更新大屏失败：{data.get('desc')}")

    def generate_uuid(self, chart_type: str) -> str:
        """生成组件 UUID"""
        timestamp = int(time.time() * 1000)
        return f"grid-type:{chart_type}-uuid:{timestamp}"

    def build_date_filter_config(
        self,
        date_filter: str,
        dim_field: Dict,
        dim_ds: Dict,
        dimension_field: str,
    ) -> List[Dict]:
        """构建日期筛选器配置

        Args:
            date_filter: 筛选器类型
                - 相对时间: thisYear, thisMonth, lastMonth, thisQuarter, lastQuarter
                - 自定义日期: YYYY-MM-DD,YYYY-MM-DD 格式
            dim_field: 维度字段信息
            dim_ds: 维度数据集信息
            dimension_field: 维度字段名

        Returns:
            筛选器配置列表
        """
        date_filter_map = {
            "thisYear": "今年",
            "lastYear": "去年",
            "thisMonth": "本月",
            "lastMonth": "上月",
            "thisQuarter": "本季度",
            "lastQuarter": "上季度",
        }

        # 检查是否是自定义日期范围 (YYYY-MM-DD,YYYY-MM-DD)
        if "," in date_filter:
            parts = date_filter.split(",")
            if len(parts) == 2:
                start_date, end_date = parts[0].strip(), parts[1].strip()
                try:
                    from datetime import datetime

                    start_ts = int(
                        datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000
                    )
                    end_ts = (
                        int(datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)
                        + 86399999
                    )
                    label = f"{start_date} 00:00~{end_date} 23:59"
                    return [
                        {
                            "datasetId": dim_ds["datasetId"],
                            "datasetMetaId": dim_ds["datasetId"],
                            "dateFormat": "YMD",
                            "fieldFilter": {
                                "conditions": [
                                    {
                                        "key": "1",
                                        "left": {
                                            "customPeriodType": False,
                                            "expressionType": False,
                                            "fieldType": True,
                                            "label": dim_field["fieldLabel"],
                                            "type": "field",
                                            "value": f"{dim_ds['datasetName']}.{dimension_field}",
                                        },
                                        "op": "bte",
                                        "opLabel": label,
                                        "right": {
                                            "customPeriodType": False,
                                            "expression": "",
                                            "expressionType": False,
                                            "fieldType": False,
                                            "globalVariableId": "",
                                            "label": label,
                                            "type": "constant",
                                            "value": [start_ts, end_ts],
                                        },
                                    }
                                ],
                                "conj": "and",
                                "empty": False,
                                "expr": "1",
                                "metaId": dim_ds["datasetId"],
                                "metaName": dim_ds["datasetName"],
                            },
                            "fieldId": dim_field["id"],
                            "fieldLabel": dim_field["fieldLabel"],
                            "fieldName": dimension_field,
                            "index": 0,
                            "metricType": "NONAGG",
                            "modelDatasetName": dim_ds["datasetName"],
                            "nativeType": dim_field["nativeType"],
                            "newFieldLabel": dim_field["fieldLabel"],
                        }
                    ]
                except ValueError:
                    raise ValueError(
                        f"无效的日期格式: '{date_filter}'，期望格式为 YYYY-MM-DD,YYYY-MM-DD（例如 2024-01-01,2024-12-31）"
                    )

        # 相对时间筛选器
        filter_expression = date_filter_map.get(date_filter, date_filter)
        return [
            {
                "datasetId": dim_ds["datasetId"],
                "datasetMetaId": dim_ds["datasetId"],
                "dateFormat": "YMD",
                "fieldFilter": {
                    "conditions": [
                        {
                            "key": "1",
                            "left": {
                                "customPeriodType": False,
                                "expressionType": False,
                                "fieldType": True,
                                "label": dim_field["fieldLabel"],
                                "type": "field",
                                "value": f"{dim_ds['datasetName']}.{dimension_field}",
                            },
                            "op": "bt",
                            "opLabel": filter_expression,
                            "right": {
                                "customPeriodType": False,
                                "expression": date_filter,
                                "expressionType": True,
                                "fieldType": False,
                                "label": filter_expression,
                                "type": "expression",
                                "value": 0,
                            },
                        }
                    ],
                    "conj": "and",
                    "empty": False,
                    "expr": "1",
                    "metaId": dim_ds["datasetId"],
                    "metaName": dim_ds["datasetName"],
                },
                "fieldId": dim_field["id"],
                "fieldLabel": dim_field["fieldLabel"],
                "fieldName": dimension_field,
                "index": 0,
                "metricType": "NONAGG",
                "modelDatasetName": dim_ds["datasetName"],
                "nativeType": dim_field["nativeType"],
                "newFieldLabel": dim_field["fieldLabel"],
            }
        ]

    def create_component_config(
        self,
        model_info: Optional[Dict],
        dimension_field: str,
        indicator_field: str,
        chart_type: str = "bar",
        top: int = 100,
        left: int = 100,
        width: int = 440,
        height: int = 270,
        view_name: Optional[str] = None,
        text_align: Optional[str] = None,
        font_size: Optional[int] = None,
        title_align: Optional[str] = None,
        metric_style: Optional[str] = None,
        metric_value_color: Optional[str] = None,
        metric_label_color: Optional[str] = None,
        metric_icon_color: Optional[str] = None,
        metric_label_visible: Optional[bool] = False,
        pie_outer_radius: Optional[int] = None,
        pie_inner_radius: Optional[int] = None,
        pie_label_position: Optional[str] = None,
        pie_legend_position: Optional[str] = None,
        bar_legend_position: Optional[str] = None,
        bar_scroll_enabled: Optional[bool] = None,
        bar_scroll_speed: Optional[int] = None,
        bar_label_show: Optional[bool] = None,
        bar_label_position: Optional[str] = None,
        bar_axis_rotate: Optional[int] = None,
        script_code: Optional[str] = None,
        order_type: Optional[str] = None,
        indicator_order_type: Optional[str] = None,
        decorate_index: Optional[int] = None,
        line_type: Optional[str] = None,
        extra_dimension_fields: Optional[List[str]] = None,
        extra_indicator_fields: Optional[List[str]] = None,
        flipper_int_figure: Optional[int] = None,
        flipper_decimal_figure: Optional[int] = None,
        flipper_thousandth: Optional[bool] = None,
        flipper_style_type: Optional[str] = None,
        flipper_font_color: Optional[str] = None,
        flipper_fill_color: Optional[str] = None,
        flipper_border_color: Optional[str] = None,
        flipper_flip_gap: Optional[int] = None,
        radar_radius: Optional[int] = None,
        radar_legend_position: Optional[str] = None,
        radar_label_position: Optional[str] = None,
        radar_mode: Optional[str] = None,
        date_filter: Optional[str] = None,
        linkage: Optional[List[str]] = None,
        indicator_label: Optional[str] = None,
    ) -> Dict:
        """创建新组件的完整配置"""

        # 非数据组件特殊处理 - 不需要模型信息
        no_data_types = ["time", "text", "decorate", "head", "card", "icon"]
        if chart_type in no_data_types:
            component_uuid = self.generate_uuid(chart_type)

            layer = {
                "uuid": component_uuid,
                "top": top,
                "left": left,
                "width": width,
                "height": height,
                "zIndex": 1,
                "visible": True,
                "disabled": False,
                "isContainer": False,
            }

            title_map = {
                "time": view_name or "时间",
                "text": view_name or "文本",
                "decorate": view_name or "装饰",
                "head": view_name or "头部",
                "card": view_name or "卡片",
                "icon": view_name or "图标",
            }
            group_label_map = {
                "time": "高级组件",
                "text": "高级组件",
                "decorate": "装饰组件",
                "head": "装饰组件",
                "card": "容器组件",
                "icon": "装饰组件",
            }

            layout = {
                "uuid": component_uuid,
                "title": title_map.get(chart_type, view_name or chart_type),
                "type": chart_type,
                "icon": self.get_chart_icon(chart_type),
                "groupLabel": group_label_map.get(chart_type, "图形组件"),
                "gridData": {},
                "resizeHandles": ["s", "e", "se"],
            }

            if chart_type == "time":
                component = self._build_time_style(
                    view_name=view_name,
                    top=top,
                    left=left,
                    width=width,
                    height=height,
                    text_align=text_align,
                    font_size=font_size,
                )
            else:
                style_content = self.get_chart_style_json(
                    chart_type,
                    left,
                    top,
                    width,
                    height,
                    view_name,
                    text_align,
                    font_size,
                    title_align,
                    metric_style,
                    metric_value_color,
                    metric_label_color,
                    metric_icon_color,
                    metric_label_visible,
                    pie_outer_radius,
                    pie_inner_radius,
                    pie_label_position,
                    pie_legend_position,
                    bar_legend_position,
                    bar_scroll_enabled,
                    bar_scroll_speed,
                    bar_label_show,
                    bar_label_position,
                    bar_axis_rotate,
                    script_code,
                    decorate_index,
                    line_type,
                )
                component_name = title_map.get(chart_type, view_name or chart_type)
                component = {
                    "viewName": component_name,
                    "styleJson": style_content,
                }

            return {
                "uuid": component_uuid,
                "layer": layer,
                "layout": layout,
                "component": component,
            }

        model_fields = (
            _build_model_fields(model_info, self.headers.get("entCode", ""))
            if model_info
            else []
        )
        assert model_info is not None
        model_id = model_info.get("modelDTO", {}).get("id")

        # 查找字段信息
        dim_field_info = None
        ind_field_info = None
        extra_dim_fields_info = []
        extra_ind_fields_info = []

        all_dimension_fields = [dimension_field] + (extra_dimension_fields or [])
        all_indicator_fields = [indicator_field] + (extra_indicator_fields or [])

        for ds in model_info.get("modelDatasetDTOList", []):
            for field in ds.get("fields", []):
                field_name = field.get("fieldName", "")
                if field_name == dimension_field:
                    dim_field_info = {"field": field, "dataset": ds}
                if field_name == indicator_field:
                    ind_field_info = {"field": field, "dataset": ds}
                if field_name in all_dimension_fields and field_name != dimension_field:
                    extra_dim_fields_info.append({"field": field, "dataset": ds})
                if field_name in all_indicator_fields and field_name != indicator_field:
                    extra_ind_fields_info.append({"field": field, "dataset": ds})

        if not dim_field_info or not ind_field_info:
            raise Exception(f"未找到字段：{dimension_field} 或 {indicator_field}")

        dim_ds = dim_field_info["dataset"]
        dim_field = dim_field_info["field"]
        ind_ds = ind_field_info["dataset"]
        ind_field = ind_field_info["field"]

        # table 类型在 UUID 中使用 customTable
        if chart_type == "table":
            component_uuid = f"grid-type:customTable-uuid:{int(time.time() * 1000)}"
        else:
            component_uuid = self.generate_uuid(chart_type)

        # 指标卡和翻牌器不需要分组，只显示总计
        is_metric = chart_type == "metric"
        # card组件是纯容器组件，不需要dimensions和indicators
        is_card = chart_type == "card"
        # 表格组件支持多维度多指标
        is_table = chart_type in ("table", "customTable")
        # 翻牌器只需要指标，不需要维度
        is_flipper = chart_type == "flipper"

        # 构建所有 displayFields
        if is_metric or is_flipper:
            display_fields = [f["fieldName"] for f in model_fields]
        else:
            display_fields = all_dimension_fields + all_indicator_fields

        # 构建 dimension
        dimension = {
            "customVal": False,
            "datasetId": dim_ds["datasetId"],
            "datasetMetaId": dim_ds["datasetId"],
            "datasetName": dim_ds["datasetName"],
            "disabled": 0,
            "entCode": self.headers.get("entCode", ""),
            "fieldLabel": dim_field["fieldLabel"],
            "fieldMetaId": dim_field.get("fieldMetaId", dim_field["id"]),
            "fieldName": dim_field["fieldName"],
            "fieldType": dim_field["fieldType"],
            "id": dim_field["id"],
            "nativeType": dim_field["nativeType"],
            "objId": dim_field["objId"],
            "status": 0,
            "vector": 0,
            "fieldId": dim_field["id"],
            "datasetLabel": dim_ds["datasetLabel"],
            "datasetType": dim_ds["datasetType"],
            "displayFields": display_fields,
            "dummy": False,
            "fields": model_fields,
            "label": dim_ds["datasetLabel"],
            "modelTableType": dim_ds["modelTableType"],
            "name": dim_ds["datasetName"],
            "origLabel": dim_ds["datasetLabel"],
            "styleJson": "{}",
            "unionDataSets": [],
            "uuid": f"{dim_ds['datasetName']}-{dimension_field}-{uuid.uuid4().hex}",
            "modelDatasetLabel": dim_ds["datasetLabel"],
            "modelDatasetName": dim_ds["datasetName"],
            "newFieldLabel": dim_field["fieldLabel"],
            "groupBy": not is_metric,  # 指标卡不分组
            "orderType": None if order_type == "none" else (order_type or "asc"),
            "sortDimension": False,
            "index": 0,
            "nodeInfo": {
                "datasetId": dim_ds["datasetId"],
                "datasetLabel": dim_ds["datasetLabel"],
                "datasetName": dim_ds["datasetName"],
                "datasetType": dim_ds["datasetType"],
                "displayFields": display_fields,
                "dummy": False,
                "entCode": self.headers.get("entCode", ""),
                "fields": model_fields,
                "label": dim_ds["datasetLabel"],
                "modelTableType": dim_ds["modelTableType"],
                "name": dim_ds["datasetName"],
                "origLabel": dim_ds["datasetLabel"],
                "styleJson": "{}",
                "unionDataSets": [],
                "groupBy": not is_metric,  # 指标卡不分组
                "orderType": None if order_type == "none" else (order_type or "asc"),
            },
        }

        # 表格组件：构建额外的维度
        dimensions_list = [dimension]
        for idx, extra_dim in enumerate(extra_dim_fields_info):
            extra_ds = extra_dim["dataset"]
            extra_f = extra_dim["field"]
            extra_dimension = {
                "customVal": False,
                "datasetId": extra_ds["datasetId"],
                "datasetMetaId": extra_ds["datasetId"],
                "datasetName": extra_ds["datasetName"],
                "disabled": 0,
                "entCode": self.headers.get("entCode", ""),
                "fieldLabel": extra_f["fieldLabel"],
                "fieldMetaId": extra_f.get("fieldMetaId", extra_f["id"]),
                "fieldName": extra_f["fieldName"],
                "fieldType": extra_f["fieldType"],
                "id": extra_f["id"],
                "nativeType": extra_f["nativeType"],
                "objId": extra_f["objId"],
                "status": 0,
                "vector": 0,
                "fieldId": extra_f["id"],
                "datasetLabel": extra_ds["datasetLabel"],
                "datasetType": extra_ds["datasetType"],
                "displayFields": display_fields,
                "dummy": False,
                "fields": model_fields,
                "label": extra_ds["datasetLabel"],
                "modelTableType": extra_ds["modelTableType"],
                "name": extra_ds["datasetName"],
                "origLabel": extra_ds["datasetLabel"],
                "styleJson": "{}",
                "unionDataSets": [],
                "uuid": f"{extra_ds['datasetName']}-{extra_f['fieldName']}-{uuid.uuid4().hex}",
                "modelDatasetLabel": extra_ds["datasetLabel"],
                "modelDatasetName": extra_ds["datasetName"],
                "newFieldLabel": extra_f["fieldLabel"],
                "groupBy": True,
                "orderType": None if order_type == "none" else (order_type or "asc"),
                "sortDimension": False,
                "index": idx + 1,
                "nodeInfo": {
                    "datasetId": extra_ds["datasetId"],
                    "datasetLabel": extra_ds["datasetLabel"],
                    "datasetName": extra_ds["datasetName"],
                    "datasetType": extra_ds["datasetType"],
                    "displayFields": display_fields,
                    "dummy": False,
                    "entCode": self.headers.get("entCode", ""),
                    "fields": model_fields,
                    "label": extra_ds["datasetLabel"],
                    "modelTableType": extra_ds["modelTableType"],
                    "name": extra_ds["datasetName"],
                    "origLabel": extra_ds["datasetLabel"],
                    "styleJson": "{}",
                    "unionDataSets": [],
                    "groupBy": True,
                    "orderType": None
                    if order_type == "none"
                    else (order_type or "asc"),
                },
            }
            dimensions_list.append(extra_dimension)

        # 构建 indicator
        # 指标卡的 displayFields 应该包含所有字段（用于数据获取），但不会用于分组
        # 非指标卡的 displayFields 包含 dimension 和 indicator
        if is_metric:
            indicator_display_fields = [
                f["fieldName"] for f in model_fields
            ]  # 所有字段
        else:
            indicator_display_fields = display_fields

        indicator = {
            "customVal": False,
            "datasetId": ind_ds["datasetId"],
            "datasetMetaId": ind_ds["datasetId"],
            "datasetName": ind_ds["datasetName"],
            "disabled": 0,
            "entCode": self.headers.get("entCode", ""),
            "fieldLabel": ind_field["fieldLabel"],
            "fieldMetaId": ind_field.get("fieldMetaId", ind_field["id"]),
            "fieldName": ind_field["fieldName"],
            "fieldType": ind_field["fieldType"],
            "id": ind_field["id"],
            "nativeType": ind_field["nativeType"],
            "objId": ind_field["objId"],
            "status": 0,
            "vector": 0,
            "fieldId": ind_field["id"],
            "datasetLabel": ind_ds["datasetLabel"],
            "datasetType": ind_ds["datasetType"],
            "displayFields": indicator_display_fields,
            "dummy": False,
            "fields": model_fields,
            "label": ind_ds["datasetLabel"],
            "modelTableType": ind_ds["modelTableType"],
            "name": ind_ds["datasetName"],
            "origLabel": ind_ds["datasetLabel"],
            "styleJson": "{}",
            "unionDataSets": [],
            "uuid": f"{ind_ds['datasetName']}-{indicator_field}-{uuid.uuid4().hex}",
            "modelDatasetLabel": ind_ds["datasetLabel"],
            "modelDatasetName": ind_ds["datasetName"],
            "newFieldLabel": indicator_label
            if indicator_label
            else ind_field["fieldLabel"],
            "nodeInfo": {
                "datasetId": ind_ds["datasetId"],
                "datasetLabel": ind_ds["datasetLabel"],
                "datasetName": ind_ds["datasetName"],
                "datasetType": ind_ds["datasetType"],
                "displayFields": indicator_display_fields,
                "dummy": False,
                "entCode": self.headers.get("entCode", ""),
                "fields": model_fields,
                "label": ind_ds["datasetLabel"],
                "modelTableType": ind_ds["modelTableType"],
                "name": ind_ds["datasetName"],
                "origLabel": ind_ds["datasetLabel"],
                "styleJson": "{}",
                "unionDataSets": [],
            },
            "metricType": "SUM",
            "valueFormat": {
                "isPercentage": 0,
                "decimalPlaces": 2,
                "useThousandsSeparator": 0,
            },
            "orderType": None
            if indicator_order_type == "none"
            else (indicator_order_type if indicator_order_type else "desc"),
            "index": 0,
        }

        # 表格组件：构建额外的指标
        indicators_list = [indicator]
        for idx, extra_ind in enumerate(extra_ind_fields_info):
            extra_ds = extra_ind["dataset"]
            extra_f = extra_ind["field"]
            extra_indicator = {
                "customVal": False,
                "datasetId": extra_ds["datasetId"],
                "datasetMetaId": extra_ds["datasetId"],
                "datasetName": extra_ds["datasetName"],
                "disabled": 0,
                "entCode": self.headers.get("entCode", ""),
                "fieldLabel": extra_f["fieldLabel"],
                "fieldMetaId": extra_f.get("fieldMetaId", extra_f["id"]),
                "fieldName": extra_f["fieldName"],
                "fieldType": extra_f["fieldType"],
                "id": extra_f["id"],
                "nativeType": extra_f["nativeType"],
                "objId": extra_f["objId"],
                "status": 0,
                "vector": 0,
                "fieldId": extra_f["id"],
                "datasetLabel": extra_ds["datasetLabel"],
                "datasetType": extra_ds["datasetType"],
                "displayFields": indicator_display_fields,
                "dummy": False,
                "fields": model_fields,
                "label": extra_ds["datasetLabel"],
                "modelTableType": extra_ds["modelTableType"],
                "name": extra_ds["datasetName"],
                "origLabel": extra_ds["datasetLabel"],
                "styleJson": "{}",
                "unionDataSets": [],
                "uuid": f"{extra_ds['datasetName']}-{extra_f['fieldName']}-{uuid.uuid4().hex}",
                "modelDatasetLabel": extra_ds["datasetLabel"],
                "modelDatasetName": extra_ds["datasetName"],
                "newFieldLabel": extra_f["fieldLabel"],
                "nodeInfo": {
                    "datasetId": extra_ds["datasetId"],
                    "datasetLabel": extra_ds["datasetLabel"],
                    "datasetName": extra_ds["datasetName"],
                    "datasetType": extra_ds["datasetType"],
                    "displayFields": indicator_display_fields,
                    "dummy": False,
                    "entCode": self.headers.get("entCode", ""),
                    "fields": model_fields,
                    "label": extra_ds["datasetLabel"],
                    "modelTableType": extra_ds["modelTableType"],
                    "name": extra_ds["datasetName"],
                    "origLabel": extra_ds["datasetLabel"],
                    "styleJson": "{}",
                    "unionDataSets": [],
                },
                "metricType": "SUM",
                "valueFormat": {
                    "isPercentage": 0,
                    "decimalPlaces": 2,
                    "useThousandsSeparator": 0,
                },
                "orderType": None
                if indicator_order_type == "none"
                else (indicator_order_type if indicator_order_type else "desc"),
                "index": idx + 1,
            }
            indicators_list.append(extra_indicator)

        # 构建组件
        # 指标卡的 displayFields 应该包含所有字段
        model_info_display_fields = (
            [f["fieldName"] for f in model_fields]
            if is_metric
            else [dimension_field, indicator_field]
        )

        # 获取图表特定的样式配置
        style_json = self.get_chart_style_json(
            chart_type,
            left,
            top,
            width,
            height,
            view_name,
            text_align,
            font_size,
            title_align,
            metric_style,
            metric_value_color,
            metric_label_color,
            metric_icon_color,
            metric_label_visible,
            pie_outer_radius,
            pie_inner_radius,
            pie_label_position,
            pie_legend_position,
            bar_legend_position,
            bar_scroll_enabled,
            bar_scroll_speed,
            bar_label_show,
            bar_label_position,
            bar_axis_rotate,
            script_code,
            decorate_index,
            line_type,
            flipper_int_figure,
            flipper_decimal_figure,
            flipper_thousandth,
            flipper_style_type,
            flipper_font_color,
            flipper_fill_color,
            flipper_border_color,
            flipper_flip_gap,
            radar_radius,
            radar_legend_position,
            radar_label_position,
            radar_mode,
        )

        # card组件使用特殊结构（纯容器）
        if is_card:
            component = {
                "styleJson": style_json,
                "templateId": component_uuid,
                "viewName": view_name or "卡片1",
            }
        else:
            component = {
                "modelId": model_id,
                "modelInfo": [
                    {
                        "datasetId": dim_ds["datasetId"],
                        "datasetLabel": dim_ds["datasetLabel"],
                        "datasetName": dim_ds["datasetName"],
                        "datasetType": dim_ds["datasetType"],
                        "displayFields": model_info_display_fields,
                        "dummy": False,
                        "entCode": self.headers.get("entCode", ""),
                        "fields": model_fields,
                        "label": dim_ds["datasetLabel"],
                        "modelTableType": dim_ds["modelTableType"],
                        "name": dim_ds["datasetName"],
                        "origLabel": dim_ds["datasetLabel"],
                        "styleJson": "{}",
                        "unionDataSets": [],
                    }
                ],
                "key": component_uuid,
                "viewName": view_name or f"{dim_field['fieldLabel']}分析",
                "parentUuid": "",
                "tabName": "",
                "styleJson": style_json,
                # 指标卡和翻牌器不需要 dimensions 数组
                # 表格组件使用多维度多指标
                "dimensions": []
                if is_metric or is_card or is_flipper
                else (dimensions_list if is_table else [dimension]),
                "indicators": []
                if is_card
                else (indicators_list if is_table else [indicator]),
                "limit": {"isSelect": True, "errText": "", "value": 10},
            }

            # 添加日期过滤器
            if date_filter and dim_field_info:
                component["filter"] = self.build_date_filter_config(
                    date_filter, dim_field, dim_ds, dimension_field
                )

            # 添加组件联动配置
            if linkage:
                component["interaction"] = {"linkage": {"sameModels": linkage}}

        # 构建 layer
        layer = {
            "uuid": component_uuid,
            "top": top,
            "left": left,
            "width": width,
            "height": height,
        }

        # 构建 layout
        # script 和 table 组件属于"高级组件"组
        high_end_types = ["script", "table", "customTable"]
        group_label = "高级组件" if chart_type in high_end_types else "图形组件"
        # table 类型在布局中使用 customTable
        layout_type = "customTable" if chart_type == "table" else chart_type
        layout = {
            "uuid": component_uuid,
            "title": view_name or f"{chart_type}图",
            "type": layout_type,
            "icon": self.get_chart_icon(chart_type),
            "groupLabel": group_label,
            "gridData": {},
            "resizeHandles": ["s", "e", "se"],
        }

        return {
            "uuid": component_uuid,
            "layer": layer,
            "layout": layout,
            "component": component,
        }

    def get_chart_icon(self, chart_type: str) -> str:
        """获取图表类型的图标文件名"""
        icon_map = {
            "bar": "chart_vertical_bar.png",
            "bar3d": "chart_vertical_bar.png",
            "line": "chart_line.png",
            "pie": "chart_pie.png",
            "metric": "indicator.png",
            "table": "chart_table_component.png",
            "customTable": "chart_table_component.png",
            "ranking": "chart_ranking.png",
            "dualAxis": "chart_dual_axis.png",
            "funnel": "chart_funnel.png",
            "gauge": "chart_gauge.png",
            "horizontalBar": "chart_horizontal_bar.png",
            "script": "chart_script_component.png",
            "text": "chart_text_component.png",
            "decorate": "chart_decorate_component.png",
            "time": "chart_time_component.png",
            "marquee": "chart_marquee_component.png",
            "card": "chart_card_component.png",
            "carousel": "chart_carousel_component.png",
            "icon": "chart_icon_component.png",
            "head": "chart_head_component.png",
            "map": "chart_map.png",
            "flipper": "chart_flipper_component.png",
            "radar": "chart_radar.png",
        }
        return icon_map.get(chart_type, f"chart_{chart_type}.png")

    def get_decorate_file(self, decorate_subtype: str, index: int = 1) -> str:
        """获取装饰组件的图片文件路径"""
        # 装饰组件类型映射
        type_map = {
            "square": "squareDecorate",  # 方形装饰（适合指标卡下方）
            "bar": "barDecorate",  # 条形装饰（适合图表标题栏）
            "base": "baseDecorate",  # 基础装饰（独立装饰元素）
            "head": "headDecorate",  # 头部装饰（大屏顶部通栏）
        }

        type_folder = type_map.get(decorate_subtype, "baseDecorate")
        return f"{type_folder}/{type_folder}{index}.png"

    def _build_time_style(
        self,
        view_name: Optional[str] = None,
        top: int = 0,
        left: int = 0,
        width: int = 450,
        height: int = 50,
        text_align: Optional[str] = None,
        font_size: Optional[int] = None,
    ) -> Dict:
        """构建时间组件的样式配置"""
        size = font_size or 20
        align = text_align or "left"
        return {
            "viewName": view_name or "时间",
            "styleJson": {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "title": {
                    "isExtra": True,
                    "textSetMap": {
                        "fontSize": size,
                        "textColor": "#FFFFFF",
                        "textBold": True,
                        "textItalic": False,
                    },
                },
                "cardSet": {
                    "textSetMap": {
                        "fontSize": size,
                        "textColor": "#FFFFFF",
                        "textBold": True,
                        "textItalic": False,
                    },
                    "text": "LCDFont",
                },
                "timeType": {
                    "type": "dateAndTime",
                    "date": "yyyy-MM-dd",
                    "time": "hh:mm:ss",
                },
            },
        }

    def get_chart_style_json(
        self,
        chart_type: str,
        left: int,
        top: int,
        width: int,
        height: int,
        view_name: Optional[str] = None,
        text_align: Optional[str] = None,
        font_size: Optional[int] = None,
        title_align: Optional[str] = None,
        metric_style: Optional[str] = None,
        metric_value_color: Optional[str] = None,
        metric_label_color: Optional[str] = None,
        metric_icon_color: Optional[str] = None,
        metric_label_visible: Optional[bool] = False,
        pie_outer_radius: Optional[int] = None,
        pie_inner_radius: Optional[int] = None,
        pie_label_position: Optional[str] = None,
        pie_legend_position: Optional[str] = None,
        bar_legend_position: Optional[str] = None,
        bar_scroll_enabled: Optional[bool] = None,
        bar_scroll_speed: Optional[int] = None,
        bar_label_show: Optional[bool] = None,
        bar_label_position: Optional[str] = None,
        bar_axis_rotate: Optional[int] = None,
        script_code: Optional[str] = None,
        decorate_index: Optional[int] = None,
        line_type: Optional[str] = None,
        flipper_int_figure: Optional[int] = None,
        flipper_decimal_figure: Optional[int] = None,
        flipper_thousandth: Optional[bool] = None,
        flipper_style_type: Optional[str] = None,
        flipper_font_color: Optional[str] = None,
        flipper_fill_color: Optional[str] = None,
        flipper_border_color: Optional[str] = None,
        flipper_flip_gap: Optional[int] = None,
        radar_radius: Optional[int] = None,
        radar_legend_position: Optional[str] = None,
        radar_label_position: Optional[str] = None,
        radar_mode: Optional[str] = None,
    ) -> Dict:
        """获取图表特定的样式配置

        Args:
            metric_style: 指标卡样式预设，可选值：
                - "default": 默认样式（深色背景，白色标题，浅色数值）
                - "gradient": 渐变样式（渐变背景，醒目数值）
                - "light": 浅色样式（浅色背景，深色文字）
                - "minimal": 极简样式（无边框，透明背景）
                - "card": 卡片样式（圆角边框，阴影效果）
            metric_value_color: 数值颜色（如 "#FF6B6B"）
            metric_label_color: 标签颜色（如 "#4ECDC4"）
            metric_icon_color: 图标颜色（如 "#5B8FFA"）
            pie_outer_radius: 饼图外半径（默认 80）
            pie_inner_radius: 饼图内半径（默认 60，设为 0 则为实心饼图）
            pie_label_position: 饼图标签位置（outside/inside/center，默认 outside）
            pie_legend_position: 饼图图例位置（bottom/top/left/right，默认 bottom）
            bar_legend_position: 柱图图例位置（bottom/top/left/right，默认 top）
            bar_scroll_enabled: 柱图是否启用滚动（默认 True）
            bar_scroll_speed: 柱图滚动速度（默认 5）
            bar_label_show: 柱图是否显示数据标签（默认 False）
            bar_label_position: 柱图数据标签位置（top/right/bottom/auto）
            bar_axis_rotate: 柱图X轴标签旋转角度（默认 0）
            script_code: 脚本组件的 JavaScript 代码
            line_type: 线图线条类型（line:折线，curve:曲线，默认 curve）
        """
        base_style = {
            "screenPosition": {
                "position": {"x": left, "y": top, "w": width, "h": height}
            },
            "card": {
                "lineWidthMap": {"width": 1, "style": "solid"},
                "padding": 12,
                "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                "border": "rgba(30, 39, 55, 0.8)",
            },
            "title": {
                "isExtra": True,
                "textSetMap": {
                    "fontSize": 20,
                    "textColor": "#FEFEFE",
                    "textBold": True,
                    "textItalic": False,
                },
            },
            "tooltip": {
                "backgroundColor": "#303467",
                "textSetMap": {"textColor": "#A6ADD0"},
            },
        }

        # 排名图特定样式
        if chart_type == "ranking":
            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "legend": {"textSetMap": {"textColor": "#177DDC"}},
                "name": {
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 14,
                        "textColor": "#fff",
                    }
                },
                "scroll": {
                    "isExtra": True,
                    "range": "all",
                    "type": "smooth",
                    "speed": 3,
                },
                "tooltip": {
                    "backgroundColor": "#303467",
                    "textSetMap": {"textColor": "#A6ADD0"},
                },
                "rank": {
                    "icon": '{"val":"img2","label":["rank_2_1.webp","rank_2_2.webp","rank_2_3.webp"]}',
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 18,
                        "textColor": "#fff",
                    },
                },
                "draw": {
                    "colorSettingMap": {
                        "color": "linear-gradient(90deg, rgb(52,113,232) 0%, rgb(31,64,128) 100%)",
                        "colorType": "singleColor",
                    }
                },
                "title": {
                    "isExtra": True,
                    "show": False,
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 16,
                        "textColor": "#FEFEFE",
                    },
                },
                "value": {
                    "isExtra": True,
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 18,
                        "textColor": "#fff",
                    },
                },
                "card": {
                    "border": "rgba(30, 39, 55, 0.8)",
                    "padding": 12,
                    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                    "lineWidthMap": {"width": 1, "style": "solid"},
                },
            }

        # 条形图特定样式（水平条形图）
        if chart_type == "horizontalBar":
            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "textData": {"show": False},
                "legend": {
                    "isExtra": True,
                    "textSetMap": {
                        "size": 14,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 14,
                        "textColor": "rgb(164,173,211)",
                    },
                    "position": "bottom",
                },
                "tooltip": {
                    "backgroundColor": "#303467",
                    "isExtra": True,
                    "textSetMap": {
                        "size": 14,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 14,
                        "textColor": "#A6ADD0",
                    },
                    "content": ["dimension", "measure"],
                },
                "scroll": {"cycleSpeed": 5, "show": True, "type": "highlight"},
                "drawSettings": {"seriesType": "bar", "widthMap": {"isAdaption": True}},
                "label": {
                    "isExtra": True,
                    "show": False,
                    "textSetMap": {
                        "size": 14,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 14,
                        "textColor": "#A6ADD0",
                    },
                    "position": "right",
                },
                "title": {
                    "isExtra": True,
                    "show": False,
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 16,
                        "textColor": "#FEFEFE",
                    },
                },
                "axis": {
                    "x": {"rotate": 0, "axes": ["showXAxis"], "scale": "auto"},
                    "y": {
                        "axes": ["showYAxis", "showAxisLine"],
                        "splitMap": {"isChecked": True},
                        "titleMap": {"isChecked": True, "value": ""},
                    },
                },
                "card": {
                    "border": "rgba(30, 39, 55, 0.8)",
                    "padding": 12,
                    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                    "lineWidthMap": {"width": 1, "style": "solid"},
                },
            }

        # 文本组件特定样式
        if chart_type == "text":
            align = text_align or "center"
            size = font_size or 36
            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "textData": {"content": []},
                "title": {
                    "isExtra": True,
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": size,
                        "align": align,
                        "textColor": "#FEFEFE",
                    },
                    "title": view_name or "文本标题",
                },
                "card": {
                    "border": "transparent",
                    "padding": 4,
                    "lineWidthMap": {"width": 1, "style": "solid"},
                    "isExtra": True,
                    "show": False,
                },
                "content": {
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": size,
                        "align": align,
                        "textColor": "#FEFEFE",
                    },
                    "textContent": view_name or "文本文本",
                },
            }

        # 装饰组件特定样式
        if chart_type == "decorate":
            decorate_subtype = (
                view_name.split(":")[0] if view_name and ":" in view_name else "square"
            )
            dec_idx = decorate_index if decorate_index is not None else 1

            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "decorate": {},
                "decorateStyle": {
                    "selectedDecorate": self.get_decorate_file(
                        decorate_subtype, dec_idx
                    )
                },
            }

        # 头部组件特定样式
        if chart_type == "head":
            dec_idx = decorate_index if decorate_index is not None else 4
            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "decorate": {},
                "decorateStyle": {
                    "selectedDecorate": self.get_decorate_file("head", dec_idx)
                },
            }

        # card组件特定样式（纯容器组件）
        if chart_type == "card":
            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "decorate": {},
                "decorateStyle": {"selectedDecorate": "cardDecorate/cardDecorate3.png"},
            }

        # 图标组件特定样式（装饰组件的一种）
        if chart_type == "icon":
            icon_idx = decorate_index if decorate_index is not None else 1
            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "decorate": {},
                "decorateStyle": {
                    "rotate": {
                        "angle": 0,
                        "verMirrored": False,
                        "levelMirrored": False,
                    },
                    "selectedDecorate": f"iconDecorate/iconDecorate{icon_idx}.png",
                },
            }

        # 地图组件特定样式
        if chart_type == "map":
            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "legend": {"textSetMap": {"textColor": "#177DDC"}},
                "tooltip": {
                    "backgroundColor": "#303467",
                    "isExtra": True,
                    "textSetMap": {
                        "size": 12,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 12,
                        "textColor": "#A6ADD0",
                    },
                    "content": ["dimension", "measure"],
                },
                "drawSettings": {
                    "colorSettingMap": {
                        "color": "linear-gradient(90deg, rgb(188,219,249) 0%, rgb(33,114,244) 100%)",
                        "colorType": "singleColor",
                    },
                    "areaColors": [
                        "#E17372",
                        "#FF8242",
                        "#F6B747",
                        "#7EC580",
                        "#EDF77C",
                        "#59CBBF",
                        "#7A8ACE",
                    ],
                },
                "label": {
                    "isExtra": True,
                    "textSetMap": {
                        "size": 10,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 10,
                        "textColor": "#A6ADD0",
                    },
                    "contentType": "content",
                    "content": [],
                },
                "title": {
                    "isExtra": True,
                    "show": False,
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 16,
                        "textColor": "#FEFEFE",
                    },
                },
                "card": {
                    "border": "rgba(30, 39, 55, 0.8)",
                    "padding": 12,
                    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                    "lineWidthMap": {"width": 1, "style": "solid"},
                },
            }

        # 脚本组件特定样式
        if chart_type == "script":
            default_script = """// Data 格式: [[维度值, 指标1值, 指标2值, ...], ...]
const xAxisData = Data.map(item => item[0]);
const seriesData = Data.map(item => item[1]);

option = {
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: xAxisData, axisLabel: { color: '#fff' } },
    yAxis: { type: 'value', axisLabel: { color: '#fff' } },
    series: [{ type: 'bar', data: seriesData, itemStyle: { color: '#0088FE' } }]
};

myChart.setOption(option);"""

            script_content = script_code if script_code else default_script

            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "title": {
                    "isExtra": True,
                    "show": False,
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 20,
                        "textColor": "#FEFEFE",
                    },
                },
                "card": {
                    "border": "#1e273700",
                    "padding": 12,
                    "cardBackgroundColor": "#0d182c00",
                    "lineWidthMap": {"width": 1, "style": "solid"},
                },
                "script": {"script": script_content},
            }

        # 翻牌器组件样式
        if chart_type == "flipper":
            flipper_font_size = font_size if font_size else 34
            flipper_int_figure = (
                flipper_int_figure if flipper_int_figure is not None else 8
            )
            flipper_decimal_figure = (
                flipper_decimal_figure if flipper_decimal_figure is not None else 2
            )
            flipper_thousandth = (
                flipper_thousandth if flipper_thousandth is not None else True
            )
            flipper_style_type = (
                flipper_style_type if flipper_style_type is not None else "round"
            )
            flipper_font_color = (
                flipper_font_color
                if flipper_font_color is not None
                else "linear-gradient(rgb(255, 255, 255) 0%, rgb(17, 93, 151) 100%)"
            )
            flipper_fill_color = (
                flipper_fill_color
                if flipper_fill_color is not None
                else "linear-gradient(180deg, rgba(2,53,107,0.5) 0%, rgba(5,101,164,0.5) 100%)"
            )
            flipper_border_color = (
                flipper_border_color if flipper_border_color is not None else "#A5CCEA"
            )
            flipper_flip_gap = flipper_flip_gap if flipper_flip_gap is not None else 12

            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "legend": {"textSetMap": {"textColor": "#177DDC"}},
                "tooltip": {
                    "backgroundColor": "#303467",
                    "textSetMap": {"textColor": "#A6ADD0"},
                },
                "drawSettings": {
                    "fillColor": flipper_fill_color,
                    "styleType": flipper_style_type,
                    "borderColor": flipper_border_color,
                    "lineWidthMap": {"width": 1, "style": "solid"},
                    "fontFamily": "LCDFont",
                    "fontSize": flipper_font_size,
                    "flipGap": flipper_flip_gap,
                    "fontColor": flipper_font_color,
                },
                "title": {
                    "isExtra": True,
                    "show": False,
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 20,
                        "textColor": "#FEFEFE",
                    },
                },
                "card": {
                    "border": "rgba(30, 39, 55, 0.8)",
                    "padding": 12,
                    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                    "lineWidthMap": {"width": 1, "style": "solid"},
                },
                "numberSet": {
                    "intFigure": flipper_int_figure,
                    "decimalFigure": flipper_decimal_figure,
                    "thousandthPlace": "thousandthPlaceChecked"
                    if flipper_thousandth
                    else "thousandthPlaceUnchecked",
                },
            }

        # 指标卡多种样式预设
        if chart_type == "metric":
            return self.get_metric_style_json(
                left=left,
                top=top,
                width=width,
                height=height,
                style_preset=metric_style,
                value_color=metric_value_color,
                label_color=metric_label_color,
                icon_color=metric_icon_color,
                label_visible=metric_label_visible,
            )

        # 饼图特定样式
        if chart_type == "pie":
            outer_radius = pie_outer_radius if pie_outer_radius is not None else 80
            inner_radius = pie_inner_radius if pie_inner_radius is not None else 60
            label_position = pie_label_position if pie_label_position else "outside"
            legend_position = pie_legend_position if pie_legend_position else "bottom"

            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "textData": {"show": False},
                "legend": {
                    "isExtra": True,
                    "textSetMap": {
                        "size": 12,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 12,
                        "textColor": "#177DDC",
                    },
                    "position": legend_position,
                },
                "tooltip": {
                    "backgroundColor": "#303467",
                    "isExtra": True,
                    "textSetMap": {
                        "size": 12,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 12,
                        "textColor": "#A6ADD0",
                    },
                    "content": ["dimension", "measure", "percent"],
                },
                "scroll": {"cycleSpeed": 5, "show": True},
                "drawSettings": {
                    "outerRadius": outer_radius,
                    "type": "default",
                    "innerRadius": inner_radius,
                },
                "label": {
                    "isExtra": True,
                    "textSetMap": {
                        "size": 12,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 12,
                        "textColor": "#A6ADD0",
                    },
                    "position": label_position,
                    "content": ["dimension", "measure", "percent"],
                },
                "title": {
                    "isExtra": True,
                    "show": True,
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 16,
                        "align": title_align or "left",
                        "textColor": "#FEFEFE",
                    },
                    "title": view_name or "饼图",
                },
                "card": {
                    "border": "rgba(30, 39, 55, 0.8)",
                    "padding": 12,
                    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                    "lineWidthMap": {"width": 1, "style": "solid"},
                },
            }

        # 雷达图特定样式
        if chart_type == "radar":
            radar_radius = radar_radius if radar_radius is not None else 50
            radar_legend_position = (
                radar_legend_position if radar_legend_position is not None else "top"
            )
            radar_label_position = (
                radar_label_position if radar_label_position is not None else "auto"
            )
            radar_mode = radar_mode if radar_mode else "indicator"

            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "textData": {"show": False},
                "branchSettings": {"type": radar_mode},
                "legend": {
                    "isExtra": True,
                    "textSetMap": {
                        "size": 14,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 14,
                        "textColor": "#177DDC",
                    },
                    "position": radar_legend_position,
                },
                "tooltip": {
                    "backgroundColor": "#303467",
                    "isExtra": True,
                    "textSetMap": {
                        "size": 14,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 14,
                        "textColor": "#A6ADD0",
                    },
                    "content": ["dimension", "measure"],
                },
                "drawSettings": {
                    "radius": radar_radius,
                },
                "label": {
                    "isExtra": True,
                    "textSetMap": {
                        "size": 14,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 14,
                        "textColor": "#A6ADD0",
                    },
                    "position": radar_label_position,
                },
                "title": {
                    "isExtra": True,
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 20,
                        "textColor": "#FEFEFE",
                    },
                },
                "card": {
                    "border": "rgba(30, 39, 55, 0.8)",
                    "padding": 12,
                    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                    "lineWidthMap": {"width": 1, "style": "solid"},
                },
            }

        # 线图特定样式
        if chart_type == "line":
            legend_pos = bar_legend_position if bar_legend_position else "top"
            scroll_enabled = (
                bar_scroll_enabled if bar_scroll_enabled is not None else False
            )
            scroll_speed = bar_scroll_speed if bar_scroll_speed is not None else 5
            label_show = bar_label_show if bar_label_show is not None else False
            axis_rotate = bar_axis_rotate if bar_axis_rotate is not None else 0
            line_style = line_type if line_type in ["line", "curve"] else "curve"

            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "textData": {"show": False},
                "legend": {
                    "isExtra": True,
                    "textSetMap": {
                        "size": 14,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 14,
                        "textColor": "#177DDC",
                    },
                    "position": legend_pos,
                },
                "tooltip": {
                    "backgroundColor": "#303467",
                    "isExtra": True,
                    "textSetMap": {
                        "size": 12,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 12,
                        "textColor": "#A6ADD0",
                    },
                    "content": ["dimension", "measure"],
                },
                "scroll": {
                    "isExtra": True,
                    "show": scroll_enabled,
                    "dimensionNum": 5,
                    "scrollSpeed": scroll_speed,
                },
                "drawSettings": {
                    "lineType": line_style,
                    "node": "circle",
                    "nodeSize": 8,
                    "gridSet": {
                        "isAdaption": True,
                        "gridLeft": None,
                        "gridTop": None,
                        "gridBottom": None,
                        "gridRight": None,
                    },
                },
                "label": {
                    "isExtra": True,
                    "show": label_show,
                    "textSetMap": {
                        "size": 12,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 12,
                        "textColor": "#A6ADD0",
                    },
                    "position": "top",
                },
                "title": {
                    "isExtra": True,
                    "show": True,
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 16,
                        "align": title_align or "left",
                        "textColor": "#FEFEFE",
                    },
                    "title": view_name or "线图",
                },
                "axis": {
                    "x": {
                        "axes": ["showXAxis"],
                        "scale": "auto",
                        "rotate": axis_rotate,
                        "textSetMap": {
                            "size": 14,
                            "fontSize": 14,
                            "textColor": "#a7adcd",
                            "textBold": False,
                            "textItalic": False,
                        },
                    },
                    "y": {
                        "axes": ["showYAxis", "showAxisLine"],
                        "titleMap": {"isChecked": True, "value": ""},
                        "splitMap": {"isChecked": True},
                        "textSetMap": {
                            "size": 14,
                            "fontSize": 14,
                            "textColor": "#a7adcd",
                            "textBold": False,
                            "textItalic": False,
                        },
                    },
                },
                "card": {
                    "border": "rgba(30, 39, 55, 0.8)",
                    "padding": 12,
                    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                    "lineWidthMap": {"width": 1, "style": "solid"},
                },
            }

        # 柱图特定样式
        if chart_type == "bar":
            legend_pos = bar_legend_position if bar_legend_position else "top"
            scroll_enabled = (
                bar_scroll_enabled if bar_scroll_enabled is not None else True
            )
            scroll_speed = bar_scroll_speed if bar_scroll_speed is not None else 5
            label_show = bar_label_show if bar_label_show is not None else False
            label_pos = bar_label_position if bar_label_position else "auto"
            axis_rotate = bar_axis_rotate if bar_axis_rotate is not None else 0

            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "textData": {"show": False},
                "legend": {
                    "isExtra": True,
                    "textSetMap": {
                        "size": 14,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 14,
                        "textColor": "#177DDC",
                    },
                    "position": legend_pos,
                },
                "tooltip": {
                    "backgroundColor": "#303467",
                    "isExtra": True,
                    "textSetMap": {
                        "size": 12,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 12,
                        "textColor": "#A6ADD0",
                    },
                    "content": ["dimension", "measure"],
                },
                "scroll": {
                    "cycleSpeed": scroll_speed,
                    "show": scroll_enabled,
                    "type": "highlight",
                },
                "drawSettings": {
                    "seriesType": "bar",
                    "widthMap": {"isAdaption": True},
                },
                "label": {
                    "isExtra": True,
                    "show": label_show,
                    "textSetMap": {
                        "size": 12,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 12,
                        "textColor": "#A6ADD0",
                    },
                    "position": label_pos,
                },
                "title": {
                    "isExtra": True,
                    "show": True,
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 16,
                        "align": title_align or "left",
                        "textColor": "#FEFEFE",
                    },
                    "title": view_name or "柱图",
                },
                "axis": {
                    "x": {
                        "rotate": axis_rotate,
                        "axes": ["showXAxis"],
                        "scale": "auto",
                    },
                    "y": {
                        "axes": ["showYAxis", "showAxisLine"],
                        "splitMap": {"isChecked": True},
                        "titleMap": {"isChecked": True, "value": ""},
                    },
                },
                "card": {
                    "border": "rgba(30, 39, 55, 0.8)",
                    "padding": 12,
                    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                    "lineWidthMap": {"width": 1, "style": "solid"},
                },
            }

        # 3D柱图特定样式
        if chart_type == "bar3d":
            legend_pos = bar_legend_position if bar_legend_position else "top"
            scroll_enabled = (
                bar_scroll_enabled if bar_scroll_enabled is not None else True
            )
            scroll_speed = bar_scroll_speed if bar_scroll_speed is not None else 5
            label_show = bar_label_show if bar_label_show is not None else False
            label_pos = bar_label_position if bar_label_position else "auto"
            axis_rotate = bar_axis_rotate if bar_axis_rotate is not None else 0

            return {
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "textData": {"show": False},
                "legend": {
                    "isExtra": True,
                    "textSetMap": {
                        "size": 14,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 14,
                        "textColor": "#177DDC",
                    },
                    "position": legend_pos,
                },
                "tooltip": {
                    "backgroundColor": "#303467",
                    "isExtra": True,
                    "textSetMap": {
                        "size": 12,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 12,
                        "textColor": "#A6ADD0",
                    },
                    "content": ["dimension", "measure"],
                },
                "scroll": {
                    "cycleSpeed": scroll_speed,
                    "show": scroll_enabled,
                    "type": "highlight",
                },
                "drawSettings": {
                    "type": "cube",
                    "cubeColorSystem": "#4CC9F0",
                    "seriesType": "bar",
                    "widthMap": {"isAdaption": True},
                },
                "label": {
                    "isExtra": True,
                    "show": label_show,
                    "textSetMap": {
                        "size": 12,
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 12,
                        "textColor": "#A6ADD0",
                    },
                    "position": label_pos,
                },
                "title": {
                    "isExtra": True,
                    "show": True,
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 16,
                        "align": title_align or "left",
                        "textColor": "#FEFEFE",
                    },
                    "title": view_name or "3D柱图",
                },
                "axis": {
                    "x": {
                        "rotate": axis_rotate,
                        "axes": ["showXAxis"],
                        "scale": "auto",
                    },
                    "y": {
                        "axes": ["showYAxis", "showAxisLine"],
                        "splitMap": {"isChecked": True},
                        "titleMap": {"isChecked": True, "value": ""},
                    },
                },
                "card": {
                    "border": "rgba(30, 39, 55, 0.8)",
                    "padding": 12,
                    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                    "lineWidthMap": {"width": 1, "style": "solid"},
                },
            }

        # 表格组件特定样式
        if chart_type == "table":
            return {
                "preSetStyle": {"themeColor": 0},
                "screenPosition": {
                    "position": {"x": left, "y": top, "w": width, "h": height}
                },
                "legend": {"textSetMap": {"textColor": "#177DDC"}},
                "scroll": {
                    "isExtra": True,
                    "show": False,
                    "type": "smooth",
                    "speed": 3,
                },
                "tooltip": {
                    "backgroundColor": "#303467",
                    "textSetMap": {"textColor": "#A6ADD0"},
                },
                "tableBodySettings": {
                    "fontFamily": "default",
                    "rowSplitLine": {"size": 1, "color": "#334979"},
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": False,
                        "fontSize": 12,
                        "textColor": "#DBDFF1",
                    },
                    "oddNumberedColor": "#0A1E38",
                    "lineHeight": 2,
                    "evenNumberedColor": "#020B1C",
                    "colSplitLine": {"size": 0, "color": "#334979"},
                },
                "tableHeaderSettings": {
                    "fontFamily": "default",
                    "bgColor": "#08143E",
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 12,
                        "textColor": "#DBDFF1",
                    },
                    "colIndex": [""],
                    "lineHeight": 2,
                },
                "title": {
                    "isExtra": True,
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 20,
                        "textColor": "#FEFEFE",
                    },
                },
                "card": {
                    "border": "rgba(30, 39, 55, 0.8)",
                    "padding": 12,
                    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                    "lineWidthMap": {"width": 1, "style": "solid"},
                },
            }

        # 其他图表类型使用基础样式（可以后续扩展）
        return base_style

    def get_metric_style_json(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        style_preset: Optional[str] = "default",
        value_color: Optional[str] = None,
        label_color: Optional[str] = None,
        icon_color: Optional[str] = None,
        label_visible: Optional[bool] = True,
    ) -> Dict:
        """获取指标卡样式配置，支持多种预设样式

        Args:
            style_preset: 样式预设
                - "default": 默认深色卡片样式
                - "gradient": 渐变背景样式
                - "light": 浅色背景样式
                - "minimal": 极简透明样式
                - "card": 圆角卡片样式
            value_color: 数值颜色，会覆盖预设的默认颜色
            label_color: 标签颜色，会覆盖预设的默认颜色
            icon_color: 图标颜色，会覆盖预设的默认颜色
            label_visible: 是否显示标签/标题，默认True显示
        """

        # 确保 style_preset 有有效值
        if not style_preset:
            style_preset = "default"

        # 预设样式定义（基于 BIupdate.curl 中 4 个指标卡的真实样式）
        presets = {
            # 样式 A：底部标题，无图标，间距 8
            "default": {
                "card": {
                    "lineWidthMap": {"width": 1, "style": "solid"},
                    "padding": 12,
                    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                    "border": "rgba(30, 39, 55, 0.8)",
                },
                "title": {
                    "isExtra": True,
                    "show": False,
                    "textSetMap": {
                        "fontSize": 20,
                        "textColor": "#FEFEFE",
                        "textBold": True,
                        "textItalic": False,
                    },
                },
                "metricName": {
                    "isExtra": True,
                    "textSetMap": {
                        "fontSize": 20,
                        "textColor": "#A6ADD0",
                        "textBold": False,
                        "textItalic": False,
                    },
                },
                "metricValue": {
                    "textSetMap": {
                        "fontSize": 32,
                        "textColor": "#A6ADD0",
                        "textBold": False,
                        "textItalic": False,
                    },
                    "prefixFontSize": 30,
                    "suffixFontSize": 12,
                },
                "drawSettings": {
                    "position": "bottom",
                    "gap": 8,
                    "iconPositionMap": {"position": "none"},
                    "iconColor": "#5B8FFA",
                },
            },
            # 样式 B：顶部标题，左对齐，无图标，间距 8
            "top": {
                "card": {
                    "lineWidthMap": {"width": 1, "style": "solid"},
                    "padding": 12,
                    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                    "border": "rgba(30, 39, 55, 0.8)",
                },
                "title": {
                    "isExtra": True,
                    "show": False,
                    "textSetMap": {
                        "fontSize": 20,
                        "textColor": "#FEFEFE",
                        "textBold": True,
                        "textItalic": False,
                        "align": "left",
                    },
                },
                "metricName": {
                    "isExtra": True,
                    "textSetMap": {
                        "fontSize": 20,
                        "textColor": "#A6ADD0",
                        "textBold": False,
                        "textItalic": False,
                    },
                },
                "metricValue": {
                    "textSetMap": {
                        "fontSize": 32,
                        "textColor": "#A6ADD0",
                        "textBold": False,
                        "textItalic": False,
                    },
                    "prefixFontSize": 30,
                    "suffixFontSize": 12,
                },
                "drawSettings": {
                    "position": {"position": "top", "align": "left"},
                    "gap": 8,
                    "iconPositionMap": {"position": "none"},
                    "iconColor": "#5B8FFA",
                },
                "textData": {"content": []},
            },
            # 样式 C：顶部标题，左对齐，左侧图标，间距 12
            "icon_left": {
                "card": {
                    "lineWidthMap": {"width": 1, "style": "solid"},
                    "padding": 12,
                    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                    "border": "rgba(30, 39, 55, 0.8)",
                },
                "title": {
                    "isExtra": True,
                    "show": False,
                    "textSetMap": {
                        "fontSize": 20,
                        "textColor": "#FEFEFE",
                        "textBold": True,
                        "textItalic": False,
                        "align": "left",
                    },
                },
                "metricName": {
                    "isExtra": True,
                    "textSetMap": {
                        "fontSize": 20,
                        "textColor": "#A6ADD0",
                        "textBold": False,
                        "textItalic": False,
                    },
                },
                "metricValue": {
                    "textSetMap": {
                        "fontSize": 32,
                        "textColor": "#A6ADD0",
                        "textBold": False,
                        "textItalic": False,
                    },
                    "prefixFontSize": 30,
                    "suffixFontSize": 12,
                },
                "drawSettings": {
                    "position": {"position": "top", "align": "left"},
                    "gap": 12,
                    "iconPositionMap": {"position": "left", "icon": "e84d"},
                    "iconColor": "#5B8FFA",
                },
                "textData": {"content": []},
            },
            # 样式 D：顶部标题，左对齐，follow 图标，间距 12
            "icon_follow": {
                "card": {
                    "lineWidthMap": {"width": 1, "style": "solid"},
                    "padding": 12,
                    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
                    "border": "rgba(30, 39, 55, 0.8)",
                },
                "title": {
                    "isExtra": True,
                    "show": False,
                    "textSetMap": {
                        "fontSize": 20,
                        "textColor": "#FEFEFE",
                        "textBold": True,
                        "textItalic": False,
                        "align": "left",
                    },
                },
                "metricName": {
                    "isExtra": True,
                    "textSetMap": {
                        "fontSize": 20,
                        "textColor": "#A6ADD0",
                        "textBold": False,
                        "textItalic": False,
                    },
                },
                "metricValue": {
                    "textSetMap": {
                        "fontSize": 32,
                        "textColor": "#A6ADD0",
                        "textBold": False,
                        "textItalic": False,
                    },
                    "prefixFontSize": 30,
                    "suffixFontSize": 12,
                },
                "drawSettings": {
                    "position": {"position": "top", "align": "left"},
                    "gap": 12,
                    "iconPositionMap": {"position": "follow", "icon": "e84d"},
                    "iconColor": "#5B8FFA",
                },
                "textData": {"content": []},
            },
            # 渐变样式：保持原有设计
            "gradient": {
                "card": {
                    "lineWidthMap": {"width": 2, "style": "solid"},
                    "padding": 16,
                    "cardBackgroundColor": "rgba(40, 60, 120, 0.9)",
                    "border": "rgba(70, 130, 220, 0.8)",
                },
                "title": {
                    "isExtra": True,
                    "textSetMap": {
                        "fontSize": 18,
                        "textColor": "#E0E6FF",
                        "textBold": True,
                        "textItalic": False,
                    },
                },
                "metricName": {
                    "isExtra": True,
                    "textSetMap": {
                        "fontSize": 20,
                        "textColor": "#B8C5E8",
                        "textBold": False,
                        "textItalic": False,
                    },
                },
                "metricValue": {
                    "textSetMap": {
                        "fontSize": 38,
                        "textColor": "#00F5FF",
                        "textBold": True,
                        "textItalic": False,
                    },
                    "prefixFontSize": 28,
                    "suffixFontSize": 14,
                },
                "drawSettings": {
                    "position": "bottom",
                    "gap": 10,
                    "iconPositionMap": {"position": "left"},
                    "iconColor": "#00D4FF",
                },
            },
            # 浅色样式：保持原有设计
            "light": {
                "card": {
                    "lineWidthMap": {"width": 1, "style": "solid"},
                    "padding": 14,
                    "cardBackgroundColor": "rgba(240, 245, 255, 0.95)",
                    "border": "rgba(180, 200, 230, 0.6)",
                },
                "title": {
                    "isExtra": True,
                    "textSetMap": {
                        "fontSize": 20,
                        "textColor": "#2C3E50",
                        "textBold": True,
                        "textItalic": False,
                    },
                },
                "metricName": {
                    "isExtra": True,
                    "textSetMap": {
                        "fontSize": 22,
                        "textColor": "#5D6D7E",
                        "textBold": False,
                        "textItalic": False,
                    },
                },
                "metricValue": {
                    "textSetMap": {
                        "fontSize": 36,
                        "textColor": "#1A5F7A",
                        "textBold": True,
                        "textItalic": False,
                    },
                    "prefixFontSize": 26,
                    "suffixFontSize": 12,
                },
                "drawSettings": {
                    "position": "bottom",
                    "gap": 8,
                    "iconPositionMap": {"position": "right"},
                    "iconColor": "#3498DB",
                },
            },
            # 极简样式：保持原有设计
            "minimal": {
                "card": {
                    "lineWidthMap": {"width": 0, "style": "solid"},
                    "padding": 8,
                    "cardBackgroundColor": "rgba(0, 0, 0, 0)",
                    "border": "transparent",
                },
                "title": {
                    "isExtra": True,
                    "textSetMap": {
                        "fontSize": 16,
                        "textColor": "#F0F0F0",
                        "textBold": False,
                        "textItalic": False,
                    },
                },
                "metricName": {
                    "isExtra": True,
                    "textSetMap": {
                        "fontSize": 18,
                        "textColor": "#CCCCCC",
                        "textBold": False,
                        "textItalic": False,
                    },
                },
                "metricValue": {
                    "textSetMap": {
                        "fontSize": 32,
                        "textColor": "#FFFFFF",
                        "textBold": True,
                        "textItalic": False,
                    },
                    "prefixFontSize": 24,
                    "suffixFontSize": 12,
                },
                "drawSettings": {
                    "position": "right",
                    "gap": 6,
                    "iconPositionMap": {"position": "none"},
                    "iconColor": "#888888",
                },
            },
            # 卡片样式：保持原有设计
            "card": {
                "card": {
                    "lineWidthMap": {"width": 2, "style": "solid"},
                    "padding": 16,
                    "cardBackgroundColor": "rgba(20, 30, 60, 0.85)",
                    "border": "rgba(100, 180, 255, 0.6)",
                    "borderRadius": 12,
                },
                "title": {
                    "isExtra": True,
                    "textSetMap": {
                        "fontSize": 20,
                        "textColor": "#FFFFFF",
                        "textBold": True,
                        "textItalic": False,
                    },
                },
                "metricName": {
                    "isExtra": True,
                    "textSetMap": {
                        "fontSize": 22,
                        "textColor": "#AABBCC",
                        "textBold": False,
                        "textItalic": False,
                    },
                },
                "metricValue": {
                    "textSetMap": {
                        "fontSize": 36,
                        "textColor": "#66DDFF",
                        "textBold": True,
                        "textItalic": False,
                    },
                    "prefixFontSize": 28,
                    "suffixFontSize": 14,
                },
                "drawSettings": {
                    "position": "bottom",
                    "gap": 12,
                    "iconPositionMap": {"position": "left"},
                    "iconColor": "#66CCFF",
                },
            },
        }

        # 获取预设样式
        style_config = presets.get(style_preset, presets["default"]).copy()

        # 应用自定义颜色覆盖
        if value_color:
            style_config["metricValue"]["textSetMap"]["textColor"] = value_color
        if label_color:
            style_config["metricName"]["textSetMap"]["textColor"] = label_color
            style_config["title"]["textSetMap"]["textColor"] = label_color
        if icon_color:
            style_config["drawSettings"]["iconColor"] = icon_color

        # 控制组件标题显示（默认不显示标题，但保留标签显示）
        if label_visible is False:
            style_config["title"]["show"] = False

        # 添加 screenPosition
        style_config["screenPosition"] = {
            "position": {"x": left, "y": top, "w": width, "h": height}
        }

        return style_config

    def add_component(
        self,
        screen_id: int,
        model_id: int,
        dimension_field: str,
        indicator_field: str,
        chart_type: str = "bar",
        top: int = 100,
        left: int = 100,
        width: int = 440,
        height: int = 270,
        view_name: Optional[str] = None,
        text_align: Optional[str] = None,
        font_size: Optional[int] = None,
        title_align: Optional[str] = None,
        metric_style: Optional[str] = None,
        metric_value_color: Optional[str] = None,
        metric_label_color: Optional[str] = None,
        metric_icon_color: Optional[str] = None,
        metric_label_visible: Optional[bool] = False,
        pie_outer_radius: Optional[int] = None,
        pie_inner_radius: Optional[int] = None,
        pie_label_position: Optional[str] = None,
        pie_legend_position: Optional[str] = None,
        bar_legend_position: Optional[str] = None,
        bar_scroll_enabled: Optional[bool] = None,
        bar_scroll_speed: Optional[int] = None,
        bar_label_show: Optional[bool] = None,
        bar_label_position: Optional[str] = None,
        bar_axis_rotate: Optional[int] = None,
        script_code: Optional[str] = None,
        order_type: Optional[str] = None,
        indicator_order_type: Optional[str] = None,
        decorate_index: Optional[int] = None,
        line_type: Optional[str] = None,
        extra_dimension_fields: Optional[List[str]] = None,
        extra_indicator_fields: Optional[List[str]] = None,
        flipper_int_figure: Optional[int] = None,
        flipper_decimal_figure: Optional[int] = None,
        flipper_thousandth: Optional[bool] = None,
        flipper_style_type: Optional[str] = None,
        flipper_font_color: Optional[str] = None,
        flipper_fill_color: Optional[str] = None,
        flipper_border_color: Optional[str] = None,
        flipper_flip_gap: Optional[int] = None,
        radar_radius: Optional[int] = None,
        radar_legend_position: Optional[str] = None,
        radar_label_position: Optional[str] = None,
        radar_mode: Optional[str] = None,
        date_filter: Optional[str] = None,
        linkage: Optional[List[str]] = None,
        indicator_label: Optional[str] = None,
    ) -> str:
        """向大屏添加新组件"""

        # 1. 获取现有配置
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id)

        # 非数据组件不需要模型信息
        no_data_types = ["time", "text", "decorate", "head", "card", "icon"]
        if chart_type in no_data_types:
            model_info = None
        else:
            # 2. 获取模型信息
            print(f"正在获取模型信息 (ID: {model_id})...")
            model_info = _get_model_info(model_id, self.base_url, self.headers)

        # 3. 校验联动配置
        no_data_types = ["time", "text", "decorate", "head", "card", "icon"]
        if linkage:
            # 规则1：只有设置了维度的组件才能联动
            if chart_type in no_data_types or not dimension_field:
                raise ValueError(
                    "只有设置了维度的组件才能联动其他组件（时间/文本/装饰/头部/卡片/图标类型不支持联动）"
                )
            # 规则2：被联动的组件必须和当前组件使用相同数据模型
            component_map = screen_data.get("componentMap", {})
            target_uuids = linkage
            for target_uuid in target_uuids:
                if target_uuid not in component_map:
                    raise ValueError(f"联动目标组件 UUID不存在: {target_uuid}")
                target_comp = component_map[target_uuid]
                target_model_id = target_comp.get("modelId")
                if target_model_id != model_id:
                    raise ValueError(
                        f"联动目标组件 UUID={target_uuid} 使用的数据模型(ID:{target_model_id})"
                        f"与当前组件(ID:{model_id})不同，联动组件必须使用相同数据模型"
                    )

        # 4. 构建新组件配置
        print(f"正在构建新组件配置...")
        new_config = self.create_component_config(
            model_info=model_info,
            dimension_field=dimension_field,
            indicator_field=indicator_field,
            chart_type=chart_type,
            top=top,
            left=left,
            width=width,
            height=height,
            view_name=view_name,
            text_align=text_align,
            font_size=font_size,
            title_align=title_align,
            metric_style=metric_style,
            metric_value_color=metric_value_color,
            metric_label_color=metric_label_color,
            metric_icon_color=metric_icon_color,
            metric_label_visible=metric_label_visible,
            pie_outer_radius=pie_outer_radius,
            pie_inner_radius=pie_inner_radius,
            pie_label_position=pie_label_position,
            pie_legend_position=pie_legend_position,
            bar_legend_position=bar_legend_position,
            bar_scroll_enabled=bar_scroll_enabled,
            bar_scroll_speed=bar_scroll_speed,
            bar_label_show=bar_label_show,
            bar_label_position=bar_label_position,
            bar_axis_rotate=bar_axis_rotate,
            script_code=script_code,
            order_type=order_type,
            indicator_order_type=indicator_order_type,
            decorate_index=decorate_index,
            line_type=line_type,
            extra_dimension_fields=extra_dimension_fields,
            extra_indicator_fields=extra_indicator_fields,
            flipper_int_figure=flipper_int_figure,
            flipper_decimal_figure=flipper_decimal_figure,
            flipper_thousandth=flipper_thousandth,
            flipper_style_type=flipper_style_type,
            flipper_font_color=flipper_font_color,
            flipper_fill_color=flipper_fill_color,
            flipper_border_color=flipper_border_color,
            flipper_flip_gap=flipper_flip_gap,
            radar_radius=radar_radius,
            radar_legend_position=radar_legend_position,
            radar_label_position=radar_label_position,
            radar_mode=radar_mode,
            date_filter=date_filter,
            linkage=linkage,
            indicator_label=indicator_label,
        )

        # 4. 添加到现有配置
        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        # 添加 layer
        if "layers" not in config["config"]:
            config["config"]["layers"] = []
        config["config"]["layers"].append(new_config["layer"])

        # 添加 layout
        config["layouts"].append(new_config["layout"])

        # 添加 component
        config["componentMap"][new_config["uuid"]] = new_config["component"]

        print(f"新组件 UUID: {new_config['uuid']}")
        print(f"位置：top={top}, left={left}, width={width}, height={height}")

        # 5. 提交更新
        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)

        return new_config["uuid"]


def main():
    import argparse

    parser = argparse.ArgumentParser(description="向大屏添加新组件")
    parser.add_argument("--screen-id", type=int, required=True, help="大屏 ID")
    parser.add_argument(
        "--model-id",
        type=int,
        required=False,
        help="数据模型 ID（时间/文本/装饰/头部/卡片/图标组件不需要）",
    )
    parser.add_argument(
        "--dimension-field",
        required=False,
        help="维度字段名（时间/文本/装饰/头部/卡片/图标组件不需要）",
    )
    parser.add_argument(
        "--indicator-field",
        required=False,
        help="指标字段名（时间/文本/装饰/头部/卡片/图标组件不需要）",
    )
    parser.add_argument(
        "--indicator-label",
        dest="indicator_label",
        required=False,
        help='指标显示名称（用于自定义指标卡显示的文字，如"本月收款金额"）',
    )
    parser.add_argument(
        "--chart-type",
        default="bar",
        choices=[
            "bar",
            "bar3d",
            "line",
            "pie",
            "metric",
            "table",
            "customTable",
            "ranking",
            "dualAxis",
            "funnel",
            "gauge",
            "horizontalBar",
            "map",
            "text",
            "decorate",
            "head",
            "script",
            "card",
            "time",
            "icon",
            "flipper",
            "radar",
        ],
        help="图表类型",
    )
    parser.add_argument(
        "--view-name",
        help="视图名称（文本组件必填，装饰组件用于指定子类型如 bar:, square:, base:）",
    )
    parser.add_argument("--top", type=int, default=100, help="组件顶部位置 (px)")
    parser.add_argument("--left", type=int, default=100, help="组件左侧位置 (px)")
    parser.add_argument("--width", type=int, default=440, help="组件宽度 (px)")
    parser.add_argument("--height", type=int, default=270, help="组件高度 (px)")
    parser.add_argument(
        "--align",
        default=None,
        choices=["left", "center", "right"],
        help="文本对齐方式（仅对文本组件有效，默认居中）",
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=None,
        help="文本字体大小（仅对文本组件有效）",
    )
    parser.add_argument(
        "--title-align",
        default=None,
        choices=["left", "center", "right"],
        help="组件标题对齐方式（仅对图表组件有效，默认居左）",
    )
    parser.add_argument(
        "--metric-style",
        default=None,
        choices=[
            "default",
            "top",
            "icon_left",
            "icon_follow",
            "gradient",
            "light",
            "minimal",
            "card",
        ],
        help="指标卡样式预设（仅对指标卡有效）：default(底部标题)/top(顶部标题)/icon_left(左侧图标)/icon_follow(跟随图标)/gradient(渐变)/light(浅色)/minimal(极简)/card(卡片)",
    )
    parser.add_argument(
        "--metric-value-color",
        default=None,
        help="指标卡数值颜色（仅对指标卡有效），如 #FF6B6B",
    )
    parser.add_argument(
        "--metric-label-color",
        default=None,
        help="指标卡标签颜色（仅对指标卡有效），如 #4ECDC4",
    )
    parser.add_argument(
        "--metric-icon-color",
        default=None,
        help="指标卡图标颜色（仅对指标卡有效），如 #5B8FFA",
    )
    parser.add_argument(
        "--metric-label-visible",
        type=lambda x: x.lower() == "true",
        default=False,
        help="指标卡标签显示控制（仅对指标卡有效），true显示/false隐藏，默认隐藏",
    )
    parser.add_argument(
        "--pie-outer-radius",
        type=int,
        default=None,
        help="饼图外半径（仅对饼图有效），默认 80",
    )
    parser.add_argument(
        "--pie-inner-radius",
        type=int,
        default=None,
        help="饼图内半径（仅对饼图有效），默认 60，设为 0 则为实心饼图",
    )
    parser.add_argument(
        "--pie-label-position",
        default=None,
        choices=["outside", "inside", "center"],
        help="饼图标签位置（仅对饼图有效）：outside(外部)/inside(内部)/center(中心)",
    )
    parser.add_argument(
        "--pie-legend-position",
        default=None,
        choices=["bottom", "top", "left", "right"],
        help="饼图图例位置（仅对饼图有效）：bottom/top/left/right",
    )
    parser.add_argument(
        "--bar-legend-position",
        default=None,
        choices=["bottom", "top", "left", "right"],
        help="柱图图例位置（仅对柱图有效）：bottom/top/left/right",
    )
    parser.add_argument(
        "--bar-scroll-enabled",
        type=lambda x: x.lower() == "true",
        default=None,
        help="柱图是否启用滚动（仅对柱图有效）：true/false",
    )
    parser.add_argument(
        "--bar-scroll-speed",
        type=int,
        default=None,
        help="柱图滚动速度（仅对柱图有效）：1-10",
    )
    parser.add_argument(
        "--bar-label-show",
        type=lambda x: x.lower() == "true",
        default=None,
        help="柱图是否显示数据标签（仅对柱图有效）：true/false",
    )
    parser.add_argument(
        "--bar-label-position",
        default=None,
        choices=["top", "right", "bottom", "auto"],
        help="柱图数据标签位置（仅对柱图有效）：top/right/bottom/auto",
    )
    parser.add_argument(
        "--bar-axis-rotate",
        type=int,
        default=None,
        help="柱图X轴标签旋转角度（仅对柱图有效）：0-45",
    )
    parser.add_argument(
        "--script-code",
        default=None,
        help="脚本组件的 JavaScript 代码（仅对 script 类型有效）",
    )
    parser.add_argument("--base-url", default=get_base_url(), help="API 基础 URL")
    parser.add_argument(
        "--env",
        default="dev",
        choices=["dev", "test", "prod"],
        help="环境 (默认 dev，与 --base-url 二选一)",
    )
    parser.add_argument(
        "--order-type",
        default=None,
        choices=["asc", "desc"],
        help="维度排序方式：asc(升序) 或 desc(降序)，默认 asc",
    )
    parser.add_argument(
        "--indicator-order-type",
        default=None,
        choices=["asc", "desc", "none"],
        help="指标排序方式：asc(升序)、desc(降序)、none(清除排序)，默认 desc",
    )
    parser.add_argument(
        "--decorate-index",
        type=int,
        default=None,
        help="装饰图片编号（仅对 head/decorate 类型有效）：1-14，默认 head 为 4，decorate 为 1",
    )
    parser.add_argument(
        "--line-type",
        default=None,
        choices=["line", "curve"],
        help="线图线条类型（仅对 line 类型有效）：line(折线)，curve(曲线)，默认 curve",
    )
    parser.add_argument(
        "--extra-dimension-fields",
        default=None,
        help="额外的维度字段（逗号分隔，仅对 table 类型有效），如 field1,field2",
    )
    parser.add_argument(
        "--extra-indicator-fields",
        default=None,
        help="额外的指标字段（逗号分隔，仅对 table 类型有效），如 field1,field2",
    )
    parser.add_argument(
        "--flipper-int-figure",
        type=int,
        default=None,
        help="翻牌器整数位数（仅对 flipper 类型有效），默认 8",
    )
    parser.add_argument(
        "--flipper-decimal-figure",
        type=int,
        default=None,
        help="翻牌器小数位数（仅对 flipper 类型有效），默认 2",
    )
    parser.add_argument(
        "--flipper-thousandth",
        type=lambda x: x.lower() == "true",
        default=None,
        help="翻牌器千分位（仅对 flipper 类型有效）：true/false，默认 true",
    )
    parser.add_argument(
        "--flipper-style-type",
        default=None,
        choices=["round", "square"],
        help="翻牌器样式类型（仅对 flipper 类型有效）：round(圆角)/square(直角)",
    )
    parser.add_argument(
        "--flipper-font-color",
        default=None,
        help="翻牌器字体颜色（仅对 flipper 类型有效），如 linear-gradient(rgb(255, 255, 255) 0%%, rgb(17, 93, 151) 100%%)",
    )
    parser.add_argument(
        "--flipper-fill-color",
        default=None,
        help="翻牌器填充颜色（仅对 flipper 类型有效），如 linear-gradient(180deg, rgba(2,53,107,0.5) 0%%, rgba(5,101,164,0.5) 100%%)",
    )
    parser.add_argument(
        "--flipper-border-color",
        default=None,
        help="翻牌器边框颜色（仅对 flipper 类型有效），如 #A5CCEA",
    )
    parser.add_argument(
        "--flipper-flip-gap",
        type=int,
        default=None,
        help="翻牌器翻牌间隔（仅对 flipper 类型有效），默认 12",
    )
    parser.add_argument(
        "--radar-radius",
        type=int,
        default=None,
        help="雷达图半径（仅对 radar 类型有效），默认 50",
    )
    parser.add_argument(
        "--radar-legend-position",
        default=None,
        choices=["top", "bottom", "left", "right"],
        help="雷达图图例位置（仅对 radar 类型有效）",
    )
    parser.add_argument(
        "--radar-label-position",
        default=None,
        choices=["auto", "top", "bottom", "left", "right"],
        help="雷达图标签位置（仅对 radar 类型有效）",
    )
    parser.add_argument(
        "--radar-mode",
        default=None,
        choices=["indicator", "dimension"],
        help="雷达图数据模式（indicator=指标驱动，dimension=维度驱动）",
    )
    parser.add_argument(
        "--date-filter",
        default=None,
        help="日期过滤条件（相对时间: thisYear/thisMonth/lastMonth/thisQuarter/lastQuarter；自定义: 2024-01-01,2024-12-31）",
    )
    parser.add_argument(
        "--linkage",
        nargs="+",
        default=None,
        help="组件联动目标 UUID（支持多选，需与当前组件使用相同数据模型）：例如 abc123 def456",
    )

    args = parser.parse_args()

    base_url = args.base_url if args.base_url else get_base_url(args.env)

    no_data_types = ["time", "text", "decorate", "head", "card", "icon"]
    if args.chart_type not in no_data_types:
        if not args.model_id:
            print(
                "错误：--model-id 是必填参数（时间/文本/装饰/头部/卡片/图标组件除外）"
            )
            sys.exit(1)
        if not args.dimension_field:
            print(
                "错误：--dimension-field 是必填参数（时间/文本/装饰/头部/卡片/图标组件除外）"
            )
            sys.exit(1)
        if not args.indicator_field:
            print(
                "错误：--indicator-field 是必填参数（时间/文本/装饰/头部/卡片/图标组件除外）"
            )
            sys.exit(1)

    adder = BiComponentAdder(base_url)

    try:
        uuid = adder.add_component(
            screen_id=args.screen_id,
            model_id=args.model_id,
            dimension_field=args.dimension_field,
            indicator_field=args.indicator_field,
            chart_type=args.chart_type,
            top=args.top,
            left=args.left,
            width=args.width,
            height=args.height,
            view_name=args.view_name,
            text_align=args.align,
            font_size=args.font_size,
            title_align=args.title_align,
            metric_style=args.metric_style,
            metric_value_color=args.metric_value_color,
            metric_label_color=args.metric_label_color,
            metric_icon_color=args.metric_icon_color,
            metric_label_visible=args.metric_label_visible,
            pie_outer_radius=args.pie_outer_radius,
            pie_inner_radius=args.pie_inner_radius,
            pie_label_position=args.pie_label_position,
            pie_legend_position=args.pie_legend_position,
            bar_legend_position=args.bar_legend_position,
            bar_scroll_enabled=args.bar_scroll_enabled,
            bar_scroll_speed=args.bar_scroll_speed,
            bar_label_show=args.bar_label_show,
            bar_label_position=args.bar_label_position,
            bar_axis_rotate=args.bar_axis_rotate,
            script_code=args.script_code,
            order_type=args.order_type,
            indicator_order_type=args.indicator_order_type,
            decorate_index=args.decorate_index,
            line_type=args.line_type,
            extra_dimension_fields=args.extra_dimension_fields.split(",")
            if args.extra_dimension_fields
            else None,
            extra_indicator_fields=args.extra_indicator_fields.split(",")
            if args.extra_indicator_fields
            else None,
            flipper_int_figure=args.flipper_int_figure,
            flipper_decimal_figure=args.flipper_decimal_figure,
            flipper_thousandth=args.flipper_thousandth,
            flipper_style_type=args.flipper_style_type,
            flipper_font_color=args.flipper_font_color,
            flipper_fill_color=args.flipper_fill_color,
            flipper_border_color=args.flipper_border_color,
            flipper_flip_gap=args.flipper_flip_gap,
            radar_radius=args.radar_radius,
            radar_legend_position=args.radar_legend_position,
            radar_label_position=args.radar_label_position,
            radar_mode=args.radar_mode,
            date_filter=args.date_filter,
            linkage=args.linkage,
            indicator_label=args.indicator_label,
        )

        print(f"\n✅ 组件添加成功!")
        print(f"组件 UUID: {uuid}")
        print(f"访问 URL: {get_preview_url(args.screen_id, base_url)}")

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
