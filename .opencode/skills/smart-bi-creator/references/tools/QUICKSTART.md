# 智能大屏创建 - 快速开始指南

## 5 分钟快速创建大屏

### 步骤 1: 准备认证信息

确保 `scripts/header.json` 已配置：

```json
{
  "accessToken": "your-access-token",
  "entCode": "your-ent-code",
  "uid": "your-user-id",
  "empCode": "your-emp-code"
}
```

### 步骤 2: 获取模型信息

```bash
# 查看可用的数据模型
python3 scripts/get_model_data.py --list

# 获取特定模型详情
python3 scripts/get_model_data.py --model-ids 2597080602 --output scripts/.cache/model.json
```

### 步骤 3: 创建基础大屏

```bash
# 创建一个柱状图大屏
python3 scripts/create_screen.py create \
  --name "公司资金分析大屏" \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --width 960 --height 400 \
  --chart-type bar

# 记录返回的 screen_id，例如：3654218321
```

### 步骤 4: 添加更多组件

```bash
# 添加指标卡（串行执行！）
python3 scripts/add_component.py \
  --screen-id 3654218321 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --width 220 --height 140 \
  --top 30 --left 20 \
  --view-name "累计收款" && \
python3 scripts/add_component.py \
  --screen-id 3654218321 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --width 220 --height 140 \
  --top 30 --left 250 \
  --view-name "本月收款"
```

### 步骤 5: 调整布局

```bash
# 查看当前所有组件位置
python3 scripts/update_screen.py --screen-id 3654218321 --show-info

# 移动组件到指定位置
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:bar-uuid:xxx" \
  --top 200 --left 410 --width 1100 --height 500
```

### 步骤 6: 修改图表标题

```bash
# 修改组件标题（重要！）
python3 scripts/rename_component.py \
  --screen-id 3654218321 \
  --uuid "grid-type:bar-uuid:xxx" \
  --title "月度收款趋势分析"
```

### 步骤 7: 查看大屏

访问返回的 URL，例如：
```
https://dev.cloud.hecom.cn/biserver/largescreenpreview?id=3654218321
```

---

## 常用命令速查

### 创建组件

```bash
# 创建大屏
python3 scripts/create_screen.py create --name "xxx" --model-id xxx ...

# 添加组件
python3 scripts/add_component.py --screen-id xxx --model-id xxx ...
```

### 调整布局

```bash
# 查看布局
python3 scripts/update_screen.py --screen-id xxx --show-info

# 调整位置/大小
python3 scripts/update_screen.py --screen-id xxx --uuid "xxx" --top 100 --left 200 --width 400 --height 300

# 居中
python3 scripts/update_screen.py --screen-id xxx --uuid "xxx" --center --width 960 --height 400
```

### 修改标题

```bash
# 修改组件标题
python3 scripts/rename_component.py --screen-id xxx --uuid "xxx" --title "新标题"
```

---

## 推荐布局模板（1920×1080）

### 标准布局

```
顶部：8 个指标卡 (top=30, 220×140, 间距 20px)
中部：主图表 (top=200, 1100×500, left=410 居中)
底部：4 个图表 (top=720, 460×300, 间距 20px)
```

### 坐标计算公式

```python
# 居中
center_left = (1920 - width) // 2

# 等分布局
margin = 20
gap = 20
count = 4
width = (1920 - margin*2 - gap*(count-1)) // count

for i in range(count):
    left = margin + i * (width + gap)
```

---

## 常见问题

### Q1: 添加组件时提示覆盖？

**A**: 必须串行执行，使用 `&&` 连接：

```bash
# ✅ 正确
python3 scripts/add_component.py ... && \
python3 scripts/add_component.py ...

# ❌ 错误（会覆盖）
python3 scripts/add_component.py ... &
python3 scripts/add_component.py ... &
```

### Q2: 修改标题不生效？

**A**: 不要使用 `update_screen.py --name`，应该使用：

```bash
python3 scripts/rename_component.py \
  --screen-id xxx \
  --uuid "xxx" \
  --title "新标题"
```

### Q3: 指标卡数值显示不全？

**A**: 增加高度到 140px：

```bash
python3 scripts/update_screen.py \
  --screen-id xxx \
  --uuid "grid-type:metric-uuid:xxx" \
  --height 140
```

### Q4: 组件重叠怎么办？

**A**: 
1. 先用 `--show-info` 查看所有组件位置
2. 计算好坐标再调整
3. 组件之间至少留 20px 间距

---

## 参考文档

- **[FAQ.md](tools/FAQ.md)** - 详细常见问题解决方案
- **[CASE_STUDY.md](../layouts/CASE_STUDY.md)** - 实战优化案例
- **[SKILL.md](SKILL.md)** - 完整技能文档
- **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - 快速参考手册

---

## 获取帮助

```bash
# 查看脚本帮助
python3 scripts/create_screen.py --help
python3 scripts/add_component.py --help
python3 scripts/update_screen.py --help
python3 scripts/rename_component.py --help
```
