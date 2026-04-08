# 柱图组件使用指南

## 概述

柱图（Bar Chart）即垂直柱状图，用于展示时间趋势和分类对比，适合：
- 月度/年度数据趋势
- 分类数据对比分析
- 环比/同比增长展示
- 多指标同时展示

## 组件特点

### 1. 垂直布局
- 柱形垂直排列，从下往上显示数值
- X 轴通常为时间或类别
- Y 轴为数值刻度

### 2. 多指标支持
- 可同时展示多个指标（如本月、上月、去年同期）
- 每个指标使用不同颜色区分
- 图例显示在顶部或底部

### 3. 滚动与动画
- 支持高亮滚动效果
- 自动循环展示更多数据
- 可配置滚动速度

## 使用方法

### 基础示例

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type bar \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --view-name "月度收款趋势"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654239893 |
| --model-id | 是 | 数据模型 ID | 2597080602 |
| --dimension-field | 是 | 维度字段（X轴） | receivingDate |
| --indicator-field | 是 | 指标字段 | receivingAmount |
| --chart-type | 是 | 图表类型，固定为 `bar` | bar |
| --top | 是 | Y 坐标 | 200 |
| --left | 是 | X 坐标 | 50 |
| --width | 是 | 组件宽度 | 450 |
| --height | 是 | 组件高度 | 300 |
| --view-name | 否 | 视图标题 | "月度收款趋势" |
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
    "title": "月度收款趋势"
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

#### 1. 图例配置
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

#### 2. 滚动配置
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

#### 3. 数据标签
```json
"label": {
  "isExtra": true,
  "show": false,
  "position": "auto"
}
```
- `show`: 是否显示数值标签（默认 false）
- `position`: 标签位置（top/right/bottom/auto）

#### 4. X轴标签旋转
```json
"axis": {
  "x": {
    "rotate": 0,
    "axes": ["showXAxis"]
  }
}
```
- `rotate`: 标签旋转角度（0-45），当标签文字较长时使用

## 实战案例

### 案例 1：月度收款趋势

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type bar \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --view-name "月度收款趋势"
```

### 案例 2：显示数据标签

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type bar \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --bar-label-show true \
  --bar-label-position top \
  --view-name "月度收款趋势"
```

### 案例 3：关闭滚动效果

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type bar \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --bar-scroll-enabled false \
  --view-name "月度收款趋势"
```

### 案例 4：调整X轴标签角度（长标签时）

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectName \
  --indicator-field receivingAmount \
  --chart-type bar \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --bar-axis-rotate 30 \
  --view-name "项目收款对比"
```

## 高级配置

### 修改图例位置

```bash
# 图例在底部
python3 scripts/add_component.py ... --bar-legend-position bottom

# 图例在右侧
python3 scripts/add_component.py ... --bar-legend-position right
```

### 使用 update_screen.py 更新样式

```bash
# 修改柱图图例位置
python3 scripts/update_screen.py --screen-id 3657066337 --uuid "grid-type:bar-uuid:xxx" --clone-style-from "grid-type:bar-uuid:yyy"

# 更新卡片背景样式
python3 scripts/update_screen.py \
  --screen-id 3657066337 \
  --uuid "grid-type:bar-uuid:xxx" \
  --card-background-color "rgba(13, 24, 44, 0.8)" \
  --card-border "rgba(30, 39, 55, 0.8)" \
  --card-padding 12
```

## 与其他组件配合

### 推荐组合

```
+----------------------------------+
| [指标卡 1] [指标卡 2] [指标卡 3]  |
+----------------------------------+
|                                  |
|  [柱图]       [饼图]   [排名图]  |
|  (趋势)       (占比)   (排行)    |
|                                  |
+----------------------------------+
|        [底部明细表格]             |
+----------------------------------+
```

### 布局建议

1. **柱图 + 指标卡**：上方指标卡展示汇总，下方柱图展示趋势
2. **柱图 + 饼图**：左侧趋势分析，右侧占比分布
3. **多柱图组合**：展示多个相关指标对比

## 柱图 vs 条形图

| 特性 | 柱图（垂直） | 条形图（水平） |
|------|------------|--------------|
| 布局方向 | 垂直 | 水平 |
| X轴方向 | 通常为类别/时间 | 通常为数值 |
| 标签显示 | 适合短标签 | 适合长标签 |
| 数据条数 | 适合较少数据 | 适合较多数据 |
| 使用场景 | 时间趋势、分布 | 类别对比、排名 |
| 空间利用 | 纵向空间利用 | 横向空间利用 |

### 选择建议

**使用柱图**：
- 时间序列数据
- 标签较短
- 数据类别较少（<8 个）
- 展示趋势变化

**使用条形图**：
- 标签名称较长
- 数据类别较多（>8 个）
- 需要精确对比数值
- 展示排名/排行榜

## 注意事项

### 1. 数据排序（重要！）

**趋势图必须使用时间维度排序，不要用指标排序！**

- **重要**：`orderType` 优先级为：指标 > 维度
- 如果设置了指标的 `orderType`，会覆盖维度的排序
- 对于趋势图，**不要设置指标的 orderType**，让维度（时间）排序生效
- 如果需要维度排序，应去掉指标的 `orderType`：

**使用 CLI 创建时：**
```bash
# ✅ 正确：清除指标排序，让时间维度排序生效
python3 scripts/update_screen.py --screen-id <ID> --uuid <uuid> --indicator-order-type none

# ❌ 错误：指标排序会覆盖维度排序
python3 scripts/add_component.py ... --indicator-order-type desc
```

**手动修改配置时：**
```python
# 错误：指标设置了排序
indicator["orderType"] = "desc"  # 这会导致按金额排序，而不是按时间！

# 正确：不设置指标排序，让维度排序生效
indicator.pop("orderType", None)
```

### 2. 日期维度格式（重要！）

**月度趋势图必须使用 `YM` 格式！**

- 日期类型维度通过 `dateFormat` 属性控制显示格式
- 月度趋势**必须**使用 `YM` 格式（显示 2024-01）
- 详细数据展示使用 `YMD` 格式（显示 2024-01-15）
- 常用格式：`YMD`、`YM`、`YD`、`MD`、`Y`、`M`、`D`

```python
# 修改组件维度配置
for dim in dimensions:
    if dim.get('fieldName') == 'receivingDate':
        dim['dateFormat'] = 'YM'  # 月度数据必须设为YM
```

### 3. X轴标签显示
- 标签过长时使用 `--bar-axis-rotate 30` 旋转
- 或增加组件宽度

### 3. 滚动效果
- 数据超过显示区域自动滚动
- 调整 `--bar-scroll-speed` 控制速度

### 4. 数据标签
- 默认不显示数值（`--bar-label-show false`）
- 显示时调整 `--bar-label-position` 位置

## 常见问题

### Q1: 柱形颜色不好看？
- 默认使用主题蓝色
- 可通过样式复制 `--clone-style-from` 应用其他组件配色

### Q2: X轴标签重叠？
- 增加组件宽度
- 使用 `--bar-axis-rotate 30` 旋转标签
- 减少显示的数据条数

### Q3: 如何显示数值？
- 添加 `--bar-label-show true`
- 调整位置 `--bar-label-position top`

### Q4: 滚动速度太快/太慢？
- 使用 `--bar-scroll-speed 3` 慢速
- 使用 `--bar-scroll-speed 8` 快速

## 参考资源

- [SKILL.md](../../SKILL.md) - 技能主文档
- [add_component.py](./add_component.py) - 组件添加脚本
- [update_screen.py](./update_screen.py) - 组件更新脚本
- [BAR3D_COMPONENT_GUIDE.md](./BAR3D_COMPONENT_GUIDE.md) - 3D柱图组件指南
- [HORIZONTAL_BAR_COMPONENT_GUIDE.md](./HORIZONTAL_BAR_COMPONENT_GUIDE.md) - 条形图组件指南
