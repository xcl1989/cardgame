# 饼图组件使用指南

## 概述

饼图（Pie Chart）用于展示**各分类占总体的比例关系**，适合：
- 项目类型占比分析
- 部门费用分布
- 业务渠道对比
- 分类构成分析

## 组件特点

### 1. 环形设计
- 默认使用环形图（外半径 80%，内半径 60%）
- 中心区域可展示总计或标题
- 比传统饼图更现代美观

### 2. 标签显示
- 支持外部标签显示
- 显示内容：分类名称、数值、百分比
- 标签引导线连接数据点和文字

### 3. 滚动效果
- 支持数据滚动展示
- 循环高亮各分类
- 可配置滚动速度

### 4. 颜色分段
- 每个分类自动分配颜色
- 与主题配色协调
- 支持多色渐变系列

## 使用方法

### 基础示例

```bash
python3 scripts/add_component.py \
  --screen-id 3654572744 \
  --model-id 2592797039 \
  --dimension-field field16 \
  --indicator-field field3 \
  --chart-type pie \
  --top 412 --left 16 \
  --width 410 --height 326 \
  --view-name "项目类型占比"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654572744 |
| --model-id | 是 | 数据模型 ID | 2592797039 |
| --dimension-field | 是 | 分类维度字段 | projectType |
| --indicator-field | 是 | 指标字段（数值） | amount |
| --chart-type | 是 | 图表类型，固定为 `pie` | pie |
| --top | 是 | Y 坐标 | 412 |
| --left | 是 | X 坐标 | 16 |
| --width | 是 | 组件宽度 | 410 |
| --height | 是 | 组件高度 | 326 |
| --view-name | 否 | 视图标题 | "项目类型占比" |
| --pie-outer-radius | 否 | 外半径（默认 80） | 90 |
| --pie-inner-radius | 否 | 内半径（默认 60，设为 0 则为实心饼图） | 0 |
| --pie-label-position | 否 | 标签位置：`outside`/`inside`/`center` | inside |
| --pie-legend-position | 否 | 图例位置：`bottom`/`top`/`left`/`right` | right |

### 饼图样式参数详解

#### 环形 vs 实心

```bash
# 环形饼图（默认）
--pie-outer-radius 80 --pie-inner-radius 60

# 实心饼图
--pie-outer-radius 90 --pie-inner-radius 0
```

#### 标签位置效果

```bash
# 外部标签（默认）- 带引导线
--pie-label-position outside

# 内部标签 - 紧凑显示
--pie-label-position inside

# 中心标签 - 显示在圆心
--pie-label-position center
```

#### 图例位置

```bash
# 底部（默认）
--pie-legend-position bottom

# 顶部
--pie-legend-position top

# 左侧
--pie-legend-position left

# 右侧
--pie-legend-position right
```

### 尺寸建议

| 场景 | 推荐宽度 | 推荐高度 | 说明 |
|------|---------|---------|------|
| 侧边辅助 | 370-420 | 260-300 | 作为辅助占比展示 |
| 主图表区 | 450-550 | 350-450 | 较大尺寸展示细节 |
| 小型预览 | 280-350 | 200-280 | 辅助展示概览 |

## 样式配置

### 完整样式结构

```json
{
  "textData": {"show": false},
  "screenPosition": {
    "position": {"x": 16, "y": 412, "w": 410, "h": 326}
  },
  "legend": {
    "isExtra": true,
    "textSetMap": {
      "size": 12,
      "textItalic": false,
      "textBold": false,
      "fontSize": 12,
      "textColor": "#177DDC"
    },
    "position": "bottom"
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
    "content": ["dimension", "measure", "percent"]
  },
  "scroll": {
    "cycleSpeed": 5,
    "show": true
  },
  "drawSettings": {
    "outerRadius": 80,
    "type": "default",
    "innerRadius": 60
  },
  "label": {
    "isExtra": true,
    "textSetMap": {
      "size": 12,
      "textItalic": false,
      "textBold": false,
      "fontSize": 12,
      "textColor": "#A6ADD0"
    },
    "position": "outside",
    "content": ["dimension", "measure", "percent"]
  },
  "title": {
    "isExtra": true,
    "show": true,
    "textSetMap": {
      "textItalic": false,
      "textBold": true,
      "fontSize": 16,
      "align": "center",
      "textColor": "#FEFEFE"
    },
    "title": "项目类型占比"
  },
  "card": {
    "border": "rgba(30, 39, 55, 0.8)",
    "padding": 12,
    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
    "lineWidthMap": {"width": 1, "style": "solid"}
  }
}
```

### 标准卡片样式（深蓝半透明）

新创建的组件默认使用以下卡片样式：

```json
"card": {
  "border": "rgba(30, 39, 55, 0.8)",
  "padding": 12,
  "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
  "lineWidthMap": {"width": 1, "style": "solid"}
}
```

**使用 update_screen.py 更新现有组件样式**:
```bash
python3 scripts/update_screen.py \
  --screen-id 3657066337 \
  --uuid "grid-type:pie-uuid:xxx" \
  --card-background-color "rgba(13, 24, 44, 0.8)" \
  --card-border "rgba(30, 39, 55, 0.8)" \
  --card-padding 12
```

### 关键样式说明

#### 1. 环形图配置
```json
"drawSettings": {
  "outerRadius": 80,
  "type": "default",
  "innerRadius": 60
}
```
- `outerRadius`: 外半径百分比（相对于组件尺寸）
- `innerRadius`: 内半径百分比（创建环形图效果）
- `type`: 图表类型，`default` 为标准饼/环形图

#### 2. 图例配置（底部）
```json
"legend": {
  "isExtra": true,
  "textSetMap": {
    "size": 12,
    "textColor": "#177DDC"
  },
  "position": "bottom"
}
```
- `position`: 图例位置（`bottom`/`top`/`left`/`right`）
- `textColor`: 与链接线颜色协调

#### 3. 标签配置
```json
"label": {
  "position": "outside",
  "content": ["dimension", "measure", "percent"]
}
```
- `position`: 标签位置
  - `outside`: 外部显示（带引导线）
  - `inside`: 内部显示
  - `center`: 中心显示
- `content`: 显示内容组合
  - `dimension`: 分类名称
  - `measure`: 数值
  - `percent`: 百分比

#### 4. 提示框配置
```json
"tooltip": {
  "backgroundColor": "#303467",
  "content": ["dimension", "measure", "percent"]
}
```
- 悬停时显示详细信息
- 深色背景配浅色文字

#### 5. 滚动效果
```json
"scroll": {
  "cycleSpeed": 5,
  "show": true
}
```
- 数据较多时自动滚动高亮
- `cycleSpeed`: 滚动速度（1-10）

## 数据要求

### 维度字段

饼图的维度字段用于**分类分组**，通常：
- 分类名称（文本类型）
- 类型编码（文本类型）
- 状态字段（文本类型）

### 指标字段

指标字段为**数值类型**，用于计算各分类的占比：
- 金额字段
- 数量字段
- 比率字段（需设置百分比格式）

### 示例数据

```
dimension_field (项目类型) | indicator_field (金额)
--------------------------|----------------------
建筑工程                  | 5000000
装饰装修                  | 3000000
机电安装                  | 2000000
市政工程                  | 1500000
其他                      | 500000
```

## 实战案例

### 案例 1：项目类型占比分析

```bash
python3 scripts/add_component.py \
  --screen-id 3654572744 \
  --model-id 2592797039 \
  --dimension-field field16 \
  --indicator-field field3 \
  --chart-type pie \
  --top 412 --left 16 \
  --width 410 --height 326 \
  --view-name "项目类型占比"
```

### 案例 2：左侧卡片内嵌饼图

```bash
# 配合卡片装饰使用
python3 scripts/add_component.py \
  --screen-id 3654572744 \
  --model-id 2592797039 \
  --dimension-field field16 \
  --indicator-field field3 \
  --chart-type pie \
  --top 430 --left 30 \
  --width 380 --height 290 \
  --view-name "成本构成分析"
```

### 案例 3：与柱图组合

```bash
# 左侧：柱图（详细数值）
python3 scripts/add_component.py \
  --screen-id 3654572744 \
  --model-id 2592797039 \
  --dimension-field field16 \
  --indicator-field field3 \
  --chart-type bar \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --view-name "各类别金额" && \

# 右侧：饼图（占比概览）
python3 scripts/add_component.py \
  --screen-id 3654572744 \
  --model-id 2592797039 \
  --dimension-field field16 \
  --indicator-field field3 \
  --chart-type pie \
  --top 200 --left 520 \
  --width 400 --height 300 \
  --view-name "各类别占比"
```

### 案例 4：实心饼图（无环形）

```bash
# 使用 inner-radius=0 创建实心饼图
python3 scripts/add_component.py \
  --screen-id 3654572744 \
  --model-id 2592797039 \
  --dimension-field field16 \
  --indicator-field field3 \
  --chart-type pie \
  --top 200 --left 50 \
  --width 400 --height 300 \
  --view-name "实心占比图" \
  --pie-outer-radius 90 \
  --pie-inner-radius 0
```

### 案例 5：内部标签 + 顶部图例

```bash
# 紧凑布局：内部标签显示，顶部图例
python3 scripts/add_component.py \
  --screen-id 3654572744 \
  --model-id 2592797039 \
  --dimension-field field16 \
  --indicator-field field3 \
  --chart-type pie \
  --top 200 --left 50 \
  --width 350 --height 280 \
  --view-name "紧凑占比图" \
  --pie-label-position inside \
  --pie-legend-position top
```

### 案例 6：中心标签 + 右侧图例

```bash
# 中心显示百分比，右侧图例
python3 scripts/add_component.py \
  --screen-id 3654572744 \
  --model-id 2592797039 \
  --dimension-field field16 \
  --indicator-field field3 \
  --chart-type pie \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --view-name "中心百分比图" \
  --pie-label-position center \
  --pie-legend-position right
```

## 与其他组件配合

### 推荐组合

```
+----------------------------------+
| [指标卡 1] [指标卡 2] [指标卡 3] |
+----------------------------------+
|                                   |
|  +-----------+   +-----------+   |
|  |  柱图     |   |   饼图    |   |
|  | (数值详情) |   |  (占比)   |   |
|  +-----------+   +-----------+   |
|                                   |
+----------------------------------+
```

### 布局建议

1. **饼图 + 指标卡**：右侧饼图展示占比，上方指标卡展示总计
2. **饼图 + 柱图**：左侧柱图展示详细数值，右侧饼图展示占比
3. **多个小饼图**：同一行并排 2-3 个小饼图展示不同维度占比

## 注意事项

### 1. 分类数量
- 饼图适合展示 **3-7 个分类**
- 分类过多会导致标签重叠
- 超过 7 个分类建议使用柱图或条形图

### 2. 尺寸要求
- 饼图组件**高度至少 250px**
- 宽度过小会导致标签显示不全
- 建议尺寸：400×300 以上

### 3. 数据分布
- 避免某个分类占比超过 80%
- 避免某个分类占比小于 5%
- 小占比分类可合并为"其他"

### 4. 标签位置
- 外部标签需要足够空间显示引导线
- 内部标签适合占比接近的场景
- 可根据数据分布调整标签位置

## 常见问题

### Q1: 饼图显示为椭圆形？
- 检查组件宽高比例
- 确保宽度约为高度的 1.2-1.5 倍

### Q2: 标签文字重叠？
- 减少显示的分类数量
- 增大组件尺寸
- 调整标签位置为 `outside`

### Q3: 如何只显示百分比？
- 修改 `label.content` 为 `["dimension", "percent"]`

### Q4: 如何改成实心饼图？
- 设置 `drawSettings.innerRadius` 为 0

### Q5: 颜色如何自定义？
- 在主题配色中设置 `graColorSystemCustomColors`

## 参考资源

- [SKILL.md](../../SKILL.md) - 技能主文档
- [add_component.py](../scripts/add_component.py) - 组件添加脚本
- [new.curl](../../new.curl) - 完整示例大屏配置
