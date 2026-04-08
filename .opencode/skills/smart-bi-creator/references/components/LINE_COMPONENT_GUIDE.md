# 线图组件使用指南

## 概述

线图（Line Chart）用于展示数据趋势和变化规律，适合：
- 时间序列数据展示
- 趋势分析（上升、下降、波动）
- 多指标对比分析
- 环比/同比增长展示

## 组件特点

### 1. 趋势展示
- 通过线条连接数据点展示连续变化
- 适合展示历史走势和预测未来
- 平滑曲线或折线可选

### 2. 多指标支持
- 可同时展示多条线（多个指标）
- 每条线使用不同颜色区分
- 支持面积填充效果

### 3. 滚动与动画
- 支持数据点滚动动画
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
  --chart-type line \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --view-name "收款趋势分析"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654239893 |
| --model-id | 是 | 数据模型 ID | 2597080602 |
| --dimension-field | 是 | 维度字段（X轴） | receivingDate |
| --indicator-field | 是 | 指标字段 | receivingAmount |
| --chart-type | 是 | 图表类型，固定为 `line` | line |
| --top | 是 | Y 坐标 | 200 |
| --left | 是 | X 坐标 | 50 |
| --width | 是 | 组件宽度 | 450 |
| --height | 是 | 组件高度 | 300 |
| --view-name | 否 | 视图标题 | "收款趋势分析" |
| --bar-legend-position | 否 | 图例位置 | bottom/top/left/right |
| --bar-scroll-enabled | 否 | 是否启用滚动 | true/false |
| --bar-scroll-speed | 否 | 滚动速度（1-10） | 5 |
| --bar-label-show | 否 | 是否显示数据标签 | true/false |
| --bar-axis-rotate | 否 | X轴标签旋转角度 | 0-45 |
| --line-type | 否 | 线条类型 | line(折线)/curve(曲线)，默认 curve |

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
    "seriesType": "line",
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
    "title": "收款趋势分析"
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
- `position`: 标签位置（auto/left/right）

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

#### 5. 线条类型
```json
"drawSettings": {
  "lineType": "curve",
  "node": "circle",
  "nodeSize": 8
}
```
- `lineType`: 线条类型
  - `curve`: 曲线（默认），线条平滑流畅
  - `line`: 折线，线条带尖角

**曲线 vs 折线：**
| 类型 | 视觉效果 | 适用场景 |
|------|---------|---------|
| curve | 平滑流畅 | 强调趋势变化，数据波动规律 |
| line | 棱角分明 | 强调精确数据点，适合数据较少时 |

## 实战案例

### 案例 1：收款趋势分析（曲线，默认）

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type line \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --view-name "收款趋势分析"
```

### 案例 2：折线风格

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type line \
  --line-type line \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --view-name "收款趋势分析"
```

### 案例 3：显示数据标签

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type line \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --bar-label-show true \
  --view-name "收款趋势分析"
```

### 案例 3：关闭滚动效果

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type line \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --bar-scroll-enabled false \
  --view-name "收款趋势分析"
```

### 案例 4：多指标趋势对比

```bash
# 注意：需要数据模型支持多指标，或手动配置
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type line \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --bar-legend-position bottom \
  --view-name "收款与付款对比"
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
# 复制其他线图的样式
python3 scripts/update_screen.py --screen-id 3657066337 --uuid "grid-type:line-uuid:xxx" --clone-style-from "grid-type:line-uuid:yyy"

# 更新卡片背景样式
python3 scripts/update_screen.py \
  --screen-id 3657066337 \
  --uuid "grid-type:line-uuid:xxx" \
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
|  [线图]       [柱图]   [饼图]    |
|  (趋势)       (对比)   (占比)    |
|                                  |
+----------------------------------+
|        [底部明细表格]             |
+----------------------------------+
```

### 布局建议

1. **线图 + 指标卡**：上方指标卡展示当前值，下方线图展示趋势
2. **多线图组合**：展示多个相关指标同时变化
3. **线图 + 柱图组合**：线图展示趋势，柱图展示对比

## 线图 vs 柱图

| 特性 | 线图 | 柱图 |
|------|------|------|
| 展示方式 | 连线 | 柱形 |
| 适合场景 | 趋势变化 | 分类对比 |
| 数据密度 | 适合大量数据点 | 适合少量数据 |
| 多指标 | 易于对比多条线 | 多柱可能重叠 |
| 视觉效果 | 轻盈流畅 | 稳重实在 |

### 选择建议

**使用线图**：
- 展示数据随时间变化的趋势
- 数据点较多，需要看整体走势
- 多指标同时对比
- 强调变化规律

**使用柱图**：
- 展示分类数据的对比
- 数据点较少，需要看具体数值
- 强调各分类间的差异

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
- 趋势展示也可使用 `YM` 格式（更简洁）
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
- 默认不显示数值
- 显示时设置 `--bar-label-show true`

## 常见问题

### Q1: 如何让线条更明显？
- 使用较深的背景色增强对比
- 通过 `--clone-style-from` 复制深色线图样式

### Q2: X轴标签重叠？
- 增加组件宽度
- 使用 `--bar-axis-rotate 30` 旋转标签
- 减少显示的数据条数

### Q3: 如何显示数据点数值？
- 添加 `--bar-label-show true`

### Q4: 滚动速度不合适？
- 使用 `--bar-scroll-speed 3` 慢速
- 使用 `--bar-scroll-speed 8` 快速

## 参考资源

- [SKILL.md](../../SKILL.md) - 技能主文档
- [add_component.py](./add_component.py) - 组件添加脚本
- [update_screen.py](./update_screen.py) - 组件更新脚本
- [BAR_COMPONENT_GUIDE.md](./BAR_COMPONENT_GUIDE.md) - 柱图组件指南
- [HORIZONTAL_BAR_COMPONENT_GUIDE.md](./HORIZONTAL_BAR_COMPONENT_GUIDE.md) - 条形图组件指南
