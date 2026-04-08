#!/usr/bin/env python3
"""
背景图片生成脚本 - 为数字大屏生成背景图片

获取大屏布局信息，由大模型根据上下文决定 prompt
生成后询问用户是否设置成背景图片
"""

import argparse
import base64
import os
import sys
import time
import json
import requests
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "header.json"
CACHE_DIR = SCRIPT_DIR / ".cache"

from auth import get_base_url, get, post

BISERVER_BASE = get_base_url()


def get_api_credentials():
    """获取 API 认证信息"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config.get("imageApiKey") or config.get("apiKey")
    return None


def get_screen_config(screen_id):
    """获取大屏配置"""
    if not CONFIG_FILE.exists():
        print("ERROR: header.json 不存在")
        sys.exit(1)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        header = json.load(f)

    url = f"{BISERVER_BASE}/biserver/paas/bi-app/largeScreen/get/{screen_id}"

    headers = {k: v for k, v in header.items() if k != "Content-Type"}

    response = get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def parse_layout_info(screen_config):
    """
    从大屏配置中解析布局信息

    Returns:
        dict: 包含 canvas_size, components 等信息
    """
    config = screen_config.get("data", {}).get("config", {})
    layouts = screen_config.get("data", {}).get("layouts", [])
    layers = config.get("layers", [])

    canvas = config.get("canvas", {})
    canvas_width = canvas.get("canvasWidth", 1920)
    canvas_height = canvas.get("canvasHeight", 1080)

    layer_map = {l["uuid"]: l for l in layers}

    components = []
    for layout in layouts:
        uuid = layout.get("uuid")
        layer = layer_map.get(uuid, {})

        comp_type = layout.get("type", "unknown")
        if comp_type in ["text", "decorate", "head"]:
            continue

        components.append(
            {
                "type": comp_type,
                "title": layout.get("title", ""),
                "top": layer.get("top", 0),
                "left": layer.get("left", 0),
                "width": layer.get("width", 0),
                "height": layer.get("height", 0),
            }
        )

    has_map = any(c["type"] == "map" for c in components)
    chart_count = len([c for c in components if c["type"] not in ["metric", "table"]])
    metric_count = len([c for c in components if c["type"] == "metric"])

    regions = analyze_regions(canvas_width, canvas_height, components)

    return {
        "canvas_width": canvas_width,
        "canvas_height": canvas_height,
        "components": components,
        "has_map": has_map,
        "chart_count": chart_count,
        "metric_count": metric_count,
        "regions": regions,
    }


def analyze_regions(canvas_width, canvas_height, components):
    """分析大屏区域分布"""
    if not components:
        return {"type": "empty", "main_area": "center"}

    top_components = [c for c in components if c["top"] < canvas_height * 0.2]
    bottom_components = [c for c in components if c["top"] > canvas_height * 0.7]
    center_components = [
        c
        for c in components
        if canvas_width * 0.3 <= c["left"] <= canvas_width * 0.7
        and canvas_height * 0.2 <= c["top"] <= canvas_height * 0.7
    ]

    large_components = [
        c
        for c in components
        if c["width"] > canvas_width * 0.4 and c["height"] > canvas_height * 0.4
    ]

    region_type = "single_focus"
    if len(large_components) > 1:
        region_type = "multi_focus"
    elif len(center_components) > 0:
        region_type = "center_focus"
    elif len(top_components) > 0:
        region_type = "top_heavy"

    return {
        "type": region_type,
        "main_area": "center"
        if region_type in ["single_focus", "center_focus"]
        else "full",
        "has_top_bar": len(top_components) > 0,
        "has_bottom_bar": len(bottom_components) > 0,
        "large_component_count": len(large_components),
    }


def print_layout_summary(layout_info):
    """打印布局摘要"""
    print(
        f"\n📐 画布尺寸: {layout_info['canvas_width']} x {layout_info['canvas_height']}"
    )
    print(f"📊 组件数量: {len(layout_info['components'])}")
    print(f"   - 图表: {layout_info['chart_count']}")
    print(f"   - 指标卡: {layout_info['metric_count']}")
    print(f"   - 地图: {'是' if layout_info['has_map'] else '否'}")
    print(f"\n🎯 布局分析: {layout_info['regions']['type']}")
    print(f"   主视觉区域: {layout_info['regions']['main_area']}")

    if layout_info["components"]:
        print(f"\n📍 组件位置分布:")
        for comp in sorted(
            layout_info["components"], key=lambda x: (x["top"], x["left"])
        ):
            print(
                f"   {comp['type']:12} | top={comp['top']:4}, left={comp['left']:4} | {comp['width']}x{comp['height']}"
            )


def generate_background(prompt, canvas_width, canvas_height, api_key, output_dir):
    """调用 MiniMax API 生成背景图片"""
    url = "https://api.minimaxi.com/v1/image_generation"
    headers = {"Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "image-01",
        "prompt": prompt,
        "width": canvas_width,
        "height": canvas_height,
        "response_format": "base64",
    }

    start_time = time.time()
    response = post(url, headers=headers, json=payload)
    elapsed = time.time() - start_time

    images = response.json()["data"]["image_base64"]

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = int(time.time())
    output_paths = []

    for i, img_base64 in enumerate(images):
        output_path = (
            output_dir / f"bg_{canvas_width}x{canvas_height}_{timestamp}_{i}.png"
        )
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(img_base64))
        output_paths.append(str(output_path))

    print(f"\n✅ 成功生成 {len(images)} 张背景图片，耗时: {elapsed:.2f} 秒")
    for path in output_paths:
        print(f"   {path}")

    return output_paths


def upload_image_to_obs(image_path):
    """上传图片到华为云 OBS 并返回 URL

    Args:
        image_path: 本地图片路径

    Returns:
        str: 图片的 CDN URL
    """
    image_file = Path(image_path)
    if not image_file.exists():
        raise Exception(f"图片文件不存在：{image_path}")

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

    print(f"正在获取上传参数...")
    get_param_url = f"{BISERVER_BASE}/universe/paas/settings/getFileUploadParamBySize"

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        header = json.load(f)
    headers = {k: v for k, v in header.items() if k != "Content-Type"}

    get_param_data = {
        "fileName": new_name,
        "fileSize": file_size,
        "bucket": "hwtest-image-public",
        "originalFileName": file_name,
    }
    response = post(
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
    from obs import ObsClient

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


def update_screen_background(screen_id, background_url):
    """更新大屏背景图片

    Args:
        screen_id: 大屏 ID
        background_url: 背景图片 URL
    """
    print(f"正在获取大屏配置...")

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        header = json.load(f)
    headers = {k: v for k, v in header.items() if k != "Content-Type"}
    headers["Content-Type"] = "application/json"

    get_url = f"{BISERVER_BASE}/biserver/paas/bi-app/largeScreen/get/{screen_id}"
    response = get(get_url, headers=headers)
    screen_data = response.json()

    if screen_data.get("result") != "0":
        raise Exception(f"获取大屏失败：{screen_data.get('desc')}")

    screen_data = screen_data.get("data", {})

    config = {
        "id": screen_id,
        "name": screen_data.get("name"),
        "config": screen_data.get("config", {}),
        "layouts": screen_data.get("layouts", []),
        "componentMap": screen_data.get("componentMap", {}),
        "topLayouts": screen_data.get("topLayouts", []),
    }

    style = config["config"].get("style", {})
    style["panelBackgroundImage"] = background_url
    style["panelBackgroundImageRepeat"] = "cover"
    config["config"]["style"] = style

    print(f"正在更新大屏背景...")
    update_url = f"{BISERVER_BASE}/biserver/paas/bi-app/largeScreen/update/{screen_id}"
    response = post(update_url, json=config, headers=headers)

    result = response.json()
    if result.get("result") != "0":
        raise Exception(f"更新大屏失败：{result.get('desc')}")

    print(f"✅ 背景图片设置成功！")
    print(f"   访问地址：{BISERVER_BASE}/largescreenpreview?id={screen_id}")


def ask_set_background(screen_id, image_paths):
    """生成背景设置选项（供 AI 调用）

    Args:
        screen_id: 大屏 ID
        image_paths: 生成的图片路径列表

    Returns:
        dict: 包含选择信息，供 AI 判断下一步操作
    """
    print(f"\n{'=' * 60}")
    if len(image_paths) == 1:
        print(f"✅ 已生成背景图片：")
    else:
        print(f"✅ 已生成 {len(image_paths)} 张背景图片：")

    for i, path in enumerate(image_paths, 1):
        print(f"   {i}. {path}")

    print(f"\n大屏预览：{BISERVER_BASE}/largescreenpreview?id={screen_id}")
    print(f"{'=' * 60}")

    return {
        "screen_id": screen_id,
        "image_paths": image_paths,
        "preview_url": f"{BISERVER_BASE}/largescreenpreview?id={screen_id}",
    }


def main():
    parser = argparse.ArgumentParser(description="为数字大屏生成背景图片")

    parser.add_argument("--screen-id", type=int, required=True, help="大屏 ID")
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="自定义 prompt（如果不提供则显示布局信息）",
    )
    parser.add_argument("--output-dir", type=str, default=None, help="输出目录")
    args = parser.parse_args()

    print(f"📥 正在获取大屏 {args.screen_id} 的配置...")
    screen_config = get_screen_config(args.screen_id)
    layout_info = parse_layout_info(screen_config)

    print_layout_summary(layout_info)

    if args.prompt:
        api_key = get_api_credentials()
        if api_key is None:
            print("ERROR: 未找到 API 密钥")
            sys.exit(1)

        output_dir = args.output_dir or str(CACHE_DIR / "backgrounds")
        print(f"\n🎨 正在生成背景图片...")
        print(f"📝 Prompt: {args.prompt}")
        image_paths = generate_background(
            args.prompt,
            layout_info["canvas_width"],
            layout_info["canvas_height"],
            api_key,
            output_dir,
        )

        print("\n" + "=" * 60)
        result = ask_set_background(args.screen_id, image_paths)
        print(f"\nAI 可根据以上信息询问用户是否设置背景")
    else:
        print("\n" + "=" * 60)
        print("💡 大模型可以根据以上布局信息决定合适的 prompt")
        print("   然后用 --prompt 参数执行生成")
        print("=" * 60)


if __name__ == "__main__":
    main()
