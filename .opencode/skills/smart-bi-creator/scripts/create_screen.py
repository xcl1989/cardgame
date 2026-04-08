#!/usr/bin/env python3
"""
智能大屏创建脚本
用于通过 API 自动化创建 BI 数据大屏
"""

import json
import uuid
import time
import requests
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

from auth import get_base_url, get_preview_url, get, post, load_headers
from bi_utils import (
    get_model_info as _get_model_info,
    build_model_fields as _build_model_fields,
)


class BiScreenCreator:
    """BI 大屏创建器"""

    def __init__(self, base_url: str = "https://dev.cloud.hecom.cn"):
        self.base_url = base_url
        self.headers = load_headers()
        self.cookies = {}

    def set_auth(
        self,
        access_token: str,
        ent_code: str,
        uid: str,
        emp_code: str,
        cookie_str: str = "",
    ):
        """设置认证信息（保留向后兼容）"""
        self.headers.update(
            {
                "accessToken": access_token,
                "entCode": ent_code,
                "uid": uid,
                "empCode": emp_code,
            }
        )
        if cookie_str:
            cookie_parts = cookie_str.split("; ")
            for part in cookie_parts:
                if "=" in part:
                    key, value = part.split("=", 1)
                    self.cookies[key] = value

    def get_model_list(self) -> List[Dict]:
        """获取数据模型列表"""
        url = f"{self.base_url}/biserver/paas/app/dataModel/operation/list"
        payload = {
            "modelName": "",
            "pageNo": 1,
            "pageSize": 500,
            "sortParam": {"field": "id", "asc": 0},
        }
        response = post(url, json=payload, headers=self.headers, cookies=self.cookies)
        data = response.json()
        if data.get("result") == "0":
            return data.get("data", {}).get("list", [])
        raise Exception(f"获取模型列表失败：{data.get('desc')}")

    def create_screen_config(
        self,
        name: str,
        model_id: int,
        model_info: Dict,
        dimension_field: str,
        indicator_field: str,
        width: int = 1920,
        height: int = 80,
        chart_type: str = "head",
        period_type: Optional[str] = None,
        top: Optional[int] = 0,
        left: Optional[int] = 0,
    ) -> Dict:
        """创建大屏配置 JSON"""

        timestamp = int(time.time() * 1000)
        screen_uuid = f"grid-type:{chart_type}-uuid:{timestamp}"

        if chart_type == "head":
            return self._create_head_screen_config(
                name=name,
                screen_uuid=screen_uuid,
                width=width,
                height=height,
                top=top if top is not None else 0,
                left=left if left is not None else 0,
            )

        # 构建模型字段
        model_fields = _build_model_fields(model_info, self.headers.get("entCode", ""))

        # 查找维度和指标字段信息
        dim_field_info = None
        ind_field_info = None

        for ds in model_info.get("modelDatasetDTOList", []):
            for field in ds.get("fields", []):
                if field.get("fieldName") == dimension_field:
                    dim_field_info = {"field": field, "dataset": ds}
                if field.get("fieldName") == indicator_field:
                    ind_field_info = {"field": field, "dataset": ds}

        if not dim_field_info:
            raise Exception(f"未找到维度字段：{dimension_field}")
        if not ind_field_info:
            raise Exception(f"未找到指标字段：{indicator_field}")

        # 构建 dimension
        dim_ds = dim_field_info["dataset"]
        dim_field = dim_field_info["field"]
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
            "displayFields": [dimension_field, indicator_field],
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
            "nodeInfo": {
                "datasetId": dim_ds["datasetId"],
                "datasetLabel": dim_ds["datasetLabel"],
                "datasetName": dim_ds["datasetName"],
                "datasetType": dim_ds["datasetType"],
                "displayFields": [dimension_field, indicator_field],
                "dummy": False,
                "entCode": self.headers.get("entCode", ""),
                "fields": model_fields,
                "label": dim_ds["datasetLabel"],
                "modelTableType": dim_ds["modelTableType"],
                "name": dim_ds["datasetName"],
                "origLabel": dim_ds["datasetLabel"],
                "styleJson": "{}",
                "unionDataSets": [],
            },
        }

        if period_type:
            dimension["periodType"] = period_type

        # 构建 indicator
        ind_ds = ind_field_info["dataset"]
        ind_field = ind_field_info["field"]
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
            "displayFields": [dimension_field, indicator_field],
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
            "newFieldLabel": ind_field["fieldLabel"],
            "nodeInfo": {
                "datasetId": ind_ds["datasetId"],
                "datasetLabel": ind_ds["datasetLabel"],
                "datasetName": ind_ds["datasetName"],
                "datasetType": ind_ds["datasetType"],
                "displayFields": [dimension_field, indicator_field],
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
            "orderType": "desc",
        }

        # 计算画布中心位置
        canvas_width = 1920
        canvas_height = 1080
        center_left = (canvas_width - width) // 2
        center_top = (canvas_height - height) // 2

        # 如果指定了坐标则使用指定的坐标，否则使用中心位置
        layer_top = top if top is not None else center_top
        layer_left = left if left is not None else center_left

        # 构建完整的配置
        config = {
            "name": name,
            "config": {
                "theme": "lgScreenDefault",
                "style": {
                    "fontFamily": "default",
                    "cardBorderRadius": 6,
                    "panelBackgroundImage": "",
                    "panelBackgroundImageRepeat": "cover",
                    "cardBackgroundImage": "",
                    "cardBackgroundImageRepeat": "cover",
                    "titleColor": "#FEFEFE",
                    "textColor": "#A6ADD0",
                    "cardBackgroundColor": "rgba(13, 24, 44, 1.0)",
                    "panelBackgroundColor": "#000",
                    "lineColor": "#313358",
                    "linkColor": "#177DDC",
                    "colorSystem": "dark",
                    "graColorSystemCustomColors": [
                        "linear-gradient( 180deg, #2897FF 0%, #0049DA 100%)",
                        "linear-gradient( 180deg, #00F5FF 0%, #035EB9 100%)",
                    ],
                },
                "page": {"windowFlex": "WidthResponsive"},
                "canvas": {
                    "canvasWidth": canvas_width,
                    "canvasHeight": canvas_height,
                    "canvasSize": 1,
                    "canvasRatioLocked": False,
                    "canvasRatio": "",
                },
                "timeSwitch": {"timeSwitchUnit": "second", "timeSwitchTimer": 30},
                "previewSetting": {"previewSettingType": "actualSize"},
                "layers": [
                    {
                        "uuid": screen_uuid,
                        "top": layer_top,
                        "left": layer_left,
                        "width": width,
                        "height": height,
                    }
                ],
            },
            "layouts": [
                {
                    "uuid": screen_uuid,
                    "title": "柱图 1" if chart_type == "bar" else f"{chart_type}图 1",
                    "type": chart_type,
                    "icon": "chart_vertical_bar.png"
                    if chart_type == "bar"
                    else f"chart_{chart_type}.png",
                    "groupLabel": "图形组件",
                    "gridData": {},
                    "resizeHandles": ["s", "e", "se"],
                }
            ],
            "componentMap": {
                screen_uuid: {
                    "modelId": model_id,
                    "modelInfo": [
                        {
                            "datasetId": dim_ds["datasetId"],
                            "datasetLabel": dim_ds["datasetLabel"],
                            "datasetName": dim_ds["datasetName"],
                            "datasetType": dim_ds["datasetType"],
                            "displayFields": [dimension_field, indicator_field],
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
                    "key": screen_uuid,
                    "viewName": dimension["newFieldLabel"] + "分析",
                    "parentUuid": "",
                    "tabName": "",
                    "styleJson": self.get_chart_style_json(
                        chart_type=chart_type,
                        left=layer_left,
                        top=layer_top,
                        width=width,
                        height=height,
                        view_name=dimension["newFieldLabel"] + "分析",
                    ),
                    "dimensions": [dimension],
                    "indicators": [indicator],
                    "limit": {"isSelect": True, "errText": "", "value": 10},
                }
            },
            "topLayouts": [],
        }

        return config

    def _create_head_screen_config(
        self,
        name: str,
        screen_uuid: str,
        width: int = 1920,
        height: int = 80,
        top: int = 0,
        left: int = 0,
    ) -> Dict:
        """创建头部组件大屏配置（只包含头部装饰和标题文本）"""
        canvas_width = 1920
        canvas_height = 1080

        head_uuid = screen_uuid
        text_uuid = f"grid-type:text-uuid:{int(time.time() * 1000) + 1}"

        config = {
            "name": name,
            "config": {
                "theme": "lgScreenDefault",
                "style": {
                    "fontFamily": "default",
                    "cardBorderRadius": 6,
                    "panelBackgroundImage": "",
                    "panelBackgroundImageRepeat": "cover",
                    "cardBackgroundImage": "",
                    "cardBackgroundImageRepeat": "cover",
                    "titleColor": "#FEFEFE",
                    "textColor": "#A6ADD0",
                    "cardBackgroundColor": "rgba(13, 24, 44, 1.0)",
                    "panelBackgroundColor": "#000",
                    "lineColor": "#313358",
                    "linkColor": "#177DDC",
                    "colorSystem": "dark",
                    "graColorSystemCustomColors": [
                        "linear-gradient( 180deg, #2897FF 0%, #0049DA 100%)",
                        "linear-gradient( 180deg, #00F5FF 0%, #035EB9 100%)",
                    ],
                },
                "page": {"windowFlex": "WidthResponsive"},
                "canvas": {
                    "canvasWidth": canvas_width,
                    "canvasHeight": canvas_height,
                    "canvasSize": 1,
                    "canvasRatioLocked": False,
                    "canvasRatio": "",
                },
                "timeSwitch": {"timeSwitchUnit": "second", "timeSwitchTimer": 30},
                "previewSetting": {"previewSettingType": "actualSize"},
                "layers": [
                    {
                        "uuid": head_uuid,
                        "top": top,
                        "left": left,
                        "width": width,
                        "height": height,
                    },
                    {
                        "uuid": text_uuid,
                        "top": 20,
                        "left": 760,
                        "width": 400,
                        "height": 50,
                    },
                ],
            },
            "layouts": [
                {
                    "uuid": head_uuid,
                    "title": "头部 1",
                    "type": "head",
                    "icon": "chart_head_component.png",
                    "groupLabel": "装饰组件",
                    "gridData": {},
                    "resizeHandles": ["s", "e", "se"],
                },
                {
                    "uuid": text_uuid,
                    "title": name,
                    "type": "text",
                    "icon": "chart_text_component.png",
                    "groupLabel": "图形组件",
                    "gridData": {},
                    "resizeHandles": ["s", "e", "se"],
                },
            ],
            "componentMap": {
                head_uuid: {
                    "modelId": 0,
                    "modelInfo": [],
                    "key": head_uuid,
                    "viewName": "头部 1",
                    "parentUuid": "",
                    "tabName": "",
                    "styleJson": {
                        "screenPosition": {
                            "position": {"x": left, "y": top, "w": width, "h": height}
                        },
                        "decorateStyle": {
                            "selectedDecorate": "headDecorate/headDecorate4.png"
                        },
                        "decorate": {},
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
                            "border": "transparent",
                            "padding": 20,
                            "cardBackgroundColor": "",
                            "lineWidthMap": {"width": 1, "style": "solid"},
                        },
                    },
                    "dimensions": [],
                    "indicators": [],
                    "limit": {"isSelect": True, "errText": "", "value": 10},
                },
                text_uuid: {
                    "modelId": 0,
                    "modelInfo": [],
                    "key": text_uuid,
                    "viewName": name,
                    "parentUuid": "",
                    "tabName": "",
                    "styleJson": {
                        "screenPosition": {
                            "position": {"x": 760, "y": 20, "w": 400, "h": 50}
                        },
                        "content": {
                            "textContent": name,
                            "textSetMap": {
                                "fontSize": 28,
                                "textColor": "#FEFEFE",
                                "textBold": True,
                                "textItalic": False,
                                "align": "center",
                            },
                        },
                        "title": {
                            "isExtra": True,
                            "show": False,
                            "textSetMap": {
                                "fontSize": 16,
                                "textColor": "#FEFEFE",
                                "textBold": False,
                                "textItalic": False,
                            },
                        },
                        "card": {
                            "border": "transparent",
                            "padding": 0,
                            "cardBackgroundColor": "",
                            "lineWidthMap": {"width": 1, "style": "solid"},
                        },
                    },
                    "dimensions": [],
                    "indicators": [],
                    "limit": {"isSelect": True, "errText": "", "value": 10},
                },
            },
            "topLayouts": [],
        }

        return config

    def create_screen(self, config: Dict) -> int:
        """创建大屏"""
        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/addAll"
        response = post(url, json=config, headers=self.headers, cookies=self.cookies)
        data = response.json()

        if data.get("result") == "0":
            return data["data"]["id"]
        raise Exception(f"创建大屏失败：{data.get('desc')}")

    def get_screen_info(self, screen_id: int) -> Dict:
        """获取大屏详情"""
        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/detail/{screen_id}"
        response = get(url, headers=self.headers, cookies=self.cookies)
        data = response.json()

        if data.get("result") == "0":
            return data.get("data", {})
        raise Exception(f"获取大屏信息失败：{data.get('desc')}")

    def update_screen(self, screen_id: int, config: Dict) -> bool:
        """更新大屏配置"""
        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/update/{screen_id}"
        response = post(url, json=config, headers=self.headers, cookies=self.cookies)
        data = response.json()

        if data.get("result") == "0":
            return True
        raise Exception(f"更新大屏失败：{data.get('desc')}")

    def get_chart_style_json(
        self,
        chart_type: str,
        left: int,
        top: int,
        width: int,
        height: int,
        view_name: Optional[str] = None,
    ) -> Dict:
        """获取图表特定的样式配置"""

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
            "legend": {
                "isExtra": True,
                "position": "top",
                "textSetMap": {
                    "size": 14,
                    "fontSize": 14,
                    "textColor": "#177DDC",
                    "textBold": False,
                    "textItalic": False,
                },
            },
            "tooltip": {
                "isExtra": True,
                "content": ["dimension", "measure"],
                "backgroundColor": "#303467",
                "textSetMap": {
                    "size": 14,
                    "fontSize": 14,
                    "textColor": "#A6ADD0",
                    "textBold": False,
                    "textItalic": False,
                },
            },
            "drawSettings": {
                "seriesType": chart_type,
                "widthMap": {"isAdaption": True},
                "gridSet": {
                    "isAdaption": True,
                    "gridLeft": None,
                    "gridTop": None,
                    "gridBottom": None,
                    "gridRight": None,
                },
            },
            "axis": {
                "x": {
                    "axes": ["showXAxis"],
                    "scale": "auto",
                    "rotate": 0,
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
            "label": {
                "isExtra": True,
                "position": "auto",
                "textSetMap": {
                    "size": 14,
                    "fontSize": 14,
                    "textColor": "#A6ADD0",
                    "textBold": False,
                    "textItalic": False,
                },
            },
            "scroll": {
                "isExtra": True,
                "show": False,
                "type": "highlight",
                "cycleSpeed": 5,
                "color": "#63c8ff",
                "dimensionNum": 5,
                "scrollSpeed": 5,
            },
            "textData": {"isExtra": True, "show": False, "content": []},
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
                    "border": "transparent",
                    "padding": 20,
                    "cardBackgroundColor": "",
                    "lineWidthMap": {"width": 1, "style": "solid"},
                },
            }

        # 饼图特定样式
        if chart_type == "pie":
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
                    "position": "bottom",
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
                    "outerRadius": 80,
                    "type": "default",
                    "innerRadius": 60,
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
                    "position": "outside",
                    "content": ["dimension", "measure", "percent"],
                },
                "title": {
                    "isExtra": True,
                    "show": True,
                    "textSetMap": {
                        "textItalic": False,
                        "textBold": True,
                        "fontSize": 16,
                        "align": "center",
                        "textColor": "#FEFEFE",
                    },
                    "title": view_name or "饼图",
                },
                "card": {
                    "border": "transparent",
                    "padding": 16,
                    "cardBackgroundColor": "",
                    "lineWidthMap": {"width": 1, "style": "solid"},
                },
            }

        return base_style


def main():
    parser = argparse.ArgumentParser(description="创建 BI 大屏（默认只带头部装饰组件）")
    parser.add_argument("--name", required=True, help="大屏名称")
    parser.add_argument("--model-id", type=int, help="数据模型 ID")
    parser.add_argument("--dimension-field", help="维度字段名")
    parser.add_argument("--indicator-field", help="指标字段名")
    parser.add_argument("--width", type=int, default=960, help="组件宽度")
    parser.add_argument("--height", type=int, default=540, help="组件高度")
    parser.add_argument(
        "--chart-type",
        default="head",
        choices=["bar", "line", "pie", "indicator", "map", "head"],
        help="图表类型（默认 head，只创建带头部组件的空大屏）",
    )
    parser.add_argument(
        "--period-type",
        default=None,
        choices=["month", "quarter", "year"],
        help="周期类型（用于时间字段分组）",
    )
    parser.add_argument("--base-url", default=get_base_url(), help="API 基础 URL")
    parser.add_argument(
        "--env",
        default="dev",
        choices=["dev", "test", "prod"],
        help="环境 (默认 dev，与 --base-url 二选一)",
    )

    args = parser.parse_args()

    # 验证必需参数
    if args.chart_type != "head":
        if not args.model_id or not args.dimension_field or not args.indicator_field:
            print(
                "❌ 错误：创建带组件的大屏需要指定 --model-id, --dimension-field, --indicator-field"
            )
            return 1

    # 优先使用 --base-url，否则用 --env
    base_url = args.base_url if args.base_url else get_base_url(args.env)
    creator = BiScreenCreator(base_url)

    try:
        if args.chart_type == "head":
            config = creator.create_screen_config(
                name=args.name,
                model_id=0,
                model_info={},
                dimension_field="",
                indicator_field="",
                width=1920,
                height=80,
                chart_type="head",
                top=0,
                left=0,
            )
        else:
            # 获取模型信息
            print(f"正在获取模型信息 (ID: {args.model_id})...")
            model_info = _get_model_info(
                args.model_id, creator.base_url, creator.headers
            )
            print(f"模型名称：{model_info.get('modelDTO', {}).get('name', 'Unknown')}")

            # 构建配置
            print("正在构建大屏配置...")
            config = creator.create_screen_config(
                name=args.name,
                model_id=args.model_id,
                model_info=model_info,
                dimension_field=args.dimension_field,
                indicator_field=args.indicator_field,
                width=args.width,
                height=args.height,
                chart_type=args.chart_type,
                period_type=args.period_type,
            )

        # 创建大屏
        print("正在创建大屏...")
        screen_id = creator.create_screen(config)
        print(f"✅ 大屏创建成功!")
        print(f"大屏 ID: {screen_id}")
        print(f"访问 URL: {get_preview_url(screen_id, base_url)}")

    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
