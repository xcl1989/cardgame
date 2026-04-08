# 配置结构详解 (Config Structure)

## 完整大屏 JSON 结构

```json
{
  "name": "测试的大屏 0318",
  "config": {
    "theme": "lgScreenDefault",
    "style": {
      "fontFamily": "default",
      "cardBorderRadius": 6,
      "panelBackgroundImage": "",
      "panelBackgroundImageRepeat": "cover",
      "cardBackgroundImage": "",
      "cardBackgroundImageRepeat": "cover",
      "titleColor": "#FEFEFE",
      "textColor": "#A6ADD0",
      "cardBackgroundColor": "rgba(13, 24, 44, 1.0)",
      "panelBackgroundColor": "#000",
      "lineColor": "#313358",
      "linkColor": "#177DDC",
      "colorSystem": "dark",
      "graColorSystemCustomColors": [
        "linear-gradient( 180deg, #2897FF 0%, #0049DA 100%)",
        "linear-gradient( 180deg, #00F5FF 0%, #035EB9 100%)"
      ]
    },
    "page": {
      "windowFlex": "WidthResponsive"
    },
    "canvas": {
      "canvasWidth": 1920,
      "canvasHeight": 1080,
      "canvasSize": 1,
      "canvasRatioLocked": false,
      "canvasRatio": ""
    },
    "timeSwitch": {
      "timeSwitchUnit": "second",
      "timeSwitchTimer": 30
    },
    "previewSetting": {
      "previewSettingType": "actualSize"
    },
    "layers": [
      {
        "uuid": "grid-type:bar-uuid:1773814252921",
        "top": 100,
        "left": 100,
        "width": 960,
        "height": 540
      }
    ]
  },
  "layouts": [
    {
      "uuid": "grid-type:bar-uuid:1773814252921",
      "title": "柱图 1",
      "type": "bar",
      "icon": "chart_vertical_bar.png",
      "groupLabel": "图形组件",
      "gridData": {},
      "resizeHandles": ["s", "e", "se"]
    }
  ],
  "componentMap": {
    "grid-type:bar-uuid:1773814252921": {
      "modelId": 3562329848,
      "modelInfo": [...],
      "key": "grid-type:bar-uuid:1773814252921",
      "viewName": "柱图 1",
      "parentUuid": "",
      "tabName": "",
      "styleJson": {...},
      "dimensions": [...],
      "indicators": [...],
      "limit": {"isSelect": true, "errText": "", "value": 10}
    }
  },
  "topLayouts": []
}
```

## config 字段说明

### style

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| fontFamily | string | default | 字体家族 |
| cardBorderRadius | number | 6 | 卡片圆角 |
| titleColor | string | #FEFEFE | 标题颜色 |
| textColor | string | #A6ADD0 | 文本颜色 |
| cardBackgroundColor | string | rgba(13, 24, 44, 1.0) | 卡片背景色 |
| panelBackgroundColor | string | #000 | 面板背景色 |
| colorSystem | string | dark | 颜色系统 (dark/light) |

### canvas

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| canvasWidth | number | 1920 | 画布宽度 |
| canvasHeight | number | 1080 | 画布高度 |
| canvasSize | number | 1 | 画布缩放比例 |
| canvasRatioLocked | boolean | false | 锁定宽高比 |

## componentMap 结构

每个组件包含以下核心字段：

### modelInfo

数据模型信息数组，包含模型的所有字段定义。

### dimensions

维度字段数组（X 轴），用于分组或分类。

### indicators

指标字段数组（Y 轴），用于数值计算和展示。

### styleJson

组件详细样式配置：

```json
{
  "screenPosition": {
    "position": {"x": 1920, "y": 1080, "w": 960, "h": 540}
  },
  "card": {
    "lineWidthMap": {"width": 1, "style": "solid"},
    "padding": 12,
    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
    "border": "rgba(30, 39, 55, 0.8)"
  },
  "title": {
    "isExtra": true,
    "textSetMap": {
      "fontSize": 20,
      "textColor": "#FEFEFE",
      "textBold": true
    }
  },
  "drawSettings": {
    "seriesType": "bar",
    "widthMap": {"isAdaption": true},
    "gridSet": {"isAdaption": true}
  },
  "axis": {
    "x": {
      "axes": ["showXAxis"],
      "scale": "auto",
      "textSetMap": {"fontSize": 14, "textColor": "#a7adcd"}
    },
    "y": {
      "axes": ["showYAxis", "showAxisLine"],
      "textSetMap": {"fontSize": 14, "textColor": "#a7adcd"}
    }
  },
  "legend": {...},
  "tooltip": {...},
  "label": {...},
  "scroll": {...},
  "textData": {...}
}
```

## 重要注意事项

1. **UUID 一致性**: `config.layers[].uuid`、`layouts[].uuid`、`componentMap` 的键、`component.key` 必须相同

2. **尺寸同步**: `config.layers[].width/height` 和 `styleJson.screenPosition.position.w/h` 应保持一致

3. **字段完整性**: `dimensions` 和 `indicators` 必须包含 `fields` 数组（模型所有字段）和 `nodeInfo` 对象

## 多组件大屏结构

一个大屏可以包含多个组件，每个组件有独立的配置：

### 组件类型支持

| 类型 | type 值 | icon 值 | 说明 |
|------|--------|--------|------|
| 柱状图 | bar | chart_vertical_bar.png | 垂直柱图 |
| 折线图 | line | chart_line.png | 折线趋势图 |
| 饼图 | pie | chart_pie.png | 饼图/环形图 |
| 指标卡 | metric | indicator.png | 数字指标展示 |
| 表格 | table | table.png | 数据表格 |
| 地图 | script | chart_script_component.png | 地图组件 |
| 文本 | text | chart_text_component.png | 文本标题 |
| 装饰 | decorate | chart_decorate_component.png | 装饰元素 |
| 时间 | time | chart_time_component.png | 时间显示 |
| 走马灯 | marquee | chart_marquee_component.png | 滚动文字 |

### 多组件配置示例

```json
{
  "name": "数字大屏演示",
  "config": {
    "canvas": {"canvasWidth": 1920, "canvasHeight": 1080},
    "layers": [
      {"uuid": "uuid-1", "top": 248, "left": 321, "width": 1279, "height": 916},
      {"uuid": "uuid-2", "top": 436, "left": 47, "width": 440, "height": 270},
      {"uuid": "uuid-3", "top": 788, "left": 47, "width": 440, "height": 270}
    ]
  },
  "layouts": [
    {"uuid": "uuid-1", "title": "地图", "type": "script"},
    {"uuid": "uuid-2", "title": "柱图 1", "type": "bar"},
    {"uuid": "uuid-3", "title": "线图 1", "type": "line"}
  ],
  "componentMap": {
    "uuid-1": {"modelId": 123, "viewName": "地图", "type": "script", ...},
    "uuid-2": {"modelId": 456, "viewName": "柱图分析", "type": "bar", ...},
    "uuid-3": {"modelId": 789, "viewName": "趋势分析", "type": "line", ...}
  }
}
```

### 图层管理

- **layers 数组**: 定义所有组件的位置和大小，按 Z 轴顺序排列（索引越大越靠上）
- **每个图层**: 包含 `uuid`, `top`, `left`, `width`, `height`, `title`, `type`
- **resizeHandles**: 定义可调整大小的方向 `["s", "e", "se"]`

### 组件布局示例

```
画布：1920 x 1080

+--------------------------------------------------+
| 装饰条 (top: -38, height: 150)                    |
| 走马灯 (top: 82)   时间 (top: 87, left: 1438)    |
+--------------------------------------------------+
| 指标卡 1 (left: 49)                               |
| 指标卡 2 (left: 49)                               |
|                                                   |
| +-------+                         +-------+      |
| | 柱图 1 |        地 图             | 柱图 2 |      |
| +-------+      (居中展示)          +-------+      |
|                                                   |
| +-------+                         +-------+      |
| | 线图 1 |                         | 饼图 1 |      |
| +-------+                         +-------+      |
+--------------------------------------------------+
```
