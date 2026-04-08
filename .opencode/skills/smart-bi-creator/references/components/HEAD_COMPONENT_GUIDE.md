# 头部组件使用指南

## 概述

头部组件（Head Component）用于大屏顶部的通栏装饰，通常作为大屏的标题栏区域，适合：
- 大屏主标题背景
- 顶部通栏装饰
- 企业/系统名称展示区
- 时间日期显示区背景

## 组件特点

### 1. 通栏布局
- 宽度：1920（占满整个画布）
- 高度：80（标准标题栏高度）
- 位置：top=0（画布顶部）

### 2. 装饰性组件
- 无需数据源配置
- 使用 PNG 图片作为装饰
- 通常配合文本组件使用

### 3. 多种样式
- 使用 `headDecorate` 系列的 PNG 图片
- 有多种样式可选（headDecorate1.png 到 headDecorateN.png）
- 默认使用 headDecorate4.png

## 使用方法

### 基础示例

```bash
# 添加头部组件（大屏顶部通栏装饰，默认 4 号样式）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type head \
  --top 0 --left 0 \
  --width 1920 --height 80 \
  --view-name "头部 1"

# 添加头部组件（使用 7 号样式）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type head \
  --top 0 --left 0 \
  --width 1920 --height 80 \
  --decorate-index 7 \
  --view-name "头部 1"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654239893 |
| --model-id | 是 | 数据模型 ID | 2597080602 |
| --dimension-field | 是 | 维度字段 | projectNo |
| --indicator-field | 是 | 指标字段 | receivingAmount |
| --chart-type | 是 | 图表类型，固定为 `head` | head |
| --top | 是 | Y 坐标，通常为 0 | 0 |
| --left | 是 | X 坐标，通常为 0 | 0 |
| --width | 是 | 组件宽度，通常 1920 | 1920 |
| --height | 是 | 组件高度，通常 80 | 80 |
| --view-name | 否 | 视图名称 | "头部 1" |
| --decorate-index | 否 | 装饰图片编号（1-14），默认 4 | 7 |

### 标准尺寸

| 属性 | 推荐值 | 说明 |
|------|-------|------|
| 宽度 | 1920 | 占满整个画布 |
| 高度 | 80 | 标准标题栏高度 |
| top | 0 | 画布顶部 |
| left | 0 | 画布左侧 |

## 样式配置

### 完整样式结构

```json
{
  "styleJson": {
    "decorate": {},
    "screenPosition": {
      "position": {
        "w": 1920,
        "x": 0,
        "h": 80,
        "y": 0
      }
    },
    "decorateStyle": {
      "selectedDecorate": "headDecorate/headDecorate4.png"
    }
  },
  "templateId": "grid-type:head-uuid:1740994773823948238",
  "viewName": "头部 1"
}
```

### 关键样式说明

#### 1. 装饰样式选择
```json
"decorateStyle": {
  "selectedDecorate": "headDecorate/headDecorate4.png"
}
```
- 格式：`headDecorate/headDecorate{编号}.png`
- 编号范围：1-14
- 默认使用 4 号样式
- 如果觉得不好看，可以换成其他编号试试

#### 2. 屏幕位置
```json
"screenPosition": {
  "position": {
    "w": 1920,
    "x": 0,
    "h": 80,
    "y": 0
  }
}
```
- 通栏布局：宽度 1920
- 顶部对齐：top=0, left=0

## 实战案例

### 案例 1：标准大屏头部

```bash
# 添加头部装饰
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type head \
  --top 0 --left 0 \
  --width 1920 --height 80 \
  --view-name "头部 1" && \

# 添加大屏标题（叠加在头部装饰上）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type text \
  --top 10 --left 780 \
  --width 385 --height 60 \
  --view-name "项目管理智慧大屏"
```

**层次结构**：
```
画布顶部 (top: 0)
  ├─ [头部装饰] (top: 0, height: 80)  ← 背景层
  └─ [文本题目] (top: 10, height: 60)  ← 叠加在上方
```

### 案例 2：头部 + 时间组件

```bash
# 添加头部装饰
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type head \
  --top 0 --left 0 \
  --width 1920 --height 80 \
  --view-name "头部 1" && \

# 添加大屏标题（左侧）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type text \
  --top 15 --left 50 \
  --width 400 --height 50 \
  --view-name "公司经营分析大屏" && \

# 添加时间组件（右侧，需要手动配置时间组件）
# 时间组件需要特殊的样式配置
```

**布局效果**：
```
+--------------------------------------------------+
| [头部装饰背景 - 通栏]                            |
|  标题：公司经营分析大屏              [时间显示]  |
+--------------------------------------------------+
```

### 案例 3：头部 + 走马灯

```bash
# 添加头部装饰
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type head \
  --top 0 --left 0 \
  --width 1920 --height 80 \
  --view-name "头部 1" && \

# 添加走马灯（滚动消息）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field noticeTitle \
  --indicator-field noticeId \
  --chart-type marquee \
  --top 20 --left 600 \
  --width 700 --height 40 \
  --view-name "重要通知"
```

**层次结构**：
```
+--------------------------------------------------+
| [头部装饰]                                        |
|           [走马灯：滚动显示重要通知]              |
+--------------------------------------------------+
```

## 样式定制

### 切换头部样式

头部组件使用图片文件，切换样式有两种方式：

**方式一：使用 --decorate-index 参数直接修改**

```bash
# 查看大屏信息获取头部组件 UUID
python3 scripts/update_screen.py --screen-id 3654239893 --show-info

# 修改为 7 号样式
python3 scripts/update_screen.py --screen-id 3654239893 --uuid "grid-type:head-uuid:xxx" --decorate-index 7
```

**方式二：手动修改样式文件**

1. 查看当前配置：
```bash
python3 scripts/update_screen.py --screen-id 3654239893 --show-info
```

2. 记录头部组件的 UUID

3. 手动修改 `decorateStyle.selectedDecorate` 字段

**可用样式**：1-14 号可选
- `headDecorate/headDecorate1.png` 到 `headDecorate/headDecorate14.png`
- 默认使用 `headDecorate4.png`
- 如果觉得不好看，可以换成其他编号

### 自定义高度

标准高度为 80px，如需调整：

```bash
# 较高的头部（100px）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --chart-type head \
  --top 0 --left 0 \
  --width 1920 --height 100
```

**注意**：图片可能会拉伸，建议配合合适的样式。

## 与其他组件配合

### 典型组合

#### 1. 头部 + 文本题目
```bash
# 头部背景
--chart-type head, top: 0, height: 80

# 标题文字（叠加）
--chart-type text, top: 10-15, height: 50-60
```

**层次**：
```
+--------------------------------------------------+
| [头部装饰] (背景层)                               |
|  [文本题目] (前景层，居中或居左)                   |
+--------------------------------------------------+
```

#### 2. 头部 + 走马灯
```bash
# 头部背景
--chart-type head, top: 0

# 走马灯（居中显示）
--chart-type marquee, top: 20, left: 600
```

#### 3. 头部 + 时间组件
```bash
# 头部背景
--chart-type head, top: 0

# 时间（右上角）
--chart-type time, top: 20, left: 1700
```

### 完整头部布局示例

```
画布：1920×1080

+--------------------------------------------------+  ← top: 0
| [头部装饰 - headDecorate4（可换1-14号）]        |
|                                                  |
|  [标题文本]              [时间显示] [走马灯]      |  ← top: 15-25
|                                                  |
+--------------------------------------------------+  ← top: 80
|                                                  |
|  [指标卡区域] top: 100                           |
|                                                  |
```

**组件添加顺序**：
```bash
# 1. 头部装饰（最底层）
python3 scripts/add_component.py --chart-type head ...

# 2. 文本题目（叠加）
python3 scripts/add_component.py --chart-type text ...

# 3. 时间组件（叠加）
# 需要手动配置时间组件样式

# 4. 走马灯（叠加）
python3 scripts/add_component.py --chart-type marquee ...
```

## 注意事项

### 1. 层级关系
- 头部组件通常在最底层（top=0）
- 文本/时间/走马灯组件叠加在上方
- 注意调整 top 坐标实现叠加效果

### 2. 尺寸标准
- 宽度固定 1920（占满画布）
- 高度通常 80（可调整）
- 不要设置过窄的宽度

### 3. 样式选择
- 编号范围 1-14，默认 4 号
- 可根据主题颜色选择不同样式
- 如果默认样式不好看，可以换成其他编号试试
- 确保与整体风格协调

### 4. 文字可读性
- 标题文字颜色要与头部背景对比
- 深色头部使用白色文字
- 浅色头部使用深色文字

## 常见问题

### Q1: 头部组件看不到？
- 检查 top 坐标是否为 0
- 检查是否被其他组件遮挡
- 检查 `selectedDecorate` 文件路径是否正确

### Q2: 如何切换头部样式？
- 修改 `decorateStyle.selectedDecorate` 字段
- 使用不同的文件名（如 `headDecorate2.png`）

### Q3: 文字与头部不协调？
- 调整文本组件的 top 坐标
- 确保文字在头部区域内
- 调整文字颜色增强对比

### Q4: 头部高度多少合适？
- 标准高度：80px
- 较高头部：100-120px
- 根据标题文字大小调整

## 头部组件 vs 装饰组件

| 特性 | 头部组件 | 装饰组件 |
|------|---------|---------|
| 用途 | 大屏顶部通栏 | 各种位置装饰 |
| 宽度 | 固定 1920 | 根据位置调整 |
| 高度 | 通常 80 | 根据类型不同 |
| 位置 | 固定 top=0 | 灵活设置 |
| 样式 | headDecorate 1-14号可选 | bar/square/base 系列 |
| 数量 | 通常 1 个 | 可多个 |

## 参考资源

- [SKILL.md](../../SKILL.md) - 技能主文档
- [add_component.py](./add_component.py) - 组件添加脚本
- [TEXT_COMPONENT_GUIDE.md](./TEXT_COMPONENT_GUIDE.md) - 文本组件指南
- [DECORATE_COMPONENT_GUIDE.md](./DECORATE_COMPONENT_GUIDE.md) - 装饰组件指南
