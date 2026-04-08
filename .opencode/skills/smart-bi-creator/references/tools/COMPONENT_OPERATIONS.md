# 组件添加与修改使用说明

## 📋 添加组件完整流程

### 方式一：单个添加（推荐新手）

```bash
# 步骤 1：添加组件
python3 scripts/add_component.py \
  --screen-id 3654350038 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type bar \
  --view-name "月度收款趋势" \
  --top 220 --left 980 \
  --width 400 --height 560

# 输出示例：
# ✅ 组件添加成功!
# 组件 UUID: grid-type:bar-uuid:1773886044832  ← 立即复制保存！

# 步骤 2：运行布局检查
python3 scripts/check_layout.py --screen-id 3654350038

# 步骤 3：修改组件标题（如需要）
python3 scripts/rename_component.py \
  --screen-id 3654350038 \
  --uuid "grid-type:bar-uuid:1773886044832" \
  --title "月度收款趋势"

# 步骤 4：查看实际效果
# 浏览器打开：https://dev.cloud.hecom.cn/largescreenpreview?id=3654350038
```

### 方式二：批量添加（串行执行）

```bash
# 使用 && 连接多个命令（必须串行！）
python3 scripts/add_component.py \
  --screen-id 3654350038 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --view-name "累计收款" \
  --top 90 --left 20 --width 230 --height 130 && \

python3 scripts/add_component.py \
  --screen-id 3654350038 \
  --model-id 2537727927 \
  --dimension-field applicationDate \
  --indicator-field applicationAmount \
  --chart-type metric \
  --view-name "累计付款" \
  --top 90 --left 270 --width 230 --height 130 && \

python3 scripts/add_component.py \
  --screen-id 3654350038 \
  --model-id 2998196151 \
  --dimension-field invoiceDate \
  --indicator-field taxAmount \
  --chart-type metric \
  --view-name "累计收票" \
  --top 90 --left 520 --width 230 --height 130 && \

python3 scripts/add_component.py \
  --screen-id 3654350038 \
  --model-id 2998192935 \
  --dimension-field invoiceDate \
  --indicator-field taxAmount \
  --chart-type metric \
  --view-name "累计开票" \
  --top 90 --left 770 --width 230 --height 130

# 全部完成后，运行一次检查
python3 scripts/check_layout.py --screen-id 3654350038
```

### 方式三：使用 JSON 配置文件（高级）

创建配置文件 `components_config.json`：
```json
{
  "screen_id": 3654350038,
  "components": [
    {
      "view_name": "累计收款",
      "model_id": 2597080602,
      "chart_type": "metric",
      "dimension_field": "receivingDate",
      "indicator_field": "receivingAmount",
      "top": 90,
      "left": 20,
      "width": 230,
      "height": 130
    },
    {
      "view_name": "累计付款",
      "model_id": 2537727927,
      "chart_type": "metric",
      "dimension_field": "applicationDate",
      "indicator_field": "applicationAmount",
      "top": 90,
      "left": 270,
      "width": 230,
      "height": 130
    }
  ]
}
```

使用脚本读取配置（需自行实现或手动执行）。

---

## 📝 修改组件完整流程

### 修改组件位置

```bash
# 查看当前组件位置
python3 scripts/update_screen.py --screen-id 3654350038 --show-info

# 修改组件位置
python3 scripts/update_screen.py \
  --screen-id 3654350038 \
  --uuid "grid-type:bar-uuid:1773886044832" \
  --top 240 --left 1000

# 运行检查
python3 scripts/check_layout.py --screen-id 3654350038
```

### 修改组件大小

```bash
# 修改组件大小（同时可改位置）
python3 scripts/update_screen.py \
  --screen-id 3654350038 \
  --uuid "grid-type:bar-uuid:1773886044832" \
  --top 220 --left 980 \
  --width 450 --height 600

# 运行检查（确保不小于最小尺寸）
python3 scripts/check_layout.py --screen-id 3654350038
```

### 修改组件标题

```bash
# 使用专用脚本（同时修改 3 个位置）
python3 scripts/rename_component.py \
  --screen-id 3654350038 \
  --uuid "grid-type:bar-uuid:1773886044832" \
  --title "月度收款趋势分析"

# 验证修改
python3 scripts/update_screen.py --screen-id 3654350038 --show-info
```

### 移动组件到画布中心

```bash
python3 scripts/update_screen.py \
  --screen-id 3654350038 \
  --uuid "grid-type:bar-uuid:1773886044832" \
  --center --width 960 --height 540
```

### 对齐组件

```bash
# 左对齐（多个组件相同的 left 坐标）
python3 scripts/update_screen.py \
  --screen-id 3654350038 \
  --uuid "grid-type:bar-uuid:xxx" \
  --top 520 --left 20

python3 scripts/update_screen.py \
  --screen-id 3654350038 \
  --uuid "grid-type:line-uuid:yyy" \
  --top 800 --left 20  # 相同的 left=20
```

---

## 🔧 常用操作示例

### 1. 添加一排指标卡（8 个）

```bash
# 前 4 个：累计指标
python3 scripts/add_component.py --screen-id 3654350038 \
  --model-id 2597080602 --dimension-field receivingDate \
  --indicator-field receivingAmount --chart-type metric \
  --view-name "累计收款" --top 90 --left 20 --width 230 --height 130 && \

python3 scripts/add_component.py --screen-id 3654350038 \
  --model-id 2537727927 --dimension-field applicationDate \
  --indicator-field applicationAmount --chart-type metric \
  --view-name "累计付款" --top 90 --left 270 --width 230 --height 130 && \

python3 scripts/add_component.py --screen-id 3654350038 \
  --model-id 2998196151 --dimension-field invoiceDate \
  --indicator-field taxAmount --chart-type metric \
  --view-name "累计收票" --top 90 --left 520 --width 230 --height 130 && \

python3 scripts/add_component.py --screen-id 3654350038 \
  --model-id 2998192935 --dimension-field invoiceDate \
  --indicator-field taxAmount --chart-type metric \
  --view-name "累计开票" --top 90 --left 770 --width 230 --height 130

# 后 4 个：季度指标
python3 scripts/add_component.py --screen-id 3654350038 \
  --model-id 2597080602 --dimension-field receivingDate \
  --indicator-field receivingAmount --chart-type metric \
  --view-name "季度收款" --top 90 --left 1020 --width 200 --height 130 && \

python3 scripts/add_component.py --screen-id 3654350038 \
  --model-id 2537727927 --dimension-field applicationDate \
  --indicator-field applicationAmount --chart-type metric \
  --view-name "季度付款" --top 90 --left 1240 --width 200 --height 130 && \

python3 scripts/add_component.py --screen-id 3654350038 \
  --model-id 2998196151 --dimension-field invoiceDate \
  --indicator-field taxAmount --chart-type metric \
  --view-name "季度收票" --top 90 --left 1460 --width 200 --height 130 && \

python3 scripts/add_component.py --screen-id 3654350038 \
  --model-id 2998192935 --dimension-field invoiceDate \
  --indicator-field taxAmount --chart-type metric \
  --view-name "季度开票" --top 90 --left 1680 --width 220 --height 130

# 完成后检查
python3 scripts/check_layout.py --screen-id 3654350038
```

### 2. 添加主图表区域

```bash
# 主图：月度收款趋势（柱状图）
python3 scripts/add_component.py --screen-id 3654350038 \
  --model-id 2597080602 --dimension-field receivingDate \
  --indicator-field receivingAmount --chart-type bar \
  --view-name "月度收款趋势" \
  --top 220 --left 980 --width 400 --height 560

# 辅助图：项目收款占比（饼图）
python3 scripts/add_component.py --screen-id 3654350038 \
  --model-id 2597080602 --dimension-field projectNo \
  --indicator-field receivingAmount --chart-type pie \
  --view-name "项目收款占比" \
  --top 220 --left 1400 --width 500 --height 400

# 辅助图：支付方式分析（柱状图）
python3 scripts/add_component.py --screen-id 3654350038 \
  --model-id 2597080602 --dimension-field paymentMethod \
  --indicator-field receivingAmount --chart-type bar \
  --view-name "支付方式分析" \
  --top 640 --left 1400 --width 500 --height 420

# 检查布局
python3 scripts/check_layout.py --screen-id 3654350038
```

### 3. 删除并替换组件

```bash
# 1. 查看当前组件
python3 scripts/delete_component.py --screen-id 3654350038 --list

# 2. 删除旧组件
python3 scripts/delete_component.py --screen-id 3654350038 \
  --uuid "grid-type:bar-uuid:old-uuid"

# 3. 添加新组件
python3 scripts/add_component.py --screen-id 3654350038 \
  --model-id 2597080602 --dimension-field receivingDate \
  --indicator-field receivingAmount --chart-type bar \
  --view-name "新版收款趋势" \
  --top 220 --left 980 --width 450 --height 600

# 4. 检查布局
python3 scripts/check_layout.py --screen-id 3654350038
```

---

## ⚠️ 重要注意事项

### 1. 必须串行执行
```bash
# ✅ 正确
cmd1 && cmd2 && cmd3

# ❌ 错误（会覆盖）
cmd1 & cmd2 & cmd3
```

### 2. 立即记录 UUID
```bash
# 添加组件后输出：
✅ 组件添加成功!
组件 UUID: grid-type:bar-uuid:1773886044832

# 立即保存到清单：
| 组件名称 | UUID | 位置 | 尺寸 |
|---------|------|------|------|
| 月度收款趋势 | grid-type:bar-uuid:1773886044832 | (980,220) | 400×560 |
```

### 3. 每次调整后必须检查
```bash
# 标准流程
添加/修改组件 → check_layout.py → 浏览器查看效果

# 只有检查通过 ✅ 才能继续下一步
```

### 4. 尺寸不能低于最小要求
```bash
# 检查输出示例：
❌ 高度不足：收票趋势 高度 170px (最小要求 250px)

# 解决方案：增加高度
python3 scripts/update_screen.py \
  --screen-id 123 \
  --uuid "xxx" \
  --top 800 --left 20 \
  --width 360 --height 280  # 从 200 增加到 280
```

### 5. 装饰组件不能拉伸
```bash
# ❌ 错误：拉伸装饰
--width 900 --height 29  # 图片变形！

# ✅ 正确：原始尺寸
--width 412 --height 29  # 条形装饰原始尺寸
```

---

## 🔍 故障排查

### 问题 1：组件添加后不显示
**可能原因**：
- 位置超出画布（检查 top/left 坐标）
- 尺寸太小（检查 width/height）
- 被其他组件覆盖（检查重叠）

**解决**：
```bash
python3 scripts/check_layout.py --screen-id 123
# 查看检查结果，修复所有 ❌ 问题
```

### 问题 2：组件标题修改不生效
**原因**：只修改了一个位置

**解决**：使用专用脚本
```bash
python3 scripts/rename_component.py \
  --screen-id 123 \
  --uuid "xxx" \
  --title "新标题"
# 自动修改 layer、componentMap、layouts 三处
```

### 问题 3：添加组件后其他组件丢失
**原因**：并行执行导致覆盖

**解决**：重新添加，必须串行
```bash
# 删除所有组件重新开始
python3 scripts/delete_component.py --screen-id 123 --uuid "uuid1" && \
python3 scripts/delete_component.py --screen-id 123 --uuid "uuid2"

# 重新串行添加
python3 scripts/add_component.py ... && \
python3 scripts/add_component.py ... && \
python3 scripts/add_component.py ...
```

---

## 📊 组件配置速查表

### 图表类型与字段配置

| 图表类型 | chart-type 值 | 维度字段示例 | 指标字段示例 |
|---------|-------------|------------|------------|
| 指标卡 | metric | receivingDate | receivingAmount |
| 柱状图 | bar | receivingDate/projectNo | receivingAmount |
| 折线图 | line | applicationDate | applicationAmount |
| 饼图 | pie | receivingType/paymentMethod | receivingAmount |
| 排名图 | ranking | projectNo | receivingAmount |
| 条形图 | horizontalBar | paymentMethod | receivingAmount |
| 装饰 | decorate | 任意（不使用） | 任意（不使用） |
| 文本 | text | 任意（不使用） | 任意（不使用） |
| 头部 | head | 任意（不使用） | 任意（不使用） |

### 常用模型 ID

| 模型名称 | 模型 ID | 主要字段 |
|---------|--------|---------|
| 收款登记模型 1219 | 2597080602 | receivingDate, receivingAmount, receivingType |
| 付款申请 | 2537727927 | applicationDate, applicationAmount, projectNo |
| 开票登记 | 2998192935 | invoiceDate, taxAmount, projectNo |
| 收票登记 | 2998196151 | invoiceDate, taxAmount, projectNo |

---

## 📖 相关文档

- [组件尺寸指南](COMPONENT_SIZE_GUIDE.md) - 最小尺寸要求
- [装饰组件指南](DECORATE_COMPONENT_GUIDE.md) - 装饰组件使用
- [布局检查工具](../tools/CHECK_LAYOUT_USAGE.md) - check_layout.py 使用说明
- [最佳实践](../tools/BEST_PRACTICES.md) - 避免常见错误
