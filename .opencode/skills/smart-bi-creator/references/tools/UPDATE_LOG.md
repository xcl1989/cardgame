# 更新日志

## 2026-03-24 - 卡片样式标准化

### 新增功能

#### 1. 组件卡片样式支持

**涉及文件**: `scripts/add_component.py`, `scripts/update_screen.py`

**卡片样式参数**:
| 参数 | 说明 | 示例值 |
|------|------|-------|
| `--card-background-color` | 卡片背景色 | `rgba(13, 24, 44, 0.8)` |
| `--card-border` | 卡片边框颜色 | `rgba(30, 39, 55, 0.8)` |
| `--card-padding` | 内边距 | `12` |

**标准卡片样式**（深蓝半透明）:
```json
{
  "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
  "border": "rgba(30, 39, 55, 0.8)",
  "padding": 12
}
```

**使用方式**:
```bash
# update_screen.py 更新卡片样式
python3 scripts/update_screen.py \
  --screen-id 3657066337 \
  --uuid "grid-type:line-uuid:xxx" \
  --card-background-color "rgba(13, 24, 44, 0.8)" \
  --card-border "rgba(30, 39, 55, 0.8)" \
  --card-padding 12
```

---

### 代码变更

#### 1. add_component.py - 默认卡片样式

**修改位置**: `get_chart_style_json()` 方法

**修改内容**: 以下组件类型的默认卡片样式从透明改为深蓝半透明：
- ✅ LINE（折线图）
- ✅ BAR（柱图）
- ✅ PIE（饼图）
- ✅ RANKING（排名图）
- ✅ HORIZONTAL BAR（条形图）
- ✅ MAP（地图）
- ✅ SCRIPT（脚本组件）

**保留透明的组件**:
- 文本组件（text）- 设计如此
- 指标卡 minimal 样式 - 极简风格需要
- 装饰组件（decorate）- 使用图片
- 头部组件（head）- 使用图片

#### 2. update_screen.py - 新增卡片样式更新

**新增方法**: `update_component_card_style()`

**参数**:
- `card_background_color`: 卡片背景色
- `card_border`: 边框颜色
- `card_padding`: 内边距

**命令行参数**:
- `--card-background-color`
- `--card-border`
- `--card-padding`

---

### 文档更新

#### 1. SKILL.md
- ✅ 新增卡片样式参数说明
- ✅ 添加 update_screen.py 卡片样式更新示例
- ✅ 添加标准卡片样式参考

#### 2. QUICK_REFERENCE.md
- ✅ 新增卡片样式调整命令

---

### 应用场景

**批量更新组件样式**:
```bash
# 更新所有非 head/text/script 组件为标准卡片样式
python3 scripts/update_screen.py --screen-id 3657066337 \
  --uuid "grid-type:pie-uuid:xxx" \
  --card-background-color "rgba(13, 24, 44, 0.8)" \
  --card-border "rgba(30, 39, 55, 0.8)" \
  --card-padding 12
```

---

## 2024-03-18 - 大屏优化与文档增强

### 新增功能

#### 1. 新增 rename_component.py 脚本
**文件**: `scripts/rename_component.py`

**用途**: 修改大屏组件标题

**使用方式**:
```bash
python3 scripts/rename_component.py \
  --screen-id 3654218321 \
  --uuid "grid-type:bar-uuid:1773823950771" \
  --title "月度收款趋势分析"
```

**原理**: 同时修改大屏配置中的 3 个位置
- `config.layers[].title` - 图层标题
- `componentMap[uuid].viewName` - 组件视图名称  
- `layouts[].title` - 布局标题

**优势**: 
- 解决了 `update_screen.py --name` 只能修改大屏名称的问题
- 一条命令同时更新 3 个位置，确保标题一致性
- 支持批量修改多个组件标题

---

### 新增文档

#### 1. FAQ.md - 常见问题与解决方案
**文件**: `FAQ.md`

**内容**:
- ✅ 指标卡高度不够，数值显示不全
- ✅ 中间图表左右太空
- ✅ 图表标题显示为默认名称（如"柱图 1"）
- ✅ 底部图表宽度不均匀
- ✅ 组件重叠问题
- ✅ 添加组件时发生覆盖
- ✅ 实用脚本模板
- ✅ 最佳实践总结
- ✅ 布局规划模板
- ✅ 坐标计算公式

**特点**:
- 每个问题都有详细的问题描述、原因分析、解决方法
- 提供可直接执行的命令示例
- 包含实用脚本模板（可保存为脚本重复使用）
- 提供最佳实践总结和检查清单

---

#### 2. CASE_STUDY.md - 实战案例
**文件**: `CASE_STUDY.md`

**内容**:
- 问题背景介绍
- 4 个主要问题及解决方案
- 最终布局展示
- 关键经验总结
- 常用命令速查
- 布局规划公式
- 组件尺寸推荐表

**特点**:
- 基于真实用户反馈的优化案例
- 完整的问题→解决流程记录
- 可直接复用的布局模板
- 实用的计算公式和尺寸参考

---

### 文档更新

#### 1. SKILL.md
**更新内容**:
- ✅ 新增 `rename_component.py` 用法说明
- ✅ 强调修改组件标题的正确方法
- ✅ 更新脚本工具表格
- ✅ 添加 FAQ.md 和 CASE_STUDY.md 引用
- ✅ 优化常见问题章节结构

**新增章节**:
```markdown
### rename_component.py 用法（修改组件标题）

> ⚠️ **重要**: `update_screen.py` 的 `--name` 参数修改的是**大屏名称**，不是组件标题。
```

---

### 优化改进

#### 1. 组件标题修改流程优化
**之前**: 需要手动编辑 JSON 或使用复杂的 Python 代码
**现在**: 一条命令完成

```bash
# 之前：需要写 20+ 行 Python 代码
python3 -c "import json, requests; ..."

# 现在：一条清晰的命令
python3 scripts/rename_component.py --screen-id xxx --uuid xxx --title "新标题"
```

#### 2. 最佳实践总结
基于实际优化经验，总结出以下最佳实践：

**布局规划**:
```
顶部：8 个指标卡 (220×140, 间距 20px)
中部：主图表 (1100×500, 居中)
底部：4 个图表 (460×300, 均匀分布)
```

**安全间距**:
- 组件之间至少 20px
- 指标卡高度≥140px
- 主图表宽度 1100px（充分利用画布）

**调试流程**:
1. 使用 `--show-info` 查看所有组件位置
2. 逐个调整，避免批量修改导致混乱
3. 使用 `rename_component.py` 修改标题

---

### 使用示例

#### 完整优化流程

```bash
# 1. 查看当前布局
python3 scripts/update_screen.py --screen-id 3654218321 --show-info

# 2. 调整指标卡高度
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:metric-uuid:xxx" \
  --top 30 --width 220 --height 140

# 3. 加宽主图表
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:bar-uuid:xxx" \
  --top 200 --left 410 --width 1100 --height 500

# 4. 修改图表标题
python3 scripts/rename_component.py \
  --screen-id 3654218321 \
  --uuid "grid-type:bar-uuid:1773823950771" \
  --title "月度收款趋势分析"

# 5. 平均分配底部图表
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:xxx" \
  --top 720 --left 20 --width 460 --height 300
```

---

### 文件清单

**新增文件**:
- ✅ `scripts/rename_component.py` - 组件标题修改脚本
- ✅ `FAQ.md` - 常见问题与解决方案
- ✅ `CASE_STUDY.md` - 实战案例文档
- ✅ `UPDATE_LOG.md` - 本文档（更新日志）

**更新文件**:
- ✅ `SKILL.md` - 添加 rename_component.py 用法和文档引用

---

### 影响范围

**适用场景**:
- 需要修改大屏组件标题
- 需要优化大屏布局
- 遇到组件重叠、尺寸不当等问题
- 需要参考最佳实践创建新大屏

**向后兼容**:
- ✅ 所有现有脚本保持不变
- ✅ 新增脚本不影响现有功能
- ✅ 文档更新不影响现有代码

---

### 后续计划

1. **增强 rename_component.py**:
   - 支持批量修改（从文件读取 UUID 和标题映射）
   - 支持自动检测未命名组件

2. **增加布局模板**:
   - 提供预设布局模板（6 指标卡、8 指标卡等）
   - 一键应用布局模板

3. **可视化工具**:
   - 创建简单的 Web 界面查看和调整布局
   - 实时预览组件位置

---

### 反馈与建议

如有问题或建议，请参考：
- [FAQ.md](./FAQ.md) - 查看常见问题
- [CASE_STUDY.md](../layouts/CASE_STUDY.md) - 参考实战案例
- [SKILL.md](../../SKILL.md) - 查看完整文档
