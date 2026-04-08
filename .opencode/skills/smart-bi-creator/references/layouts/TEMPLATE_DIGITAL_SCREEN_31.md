# 数字大屏模版31 - 完整布局模板

## 概述

本模板来源于实际生产环境中的"数字大屏模版31"（精工装管理驾驶舱），采用深色科技主题，适合企业级数据展示大屏。

**画布尺寸**: 1920 x 1080
**主题**: lgScreenTechnology (深色科技风)
**组件总数**: 42 个图层，33 个数据组件
**大屏 ID**: 3654572744
**预览地址**: https://dev.cloud.hecom.cn/largescreenpreview?id=3654572744

## 配色方案

```json
{
  "theme": "lgScreenTechnology",
  "colorSystem": "dark",
  "cardBackgroundColor": "rgba(5,38,82,0.60)",
  "titleColor": "#FEFEFE",
  "textColor": "#A6ADD0",
  "lineColor": "#313358",
  "linkColor": "#177DDC",
  "panelBackgroundColor": "#020430",
  "cardBorderRadius": 6
}
```

## 视觉布局图

```
┌──────────────────────────────────────────────────────────────────────────────────┐ top=0
│ [头部装饰 - 1920×80, headDecorate/headDecorate3.png]                              │ h=80
├──────────────────────────────────────────────────────────────────────────────────┤
│                              [主标题 - 居中白色40px粗体]                          │ top=20
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────┐                              ┌─────────────┐                  │
│  │ 卡片1       │                              │ 卡片1       │                  │
│  │ 412×320     │                              │ 412×320     │                  │
│  │ ┌─────────┐ │                              │ ┌─────────┐ │                  │ top=80
│  │ │水平条形图│ │                              │ │ 排名图  │ │                  │
│  │ │411×319  │ │                              │ │411×319  │ │                  │
│  │ └─────────┘ │                              │ └─────────┘ │                  │
│  └─────────────┘                              └─────────────┘                  │
│                                                                                  │
│  ┌──────┬────────┬──────┬───┬────────┬──────┬───┬────────┬──────┬───┬────────┐ │
│  │装饰231│指标卡  │装饰  │图标│指标卡  │装饰  │图标│指标卡  │装饰  │图标│指标卡  │ │ top=98
│  │ ×80  │150×80 │231×80│79 │150×80 │231×80│78 │150×80 │231×80│79 │150×80 │ │ h=80
│  └──────┴────────┴──────┴───┴────────┴──────┴───┴────────┴──────┴───┴────────┘ │
│    472      551      720   722    801      968   969   1048    1217  1218  1296   │
│←─────────────────────────────────────────────────────────────────────────────→   │
│                        ┌───────────────────────────────┐                         │
│                        │                               │                         │
│                        │           地图组件            │                         │
│                        │        1030 × 542            │                         │ top=198
│                        │       (视觉焦点 - 居中)       │                         │ h=542
│                        │                               │                         │
│                        └───────────────────────────────┘                         │
│                               left=445, top=198                                  │
│                                                                                  │
├──────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐                              ┌─────────────┐                    │
│  │ 卡片1       │                              │ 卡片1       │                    │
│  │ 412×326     │                              │ 412×326     │                    │
│  │ ┌─────────┐ │                              │ ┌─────────┐ │                    │ top=412
│  │ │  饼图   │ │                              │ │ 漏斗图  │ │                  │ h=326
│  │ │410×325  │ │                              │ │410×326  │ │                  │
│  │ └─────────┘ │                              │ └─────────┘ │                  │
│  └─────────────┘                              └─────────────┘                    │
│   15,412                    ←中间基础装饰 739,611 455×124→                        │
│                                                                                  │
│  ┌─────────────┐                        ┌─────────────────────────┐              │
│  │  仪表盘     │                        │       折线图            │              │
│  │  411×319   │                        │      1030×319           │              │ top=753
│  └─────────────┘                        └─────────────────────────┘              │
│   17,753                                                                  445,753│
│                                                                                  │
├──────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐                        ┌─────────────────────────┐  ┌─────────┐ │
│  │  卡片1      │                        │       卡片1              │  │ 卡片1   │ │
│  │  412×320   │                        │      1032×320            │  │ 412×320 │ │ top=752
│  │  ┌───────┐ │                        │  ┌───────────────────┐  │  │┌───────┐│ │ h=320
│  │  │ 柱图  │ │                        │  │                   │  │  ││ 柱图  ││ │
│  │  │412×319│ │                        │  │                   │  │  ││412×319││ │
│  │  └───────┘ │                        │  └───────────────────┘  │  │└───────┘│ │
│  └─────────────┘                        └─────────────────────────┘  └─────────┘ │
│   15,752                               444,752                         1492,752│
└──────────────────────────────────────────────────────────────────────────────────┘ top=1072
```

## 完整组件坐标表（按 Y 坐标排序）

| Top | Left | Width | Height | Type | Title | 样式/备注 |
|-----|------|-------|--------|------|-------|----------|
| -1 | 724 | 455 | 70 | text | - | 装饰性文本(覆盖装饰条) |
| 0 | 0 | 1920 | 80 | head | 头部1 | headDecorate/headDecorate3.png |
| 20 | 768 | 371 | 43 | text | 项目管理智慧大屏 | fontSize=28, #FEFEFE, bold |
| 80 | 15 | 412 | 320 | card | 卡片1 | 左侧容器 |
| 80 | 16 | 411 | 319 | horizontalBar | 项目成本情况统计 | 水平条形图 |
| 80 | 1492 | 412 | 320 | card | 卡片1 | 右侧容器 |
| 80 | 1492 | 411 | 319 | ranking | 排名1 | 排名图 |
| 98 | 472 | 231 | 80 | decorate | 其他1 | squareDecorate/squareDecorate1.png |
| 98 | 551 | 150 | 80 | metric | 指标卡1 | 数值色:rgb(131,246,255) |
| 98 | 720 | 231 | 80 | decorate | 其他1 | squareDecorate/squareDecorate1.png |
| 98 | 722 | 79 | 78 | icon | 图标5 | 叠加在装饰上方 |
| 98 | 801 | 150 | 80 | metric | 指标卡1 | 数值色:rgb(131,246,255) |
| 98 | 968 | 231 | 80 | decorate | 其他1 | squareDecorate/squareDecorate1.png |
| 98 | 969 | 79 | 78 | icon | 图标5 | 叠加在装饰上方 |
| 98 | 1048 | 150 | 80 | metric | 指标卡1 | 数值色:rgb(131,246,255) |
| 98 | 1217 | 231 | 80 | decorate | 其他1 | squareDecorate/squareDecorate1.png |
| 98 | 1218 | 79 | 78 | icon | 图标5 | 叠加在装饰上方 |
| 98 | 1296 | 150 | 80 | metric | 指标卡1 | 数值色:rgb(131,246,255) |
| 99 | 473 | 79 | 78 | icon | 图标5 | 多出的图标 |
| 198 | 445 | 1030 | 542 | map | 地图1 | 视觉焦点 |
| 264 | 781 | 223 | 115 | - | - | 装饰性组件 |
| 311 | 572 | 273 | 42 | - | - | 装饰性组件 |
| 389 | 805 | 391 | 275 | - | - | 装饰性组件 |
| 412 | 15 | 412 | 326 | card | 卡片1 | 左侧容器 |
| 412 | 16 | 410 | 325 | pie | 项目成本情况统计 | 饼图 |
| 412 | 1492 | 412 | 326 | card | 卡片1 | 右侧容器 |
| 412 | 1493 | 410 | 326 | funnel | 漏斗图1 | 漏斗图 |
| 596 | 149 | 151 | 25 | text | 累计完工金额(元) | fontSize=12, #FEFEFE, bold |
| 611 | 739 | 455 | 124 | decorate | 其他5 | baseDecorate/baseDecorate1.png |
| 752 | 15 | 412 | 320 | card | 卡片1 | 左下容器 |
| 752 | 444 | 1032 | 320 | card | 卡片1 | 底部大容器 |
| 752 | 1492 | 412 | 320 | card | 卡片1 | 右下容器 |
| 752 | 1492 | 412 | 319 | bar | 柱图1 | 柱图 |
| 753 | 17 | 411 | 319 | gauge | 仪表盘1 | 仪表盘 |
| 753 | 445 | 1030 | 319 | line | 线图1 | 折线图 |

## 顶部指标区详细布局（top=98）

### 布局示意

```
left:   472     551     720     722     801     968     969    1048    1217    1218    1296
         ↓       ↓       ↓       ↓       ↓       ↓       ↓       ↓       ↓       ↓       ↓
       ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
       │装饰 │ │指标卡│ │装饰 │ │图标 │ │指标卡│ │装饰 │ │图标 │ │指标卡│ │装饰 │ │图标 │ │指标卡│
       │231× │ │150× │ │231× │ │79×  │ │150× │ │231× │ │78×  │ │150× │ │231× │ │79×  │ │150× │
       │ 80  │ │ 80  │ │ 80  │ │ 78  │ │ 80  │ │ 80  │ │ 78  │ │ 80  │ │ 80  │ │ 78  │ │ 80  │
       └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘
```

### 组件间距计算

| 关系 | 计算 | 值 |
|------|------|-----|
| 装饰宽度 | - | 231 |
| 指标卡宽度 | - | 150 |
| 图标宽度 | - | 79 |
| 装饰-指标卡间距 | (231-150)/2 | 40.5 |
| 装饰-图标间距 | 231-79 | 152（图标在装饰范围内居中）|
| 相邻组合间距 | 968-801-150 | 17 |

## 组件尺寸速查表

| 组件类型 | 宽度 | 高度 | 数量 | 不可调 | 样式文件 |
|---------|------|------|------|--------|----------|
| 头部装饰 (head) | 1920 | 80 | 1 | - | headDecorate/headDecorate3.png |
| 标准卡片 (card) | 412 | 320/326 | 7 | - | - |
| 大卡片 (card) | 1032 | 320 | 1 | - | - |
| 指标卡 (metric) | 150 | 80 | 4 | - | 数值色:rgb(131,246,255) |
| 方形装饰 (decorate) | 231 | 80 | 4 | **是** | squareDecorate/squareDecorate1.png |
| 基础装饰 (decorate) | 455 | 124 | 1 | **是** | baseDecorate/baseDecorate1.png |
| 图标 (icon) | 79 | 78 | 5 | - | - |
| 水平条形图 | 411 | 319 | 1 | - | - |
| 排名图 (ranking) | 411 | 319 | 1 | - | - |
| 地图 (map) | 1030 | 542 | 1 | - | 视觉焦点 |
| 饼图 (pie) | 410 | 325 | 1 | - | - |
| 漏斗图 (funnel) | 410 | 326 | 1 | - | - |
| 仪表盘 (gauge) | 411 | 319 | 1 | - | - |
| 折线图 (line) | 1030 | 319 | 1 | - | - |
| 柱图 (bar) | 412 | 319 | 1 | - | - |
| 文本 (text) | 371/151 | 43/25 | 2 | - | fontSize:40/28/12 |

## 装饰组件使用规范

### ⚠️ 重要限制

**装饰组件不能改变大小！必须使用原始尺寸！**

| 装饰类型 | 宽度 | 高度 | 样式文件 | view-name 参数 |
|---------|------|------|----------|----------------|
| 方形装饰 (square) | 231 | 80 | squareDecorate/squareDecorate1.png | "其他1" |
| 基础装饰 (base) | 455 | 124 | baseDecorate/baseDecorate1.png | "其他5" |
| 头部装饰 (head) | 1920 | 80 | headDecorate/headDecorate3.png | "头部1" |

### 装饰组件添加示例

```bash
# 方形装饰（顶部指标区用）
python3 scripts/add_component.py \
  --screen-id <ID> \
  --model-id 2592797039 \
  --dimension-field field16 \
  --indicator-field field3 \
  --chart-type decorate \
  --top 98 --left 472 \
  --width 231 --height 80 \
  --view-name "其他1"

# 基础装饰（中间装饰用）
python3 scripts/add_component.py \
  --screen-id <ID> \
  --model-id 2592797039 \
  --dimension-field field16 \
  --indicator-field field3 \
  --chart-type decorate \
  --top 611 --left 739 \
  --width 455 --height 124 \
  --view-name "其他5"

# 头部装饰
python3 scripts/add_component.py \
  --screen-id <ID> \
  --model-id 2592797039 \
  --dimension-field field16 \
  --indicator-field field3 \
  --chart-type head \
  --top 0 --left 0 \
  --width 1920 --height 80 \
  --view-name "头部1"
```

## 指标卡样式

### 样式配置

```json
{
  "card": {
    "cardBackgroundColor": "rgba(5,38,82,0.60)"
  },
  "metricValue": {
    "textSetMap": {
      "textColor": "rgb(131,246,255)"
    },
    "prefixFontSize": 24
  }
}
```

### 添加指标卡示例

```bash
python3 scripts/add_component.py \
  --screen-id <ID> \
  --model-id 2592797039 \
  --dimension-field field16 \
  --indicator-field field3 \
  --chart-type metric \
  --top 98 --left 551 \
  --width 150 --height 80 \
  --view-name "指标卡1"
```

## 文本组件样式

| 用途 | Top | Left | Width | Height | fontSize | color | bold | align |
|------|-----|------|-------|--------|----------|-------|------|-------|
| 主标题 | 20 | 768 | 371 | 43 | 28 | #FEFEFE | true | - |
| 累计完工金额标签 | 596 | 149 | 151 | 25 | 12 | #FEFEFE | true | - |

### 添加文本组件示例

```bash
# 主标题
python3 scripts/add_component.py \
  --screen-id <ID> \
  --model-id 2592797039 \
  --dimension-field field16 \
  --indicator-field field3 \
  --chart-type text \
  --top 20 --left 768 \
  --width 371 --height 43 \
  --view-name "项目管理智慧大屏"

# 图表标签
python3 scripts/add_component.py \
  --screen-id <ID> \
  --model-id 2592797039 \
  --dimension-field field16 \
  --indicator-field field3 \
  --chart-type text \
  --top 596 --left 149 \
  --width 151 --height 25 \
  --view-name "累计完工金额(元)"
```

## 完整创建命令序列

### 基础设置

```bash
# 大屏 ID
SCREEN_ID=3654572744
MODEL_ID=2592797039
DIM_FIELD=field27__province
IND_FIELD=field3
```

### 步骤 1: 创建基础大屏（地图）

```bash
python3 scripts/create_screen.py create \
  --name "数字大屏模版31" \
  --model-id $MODEL_ID \
  --dimension-field $DIM_FIELD \
  --indicator-field $IND_FIELD \
  --chart-type map \
  --width 1030 --height 542
```

### 步骤 2: 添加头部装饰

```bash
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID \
  --model-id $MODEL_ID \
  --dimension-field field16 \
  --indicator-field $IND_FIELD \
  --chart-type head \
  --top 0 --left 0 \
  --width 1920 --height 80 \
  --view-name "头部1"
```

### 步骤 3: 添加主标题

```bash
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID \
  --model-id $MODEL_ID \
  --dimension-field field16 \
  --indicator-field $IND_FIELD \
  --chart-type text \
  --top 20 --left 768 \
  --width 371 --height 43 \
  --view-name "项目管理智慧大屏"
```

### 步骤 4: 添加左侧卡片和水平条形图

```bash
# 卡片容器
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID \
  --model-id $MODEL_ID \
  --dimension-field field16 \
  --indicator-field $IND_FIELD \
  --chart-type card \
  --top 80 --left 15 \
  --width 412 --height 320 \
  --view-name "卡片1"

# 水平条形图
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID \
  --model-id $MODEL_ID \
  --dimension-field field16 \
  --indicator-field $IND_FIELD \
  --chart-type horizontalBar \
  --top 80 --left 16 \
  --width 411 --height 319 \
  --view-name "项目成本情况统计"
```

### 步骤 5: 添加右侧卡片和排名图

```bash
# 卡片容器
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID \
  --model-id $MODEL_ID \
  --dimension-field field16 \
  --indicator-field $IND_FIELD \
  --chart-type card \
  --top 80 --left 1492 \
  --width 412 --height 320 \
  --view-name "卡片1"

# 排名图
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID \
  --model-id $MODEL_ID \
  --dimension-field field16 \
  --indicator-field $IND_FIELD \
  --chart-type ranking \
  --top 80 --left 1492 \
  --width 411 --height 319 \
  --view-name "排名1"
```

### 步骤 6: 添加顶部指标卡组（4组装饰+图标+指标卡）

```bash
# ===== 第1组 =====
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type decorate --top 98 --left 472 --width 231 --height 80 --view-name "其他1" && \
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type metric --top 98 --left 551 --width 150 --height 80 --view-name "指标卡1"

# ===== 第2组 =====
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type decorate --top 98 --left 720 --width 231 --height 80 --view-name "其他1" && \
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type icon --top 98 --left 722 --width 79 --height 78 --view-name "图标5" && \
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type metric --top 98 --left 801 --width 150 --height 80 --view-name "指标卡1"

# ===== 第3组 =====
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type decorate --top 98 --left 968 --width 231 --height 80 --view-name "其他1" && \
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type icon --top 98 --left 969 --width 79 --height 78 --view-name "图标5" && \
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type metric --top 98 --left 1048 --width 150 --height 80 --view-name "指标卡1"

# ===== 第4组 =====
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type decorate --top 98 --left 1217 --width 231 --height 80 --view-name "其他1" && \
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type icon --top 98 --left 1218 --width 79 --height 78 --view-name "图标5" && \
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type metric --top 98 --left 1296 --width 150 --height 80 --view-name "指标卡1"
```

### 步骤 7: 添加左侧饼图区域

```bash
# 卡片容器
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type card --top 412 --left 15 --width 412 --height 326 --view-name "卡片1"

# 饼图
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type pie --top 412 --left 16 --width 410 --height 325 --view-name "项目成本情况统计"

# 饼图标签
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type text --top 596 --left 149 --width 151 --height 25 --view-name "累计完工金额(元)"

# 基础装饰
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type decorate --top 611 --left 739 --width 455 --height 124 --view-name "其他5"
```

### 步骤 8: 添加右侧漏斗图区域

```bash
# 卡片容器
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type card --top 412 --left 1492 --width 412 --height 326 --view-name "卡片1"

# 漏斗图
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type funnel --top 412 --left 1493 --width 410 --height 326 --view-name "漏斗图1"
```

### 步骤 9: 添加底部区域

```bash
# 左下卡片
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type card --top 752 --left 15 --width 412 --height 320 --view-name "卡片1"

# 仪表盘
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type gauge --top 753 --left 17 --width 411 --height 319 --view-name "仪表盘1"

# 底部大卡片
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type card --top 752 --left 444 --width 1032 --height 320 --view-name "卡片1"

# 折线图
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type line --top 753 --left 445 --width 1030 --height 319 --view-name "线图1"

# 右下卡片
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type card --top 752 --left 1492 --width 412 --height 320 --view-name "卡片1"

# 柱图
python3 scripts/add_component.py \
  --screen-id $SCREEN_ID --model-id $MODEL_ID --dimension-field field16 --indicator-field $IND_FIELD \
  --chart-type bar --top 752 --left 1492 --width 412 --height 319 --view-name "柱图1"
```

## 组件添加顺序（重要）

1. **地图** - 创建基础大屏时指定
2. **头部装饰** - 顶层背景
3. **主标题文本** - 叠加在头部上
4. **左侧卡片+水平条形图** - top=80
5. **右侧卡片+排名图** - top=80
6. **顶部指标卡组** - top=98（装饰→图标→指标卡，串行执行）
7. **左侧饼图区域** - top=412
8. **右侧漏斗图区域** - top=412
9. **底部仪表盘+折线图+柱图** - top=752/753

**⚠️ 重要：所有组件添加必须串行执行，使用 `&&` 连接！**

## 布局规律总结

### 水平间距
- 顶部指标卡组相邻组合间距：17px
- 左侧卡片到中央：430px (445-15)
- 右侧卡片到边缘：16px (1920-1492-412)

### 垂直间距
- 顶部区域到中央地图：100px (198-98)
- 中央地图到底部区域：14px (752-738)
- 底部仪表盘到折线图：0px (同一水平线 top=752/753)

### 卡片与内容间距
- 卡片内边距约 3-5px
- 内容在卡片内居中或靠左上

## 适用场景

- 企业经营分析大屏
- 项目管理驾驶舱
- 地理分布数据展示
- 多维度数据分析看板
- 智慧工厂/车间管理

## 参考资源

- 原始大屏 ID: 3654572744
- 预览地址: https://dev.cloud.hecom.cn/largescreenpreview?id=3654572744
- 模型 ID: 2592797039
- 维度字段: field27__province (省份)
- 指标字段: field3
