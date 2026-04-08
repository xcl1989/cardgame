# 表格组件使用指南

表格组件用于展示**结构化数据**，适合展示明细数据、列表数据等场景。

> **注意**：系统内部使用的类型是 `customTable`，脚本会自动处理转换。

## 快速开始

```bash
# 添加单维度单指标表格
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2586391007 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type table \
  --top 200 --left 50 \
  --width 600 --height 300 \
  --view-name "收款明细"
```

## 多维度多指标表格

表格组件支持添加多个维度和指标，使用 `--extra-dimension-fields` 和 `--extra-indicator-fields` 参数：

```bash
# 添加多维度多指标表格
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2586391007 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type table \
  --top 200 --left 50 \
  --width 800 --height 400 \
  --view-name "收款明细" \
  --extra-dimension-fields "projectNo" \
  --extra-indicator-fields "invoiceReceivingAmount"
```

## 配置结构

表格组件的 `styleJson` 包含以下关键配置：

### tableBodySettings（表格内容样式）

| 属性 | 说明 | 示例值 |
|------|------|--------|
| `fontFamily` | 字体 | `"default"` |
| `rowSplitLine.size` | 行分割线宽度 | `1` |
| `rowSplitLine.color` | 行分割线颜色 | `"#334979"` |
| `textSetMap.textColor` | 文字颜色 | `"#DBDFF1"` |
| `textSetMap.fontSize` | 字体大小 | `12` |
| `oddNumberedColor` | 奇数行背景色 | `"#0A1E38"` |
| `evenNumberedColor` | 偶数行背景色 | `"#020B1C"` |
| `lineHeight` | 行高倍数 | `2` |
| `colSplitLine.size` | 列分割线宽度 | `0` |

### tableHeaderSettings（表头样式）

| 属性 | 说明 | 示例值 |
|------|------|--------|
| `fontFamily` | 字体 | `"default"` |
| `bgColor` | 背景色 | `"#08143E"` |
| `textSetMap.textColor` | 文字颜色 | `"#DBDFF1"` |
| `textSetMap.fontSize` | 字体大小 | `12` |
| `textSetMap.textBold` | 是否加粗 | `true` |
| `lineHeight` | 行高倍数 | `2` |

### 样式预设（preSetStyle）

```json
"preSetStyle": {
    "themeColor": 0
}
```

### 滚动设置（scroll）

```json
"scroll": {
    "isExtra": true,
    "show": false,
    "type": "smooth",
    "speed": 3
}
```

## 示例：基于真实大屏配置

以下配置来自"数字大屏表格脚本组件-四川科景"大屏中的表格组件：

```json
{
    "dimensions": [
        {
            "datasetId": 2148797900,
            "fieldLabel": "收款日期",
            "fieldName": "receivingDate",
            "groupBy": true,
            "index": 0,
            "modelDatasetName": "collectionReg3X",
            "nativeType": "DATE",
            "dateFormat": "YMD"
        },
        {
            "datasetId": 2148783937,
            "fieldLabel": "项目名称",
            "fieldName": "projectNo",
            "groupBy": true,
            "index": 1,
            "modelDatasetName": "project3X",
            "nativeType": "TEXT"
        }
    ],
    "indicators": [
        {
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
            "datasetId": 2148797900,
            "fieldLabel": "本次关联发票收款金额",
            "fieldName": "invoiceReceivingAmount",
            "index": 1,
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
        "preSetStyle": {"themeColor": 0},
        "screenPosition": {
            "position": {"w": 455, "x": 1920, "h": 320, "y": 1080}
        },
        "tableBodySettings": {
            "fontFamily": "default",
            "rowSplitLine": {"size": 1, "color": "#334979"},
            "textSetMap": {
                "textItalic": false,
                "textBold": false,
                "fontSize": 12,
                "textColor": "#DBDFF1"
            },
            "oddNumberedColor": "#0A1E38",
            "lineHeight": 2,
            "evenNumberedColor": "#020B1C",
            "colSplitLine": {"size": 0, "color": "#334979"}
        },
        "tableHeaderSettings": {
            "fontFamily": "default",
            "bgColor": "#08143E",
            "textSetMap": {
                "textItalic": false,
                "textBold": true,
                "fontSize": 12,
                "textColor": "#DBDFF1"
            },
            "colIndex": [""],
            "lineHeight": 2
        },
        "scroll": {
            "isExtra": true,
            "show": false,
            "type": "smooth",
            "speed": 3
        }
    },
    "viewName": "表格1"
}
```

## 适用场景

| 场景 | 推荐 |
|------|------|
| 明细数据查看 | ✅ 表格 |
| 排行榜 Top N | ❌ 排名图 |
| 趋势分析 | ❌ 柱图/折线图 |
| 占比分析 | ❌ 饼图 |
| 单指标展示 | ❌ 指标卡 |

## 注意事项

1. **数据量控制**：表格展示数据条数较多时，建议设置 `limit` 参数限制
2. **列宽设置**：列宽由系统自动分配，如需精确控制可后续手动调整
3. **奇偶行颜色**：默认开启奇偶行交替颜色，便于行间区分