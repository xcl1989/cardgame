---
name: smart-bi-creator
description: 智能大屏创建技能，用于通过 API 自动化创建和管理 BI 数据大屏。支持创建单组件/多组件大屏、获取和更新大屏配置、调整组件位置大小样式。当用户需要创建新大屏、更新已有大屏、管理多组件布局时使用此技能。所有脚本执行前必须确保工作目录是技能根目录。
---

# 智能大屏创建 (Smart BI Creator)

## 🚀 快速开始

**5 分钟创建你的第一个大屏** → [快速开始指南](references/tools/QUICKSTART.md)

---

## ⚠️ 核心原则（必读）

### 1. 工作目录要求

**所有脚本必须在技能根目录执行**：

```bash
# 方式 1：cd 到技能目录（推荐）
cd /path/to/smart-bi-creator
python3 scripts/create_screen.py create --name "测试大屏" ...

# 方式 2：使用 workdir 参数
workdir="/path/to/smart-bi-creator"
command="python3 scripts/create_screen.py ..."

# 方式 3：使用绝对路径
python3 /path/to/smart-bi-creator/scripts/create_screen.py ...
```

### 2. 操作完成检查

**每次创建/修改/删除组件后必须执行检查**：

```bash
python3 scripts/check_layout.py --screen-id <大屏ID>
```

检查结果：
- ✅ 无重叠 → 告知用户完成
- ❌ 有重叠 → 先修复问题，再检查直到通过

### 3. 串行执行

**添加多个组件必须串行执行**：

```bash
# ✅ 正确：使用 && 连接
python3 scripts/add_component.py ... && \
python3 scripts/add_component.py ... && \
python3 scripts/add_component.py ...

# ❌ 错误：并行执行（会覆盖）
python3 scripts/add_component.py ... &
python3 scripts/add_component.py ... &
```

---

## ⚠️ 数据模型原则（重要！）

**一个大屏可以用多个数据模型，但每个组件内只能使用一个数据模型！**

- 组件的 `modelId` 决定了该组件使用哪个数据模型
- 组件内所有配置（indicators、filter、dimensions）必须使用同一个数据模型
- 如果组件使用了支付记录模型（2593236659），那筛选配置中的 datasetId、fieldId 等都必须对应支付记录模型

详见：[FAQ - 数据模型原则](references/tools/FAQ.md)

---

## 📊 核心工作流

### 方式一：快速创建（单组件）

```bash
python3 scripts/create_screen.py create \
  --name "收款分析大屏" \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --width 960 --height 400 \
  --chart-type bar
```

### 方式二：分步构建多组件大屏（推荐）

**步骤 1：创建基础大屏**
```bash
python3 scripts/create_screen.py create \
  --name "项目收付款分析大屏"
```

**步骤 2：添加组件（串行！）**
```bash
# 添加指标卡
python3 scripts/add_component.py \
  --screen-id <ID> --model-id 2597080602 \
  --dimension-field receivingDate --indicator-field receivingAmount \
  --chart-type metric --top 10 --left 10 \
  --width 230 --height 130 --view-name "累计收款" && \

# 添加柱图
python3 scripts/add_component.py \
  --screen-id <ID> --model-id 2597080602 \
  --dimension-field receivingDate --indicator-field receivingAmount \
  --chart-type bar --top 200 --left 50 \
  --width 450 --height 300 --view-name "收款趋势"
```

**步骤 3：检查布局**
```bash
python3 scripts/check_layout.py --screen-id <ID>
```

### 方式三：智能工作流（利用大模型）

```bash
# 1. 获取模型列表
python3 scripts/get_model_data.py --list

# 2. 获取选中模型详情
python3 scripts/get_model_data.py \
  --model-ids 2597080602 2537727927 \
  --output scripts/.cache/models_info.json

# 3. 根据设计方案创建大屏
```

详见 [智能工作流](references/tools/WORKFLOW.md)

---

## 📁 脚本工具

| 脚本 | 说明 |
|------|------|
| `get_model_data.py` | 获取模型列表和详细信息 |
| `list_screens.py` | 列出所有大屏、按名称搜索 |
| `check_layout.py` | **检查布局**（每次操作后必执行） |
| `create_screen.py` | 创建新大屏 |
| `add_component.py` | 添加新组件到已有大屏 |
| `delete_component.py` | 删除组件 |
| `delete_screen.py` | **删除整个大屏**（删除前需用户确认） |
| `update_screen.py` | 查看和更新大屏配置 |
| `rename_component.py` | 修改组件标题 |
| `generate_background.py` | 生成 AI 背景图片 |
| `header.json` | 认证配置文件 |

---

## 🗑️ 删除大屏

删除大屏前**必须用户确认**，不会直接删除。

```bash
# 查看所有大屏
python3 scripts/delete_screen.py --list

# 删除大屏（会提示确认）
python3 scripts/delete_screen.py --screen-id 3662265901
```

删除确认提示：
```
⚠️  确认删除大屏
==================================================
大屏 ID: 3662265901
大屏名称: 企业收付款分析大屏
访问地址: https://dev.cloud.hecom.cn/largescreenpreview?id=3662265901
==================================================

请输入 'yes' 确认删除: 
```

---

## 📐 布局规范（重要）

**创建大屏时必须遵循以下布局规范，这样大屏才会饱满丰富：**

### 边距规范
| 位置 | 边距 | 说明 |
|------|------|------|
| 左侧 | 20px | 固定 |
| 右侧 | 20px | 固定 |
| 底部 | 20px | 固定 |

### 组件间隔
| 间隔类型 | 间距 | 说明 |
|----------|------|------|
| 组件之间 | 20px | 所有数据组件之间的间隔 |
| 行与行之间 | 20px | 指标卡行、中间层、底部层之间 |

### 高度分配（画布1080px）

```
头部: top=0, height=80
指标卡: top=80, height=130, bottom=210
间隔: 20px
中间层: top=210, height=350, bottom=560
间隔: 20px
底部层: top=560, height=500, bottom=1060
底部边距: 20px
```

### 计算公式

**多列布局宽度计算：**
```
可用宽度 = 1920 - 左20 - 右20 = 1880px
组件宽度 = (可用宽度 - (列数-1) × 20) / 列数
```

**示例：7个指标卡**
```python
可用宽度 = 1880
组件宽度 = (1880 - 6 × 20) / 7 = 251px
```

**示例：三列图表**
```python
可用宽度 = 1880
列1宽度 = 580
列2宽度 = 580
列3宽度 = 1880 - 580 - 580 - 2 × 20 = 680
```

### ❌ 错误示例
- 左右边距不一致（左边20，右边100）
- 组件之间间距不统一（有的20，有的50）
- 底部边距太大（超过50px显得空旷）

---

## 📋 布局模板：7+3+3 标准布局

**最常用的收付款分析大屏模板**，结构为：7个指标卡 + 3列中间图表 + 3列底部图表

### 模板结构图
```
┌─────────────────────────────────────────────────────────────────┐
│  头部 (1920×80)                                                │
├─────────────────────────────────────────────────────────────────┤
│  指标卡1  指标卡2  指标卡3  指标卡4  指标卡5  指标卡6  指标卡7  │  ← top=80, h=130
├─────────────────────────────────────────────────────────────────┤
│                                                                  │  ← 间隔20px
│  月度趋势柱图    趋势折线图    月度付款柱图                       │  ← top=230, h=350
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │  ← 间隔20px
│  项目收款排名   供应商付款排名   收款类型饼图                     │  ← top=600, h=460
│                                                                  │
└─────────────────────────────────────────────────────────────────┘  ← 底部边距20px
```

### 模板参数

| 层级 | top | height | 说明 |
|------|-----|--------|------|
| 头部 | 0 | 80 | 固定 |
| 指标卡 | 80 | 130 | 7个并排，间距20px |
| 中间层 | 230 | 350 | 3列，间距20px |
| 底部层 | 600 | 460 | 3列，间距20px |
| 底部边距 | - | 20 | 固定 |

### 指标卡位置（7个）
```
left = 20, 291, 562, 833, 1104, 1375, 1646
width = 251
间距 = 20px
```

### 三列图表位置
```
可用宽度 = 1880
列1: left=20, width=580
列2: left=620, width=580
列3: left=1220, width=680
间距 = 20px
```

### 快速创建命令

```bash
# 1. 创建大屏
python3 scripts/create_screen.py --name "收付款分析大屏" --model-id 2597080602

# 2. 添加7个指标卡（使用循环或手动）
python3 scripts/add_component.py --screen-id <ID> --model-id xxx \
  --chart-type metric --top 80 --left 20 --width 251 --height 130 ...

# 3. 添加中间层3个图表
python3 scripts/add_component.py --screen-id <ID> --chart-type bar \
  --top 230 --left 20 --width 580 --height 350 ...
python3 scripts/add_component.py --screen-id <ID> --chart-type line \
  --top 230 --left 620 --width 580 --height 350 ...
python3 scripts/add_component.py --screen-id <ID> --chart-type bar \
  --top 230 --left 1220 --width 680 --height 350 ...

# 4. 添加底部层3个图表
python3 scripts/add_component.py --screen-id <ID> --chart-type ranking \
  --top 600 --left 20 --width 580 --height 460 ...
python3 scripts/add_component.py --screen-id <ID> --chart-type ranking \
  --top 600 --left 620 --width 580 --height 460 ...
python3 scripts/add_component.py --screen-id <ID> --chart-type pie \
  --top 600 --left 1220 --width 680 --height 460 ...

# 5. 检查布局
python3 scripts/check_layout.py --screen-id <ID>
```

---

## 🧩 组件类型

| 类型 | CLI 值 | 说明 |
|------|--------|------|
| 柱状图 | `bar` | 垂直柱图、时间趋势 |
| 3D柱图 | `bar3D` | 3D 柱状图 |
| 折线图 | `line` | 趋势线 |
| 饼图 | `pie` | 占比分析（支持环形/实心） |
| 指标卡 | `metric` | 数字指标（5 种样式） |
| 表格 | `table` | 数据表格 |
| 排名图 | `ranking` | Top N 排行榜 |
| 条形图 | `horizontalBar` | 水平条形图 |
| 地图 | `map` | 地理分布 |
| 雷达图 | `radar` | 多指标对比 |
| 翻牌器 | `flipper` | 数字滚动 |
| 双轴图 | `dualAxis` | 双 Y 轴组合图 |
| 漏斗图 | `funnel` | 漏斗流程分析 |
| 仪表盘 | `gauge` | 仪表盘/进度 |
| 脚本组件 | `script` | ECharts 自定义 |
| 文本 | `text` | 标题/标签 |
| 装饰 | `decorate` | 装饰元素 |
| 头部 | `head` | 顶部通栏装饰 |
| 时间 | `time` | 时间显示 |
| 走马灯 | `marquee` | 滚动文字 |
| 卡片 | `card` | 容器卡片 |
| 图标 | `icon` | 图标展示 |

## 📚 组件指南（20 个）

### ⚠️ 趋势图要求（重要）

**趋势图（柱图、折线图）必须满足以下两点：**

#### 1. 排序：使用时间维度排序，禁止指标排序
- 指标 `orderType` 优先级高于维度 `orderType`
- 如果设置了指标排序，时间维度排序会失效
- 创建趋势图后，使用 `--indicator-order-type none` 清除指标排序

```bash
# ✅ 正确：清除指标排序
python3 scripts/update_screen.py --screen-id <ID> --uuid <uuid> --indicator-order-type none
```

#### 2. 日期格式：月度数据必须使用 YM 格式
- 月度趋势图的日期维度必须设置 `dateFormat: YM`
- 显示格式：2024-01 而不是 2024-01-15
- 通过修改组件配置 `dimensions[].dateFormat = "YM"` 实现

### ⚠️ 指标卡要求（重要）

**多个指标卡必须满足以下两点：**

#### 1. 颜色统一
- 同一大屏中的指标卡使用**相同颜色**（如 `#00D4FF` 科技蓝）
- 保持视觉一致性，推荐颜色：`#00D4FF`、`#00FF88`、`#FFB800`

#### 2. 布局对齐
- 指标卡必须**左右对齐**
- 左侧边距 = 右侧边距（对称）
- 所有指标卡**宽度相同**，**间距相同**

**计算公式（7个指标卡）：**
```
左边距=20, 右边距=20, 间距=20
指标卡宽度 = (1920-40-6*20)/7 = 251px
```

### 数据可视化
- [指标卡](references/components/METRIC_COMPONENT_GUIDE.md) - 5 种样式预设
- [柱图](references/components/BAR_COMPONENT_GUIDE.md)
- [3D柱图](references/components/BAR3D_COMPONENT_GUIDE.md)
- [折线图](references/components/LINE_COMPONENT_GUIDE.md)
- [饼图](references/components/PIE_COMPONENT_GUIDE.md)
- [条形图](references/components/HORIZONTAL_BAR_COMPONENT_GUIDE.md)
- [排名图](references/components/RANKING_COMPONENT_GUIDE.md)
- [雷达图](references/components/RADAR_COMPONENT_GUIDE.md)
- [地图](references/components/MAP_COMPONENT_GUIDE.md)
- [漏斗图](references/components/FUNNEL_COMPONENT_GUIDE.md)
- [仪表盘](references/components/GAUGE_COMPONENT_GUIDE.md)

### 数据展示
- [表格](references/components/TABLE_COMPONENT_GUIDE.md)
- [翻牌器](references/components/FLIPPER_COMPONENT_GUIDE.md)

### 装饰与布局
- [文本](references/components/TEXT_COMPONENT_GUIDE.md)
- [装饰](references/components/DECORATE_COMPONENT_GUIDE.md)
- [头部](references/components/HEAD_COMPONENT_GUIDE.md)
- [卡片](references/components/CARD_COMPONENT_GUIDE.md)
- [图标](references/components/ICON_COMPONENT_GUIDE.md)
- [时间](references/components/TIME_COMPONENT_GUIDE.md)
- [走马灯](references/components/MARQUEE_COMPONENT_GUIDE.md)

### 高级功能
- [脚本组件](references/components/SCRIPT_COMPONENT_GUIDE.md) - ECharts 自定义
- [组件联动](references/components/LINKAGE_GUIDE.md)
- [双轴图](references/components/DUAL_AXIS_COMPONENT_GUIDE.md)
- [组件尺寸](references/components/COMPONENT_SIZE_GUIDE.md)

---

## ⚡ 常用命令速查

```bash
# 创建大屏
python3 scripts/create_screen.py create --name "xxx" --model-id xxx ...

# 添加组件
python3 scripts/add_component.py --screen-id xxx --model-id xxx \
  --dimension-field xxx --indicator-field xxx \
  --chart-type bar --top 200 --left 50 --width 450 --height 300

# 查看布局
python3 scripts/update_screen.py --screen-id xxx --show-info

# 移动组件
python3 scripts/update_screen.py --screen-id xxx --uuid "xxx" --top 100 --left 200

# 修改组件标题
python3 scripts/rename_component.py --screen-id xxx --uuid "xxx" --title "新标题"

# 删除组件
python3 scripts/delete_component.py --screen-id xxx --uuid "xxx"

# 检查布局
python3 scripts/check_layout.py --screen-id xxx

# 环境切换
--env dev    # 开发环境（默认）
--env test   # 测试环境
--env prod   # 生产环境
```

---

## 🔧 认证配置

`scripts/header.json` 存储认证信息：

```json
{
  "accessToken": "your-access-token",
  "entCode": "your-ent-code",
  "uid": "your-user-id",
  "empCode": "your-emp-code"
}
```

---

## ❓ 常见问题

详见 [FAQ.md](references/tools/FAQ.md)

| 问题 | 解决方案 |
|------|----------|
| 组件被覆盖 | 使用 `&&` 串行执行 |
| 标题修改不生效 | 使用 `rename_component.py` |
| 指标卡数值不全 | 增加高度到 130px+ |
| 装饰图片变形 | 使用原始尺寸，不拉伸 |
| 日期格式不对 | 设置 `dateFormat` 属性 |

---

## 📖 参考文档

### 快速入门
- [快速开始](references/tools/QUICKSTART.md) - 5 分钟创建第一个大屏
- [快速参考](references/tools/QUICK_REFERENCE.md) - 命令速查手册

### 组件指南
- [指标卡](references/components/METRIC_COMPONENT_GUIDE.md) - 5 种样式预设
- [柱图](references/components/BAR_COMPONENT_GUIDE.md)
- [折线图](references/components/LINE_COMPONENT_GUIDE.md)
- [饼图](references/components/PIE_COMPONENT_GUIDE.md)
- [表格](references/components/TABLE_COMPONENT_GUIDE.md)
- [地图](references/components/MAP_COMPONENT_GUIDE.md)
- [排名图](references/components/RANKING_COMPONENT_GUIDE.md)
- [条形图](references/components/HORIZONTAL_BAR_COMPONENT_GUIDE.md)
- [翻牌器](references/components/FLIPPER_COMPONENT_GUIDE.md)
- [雷达图](references/components/RADAR_COMPONENT_GUIDE.md)
- [脚本组件](references/components/SCRIPT_COMPONENT_GUIDE.md)

### 布局与案例
- [数字大屏模版31](references/layouts/TEMPLATE_DIGITAL_SCREEN_31.md) - 深色科技风布局（推荐）
- [经典布局模板](references/layouts/CLASSIC_LAYOUT_TEMPLATE.md)
- [实战案例](references/layouts/case_study.md)

### 工具文档
- [智能工作流](references/tools/WORKFLOW.md) - 利用大模型创建大屏
- [FAQ](references/tools/FAQ.md) - 常见问题与解决方案
- [删除组件](references/tools/DELETE_COMPONENT_USAGE.md)
- [最佳实践](references/tools/QUICK_REFERENCE.md)

### 技术参考
- [配置结构详解](references/config_structure.md)
- [必填字段说明](references/required_fields.md)
- [数据模型 API](references/model_api.md)

### 其他
- [目录结构](DIRECTORY_STRUCTURE.md) - 项目目录组织
- [更新日志](references/tools/UPDATE_LOG.md)

---

## 🎯 最佳实践

| 习惯 | 重要性 |
|------|--------|
| 执行前确认目录 (`pwd`) | ⭐⭐⭐⭐⭐ |
| 添加组件串行执行 (`&&`) | ⭐⭐⭐⭐⭐ |
| 调整后必运行检查 | ⭐⭐⭐⭐⭐ |
| 立即记录 UUID | ⭐⭐⭐⭐ |
| 小步快跑（每次 1-2 个组件） | ⭐⭐⭐⭐ |
| 先规划后执行 | ⭐⭐⭐⭐ |

详见 [快速参考](references/tools/QUICK_REFERENCE.md)
