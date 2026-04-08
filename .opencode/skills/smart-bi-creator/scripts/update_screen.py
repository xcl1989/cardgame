#!/usr/bin/env python3
"""
更新大屏配置脚本 - 支持多组件操作和样式更新
使用方式：
1. 位置/大小更新：python3 scripts/update_screen.py --screen-id xxx --uuid xxx --top 100 --left 200
2. 样式复制：python3 scripts/update_screen.py --screen-id xxx --clone-style-from uuid1 --clone-style-to uuid2 uuid3 ...
3. 查看详情：python3 scripts/update_screen.py --screen-id xxx --show-info
4. 设置背景图：python3 scripts/update_screen.py --screen-id xxx --set-background /path/to/image.png
"""

import json
import requests
from pathlib import Path
from typing import Dict, Optional, List
import copy
import time
import hashlib

from auth import (
    load_headers,
    get_preview_url,
    get_base_url,
    get_retry,
    post_retry,
    screen_cache_get,
    screen_cache_set,
)


class BiScreenUpdater:
    """BI 大屏更新器"""

    def __init__(self, base_url: str = "https://dev.cloud.hecom.cn"):
        self.base_url = base_url
        self.headers = load_headers()
        self.cookies = {}

    def get_screen(self, screen_id: int, use_cache: bool = True) -> Dict:
        """获取大屏配置（使用 /get/{screen_id} API）

        Args:
            screen_id: 大屏 ID
            use_cache: 是否使用本地缓存（默认 True，更新操作建议传 False）
        """
        if use_cache:
            cached = screen_cache_get(screen_id)
            if cached is not None:
                print(f"使用缓存的大屏配置 (ID: {screen_id})")
                return cached

        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/get/{screen_id}"
        response = get_retry(url, headers=self.headers, cookies=self.cookies)
        data = response.json()

        if data.get("result") == "0":
            result = data.get("data", {})
            if use_cache:
                screen_cache_set(screen_id, result)
            return result
        raise Exception(f"获取大屏失败：{data.get('desc')}")

    def update_screen(self, screen_id: int, config: Dict) -> bool:
        """更新大屏配置（使用 /update/{screen_id} API）"""
        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/update/{screen_id}"
        response = post_retry(
            url, json=config, headers=self.headers, cookies=self.cookies
        )
        data = response.json()

        if data.get("result") == "0":
            return True
        raise Exception(f"更新大屏失败：{data.get('desc')}")

    def print_screen_info(self, screen_data: Dict, show_style: bool = False):
        """打印大屏信息

        Args:
            screen_data: 大屏配置数据
            show_style: 是否显示样式详情
        """
        print(f"\n=== 大屏基本信息 ===")
        print(f"名称：{screen_data.get('name')}")
        print(f"ID: {screen_data.get('id')}")

        config = screen_data.get("config", {})
        layers = config.get("layers", [])
        print(f"\n=== 图层数量：{len(layers)} ===")

        for i, layer in enumerate(layers, 1):
            print(f"\n图层{i}: {layer.get('title')} ({layer.get('type')})")
            print(f"  UUID: {layer.get('uuid')}")
            print(f"  位置：top={layer.get('top')}, left={layer.get('left')}")
            print(f"  大小：width={layer.get('width')}, height={layer.get('height')}")

        component_map = screen_data.get("componentMap", {})
        print(f"\n=== 数据组件数量：{len(component_map)} ===")

        for uuid, comp in component_map.items():
            model_id = comp.get("modelId")
            view_name = comp.get("viewName", "")
            comp_type = comp.get("type", "unknown")
            dimensions = comp.get("dimensions", [])
            indicators = comp.get("indicators", [])
            style_json = comp.get("styleJson", {})

            if comp_type in ["text", "decorate", "time", "marquee", "script"]:
                continue  # 跳过无数据组件

            # 获取指标卡关键样式
            metric_info = ""
            if "metric" in uuid and style_json:
                card_bg = style_json.get("card", {}).get("cardBackgroundColor", "")
                value_color = (
                    style_json.get("metricValue", {})
                    .get("textSetMap", {})
                    .get("textColor", "")
                )
                metric_info = f" [背景:{card_bg[:30]}... 数值色:{value_color}]"

            print(f"\n组件：{view_name} ({comp_type}){metric_info}")
            print(f"  UUID: {uuid}")
            print(f"  模型 ID: {model_id}")
            if dimensions:
                print(f"  维度：{[d.get('fieldName') for d in dimensions]}")
            if indicators:
                print(f"  指标：{[i.get('fieldName') for i in indicators]}")

            if show_style and style_json:
                print(
                    f"  样式JSON: {json.dumps(style_json, ensure_ascii=False)[:200]}..."
                )

    def update_component_position(
        self,
        screen_id: int,
        uuid: str,
        top: Optional[int] = None,
        left: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        name: Optional[str] = None,
    ) -> bool:
        """更新指定组件的位置/大小"""
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": name if name else screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        found = False
        if "layers" in config["config"]:
            for layer in config["config"]["layers"]:
                if layer.get("uuid") == uuid:
                    if top is not None:
                        layer["top"] = top
                    if left is not None:
                        layer["left"] = left
                    if width is not None:
                        layer["width"] = width
                    if height is not None:
                        layer["height"] = height
                    found = True
                    print(f"修改图层位置：uuid={uuid}")
                    print(f"  新位置：top={layer.get('top')}, left={layer.get('left')}")
                    print(
                        f"  新大小：width={layer.get('width')}, height={layer.get('height')}"
                    )
                    break

        if not found:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        if uuid in config["componentMap"]:
            comp = config["componentMap"][uuid]
            if "styleJson" in comp and "screenPosition" in comp["styleJson"]:
                pos = comp["styleJson"]["screenPosition"]["position"]
                if top is not None:
                    pos["y"] = top
                if left is not None:
                    pos["x"] = left
                if width is not None:
                    pos["w"] = width
                if height is not None:
                    pos["h"] = height
                print(f"同步更新组件样式配置")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def clone_component_style(
        self,
        screen_id: int,
        source_uuid: str,
        target_uuids: List[str],
    ) -> bool:
        """复制组件样式

        Args:
            screen_id: 大屏 ID
            source_uuid: 样式来源组件的 UUID
            target_uuids: 要应用样式的目标组件 UUID 列表
        """
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if source_uuid not in component_map:
            raise Exception(f"未找到来源组件：{source_uuid}")

        source_comp = component_map[source_uuid]
        source_style = source_comp.get("styleJson", {})

        print(f"复制样式：{source_uuid} -> {target_uuids}")
        for target_uuid in target_uuids:
            if target_uuid not in component_map:
                print(f"  警告：未找到目标组件 {target_uuid}，跳过")
                continue

            target_comp = component_map[target_uuid]
            target_comp["styleJson"] = json.loads(json.dumps(source_style))
            print(f"  已复制到：{target_uuid}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def upload_image_to_obs(self, local_path: str) -> str:
        """上传本地图片到 OBS 并返回 URL

        Args:
            local_path: 本地图片路径

        Returns:
            OBS 上的图片 URL
        """
        import uuid
        from datetime import datetime

        if not Path(local_path).exists():
            raise Exception(f"图片文件不存在：{local_path}")

        with open(local_path, "rb") as f:
            image_data = f.read()

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"backgrounds/bg_{timestamp}_{uuid.uuid4().hex[:8]}.png"
        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/upload"

        files = {"file": (filename, image_data, "image/png")}
        response = post_retry(
            url, files=files, headers=self.headers, cookies=self.cookies
        )

        data = response.json()
        if data.get("result") == "0" or data.get("code") == "0":
            return data.get("data", {}).get("url", "")
        raise Exception(f"图片上传失败：{data.get('desc') or data.get('msg')}")

    def set_background_image(
        self,
        screen_id: int,
        local_image_path: str,
    ) -> bool:
        """设置大屏背景图片

        Args:
            screen_id: 大屏 ID
            local_image_path: 本地图片路径
        """
        print(f"正在上传图片...")
        image_url = self._upload_image_to_obs_huawei(local_image_path)
        print(f"图片 URL：{image_url}")

        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        style = config["config"].get("style", {})
        style["panelBackgroundImage"] = image_url
        style["panelBackgroundImageRepeat"] = "cover"
        config["config"]["style"] = style
        print(f"正在更新大屏...")

        self.update_screen(screen_id, config)
        return True

    def _upload_image_to_obs_huawei(self, local_path: str) -> str:
        """上传本地图片到华为云 OBS 并返回 CDN URL

        Args:
            local_path: 本地图片路径

        Returns:
            CDN 上的图片 URL
        """
        from obs import ObsClient

        image_file = Path(local_path)
        if not image_file.exists():
            raise Exception(f"图片文件不存在：{local_path}")

        file_size = image_file.stat().st_size
        file_name = image_file.name
        timestamp = int(time.time() * 1000)

        canvas_width = 1920
        canvas_height = 1080
        name_parts = file_name.rsplit(".", 1)
        if len(name_parts) == 2:
            new_name = f"bg{canvas_width}x{canvas_height}{timestamp}.{name_parts[1]}"
        else:
            new_name = f"bg{canvas_width}x{canvas_height}{timestamp}.png"

        script_dir = Path(__file__).parent
        config_file = script_dir / "header.json"

        with open(config_file, "r", encoding="utf-8") as f:
            header = json.load(f)
        headers = {k: v for k, v in header.items() if k != "Content-Type"}

        get_param_url = (
            f"{self.base_url}/universe/paas/settings/getFileUploadParamBySize"
        )
        get_param_data = {
            "fileName": new_name,
            "fileSize": file_size,
            "bucket": "hwtest-image-public",
            "originalFileName": file_name,
        }
        response = post_retry(
            get_param_url,
            json=get_param_data,
            headers=headers,
        )
        result = response.json()

        if result.get("result") != "0":
            raise Exception(f"获取上传参数失败：{result.get('desc')}")

        upload_params = result.get("data", {})
        access_key_id = upload_params.get("accessKeyId")
        access_key_secret = upload_params.get("accessKeySecret")
        object_key = upload_params.get("objectKey")
        security_token = upload_params.get("securityToken")

        if not all([access_key_id, access_key_secret, object_key, security_token]):
            raise Exception("上传参数不完整，缺少必要的认证信息")

        print(f"正在上传图片到 OBS...")
        obs_client = ObsClient(
            access_key_id=access_key_id,
            secret_access_key=access_key_secret,
            server="obs.cn-north-4.myhuaweicloud.com",
            security_token=security_token,
        )

        with open(image_file, "rb") as f:
            file_content = f.read()

        resp = obs_client.putContent(
            "hwtest-image-public",
            object_key,
            content=file_content,
        )

        if resp.status is not None and resp.status >= 300:
            raise Exception(f"上传失败：{resp.errorCode} - {resp.errorMessage}")

        print(f"图片上传成功")
        return f"https://hwtest-image-public.cloud.hecom.cn/{object_key}"

    def update_decorate_index(
        self,
        screen_id: int,
        uuid: str,
        decorate_index: int,
    ) -> bool:
        """更新组件的装饰图片编号

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            decorate_index: 装饰图片编号（1-14）
        """
        if decorate_index < 1 or decorate_index > 14:
            raise Exception(f"装饰编号无效：{decorate_index}，有效范围 1-14")

        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        style_json = comp.get("styleJson", {})

        if "decorateStyle" not in style_json:
            raise Exception(f"组件没有 decorateStyle 配置，无法更新装饰图片")

        old_decorate = style_json["decorateStyle"].get("selectedDecorate", "")

        type_map = {
            "squareDecorate": "squareDecorate",
            "barDecorate": "barDecorate",
            "baseDecorate": "baseDecorate",
            "headDecorate": "headDecorate",
        }

        new_decorate = None
        for prefix, folder in type_map.items():
            if old_decorate.startswith(prefix):
                new_decorate = f"{folder}/{folder}{decorate_index}.png"
                break

        if new_decorate is None:
            raise Exception(f"无法解析当前装饰类型：{old_decorate}")

        style_json["decorateStyle"]["selectedDecorate"] = new_decorate
        print(f"更新装饰图片：{old_decorate} -> {new_decorate}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_line_type(
        self,
        screen_id: int,
        uuid: str,
        line_type: str,
    ) -> bool:
        """更新线图的线条类型

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            line_type: 线条类型（line:折线，curve:曲线）
        """
        if line_type not in ["line", "curve"]:
            raise Exception(f"线条类型无效：{line_type}，有效值 line 或 curve")

        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        style_json = comp.get("styleJson", {})

        if "drawSettings" not in style_json:
            raise Exception(f"组件没有 drawSettings 配置，无法更新线条类型")

        old_line_type = style_json["drawSettings"].get("lineType", "curve")
        style_json["drawSettings"]["lineType"] = line_type
        print(f"更新线条类型：{old_line_type} -> {line_type}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_dimension_order(
        self,
        screen_id: int,
        uuid: str,
        order_type: str,
    ) -> bool:
        """更新组件的维度排序

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            order_type: 排序类型（asc:升序，desc:降序，none:清除排序）
        """
        if order_type not in ["asc", "desc", "none"]:
            raise Exception(f"排序类型无效：{order_type}，有效值 asc/desc/none")

        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        dimensions = comp.get("dimensions", [])
        if not dimensions:
            raise Exception(f"组件没有维度配置")

        old_order = dimensions[0].get("orderType", "desc")
        if order_type == "none":
            for dim in dimensions:
                if "orderType" in dim:
                    del dim["orderType"]
            print(f"清除维度排序：{old_order} -> none")
        else:
            for dim in dimensions:
                dim["orderType"] = order_type
            print(f"更新维度排序：{old_order} -> {order_type}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_indicator_order(
        self,
        screen_id: int,
        uuid: str,
        order_type: str,
    ) -> bool:
        """更新组件的指标排序

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            order_type: 排序类型（asc:升序，desc:降序，none:清除排序）
        """
        if order_type not in ["asc", "desc", "none"]:
            raise Exception(f"排序类型无效：{order_type}，有效值 asc/desc/none")

        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        indicators = comp.get("indicators", [])
        if not indicators:
            raise Exception(f"组件没有指标配置")

        old_order = indicators[0].get("orderType", "desc")
        if order_type == "none":
            for ind in indicators:
                if "orderType" in ind:
                    del ind["orderType"]
            print(f"清除指标排序：{old_order} -> none")
        else:
            for ind in indicators:
                ind["orderType"] = order_type
            print(f"更新指标排序：{old_order} -> {order_type}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_indicator_label(
        self,
        screen_id: int,
        uuid: str,
        indicator_label: str,
    ) -> bool:
        """更新组件的指标显示名称

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            indicator_label: 新的指标显示名称（如"本月收款金额"）
        """
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        indicators = comp.get("indicators", [])
        if not indicators:
            raise Exception(f"组件没有指标配置")

        old_label = indicators[0].get("newFieldLabel", "")
        for ind in indicators:
            ind["newFieldLabel"] = indicator_label
        print(f"更新指标显示名称：{old_label} -> {indicator_label}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_metric_style(
        self,
        screen_id: int,
        uuid: str,
        metric_style: str,
    ) -> bool:
        """更新指标卡的样式预设

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            metric_style: 样式预设（default/top/icon_left/icon_follow/gradient/light/minimal/card）
        """
        valid_styles = [
            "default",
            "top",
            "icon_left",
            "icon_follow",
            "gradient",
            "light",
            "minimal",
            "card",
        ]
        if metric_style not in valid_styles:
            raise Exception(f"指标卡样式无效：{metric_style}，有效值 {valid_styles}")

        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        style_json = comp.get("styleJson", {})

        if "drawSettings" not in style_json:
            raise Exception(f"组件没有 drawSettings 配置")

        old_style = style_json["drawSettings"].get("position", "default")
        style_json["drawSettings"]["position"] = metric_style
        print(f"更新指标卡样式：{old_style} -> {metric_style}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_metric_label_visible(
        self,
        screen_id: int,
        uuid: str,
        visible: bool,
    ) -> bool:
        """更新指标卡的标签可见性

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            visible: 是否显示标签
        """
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        style_json = comp.get("styleJson", {})

        if "metricName" not in style_json:
            raise Exception(f"组件没有 metricName 配置")

        old_visible = style_json["metricName"].get("isExtra", True)
        style_json["metricName"]["isExtra"] = visible
        print(f"更新指标卡标签可见性：{old_visible} -> {visible}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_text_font_size(
        self,
        screen_id: int,
        uuid: str,
        font_size: int,
    ) -> bool:
        """更新文本组件的字体大小

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            font_size: 字体大小
        """
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        style_json = comp.get("styleJson", {})

        if "textSetMap" not in style_json:
            raise Exception(f"组件没有 textSetMap 配置")

        old_size = style_json["textSetMap"].get("fontSize", 14)
        style_json["textSetMap"]["fontSize"] = font_size
        print(f"更新文本字体大小：{old_size} -> {font_size}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_text_align(
        self,
        screen_id: int,
        uuid: str,
        align: str,
    ) -> bool:
        """更新文本组件的对齐方式

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            align: 对齐方式（left/center/right）
        """
        if align not in ["left", "center", "right"]:
            raise Exception(f"对齐方式无效：{align}，有效值 left/center/right")

        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        style_json = comp.get("styleJson", {})

        if "title" not in style_json or "textSetMap" not in style_json.get("title", {}):
            raise Exception(f"组件没有 title.textSetMap 配置")

        old_align = style_json["title"]["textSetMap"].get("align", "center")
        style_json["title"]["textSetMap"]["align"] = align
        print(f"更新文本对齐方式：{old_align} -> {align}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_time_font_size(
        self,
        screen_id: int,
        uuid: str,
        font_size: int,
    ) -> bool:
        """更新时间组件的字体大小

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            font_size: 字体大小
        """
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        style_json = comp.get("styleJson", {})

        if "cardSet" not in style_json or "textSetMap" not in style_json.get(
            "cardSet", {}
        ):
            raise Exception(f"组件没有 cardSet.textSetMap 配置")

        old_size = style_json["cardSet"]["textSetMap"].get("fontSize", 24)
        style_json["cardSet"]["textSetMap"]["fontSize"] = font_size
        if "title" in style_json and "textSetMap" in style_json.get("title", {}):
            style_json["title"]["textSetMap"]["fontSize"] = font_size
        print(f"更新时间组件字体大小：{old_size} -> {font_size}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_time_color(
        self,
        screen_id: int,
        uuid: str,
        color: str,
    ) -> bool:
        """更新时间组件的文字颜色

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            color: 文字颜色（如 #A6ADD0）
        """
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        style_json = comp.get("styleJson", {})

        if "cardSet" not in style_json or "textSetMap" not in style_json.get(
            "cardSet", {}
        ):
            raise Exception(f"组件没有 cardSet.textSetMap 配置")

        old_color = style_json["cardSet"]["textSetMap"].get("textColor", "#A6ADD0")
        style_json["cardSet"]["textSetMap"]["textColor"] = color
        if "title" in style_json and "textSetMap" in style_json.get("title", {}):
            style_json["title"]["textSetMap"]["textColor"] = color
        print(f"更新时间组件文字颜色：{old_color} -> {color}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_time_format(
        self,
        screen_id: int,
        uuid: str,
        time_type: str = "dateAndTime",
        date_format: str = "yyyy-MM-dd",
        time_format: str = "hh:mm:ss",
    ) -> bool:
        """更新时间组件的格式

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            time_type: 时间类型（dateAndTime/date/time）
            date_format: 日期格式（如 yyyy-MM-dd）
            time_format: 时间格式（如 hh:mm:ss）
        """
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        style_json = comp.get("styleJson", {})

        if "timeType" not in style_json:
            raise Exception(f"组件没有 timeType 配置")

        old_type = style_json["timeType"].get("type", "dateAndTime")
        old_date = style_json["timeType"].get("date", "yyyy-MM-dd")
        old_time = style_json["timeType"].get("time", "hh:mm:ss")
        style_json["timeType"]["type"] = time_type
        style_json["timeType"]["date"] = date_format
        style_json["timeType"]["time"] = time_format
        print(f"更新时间组件格式：")
        print(f"  类型：{old_type} -> {time_type}")
        print(f"  日期格式：{old_date} -> {date_format}")
        print(f"  时间格式：{old_time} -> {time_format}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_script_code(
        self,
        screen_id: int,
        uuid: str,
        script_code: str,
    ) -> bool:
        """更新脚本组件的代码

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            script_code: JavaScript 代码
        """
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        style_json = comp.get("styleJson", {})

        old_code = style_json.get("script", "")
        style_json["script"] = script_code
        print(f"更新脚本代码，长度：{len(old_code)} -> {len(script_code)}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_table_style(
        self,
        screen_id: int,
        uuid: str,
        body_font_size: Optional[int] = None,
        body_text_color: Optional[str] = None,
        body_bold: Optional[bool] = None,
        header_bg_color: Optional[str] = None,
        header_font_size: Optional[int] = None,
        header_text_color: Optional[str] = None,
        header_bold: Optional[bool] = None,
        odd_row_color: Optional[str] = None,
        even_row_color: Optional[str] = None,
        row_split_line_color: Optional[str] = None,
        row_split_line_size: Optional[int] = None,
        col_split_line_color: Optional[str] = None,
        col_split_line_size: Optional[int] = None,
        scroll_show: Optional[bool] = None,
        scroll_speed: Optional[int] = None,
    ) -> bool:
        """更新表格组件的样式

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            body_font_size: 表格内容字体大小
            body_text_color: 表格内容文字颜色
            body_bold: 表格内容是否加粗
            header_bg_color: 表头背景色
            header_font_size: 表头字体大小
            header_text_color: 表头文字颜色
            header_bold: 表头是否加粗
            odd_row_color: 奇数行背景色
            even_row_color: 偶数行背景色
            row_split_line_color: 行分割线颜色
            row_split_line_size: 行分割线宽度
            col_split_line_color: 列分割线颜色
            col_split_line_size: 列分割线宽度
            scroll_show: 是否显示滚动
            scroll_speed: 滚动速度
        """
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        style_json = comp.get("styleJson", {})

        updates = []

        # tableBodySettings
        if "tableBodySettings" not in style_json:
            style_json["tableBodySettings"] = {}
        body_settings = style_json["tableBodySettings"]

        if body_font_size is not None:
            old_val = body_settings.get("textSetMap", {}).get("fontSize", 14)
            if "textSetMap" not in body_settings:
                body_settings["textSetMap"] = {}
            body_settings["textSetMap"]["fontSize"] = body_font_size
            updates.append(f"表格内容字体大小: {old_val} -> {body_font_size}")

        if body_text_color is not None:
            old_val = body_settings.get("textSetMap", {}).get("textColor", "#DBDFF1")
            if "textSetMap" not in body_settings:
                body_settings["textSetMap"] = {}
            body_settings["textSetMap"]["textColor"] = body_text_color
            updates.append(f"表格内容文字颜色: {old_val} -> {body_text_color}")

        if body_bold is not None:
            old_val = body_settings.get("textSetMap", {}).get("textBold", False)
            if "textSetMap" not in body_settings:
                body_settings["textSetMap"] = {}
            body_settings["textSetMap"]["textBold"] = body_bold
            updates.append(f"表格内容加粗: {old_val} -> {body_bold}")

        if odd_row_color is not None:
            old_val = body_settings.get("oddNumberedColor", "#0A1E38")
            body_settings["oddNumberedColor"] = odd_row_color
            updates.append(f"奇数行背景色: {old_val} -> {odd_row_color}")

        if even_row_color is not None:
            old_val = body_settings.get("evenNumberedColor", "#020B1C")
            body_settings["evenNumberedColor"] = even_row_color
            updates.append(f"偶数行背景色: {old_val} -> {even_row_color}")

        if row_split_line_color is not None:
            old_val = body_settings.get("rowSplitLine", {}).get("color", "#334979")
            if "rowSplitLine" not in body_settings:
                body_settings["rowSplitLine"] = {}
            body_settings["rowSplitLine"]["color"] = row_split_line_color
            updates.append(f"行分割线颜色: {old_val} -> {row_split_line_color}")

        if row_split_line_size is not None:
            old_val = body_settings.get("rowSplitLine", {}).get("size", 1)
            if "rowSplitLine" not in body_settings:
                body_settings["rowSplitLine"] = {}
            body_settings["rowSplitLine"]["size"] = row_split_line_size
            updates.append(f"行分割线宽度: {old_val} -> {row_split_line_size}")

        if col_split_line_color is not None:
            old_val = body_settings.get("colSplitLine", {}).get("color", "#334979")
            if "colSplitLine" not in body_settings:
                body_settings["colSplitLine"] = {}
            body_settings["colSplitLine"]["color"] = col_split_line_color
            updates.append(f"列分割线颜色: {old_val} -> {col_split_line_color}")

        if col_split_line_size is not None:
            old_val = body_settings.get("colSplitLine", {}).get("size", 0)
            if "colSplitLine" not in body_settings:
                body_settings["colSplitLine"] = {}
            body_settings["colSplitLine"]["size"] = col_split_line_size
            updates.append(f"列分割线宽度: {old_val} -> {col_split_line_size}")

        # tableHeaderSettings
        if "tableHeaderSettings" not in style_json:
            style_json["tableHeaderSettings"] = {}
        header_settings = style_json["tableHeaderSettings"]

        if header_bg_color is not None:
            old_val = header_settings.get("bgColor", "#08143E")
            header_settings["bgColor"] = header_bg_color
            updates.append(f"表头背景色: {old_val} -> {header_bg_color}")

        if header_font_size is not None:
            old_val = header_settings.get("textSetMap", {}).get("fontSize", 12)
            if "textSetMap" not in header_settings:
                header_settings["textSetMap"] = {}
            header_settings["textSetMap"]["fontSize"] = header_font_size
            updates.append(f"表头字体大小: {old_val} -> {header_font_size}")

        if header_text_color is not None:
            old_val = header_settings.get("textSetMap", {}).get("textColor", "#DBDFF1")
            if "textSetMap" not in header_settings:
                header_settings["textSetMap"] = {}
            header_settings["textSetMap"]["textColor"] = header_text_color
            updates.append(f"表头文字颜色: {old_val} -> {header_text_color}")

        if header_bold is not None:
            old_val = header_settings.get("textSetMap", {}).get("textBold", True)
            if "textSetMap" not in header_settings:
                header_settings["textSetMap"] = {}
            header_settings["textSetMap"]["textBold"] = header_bold
            updates.append(f"表头加粗: {old_val} -> {header_bold}")

        # scroll
        if scroll_show is not None or scroll_speed is not None:
            if "scroll" not in style_json:
                style_json["scroll"] = {}
            scroll_settings = style_json["scroll"]

            if scroll_show is not None:
                old_val = scroll_settings.get("show", True)
                scroll_settings["show"] = scroll_show
                updates.append(f"滚动显示: {old_val} -> {scroll_show}")

            if scroll_speed is not None:
                old_val = scroll_settings.get("speed", 5)
                scroll_settings["speed"] = scroll_speed
                updates.append(f"滚动速度: {old_val} -> {scroll_speed}")

        if updates:
            print("更新表格样式：")
            for u in updates:
                print(f"  {u}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_flipper_style(
        self,
        screen_id: int,
        uuid: str,
        flipper_int_figure: Optional[int] = None,
        flipper_decimal_figure: Optional[int] = None,
        flipper_thousandth: Optional[bool] = None,
        flipper_style_type: Optional[str] = None,
        flipper_font_color: Optional[str] = None,
        flipper_fill_color: Optional[str] = None,
        flipper_border_color: Optional[str] = None,
        flipper_flip_gap: Optional[int] = None,
        flipper_font_size: Optional[int] = None,
    ) -> bool:
        """更新翻牌器组件的样式

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            flipper_int_figure: 整数位数
            flipper_decimal_figure: 小数位数
            flipper_thousandth: 是否显示千分位
            flipper_style_type: 样式类型（round/square）
            flipper_font_color: 字体颜色
            flipper_fill_color: 填充颜色
            flipper_border_color: 边框颜色
            flipper_flip_gap: 翻牌间隔
            flipper_font_size: 字体大小
        """
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        style_json = comp.get("styleJson", {})

        updates = []

        # drawSettings
        if "drawSettings" not in style_json:
            style_json["drawSettings"] = {}
        draw_settings = style_json["drawSettings"]

        if flipper_font_size is not None:
            old_val = draw_settings.get("fontSize", 34)
            draw_settings["fontSize"] = flipper_font_size
            updates.append(f"字体大小: {old_val} -> {flipper_font_size}")

        if flipper_style_type is not None:
            old_val = draw_settings.get("styleType", "round")
            draw_settings["styleType"] = flipper_style_type
            updates.append(f"样式类型: {old_val} -> {flipper_style_type}")

        if flipper_font_color is not None:
            old_val = draw_settings.get("fontColor", "")
            draw_settings["fontColor"] = flipper_font_color
            updates.append(
                f"字体颜色: {old_val[:50]}... -> {flipper_font_color[:50]}..."
            )

        if flipper_fill_color is not None:
            old_val = draw_settings.get("fillColor", "")
            draw_settings["fillColor"] = flipper_fill_color
            updates.append(
                f"填充颜色: {old_val[:50]}... -> {flipper_fill_color[:50]}..."
            )

        if flipper_border_color is not None:
            old_val = draw_settings.get("borderColor", "")
            draw_settings["borderColor"] = flipper_border_color
            updates.append(f"边框颜色: {old_val} -> {flipper_border_color}")

        if flipper_flip_gap is not None:
            old_val = draw_settings.get("flipGap", 12)
            draw_settings["flipGap"] = flipper_flip_gap
            updates.append(f"翻牌间隔: {old_val} -> {flipper_flip_gap}")

        # numberSet
        if "numberSet" not in style_json:
            style_json["numberSet"] = {}
        number_set = style_json["numberSet"]

        if flipper_int_figure is not None:
            old_val = number_set.get("intFigure", 8)
            number_set["intFigure"] = flipper_int_figure
            updates.append(f"整数位数: {old_val} -> {flipper_int_figure}")

        if flipper_decimal_figure is not None:
            old_val = number_set.get("decimalFigure", 2)
            number_set["decimalFigure"] = flipper_decimal_figure
            updates.append(f"小数位数: {old_val} -> {flipper_decimal_figure}")

        if flipper_thousandth is not None:
            old_val = number_set.get("thousandthPlace", "thousandthPlaceChecked")
            thousandth_value = (
                "thousandthPlaceChecked"
                if flipper_thousandth
                else "thousandthPlaceUnchecked"
            )
            number_set["thousandthPlace"] = thousandth_value
            updates.append(f"千分位: {old_val} -> {thousandth_value}")

        if updates:
            print("更新翻牌器样式：")
            for u in updates:
                print(f"  {u}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_radar_style(
        self,
        screen_id: int,
        uuid: str,
        radar_radius: Optional[int] = None,
        radar_legend_position: Optional[str] = None,
        radar_label_position: Optional[str] = None,
    ) -> bool:
        """更新雷达图组件的样式

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            radar_radius: 雷达半径
            radar_legend_position: 图例位置（top/bottom/left/right）
            radar_label_position: 标签位置（auto/top/bottom/left/right）
        """
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        style_json = comp.get("styleJson", {})

        updates = []

        # drawSettings
        if "drawSettings" not in style_json:
            style_json["drawSettings"] = {}
        draw_settings = style_json["drawSettings"]

        if radar_radius is not None:
            old_val = draw_settings.get("radius", 50)
            draw_settings["radius"] = radar_radius
            updates.append(f"雷达半径: {old_val} -> {radar_radius}")

        # legend
        if radar_legend_position is not None:
            if "legend" not in style_json:
                style_json["legend"] = {}
            old_val = style_json["legend"].get("position", "top")
            style_json["legend"]["position"] = radar_legend_position
            updates.append(f"图例位置: {old_val} -> {radar_legend_position}")

        # label
        if radar_label_position is not None:
            if "label" not in style_json:
                style_json["label"] = {}
            old_val = style_json["label"].get("position", "auto")
            style_json["label"]["position"] = radar_label_position
            updates.append(f"标签位置: {old_val} -> {radar_label_position}")

        if updates:
            print("更新雷达图样式：")
            for u in updates:
                print(f"  {u}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_component_linkage(
        self,
        screen_id: int,
        uuid: str,
        linkage: List[str],
    ) -> bool:
        """更新组件的联动配置

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            linkage: 联动目标组件 UUID 列表（传空列表 [] 则清除联动）
        """
        no_data_types = ["time", "text", "decorate", "head", "card", "icon"]

        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        comp_type = comp.get("type", "")
        dimensions = comp.get("dimensions", [])
        model_id = comp.get("modelId")

        if comp_type in no_data_types or not dimensions:
            raise Exception(
                f"只有设置了维度的组件才能联动其他组件（{uuid} 类型为 {comp_type} 或没有维度）"
            )

        if linkage:
            for target_uuid in linkage:
                if target_uuid not in component_map:
                    raise Exception(f"联动目标组件 UUID 不存在: {target_uuid}")
                target_comp = component_map[target_uuid]
                target_model_id = target_comp.get("modelId")
                if target_model_id != model_id:
                    raise Exception(
                        f"联动目标组件 UUID={target_uuid} 使用的数据模型(ID:{target_model_id})"
                        f"与当前组件(ID:{model_id})不同，联动组件必须使用相同数据模型"
                    )

        if linkage:
            comp["interaction"] = {"linkage": {"sameModels": linkage}}
            print(f"更新组件联动：")
            print(f"  源组件: {uuid}")
            print(f"  联动目标: {linkage}")
        else:
            if "interaction" in comp:
                del comp["interaction"]
            print(f"清除组件联动：{uuid}")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def build_date_filter_config(
        self,
        date_filter: str,
        dim: Dict,
    ) -> List[Dict]:
        """构建日期筛选器配置

        Args:
            date_filter: 筛选器类型
                - 相对时间: thisYear, thisMonth, lastMonth, thisQuarter, lastQuarter
                - 自定义日期: YYYY-MM-DD,YYYY-MM-DD 格式
            dim: 维度字段信息

        Returns:
            筛选器配置列表
        """
        from datetime import datetime

        date_filter_map = {
            "thisYear": "今年",
            "lastYear": "去年",
            "thisMonth": "本月",
            "lastMonth": "上月",
            "thisQuarter": "本季度",
            "lastQuarter": "上季度",
        }

        dim_field_label = dim.get("fieldLabel", "")
        dim_field_name = dim.get("fieldName", "")
        dim_ds_name = dim.get("datasetName", "")
        dim_ds_id = dim.get("datasetId", "")
        dim_field_id = dim.get("id", "")

        if "," in date_filter:
            parts = date_filter.split(",")
            if len(parts) == 2:
                start_date, end_date = parts[0].strip(), parts[1].strip()
                try:
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
                            "datasetId": dim_ds_id,
                            "datasetMetaId": dim_ds_id,
                            "dateFormat": "YMD",
                            "fieldFilter": {
                                "conditions": [
                                    {
                                        "key": "1",
                                        "left": {
                                            "customPeriodType": False,
                                            "expressionType": False,
                                            "fieldType": True,
                                            "label": dim_field_label,
                                            "type": "field",
                                            "value": f"{dim_ds_name}.{dim_field_name}",
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
                                "metaId": dim_ds_id,
                                "metaName": dim_ds_name,
                            },
                            "fieldId": dim_field_id,
                            "fieldLabel": dim_field_label,
                            "fieldName": dim_field_name,
                            "index": 0,
                            "metricType": "NONAGG",
                            "modelDatasetName": dim_ds_name,
                            "nativeType": dim.get("nativeType", ""),
                            "newFieldLabel": dim_field_label,
                        }
                    ]
                except ValueError:
                    raise ValueError(
                        f"无效的日期格式: '{date_filter}'，期望格式为 YYYY-MM-DD,YYYY-MM-DD（例如 2024-01-01,2024-12-31）"
                    )

        filter_expression = date_filter_map.get(date_filter, date_filter)
        return [
            {
                "datasetId": dim_ds_id,
                "datasetMetaId": dim_ds_id,
                "dateFormat": "YMD",
                "fieldFilter": {
                    "conditions": [
                        {
                            "key": "1",
                            "left": {
                                "customPeriodType": False,
                                "expressionType": False,
                                "fieldType": True,
                                "label": dim_field_label,
                                "type": "field",
                                "value": f"{dim_ds_name}.{dim_field_name}",
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
                    "metaId": dim_ds_id,
                    "metaName": dim_ds_name,
                },
                "fieldId": dim_field_id,
                "fieldLabel": dim_field_label,
                "fieldName": dim_field_name,
                "index": 0,
                "metricType": "NONAGG",
                "modelDatasetName": dim_ds_name,
                "nativeType": dim.get("nativeType", ""),
                "newFieldLabel": dim_field_label,
            }
        ]

    def update_component_filter(
        self,
        screen_id: int,
        uuid: str,
        date_filter: str,
    ) -> bool:
        """更新组件的日期筛选器

        Args:
            screen_id: 大屏 ID
            uuid: 组件 UUID
            date_filter: 日期筛选器
                - 相对时间: thisYear, thisMonth, lastMonth, thisQuarter, lastQuarter
                - 自定义日期: YYYY-MM-DD,YYYY-MM-DD 格式
                - clear: 清除筛选器
        """
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)

        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": screen_data.get("componentMap", {}),
            "topLayouts": screen_data.get("topLayouts", []),
        }

        component_map = config["componentMap"]
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")

        comp = component_map[uuid]
        dimensions = comp.get("dimensions", [])
        if not dimensions:
            raise Exception(f"组件没有维度配置，无法设置日期筛选器")

        dim = dimensions[0]

        if date_filter == "clear":
            if "filter" in comp:
                del comp["filter"]
            print(f"清除组件日期筛选器：{uuid}")
        else:
            comp["filter"] = self.build_date_filter_config(date_filter, dim)
            print(f"更新组件日期筛选器：{uuid}")
            print(f"  筛选器类型：{date_filter}")
            print(f"  维度字段：{dim.get('fieldLabel')} ({dim.get('fieldName')})")

        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def move_to_center(
        self,
        screen_id: int,
        uuid: str,
        width: int = 960,
        height: int = 400,
        name: Optional[str] = None,
    ) -> bool:
        """将组件移到画布中心"""
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)
        canvas_width = (
            screen_data.get("config", {}).get("canvas", {}).get("canvasWidth", 1920)
        )
        canvas_height = (
            screen_data.get("config", {}).get("canvas", {}).get("canvasHeight", 1080)
        )
        center_top = (canvas_height - height) // 2
        center_left = (canvas_width - width) // 2
        return self.update_component_position(
            screen_id,
            uuid,
            top=center_top,
            left=center_left,
            width=width,
            height=height,
            name=name or screen_data.get("name"),
        )

    def reorder_layer(
        self,
        screen_id: int,
        uuid: str,
        direction: str,
    ) -> bool:
        """调整图层层级顺序"""
        direction = direction.lower()
        if direction not in ("up", "down", "top", "bottom"):
            raise Exception(f"无效的方向：{direction}，有效值 up/down/top/bottom")
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)
        layers = screen_data.get("config", {}).get("layers", [])
        layouts = screen_data.get("layouts", [])
        component_map = screen_data.get("componentMap", {})
        for layer in layers:
            if layer.get("uuid") == uuid:
                current_z = layer.get("zIndex", 1)
                if direction == "up":
                    layer["zIndex"] = current_z + 1
                elif direction == "down":
                    layer["zIndex"] = max(1, current_z - 1)
                elif direction == "top":
                    layer["zIndex"] = len(layers) + 1
                elif direction == "bottom":
                    layer["zIndex"] = 1
                print(f"调整图层顺序：{uuid} -> {direction} (zIndex={layer['zIndex']})")
                break
        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": layouts,
            "componentMap": component_map,
            "topLayouts": screen_data.get("topLayouts", []),
        }
        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True

    def update_component_card_style(
        self,
        screen_id: int,
        uuid: str,
        card_background_color: Optional[str] = None,
        card_border: Optional[str] = None,
        card_padding: Optional[int] = None,
    ) -> bool:
        """更新组件的卡片样式"""
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id, use_cache=False)
        component_map = screen_data.get("componentMap", {})
        if uuid not in component_map:
            raise Exception(f"未找到 UUID 为 {uuid} 的组件")
        comp = component_map[uuid]
        style_json = comp.get("styleJson", {})
        if "card" not in style_json:
            style_json["card"] = {}
        card = style_json["card"]
        updates = []
        if card_background_color is not None:
            old = card.get("cardBackgroundColor", "")
            card["cardBackgroundColor"] = card_background_color
            updates.append(f"背景色: {old} -> {card_background_color}")
        if card_border is not None:
            old = card.get("border", "")
            card["border"] = card_border
            updates.append(f"边框: {old} -> {card_border}")
        if card_padding is not None:
            old = card.get("padding", 0)
            card["padding"] = card_padding
            updates.append(f"内边距: {old} -> {card_padding}")
        if updates:
            print("更新卡片样式：")
            for u in updates:
                print(f"  {u}")
        config = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": screen_data.get("config", {}),
            "layouts": screen_data.get("layouts", []),
            "componentMap": component_map,
            "topLayouts": screen_data.get("topLayouts", []),
        }
        print(f"正在更新大屏...")
        self.update_screen(screen_id, config)
        return True


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="更新大屏配置",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 1. 查看大屏详情
  python3 scripts/update_screen.py --screen-id 3654939432 --show-info

  # 2. 更新组件位置
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:bar-uuid:xxx" --top 100 --left 200

  # 3. 移动组件到画布中心
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:bar-uuid:xxx" --center --width 440 --height 270

  # 4. 复制样式（将组件A的样式应用到组件B、C）
  python3 scripts/update_screen.py --screen-id 3654939432 --clone-style-from "grid-type:metric-uuid:aaa" --clone-style-to "grid-type:metric-uuid:bbb" "grid-type:metric-uuid:ccc"

  # 5. 批量更新指标卡样式（把所有指标卡改成和收入合同金额一样）
  python3 scripts/update_screen.py --screen-id 3654939432 --clone-style-from "grid-type:metric-uuid:1773967404738" --clone-style-to "grid-type:metric-uuid:1773967415673" "grid-type:metric-uuid:1773967417343" "grid-type:metric-uuid:1773967421429"

  # 6. 调整文本组件字体大小
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:text-uuid:1773967632945" --font-size 36

  # 7. 更新脚本组件代码
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:script-uuid:1773967632945" --script-code 'option = { ... }; myChart.setOption(option);'

  # 8. 调整图层层级顺序
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:metric-uuid:xxx" --move-layer top

  # 9. 更新组件维度排序
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:line-uuid:xxx" --order-type asc

  # 10. 清除指标排序（只按维度排序）
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:line-uuid:xxx" --indicator-order-type none

  # 11. 更新文本组件对齐方式（居中）
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:text-uuid:xxx" --align center

  # 12. 设置大屏背景图片
  python3 scripts/update_screen.py --screen-id 3654939432 --set-background /path/to/background.png

  # 13. 更新组件卡片样式（设置背景色、边框、内边距）
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:line-uuid:xxx" --card-background-color "rgba(13, 24, 44, 0.8)" --card-border "rgba(30, 39, 55, 0.8)" --card-padding 12

  # 14. 修改头部组件的装饰图片（换成 7 号样式）
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:head-uuid:xxx" --decorate-index 7

  # 15. 修改线图线条类型（改成折线）
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:line-uuid:xxx" --line-type line

  # 16. 更新指标卡样式
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:metric-uuid:xxx" --metric-style card

  # 17. 隐藏指标卡标签
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:metric-uuid:xxx" --metric-label-visible false

  # 18. 更新表格样式（表头背景、内容字体、表行颜色等）
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:table-uuid:xxx" \
    --table-body-font-size 14 --table-body-text-color "#DBDFF1" \
    --table-header-bg-color "#08143E" --table-header-font-size 12 --table-header-bold true \
    --table-odd-row-color "#0A1E38" --table-even-row-color "#020B1C" \
    --table-row-split-line-color "#334979" --table-row-split-line-size 1 \
    --table-scroll-show true --table-scroll-speed 5

  # 19. 更新翻牌器样式
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:flipper-uuid:xxx" \
    --flipper-int-figure 8 --flipper-decimal-figure 2 --flipper-thousandth true \
    --flipper-style-type round --flipper-font-size 34 \
    --flipper-fill-color "linear-gradient(180deg, rgba(2,53,107,0.5) 0%, rgba(5,101,164,0.5) 100%)" \
    --flipper-border-color "#A5CCEA" --flipper-flip-gap 12

  # 20. 更新组件联动配置
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:bar-uuid:xxx" \
    --update-linkage "grid-type:pie-uuid:yyy" "grid-type:table-uuid:zzz"

  # 21. 清除组件联动
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:bar-uuid:xxx" \
    --clear-linkage

  # 22. 更新组件日期筛选器（相对时间）
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:bar-uuid:xxx" \
    --filter thisMonth

  # 23. 更新组件日期筛选器（自定义日期范围）
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:bar-uuid:xxx" \
    --filter "2024-01-01,2024-12-31"

  # 24. 清除组件日期筛选器
  python3 scripts/update_screen.py --screen-id 3654939432 --uuid "grid-type:bar-uuid:xxx" \
    --filter clear
""",
    )
    parser.add_argument("--screen-id", type=int, required=True, help="大屏 ID")
    parser.add_argument("--uuid", help="组件 UUID（不传则显示所有组件信息）")
    parser.add_argument("--top", type=int, help="top 坐标")
    parser.add_argument("--left", type=int, help="left 坐标")
    parser.add_argument("--width", type=int, help="组件宽度")
    parser.add_argument("--height", type=int, help="组件高度")
    parser.add_argument("--name", help="大屏名称（可选，不传则保持原名）")
    parser.add_argument("--center", action="store_true", help="将组件移到画布中心")
    parser.add_argument("--show-info", action="store_true", help="显示大屏详细信息")
    parser.add_argument(
        "--show-style",
        action="store_true",
        help="显示样式详情（配合 --show-info 使用）",
    )
    parser.add_argument("--clone-style-from", help="样式来源组件的 UUID")
    parser.add_argument(
        "--clone-style-to", nargs="+", help="要应用样式的目标组件 UUID 列表"
    )
    parser.add_argument(
        "--font-size", type=int, help="文本组件字体大小（仅对 text 类型组件有效）"
    )
    parser.add_argument(
        "--align",
        choices=["left", "center", "right"],
        help="文本组件对齐方式（仅对 text 类型组件有效）：left(左对齐)、center(居中对齐)、right(右对齐)",
    )
    parser.add_argument(
        "--script-code", help="脚本组件的 JavaScript 代码（仅对 script 类型组件有效）"
    )
    parser.add_argument("--base-url", default=get_base_url(), help="API 基础 URL")
    parser.add_argument(
        "--env",
        default="dev",
        choices=["dev", "test", "prod"],
        help="环境 (默认 dev，与 --base-url 二选一)",
    )
    parser.add_argument(
        "--move-layer",
        choices=["up", "down", "top", "bottom"],
        help="调整图层层级顺序：up(上移一层)、down(下移一层)、top(移到最顶层)、bottom(移至最底层)",
    )
    parser.add_argument(
        "--order-type",
        choices=["asc", "desc", "none"],
        help="更新组件维度的排序方式：asc(升序) 或 desc(降序)，none(清除排序)",
    )
    parser.add_argument(
        "--indicator-order-type",
        choices=["asc", "desc", "none"],
        help="更新组件指标的排序方式：asc(升序)、desc(降序)、none(清除排序)",
    )
    parser.add_argument(
        "--indicator-label",
        type=str,
        help='更新指标显示名称（如"本月收款金额"）',
    )
    parser.add_argument(
        "--set-background",
        type=str,
        help="设置大屏背景图片（传入本地图片路径）",
    )
    parser.add_argument(
        "--card-background-color",
        type=str,
        help="卡片背景颜色（如 rgba(13, 24, 44, 0.8)）",
    )
    parser.add_argument(
        "--card-border",
        type=str,
        help="卡片边框颜色（如 rgba(30, 39, 55, 0.8)）",
    )
    parser.add_argument(
        "--card-padding",
        type=int,
        help="卡片内边距（如 12）",
    )
    parser.add_argument(
        "--decorate-index",
        type=int,
        help="装饰图片编号（1-14，仅对 head/decorate 类型组件有效）",
    )
    parser.add_argument(
        "--line-type",
        type=str,
        choices=["line", "curve"],
        help="线图线条类型（仅对 line 类型组件有效）：line(折线)，curve(曲线)",
    )
    parser.add_argument(
        "--metric-style",
        type=str,
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
        help="指标卡样式预设（仅对 metric 类型组件有效）",
    )
    parser.add_argument(
        "--metric-label-visible",
        type=str,
        choices=["true", "false"],
        help="指标卡标签可见性（仅对 metric 类型组件有效）：true(显示)，false(隐藏)",
    )
    parser.add_argument(
        "--time-color",
        type=str,
        help="时间组件文字颜色（仅对 time 类型组件有效，如 #A6ADD0）",
    )
    parser.add_argument(
        "--time-format",
        type=str,
        help="时间组件格式类型（仅对 time 类型组件有效）：dateAndTime(日期+时间)、date(仅日期)、time(仅时间)",
    )
    parser.add_argument(
        "--table-body-font-size",
        type=int,
        help="表格内容字体大小（仅对 table 类型组件有效）",
    )
    parser.add_argument(
        "--table-body-text-color",
        type=str,
        help="表格内容文字颜色（仅对 table 类型组件有效），如 #DBDFF1",
    )
    parser.add_argument(
        "--table-body-bold",
        type=str,
        choices=["true", "false"],
        help="表格内容是否加粗（仅对 table 类型组件有效）",
    )
    parser.add_argument(
        "--table-header-bg-color",
        type=str,
        help="表头背景色（仅对 table 类型组件有效），如 #08143E",
    )
    parser.add_argument(
        "--table-header-font-size",
        type=int,
        help="表头字体大小（仅对 table 类型组件有效）",
    )
    parser.add_argument(
        "--table-header-text-color",
        type=str,
        help="表头文字颜色（仅对 table 类型组件有效），如 #DBDFF1",
    )
    parser.add_argument(
        "--table-header-bold",
        type=str,
        choices=["true", "false"],
        help="表头是否加粗（仅对 table 类型组件有效）",
    )
    parser.add_argument(
        "--table-odd-row-color",
        type=str,
        help="奇数行背景色（仅对 table 类型组件有效），如 #0A1E38",
    )
    parser.add_argument(
        "--table-even-row-color",
        type=str,
        help="偶数行背景色（仅对 table 类型组件有效），如 #020B1C",
    )
    parser.add_argument(
        "--table-row-split-line-color",
        type=str,
        help="行分割线颜色（仅对 table 类型组件有效），如 #334979",
    )
    parser.add_argument(
        "--table-row-split-line-size",
        type=int,
        help="行分割线宽度（仅对 table 类型组件有效）",
    )
    parser.add_argument(
        "--table-col-split-line-color",
        type=str,
        help="列分割线颜色（仅对 table 类型组件有效），如 #334979",
    )
    parser.add_argument(
        "--table-col-split-line-size",
        type=int,
        help="列分割线宽度（仅对 table 类型组件有效）",
    )
    parser.add_argument(
        "--table-scroll-show",
        type=str,
        choices=["true", "false"],
        help="滚动显示（仅对 table 类型组件有效）",
    )
    parser.add_argument(
        "--table-scroll-speed",
        type=int,
        help="滚动速度（仅对 table 类型组件有效），1-10",
    )
    parser.add_argument(
        "--flipper-int-figure",
        type=int,
        help="翻牌器整数位数（仅对 flipper 类型组件有效）",
    )
    parser.add_argument(
        "--flipper-decimal-figure",
        type=int,
        help="翻牌器小数位数（仅对 flipper 类型组件有效）",
    )
    parser.add_argument(
        "--flipper-thousandth",
        type=str,
        choices=["true", "false"],
        help="翻牌器千分位（仅对 flipper 类型组件有效）：true(显示)/false(隐藏)",
    )
    parser.add_argument(
        "--flipper-style-type",
        type=str,
        choices=["round", "square"],
        help="翻牌器样式类型（仅对 flipper 类型组件有效）：round(圆角)/square(直角)",
    )
    parser.add_argument(
        "--flipper-font-color",
        type=str,
        help="翻牌器字体颜色（仅对 flipper 类型组件有效）",
    )
    parser.add_argument(
        "--flipper-fill-color",
        type=str,
        help="翻牌器填充颜色（仅对 flipper 类型组件有效）",
    )
    parser.add_argument(
        "--flipper-border-color",
        type=str,
        help="翻牌器边框颜色（仅对 flipper 类型组件有效）",
    )
    parser.add_argument(
        "--flipper-flip-gap",
        type=int,
        help="翻牌器翻牌间隔（仅对 flipper 类型组件有效）",
    )
    parser.add_argument(
        "--flipper-font-size",
        type=int,
        help="翻牌器字体大小（仅对 flipper 类型组件有效）",
    )
    parser.add_argument(
        "--radar-radius",
        type=int,
        help="雷达图半径（仅对 radar 类型组件有效）",
    )
    parser.add_argument(
        "--radar-legend-position",
        type=str,
        choices=["top", "bottom", "left", "right"],
        help="雷达图图例位置（仅对 radar 类型组件有效）",
    )
    parser.add_argument(
        "--radar-label-position",
        type=str,
        choices=["auto", "top", "bottom", "left", "right"],
        help="雷达图标签位置（仅对 radar 类型组件有效）",
    )
    parser.add_argument(
        "--update-linkage",
        type=str,
        nargs="+",
        help="更新组件联动配置（传目标组件 UUID 列表）",
    )
    parser.add_argument(
        "--clear-linkage",
        action="store_true",
        help="清除组件联动配置",
    )
    parser.add_argument(
        "--filter",
        type=str,
        help="更新组件日期筛选器（相对时间: thisYear/thisMonth/lastMonth/thisQuarter/lastQuarter；自定义: 2024-01-01,2024-12-31；清除: clear）",
    )

    args = parser.parse_args()

    base_url = args.base_url if args.base_url else get_base_url(args.env)
    updater = BiScreenUpdater(base_url)

    try:
        screen_data = updater.get_screen(args.screen_id, use_cache=False)

        if args.show_info or not args.uuid:
            updater.print_screen_info(screen_data, show_style=args.show_style)

        # 样式复制模式
        if args.clone_style_from:
            if not args.clone_style_to:
                print("错误：--clone-style-from 需要配合 --clone-style-to 使用")
                return 1
            updater.clone_component_style(
                args.screen_id,
                args.clone_style_from,
                args.clone_style_to,
            )
            print(f"\n✅ 样式复制成功!")
            print(f"访问 URL: {get_preview_url(args.screen_id, base_url)}")
            return 0

        if args.set_background:
            updater.set_background_image(args.screen_id, args.set_background)
            print(f"\n✅ 背景图片设置成功!")
            print(f"访问 URL: {get_preview_url(args.screen_id, base_url)}")
            return 0

        if not args.uuid:
            print("\n提示：使用 --uuid 指定要操作的组件")
            print("      或使用 --clone-style-from / --clone-style-to 复制样式")
            return 0

        if args.font_size is not None:
            if not args.uuid:
                print("错误：--font-size 需要配合 --uuid 使用")
                return 1
            updater.update_text_font_size(
                args.screen_id,
                args.uuid,
                args.font_size,
            )
        elif args.time_color is not None:
            if not args.uuid:
                print("错误：--time-color 需要配合 --uuid 使用")
                return 1
            updater.update_time_color(
                args.screen_id,
                args.uuid,
                args.time_color,
            )
        elif args.time_format is not None:
            if not args.uuid:
                print("错误：--time-format 需要配合 --uuid 使用")
                return 1
            time_type_map = {
                "dateAndTime": ("yyyy-MM-dd", "hh:mm:ss"),
                "date": ("yyyy-MM-dd", ""),
                "time": ("", "hh:mm:ss"),
            }
            if args.time_format not in time_type_map:
                print("错误：--time-format 无效，有效值：dateAndTime, date, time")
                return 1
            date_fmt, time_fmt = time_type_map[args.time_format]
            updater.update_time_format(
                args.screen_id,
                args.uuid,
                time_type=args.time_format,
                date_format=date_fmt,
                time_format=time_fmt,
            )
        elif args.align is not None:
            if not args.uuid:
                print("错误：--align 需要配合 --uuid 使用")
                return 1
            updater.update_text_align(
                args.screen_id,
                args.uuid,
                args.align,
            )
        elif args.script_code is not None:
            if not args.uuid:
                print("错误：--script-code 需要配合 --uuid 使用")
                return 1
            updater.update_script_code(
                args.screen_id,
                args.uuid,
                args.script_code,
            )
        elif args.center:
            updater.move_to_center(
                args.screen_id,
                args.uuid,
                args.width or 960,
                args.height or 400,
                args.name,
            )
        elif args.top is not None or args.left is not None:
            updater.update_component_position(
                args.screen_id,
                args.uuid,
                top=args.top,
                left=args.left,
                width=args.width,
                height=args.height,
                name=args.name,
            )
        elif args.move_layer:
            if not args.uuid:
                print("错误：--move-layer 需要配合 --uuid 使用")
                return 1
            updater.reorder_layer(
                args.screen_id,
                args.uuid,
                args.move_layer,
            )
        if args.order_type:
            if not args.uuid:
                print("错误：--order-type 需要配合 --uuid 使用")
                return 1
            updater.update_dimension_order(
                args.screen_id,
                args.uuid,
                args.order_type,
            )
        if args.indicator_order_type:
            if not args.uuid:
                print("错误：--indicator-order-type 需要配合 --uuid 使用")
                return 1
            updater.update_indicator_order(
                args.screen_id,
                args.uuid,
                args.indicator_order_type,
            )

        if args.indicator_label:
            if not args.uuid:
                print("错误：--indicator-label 需要配合 --uuid 使用")
                return 1
            updater.update_indicator_label(
                args.screen_id,
                args.uuid,
                args.indicator_label,
            )

        # 更新卡片样式
        if (
            args.card_background_color is not None
            or args.card_border is not None
            or args.card_padding is not None
        ):
            if not args.uuid:
                print("错误：卡片样式参数需要配合 --uuid 使用")
                return 1
            updater.update_component_card_style(
                args.screen_id,
                args.uuid,
                card_background_color=args.card_background_color,
                card_border=args.card_border,
                card_padding=args.card_padding,
            )

        if args.decorate_index is not None:
            if not args.uuid:
                print("错误：--decorate-index 需要配合 --uuid 使用")
                return 1
            updater.update_decorate_index(
                args.screen_id,
                args.uuid,
                args.decorate_index,
            )

        if args.line_type is not None:
            if not args.uuid:
                print("错误：--line-type 需要配合 --uuid 使用")
                return 1
            updater.update_line_type(
                args.screen_id,
                args.uuid,
                args.line_type,
            )

        if args.metric_style is not None:
            if not args.uuid:
                print("错误：--metric-style 需要配合 --uuid 使用")
                return 1
            updater.update_metric_style(
                args.screen_id,
                args.uuid,
                args.metric_style,
            )

        if args.metric_label_visible is not None:
            if not args.uuid:
                print("错误：--metric-label-visible 需要配合 --uuid 使用")
                return 1
            updater.update_metric_label_visible(
                args.screen_id,
                args.uuid,
                args.metric_label_visible == "true",
            )

        # 更新表格样式
        table_args = [
            args.table_body_font_size,
            args.table_body_text_color,
            args.table_body_bold,
            args.table_header_bg_color,
            args.table_header_font_size,
            args.table_header_text_color,
            args.table_header_bold,
            args.table_odd_row_color,
            args.table_even_row_color,
            args.table_row_split_line_color,
            args.table_row_split_line_size,
            args.table_col_split_line_color,
            args.table_col_split_line_size,
            args.table_scroll_show,
            args.table_scroll_speed,
        ]
        if any(a is not None for a in table_args):
            if not args.uuid:
                print("错误：表格样式参数需要配合 --uuid 使用")
                return 1
            updater.update_table_style(
                args.screen_id,
                args.uuid,
                body_font_size=args.table_body_font_size,
                body_text_color=args.table_body_text_color,
                body_bold=args.table_body_bold == "true"
                if args.table_body_bold
                else None,
                header_bg_color=args.table_header_bg_color,
                header_font_size=args.table_header_font_size,
                header_text_color=args.table_header_text_color,
                header_bold=args.table_header_bold == "true"
                if args.table_header_bold
                else None,
                odd_row_color=args.table_odd_row_color,
                even_row_color=args.table_even_row_color,
                row_split_line_color=args.table_row_split_line_color,
                row_split_line_size=args.table_row_split_line_size,
                col_split_line_color=args.table_col_split_line_color,
                col_split_line_size=args.table_col_split_line_size,
                scroll_show=args.table_scroll_show == "true"
                if args.table_scroll_show
                else None,
                scroll_speed=args.table_scroll_speed,
            )

        # 更新翻牌器样式
        flipper_args = [
            args.flipper_int_figure,
            args.flipper_decimal_figure,
            args.flipper_thousandth,
            args.flipper_style_type,
            args.flipper_font_color,
            args.flipper_fill_color,
            args.flipper_border_color,
            args.flipper_flip_gap,
            args.flipper_font_size,
        ]
        if any(a is not None for a in flipper_args):
            if not args.uuid:
                print("错误：翻牌器样式参数需要配合 --uuid 使用")
                return 1
            updater.update_flipper_style(
                args.screen_id,
                args.uuid,
                flipper_int_figure=args.flipper_int_figure,
                flipper_decimal_figure=args.flipper_decimal_figure,
                flipper_thousandth=args.flipper_thousandth == "true"
                if args.flipper_thousandth
                else None,
                flipper_style_type=args.flipper_style_type,
                flipper_font_color=args.flipper_font_color,
                flipper_fill_color=args.flipper_fill_color,
                flipper_border_color=args.flipper_border_color,
                flipper_flip_gap=args.flipper_flip_gap,
                flipper_font_size=args.flipper_font_size,
            )

        # 更新雷达图样式
        radar_args = [
            args.radar_radius,
            args.radar_legend_position,
            args.radar_label_position,
        ]
        if any(a is not None for a in radar_args):
            if not args.uuid:
                print("错误：雷达图样式参数需要配合 --uuid 使用")
                return 1
            updater.update_radar_style(
                args.screen_id,
                args.uuid,
                radar_radius=args.radar_radius,
                radar_legend_position=args.radar_legend_position,
                radar_label_position=args.radar_label_position,
            )

        # 更新组件联动
        if args.update_linkage is not None:
            if not args.uuid:
                print("错误：--update-linkage 需要配合 --uuid 使用")
                return 1
            linkage_list = args.update_linkage if args.update_linkage else []
            updater.update_component_linkage(
                args.screen_id,
                args.uuid,
                linkage_list,
            )
        elif args.clear_linkage:
            if not args.uuid:
                print("错误：--clear-linkage 需要配合 --uuid 使用")
                return 1
            updater.update_component_linkage(
                args.screen_id,
                args.uuid,
                [],
            )

        if args.filter is not None:
            if not args.uuid:
                print("错误：--filter 需要配合 --uuid 使用")
                return 1
            updater.update_component_filter(
                args.screen_id,
                args.uuid,
                args.filter,
            )

        if (
            not args.order_type
            and not args.indicator_order_type
            and args.top is None
            and args.left is None
            and not args.center
            and not args.move_layer
            and not args.font_size
            and not args.align
            and not args.script_code
            and not args.clone_style_from
            and args.card_background_color is None
            and args.card_border is None
            and args.card_padding is None
            and args.decorate_index is None
            and args.line_type is None
            and args.metric_style is None
            and args.metric_label_visible is None
            and args.table_body_font_size is None
            and args.table_body_text_color is None
            and args.table_body_bold is None
            and args.table_header_bg_color is None
            and args.table_header_font_size is None
            and args.table_header_text_color is None
            and args.table_header_bold is None
            and args.table_odd_row_color is None
            and args.table_even_row_color is None
            and args.table_row_split_line_color is None
            and args.table_row_split_line_size is None
            and args.table_col_split_line_color is None
            and args.table_col_split_line_size is None
            and args.table_scroll_show is None
            and args.table_scroll_speed is None
            and args.flipper_int_figure is None
            and args.flipper_decimal_figure is None
            and args.flipper_thousandth is None
            and args.flipper_style_type is None
            and args.flipper_font_color is None
            and args.flipper_fill_color is None
            and args.flipper_border_color is None
            and args.flipper_flip_gap is None
            and args.flipper_font_size is None
            and args.radar_radius is None
            and args.radar_legend_position is None
            and args.radar_label_position is None
            and args.update_linkage is None
            and not args.clear_linkage
            and args.filter is None
        ):
            print(
                "请使用 --top/--left 或 --center 或 --font-size 或 --align 或 --script-code 或 --card-* 或 --decorate-index 或 --line-type 或 --metric-style 或 --metric-label-visible 或 --table-* 或 --flipper-* 或 --radar-* 或 --update-linkage 或 --clear-linkage 或 --filter 指定操作"
            )
            return 0

        print(f"\n✅ 大屏更新成功!")
        print(f"访问 URL: {get_preview_url(args.screen_id, base_url)}")

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
