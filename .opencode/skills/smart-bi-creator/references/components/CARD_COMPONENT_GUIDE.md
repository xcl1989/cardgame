# 卡片组件使用指南

## 概述

卡片组件（Card Component）是纯容器组件，用于为其他图表组件提供背景容器。适用于大屏布局中需要分组展示多个图表的场景，如模版31中的多列布局。

## 组件特点

### 1. 纯容器组件
- 不需要配置维度和指标
- 不绑定数据源
- 仅提供视觉背景容器

### 2. 样式特点
- 半透明深色背景
- 圆角边框
- 可叠加其他图表组件

### 3. 典型用途
- 图表分组容器（如左/中/右三列布局）
- 视觉层次分隔
- 区域背景装饰

## 使用方法

### 添加卡片组件

```bash
python3 scripts/add_component.py \
  --screen-id 3654958357 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type card \
  --top 80 --left 15 \
  --width 412 --height 320 \
  --view-name "卡片1"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654958357 |
| --model-id | 是 | 数据模型 ID | 2597080602 |
| --dimension-field | 是 | 维度字段（可任意填） | receivingDate |
| --indicator-field | 是 | 指标字段（可任意填） | receivingAmount |
| --chart-type | 是 | 固定为 `card` | card |
| --top | 是 | Y 坐标 | 80 |
| --left | 是 | X 坐标 | 15 |
| --width | 是 | 组件宽度 | 412 |
| --height | 是 | 组件高度 | 320 |
| --view-name | 否 | 视图名称 | "卡片1" |

## 典型布局（模版31）

### 布局结构

```
画布：1920×1080

+--------------------------------------------------+
| top=0: 头部装饰 (1920×80)                        |
+--------------------------------------------------+
| top=80:                                          |
|   left=15: 卡片容器 (412×320)                    |
|     └─ 水平条形图 (411×319)                     |
|   left=1492: 卡片容器 (412×320)                  |
|     └─ 排名图 (411×319)                         |
+--------------------------------------------------+
| top=412:                                         |
|   left=15: 卡片容器 (412×326)                    |
|     └─ 饼图 (410×325)                            |
|   left=1492: 卡片容器 (412×326)                  |
|     └─ 漏斗图 (410×326)                         |
+--------------------------------------------------+
| top=752:                                         |
|   left=15: 卡片容器 (412×320)                    |
|     └─ 仪表盘 (411×319)                         |
|   left=444: 卡片容器 (1032×320)                  |
|     └─ 折线图 (1030×319)                         |
|   left=1492: 卡片容器 (412×320)                  |
|     └─ 柱图 (412×319)                            |
+--------------------------------------------------+
```

### 创建命令序列

```bash
# 顶部左侧卡片
python3 scripts/add_component.py \
  --screen-id 3654958357 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type card \
  --top 80 --left 15 --width 412 --height 320 \
  --view-name "卡片1"

# 顶部右侧卡片
python3 scripts/add_component.py \
  --screen-id 3654958357 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type card \
  --top 80 --left 1492 --width 412 --height 320 \
  --view-name "卡片1"

# 中部左侧卡片
python3 scripts/add_component.py \
  --screen-id 3654958357 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type card \
  --top 412 --left 15 --width 412 --height 326 \
  --view-name "卡片1"

# 中部右侧卡片
python3 scripts/add_component.py \
  --screen-id 3654958357 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type card \
  --top 412 --left 1492 --width 412 --height 326 \
  --view-name "卡片1"

# 底部三个卡片
python3 scripts/add_component.py \
  --screen-id 3654958357 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type card \
  --top 752 --left 15 --width 412 --height 320 \
  --view-name "卡片1"

python3 scripts/add_component.py \
  --screen-id 3654958357 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type card \
  --top 752 --left 444 --width 1032 --height 320 \
  --view-name "卡片1"

python3 scripts/add_component.py \
  --screen-id 3654958357 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type card \
  --top 752 --left 1492 --width 412 --height 320 \
  --view-name "卡片1"
```

## 样式配置

### 完整样式结构

```json
{
  "styleJson": {
    "decorate": {},
    "screenPosition": {
      "position": {"x": 15, "y": 80, "w": 412, "h": 320}
    },
    "decorateStyle": {
      "selectedDecorate": "cardDecorate/cardDecorate3.png"
    }
  },
  "templateId": "grid-type:card-uuid:1773985862233",
  "viewName": "卡片1"
}
```

### 关键样式说明

| 字段 | 说明 |
|------|------|
| screenPosition.position.x | 左侧坐标 |
| screenPosition.position.y | 顶部坐标 |
| screenPosition.position.w | 宽度 |
| screenPosition.position.h | 高度 |
| decorateStyle.selectedDecorate | 装饰图片路径 |

## 调整卡片位置

使用 `update_screen.py` 调整卡片组件的位置：

```bash
# 修改卡片位置和大小
python3 scripts/update_screen.py \
  --screen-id 3654958357 \
  --uuid "grid-type:card-uuid:1773985862233" \
  --top 100 --left 200 --width 400 --height 300
```

## 注意事项

### 1. 尺寸要求
- 宽度建议 400-1200px
- 高度建议 300-600px
- 应能容纳内部图表组件

### 2. 层级关系
- 卡片容器应先于内部图表添加
- 内部图表叠加在卡片上方
- 调整图层顺序使用 `--move-layer` 参数

### 3. 位置规划
- 规划好整体布局再添加
- 避免卡片之间重叠
- 预留组件间距

## 与其他组件配合

### 典型组合：卡片 + 图表

```bash
# 1. 先添加卡片容器
python3 scripts/add_component.py \
  --screen-id 3654958357 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type card \
  --top 80 --left 15 --width 412 --height 320 \
  --view-name "卡片1"

# 2. 再添加图表组件（叠加在卡片上方）
python3 scripts/add_component.py \
  --screen-id 3654958357 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type horizontalBar \
  --top 80 --left 16 --width 411 --height 319 \
  --view-name "项目收款对比"
```

## 图层顺序调整

如果图表组件被卡片遮挡，可以使用 `--move-layer` 调整层级：

```bash
# 将图表移到卡片上方
python3 scripts/update_screen.py \
  --screen-id 3654958357 \
  --uuid "grid-type:horizontalBar-uuid:1773985554109" \
  --move-layer top

# 将图表下移一层
python3 scripts/update_screen.py \
  --screen-id 3654958357 \
  --uuid "grid-type:horizontalBar-uuid:1773985554109" \
  --move-layer down
```

## 常见问题

### Q1: 卡片组件看不到？
- 检查组件位置是否正确
- 检查是否有其他组件遮挡
- 确认尺寸不为 0

### Q2: 图表被卡片遮挡？
- 使用 `--move-layer top` 将图表移到最顶层
- 或使用 `--move-layer up` 逐步上移

### Q3: 如何复制卡片样式？
```bash
python3 scripts/update_screen.py \
  --screen-id 3654958357 \
  --clone-style-from "grid-type:card-uuid:源UUID" \
  --clone-style-to "grid-type:card-uuid:目标UUID"
```

## 参考资源

- [SKILL.md](../../SKILL.md) - 技能主文档
- [add_component.py](../../scripts/add_component.py) - 组件添加脚本
- [update_screen.py](../../scripts/update_screen.py) - 组件更新脚本
- [TEMPLATE_DIGITAL_SCREEN_31.md](../layouts/TEMPLATE_DIGITAL_SCREEN_31.md) - 模版31布局参考
