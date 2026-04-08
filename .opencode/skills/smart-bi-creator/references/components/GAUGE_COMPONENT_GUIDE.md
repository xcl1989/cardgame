# 仪表盘组件使用指南

## 概述

仪表盘（Gauge Chart）用于展示指标完成进度或达成率，适合：
- KPI 完成率展示
- 目标达成进度
- 性能指标监控
- 单一指标可视化

## 组件特点

### 1. 圆环仪表样式
- 半圆形或圆环形刻度
- 指针指示当前值
- 支持多个指标分段着色

### 2. 进度展示
- 显示当前值与目标值的比例
- 可设置警戒值（红区）
- 动态指针动画效果

### 3. 适用场景
- 销售目标完成率
- 项目进度跟踪
- 设备运行状态
- 性能指标监控

## 使用方法

### 基础示例

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type gauge \
  --top 200 --left 50 \
  --width 350 --height 250 \
  --view-name "本月收款完成率"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654239893 |
| --model-id | 是 | 数据模型 ID | 2597080602 |
| --dimension-field | 是 | 维度字段 | receivingDate |
| --indicator-field | 是 | 指标字段 | receivingAmount |
| --chart-type | 是 | 图表类型，固定为 `gauge` | gauge |
| --top | 是 | Y 坐标 | 200 |
| --left | 是 | X 坐标 | 50 |
| --width | 是 | 组件宽度 | 350 |
| --height | 是 | 组件高度 | 250 |
| --view-name | 否 | 视图标题 | "本月收款完成率" |

### 尺寸建议

| 场景 | 推荐宽度 | 推荐高度 | 说明 |
|------|---------|---------|------|
| 单独展示 | 280-350 | 200-280 | 突出进度 |
| 组合展示 | 220-280 | 180-220 | 多个并排 |
| 迷你仪表 | 150-200 | 120-150 | 小型指标卡 |

## 样式配置

### 完整样式结构

```json
{
  "screenPosition": {
    "position": {"x": 50, "y": 200, "w": 350, "h": 250}
  },
  "textData": {"show": true},
  "legend": {
    "isExtra": true,
    "textSetMap": {
      "size": 14,
      "fontSize": 14,
      "textColor": "#177DDC"
    }
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
    "seriesType": "gauge",
    "min": 0,
    "max": 100,
    "splitNumber": 5
  },
  "gaugeStyle": {
    "radius": "75%",
    "startAngle": 180,
    "endAngle": 0,
    "pointer": {
      "show": true,
      "length": "60%"
    },
    "axisLine": {
      "show": true,
      "lineStyle": {
        "width": 10
      }
    },
    "axisTick": {
      "show": true,
      "distance": 5
    },
    "splitLine": {
      "show": true,
      "distance": 5
    }
  }
}
```

## 进阶配置

### 自定义刻度范围

```bash
# 设置 0-1000 的范围
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type gauge \
  --top 200 --left 50 \
  --width 350 --height 250 \
  --view-name "本月收款完成率" \
  --gauge-min 0 \
  --gauge-max 1000000
```

### 仪表盘分段颜色

通过 styleJson 配置文件设置分段颜色：

```json
{
  "drawSettings": {
    "seriesType": "gauge",
    "axisLine": {
      "lineStyle": {
        "color": [
          [0.3, "#67e0e3"],
          [0.7, "#37a2de"],
          [1, "#fd666d"]
        ]
      }
    }
  }
}
```

## 常见问题

### Q1: 如何显示百分比？

**A**: 仪表盘默认显示数值。如果需要显示百分比，需要：
1. 在数据模型中计算好百分比字段
2. 或者使用脚本组件自定义显示格式

### Q2: 指针不显示？

**A**: 检查 `gaugeStyle.pointer.show` 是否为 true。

### Q3: 如何实现动态仪表盘？

**A**: 可以使用脚本组件实现动态数据更新的仪表盘，参考 [脚本组件指南](SCRIPT_COMPONENT_GUIDE.md)。

## 相关文档

- [指标卡组件](METRIC_COMPONENT_GUIDE.md)
- [翻牌器组件](FLIPPER_COMPONENT_GUIDE.md)
- [脚本组件](SCRIPT_COMPONENT_GUIDE.md)
