# 3D柱图组件使用指南

## 概述

3D柱图（3D Bar Chart）是具有立体视觉效果的数据可视化组件，适合展示：
- 时间趋势和分类对比
- 数据强调和视觉突出
- 需要立体效果的展示场景
- 与普通柱图配合形成对比效果

## 与普通柱图的区别

| 特性 | 普通柱图 (bar) | 3D柱图 (bar3d) |
|------|--------------|---------------|
| 视觉效果 | 平面2D | 立体3D |
| 图表类型值 | `bar` | `bar3d` |
| 适用场景 | 常规数据展示 | 强调、突出展示 |

## 使用方法

### 基础示例

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type bar3d \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --view-name "3D收款趋势"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654239893 |
| --model-id | 是 | 数据模型 ID | 2597080602 |
| --dimension-field | 是 | 维度字段（X轴） | receivingDate |
| --indicator-field | 是 | 指标字段 | receivingAmount |
| --chart-type | 是 | 图表类型，固定为 `bar3d` | bar3d |
| --top | 是 | Y 坐标 | 200 |
| --left | 是 | X 坐标 | 50 |
| --width | 是 | 组件宽度 | 450 |
| --height | 是 | 组件高度 | 300 |
| --view-name | 否 | 视图标题 | "3D收款趋势" |
| --bar-legend-position | 否 | 图例位置 | bottom/top/left/right |
| --bar-scroll-enabled | 否 | 是否启用滚动 | true/false |
| --bar-scroll-speed | 否 | 滚动速度（1-10） | 5 |
| --bar-label-show | 否 | 是否显示数据标签 | true/false |
| --bar-label-position | 否 | 标签位置 | top/right/bottom/auto |
| --bar-axis-rotate | 否 | X轴标签旋转角度 | 0-45 |

### 尺寸建议

| 场景 | 推荐宽度 | 推荐高度 | 说明 |
|------|---------|---------|------|
| 主图表区 | 450-550 | 300-350 | 展示 10-15 个周期 |
| 小型图表 | 300-350 | 200-250 | 辅助展示 5-8 个周期 |
| 宽屏布局 | 600-700 | 280-320 | 横向空间充足时 |

## 样式配置

### 完整样式结构

```json
{
  "screenPosition": {
    "position": {"x": 50, "y": 200, "w": 450, "h": 300}
  },
  "textData": {"show": false},
  "legend": {
    "isExtra": true,
    "textSetMap": {
      "size": 14,
      "textItalic": false,
      "textBold": false,
      "fontSize": 14,
      "textColor": "#177DDC"
    },
    "position": "top"
  },
  "tooltip": {
    "backgroundColor": "#303467",
    "isExtra": true,
    "textSetMap": {
      "size": 12,
      "textItalic": false,
      "textBold": false,
      "fontSize": 12,
      "textColor": "#A6ADD0"
    },
    "content": ["dimension", "measure"]
  },
  "scroll": {
    "cycleSpeed": 5,
    "show": true,
    "type": "highlight"
  },
  "drawSettings": {
    "type": "cube",
    "cubeColorSystem": "#4CC9F0",
    "seriesType": "bar",
    "widthMap": {"isAdaption": true}
  },
  "label": {
    "isExtra": true,
    "show": false,
    "textSetMap": {
      "size": 12,
      "textItalic": false,
      "textBold": false,
      "fontSize": 12,
      "textColor": "#A6ADD0"
    },
    "position": "auto"
  },
  "title": {
    "isExtra": true,
    "show": true,
    "textSetMap": {
      "textItalic": false,
      "textBold": true,
      "fontSize": 16,
      "align": "left",
      "textColor": "#FEFEFE"
    },
    "title": "3D收款趋势"
  },
  "axis": {
    "x": {
      "rotate": 0,
      "axes": ["showXAxis"],
      "scale": "auto"
    },
    "y": {
      "axes": ["showYAxis", "showAxisLine"],
      "splitMap": {"isChecked": true},
      "titleMap": {"isChecked": true, "value": ""}
    }
  },
  "card": {
    "border": "rgba(30, 39, 55, 0.8)",
    "padding": 12,
    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
    "lineWidthMap": {"width": 1, "style": "solid"}
  }
}
```

### 关键样式说明

#### 1. 3D效果配置
```json
"drawSettings": {
  "type": "cube",
  "cubeColorSystem": "#4CC9F0",
  "seriesType": "bar",
  "widthMap": {"isAdaption": true}
}
```
- `type`: 固定为 `"cube"` 表示3D立方体效果
- `cubeColorSystem`: 3D柱子的颜色（如 `#4CC9F0`）
- `seriesType`: 图表类型，固定为 `"bar"`

#### 2. 图例配置
```json
"legend": {
  "isExtra": true,
  "textSetMap": {
    "size": 14,
    "textColor": "#177DDC"
  },
  "position": "top"
}
```
- `position`: 图例位置（默认 top，可选 bottom/left/right）

#### 3. 滚动配置
```json
"scroll": {
  "cycleSpeed": 5,
  "show": true,
  "type": "highlight"
}
```
- `show`: 是否启用滚动（默认 true）
- `type`: `highlight` 高亮滚动
- `cycleSpeed`: 滚动速度（1-10，默认 5）

#### 4. 数据标签
```json
"label": {
  "isExtra": true,
  "show": false,
  "position": "auto"
}
```
- `show`: 是否显示数值标签（默认 false）
- `position`: 标签位置（top/right/bottom/auto）

## 实战案例

### 案例 1：3D月度收款趋势

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type bar3d \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --view-name "3D月度收款趋势"
```

### 案例 2：3D柱图显示数据标签

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type bar3d \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --bar-label-show true \
  --bar-label-position top \
  --view-name "3D月度收款趋势"
```

### 案例 3：关闭滚动效果

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type bar3d \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --bar-scroll-enabled false \
  --view-name "3D月度收款趋势"
```

## 与普通柱图配合

### 布局建议

```
+----------------------------------+
| [指标卡 1] [指标卡 2] [指标卡 3]  |
+----------------------------------+
|                                  |
|  [普通柱图]    [3D柱图]   [饼图]  |
|  (常规展示)    (强调效果)  (占比)  |
|                                  |
+----------------------------------+
|        [底部明细表格]             |
+----------------------------------+
```

### 选择建议

**使用普通柱图 (bar)**：
- 常规数据展示
- 需要精确对比数值
- 数据量较大（>8 个类别）

**使用3D柱图 (bar3d)**：
- 需要视觉强调和突出
- 数据量适中（<10 个类别）
- 配合普通柱图形成对比效果

## 注意事项

### 1. 数据排序
- 默认按指标值降序排列
- 可通过 `--indicator-order-type` 控制排序

### 2. X轴标签显示
- 标签过长时使用 `--bar-axis-rotate 30` 旋转
- 或增加组件宽度

### 3. 滚动效果
- 数据超过显示区域自动滚动
- 调整 `--bar-scroll-speed` 控制速度

### 4. 3D效果
- 3D柱图默认使用立方体效果
- 颜色可通过 `cubeColorSystem` 自定义

## 常见问题

### Q1: 3D效果不显示？
- 确保 `--chart-type` 参数值为 `bar3d`（不是 `bar`）
- 检查 `drawSettings.type` 是否为 `"cube"`

### Q2: X轴标签重叠？
- 增加组件宽度
- 使用 `--bar-axis-rotate 30` 旋转标签
- 减少显示的数据条数

### Q3: 如何显示数值？
- 添加 `--bar-label-show true`
- 调整位置 `--bar-label-position top`

### Q4: 滚动速度不合适？
- 使用 `--bar-scroll-speed 3` 慢速
- 使用 `--bar-scroll-speed 8` 快速

## 参考资源

- [SKILL.md](../../SKILL.md) - 技能主文档
- [add_component.py](./add_component.py) - 组件添加脚本
- [update_screen.py](./update_screen.py) - 组件更新脚本
- [BAR_COMPONENT_GUIDE.md](./BAR_COMPONENT_GUIDE.md) - 普通柱图组件指南
