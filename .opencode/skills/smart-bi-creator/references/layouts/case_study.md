# 大屏优化实战案例

## 问题背景

用户创建了一个公司资金分析大屏，包含：
- 顶部：8 个指标卡（累计收款、本月收款、累计开票、本月开票、累计付款、本月付款、收款方式、项目阶段）
- 中部：主图表（收款日期分析柱状图）
- 底部：4 个图表（收款类型占比、付款申请趋势、开票趋势、项目收款排行）

## 遇到的问题

### 问题 1: 指标卡高度不够
**现象**: 数值显示不完整，被截断  
**原因**: 默认高度 110px 太小

### 问题 2: 中间图表左右太空
**现象**: 主图表宽度 850px，左右有大量空白  
**原因**: 宽度不够，未充分利用 1920px 画布

### 问题 3: 图表标题显示为"柱图 1"
**现象**: 图表标题没有使用创建时的 view-name 参数  
**原因**: 需要同时修改大屏配置中的 3 个位置

### 问题 4: 底部图表宽度不均匀
**现象**: 第 4 个图表只有 170px 宽度，特别窄  
**原因**: 布局计算不当

## 解决方案

### 1. 增加指标卡高度

```bash
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:metric-uuid:xxx" \
  --top 30 --width 220 --height 140
```

**效果**: 所有指标卡高度从 110px 增加到 140px，数值完整显示

### 2. 加宽中间图表

```bash
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:bar-uuid:xxx" \
  --top 200 --left 410 \
  --width 1100 --height 500
```

**计算**: `left = (1920 - 1100) / 2 = 410px`（居中）

**效果**: 主图表从 850px 加宽到 1100px，减少左右空白

### 3. 修改图表标题

创建专用脚本 `scripts/rename_component.py`:

```bash
python3 scripts/rename_component.py \
  --screen-id 3654218321 \
  --uuid "grid-type:bar-uuid:1773823950771" \
  --title "月度收款趋势分析"
```

**原理**: 同时修改 3 个位置
- `config.layers[].title` - 图层标题
- `componentMap[uuid].viewName` - 组件视图名称
- `layouts[].title` - 布局标题

**效果**: 图表标题从"柱图 1"改为"月度收款趋势分析"

### 4. 平均分配底部图表宽度

```bash
# 计算：(1920 - 40 - 60) / 4 = 455 ≈ 460px
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:pie-uuid:xxx" \
  --top 720 --left 20 --width 460 --height 300 && \
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:line-uuid:xxx" \
  --top 720 --left 500 --width 460 --height 300 && \
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:line-uuid:xxx" \
  --top 720 --left 980 --width 460 --height 300 && \
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:bar-uuid:xxx" \
  --top 720 --left 1460 --width 460 --height 300
```

**布局**:
```
left=20   → 图 1 (460px)
left=500  → 图 2 (460px)
left=980  → 图 3 (460px)
left=1460 → 图 4 (460px)
间距：20px
```

**效果**: 4 个图表宽度均匀，布局美观

## 最终布局

```
画布：1920 × 1080

┌────────────────────────────────────────────────────────────┐
│ 顶部：8 个指标卡 (top=30, 220×140, 间距 20px)              │
│ [累计收款][本月收款][累计开票][本月开票][累计付款][本月付款][收款方式][项目阶段] │
├────────────────────────────────────────────────────────────┤
│                                                             │
│        月度收款趋势分析 (柱图，1100×500, 居中)             │
│        top=200, left=410                                  │
│                                                             │
├────────────────────────────────────────────────────────────┤
│ 底部：4 个图表 (top=720, 460×300, 间距 20px)               │
│ [收款类型占比] [付款申请趋势] [开票趋势] [项目收款排行]   │
│   left=20    left=500    left=980    left=1460           │
└────────────────────────────────────────────────────────────┘
```

## 关键经验

### 1. 布局规划公式

```python
# 居中计算
center_left = (canvas_width - component_width) // 2

# 等分布局
margin = 20  # 边距
gap = 20     # 间距
count = 4    # 组件数量
width = (1920 - margin * 2 - gap * (count - 1)) // count

for i in range(count):
    left = margin + i * (width + gap)
```

### 2. 组件尺寸推荐

| 组件类型 | 宽度 | 高度 | 说明 |
|---------|------|------|------|
| 指标卡 | 220 | 140 | 高度至少 140，数值才完整 |
| 主图表 | 1100 | 500 | 视觉焦点，居中展示 |
| 底部图表 | 460 | 300 | 4 个并排，均匀分布 |

### 3. 安全间距

- 指标卡到底部：170px (top=30 + height=140)
- 主图表顶部：200px (留 30px 间距)
- 主图表底部：700px (top=200 + height=500)
- 底部图表顶部：720px (留 20px 间距)

### 4. 修改组件标题

**不要使用**: `update_screen.py --name` (这是修改大屏名称)

**应该使用**: 
```bash
python3 scripts/rename_component.py \
  --screen-id xxx \
  --uuid "xxx" \
  --title "新标题"
```

## 常用命令速查

```bash
# 查看大屏信息
python3 scripts/update_screen.py --screen-id 3654218321 --show-info

# 调整组件位置/大小
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:xxx" \
  --top 30 --left 20 --width 220 --height 140

# 修改组件标题
python3 scripts/rename_component.py \
  --screen-id 3654218321 \
  --uuid "grid-type:bar-uuid:xxx" \
  --title "新标题"

# 访问大屏
https://dev.cloud.hecom.cn/biserver/largescreenpreview?id=3654218321
```

## 参考文档

- [FAQ.md](FAQ.md) - 常见问题与解决方案
- [SKILL.md](SKILL.md) - 完整技能文档
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 快速参考
