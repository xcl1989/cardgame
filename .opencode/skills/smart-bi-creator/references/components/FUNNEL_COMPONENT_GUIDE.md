# 漏斗图组件使用指南

## 概述

漏斗图（Funnel Chart）用于展示业务流程中的转化分析，适合：
- 销售渠道转化分析
- 客户漏斗分析
- 转化率可视化
- 层层递减的数据展示

## 组件特点

### 1. 梯形布局
- 自上而下逐渐收缩的梯形
- 每个阶段用不同颜色区分
- 数据从大到小依次递减

### 2. 转化标注
- 支持显示当前阶段数值
- 可选显示转化率
- 显示相邻阶段差异

### 3. 适用场景
- 销售漏斗：线索→意向→成交
- 转化分析：访问→注册→付费
- 流程监控：启动→进行→完成

## 使用方法

### 基础示例

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingType \
  --indicator-field receivingAmount \
  --chart-type funnel \
  --top 200 --left 50 \
  --width 450 --height 350 \
  --view-name "收款渠道转化"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654239893 |
| --model-id | 是 | 数据模型 ID | 2597080602 |
| --dimension-field | 是 | 维度字段（阶段名称） | receivingType |
| --indicator-field | 是 | 指标字段 | receivingAmount |
| --chart-type | 是 | 图表类型，固定为 `funnel` | funnel |
| --top | 是 | Y 坐标 | 200 |
| --left | 是 | X 坐标 | 50 |
| --width | 是 | 组件宽度 | 450 |
| --height | 是 | 组件高度 | 350 |
| --view-name | 否 | 视图标题 | "收款渠道转化" |

### 尺寸建议

| 场景 | 推荐宽度 | 推荐高度 | 说明 |
|------|---------|---------|------|
| 主图表区 | 400-500 | 350-450 | 展示完整漏斗 |
| 小型图表 | 300-350 | 280-320 | 辅助展示 |
| 宽屏布局 | 500-600 | 350-400 | 横向空间充足时 |

## 样式配置

### 完整样式结构

```json
{
  "screenPosition": {
    "position": {"x": 50, "y": 200, "w": 450, "h": 350}
  },
  "textData": {"show": true},
  "legend": {
    "isExtra": true,
    "textSetMap": {
      "size": 14,
      "fontSize": 14,
      "textColor": "#177DDC"
    },
    "position": "bottom"
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
    "seriesType": "funnel",
    "sort": "descending"
  },
  "label": {
    "show": true,
    "position": "inside",
    "textSetMap": {
      "size": 12,
      "fontSize": 12,
      "textColor": "#FFFFFF"
    }
  }
}
```

## 进阶配置

### 显示数值标签

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingType \
  --indicator-field receivingAmount \
  --chart-type funnel \
  --top 200 --left 50 \
  --width 450 --height 350 \
  --view-name "收款渠道转化" \
  --funnel-label-show true
```

### 漏斗形状配置

漏斗图支持不同的形状变化，可通过 `drawSettings` 调整：

```json
{
  "drawSettings": {
    "seriesType": "funnel",
    "sort": "descending",
    "gap": 2
  }
}
```

## 常见问题

### Q1: 漏斗数据不递减怎么办？

**A**: 确保数据是按从大到小排列的，数据模型中可以使用 `orderType: desc` 排序。

### Q2: 漏斗阶段太少不好看？

**A**: 漏斗图通常展示 3-7 个阶段。阶段太少可以考虑使用柱图，阶段太多可以合并相近的阶段。

## 相关文档

- [柱图组件](BAR_COMPONENT_GUIDE.md)
- [饼图组件](PIE_COMPONENT_GUIDE.md)
- [脚本组件](SCRIPT_COMPONENT_GUIDE.md) - 可用 ECharts 自定义漏斗样式
