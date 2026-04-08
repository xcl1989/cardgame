#!/usr/bin/env python3
"""
删除大屏组件脚本
用于通过 API 删除大屏中的一个或多个组件

使用示例：
    # 删除单个组件
    python3 scripts/delete_component.py --screen-id 3654239893 --uuid "grid-type:bar-uuid:xxx"
    
    # 删除多个组件
    python3 scripts/delete_component.py --screen-id 3654239893 \
        --uuid "grid-type:bar-uuid:xxx" \
        --uuid "grid-type:line-uuid:yyy"
    
    # 查看大屏组件列表
    python3 scripts/delete_component.py --screen-id 3654239893 --list
"""

import json
import requests
import argparse
from pathlib import Path
from typing import Dict, List, Optional

from auth import load_headers, get_preview_url, get_base_url, get, post


class BiComponentDeleter:
    """BI 大屏组件删除器"""

    def __init__(self, base_url: str = "https://dev.cloud.hecom.cn"):
        self.base_url = base_url
        self.headers = load_headers()
        self.cookies = {}

    def get_screen(self, screen_id: int) -> Dict:
        """获取大屏配置"""
        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/get/{screen_id}"
        response = get(url, headers=self.headers, cookies=self.cookies)
        data = response.json()

        if data.get("result") == "0":
            return data.get("data", {})
        raise Exception(f"获取大屏失败：{data.get('desc')}")

    def update_screen(self, screen_id: int, config: Dict) -> bool:
        """更新大屏配置"""
        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/update/{screen_id}"
        response = post(url, json=config, headers=self.headers, cookies=self.cookies)
        data = response.json()

        if data.get("result") == "0":
            return True
        raise Exception(f"更新大屏失败：{data.get('desc')}")

    def list_components(self, screen_id: int):
        """列出大屏所有组件"""
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id)

        print(f"\n=== 大屏基本信息 ===")
        print(f"名称：{screen_data.get('name')}")
        print(f"ID: {screen_id}")

        config = screen_data.get("config", {})
        layers = config.get("layers", []) if isinstance(config, dict) else []
        print(f"\n=== 图层数量：{len(layers)} ===")

        for i, layer in enumerate(layers, 1):
            print(f"{i}. {layer.get('title', 'N/A')}")
            print(f"   UUID: {layer.get('uuid')}")
            print(f"   位置：top={layer.get('top')}, left={layer.get('left')}")
            print(f"   大小：width={layer.get('width')}, height={layer.get('height')}")
            print()

        component_map = screen_data.get("componentMap", {})
        print(f"=== 数据组件数量：{len(component_map)} ===")

        if not component_map:
            print("(无数据组件)")
            return

        for uuid, comp in component_map.items():
            model_id = comp.get("modelId")
            view_name = comp.get("viewName", "")
            comp_type = comp.get("type", "unknown")

            print(f"\n组件：{view_name} ({comp_type})")
            print(f"  UUID: {uuid}")
            print(f"  模型 ID: {model_id}")

    def delete_components(self, screen_id: int, uuids: List[str]) -> bool:
        """删除指定的组件"""
        print(f"正在获取大屏配置...")
        screen_data = self.get_screen(screen_id)

        config = screen_data.get("config", {})
        layers = config.get("layers", [])
        layouts = screen_data.get("layouts", [])
        component_map = screen_data.get("componentMap", {})

        original_layer_count = len(layers)
        original_layout_count = len(layouts)
        original_comp_count = len(component_map)

        print(f"删除前：图层={original_layer_count}, 组件={original_comp_count}")
        print(f"准备删除 {len(uuids)} 个组件:")
        for uuid in uuids:
            print(f"  - {uuid}")

        # 从 layers 中删除
        layers = [l for l in layers if l.get("uuid") not in uuids]

        # 从 layouts 中删除
        layouts = [l for l in layouts if l.get("uuid") not in uuids]

        # 从 componentMap 中删除
        for uuid in uuids:
            component_map.pop(uuid, None)

        # 更新配置
        config["layers"] = layers
        config["layersCount"] = len(layers)

        update_data = {
            "id": screen_id,
            "name": screen_data.get("name"),
            "config": config,
            "layouts": layouts,
            "componentMap": component_map,
            "topLayouts": screen_data.get("topLayouts", []),
        }

        print(f"\n正在提交更新...")
        self.update_screen(screen_id, update_data)

        print(f"\n✅ 成功删除 {len(uuids)} 个组件!")
        print(f"剩余图层：{len(layers)} (原 {original_layer_count})")
        print(f"剩余组件：{len(component_map)} (原 {original_comp_count})")

        return True


def main():
    parser = argparse.ArgumentParser(
        description="删除大屏组件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 查看组件列表
  python3 scripts/delete_component.py --screen-id 3654239893 --list
  
  # 删除单个组件
  python3 scripts/delete_component.py --screen-id 3654239893 --uuid "grid-type:bar-uuid:xxx"
  
  # 删除多个组件
  python3 scripts/delete_component.py --screen-id 3654239893 \\
      --uuid "grid-type:bar-uuid:xxx" \\
      --uuid "grid-type:line-uuid:yyy"
        """,
    )

    parser.add_argument(
        "--screen-id",
        type=int,
        required=True,
        help="大屏 ID",
    )

    parser.add_argument(
        "--uuid",
        action="append",
        dest="uuids",
        help="要删除的组件 UUID (可指定多个)",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_mode",
        help="列出所有组件",
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
    deleter = BiComponentDeleter(base_url)

    try:
        if args.list_mode:
            deleter.list_components(args.screen_id)
        elif args.uuids:
            deleter.delete_components(args.screen_id, args.uuids)
        else:
            print("❌ 请指定 --uuid 或 --list 参数")
            parser.print_help()
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        exit(1)


if __name__ == "__main__":
    main()
