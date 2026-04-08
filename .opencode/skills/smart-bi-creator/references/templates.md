# 示例配置模板 (Templates)

## 柱状图配置模板

```json
{
  "name": "项目收款分析大屏",
  "config": {
    "theme": "lgScreenDefault",
    "style": {
      "fontFamily": "default",
      "cardBorderRadius": 6,
      "titleColor": "#FEFEFE",
      "textColor": "#A6ADD0",
      "cardBackgroundColor": "rgba(13, 24, 44, 1.0)",
      "panelBackgroundColor": "#000",
      "colorSystem": "dark"
    },
    "canvas": {
      "canvasWidth": 1920,
      "canvasHeight": 1080,
      "canvasSize": 1
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
      "viewName": "柱图 1",
      "styleJson": {
        "screenPosition": {"position": {"x": 1920, "y": 1080, "w": 960, "h": 540}},
        "drawSettings": {"seriesType": "bar", "widthMap": {"isAdaption": true}},
        "title": {"isExtra": true, "textSetMap": {"fontSize": 20, "textColor": "#FEFEFE", "textBold": true}}
      },
      "dimensions": [...],
      "indicators": [...],
      "limit": {"isSelect": true, "value": 10}
    }
  }
}
```

## 折线图配置模板

```json
{
  "layouts": [{
    "uuid": "grid-type:line-uuid:1773814252921",
    "title": "折线图 1",
    "type": "line",
    "icon": "chart_line.png",
    "groupLabel": "图形组件"
  }],
  "componentMap": {
    "grid-type:line-uuid:1773814252921": {
      "modelId": 3562329848,
      "viewName": "折线图 1",
      "styleJson": {
        "drawSettings": {"seriesType": "line"}
      }
    }
  }
}
```

## 饼图配置模板

```json
{
  "layouts": [{
    "uuid": "grid-type:pie-uuid:1773814252921",
    "title": "饼图 1",
    "type": "pie",
    "icon": "chart_pie.png",
    "groupLabel": "图形组件"
  }],
  "componentMap": {
    "grid-type:pie-uuid:1773814252921": {
      "modelId": 3562329848,
      "viewName": "饼图 1",
      "styleJson": {
        "drawSettings": {"seriesType": "pie"}
      }
    }
  }
}
```

## 指标卡配置模板

```json
{
  "layouts": [{
    "uuid": "grid-type:indicator-uuid:1773814252921",
    "title": "指标卡 1",
    "type": "indicator",
    "icon": "indicator.png",
    "groupLabel": "图形组件"
  }],
  "componentMap": {
    "grid-type:indicator-uuid:1773814252921": {
      "modelId": 3562329848,
      "viewName": "指标卡 1",
      "styleJson": {
        "drawSettings": {"seriesType": "indicator"}
      },
      "indicators": [...]
    }
  }
}
```

## 多组件大屏模板

```json
{
  "config": {
    "layers": [
      {"uuid": "grid-type:bar-uuid:1", "top": 50, "left": 50, "width": 900, "height": 500},
      {"uuid": "grid-type:line-uuid:2", "top": 50, "left": 970, "width": 900, "height": 500},
      {"uuid": "grid-type:pie-uuid:3", "top": 570, "left": 50, "width": 900, "height": 460}
    ]
  },
  "layouts": [
    {"uuid": "grid-type:bar-uuid:1", "title": "柱图", "type": "bar"},
    {"uuid": "grid-type:line-uuid:2", "title": "折线图", "type": "line"},
    {"uuid": "grid-type:pie-uuid:3", "title": "饼图", "type": "pie"}
  ],
  "componentMap": {
    "grid-type:bar-uuid:1": {...},
    "grid-type:line-uuid:2": {...},
    "grid-type:pie-uuid:3": {...}
  }
}
```

## 使用脚本生成配置

```bash
# 创建柱状图大屏
python scripts/create_screen.py \
  --name "项目收款分析" \
  --model-id 3562329848 \
  --dimension-field projectNo \
  --dimension-label "项目名称" \
  --indicator-field receivingAmount \
  --indicator-label "收款金额" \
  --metric-type SUM \
  --chart-type bar \
  --width 960 \
  --height 540

# 创建多组件大屏
python scripts/create_multi_screen.py \
  --name "综合大屏" \
  --config configs/multi_screen_config.json
```
