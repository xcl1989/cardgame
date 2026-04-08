# 智能大屏创建工作流

## 概述

本工作流利用大模型的理解和规划能力，配合自动化工具，实现从模糊需求到完整大屏的创建。

## 工作流程

```
用户需求 → 获取模型列表 → 大模型选择模型 → 获取模型详情 → 大模型设计布局 → 自动创建大屏
```

## 步骤详解

### 步骤 1：获取模型列表

```bash
python3 scripts/get_model_data.py --list --output scripts/.cache/model_list.json
```

**输出**: 包含所有模型 ID 和名称的 JSON 文件

### 步骤 2：大模型选择合适的模型

将模型列表提供给大模型，让它根据用户需求选择合适的模型。

**示例提示词**:
```
用户需求：我想创建一个大屏来分析公司的收款和付款情况

以下是所有可用的数据模型（共 283 个）：
[粘贴 model_list.json 的内容]

请帮我分析：
1. 哪些模型适合分析"收款和付款情况"？
2. 每个模型可能包含哪些关键字段？
3. 推荐 3-5 个最相关的模型 ID

请以 JSON 格式返回：
{
  "selected_models": [
    {"id": 123, "name": "模型名", "reason": "选择理由"},
    ...
  ],
  "analysis": "分析说明"
}
```

### 步骤 3：获取选中模型的详细信息

```bash
python3 scripts/get_model_data.py \
  --model-ids 2597080602 2537727927 2782975184 \
  --output scripts/.cache/selected_models_info.json
```

**输出**: 包含选中模型详细字段信息的 JSON 文件

### 步骤 4：大模型设计大屏布局

将模型详细信息提供给大模型，让它设计大屏布局。

**示例提示词**:
```
用户需求：我想创建一个大屏来分析公司的收款和付款情况

已选择的模型详细信息：
[粘贴 selected_models_info.json 的内容]

请帮我设计一个大屏，包含：
1. 大屏名称（要有吸引力）
2. 需要哪些组件？（建议 5-8 个）
3. 每个组件的类型、位置、大小
4. 每个组件使用哪个模型的哪些字段

画布大小：1920 x 1080

请以 JSON 格式返回设计方案：
{
  "dashboard_name": "大屏名称",
  "components": [
    {
      "order": 1,
      "view_name": "组件显示名称",
      "chart_type": "bar|line|pie|metric",
      "model_id": 123,
      "dimension_field": "维度字段名",
      "indicator_field": "指标字段名",
      "top": 100,
      "left": 100,
      "width": 440,
      "height": 270,
      "description": "这个组件分析什么内容"
    },
    ...
  ],
  "layout_description": "整体布局说明"
}
```

### 步骤 5：根据设计方案创建大屏

#### 5.1 创建基础大屏（第一个组件）

```bash
python3 scripts/create_screen.py create \
  --name "公司收款付款分析大屏" \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --width 960 \
  --height 400 \
  --chart-type bar
```

记录返回的 `screen_id`。

#### 5.2 添加其他组件

> ⚠️ **重要：添加组件必须串行执行！**
> 
> `add_component.py` 脚本会先获取当前大屏配置，添加新组件后再更新。如果并行执行多个添加命令，后面的命令会基于旧配置覆盖前面已添加的组件。
> 
> **正确做法**：使用 `&&` 连接多个命令，或逐个执行等待完成后再执行下一个。

根据设计方案的 `components` 数组，从第 2 个组件开始：

```bash
# 组件 2-6：一次性添加所有组件（使用 && 串行执行）
python3 scripts/add_component.py \
  --screen-id 3654099936 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 80 --left 40 \
  --width 260 --height 120 \
  --view-name "累计收款" && \
python3 scripts/add_component.py \
  --screen-id 3654099936 \
  --model-id 2597080602 \
  --dimension-field paymentMethod \
  --indicator-field receivingAmount \
  --chart-type bar \
  --top 240 --left 40 \
  --width 460 --height 300 \
  --view-name "收款类型分析" && \
python3 scripts/add_component.py \
  --screen-id 3654099936 \
  --model-id 2597080602 \
  --dimension-field paymentMethod \
  --indicator-field receivingAmount \
  --chart-type pie \
  --top 240 --left 1420 \
  --width 460 --height 300 \
  --view-name "收款类型占比" && \
python3 scripts/add_component.py \
  --screen-id 3654099936 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type line \
  --top 580 --left 40 \
  --width 860 --height 320 \
  --view-name "收款趋势分析" && \
python3 scripts/add_component.py \
  --screen-id 3654099936 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type bar \
  --top 240 --left 540 \
  --width 840 --height 300 \
  --view-name "项目收款排名"
```

### 步骤 6：查看和调整

```bash
# 查看大屏所有组件
python3 scripts/update_screen.py \
  --screen-id 3654099936 \
  --show-info

# 调整某个组件的位置
python3 scripts/update_screen.py \
  --screen-id 3654099936 \
  --uuid "grid-type:bar-uuid:1773817761165" \
  --top 250 --left 50
```

## 完整示例

### 需求：分析公司收款和付款情况

#### 1. 获取模型列表
```bash
python3 scripts/get_model_data.py --list
```

#### 2. 大模型分析后推荐模型
```json
{
  "selected_models": [
    {"id": 2597080602, "name": "收款登记模型 1219", "reason": "包含收款日期、收款金额、收款类型等字段"},
    {"id": 2537727927, "name": "付款申请", "reason": "包含申请日期、申请金额、实际支付金额等字段"},
    {"id": 2782975184, "name": "项目收付款情况", "reason": "同时包含收款金额和付款金额"}
  ]
}
```

#### 3. 获取模型详情
```bash
python3 scripts/get_model_data.py \
  --model-ids 2597080602 2537727927 2782975184 \
  --output scripts/.cache/models_info.json
```

#### 4. 大模型设计布局
```json
{
  "dashboard_name": "公司资金分析大屏",
  "components": [
    {
      "order": 1,
      "view_name": "累计收款",
      "chart_type": "metric",
      "model_id": 2597080602,
      "dimension_field": "",
      "indicator_field": "receivingAmount",
      "top": 80, "left": 40, "width": 260, "height": 120
    },
    {
      "order": 2,
      "view_name": "累计付款",
      "chart_type": "metric",
      "model_id": 2537727927,
      "dimension_field": "",
      "indicator_field": "applicationAmount",
      "top": 80, "left": 320, "width": 260, "height": 120
    },
    {
      "order": 3,
      "view_name": "收款类型分析",
      "chart_type": "bar",
      "model_id": 2597080602,
      "dimension_field": "paymentMethod",
      "indicator_field": "receivingAmount",
      "top": 240, "left": 40, "width": 460, "height": 300
    },
    ...
  ]
}
```

#### 5. 创建大屏
按上述 JSON 中的组件顺序，依次调用 `create_screen.py` 和 `add_component.py`。

## 优势

1. **充分利用大模型能力**: 模型选择、字段分析、布局设计都由大模型完成
2. **代码简洁**: 工具脚本只负责数据获取和 API 调用
3. **灵活可调整**: 可以随时让大模型重新设计或手动调整
4. **易于理解**: 每一步都有清晰的输入输出
5. **可复用**: 同样的工作流适用于不同的大屏需求

## 常用组件尺寸参考

| 组件类型 | 宽度 | 高度 | 说明 |
|---------|------|------|------|
| 指标卡 | 240-280 | 110-140 | 顶部展示关键指标 |
| 柱图/线图/饼图 | 440-480 | 270-320 | 标准图表尺寸 |
| 大图表 | 800-900 | 300-400 | 中间主图表 |
| 文本标题 | 400-500 | 24-30 | 图表标题栏 |

## 画布布局参考

```
1920 x 1080 画布

+--------------------------------------------------+
| 标题栏 (可选)                                     |
+--------------------------------------------------+
| [指标卡 1] [指标卡 2] [指标卡 3]                  |
| top:80     top:80     top:80                     |
| left:40    left:320   left:600                   |
+--------------------------------------------------+
| +------------+                    +------------+  |
| | 组件 1     |      中间大图表     | 组件 2     |  |
| | left:40    |      left:540     | left:1420  |  |
| | top:240    |      top:240      | top:240    |  |
| +------------+                    +------------+  |
+--------------------------------------------------+
| +-------------------+  +---------------------+   |
| | 底部组件 1        |  | 底部组件 2          |   |
| | left:40           |  | left:940            |   |
| | top:580           |  | top:580             |   |
| +-------------------+  +---------------------+   |
+--------------------------------------------------+
```

## 常见问题与解决方案

### 1. 组件重叠问题

**症状**: 两个或多个组件部分或完全重叠

**原因**:
- 组件坐标计算错误
- 组件尺寸过大
- 组件数量过多

**解决方案**:
1. 使用 `update_screen.py --show-info` 查看所有组件位置
2. 逐个调整重叠组件的 `top` 和 `left` 值
3. 如无法调整，考虑删除重复组件

**预防措施**:
- 创建前用纸笔或 Excel 规划布局
- 组件之间预留 10-20px 间距
- 1920×1080 画布建议 12-18 个组件

### 2. 指标卡数值显示不全

**症状**: 指标卡的数值被截断

**解决方案**: 增加高度到 130px
```bash
python3 scripts/update_screen.py \
  --screen-id 123 \
  --uuid "grid-type:metric-uuid:xxx" \
  --width 230 --height 130
```

### 3. 大屏留白过多

**症状**: 大屏有大片空白区域

**解决方案**:
1. 增加顶部指标卡数量（6-8 个）
2. 加大中间主图表（800-900 宽度）
3. 底部用 3 个柱图并排填满

### 4. 没有视觉焦点

**症状**: 所有组件一样大，看不出重点

**解决方案**: 创建大尺寸主图表（850×550）居中放置

---

## 参考文档

更多详细案例和实战经验，请查看：
- [实战案例](references/case_study.md) - 完整的问题解决过程
- [布局规划模板](references/layout_template.md) - 布局规划工具和模板
