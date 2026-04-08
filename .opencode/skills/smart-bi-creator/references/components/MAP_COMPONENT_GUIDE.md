# 地图组件使用指南

## 概述

地图组件用于展示**地理分布数据**，通过不同颜色或渐变显示各地区的数值差异，适合：
- 项目分布区域分析
- 销售网络可视化
- 业务覆盖范围展示
- 区域对比分析

## 组件特点

### 1. 地理维度
- 使用省市区字段（如 `field27__province`）作为维度
- 自动匹配中国省份/城市地图
- 支持区域钻取（省级 → 市级 → 区级）

### 2. 颜色映射
- 支持单色渐变（如蓝色系）
- 支持多色分段（如七色图）
- 数值越大颜色越深/越鲜艳

### 3. 视觉醒目
- 适合作为大屏**视觉焦点**
- 通常放置在画布中央位置
- 尺寸较大以显示清晰

## 使用方法

### 基础示例

```bash
python3 scripts/add_component.py \
  --screen-id 3654572744 \
  --model-id 2592797039 \
  --dimension-field field27__province \
  --indicator-field field3 \
  --chart-type map \
  --top 198 --left 445 \
  --width 1030 --height 542 \
  --view-name "项目分布地图"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654572744 |
| --model-id | 是 | 数据模型 ID | 2592797039 |
| --dimension-field | 是 | 地理维度字段（省/市/区） | field27__province |
| --indicator-field | 是 | 指标字段（数值） | field3 |
| --chart-type | 是 | 图表类型，固定为 `map` | map |
| --top | 是 | Y 坐标 | 198 |
| --left | 是 | X 坐标 | 445 |
| --width | 是 | 组件宽度 | 1030 |
| --height | 是 | 组件高度 | 542 |
| --view-name | 否 | 视图标题 | "项目分布地图" |

### 尺寸建议

| 场景 | 推荐宽度 | 推荐高度 | 说明 |
|------|---------|---------|------|
| 视觉焦点（中央） | 800-1000 | 500-650 | 作为主图表居中展示 |
| 侧边辅助 | 400-500 | 300-400 | 较小范围的区域展示 |
| 小型预览 | 300-400 | 200-300 | 辅助展示 |

## 样式配置

### 完整样式结构

```json
{
  "screenPosition": {
    "position": {"x": 445, "y": 198, "w": 1030, "h": 542}
  },
  "legend": {
    "textSetMap": {"textColor": "#177DDC"}
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
    "content": ["dimension", "measure"]
  },
  "drawSettings": {
    "colorSettingMap": {
      "color": "linear-gradient(90deg, rgb(188,219,249) 0%, rgb(33,114,244) 100%)",
      "colorType": "singleColor"
    },
    "areaColors": ["#E17372", "#FF8242", "#F6B747", "#7EC580", "#EDF77C", "#59CBBF", "#7A8ACE"]
  },
  "label": {
    "isExtra": true,
    "textSetMap": {
      "size": 10,
      "textItalic": false,
      "textBold": false,
      "fontSize": 10,
      "textColor": "#A6ADD0"
    },
    "contentType": "content",
    "content": []
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
  --uuid "grid-type:map-uuid:xxx" \
  --card-background-color "rgba(13, 24, 44, 0.8)" \
  --card-border "rgba(30, 39, 55, 0.8)" \
  --card-padding 12
```

### 关键样式说明

#### 1. 颜色渐变配置（单色渐变）
```json
"drawSettings": {
  "colorSettingMap": {
    "color": "linear-gradient(90deg, rgb(188,219,249) 0%, rgb(33,114,244) 100%)",
    "colorType": "singleColor"
  }
}
```
- `colorType`: `singleColor` 表示单色渐变
- `color`: 线性渐变，从浅蓝到深蓝
- 数值越大，颜色越深

#### 2. 多色分段配置（七色图）
```json
"drawSettings": {
  "areaColors": ["#E17372", "#FF8242", "#F6B747", "#7EC580", "#EDF77C", "#59CBBF", "#7A8ACE"]
}
```
- 7 个颜色对应 7 个数值区间
- 从红(高) → 橙 → 黄 → 绿(低)
- 适合展示离散分布数据

#### 3. 图例配置
```json
"legend": {
  "textSetMap": {"textColor": "#177DDC"}
}
```
- 地图组件图例较简单
- 只配置文字颜色

#### 4. 提示框配置
```json
"tooltip": {
  "backgroundColor": "#303467",
  "content": ["dimension", "measure"]
}
```
- 悬停显示地区名称和数值
- 深色背景配浅色文字

#### 5. 地图标签
```json
"label": {
  "contentType": "content",
  "content": []
}
```
- 默认不显示省份名称标签
- 如需显示，可添加 `content: ["dimension"]`

## 数据要求

### 地理字段

地图组件需要**省市区类型字段**，通常命名规律：
- `field27__province` - 省份
- `field27__city` - 城市
- `field27__district` - 区县

### 字段类型

| 字段类型 | nativeType | 说明 |
|---------|------------|------|
| 省份 | TEXT | 如 "广东省"、"山东省" |
| 城市 | TEXT | 如 "广州市"、"深圳市" |
| 区县 | TEXT | 如 "天河区"、"南山区" |

### 示例数据

```
dimension_field     | indicator_field (field3)
--------------------|----------------------
广东省              | 1250000
浙江省              | 980000
江苏省              | 870000
北京市              | 1500000
上海市              | 1350000
```

## 实战案例

### 案例 1：项目分布地图（中央焦点）

```bash
# 作为大屏视觉焦点，放置在中央位置
python3 scripts/add_component.py \
  --screen-id 3654572744 \
  --model-id 2592797039 \
  --dimension-field field27__province \
  --indicator-field field3 \
  --chart-type map \
  --top 198 --left 445 \
  --width 1030 --height 542 \
  --view-name "项目分布地图"
```

### 案例 2：左侧区域分析

```bash
# 较小尺寸，作为辅助分析
python3 scripts/add_component.py \
  --screen-id 3654572744 \
  --model-id 2592797039 \
  --dimension-field field27__province \
  --indicator-field field3 \
  --chart-type map \
  --top 200 --left 20 \
  --width 400 --height 300 \
  --view-name "华南地区分布"
```

### 案例 3：与指标卡组合

```bash
# 上方 4 个指标卡
python3 scripts/add_component.py \
  --screen-id 3654572744 \
  --model-id 2592797039 \
  --dimension-field receivingDate \
  --indicator-field field3 \
  --chart-type metric \
  --top 80 --left 20 \
  --width 230 --height 100 \
  --view-name "项目总数" && \
python3 scripts/add_component.py \
  --screen-id 3654572744 \
  --model-id 2592797039 \
  --dimension-field field27__province \
  --indicator-field field3 \
  --chart-type map \
  --top 200 --left 300 \
  --width 900 --height 500 \
  --view-name "项目区域分布"
```

## 与其他组件配合

### 推荐布局

```
+--------------------------------------------------+
| [指标卡1] [指标卡2] [指标卡3] [指标卡4]          |
+--------------------------------------------------+
|                                                  |
|  +-----------+    +-----------+    +-----------+ |
|  | 柱图 1    |    |   地图    |    | 柱图 2   | |
|  | (左侧)   |    | (中央焦点) |    | (右侧)   | |
|  +-----------+    +-----------+    +-----------+ |
|                                                  |
+--------------------------------------------------+
|        [底部：条形图 + 饼图组合]                  |
+--------------------------------------------------+
```

### 布局建议

1. **地图 + 柱图**：地图展示区域分布，柱图展示具体数值
2. **地图 + 饼图**：地图展示位置，饼图展示占比
3. **地图 + 排名图**：地图定位，排名图展示 Top N

## 注意事项

### 1. 数据匹配
- 地理字段值必须与系统地图数据匹配
- 如 "广东省" 不能写成 "广东"
- 建议使用标准行政区划名称

### 2. 尺寸要求
- 地图组件**高度至少 250px**
- 宽度过小会导致省份名称显示不全
- 建议作为主图表使用较大尺寸

### 3. 颜色选择
- 单色渐变：适合展示连续分布
- 七色图：适合展示离散分段
- 避免使用过多颜色（影响美观）

### 4. 无数据地区
- 没有数据的地区显示为灰色或透明
- 可在 `areaColors` 首位置添加灰色

## 常见问题

### Q1: 地图不显示某些省份？
- 检查地理字段值是否正确
- 确保数据中存在该省份的记录

### Q2: 颜色与数值不匹配？
- 检查 `colorType` 设置
- `singleColor` 表示渐变色
- 多颜色分段使用 `areaColors`

### Q3: 如何只显示部分省份？
- 在数据模型中添加过滤条件
- 或在 dimension 中使用过滤配置

### Q4: 地图背景如何设置透明？
- 设置 `card.cardBackgroundColor: ""`
- 或设置 `card.border: "transparent"`

## 参考资源

- [SKILL.md](../../SKILL.md) - 技能主文档
- [add_component.py](../scripts/add_component.py) - 组件添加脚本
- [new.curl](../../new.curl) - 完整示例大屏配置
