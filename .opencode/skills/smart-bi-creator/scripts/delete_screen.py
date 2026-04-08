#!/usr/bin/env python3
"""
删除大屏脚本
用于通过 API 删除整个大屏

使用示例：
    # 删除大屏（需用户确认）
    python3 scripts/delete_screen.py --screen-id 3662265901

    # 查看大屏列表
    python3 scripts/delete_screen.py --list
"""

import json
import requests
import argparse
from pathlib import Path
from typing import Dict, List, Optional

from auth import (
    load_headers,
    get_preview_url,
    get_base_url,
    get,
    post,
    _request_with_raise,
)


class BiScreenDeleter:
    """BI 大屏删除器"""

    def __init__(self, base_url: str = "https://dev.cloud.hecom.cn"):
        self.base_url = base_url
        self.headers = load_headers()
        self.cookies = {}

    def list_screens(self) -> List[Dict]:
        """获取大屏列表"""
        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/list"
        payload = {
            "pageNo": 1,
            "pageSize": 100,
        }
        response = post(url, json=payload, headers=self.headers, cookies=self.cookies)
        data = response.json()

        if data.get("result") == "0":
            return data.get("data", {}).get("list", [])
        raise Exception(f"获取大屏列表失败：{data.get('desc')}")

    def get_screen(self, screen_id: int) -> Dict:
        """获取大屏详情"""
        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/get/{screen_id}"
        response = get(url, headers=self.headers, cookies=self.cookies)
        data = response.json()

        if data.get("result") == "0":
            return data.get("data", {})
        raise Exception(f"获取大屏失败：{data.get('desc')}")

    def delete_screen(self, screen_id: int) -> bool:
        """删除指定大屏"""
        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/delete/{screen_id}"
        response = _request_with_raise(
            requests.delete, url, headers=self.headers, cookies=self.cookies
        )
        data = response.json()

        if data.get("result") == "0":
            return True
        raise Exception(f"删除大屏失败：{data.get('desc')}")

    def list_all_screens(self):
        """列出所有大屏"""
        print("正在获取大屏列表...")
        screens = self.list_screens()

        if not screens:
            print("\n未找到任何大屏")
            return

        print(f"\n=== 大屏列表 (共 {len(screens)} 个) ===\n")
        for screen in screens:
            screen_id = screen.get("id")
            print(f"ID: {screen_id}")
            print(f"名称: {screen.get('name')}")
            print(f"创建时间: {screen.get('createTime', 'N/A')}")
            if screen_id:
                print(f"访问地址: {get_preview_url(int(screen_id))}")
            print()

    def confirm_delete(self, screen_id: int) -> bool:
        """确认删除大屏"""
        try:
            screen = self.get_screen(screen_id)
            name = screen.get("name", "未命名大屏")

            print(f"\n⚠️  确认删除大屏")
            print(f"=" * 50)
            print(f"大屏 ID: {screen_id}")
            print(f"大屏名称: {name}")
            print(f"访问地址: {get_preview_url(screen_id)}")
            print(f"=" * 50)

            confirm = input("\n请输入 'yes' 确认删除: ").strip().lower()

            if confirm == "yes":
                return True
            else:
                print("\n❌ 删除操作已取消")
                return False
        except Exception as e:
            print(f"\n❌ 获取大屏信息失败：{e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="删除大屏",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 查看大屏列表
  python3 scripts/delete_screen.py --list

  # 删除大屏（会提示确认）
  python3 scripts/delete_screen.py --screen-id 3662265901
        """,
    )

    parser.add_argument(
        "--screen-id",
        type=int,
        help="要删除的大屏 ID",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_mode",
        help="列出所有大屏",
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
    deleter = BiScreenDeleter(base_url)

    try:
        if args.list_mode:
            deleter.list_all_screens()
        elif args.screen_id:
            if deleter.confirm_delete(args.screen_id):
                print("\n正在删除大屏...")
                deleter.delete_screen(args.screen_id)
                print(f"\n✅ 大屏 {args.screen_id} 已成功删除!")
        else:
            print("❌ 请指定 --screen-id 或 --list 参数")
            parser.print_help()
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        exit(1)


if __name__ == "__main__":
    main()
