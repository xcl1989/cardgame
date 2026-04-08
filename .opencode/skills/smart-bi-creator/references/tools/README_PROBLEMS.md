# 大屏创建问题总结与经验教训

## 概述

本文档记录了在创建"精工装经营驾驶舱"大屏过程中遇到的所有问题、解决方案和经验教训。

**项目目标**: 创建一个大屏分析公司的项目、收款、付款和开票数据

**最终成果**: 
- 大屏名称：精工装经营驾驶舱 2024
- 大屏 ID: 3654109910
- 组件数量：15 个
- 访问地址：https://dev.cloud.hecom.cn/largescreenpreview?id=3654109910

---

## 问题时间线

### 问题 1：并行添加组件导致覆盖 ❌

**时间**: 第一次添加组件时

**现象**: 
- 执行了 4 个并行的 `add_component.py` 命令
- 期望添加 4 个指标卡
- 实际只添加了 1-2 个

**原因分析**:
```
add_component.py 工作流程:
1. GET /largeScreen/get/{id} - 获取当前配置（N 个组件）
2. 在内存中添加新组件（N+1 个）
3. POST /largeScreen/update/{id} - 更新配置

并行执行时:
命令 A: GET(配置 N) → 添加 A → UPDATE(N+1 个组件)
命令 B: GET(配置 N) → 添加 B → UPDATE(N+1 个组件) ← 覆盖了 A!
命令 C: GET(配置 N) → 添加 C → UPDATE(N+1 个组件) ← 覆盖了 A 和 B!
```

**解决方案**: 使用 `&&` 串行执行

```bash
# ✅ 正确做法
python3 scripts/add_component.py ... && \
python3 scripts/add_component.py ... && \
python3 scripts/add_component.py ...
```

**影响**: 
- 在 SKILL.md 中添加了醒目的警告提示
- 在 QUICK_REFERENCE.md 中作为第一条注意事项
- 在 WORKFLOW.md 中添加了详细说明

**教训**: ⚠️ **这是最重要的教训，必须串行执行！**

---

### 问题 2：组件重叠 ❌

**时间**: 添加 19 个组件后

**现象**: 
- 右上角两个柱图部分重叠
- 中间的饼图和折线图重叠
- 指标卡之间也有重叠

**原因分析**:
1. 组件数量过多（19 个）
2. 位置计算不精确
3. 没有预留足够间距
4. 边创建边调整，缺乏整体规划

**尝试的解决方案**:

1. **逐个调整位置** - 修改了 10+ 次
   ```bash
   python3 scripts/update_screen.py \
     --screen-id 3654102867 \
     --uuid "xxx" \
     --top 190 --left 510
   ```

2. **调整组件尺寸** - 缩小到 430×270
   ```bash
   python3 scripts/update_screen.py \
     --screen-id 3654102867 \
     --uuid "xxx" \
     --width 430 --height 270
   ```

3. **删除重复组件** - 移除 2 个
   ```python
   uuids_to_remove = [
       "grid-type:bar-uuid:xxx",  # 实际付款金额（重复）
       "grid-type:pie-uuid:xxx",  # 项目状态分布（无数据）
   ]
   ```

**最终解决**: 重新创建大屏，精简到 15 个组件，合理布局

**影响**: 
- 在 SKILL.md 中添加了"组件重叠问题"章节
- 创建了 layout_template.md 提供布局模板
- 建议 1920×1080 画布使用 12-18 个组件

**教训**: 📐 **创建前必须规划布局！**

---

### 问题 3：指标卡数值显示不全 ❌

**时间**: 查看大屏效果时

**现象**: 
```
累计收款
收款金额
0.0  ← 最后一位被截断
```

**原因分析**: 
- 指标卡高度设置为 90-110px
- 数值字体大小 + 标签高度 > 指标卡高度

**解决方案**: 增加高度到 130px

```bash
python3 scripts/update_screen.py \
  --screen-id 3654109910 \
  --uuid "grid-type:metric-uuid:xxx" \
  --top 40 --left 20 \
  --width 230 --height 130
```

**影响**: 
- 在 SKILL.md 中添加了"指标卡数值显示不全"章节
- 推荐指标卡最小高度 120px，最佳 130-140px

**教训**: 📏 **指标卡高度至少 130px！**

---

### 问题 4：大屏留白过多 ❌

**时间**: 第一次创建完成后

**现象**: 
- 右侧 1/3 画布空白
- 底部 1/4 画布空白
- 组件只占据了左上角区域

**原因分析**:
1. 组件数量太少（只有 10 个）
2. 组件尺寸偏小（都是 400-500 宽度）
3. 缺乏整体布局规划

**解决方案**:

1. **增加顶部指标卡** - 从 4 个增加到 8 个
   ```bash
   python3 scripts/add_component.py ... --view-name "本月收款" && \
   python3 scripts/add_component.py ... --view-name "季度收款" && \
   python3 scripts/add_component.py ... --view-name "实际付款" && \
   python3 scripts/add_component.py ... --view-name "项目总数"
   ```

2. **添加中间主图表** - 作为视觉焦点
   ```bash
   python3 scripts/add_component.py \
     --width 850 --height 550 \
     --top 190 --left 550 \
     --view-name "资金流入趋势分析"
   ```

3. **填充底部** - 3 个柱图并排
   ```bash
   python3 scripts/add_component.py \
     --width 600 --height 300 \
     --top 760 --left 20 && \
   python3 scripts/add_component.py \
     --width 600 --height 300 \
     --top 760 --left 640 && \
   python3 scripts/add_component.py \
     --width 600 --height 300 \
     --top 760 --left 1260
   ```

**影响**: 
- 在 SKILL.md 中添加了"大屏留白过多"章节
- 在 layout_template.md 中提供了 3 种布局模板
- 推荐顶部 8 个指标卡、中间大图表、底部 3 个柱图的布局

**教训**: 📊 **充分利用画布空间！**

---

### 问题 5：没有视觉焦点 ❌

**时间**: 布局调整过程中

**现象**: 
- 所有组件都是 400-500 宽度
- 不知道应该看哪里
- 缺乏层次感

**原因分析**: 
- 平均主义思维，所有组件一样大
- 没有主次的概念

**解决方案**: 创建大尺寸主图表

```bash
python3 scripts/add_component.py \
  --width 850 --height 550 \
  --top 190 --left 550 \
  --view-name "资金流入趋势分析"
```

**效果对比**:
- **之前**: 10 个组件都是 500×300，无重点
- **之后**: 中间 850×550 大图表，两侧 480-510 小图表

**影响**: 
- 在 SKILL.md 中添加了"没有视觉焦点"章节
- 在所有布局模板中都包含了大尺寸主图表
- 推荐主图表尺寸 800-900×520-580

**教训**: 🎯 **必须有一个明显的主视觉图表！**

---

### 问题 6：访问 URL 格式错误 ❌

**时间**: 每次创建大屏后

**现象**: 
- 脚本输出的 URL 无法访问
- 显示 404 错误

**原因分析**: 
使用了错误的 URL 格式
```
❌ https://dev.cloud.hecom.cn/paas/bi-app/largeScreen/3654102867
✅ https://dev.cloud.hecom.cn/biserver/largescreenpreview?id=3654102867
```

**解决方案**: 修改 3 个脚本的 URL 输出
- `create_screen.py` - 2 处（第 608 行、第 664 行）
- `add_component.py` - 1 处（第 522 行）
- `update_screen.py` - 1 处（第 254 行）

**修改内容**:
```python
# 修改前
print(f"访问 URL: {args.base_url}/paas/bi-app/largeScreen/{screen_id}")

# 修改后
print(f"访问 URL: {args.base_url}/largescreenpreview?id={screen_id}")
```

**影响**: 
- 所有脚本的 URL 输出已统一修正
- 避免了后续使用中的困惑

**教训**: 🔗 **URL 格式要随时检查！**

---

## 经验总结

### 关键教训 TOP 5

1. ⚠️ **串行执行** - 添加组件必须用 `&&` 连接，否则会覆盖
2. 📐 **先规划后执行** - 用 Excel 或纸笔规划位置再执行
3. 📊 **组件数量** - 1920×1080 画布建议 12-18 个组件
4. 📏 **指标卡高度** - 至少 120px，推荐 130-140px
5. 🎯 **视觉焦点** - 必须有一个大尺寸主图表（850×550）

### 推荐工作流程

1. **获取模型信息** - 了解可用字段
   ```bash
   python3 scripts/get_model_data.py --list
   ```

2. **设计布局** - 画草图，标注尺寸和位置
   - 参考 layout_template.md 中的模板
   - 用 Excel 计算坐标

3. **创建基础大屏** - 先创建一个主图表
   ```bash
   python3 scripts/create_screen.py create ...
   ```

4. **串行添加组件** - 用 `&&` 逐个添加
   ```bash
   python3 scripts/add_component.py ... && \
   python3 scripts/add_component.py ... && \
   python3 scripts/add_component.py ...
   ```

5. **调整位置** - 微调坐标和尺寸
   ```bash
   python3 scripts/update_screen.py --screen-id 123 --uuid "xxx" --top 200 --left 550
   ```

6. **检查效果** - 访问 URL 查看实际效果
   ```bash
   # 查看 https://dev.cloud.hecom.cn/biserver/largescreenpreview?id=123
   ```

### 文档更新

**新增文档**:
1. `references/case_study.md` - 完整实战案例
2. `references/layout_template.md` - 布局模板和计算工具
3. `QUICK_REFERENCE.md` - 快速参考卡片
4. `README_PROBLEMS.md` - 本文档

**更新文档**:
1. `SKILL.md` - 添加常见问题章节（8 个问题）
2. `WORKFLOW.md` - 添加常见问题和参考文档链接

---

## 最佳实践检查清单

### 创建前
- [ ] 确定大屏主题和目标受众
- [ ] 选择合适的模型和字段
- [ ] 确定组件数量（12-18 个）
- [ ] 用 Excel 或纸笔画出布局草图
- [ ] 计算每个组件的坐标和尺寸
- [ ] 预留组件间距（至少 10px）

### 创建时
- [ ] 使用 `&&` 串行添加组件
- [ ] 先创建主图表（视觉焦点）
- [ ] 再添加指标卡
- [ ] 然后添加两侧图表
- [ ] 最后添加底部图表
- [ ] 记录每个组件的 UUID

### 创建后
- [ ] 检查是否有组件重叠
- [ ] 检查指标卡数值是否完整显示
- [ ] 检查是否有大量留白
- [ ] 检查是否有明确的视觉焦点
- [ ] 调整不合理的组件位置
- [ ] 访问实际 URL 查看效果

---

## 最终推荐配置

### 大屏配置
- **名称**: 精工装经营驾驶舱 2024
- **画布**: 1920×1080
- **组件数**: 15 个

### 布局
- **顶部**: 8 个指标卡（230×130）
- **左中**: 月度收款趋势（柱图 510×260）
- **左下**: 收款方式构成（饼图 510×270）
- **中间**: 资金流入趋势分析（大折线图 850×550）⭐ 主视觉
- **右上**: 付款趋势（折线图 480×260）
- **右下**: 开票分析（饼图 480×270）
- **底部**: 3 个柱图（600×300）

### 访问地址
https://dev.cloud.hecom.cn/biserver/largescreenpreview?id=3654109910

---

## 结语

通过这次大屏创建实践，我们遇到了 6 个主要问题，每一个都提供了解决方案和预防措施。这些经验教训已经整理到技能文档中，希望能为后续的大屏创建工作提供参考。

**核心理念**: 
1. **规划先行** - 磨刀不误砍柴工
2. **串行执行** - 永远用 `&&` 连接
3. **视觉焦点** - 必须有大尺寸主图表
4. **合理布局** - 12-18 个组件最合适
5. **持续优化** - 创建后检查和调整

**文档不是终点，而是起点。** 希望这些文档能帮助更多人创建出美观、实用的大屏！
