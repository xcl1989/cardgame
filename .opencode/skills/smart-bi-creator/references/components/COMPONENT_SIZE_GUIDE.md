# 组件尺寸指南

## ⚠️ 最小尺寸要求（强制执行）

为保证大屏显示效果，所有组件必须满足以下最小尺寸要求：

| 组件类型 | 最小宽度 | 最小高度 | 推荐尺寸 | 违反后果 |
|---------|---------|---------|---------|---------|
| **指标卡 (metric)** | 200px | 110px | 230×130 | 数值显示不完整 |
| **柱状图 (bar)** | 300px | 250px | 360×280 | Y 轴刻度重叠 |
| **折线图 (line)** | 300px | 250px | 360×280 | 趋势线被压缩 |
| **饼图 (pie)** | 300px | 250px | 450×280 | 图例文字重叠 |
| **排名图 (ranking)** | 350px | 280px | 470×280 | 只能显示 3-4 条 |
| **条形图 (horizontalBar)** | 300px | 280px | 360×350 | 标签被截断 |
| **双轴图 (dualAxis)** | 350px | 300px | 450×350 | 双 Y 轴拥挤 |
| **漏斗图 (funnel)** | 300px | 250px | 400×300 | 层次不清晰 |
| **仪表盘 (gauge)** | 250px | 200px | 300×250 | 刻度看不清 |
| **表格 (table)** | 400px | 200px | 600×300 | 列宽不足 |
| **地图 (map)** | 600px | 400px | 850×550 | 区域太小 |
| **文本 (text)** | 100px | 24px | 400×40 | 字体太小 |
| **装饰 (decorate)** | 固定尺寸 | 固定尺寸 | 见下表 | 图片变形 |

### 装饰组件固定尺寸

| 装饰类型 | 宽度 | 高度 | 说明 |
|---------|------|------|------|
| 条形装饰 (bar) | 412px | 29px | 不能调整大小 |
| 方形装饰 (square) | 242px | 84px | 不能调整大小 |
| 基础装饰 (base) | 170px | 110px | 不能调整大小 |
| 头部装饰 (head) | 1920px | 80px | 可调整宽度 |

## 📏 各区域组件尺寸推荐

### 1. 顶部指标卡区域（y: 90-220）

```
画布宽度：1920px
建议组件数：6-8 个指标卡

计算方式：
- 每个指标卡宽度：230px
- 间距：10px
- 总宽度：8 × 230 + 7 × 10 = 1910px（刚好填满）
```

**推荐配置**：
```bash
# 累计指标卡（4 个）
python3 scripts/add_component.py --chart-type metric \
  --top 90 --left 20 --width 230 --height 130 \
  --view-name "累计收款"

python3 scripts/add_component.py --chart-type metric \
  --top 90 --left 270 --width 230 --height 130 \
  --view-name "累计付款"

python3 scripts/add_component.py --chart-type metric \
  --top 90 --left 520 --width 230 --height 130 \
  --view-name "累计收票"

python3 scripts/add_component.py --chart-type metric \
  --top 90 --left 770 --width 230 --height 130 \
  --view-name "累计开票"

# 季度指标卡（4 个）
python3 scripts/add_component.py --chart-type metric \
  --top 90 --left 1020 --width 200 --height 130 \
  --view-name "季度收款"

python3 scripts/add_component.py --chart-type metric \
  --top 90 --left 1240 --width 200 --height 130 \
  --view-name "季度付款"
```

### 2. 中上区域（y: 220-500）

**左侧图表**（饼图、排名图）：
```bash
# 收款类型占比（饼图）
python3 scripts/add_component.py --chart-type pie \
  --top 220 --left 20 --width 450 --height 280 \
  --view-name "收款类型占比"

# 项目收款排名（排名图）
python3 scripts/add_component.py --chart-type ranking \
  --top 220 --left 490 --width 470 --height 280 \
  --view-name "项目收款排名"
```

**右侧主图**（柱状图、折线图）：
```bash
# 月度收款趋势（柱状图，视觉焦点）
python3 scripts/add_component.py --chart-type bar \
  --top 220 --left 980 --width 400 --height 560 \
  --view-name "月度收款趋势"
```

### 3. 中部区域（y: 520-780）

```bash
# 付款趋势（折线图）
python3 scripts/add_component.py --chart-type line \
  --top 520 --left 20 --width 360 --height 260 \
  --view-name "付款趋势"

# 收款方式分析（条形图）
python3 scripts/add_component.py --chart-type horizontalBar \
  --top 520 --left 400 --width 360 --height 260 \
  --view-name "收款方式分析"

# 项目收款 TOP10（垂直条形图）
python3 scripts/add_component.py --chart-type horizontalBar \
  --top 520 --left 780 --width 200 --height 540 \
  --view-name "项目收款 TOP10"
```

### 4. 底部区域（y: 800-1080）

```bash
# 收票趋势（柱状图）
python3 scripts/add_component.py --chart-type bar \
  --top 800 --left 20 --width 360 --height 260 \
  --view-name "收票趋势"

# 开票趋势（柱状图）
python3 scripts/add_component.py --chart-type bar \
  --top 800 --left 400 --width 360 --height 260 \
  --view-name "开票趋势"

# 项目付款排名（排名图）
python3 scripts/add_component.py --chart-type ranking \
  --top 800 --left 980 --width 420 --height 260 \
  --view-name "项目付款排名"
```

## 📐 组件间距规范

### 水平间距
- 指标卡之间：10px
- 图表之间：20px
- 图表与画布边缘：20px

### 垂直间距
- 指标卡与头部：10px（头部 bottom=80，指标卡 top=90）
- 指标卡与图表：20px（指标卡 bottom=220，图表 top=220）
- 图表之间：20px

### 计算示例
```
指标卡布局（8 个）：
left 坐标：20, 270, 520, 770, 1020, 1240, 1460, 1680
计算：20 + (230+10)×n

n=0: left=20
n=1: left=20+240=260 → 实际用 270（多 10px 间距）
n=2: left=270+250=520
n=3: left=520+250=770
...
```

## 🔍 尺寸检查

### 使用检查脚本
```bash
python3 scripts/check_layout.py --screen-id 123
```

**检查输出**：
```
4️⃣ 组件高度检查:
   ❌ 高度不足：收票趋势 高度 170px (最小要求 250px，建议增加 80px)
   ❌ 高度不足：开票趋势 高度 170px (最小要求 250px，建议增加 80px)
```

### 手动检查清单
- [ ] 所有指标卡高度 >= 110px
- [ ] 所有柱状图/折线图高度 >= 250px
- [ ] 所有排名图高度 >= 280px
- [ ] 装饰组件使用原始尺寸（未拉伸）
- [ ] 组件 right 坐标 <= 1920（不超出右边界）
- [ ] 组件 bottom 坐标 <= 1080（不超出下边界）

## ⚠️ 常见问题

### 问题 1：组件被压缩变形
**症状**：图表中的文字重叠、数据标签看不清

**原因**：高度低于最小要求

**解决**：
```bash
# 增加高度到推荐值
python3 scripts/update_screen.py \
  --screen-id 123 \
  --uuid "grid-type:bar-uuid:xxx" \
  --top 800 --left 20 \
  --width 360 --height 280  # 从 200 增加到 280
```

### 问题 2：装饰组件拉伸变形
**症状**：装饰图案模糊、失真

**原因**：改变了装饰组件的原始尺寸

**解决**：
```bash
# 删除拉伸的装饰，重新添加原始尺寸
python3 scripts/delete_component.py \
  --screen-id 123 \
  --uuid "grid-type:decorate-uuid:xxx"

python3 scripts/add_component.py \
  --chart-type decorate \
  --view-name "bar" \
  --top 210 --left 20 \
  --width 412 --height 29  # 使用原始尺寸
```

### 问题 3：组件超出画布
**症状**：组件底部或右侧被截断

**原因**：top + height > 1080 或 left + width > 1920

**解决**：
```bash
# 检查边界
right = left + width = 1000 + 500 = 1500 ✅ (< 1920)
bottom = top + height = 800 + 260 = 1060 ✅ (< 1080)

# 如果超出，调整位置或减小尺寸
python3 scripts/update_screen.py \
  --screen-id 123 \
  --uuid "xxx" \
  --top 800 --left 980 \
  --width 420 --height 260  # 确保 bottom <= 1080
```

## 📊 布局模板

详见：
- [经典经营分析大屏布局模板](../layouts/CLASSIC_LAYOUT_TEMPLATE.md)
- [1920×1080 画布布局参考](../layouts/layout_template.md)

## 🛠️ 工具推荐

### 布局规划工具
1. **Excel 布局规划表** - 计算每个组件的坐标
2. **纸笔草图** - 快速画出布局想法
3. **check_layout.py** - 自动检查尺寸和重叠

### 尺寸计算器
```python
# 快速计算组件位置
def calc_left(start, width, gap, index):
    """计算第 index 个组件的 left 坐标"""
    return start + (width + gap) * index

# 示例：8 个指标卡，每个 230px，间距 10px
for i in range(8):
    left = calc_left(20, 230, 10, i)
    print(f"指标卡{i+1}: left={left}")
# 输出：20, 260, 500, 740, 980, 1220, 1460, 1700
```
