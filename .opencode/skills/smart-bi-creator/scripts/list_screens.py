#!/usr/bin/env python3
"""
获取大屏列表脚本 - 支持按名称搜索
使用方式：
1. 获取所有大屏列表
2. 按名称搜索大屏
3. 返回匹配的大屏 ID 和详细信息
"""

import json
import requests
import sys
from pathlib import Path
from typing import Dict, List, Optional

from auth import get_base_url, get_retry, post_retry, post, load_headers


class BiScreenLister:
    """BI 大屏列表器"""

    def __init__(self, base_url: str = "https://dev.cloud.hecom.cn"):
        self.base_url = base_url
        self.headers = load_headers()
        self.cookies = {}

    def list_screens(
        self,
        page_no: int = 1,
        page_size: int = 100,
        sort_field: str = "id",
        desc: bool = True,
    ) -> List[Dict]:
        """获取大屏列表"""
        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/list"
        payload = {
            "pageSize": page_size,
            "pageNo": page_no,
            "sortParam": {"field": sort_field, "asc": 0 if desc else 1},
        }
        response = post(url, json=payload, headers=self.headers, cookies=self.cookies)
        data = response.json()

        if data.get("result") == "0":
            return data.get("data", {}).get("list", [])
        raise Exception(f"获取大屏列表失败：{data.get('desc')}")

    def search_screens(self, keyword: str, case_sensitive: bool = False) -> List[Dict]:
        """按名称搜索大屏"""
        all_screens = self.list_screens()
        matched = []

        for screen in all_screens:
            name = screen.get("name", "")
            if case_sensitive:
                if keyword in name:
                    matched.append(screen)
            else:
                if keyword.lower() in name.lower():
                    matched.append(screen)

        return matched

    def format_screens_for_llm(self, screens: List[Dict]) -> str:
        """格式化大屏列表为大模型可读的格式"""
        if not screens:
            return "未找到匹配的大屏"

        lines = []
        lines.append(f"找到 {len(screens)} 个匹配的大屏：\n")

        for i, screen in enumerate(screens, 1):
            screen_id = screen.get("id")
            name = screen.get("name", "未命名")
            config = screen.get("config", {})
            if isinstance(config, str):
                try:
                    config = json.loads(config)
                except (json.JSONDecodeError, ValueError):
                    config = {}
            elif config is None:
                config = {}

            layers = config.get("layers", []) if isinstance(config, dict) else []
            layer_count = len(layers)
            update_time = screen.get("updateTime", "")

            lines.append(f"{i}. ID: {screen_id}")
            lines.append(f"   名称：{name}")
            lines.append(f"   组件数：{layer_count}")
            lines.append(f"   更新时间：{update_time}")
            lines.append("")

        return "\n".join(lines)

    def print_screen_list(
        self, screens: List[Dict], verbose: bool = False, show_index: bool = False
    ):
        """打印大屏列表"""
        if not screens:
            print("未找到大屏")
            return

        print(f"\n=== 大屏列表 (共 {len(screens)} 个) ===\n")
        if show_index:
            print(f"{'序号':<6} {'ID':<15} {'名称':<40} {'组件数':<10} {'更新时间'}")
            print("-" * 95)
        else:
            print(f"{'ID':<15} {'名称':<40} {'组件数':<10} {'更新时间'}")
            print("-" * 90)

        for i, screen in enumerate(screens):
            screen_id = screen.get("id")
            name = screen.get("name", "未命名")
            config = screen.get("config", {})
            # config 可能是字符串或 None，需要处理
            if isinstance(config, str):
                try:
                    config = json.loads(config)
                except (json.JSONDecodeError, ValueError):
                    config = {}
            elif config is None:
                config = {}
            # 再次检查 config 是否为 dict
            if not isinstance(config, dict):
                print(
                    f"警告：大屏 {screen_id} 的 config 类型异常：{type(config)}",
                    file=sys.stderr,
                )
                config = {}
            layers = config.get("layers", [])
            layer_count = len(layers)
            update_time = screen.get("updateTime", "")

            if verbose:
                print(f"\nID: {screen_id}")
                print(f"名称：{name}")
                print(f"组件数：{layer_count}")
                print(f"更新时间：{update_time}")
                print(
                    f"预览 URL: {self.base_url.split('/biserver')[0] if '/biserver' in self.base_url else self.base_url}/largescreenpreview?id={screen_id}"
                )
                print("-" * 60)
            else:
                name_display = name[:38] + ".." if len(name) > 40 else name
                if show_index:
                    print(
                        f"{i + 1:<6} {screen_id:<15} {name_display:<40} {layer_count:<10} {update_time}"
                    )
                else:
                    print(
                        f"{screen_id:<15} {name_display:<40} {layer_count:<10} {update_time}"
                    )

    def get_screen_by_name(self, name: str, exact: bool = False) -> Optional[Dict]:
        """根据名称获取大屏（返回第一个匹配的）"""
        matched = self.search_screens(name)

        if exact:
            for screen in matched:
                if screen.get("name") == name:
                    return screen
            return None

        return matched[0] if matched else None


def main():
    import argparse

    parser = argparse.ArgumentParser(description="获取大屏列表")
    parser.add_argument("--list", action="store_true", help="列出所有大屏")
    parser.add_argument("--search", help="按名称搜索大屏")
    parser.add_argument(
        "--exact", action="store_true", help="精确匹配名称（与 --search 配合使用）"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    parser.add_argument("--page-no", type=int, default=1, help="页码（默认 1）")
    parser.add_argument(
        "--page-size", type=int, default=100, help="每页数量（默认 100）"
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
    lister = BiScreenLister(base_url)

    try:
        if args.search:
            print(f"搜索大屏：'{args.search}'")
            matched = lister.search_screens(args.search, case_sensitive=args.exact)

            if not matched:
                print("未找到大屏")
                return 0

            # 输出格式化的大屏列表，供大模型分析
            print(lister.format_screens_for_llm(matched))

            # 同时输出传统列表格式
            print("\n=== 详细列表 ===")
            lister.print_screen_list(matched, verbose=args.verbose)

            if len(matched) == 1:
                print(f"\n💡 使用提示：")
                print(
                    f"   修改大屏示例：python3 scripts/update_screen.py --screen-id {matched[0].get('id')} --show-info"
                )
            else:
                print(f"\n💡 使用提示：")
                print(f"   以上 {len(matched)} 个大屏供大模型分析，推荐最合适的一个")
                print(
                    f"   或让用户选择后执行：python3 scripts/update_screen.py --screen-id <ID> --show-info"
                )
        elif args.list:
            screens = lister.list_screens(
                page_no=args.page_no, page_size=args.page_size
            )
            lister.print_screen_list(screens, verbose=args.verbose)
        else:
            parser.print_help()

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
