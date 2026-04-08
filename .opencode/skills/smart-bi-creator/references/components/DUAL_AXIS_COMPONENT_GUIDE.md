# 双轴图组件使用指南

## 概述

双轴图（Dual Axis Chart）用于在同一个图表中展示两个不同量级的指标，适合：
- 收入与增长率对比
- 数量与百分比对比
- 实际与目标对比
- 两个相关但量级不同的指标

## 组件特点

### 1. 双 Y 轴设计
- 左侧 Y 轴：第一个指标（绝对值）
- 右侧 Y 轴：第二个指标（相对值/百分比）
- 同一 X 轴共享时间或类别

### 2. 混合图表类型
- 通常为柱图 + 折线图组合
- 柱图展示绝对值（左侧刻度）
- 折线图展示相对值（右侧刻度）

### 3. 适用场景
- 销售收入与同比增长率
- 实际完成与目标对比
- 数量与占比同时展示
- 多指标横向对比

## 使用方法

### 基础示例

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type dualAxis \
  --top 200 --left 50 \
  --width 500 --height 300 \
  --view-name "收款与增长率"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654239893 |
| --model-id | 是 | 数据模型 ID | 2597080602 |
| --dimension-field | 是 | 维度字段（X轴） | receivingDate |
| --indicator-field | 是 | 指标字段 1（柱图） | receivingAmount |
| --extra-indicator-fields | 否 | 指标字段 2（折线） | growthRate |
| --chart-type | 是 | 图表类型，固定为 `dualAxis` | dualAxis |
| --top | 是 | Y 坐标 | 200 |
| --left | 是 | X 坐标 | 50 |
| --width | 是 | 组件宽度 | 500 |
| --height | 是 | 组件高度 | 300 |
| --view-name | 否 | 视图标题 | "收款与增长率" |

### 尺寸建议

| 场景 | 推荐宽度 | 推荐高度 | 说明 |
|------|---------|---------|------|
| 主图表区 | 500-600 | 300-350 | 展示完整趋势 |
| 小型图表 | 350-450 | 220-280 | 辅助展示 |
| 宽屏布局 | 650-750 | 300-350 | 横向空间充足时 |

## 样式配置

### 完整样式结构

```json
{
  "screenPosition": {
    "position": {"x": 50, "y": 200, "w": 500, "h": 300}
  },
  "textData": {"show": false},
  "legend": {
    "isExtra": true,
    "textSetMap": {
      "size": 14,
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
      "fontSize": 12,
      "textColor": "#A6ADD0"
    },
    "content": ["dimension", "measure"]
  },
  "drawSettings": {
    "seriesType": "bar",
    "barSeriesIndex": 0,
    "lineSeriesIndex": 1
  },
  "yAxis": [
    {
      "position": "left",
      "axisLabel": {
        "textSetMap": {
          "textColor": "#177DDC"
        }
      },
      "axisLine": {
        "show": true,
        "lineStyle": {
          "color": "#177DDC"
        }
      }
    },
    {
      "position": "right",
      "axisLabel": {
        "textSetMap": {
          "textColor": "#FF9900"
        }
      },
      "axisLine": {
        "show": true,
        "lineStyle": {
          "color": "#FF9900"
        }
      }
    }
  ]
}
```

## 进阶配置

### 设置左右轴指标

```bash
# 左侧柱图：收款金额
# 右侧折线：增长率
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type dualAxis \
  --top 200 --left 50 \
  --width 500 --height 300 \
  --view-name "收款与增长率" \
  --extra-indicator-fields "growthRate" \
  --bar-series-index 0 \
  --line-series-index 1
```

### 双轴图参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| bar-series-index | 柱图对应的指标索引 | 0, 1, 2... |
| line-series-index | 折线对应的指标索引 | 0, 1, 2... |
| left-axis-label | 左侧轴标签颜色 | hex 颜色值 |
| right-axis-label | 右侧轴标签颜色 | hex 颜色值 |

## 常见问题

### Q1: 两个指标量级差距太大怎么办？

**A**: 可以使用对数刻度或者标准化处理。如果一个指标是万级，一个是万分比，可以：
1. 将百分比乘以一个系数（如 10000）使其可视化可比较
2. 或者使用脚本组件进行自定义处理

### Q2: 如何控制柱图和折线的颜色？

**A**: 通过 `styleJson` 中的 `series` 数组配置每个系列的颜色：

```json
{
  "series": [
    {
      "type": "bar",
      "itemStyle": {"color": "#177DDC"}
    },
    {
      "type": "line",
      "itemStyle": {"color": "#FF9900"}
    }
  ]
}
```

### Q3: 柱图和折线顺序如何调整？

**A**: 调整 `barSeriesIndex` 和 `lineSeriesIndex` 参数，决定哪个指标用柱图，哪个用折线。

## 相关文档

- [柱图组件](BAR_COMPONENT_GUIDE.md)
- [折线图组件](LINE_COMPONENT_GUIDE.md)
- [脚本组件](SCRIPT_COMPONENT_GUIDE.md) - 可用 ECharts 自定义更复杂的双轴图
