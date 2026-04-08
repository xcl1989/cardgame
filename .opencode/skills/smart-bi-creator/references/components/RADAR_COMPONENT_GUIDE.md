# 雷达图组件使用指南

雷达图组件用于展示**多指标对比分析**或**多维度对比分析**，类似蜘蛛网状的图表。

## 两种模式

雷达图支持两种数据组织模式：

| 模式 | branchSettings.type | 说明 | 适用场景 |
|------|---------------------|------|---------|
| 指标驱动 | `"indicator"` | 每个指标形成一个角，多个指标围成多边形 | 多指标综合评价 |
| 维度驱动 | `"dimension"` | 每个维度值形成一个角，多个维度值围成多边形 | 多维度对比分析 |

### 指标驱动模式（默认）

- 每个指标形成一个雷达图的角
- 适合展示单个项目在多个指标上的表现
- 需要多个指标才有意义

### 维度驱动模式

- 每个维度值形成一个雷达图的角
- 适合展示多个项目在单个指标上的对比
- 只需要1个指标即可

## 快速开始

```bash
# 添加雷达图组件（默认使用指标驱动模式）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2586391007 \
  --dimension-field paymentMethod \
  --indicator-field receivingAmount \
  --chart-type radar \
  --top 200 --left 50 \
  --width 400 --height 400 \
  --view-name "支付方式分析"

# 使用维度驱动模式
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2586391007 \
  --dimension-field receivingType \
  --indicator-field receivingAmount \
  --chart-type radar \
  --top 200 --left 50 \
  --width 400 --height 400 \
  --view-name "收款类型分析" \
  --radar-mode dimension
```

## CLI 参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `--radar-radius` | 雷达半径，默认 50 | `60` |
| `--radar-legend-position` | 图例位置 | `top/bottom/left/right` |
| `--radar-label-position` | 标签位置 | `auto/top/bottom/left/right` |
| `--radar-mode` | 数据模式 | `indicator/dimension` |

## 配置结构

雷达图组件的 `styleJson` 包含以下关键配置：

### branchSettings（分支设置）

| 属性 | 说明 | 示例值 |
|------|------|--------|
| `type` | 分支类型：`"indicator"` 或 `"dimension"` | `"indicator"` |

### drawSettings（绘图设置）

| 属性 | 说明 | 示例值 |
|------|------|--------|
| `radius` | 雷达半径 | `50` |

### legend（图例设置）

| 属性 | 说明 | 示例值 |
|------|------|--------|
| `position` | 图例位置 | `"top"` |
| `textSetMap.textColor` | 文字颜色 | `"#177DDC"` |

### label（标签设置）

| 属性 | 说明 | 示例值 |
|------|------|--------|
| `position` | 标签位置 | `"auto"` |
| `textSetMap.textColor` | 文字颜色 | `"#A6ADD0"` |

## 示例：基于真实大屏配置

以下配置来自"数字大屏表格脚本组件-四川科景"大屏中的雷达图组件：

```json
{
    "dimensions": [
        {
            "datasetId": 2148797900,
            "fieldLabel": "支付方式",
            "fieldName": "paymentMethod",
            "groupBy": true,
            "index": 0,
            "modelDatasetName": "collectionReg3X",
            "nativeType": "TEXT"
        }
    ],
    "indicators": [
        {
            "customIndicator": false,
            "datasetId": 2148797900,
            "fieldLabel": "收款金额",
            "fieldName": "receivingAmount",
            "index": 0,
            "metricType": "SUM",
            "modelDatasetName": "collectionReg3X",
            "nativeType": "INT",
            "valueFormat": {
                "decimalPlaces": 2,
                "isPercentage": 0,
                "useThousandsSeparator": 0
            }
        },
        {
            "customIndicator": false,
            "datasetId": 2148797900,
            "fieldLabel": "本次关联发票收款金额",
            "fieldName": "invoiceReceivingAmount",
            "index": 1,
            "metricType": "SUM",
            "modelDatasetName": "collectionReg3X",
            "nativeType": "INT"
        }
    ],
    "modelId": 2586391007,
    "styleJson": {
        "branchSettings": {
            "type": "indicator"
        },
        "screenPosition": {
            "position": {
                "w": 455,
                "x": 1920,
                "h": 320,
                "y": 1080
            }
        },
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
                "size": 14,
                "textItalic": false,
                "textBold": false,
                "fontSize": 14,
                "textColor": "#A6ADD0"
            },
            "content": ["dimension", "measure"]
        },
        "drawSettings": {
            "radius": 50
        },
        "label": {
            "isExtra": true,
            "textSetMap": {
                "size": 14,
                "textItalic": false,
                "textBold": false,
                "fontSize": 14,
                "textColor": "#A6ADD0"
            },
            "position": "auto"
        },
        "card": {
            "border": "rgba(30, 39, 55, 0.8)",
            "padding": 12,
            "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
            "lineWidthMap": {
                "width": 1,
                "style": "solid"
            }
        }
    },
    "viewName": "雷达图1"
}
```

## 更新雷达图样式

```bash
# 更新雷达图样式参数
python3 scripts/update_screen.py --screen-id 3654239893 \
  --uuid "grid-type:radar-uuid:xxx" \
  --radar-radius 60 \
  --radar-legend-position top \
  --radar-label-position auto
```

## 适用场景

| 场景 | 推荐模式 |
|------|---------|
| 多指标综合对比 | 指标驱动模式 |
| 多维度对比分析 | 维度驱动模式 |
| 时间趋势分析 | ❌ 柱图/折线图 |
| 占比分析 | ❌ 饼图 |
| 单一指标展示 | ❌ 指标卡/翻牌器 |

## 注意事项

### 指标驱动模式
1. 需要 2-6 个指标才有意义
2. 每个指标形成一个角
3. 适合展示单个主体在多维度的表现

### 维度驱动模式
1. 只需要 1 个或多个指标
2. 每个维度值形成一个角
3. 适合展示多个主体在单一指标的对比

### 数据归一化
各指标数值范围差异大时，建议先进行标准化处理