# 装饰组件使用指南

## ⚠️ 重要限制（必读）

**装饰组件不能改变大小！必须使用原始尺寸！**

| 装饰类型 | 原始宽度 | 原始高度 | 可否调整 |
|---------|---------|---------|---------|
| 条形装饰 (bar) | 412px | 29px | ❌ 不可调整 |
| 方形装饰 (square) | 242px | 84px | ❌ 不可调整 |
| 基础装饰 (base) | 170px | 110px | ❌ 不可调整 |

**违反后果**：
- PNG 图片被拉伸变形
- 图案模糊失真
- 视觉效果极差

**错误示例**：
```bash
# ❌ 错误：拉伸条形装饰到 900px 宽度
python3 scripts/add_component.py \
  --chart-type decorate \
  --view-name "bar" \
  --width 900 --height 29  # 图片会严重变形！

# ✅ 正确：使用原始尺寸
python3 scripts/add_component.py \
  --chart-type decorate \
  --view-name "bar" \
  --width 412 --height 29  # 原始尺寸
```

**替代方案**：
- 如果需要长标题栏 → 使用多个条形装饰并排，或直接用文本组件
- 如果需要大装饰 → 使用基础装饰 (base)，不要拉伸小装饰

## 概述

装饰组件（Decorate Component）用于美化大屏布局，增强视觉效果，适合：
- 指标卡底部装饰
- 图表标题栏装饰
- 区域分隔装饰
- 角落点缀装饰
- 背景装饰元素

## 组件特点

### 1. 无需数据源
- 不需要配置维度和指标
- 纯装饰性组件
- 脚本仍要求传入模型参数（可忽略）

### 2. 多种类型
根据形状和用途分为三种类型：
- **方形装饰（square）**：适合指标卡下方
- **条形装饰（bar）**：适合图表标题栏
- **基础装饰（base）**：独立装饰元素

### 3. 样式丰富
- 每种类型有多种样式可选
- 使用 PNG 图片格式
- 透明背景，易于融合

## 装饰类型详解

### 1. 方形装饰（squareDecorate）

**特点**：
- 形状：方形或接近方形
- 尺寸：约 242×84
- 用途：指标卡底部装饰

**样式文件**：
- `squareDecorate/squareDecorate1.png`
- `squareDecorate/squareDecorate2.png`
- `squareDecorate/squareDecorate3.png`

**典型布局**：
```
+------------------+
|    指标卡内容     |
+------------------+
| [方形装饰图片]   |  ← 紧贴指标卡下方
+------------------+
```

**使用示例**：
```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type decorate \
  --top 123 --left 451 \
  --width 242 --height 84 \
  --view-name "square:其他 1"
```

### 2. 条形装饰（barDecorate）

**特点**：
- 形状：细长条形
- 尺寸：约 412×29 或 337×29
- 用途：图表标题栏、区域分隔

**样式文件**：
- `barDecorate/barDecorate1.png`
- `barDecorate/barDecorate2.png`
- `barDecorate/barDecorate3.png`

**典型布局**：
```
+------------------+
| [条形装饰图片]   |  ← 作为标题栏
+------------------+
|                  |
|    图表内容      |
|                  |
+------------------+
```

**使用示例**：
```bash
# 图表标题栏装饰
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type decorate \
  --top 92 --left 16 \
  --width 412 --height 29 \
  --view-name "bar:其他 5"
```

### 3. 基础装饰（baseDecorate）

**特点**：
- 形状：不规则或特殊形状
- 尺寸：约 170×110
- 用途：角落点缀、独立装饰

**样式文件**：
- `baseDecorate/baseDecorate1.png`
- `baseDecorate/baseDecorate2.png`
- `baseDecorate/baseDecorate3.png`

**典型布局**：
```
+------------------+
|                  |
|   [基础装饰]     |  ← 角落或空白处
|                  |
+------------------+
```

**使用示例**：
```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type decorate \
  --top 683 --left 39 \
  --width 170 --height 110 \
  --view-name "base:其他 15"
```

## 使用方法

### 基础示例

```bash
# 添加条形装饰（作为图表标题栏）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type decorate \
  --top 92 --left 16 \
  --width 412 --height 29 \
  --view-name "bar"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654239893 |
| --model-id | 是 | 数据模型 ID | 2597080602 |
| --dimension-field | 是 | 维度字段 | projectNo |
| --indicator-field | 是 | 指标字段 | receivingAmount |
| --chart-type | 是 | 图表类型，固定为 `decorate` | decorate |
| --top | 是 | Y 坐标 | 92 |
| --left | 是 | X 坐标 | 16 |
| --width | 是 | 组件宽度 | 412 |
| --height | 是 | 组件高度 | 29 |
| --view-name | 否 | 装饰子类型前缀 | "bar" 或 "square" 或 "base" |

### 尺寸建议

| 装饰类型 | 推荐宽度 | 推荐高度 | 使用场景 |
|---------|---------|---------|---------|
| 方形装饰 | 240-250 | 80-90 | 指标卡底部 |
| 条形装饰 | 410-420 | 28-30 | 图表标题栏 |
| 条形装饰（短） | 335-340 | 28-30 | 小图表标题 |
| 基础装饰 | 170-180 | 110-120 | 角落点缀 |

## 样式配置

### 完整样式结构

```json
{
  "screenPosition": {
    "position": {"x": 16, "y": 92, "w": 412, "h": 29}
  },
  "decorate": {},
  "decorateStyle": {
    "selectedDecorate": "barDecorate/barDecorate1.png"
  }
}
```

### 关键样式说明

#### 1. 装饰样式选择
```json
"decorateStyle": {
  "selectedDecorate": "barDecorate/barDecorate1.png"
}
```
- 格式：`{类型文件夹}/{类型文件名}.png`
- 决定使用哪个装饰图片

#### 2. 屏幕位置
```json
"screenPosition": {
  "position": {"x": 16, "y": 92, "w": 412, "h": 29}
}
```
- `x`: 左侧坐标
- `y`: 顶部坐标
- `w`: 宽度
- `h`: 高度

## 实战案例

### 案例 1：指标卡组合装饰

```bash
# 添加指标卡
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 20 --left 20 \
  --width 230 --height 130 \
  --view-name "累计收款" && \

# 添加方形装饰（指标卡下方）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type decorate \
  --top 150 --left 20 \
  --width 242 --height 84 \
  --view-name "square"
```

### 案例 2：图表标题栏装饰条

```bash
# 添加条形装饰（标题栏）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type decorate \
  --top 92 --left 16 \
  --width 412 --height 29 \
  --view-name "bar" && \

# 添加文本标题（装饰条上方）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type text \
  --top 92 --left 62 \
  --width 176 --height 35 \
  --view-name "收入合同" && \

# 添加图表（装饰条下方）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type bar \
  --top 130 --left 16 \
  --width 412 --height 300 \
  --view-name "收款趋势"
```

**层次结构**：
```
装饰条 (top: 92, height: 29)
  └─ 文本题目 (top: 92, 覆盖在装饰条上)
图表 (top: 130, 紧接装饰条下方)
```

### 案例 3：多个装饰条并列

```bash
# 第一排装饰条（4 个）
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type decorate \
  --top 123 --left 451 \
  --width 242 --height 84 \
  --view-name "square" && \

python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type decorate \
  --top 123 --left 710 \
  --width 242 --height 84 \
  --view-name "square" && \

python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type decorate \
  --top 123 --left 969 \
  --width 242 --height 84 \
  --view-name "square" && \

python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type decorate \
  --top 123 --left 1228 \
  --width 242 --height 84 \
  --view-name "square"
```

**布局效果**：
```
[装饰 1] [装饰 2] [装饰 3] [装饰 4]
  ↓      ↓      ↓      ↓
[指标卡 1][指标卡 2][指标卡 3][指标卡 4]
```

### 案例 4：角落基础装饰

```bash
# 左下角装饰
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type decorate \
  --top 970 --left 20 \
  --width 170 --height 110 \
  --view-name "base" && \

# 右下角装饰
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type decorate \
  --top 970 --left 1730 \
  --width 170 --height 110 \
  --view-name "base"
```

## 类型选择指南

### 按用途选择

| 用途 | 推荐类型 | 理由 |
|------|---------|------|
| 指标卡底部 | 方形装饰（square） | 形状匹配，视觉协调 |
| 图表标题栏 | 条形装饰（bar） | 细长形状，适合做标题背景 |
| 区域分隔 | 条形装饰（bar） | 水平线条，分隔清晰 |
| 角落点缀 | 基础装饰（base） | 不规则形状，灵活点缀 |
| 背景装饰 | 基础装饰（base） | 独立元素，不依赖其他组件 |

### 按位置选择

| 位置 | 推荐类型 | 典型尺寸 |
|------|---------|---------|
| 指标卡下方 | square | 242×84 |
| 图表上方 | bar | 412×29 |
| 画布顶部 | bar | 1920×80（通栏） |
| 画布角落 | base | 170×110 |
| 空白区域 | base | 根据空间调整 |

## 样式定制

### 切换装饰样式

装饰组件使用图片文件，切换样式需要修改 `selectedDecorate` 字段：

1. 查看当前配置：
```bash
python3 scripts/update_screen.py --screen-id 3654239893 --show-info
```

2. 记录装饰组件的 UUID

3. 手动修改样式（需要调用 API 或修改配置）

### 可用样式列表

**方形装饰**：
- `squareDecorate/squareDecorate1.png`
- `squareDecorate/squareDecorate2.png`
- `squareDecorate/squareDecorate3.png`

**条形装饰**：
- `barDecorate/barDecorate1.png`
- `barDecorate/barDecorate2.png`
- `barDecorate/barDecorate3.png`

**基础装饰**：
- `baseDecorate/baseDecorate1.png`
- `baseDecorate/baseDecorate2.png`
- `baseDecorate/baseDecorate3.png`

## 注意事项

### 1. 层级关系
- 装饰组件通常作为背景层
- 文本/指标卡组件叠加在装饰上方
- 注意调整 top 坐标实现叠加效果

### 2. 尺寸匹配
- 装饰宽度应与上方组件匹配
- 指标卡 230 宽 → 装饰 242 宽
- 图表 412 宽 → 装饰 412 宽

### 3. 颜色协调
- 装饰颜色应与主题一致
- 深色主题使用深色装饰
- 避免装饰过于鲜艳抢镜

### 4. 适度使用
- 装饰组件用于点缀，不宜过多
- 避免装饰影响数据展示
- 保持视觉简洁

## 与其他组件配合

### 典型组合

#### 1. 指标卡 + 方形装饰
```
+------------------+  ← top: 20
|   指标卡内容     |
+------------------+  ← top: 150
| [方形装饰]     |  ← 紧贴下方
+------------------+
```

#### 2. 装饰条 + 文本 + 图表
```
+------------------+  ← top: 92（装饰条）
| [文本标题]     |  ← top: 92（叠加）
+------------------+
|                  |  ← top: 130（图表）
|   图表内容      |
|                  |
+------------------+
```

#### 3. 角落基础装饰
```
+------------------+
| 大屏内容        |
|                  |
|         [装饰]  |  ← 右下角点缀
+------------------+
```

### 布局模板

```
画布：1920×1080

+--------------------------------------------------+
| [通栏装饰条 - bar] top: 0, height: 80            |  ← 顶部装饰
+--------------------------------------------------+
| [装饰条] [装饰条] [装饰条] [装饰条]              |  ← 指标卡标题栏
|  ↓      ↓      ↓      ↓                         |
| [指标卡][指标卡][指标卡][指标卡]                  |  ← 指标卡区域
|                                                  |
| [装饰条]                [装饰条]                 |  ← 图表标题栏
|  ↓                        ↓                     |
| [柱图 1]                [饼图 1]                 |  ← 图表区域
|                                                  |
| +-------------------------------------------+    |
| | [基础装饰]                         [基础装饰] | |  ← 角落装饰
| +-------------------------------------------+    |
+--------------------------------------------------+
```

## 常见问题

### Q1: 装饰组件看不到？
- 检查 `selectedDecorate` 文件路径是否正确
- 检查组件位置是否被其他组件遮挡
- 检查尺寸是否太小

### Q2: 如何切换装饰样式？
- 修改 `decorateStyle.selectedDecorate` 字段
- 使用不同的文件名（如 `barDecorate2.png`）

### Q3: 装饰与组件不对齐？
- 调整装饰的 `left` 和 `width` 参数
- 确保与上方组件宽度一致
- 使用相同的 `left` 坐标

### Q4: 如何叠加文本和装饰？
- 设置相同的 `top` 和 `left` 坐标
- 调整组件的层级顺序（layers 数组顺序）
- 确保文本在装饰上方显示

## 参考资源

- [SKILL.md](../../SKILL.md) - 技能主文档
- [add_component.py](./add_component.py) - 组件添加脚本
- [TEXT_COMPONENT_GUIDE.md](./TEXT_COMPONENT_GUIDE.md) - 文本组件指南
- [METRIC_COMPONENT_GUIDE.md](./METRIC_COMPONENT_GUIDE.md) - 指标卡组件指南（待创建）
