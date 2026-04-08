#!/usr/bin/env python3
"""
大屏布局检查工具
检查项目：
1. 组件是否超出画布边界
2. 组件之间是否重叠
3. 是否存在大片空白区域
"""

import requests
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass

from auth import load_headers, get_base_url, get


@dataclass
class Component:
    """组件信息"""

    uuid: str
    title: str
    type: str
    top: int
    left: int
    width: int
    height: int

    @property
    def right(self) -> int:
        return self.left + self.width

    @property
    def bottom(self) -> int:
        return self.top + self.height

    def overlaps_with(self, other: "Component") -> bool:
        """检查是否与另一个组件重叠"""
        # 没有重叠的情况
        if self.right <= other.left + 10:  # 留 10px 间距
            return False
        if self.left >= other.right - 10:
            return False
        if self.bottom <= other.top + 10:
            return False
        if self.top >= other.bottom - 10:
            return False
        return True

    def get_overlap_area(self, other: "Component") -> int:
        """计算重叠面积"""
        overlap_left = max(self.left, other.left)
        overlap_right = min(self.right, other.right)
        overlap_top = max(self.top, other.top)
        overlap_bottom = min(self.bottom, other.bottom)

        if overlap_left >= overlap_right or overlap_top >= overlap_bottom:
            return 0

        return (overlap_right - overlap_left) * (overlap_bottom - overlap_top)

    def __str__(self):
        return f"{self.title} [{self.type}]: [{self.left}, {self.top}, {self.width}×{self.height}]"


class LayoutChecker:
    """布局检查器"""

    # 各类组件的最小高度要求
    MIN_HEIGHTS = {
        "metric": 110,  # 指标卡最小高度
        "bar": 250,  # 柱状图最小高度
        "line": 250,  # 折线图最小高度
        "pie": 250,  # 饼图最小高度
        "ranking": 250,  # 排名图最小高度
        "horizontalBar": 250,  # 条形图最小高度
        "table": 200,  # 表格最小高度
        "default": 200,  # 默认最小高度
    }

    def __init__(
        self,
        screen_id: int,
        canvas_width: int = 1920,
        canvas_height: int = 1080,
        base_url: str = "",
        env: str = "dev",
    ):
        self.screen_id = screen_id
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.base_url = base_url or get_base_url(env)
        self.components: List[Component] = []
        self.headers = load_headers()

    def fetch_screen_info(self) -> Dict:
        """获取大屏配置"""
        url = f"{self.base_url}/biserver/paas/bi-app/largeScreen/get/{self.screen_id}"
        response = get(url, headers=self.headers)
        data = response.json()
        if data.get("result") == "0":
            return data.get("data", {})
        raise Exception(f"获取大屏失败：{data.get('desc')}")

    def parse_components(self, screen_data: Dict):
        """解析组件信息"""
        config = screen_data.get("config", {})
        layers = config.get("layers", [])
        component_map = screen_data.get("componentMap", {})

        self.components = []
        for layer in layers:
            uuid = layer.get("uuid", "")
            layer_type = layer.get("type", "unknown")
            top = layer.get("top", 0)
            left = layer.get("left", 0)
            width = layer.get("width", 100)
            height = layer.get("height", 100)

            title = "未命名"
            if uuid in component_map:
                comp_info = component_map[uuid]
                title = comp_info.get("viewName", "未命名")
                style_json = comp_info.get("styleJson", {})
                chart_type = style_json.get("chartType", "")
                if chart_type:
                    layer_type = chart_type
                elif "metric" in uuid:
                    layer_type = "metric"
                elif "bar" in uuid:
                    layer_type = "bar"
                elif "line" in uuid:
                    layer_type = "line"
                elif "pie" in uuid:
                    layer_type = "pie"
                elif "ranking" in uuid:
                    layer_type = "ranking"
                elif "customTable" in uuid or "table" in uuid:
                    layer_type = "table"
                elif "horizontalBar" in uuid:
                    layer_type = "horizontalBar"
                elif "flipper" in uuid:
                    layer_type = "flipper"
                elif "text" in uuid:
                    layer_type = "text"
                elif "head" in uuid:
                    layer_type = "head"
                elif "script" in uuid:
                    layer_type = "script"

            self.components.append(
                Component(
                    uuid=uuid,
                    title=title,
                    type=layer_type,
                    top=top,
                    left=left,
                    width=width,
                    height=height,
                )
            )

    def check_boundaries(self) -> List[str]:
        """检查是否有组件超出画布"""
        issues = []
        for comp in self.components:
            # 检查右边界
            if comp.right > self.canvas_width:
                overflow = comp.right - self.canvas_width
                issues.append(
                    f"❌ 超出右边界：{comp.title} 右边界 {comp.right}px "
                    f"(超出 {overflow}px)"
                )
            # 检查下边界
            if comp.bottom > self.canvas_height:
                overflow = comp.bottom - self.canvas_height
                issues.append(
                    f"❌ 超出下边界：{comp.title} 下边界 {comp.bottom}px "
                    f"(超出 {overflow}px)"
                )
            # 检查左边界（负数）
            if comp.left < 0:
                issues.append(f"❌ 超出左边界：{comp.title} 左边界 {comp.left}px")
            # 检查上边界（负数）
            if comp.top < 0:
                issues.append(f"❌ 超出上边界：{comp.title} 上边界 {comp.top}px")
        return issues

    def check_overlaps(self) -> List[str]:
        """检查组件重叠"""
        issues = []
        n = len(self.components)
        for i in range(n):
            for j in range(i + 1, n):
                comp1 = self.components[i]
                comp2 = self.components[j]
                if comp1.overlaps_with(comp2):
                    area = comp1.get_overlap_area(comp2)
                    issues.append(
                        f"❌ 组件重叠：{comp1.title} ↔ {comp2.title} "
                        f"(重叠面积：{area}px²)"
                    )
        return issues

    def check_empty_areas(
        self, min_width: int = 300, min_height: int = 200
    ) -> List[str]:
        """检查大片空白区域（排除头部装饰下方的正常留白）"""
        issues = []

        # 找出头部装饰的底部位置，排除其下方正常留白的干扰
        head_bottom = 0
        for comp in self.components:
            if comp.type == "head":
                head_bottom = max(head_bottom, comp.bottom)

        # 将画布划分为网格进行检查
        grid_size = 50  # 50px 网格
        canvas_grid = [
            [False] * (self.canvas_width // grid_size)
            for _ in range(self.canvas_height // grid_size)
        ]

        # 标记被组件覆盖的网格（向上取整，确保不漏掉边角）
        for comp in self.components:
            start_x = max(0, comp.left // grid_size)
            end_x = min(len(canvas_grid[0]), (comp.right + grid_size - 1) // grid_size)
            start_y = max(0, comp.top // grid_size)
            end_y = min(len(canvas_grid), (comp.bottom + grid_size - 1) // grid_size)

            for y in range(start_y, end_y):
                for x in range(start_x, end_x):
                    canvas_grid[y][x] = True

        # 查找空白区域
        empty_areas = []
        visited = [[False] * len(canvas_grid[0]) for _ in range(len(canvas_grid))]

        def find_empty_area(start_x, start_y):
            """使用 BFS 查找连续的空白区域"""
            queue = [(start_x, start_y)]
            area_points = []
            min_x, min_y = start_x, start_y
            max_x, max_y = start_x, start_y

            while queue:
                x, y = queue.pop(0)
                if (
                    0 <= x < len(canvas_grid[0])
                    and 0 <= y < len(canvas_grid)
                    and not canvas_grid[y][x]
                    and not visited[y][x]
                ):
                    visited[y][x] = True
                    area_points.append((x, y))
                    queue.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

            if area_points:
                width = (max_x - min_x + 1) * grid_size
                height = (max_y - min_y + 1) * grid_size
                if width >= min_width and height >= min_height:
                    # 排除头部装饰下方的大片留白（这是正常设计空间）
                    if head_bottom > 0:
                        area_top_px = min_y * grid_size
                        area_bottom_px = (max_y + 1) * grid_size
                        if (
                            area_top_px >= head_bottom
                            and width >= self.canvas_width * 0.8
                            and area_top_px < self.canvas_height * 0.4
                        ):
                            return  # 头部下方延伸至画面中上部的大面积空白，可忽略
                    empty_areas.append(
                        {
                            "left": min_x * grid_size,
                            "top": min_y * grid_size,
                            "width": width,
                            "height": height,
                            "area": width * height,
                        }
                    )

        # 查找所有空白区域
        for y in range(len(canvas_grid)):
            for x in range(len(canvas_grid[0])):
                if not canvas_grid[y][x] and not visited[y][x]:
                    find_empty_area(x, y)

        # 按面积排序，报告最大的空白区域
        empty_areas.sort(key=lambda x: x["area"], reverse=True)
        for i, area in enumerate(empty_areas[:5], 1):  # 只报告前 5 个最大的
            issues.append(
                f"⚠️ 空白区域 #{i}: 位置 [{area['left']}, {area['top']}] "
                f"大小 {area['width']}×{area['height']} "
                f"(面积：{area['area'] // 10000} 万 px²)"
            )

        return issues

    def check_min_heights(self) -> List[str]:
        """检查组件高度是否满足最小要求"""
        issues = []
        for comp in self.components:
            # 跳过装饰组件和文本组件
            if comp.type in ["decorate", "head", "text", "time", "marquee", "unknown"]:
                continue

            # 获取组件类型对应的最小高度
            min_height = self.MIN_HEIGHTS.get(comp.type, self.MIN_HEIGHTS["default"])

            if comp.height < min_height:
                issues.append(
                    f"❌ 高度不足：{comp.title} 高度 {comp.height}px "
                    f"(最小要求 {min_height}px，建议增加 {min_height - comp.height}px)"
                )

        return issues

    def generate_summary(self):
        """生成布局摘要"""
        print("\n" + "=" * 80)
        print(f"📊 大屏布局检查报告 - 大屏 ID: {self.screen_id}")
        print("=" * 80)

        print(f"\n📐 画布尺寸：{self.canvas_width} × {self.canvas_height}")
        print(f" 组件数量：{len(self.components)}")

        print("\n📋 组件列表:")
        print(f"{'序号':<4} {'名称':<20} {'类型':<12} {'位置':<25} {'大小':<15}")
        print("-" * 80)
        for i, comp in enumerate(self.components, 1):
            pos = f"[{comp.left}, {comp.top}]"
            size = f"{comp.width}×{comp.height}"
            print(f"{i:<4} {comp.title:<20} {comp.type:<12} {pos:<25} {size:<15}")

        print("\n" + "=" * 80)
        print("🔍 检查结果:")
        print("=" * 80)

    def run_check(self):
        """运行完整检查"""
        # 获取大屏信息
        print("正在获取大屏配置...")
        screen_data = self.fetch_screen_info()
        self.parse_components(screen_data)

        # 生成摘要
        self.generate_summary()

        # 检查边界
        boundary_issues = self.check_boundaries()
        print(f"\n1️⃣ 边界检查 (发现 {len(boundary_issues)} 个问题):")
        if boundary_issues:
            for issue in boundary_issues:
                print(f"   {issue}")
        else:
            print("   ✅ 所有组件都在画布范围内")

        # 检查重叠
        overlap_issues = self.check_overlaps()
        print(f"\n2️⃣ 重叠检查 (发现 {len(overlap_issues)} 个问题):")
        if overlap_issues:
            for issue in overlap_issues:
                print(f"   {issue}")
        else:
            print("   ✅ 没有组件重叠")

        # 检查空白区域
        empty_issues = self.check_empty_areas()
        print(f"\n3️⃣ 空白区域检查:")
        if empty_issues:
            for issue in empty_issues:
                print(f"   {issue}")
        else:
            print("   ✅ 没有发现明显空白区域")

        # 检查组件最小高度
        height_issues = self.check_min_heights()
        print(f"\n4️⃣ 组件高度检查:")
        if height_issues:
            for issue in height_issues:
                print(f"   {issue}")
        else:
            print("   ✅ 所有组件高度合理")

        # 总结
        total_issues = len(boundary_issues) + len(overlap_issues) + len(height_issues)
        print("\n" + "=" * 80)
        if total_issues == 0:
            print("✅ 布局检查通过！没有发现严重问题。")
        else:
            print(f"❌ 发现 {total_issues} 个问题需要修复！")
        print("=" * 80)

        # 提供自动修复建议
        if total_issues > 0:
            self.print_fix_suggestions(boundary_issues, overlap_issues, height_issues)

        return {
            "boundary_issues": boundary_issues,
            "overlap_issues": overlap_issues,
            "empty_areas": empty_issues,
            "height_issues": height_issues,
            "total_critical": total_issues,
        }

    def print_fix_suggestions(self, boundary_issues, overlap_issues, height_issues):
        """打印自动修复建议"""
        print("\n💡 修复建议:\n")

        # 边界问题修复建议
        if boundary_issues:
            print("1️⃣ 边界问题修复:")
            for issue in boundary_issues:
                if "右边界" in issue:
                    # 提取组件名和超出量
                    print(f"   建议：减小组件宽度或向左移动")
                elif "下边界" in issue:
                    print(f"   建议：减小组件高度或向上移动")
                elif "左边界" in issue:
                    print(f"   建议：向右移动组件 (left >= 0)")
                elif "上边界" in issue:
                    print(f"   建议：向下移动组件 (top >= 0)")
            print()

        # 重叠问题修复建议
        if overlap_issues:
            print("2️⃣ 重叠问题修复:")
            for issue in overlap_issues:
                if "未命名 ↔ 未命名" in issue and "重叠面积：20000px²" in issue:
                    # 头部装饰和标题的重叠，正常情况
                    print(f"   ℹ️  头部装饰和标题重叠（正常设计，可忽略）")
                else:
                    print(f"   建议：调整其中一个组件的位置或大小")
            print()

        # 高度问题修复建议
        if height_issues:
            print("3️⃣ 高度问题修复命令示例:")
            print("   使用以下命令增加组件高度:")
            print("   python3 scripts/update_screen.py \\")
            print("     --screen-id <大屏 ID> \\")
            print('     --uuid "<组件 UUID>" \\')
            print("     --top <y 坐标> --left <x 坐标> \\")
            print("     --width <宽度> --height <建议高度>")
            print()

        # 空白区域修复建议
        print("4️⃣ 空白区域利用建议:")
        print("   - 添加指标卡填满顶部空白")
        print("   - 添加辅助图表填充中部空白")
        print("   - 考虑添加装饰文本或时间组件")
        print()

        # 快速修复命令生成
        print("📝 快速修复命令:")
        print("-" * 80)

        # 为高度不足的组件生成修复命令
        for issue in height_issues:
            # 解析组件信息
            if "高度不足：" in issue:
                comp_name = issue.split("高度不足：")[1].split(" 高度")[0]
                current_height = int(issue.split("高度 ")[1].split("px")[0])
                min_height = int(issue.split("最小要求 ")[1].split("px")[0])
                suggested_height = min_height + 20  # 额外增加 20px 余量

                # 查找组件 UUID
                for comp in self.components:
                    if comp.title == comp_name:
                        print(f"# 修复 {comp_name} 高度不足:")
                        print(f"python3 scripts/update_screen.py \\")
                        print(f"  --screen-id {self.screen_id} \\")
                        print(f'  --uuid "{comp.uuid}" \\')
                        print(f"  --top {comp.top} --left {comp.left} \\")
                        print(f"  --width {comp.width} --height {suggested_height}")
                        print()
                        break


def main():
    import argparse

    parser = argparse.ArgumentParser(description="大屏布局检查工具")
    parser.add_argument("--screen-id", type=int, required=True, help="大屏 ID")
    parser.add_argument("--width", type=int, default=1920, help="画布宽度 (默认 1920)")
    parser.add_argument("--height", type=int, default=1080, help="画布高度 (默认 1080)")
    parser.add_argument(
        "--env", default="dev", choices=["dev", "test", "prod"], help="环境 (默认 dev)"
    )
    parser.add_argument("--base-url", help="API 基础 URL (优先级高于 --env)")

    args = parser.parse_args()

    checker = LayoutChecker(
        screen_id=args.screen_id,
        canvas_width=args.width,
        canvas_height=args.height,
        base_url=args.base_url,
        env=args.env,
    )

    result = checker.run_check()

    # 如果有严重问题，返回非零退出码
    if result["total_critical"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
