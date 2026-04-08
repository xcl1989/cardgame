#!/usr/bin/env python3
"""
修改大屏组件标题脚本

使用方式:
python3 scripts/rename_component.py \
  --screen-id 3654218321 \
  --uuid "grid-type:bar-uuid:1773823950771" \
  --title "月度收款趋势分析"

原理：组件标题存储在大屏配置的 3 个位置，必须同时修改：
1. config.layers[].title - 图层标题（显示在画布上）
2. componentMap[uuid].viewName - 组件视图名称（显示数据标题）
3. layouts[].title - 布局标题（组件列表显示）
"""

import json
import requests
import argparse
from pathlib import Path

from auth import load_headers, get_preview_url, get, post


def rename_component(
    screen_id: int,
    uuid: str,
    new_title: str,
    base_url: str = "https://dev.cloud.hecom.cn",
) -> bool:
    """修改大屏组件标题"""

    headers = load_headers()

    print(f"正在获取大屏配置 (ID: {screen_id})...")

    # 获取大屏配置
    url = f"{base_url}/biserver/paas/bi-app/largeScreen/get/{screen_id}"
    resp = get(url, headers=headers)
    data = resp.json()

    if data.get("result") != "0":
        print(f"❌ 获取大屏失败：{data.get('desc')}")
        return False

    config = data["data"]

    # 修改三个位置的标题
    modified = False

    # 1. 修改 layer 中的 title
    for layer in config["config"]["layers"]:
        if layer["uuid"] == uuid:
            layer["title"] = new_title
            modified = True
            print(f"✓ 已修改 layer.title: {new_title}")

    # 2. 修改 componentMap 中的 viewName
    if uuid in config["componentMap"]:
        config["componentMap"][uuid]["viewName"] = new_title
        modified = True
        print(f"✓ 已修改 component.viewName: {new_title}")
    else:
        print(f"⚠ 未找到 UUID 为 {uuid} 的组件")

    # 3. 修改 layout 中的 title
    for layout in config["layouts"]:
        if layout["uuid"] == uuid:
            layout["title"] = new_title
            modified = True
            print(f"✓ 已修改 layout.title: {new_title}")

    if not modified:
        print(f"❌ 未找到 UUID 为 {uuid} 的组件")
        return False

    # 提交更新
    print(f"正在更新大屏...")
    update_url = f"{base_url}/biserver/paas/bi-app/largeScreen/update/{screen_id}"
    config["id"] = screen_id
    resp = post(update_url, json=config, headers=headers)
    result = resp.json()

    if result.get("result") == "0":
        print(f"\n✅ 组件标题已修改为：{new_title}")
        print(f"访问 URL: {get_preview_url(screen_id, base_url)}")
        return True
    else:
        print(f"\n❌ 更新失败：{result.get('desc')}")
        return False


def main():
    parser = argparse.ArgumentParser(description="修改大屏组件标题")
    parser.add_argument("--screen-id", type=int, required=True, help="大屏 ID")
    parser.add_argument(
        "--uuid", required=True, help="组件 UUID (格式：grid-type:bar-uuid:123)"
    )
    parser.add_argument("--title", required=True, help="新标题")
    from auth import get_base_url

    parser.add_argument("--base-url", default=get_base_url(), help="API 基础 URL")
    parser.add_argument(
        "--env",
        default="dev",
        choices=["dev", "test", "prod"],
        help="环境 (默认 dev，与 --base-url 二选一)",
    )
    args = parser.parse_args()

    base_url = args.base_url if args.base_url else get_base_url(args.env)
    success = rename_component(args.screen_id, args.uuid, args.title, base_url)
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
