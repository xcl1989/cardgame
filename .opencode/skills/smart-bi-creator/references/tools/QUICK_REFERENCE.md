# 智能大屏创建 - 快速参考卡片

## 🚀 快速开始

### 1. 创建大屏（单组件）
```bash
python3 scripts/create_screen.py create \
  --name "经营分析大屏 2024" \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --width 900 --height 500
```

### 2. 添加组件（串行！）
```bash
python3 scripts/add_component.py \
  --screen-id 3654109910 \
  --model-id 2597080602 \
  --dimension-field paymentMethod \
  --indicator-field receivingAmount \
  --chart-type pie \
  --top 190 --left 600 \
  --width 370 --height 290 \
  --view-name "收款方式构成" && \
python3 scripts/add_component.py \
  --screen-id 3654109910 \
  --model-id 2537727927 \
  --dimension-field applicationDate \
  --indicator-field applicationAmount \
  --chart-type line \
  --top 190 --left 990 \
  --width 370 --height 290 \
  --view-name "付款趋势"
```

### 3. 调整位置
```bash
python3 scripts/update_screen.py \
  --screen-id 3654109910 \
  --uuid "grid-type:bar-uuid:xxx" \
  --top 190 --left 550 \
  --width 850 --height 550
```

### 4. 查看状态
```bash
python3 scripts/update_screen.py \
  --screen-id 3654109910 \
  --show-info
```

---

## ⚠️ 重要警告

### 必须串行执行！
```bash
# ❌ 错误：并行会覆盖
python3 scripts/add_component.py ... &
python3 scripts/add_component.py ... &

# ✅ 正确：使用 && 连接
python3 scripts/add_component.py ... && \
python3 scripts/add_component.py ... && \
python3 scripts/add_component.py ...
```

**原因**: `add_component.py` 会获取当前配置→添加组件→更新配置。并行执行时，多个命令同时获取旧配置，导致后面的覆盖前面的。

---

## 📐 推荐尺寸

| 组件 | 宽度 | 高度 | 说明 |
|------|------|------|------|
| 指标卡 | 230 | 130 | 高度至少 120 |
| 主图表 | 850 | 550 | 视觉焦点 |
| 侧边图 | 480-510 | 260-290 | 对称分布 |
| 底部图 | 600 | 300 | 并排 3 个 |

---

## 🎯 推荐布局（15 组件）

```
顶部：8 个指标卡（230×130）
左中：月度收款（柱图 510×260）
中间：资金趋势（大折线图 850×550）⭐
左下：收款方式（饼图 510×270）
右上：付款趋势（折线图 480×260）
右下：开票分析（饼图 480×270）
底部：3 个柱图（600×300）
```

---

## 🐛 常见问题速查

| 问题 | 原因 | 解决 |
|------|------|------|
| 组件重叠 | 位置计算错误 | 用 `--show-info` 查看，逐个调整 |
| 数值截断 | 指标卡太矮 | 高度增加到 130px |
| 大量留白 | 组件太少/太小 | 增加指标卡，加大主图表 |
| 无视觉焦点 | 组件一样大 | 创建 850×550 大图表居中 |
| 组件丢失 | 并行执行 | 用 `&&` 串行执行 |

---

## 📋 命令速查

### 创建
```bash
# 创建基础大屏
python3 scripts/create_screen.py create \
  --name "大屏名称" \
  --model-id 123 \
  --dimension-field date \
  --indicator-field amount \
  --width 900 --height 500
```

### 添加
```bash
# 添加组件（记得用 &&）
python3 scripts/add_component.py \
  --screen-id 123 \
  --model-id 456 \
  --dimension-field field1 \
  --indicator-field field2 \
  --chart-type bar \
  --top 200 --left 50 \
  --width 500 --height 300 \
  --view-name "组件名称"
```

### 调整
```bash
# 调整位置
python3 scripts/update_screen.py \
  --screen-id 123 \
  --uuid "grid-type:xxx" \
  --top 200 --left 550 \
  --width 850 --height 550

# 更新卡片样式（背景色、边框、内边距）
python3 scripts/update_screen.py \
  --screen-id 123 \
  --uuid "grid-type:xxx" \
  --card-background-color "rgba(13, 24, 44, 0.8)" \
  --card-border "rgba(30, 39, 55, 0.8)" \
  --card-padding 12

# 查看状态
python3 scripts/update_screen.py \
  --screen-id 123 \
  --show-info
```

---

## 📊 布局规划步骤

1. **画草图** - 用纸笔或 Excel 规划布局
2. **算坐标** - 计算每个组件的 top/left/width/height
3. **建大屏** - 创建基础大屏（主图表）
4. **加组件** - 串行添加其他组件
5. **调位置** - 微调坐标和尺寸
6. **查效果** - 访问 URL 查看实际效果

---

## 🔗 参考文档

- [case_study.md](./case_study.md) - 实战案例
- [layout_template.md](./layout_template.md) - 布局模板
- [WORKFLOW.md](./WORKFLOW.md) - 完整工作流
- [SKILL.md](SKILL.md) - 技能说明

---

## 💡 提示

- **指标卡高度**: 至少 120px，推荐 130-140px
- **组件间距**: 至少 10px，推荐 15-20px
- **主图表尺寸**: 至少 800×500
- **组件数量**: 12-18 个最合适
- **串行执行**: 永远用 `&&` 连接添加命令
