# 指标卡组件使用指南

## 概述

指标卡（Metric Card）是数字大屏中用于突出展示关键绩效指标（KPI）的核心组件，适合：
- 展示汇总数值（如总金额、总数量）
- 突出关键业绩指标
- 实时数据监控
- 目标达成情况展示

## 组件特点

### 1. 数据聚合
- 自动对指标字段进行 SUM 汇总
- 支持多种数值格式（百分比、千分位分隔符等）
- 支持自定义小数位数

### 2. 多种样式预设
支持 5 种预设样式，方便快速创建不同风格的大屏：
- `default`：默认深色卡片样式
- `gradient`：渐变背景样式（醒目数值）
- `light`：浅色背景样式
- `minimal`：极简透明样式
- `card`：圆角卡片样式

### 3. 灵活的颜色定制
- 可自定义数值颜色
- 可自定义标签颜色
- 可自定义图标颜色

## 使用方法

### 基础示例

```bash
# 添加默认样式的指标卡
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 100 --left 50 \
  --width 280 --height 140 \
  --view-name "累计收款"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654239893 |
| --model-id | 是 | 数据模型 ID | 2597080602 |
| --dimension-field | 是 | 维度字段（用于数据分组/过滤） | receivingDate |
| --indicator-field | 是 | 指标字段（会进行 SUM 汇总） | receivingAmount |
| --chart-type | 是 | 图表类型，固定为 `metric` | metric |
| --top | 是 | Y 坐标 | 100 |
| --left | 是 | X 坐标 | 50 |
| --width | 是 | 组件宽度 | 280 |
| --height | 是 | 组件高度 | 140 |
| --view-name | 是 | 指标卡标题 | "累计收款" |
| --metric-style | 否 | 样式预设 | 见下方样式选项 |
| --metric-value-color | 否 | 数值颜色 | #FF6B6B |
| --metric-label-color | 否 | 标签颜色 | #4ECDC4 |
| --metric-icon-color | 否 | 图标颜色 | #5B8FFA |

### 样式选项 (--metric-style)

| 样式 | 说明 | drawSettings.position | gap | 图标位置 |
|------|------|---------------------|-----|----------|
| default | 底部标题，无图标 | "bottom" | 8 | none |
| top | 顶部标题，无图标 | {"position":"top","align":"left"} | 8 | none |
| icon_left | 顶部标题，左侧图标 | {"position":"top","align":"left"} | 12 | left |
| icon_follow | 顶部标题，跟随图标 | {"position":"top","align":"left"} | 12 | follow |
| gradient | 渐变背景样式 | "bottom" | 10 | left |
| light | 浅色背景样式 | "bottom" | 8 | right |
| minimal | 极简透明样式 | "right" | 6 | none |
| card | 圆角卡片样式 | "bottom" | 12 | left |

### 尺寸建议

| 场景 | 推荐宽度 | 推荐高度 | 说明 |
|------|---------|---------|------|
| 顶部指标栏 | 220-280 | 120-150 | 大屏顶部一排展示 |
| 侧边指标卡 | 240-300 | 140-170 | 左右两侧垂直排列 |
| 中心突出展示 | 350-450 | 180-220 | 需要放大的重点指标 |
| 小型指标 | 180-220 | 100-120 | 紧凑布局 |

## 样式预设详解

基于 BIupdate.curl 中 4 个指标卡的真实样式，支持以下预设：

### 1. default（默认样式 - 底部标题）

标题在底部，无图标，间距 8px。

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 100 --left 50 \
  --width 280 --height 140 \
  --view-name "累计收款" \
  --metric-style default
```

**样式特点**：
- `drawSettings.position`: "bottom"
- `drawSettings.gap`: 8
- `drawSettings.iconPositionMap.position`: "none"
- 无 textData 字段

```json
{
  "drawSettings": {
    "position": "bottom",
    "gap": 8,
    "iconPositionMap": {"position": "none"},
    "iconColor": "#5B8FFA"
  }
}
```

### 2. top（顶部标题样式）

标题在顶部，左对齐，无图标，间距 8px。

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 100 --left 350 \
  --width 280 --height 140 \
  --view-name "本月收款" \
  --metric-style top
```

**样式特点**：
- `drawSettings.position`: {"position": "top", "align": "left"}
- `drawSettings.gap`: 8
- `drawSettings.iconPositionMap.position`: "none"
- 有 textData: {"content": []}

```json
{
  "drawSettings": {
    "position": {"position": "top", "align": "left"},
    "gap": 8,
    "iconPositionMap": {"position": "none"},
    "iconColor": "#5B8FFA"
  },
  "textData": {"content": []}
}
```

### 3. icon_left（左侧图标样式）

标题在顶部，左对齐，左侧显示图标，间距 12px。

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 100 --left 650 \
  --width 280 --height 140 \
  --view-name "季度收款" \
  --metric-style icon_left
```

**样式特点**：
- `drawSettings.position`: {"position": "top", "align": "left"}
- `drawSettings.gap`: 12
- `drawSettings.iconPositionMap.position`: "left"
- `drawSettings.iconPositionMap.icon`: "e84d"

```json
{
  "drawSettings": {
    "position": {"position": "top", "align": "left"},
    "gap": 12,
    "iconPositionMap": {"position": "left", "icon": "e84d"},
    "iconColor": "#5B8FFA"
  }
}
```

### 4. icon_follow（跟随图标样式）

标题在顶部，左对齐，图标跟随数值显示，间距 12px。

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 100 --left 950 \
  --width 280 --height 140 \
  --view-name "年度收款" \
  --metric-style icon_follow
```

**样式特点**：
- `drawSettings.position`: {"position": "top", "align": "left"}
- `drawSettings.gap`: 12
- `drawSettings.iconPositionMap.position`: "follow"
- `drawSettings.iconPositionMap.icon`: "e84d"

```json
{
  "drawSettings": {
    "position": {"position": "top", "align": "left"},
    "gap": 12,
    "iconPositionMap": {"position": "follow", "icon": "e84d"},
    "iconColor": "#5B8FFA"
  }
}
```

### 5. gradient（渐变样式）

渐变背景，醒目数值，适合突出重点指标。

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 100 --left 350 \
  --width 280 --height 140 \
  --view-name "本月收款" \
  --metric-style gradient
```

**样式特点**：
- 背景：`rgba(40, 60, 120, 0.9)` 深蓝渐变
- 标题：浅蓝白 #E0E6FF，18px，粗体
- 数值：青色 #00F5FF，38px，粗体（非常醒目）
- 图标：左侧显示，青色

### 6. light（浅色样式）

浅色背景，深色文字，适合浅色主题或需要高可读性的场景。

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 100 --left 650 \
  --width 280 --height 140 \
  --view-name "季度收款" \
  --metric-style light
```

**样式特点**：
- 背景：`rgba(240, 245, 255, 0.95)` 浅蓝灰
- 标题：深灰 #2C3E50，20px，粗体
- 数值：深青 #1A5F7A，36px，粗体

### 7. minimal（极简样式）

无边框，透明背景，极简设计，适合叠加在其他组件上。

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 100 --left 950 \
  --width 240 --height 120 \
  --view-name "年度目标" \
  --metric-style minimal
```

**样式特点**：
- 背景：完全透明 `rgba(0, 0, 0, 0)`
- 无边框、无图标
- 最小化的视觉干扰

### 8. card（卡片样式）

圆角边框，醒目边框色，现代卡片设计风格。

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 100 --left 1210 \
  --width 280 --height 140 \
  --view-name "项目数量" \
  --metric-style card
```

**样式特点**：
- 背景：`rgba(20, 30, 60, 0.85)` 深蓝灰
- 数值：亮青 #66DDFF，36px，粗体
- 边框：2px 实线，12px 圆角，蓝白边框

## 颜色定制

### 自定义数值颜色

使用 `--metric-value-color` 参数自定义数值颜色：

```bash
# 红色数值（适合警示/支出类指标）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field paymentAmount \
  --chart-type metric \
  --top 100 --left 50 \
  --width 280 --height 140 \
  --view-name "本月支出" \
  --metric-style default \
  --metric-value-color "#FF6B6B"
```

### 自定义标签颜色

使用 `--metric-label-color` 参数同时修改标题和标签颜色：

```bash
# 绿色标签（适合增长/收入类指标）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 100 --left 350 \
  --width 280 --height 140 \
  --view-name "本月收入" \
  --metric-style default \
  --metric-label-color "#4ECDC4"
```

### 组合使用

可以同时指定多种颜色：

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 100 --left 650 \
  --width 280 --height 140 \
  --view-name "净利润" \
  --metric-style gradient \
  --metric-value-color "#00FF88" \
  --metric-label-color "#FFFFFF" \
  --metric-icon-color "#00FF88"
```

## 实战案例

### 案例 1：顶部指标栏

在大屏顶部创建一排 4 个指标卡，展示关键汇总数据：

```bash
# 指标卡 1：累计收款
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 60 --left 20 \
  --width 230 --height 130 \
  --view-name "累计收款" \
  --metric-style default && \

# 指标卡 2：本月收款
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 60 --left 270 \
  --width 230 --height 130 \
  --view-name "本月收款" \
  --metric-style gradient && \

# 指标卡 3：季度收款
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 60 --left 520 \
  --width 230 --height 130 \
  --view-name "季度收款" \
  --metric-style card && \

# 指标卡 4：年度收款
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 60 --left 770 \
  --width 230 --height 130 \
  --view-name "年度收款" \
  --metric-style light
```

**布局效果**：
```
+------------------------------------------------------------------+
| [累计收款]  [本月收款]  [季度收款]  [年度收款]                      |  ← top: 60
|   ¥888万      ¥128万      ¥356万      ¥1,280万                      |
+------------------------------------------------------------------+
```

### 案例 2：侧边指标栏

在大屏左侧创建垂直排列的指标卡：

```bash
# 左侧指标卡 1
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 220 --left 20 \
  --width 260 --height 160 \
  --view-name "项目总数" \
  --metric-style card \
  --metric-value-color "#66DDFF" && \

# 左侧指标卡 2
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 400 --left 20 \
  --width 260 --height 160 \
  --view-name "进行中" \
  --metric-style gradient \
  --metric-value-color "#FFD700" && \

# 左侧指标卡 3
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 580 --left 20 \
  --width 260 --height 160 \
  --view-name "已完成" \
  --metric-style default \
  --metric-value-color "#4ECDC4"
```

### 案例 3：突出展示重点指标

使用 gradient 或 card 样式突出展示核心指标：

```bash
# 核心指标：年度目标完成率
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 300 --left 600 \
  --width 400 --height 200 \
  --view-name "年度目标完成率" \
  --metric-style gradient \
  --metric-value-color "#00FF88" \
  --metric-label-color "#FFFFFF"
```

## 样式配置结构

### 完整样式 JSON

```json
{
  "screenPosition": {
    "position": {"x": 50, "y": 100, "w": 280, "h": 140}
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
      "textBold": true,
      "textItalic": false
    }
  },
  "metricName": {
    "isExtra": true,
    "textSetMap": {
      "fontSize": 24,
      "textColor": "#A6ADD0",
      "textBold": false,
      "textItalic": false
    }
  },
  "metricValue": {
    "textSetMap": {
      "fontSize": 34,
      "textColor": "#A6ADD0",
      "textBold": false,
      "textItalic": false
    },
    "prefixFontSize": 30,
    "suffixFontSize": 12
  },
  "drawSettings": {
    "position": "bottom",
    "gap": 8,
    "iconPositionMap": {"position": "none"},
    "iconColor": "#5B8FFA"
  }
}
```

### 关键样式说明

#### 1. 卡片背景
```json
"card": {
  "lineWidthMap": {"width": 1, "style": "solid"},
  "padding": 12,
  "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
  "border": "rgba(30, 39, 55, 0.8)"
}
```
- `cardBackgroundColor`: 背景颜色，支持 RGBA 格式（0.8 = 80% 透明度）
- `padding`: 内边距
- `border`: 边框颜色

#### 2. 标题样式
```json
"title": {
  "isExtra": true,
  "textSetMap": {
    "fontSize": 20,
    "textColor": "#FEFEFE",
    "textBold": true,
    "textItalic": false
  }
}
```
- `isExtra`: 是否额外显示
- `fontSize`: 字体大小
- `textColor`: 文字颜色
- `textBold`: 是否粗体

#### 3. 数值样式
```json
"metricValue": {
  "textSetMap": {
    "fontSize": 34,
    "textColor": "#A6ADD0",
    "textBold": false,
    "textItalic": false
  },
  "prefixFontSize": 30,
  "suffixFontSize": 12
}
```
- `metricValue`: 数值本身的大小和颜色
- `prefixFontSize`: 单位前缀（如"¥"符号）的大小
- `suffixFontSize`: 后缀（如百分比"%"）的大小

#### 4. 图标设置
```json
"drawSettings": {
  "position": "bottom",
  "gap": 8,
  "iconPositionMap": {"position": "none"},
  "iconColor": "#5B8FFA"
}
```
- `position`: 图标位置（bottom/left/right/none）
- `iconColor`: 图标颜色

## 数值格式化

指标卡的数值格式化通过 `valueFormat` 参数控制：

```json
"valueFormat": {
  "isPercentage": 0,
  "decimalPlaces": 2,
  "useThousandsSeparator": 0
}
```

| 参数 | 说明 | 示例值 |
|------|------|--------|
| isPercentage | 是否显示为百分比 | 0=否, 1=是 |
| decimalPlaces | 小数位数 | 2 |
| useThousandsSeparator | 是否使用千分位分隔符 | 0=否, 1=是 |

**示例**：显示为百分比，保留 2 位小数
```json
"valueFormat": {
  "isPercentage": 1,
  "decimalPlaces": 2,
  "useThousandsSeparator": 1
}
```

## 注意事项

### 1. 数据聚合
- 指标卡默认对指标字段进行 **SUM**（求和）汇总
- 如需其他聚合方式（如 AVG、COUNT），目前需要手动修改 JSON 配置

### 2. 维度字段
- 维度字段用于数据过滤和分组
- 如果不指定维度，会对所有数据进行汇总
- 建议选择一个有意义的时间字段作为维度

### 3. 指标重命名

**通过 `newFieldLabel` 可以修改指标的显示名称：**

```python
"indicators": [{
    "fieldName": "receivingAmount",
    "newFieldLabel": "本月收款金额",  # 修改后的名称
    "metricType": "SUM"
}]
```

### 4. 尺寸要求
- 最小宽度：200px
- 最小高度：110px
- 推荐高度：120-150px（确保数值完整显示）

### 4. 样式组合
- 预设样式（`--metric-style`）和自定义颜色可以组合使用
- 自定义颜色会覆盖预设的对应颜色

### 5. 串行执行
- 添加多个指标卡时**必须串行执行**
- 使用 `&&` 连接多个命令，避免覆盖

### 6. 颜色设计原则（重要！）

**多个指标卡颜色要统一协调，不要五颜六色！**

**推荐做法：**
- 同一大屏中的指标卡使用**相同颜色**或**同色系**
- 科技风格大屏推荐使用科技蓝 `#00D4FF` 或蓝绿色系
- 保持视觉一致性，避免花哨

**颜色推荐：**
| 风格 | 颜色代码 | 效果 |
|------|----------|------|
| 科技蓝 | `#00D4FF` | 现代、科技感 |
| 渐变蓝 | `#00F5FF` | 醒目、活泼 |
| 金色 | `#FFB800` | 高端、尊贵 |
| 绿色 | `#00FF88` | 健康、增长 |

**示例：统一使用科技蓝**
```bash
# 第一个指标卡
--metric-value-color "#00D4FF"

# 后续所有指标卡都使用相同颜色
--metric-value-color "#00D4FF"
```

**错误示例（不要这样）：**
```bash
# ❌ 每个指标卡用不同颜色，五颜六色很丑
--metric-value-color "#00FF88"  # 绿色
--metric-value-color "#FF6B6B"  # 红色
--metric-value-color "#9B59B6"  # 紫色
--metric-value-color "#3498DB"  # 蓝色
```

### 7. 布局对齐原则（重要！）

**多个指标卡必须左右对齐，保持整齐美观！**

**布局计算公式：**
```
画布宽度 = 1920
左边距 = 20px
右边距 = 20px
指标卡数量 = n
指标卡间距 = 20px
指标卡宽度 = (1920 - 40 - (n-1)*20) / n
```

**示例：7个指标卡**
```python
canvas_width = 1920
left_margin = 20
right_margin = 20
num_cards = 7
gap = 20

usable_width = canvas_width - left_margin - right_margin
card_width = (usable_width - (num_cards - 1) * gap) // num_cards
# card_width = (1880 - 120) // 7 = 251px
```

**对齐检查：**
- ✅ 左侧边距 = 右侧边距（对称）
- ✅ 所有指标卡宽度相同
- ✅ 所有间距相同

**错误示例：**
- ❌ 左侧边距20px，右侧边距100px（不对称）
- ❌ 指标卡宽度有的240有的260（不一致）
- ❌ 间距有的20有的30（不整齐）

## 常见问题

### Q1: 如何让指标卡显示百分比？
目前需要在创建后手动修改 JSON 配置中的 `valueFormat`：
```json
"valueFormat": {
  "isPercentage": 1,
  "decimalPlaces": 2,
  "useThousandsSeparator": 0
}
```

### Q2: 数值显示为科学计数法怎么办？
在 `valueFormat` 中设置 `useThousandsSeparator: 1` 启用千分位分隔符，或增加小数位数。

### Q3: 如何让指标卡数值使用不同颜色？
使用 `--metric-value-color` 参数：
```bash
--metric-value-color "#FF6B6B"
```

### Q4: 可以在一个大屏中混用不同样式吗？
可以！每个指标卡都可以独立设置样式：
```bash
# 样式 1
python3 scripts/add_component.py ... --metric-style default

# 样式 2
python3 scripts/add_component.py ... --metric-style gradient

# 样式 3
python3 scripts/add_component.py ... --metric-style card
```

### Q5: 指标卡的高度太小导致数值显示不全？
增加高度到 130px 以上，并适当调整 `padding` 样式。

## 样式 JSON 结构详解

### 样式 JSON 包含的字段

指标卡的 `styleJson` 包含以下主要字段：

```json
{
  "metricName": {
    "isExtra": true,
    "textSetMap": {
      "fontSize": 20,
      "textColor": "#B8C5E8",
      "textBold": false,
      "textItalic": false
    }
  },
  "metricValue": {
    "textSetMap": {
      "fontSize": 38,
      "textColor": "#00F5FF",
      "textBold": true,
      "textItalic": false
    },
    "prefixFontSize": 28,
    "suffixFontSize": 14
  },
  "drawSettings": {
    "gap": 10,
    "iconColor": "#00D4FF",
    "iconPositionMap": {"position": "left"},
    "position": "bottom"
  },
  "title": {
    "isExtra": true,
    "textSetMap": {
      "fontSize": 18,
      "textColor": "#E0E6FF",
      "textBold": true,
      "textItalic": false
    }
  },
  "card": {
    "border": "rgba(70, 130, 220, 0.8)",
    "padding": 16,
    "cardBackgroundColor": "rgba(40, 60, 120, 0.9)",
    "lineWidthMap": {"width": 2, "style": "solid"}
  },
  "screenPosition": {
    "position": {"x": 20, "y": 95, "w": 230, "h": 130}
  }
}
```

| 字段 | 说明 |
|------|------|
| metricName | 指标名称/标签的文字样式 |
| metricValue | 指标数值的文字样式（fontSize、textColor 等） |
| drawSettings | 图标设置（gap 间距、iconColor 图标颜色、iconPositionMap 图标位置、position 布局位置） |
| title | 组件标题的文字样式 |
| card | 卡片背景和边框样式（border 边框颜色、padding 内边距、cardBackgroundColor 背景色） |
| screenPosition | 组件在画布上的位置和大小 |

### 批量复制/更新样式

如果大屏中多个指标卡样式不统一，可以使用 `update_screen.py` 的样式复制功能：

```bash
# 1. 先查看大屏所有组件，找出要复制的样式和要更新的组件
python3 scripts/update_screen.py --screen-id 3654939432 --show-info

# 2. 假设"收入合同金额"指标卡样式是正确的
#    UUID: grid-type:metric-uuid:1773967404738

# 3. 将该样式复制到其他所有指标卡
python3 scripts/update_screen.py \
  --screen-id 3654939432 \
  --clone-style-from "grid-type:metric-uuid:1773967404738" \
  --clone-style-to "grid-type:metric-uuid:1773967415673" \
                   "grid-type:metric-uuid:1773967417343" \
                   "grid-type:metric-uuid:1773967421429" \
                   "grid-type:metric-uuid:1773967418709" \
                   "grid-type:metric-uuid:1773967420268"
```

**原理说明**：
- `--clone-style-from` 指定样式来源组件
- `--clone-style-to` 指定要应用该样式的目标组件列表
- 目标组件的原有位置/尺寸 (`screenPosition`) 会被保留
- 只更新 `styleJson` 中的其他样式字段

## 参考资源

- [SKILL.md](../../SKILL.md) - 技能主文档
- [add_component.py](./add_component.py) - 组件添加脚本
- [TEXT_COMPONENT_GUIDE.md](./TEXT_COMPONENT_GUIDE.md) - 文本组件指南
- [RANKING_COMPONENT_GUIDE.md](./RANKING_COMPONENT_GUIDE.md) - 排名图组件指南
- [CLASSIC_LAYOUT_TEMPLATE.md](../layouts/CLASSIC_LAYOUT_TEMPLATE.md) - 经典布局模板
