# 条形图组件使用指南

## 概述

条形图（Horizontal Bar Chart）即水平条形图，用于展示分类数据的对比，适合：
- 项目收款/付款对比
- 部门业绩排行
- 类别数据比较
- 长标签名称展示（水平布局更易读）

## 组件特点

### 1. 水平布局
- 条形水平排列，从左到右显示数值
- 适合标签名称较长的场景
- 支持自动滚动显示更多数据

### 2. 多指标支持
- 可同时展示多个指标（如最大值、平均值、最小值）
- 每个指标使用不同颜色区分
- 图例显示在底部

### 3. 高亮滚动
- 支持高亮滚动效果
- 自动循环展示数据
- 可配置滚动速度

## 使用方法

### 基础示例

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type horizontalBar \
  --top 368 --left 19 \
  --width 412 --height 196 \
  --view-name "项目收款对比"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654239893 |
| --model-id | 是 | 数据模型 ID | 2597080602 |
| --dimension-field | 是 | 维度字段（用于分组） | projectNo |
| --indicator-field | 是 | 指标字段（第一个） | receivingAmount |
| --chart-type | 是 | 图表类型，固定为 `horizontalBar` | horizontalBar |
| --top | 是 | Y 坐标 | 368 |
| --left | 是 | X 坐标 | 19 |
| --width | 是 | 组件宽度 | 412 |
| --height | 是 | 组件高度 | 196 |
| --view-name | 否 | 视图标题 | "项目收款对比" |

### 尺寸建议

| 场景 | 推荐宽度 | 推荐高度 | 说明 |
|------|---------|---------|------|
| 侧边对比 | 400-450 | 200-250 | 单侧展示 5-8 条数据 |
| 主图表区 | 500-600 | 300-350 | 展示 10-15 条数据 |
| 小型对比 | 300-350 | 150-200 | 辅助展示 3-5 条数据 |

## 样式配置

### 完整样式结构

```json
{
  "textData": {"show": false},
  "screenPosition": {
    "position": {"x": 19, "y": 368, "w": 412, "h": 196}
  },
  "legend": {
    "isExtra": true,
    "textSetMap": {
      "size": 14,
      "textItalic": false,
      "textBold": false,
      "fontSize": 14,
      "textColor": "rgb(164,173,211)"
    },
    "position": "bottom"
  },
  "tooltip": {
    "backgroundColor": "#303467",
    "isExtra": true,
    "textSetMap": {
      "size": 14,
      "textItalic": false,
      "textBold": false,
      "fontSize": 14,
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
      "size": 14,
      "textItalic": false,
      "textBold": false,
      "fontSize": 14,
      "textColor": "#A6ADD0"
    },
    "position": "right"
  },
  "title": {
    "isExtra": true,
    "show": false,
    "textSetMap": {
      "textItalic": false,
      "textBold": true,
      "fontSize": 16,
      "textColor": "#FEFEFE"
    }
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
  --uuid "grid-type:horizontalBar-uuid:xxx" \
  --card-background-color "rgba(13, 24, 44, 0.8)" \
  --card-border "rgba(30, 39, 55, 0.8)" \
  --card-padding 12
```

### 关键样式说明

#### 1. 图例配置（底部）
```json
"legend": {
  "isExtra": true,
  "textSetMap": {
    "size": 14,
    "textBold": false,
    "fontSize": 14,
    "textColor": "rgb(164,173,211)"
  },
  "position": "bottom"
}
```
- `position`: 图例位置（底部）
- `textColor`: 灰蓝色，与主题协调

#### 2. 滚动配置
```json
"scroll": {
  "cycleSpeed": 5,
  "show": true,
  "type": "highlight"
}
```
- `show`: 是否启用滚动
- `type`: `highlight` 高亮滚动
- `cycleSpeed`: 滚动速度（1-10）

#### 3. 绘图设置
```json
"drawSettings": {
  "seriesType": "bar",
  "widthMap": {"isAdaption": true}
}
```
- `seriesType`: 条形图类型
- `widthMap.isAdaption`: 自动适应宽度

#### 4. 数据标签
```json
"label": {
  "isExtra": true,
  "show": false,
  "position": "right"
}
```
- `show`: 是否显示数值标签
- `position`: 标签位置（右侧）

#### 5. 坐标轴
```json
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
}
```
- X 轴：显示轴线，自动缩放
- Y 轴：显示轴线和分割线

## 实战案例

### 案例 1：项目收款对比

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type horizontalBar \
  --top 368 --left 19 \
  --width 412 --height 196 \
  --view-name "项目收款 Top10"
```

### 案例 2：部门业绩多指标对比

```bash
# 注意：需要修改脚本支持多指标，或手动添加多个指标
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field deptName \
  --indicator-field receivingAmount \
  --chart-type horizontalBar \
  --top 200 --left 500 \
  --width 500 --height 300 \
  --view-name "部门业绩对比"
```

### 案例 3：与柱图组合使用

```bash
# 左侧：垂直柱图（趋势分析）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type bar \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --view-name "月度收款趋势" && \

# 右侧：水平条形图（类别对比）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectType \
  --indicator-field receivingAmount \
  --chart-type horizontalBar \
  --top 200 --left 520 \
  --width 450 --height 300 \
  --view-name "项目类型对比"
```

## 条形图 vs 柱状图

| 特性 | 条形图（水平） | 柱状图（垂直） |
|------|--------------|--------------|
| 布局方向 | 水平 | 垂直 |
| 标签显示 | 适合长标签 | 适合短标签 |
| 数据条数 | 适合较多数据 | 适合较少数据 |
| 使用场景 | 类别对比、排名 | 时间趋势、分布 |
| 空间利用 | 横向空间利用 | 纵向空间利用 |

### 选择建议

**使用条形图**：
- 标签名称较长
- 数据类别较多（>8 个）
- 需要精确对比数值
- 展示排名/排行榜

**使用柱状图**：
- 时间序列数据
- 标签较短
- 数据类别较少（<8 个）
- 展示趋势变化

## 注意事项

### 1. 数据排序
- 默认按指标值降序排列
- 可通过 `indicator.orderType` 控制

### 2. 多指标展示
- 当前脚本版本支持单指标
- 多指标需要手动修改配置添加多个 indicator

### 3. 滚动效果
- 数据超过显示区域自动滚动
- 调整 `scroll.cycleSpeed` 控制速度

### 4. 标签显示
- `label.show: false` 默认不显示数值
- 设置 `true` 可在条形右侧显示数值

## 与其他组件配合

### 推荐组合

```
+----------------------------------+
| [指标卡 1] [指标卡 2] [指标卡 3]  |
+----------------------------------+
|                                  |
|  [条形图]     [柱图]   [饼图]     |
|  (类别对比)  (趋势)   (占比)     |
|                                  |
+----------------------------------+
|        [底部明细表格]             |
+----------------------------------+
```

### 布局建议

1. **条形图 + 指标卡**：上方显示总计，下方显示分类对比
2. **条形图 + 柱图**：左侧类别对比，右侧时间趋势
3. **条形图 + 饼图**：左侧详细对比，右侧占比分布

## 常见问题

### Q1: 条形颜色不明显？
- 检查主题配色
- 修改 `drawSettings` 中的颜色配置

### Q2: 标签文字重叠？
- 增加组件宽度
- 减少显示的数据条数
- 使用滚动展示

### Q3: 如何显示数值标签？
- 设置 `label.show: true`
- 调整 `label.position: "right"`

### Q4: 多指标如何配置？
- 在 `indicators` 数组中添加多个指标对象
- 每个指标设置不同的 `metricType`（SUM/AVG/MAX/MIN）

## 参考资源

- [SKILL.md](../../SKILL.md) - 技能主文档
- [add_component.py](./add_component.py) - 组件添加脚本
- [RANKING_COMPONENT_GUIDE.md](./RANKING_COMPONENT_GUIDE.md) - 排名图组件指南
