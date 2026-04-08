# 文本组件使用指南

## 概述

文本组件（Text Component）用于在大屏中添加标题、标签、说明文字等静态文本内容，适合：
- 大屏主标题
- 区域小标题
- 图表标签
- 装饰性文字
- 说明性文本

## 组件特点

### 1. 简单易用
- 无需数据源配置
- 直接设置文本内容
- 无需维度和指标

### 2. 样式灵活
- 支持字体大小调整
- 支持粗体/斜体
- 支持文字对齐（左/中/右）
- 支持颜色自定义

### 3. 透明背景
- 默认无边框
- 默认无背景色
- 易于与其他组件叠加

## 使用方法

### 基础示例

```bash
# 添加文本组件（作为区域标题）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type text \
  --top 330 --left 60 \
  --width 180 --height 35 \
  --view-name "收入合同"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654239893 |
| --model-id | 是 | 数据模型 ID（文本组件实际不需要，但脚本要求） | 2597080602 |
| --dimension-field | 是 | 维度字段（文本组件不需要） | projectNo |
| --indicator-field | 是 | 指标字段（文本组件不需要） | receivingAmount |
| --chart-type | 是 | 图表类型，固定为 `text` | text |
| --top | 是 | Y 坐标 | 330 |
| --left | 是 | X 坐标 | 60 |
| --width | 是 | 组件宽度 | 180 |
| --height | 是 | 组件高度 | 35 |
| --view-name | 是 | **显示的文本内容** | "收入合同" |
| --align | 否 | 文本对齐方式 | left / center / right |
| --font-size | 否 | 字体大小（像素） | 24 |

### 尺寸建议

| 场景 | 推荐宽度 | 推荐高度 | 字体大小 |
|------|---------|---------|---------|
| 大屏主标题 | 380-400 | 60-70 | 36-40 |
| 区域小标题 | 170-200 | 34-36 | 22-24 |
| 图表标签 | 150-180 | 30-35 | 20-22 |
| 说明文字 | 200-300 | 40-60 | 16-18 |

### 对齐方式

文本对齐通过 `align` 参数控制：
- `left`: 左对齐（默认）
- `center`: 居中对齐
- `right`: 右对齐

**使用示例**：
```bash
# 居中对齐的大标题
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type text \
  --top 6 --left 560 \
  --width 800 --height 60 \
  --view-name "企业经营分析大屏" \
  --align center \
  --font-size 36
```

## 样式配置

### 完整样式结构

```json
{
  "screenPosition": {
    "position": {"x": 60, "y": 330, "w": 180, "h": 35}
  },
  "textData": {
    "content": []
  },
  "title": {
    "isExtra": true,
    "textSetMap": {
      "textItalic": false,
      "textBold": true,
      "fontSize": 22,
      "align": "left",
      "textColor": "#FEFEFE"
    },
    "title": "收入合同"
  },
  "card": {
    "border": "transparent",
    "padding": 4,
    "lineWidthMap": {
      "width": 1,
      "style": "solid"
    },
    "isExtra": true,
    "show": false
  },
  "content": {
    "textSetMap": {
      "textItalic": false,
      "textBold": true,
      "fontSize": "24",
      "align": "left",
      "textColor": "#FEFEFE"
    },
    "textContent": "收入合同"
  }
}
```

### 关键样式说明

#### 1. 文字内容
```json
"content": {
  "textSetMap": {
    "textItalic": false,
    "textBold": true,
    "fontSize": "24",
    "align": "left",
    "textColor": "#FEFEFE"
  },
  "textContent": "收入合同"
}
```
- `textContent`: 实际显示的文字
- `fontSize`: 字体大小（字符串格式，如 "24"）
- `align`: 对齐方式（left/center/right）
- `textColor`: 文字颜色
- `textBold`: 是否粗体
- `textItalic`: 是否斜体

#### 2. 标题配置
```json
"title": {
  "isExtra": true,
  "textSetMap": {
    "textBold": true,
    "fontSize": 22,
    "align": "left",
    "textColor": "#FEFEFE"
  },
  "title": "收入合同"
}
```
- 与 `content` 类似，但用于标题
- 字体大小通常略小（数字格式，如 22）

#### 3. 卡片背景
```json
"card": {
  "border": "transparent",
  "padding": 4,
  "isExtra": true,
  "show": false
}
```
- `show: false`: 不显示背景
- `border: "transparent"`: 透明边框
- 文本组件通常使用透明背景

## 实战案例

### 案例 1：大屏主标题

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type text \
  --top 6 --left 780 \
  --width 385 --height 60 \
  --view-name "项目管理智慧大屏"
```

**说明**：
- 居中显示的大标题
- 宽度 385，高度 60
- 字体大小 38（需手动调整样式）

### 案例 2：区域小标题组合

```bash
# 左侧区域标题
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type text \
  --top 78 --left 62 \
  --width 176 --height 35 \
  --view-name "收入合同" && \

# 中间区域标题
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type text \
  --top 78 --left 480 \
  --width 176 --height 35 \
  --view-name "付款申请" && \

# 右侧区域标题
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type text \
  --top 78 --left 834 \
  --width 176 --height 35 \
  --view-name "开票记录"
```

**说明**：
- 多个文本组件水平排列
- 相同的宽度和高度
- 统一的样式风格

### 案例 3：配合图表使用

```bash
# 先添加标题
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type text \
  --top 330 --left 60 \
  --width 180 --height 35 \
  --view-name "月度收款趋势" && \

# 再添加图表
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type line \
  --top 370 --left 60 \
  --width 450 --height 300 \
  --view-name "收款趋势图"
```

**说明**：
- 标题在图表上方
- 标题宽度略小于图表
- 形成视觉层次

## 样式定制

### 修改文字颜色

文本组件默认使用白色文字（#FEFEFE），如需修改颜色：

1. 使用 `update_screen.py` 查看组件：
```bash
python3 scripts/update_screen.py --screen-id 3654239893 --show-info
```

2. 记录文本组件的 UUID

3. 手动编辑样式（需要修改脚本或 API 调用）

### 修改字体大小和对齐方式

创建文本组件时直接指定：

```bash
# 创建居中大标题
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type text \
  --top 6 --left 560 \
  --width 800 --height 60 \
  --view-name "主标题" \
  --align center \
  --font-size 36
```

**参数说明**：
- `--align`: 文本对齐方式，可选 `left`、`center`、`right`
- `--font-size`: 字体大小（像素），建议主标题 36-40，区域标题 22-24

## 注意事项

### 1. 必需参数
- 文本组件实际上不需要数据源
- 但脚本仍要求传入 `model-id`、`dimension-field`、`indicator-field`
- 这些参数对文本组件没有实际作用

### 2. 文字内容
- `--view-name` 参数决定显示的文字
- 支持换行符 `\n`（如 "第一行\n第二行"）
- 建议保持简洁明了

### 3. 尺寸设置
- 宽度要足够容纳文字
- 高度根据字体大小调整
- 主标题需要更大的高度

### 4. 颜色对比
- 默认白色文字适合深色背景
- 如背景较浅，需调整文字颜色
- 确保足够的对比度

## 与其他组件配合

### 典型布局

```
+----------------------------------+
|        [主标题 - 文本]            |  ← top: 6, height: 60
+----------------------------------+
|                                  |
| [小标题]  [图表 1]  [小标题] [图表 2] |  ← 标题在上，图表在下
|                                  |
+----------------------------------+
| [小标题]  [图表 3]                 |
+----------------------------------+
```

### 间距建议

- 标题与图表间距：5-10px
- 多个标题间距：根据布局决定
- 标题与画布边缘：至少 10px

## 常见问题

### Q1: 文本组件需要数据源吗？
- 不需要。文本组件是静态的
- 但脚本要求传入参数，可随意填写

### Q2: 如何修改已添加的文本？
使用 `rename_component.py`：
```bash
python3 scripts/rename_component.py \
  --screen-id 3654239893 \
  --uuid "grid-type:text-uuid:xxx" \
  --title "新标题"
```

### Q3: 文字显示不全？
- 增加组件宽度
- 减小字体大小
- 检查是否超出画布边界

### Q4: 如何添加多行文本？
在 `--view-name` 中使用换行符：
```bash
--view-name "第一行内容\n第二行内容"
```

## 参考资源

- [SKILL.md](../../SKILL.md) - 技能主文档
- [add_component.py](./add_component.py) - 组件添加脚本
- [RANKING_COMPONENT_GUIDE.md](./RANKING_COMPONENT_GUIDE.md) - 排名图组件指南
- [HORIZONTAL_BAR_COMPONENT_GUIDE.md](./HORIZONTAL_BAR_COMPONENT_GUIDE.md) - 条形图组件指南
