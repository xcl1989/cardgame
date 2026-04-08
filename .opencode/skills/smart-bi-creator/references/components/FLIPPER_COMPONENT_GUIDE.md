# 翻牌器组件使用指南

翻牌器组件用于展示**数字滚动效果**，类似机场/车站的 flip board 显示牌，适合展示金额、数量等指标。

## 快速开始

```bash
# 添加翻牌器组件
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2586391007 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type flipper \
  --top 100 --left 50 \
  --width 400 --height 150 \
  --view-name "累计收款"
```

## 高级参数

```bash
# 自定义翻牌器样式
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2586391007 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type flipper \
  --top 100 --left 50 \
  --width 500 --height 180 \
  --view-name "本月收款" \
  --flipper-int-figure 10 \
  --flipper-decimal-figure 2 \
  --flipper-thousandth true \
  --flipper-style-type round \
  --flipper-font-size 40 \
  --flipper-fill-color "linear-gradient(180deg, rgba(2,53,107,0.5) 0%, rgba(5,101,164,0.5) 100%)" \
  --flipper-border-color "#A5CCEA" \
  --flipper-flip-gap 15
```

## 配置结构

翻牌器组件的 `styleJson` 包含以下关键配置：

### drawSettings（绘图设置）

| 属性 | 说明 | 示例值 |
|------|------|--------|
| `fillColor` | 填充颜色（渐变） | `"linear-gradient(180deg, rgba(2,53,107,0.5) 0%, rgba(5,101,164,0.5) 100%)"` |
| `styleType` | 样式类型 | `"round"`(圆角) / `"square"`(直角) |
| `borderColor` | 边框颜色 | `"#A5CCEA"` |
| `fontFamily` | 字体 | `"LCDFont"` |
| `fontSize` | 字体大小 | `34` |
| `flipGap` | 翻牌间隔 | `12` |
| `fontColor` | 字体颜色（渐变） | `"linear-gradient(rgb(255, 255, 255) 0%, rgb(17, 93, 151) 100%)"` |

### numberSet（数字设置）

| 属性 | 说明 | 示例值 |
|------|------|--------|
| `intFigure` | 整数位数 | `8` |
| `decimalFigure` | 小数位数 | `2` |
| `thousandthPlace` | 千分位 | `"thousandthPlaceChecked"` / `"thousandthPlaceUnchecked"` |

## 示例：基于真实大屏配置

以下配置来自"数字大屏表格脚本组件-四川科景"大屏中的翻牌器组件：

```json
{
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
        }
    ],
    "modelId": 2586391007,
    "styleJson": {
        "screenPosition": {
            "position": {
                "w": 455,
                "x": 1920,
                "h": 320,
                "y": 1080
            }
        },
        "drawSettings": {
            "fillColor": "linear-gradient(180deg, rgba(2,53,107,0.5) 0%, rgba(5,101,164,0.5) 100%)",
            "styleType": "round",
            "borderColor": "#A5CCEA",
            "lineWidthMap": {
                "width": 1,
                "style": "solid"
            },
            "fontFamily": "LCDFont",
            "fontSize": 34,
            "flipGap": 12,
            "fontColor": "linear-gradient(rgb(255, 255, 255) 0%, rgb(17, 93, 151) 100%)"
        },
        "numberSet": {
            "intFigure": 8,
            "decimalFigure": 2,
            "thousandthPlace": "thousandthPlaceChecked"
        }
    },
    "viewName": "翻牌器1"
}
```

## 更新翻牌器样式

```bash
# 更新翻牌器样式参数
python3 scripts/update_screen.py --screen-id 3654239893 \
  --uuid "grid-type:flipper-uuid:xxx" \
  --flipper-int-figure 10 \
  --flipper-decimal-figure 2 \
  --flipper-thousandth true \
  --flipper-style-type round \
  --flipper-font-size 40 \
  --flipper-fill-color "linear-gradient(180deg, rgba(2,53,107,0.5) 0%, rgba(5,101,164,0.5) 100%)" \
  --flipper-border-color "#A5CCEA" \
  --flipper-flip-gap 15
```

## 适用场景

| 场景 | 推荐 |
|------|------|
| 金额展示（带动画效果） | ✅ 翻牌器 |
| 简单数字展示 | ❌ 指标卡 |
| 多指标对比 | ❌ 柱图/条形图 |
| 趋势分析 | ❌ 折线图 |

## 注意事项

1. **位数规划**：根据数据范围合理设置 `intFigure`，避免溢出
2. **千分位**：大金额建议开启千分位，便于阅读
3. **翻牌间隔**：`flipGap` 影响翻牌动画的间隔时间，值越大间隔越长
4. **颜色渐变**：翻牌器支持线性渐变颜色，可用于营造科技感