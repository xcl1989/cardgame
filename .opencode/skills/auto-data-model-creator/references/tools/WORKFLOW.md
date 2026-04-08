# 智能工作流

利用大模型能力自动设计和创建数据模型

## 工作流概览

传统方式创建模型需要：
1. 手动查找可用节点
2. 逐个查看节点字段
3. 设计关联关系
4. 编写配置命令

智能工作流让大模型帮你完成：
1. ✅ 智能分析需求
2. ✅ 自动选择节点
3. ✅ 推荐字段组合
4. ✅ 设计关联关系

## 完整工作流

### 步骤 1: 获取所有节点列表

```bash
python3 scripts/get_nodes.py --list
```

**输出示例**：
```
已保存 50 个节点到 scripts/.cache/nodes_list.json
前 20 个节点:
  ID: 2148783937, 名称：项目信息 (project3X), 字段数：15
  ID: 2148797900, 名称：收款登记 (collectionReg3X), 字段数：12
  ID: 2537727927, 名称：付款申请 (paymentApply3X), 字段数：18
  ID: 2782975184, 名称：合同管理 (contract3X), 字段数：20
  ...
```

### 步骤 2: 让大模型推荐节点

将步骤 1 的输出复制给大模型，使用以下提示词：

```
用户需求：分析公司项目收款情况

从以下 50 个节点中选择最相关的 3-5 个节点，并说明理由：

[粘贴节点列表]

请返回：
1. 推荐的节点列表（包含节点名称和 datasetName）
2. 每个节点应该包含的字段（3-5 个关键字段）
3. 节点间的关联关系建议
```

**大模型返回示例**：
```
根据您的需求，推荐以下节点：

1. 项目信息 (project3X) - 主表
   推荐字段：name(项目编号), code(编码), manager(项目经理), startDate(开始日期)

2. 收款登记 (collectionReg3X) - 关联表
   推荐字段：project(项目编号), amount(金额), date(收款日期), method(收款方式)

3. 合同管理 (contract3X) - 关联表
   推荐字段：code(合同编号), name(合同名称), amount(合同金额), projectCode(项目编码)

关联关系：
- project3X.code → collectionReg3X.project (LEFT_JOIN)
- project3X.code → contract3X.projectCode (LEFT_JOIN)
```

### 步骤 3: 获取推荐节点的详细信息

```bash
python3 scripts/get_nodes.py \
  --node-ids 2148783937 2148797900 2782975184 \
  --output scripts/.cache/nodes_info.json
```

**输出示例**：
```
✓ 已获取节点 2148783937 的详细信息
✓ 已获取节点 2148797900 的详细信息
✓ 已获取节点 2782975184 的详细信息
已保存 3 个节点的详细信息到 scripts/.cache/nodes_info.json
```

### 步骤 4: 让大模型设计模型结构

打开缓存文件，查看节点详情：

```bash
cat scripts/.cache/nodes_info.json
```

将内容复制给大模型，使用以下提示词：

```
根据以下 3 个节点的详细字段信息，设计一个数据模型配置方案

用户需求：分析公司项目收款情况，包含项目基本信息、收款情况和合同情况

请返回：
1. 模型名称建议
2. 每个节点的具体字段选择（使用 fieldName）
3. 完整的关联关系配置（使用 fieldName）
4. 返回 JSON 格式的模型配置（可选）

节点信息：
[粘贴 nodes_info.json 内容]
```

**大模型返回示例**：
```
模型设计方案：

模型名称：项目经营分析模型

节点配置：
1. project3X (主表)
   字段：name, code, manager, startDate

2. collectionReg3X (关联表)
   字段：project, amount, date, method

3. contract3X (关联表)
   字段：code, name, amount, projectCode

关联关系：
- project3X.code → collectionReg3X.project
- project3X.code → contract3X.projectCode

创建命令：
python3 scripts/create_model.py create \
  --name "项目经营分析模型" \
  --nodes "project3X:name,code,manager,startDate;collectionReg3X:project,amount,date,method;contract3X:code,name,amount,projectCode" \
  --relation "project3X.code:collectionReg3X.project"
```

### 步骤 5: 创建模型

根据大模型的设计方案，执行创建命令：

```bash
# 方式一：一次性创建完整模型
python3 scripts/create_model.py create \
  --name "项目经营分析模型" \
  --nodes "project3X:name,code,manager,startDate;collectionReg3X:project,amount,date,method;contract3X:code,name,amount,projectCode" \
  --relation "project3X.code:collectionReg3X.project"
```

或者分步创建：

```bash
# 步骤 1：创建基础模型（主表）
python3 scripts/create_model.py create \
  --name "项目经营分析模型" \
  --nodes "project3X:name,code,manager,startDate"

# 步骤 2：添加收款节点
python3 scripts/add_node.py \
  --model-id 3654347769 \
  --node-name collectionReg3X \
  --fields project,amount,date,method \
  --relation "project3X.code:collectionReg3X.project" && \

# 步骤 3：添加合同节点
python3 scripts/add_node.py \
  --model-id 3654347769 \
  --node-name contract3X \
  --fields code,name,amount,projectCode \
  --relation "project3X.code:contract3X.projectCode"
```

### 步骤 6: 验证和调整

```bash
# 查看模型详情
python3 scripts/get_model_data.py \
  --model-id 3654347769 \
  --show-info

# 如需调整，添加或删除字段
python3 scripts/update_model.py \
  --model-id 3654347769 \
  --add-fields "project3X:endDate"
```

## 智能提示词模板

### 节点选择提示词

```
你是一个数据模型设计专家。请根据用户需求，从可用节点列表中选择最相关的节点。

用户需求：{用户需求描述}

可用节点列表：
{节点列表}

请返回：
1. 推荐的节点（3-5 个），包含节点名称和 datasetName
2. 选择理由
3. 每个节点推荐 3-5 个关键字段
4. 节点间的关联关系建议
```

### 字段设计提示词

```
你是一个数据模型设计专家。请根据节点详细信息，设计完整的数据模型配置。

用户需求：{用户需求描述}

节点详细信息：
{节点详情 JSON}

请返回：
1. 模型名称建议
2. 每个节点的具体字段选择（使用 fieldName）
3. 完整的关联关系配置
4. 可直接执行的创建命令
```

### 配置生成提示词

```
你是一个数据模型配置专家。请根据以下信息生成完整的模型配置 JSON。

模型名称：{模型名称}
节点配置：{节点配置}
关联关系：{关联关系}

节点字段详情：
{字段详情}

请返回完整的 saveModelAll 接口请求体 JSON，包含：
- modelDTO
- modelRelationDTOList
- modelDatasetDTOList
```

## 优势对比

| 方面 | 传统方式 | 智能工作流 |
|------|---------|-----------|
| 节点选择 | 用户手动查找，可能遗漏 | 大模型全面分析，智能推荐 |
| 字段分析 | 逐个查看节点，耗时 | 批量分析，快速理解 |
| 关联设计 | 用户经验判断 | 大模型基于字段类型智能匹配 |
| 配置编写 | 手动编写，易出错 | 自动生成，格式正确 |
| 灵活性 | 固定规则 | 灵活调整，支持复杂需求 |
| 学习成本 | 需要了解所有节点 | 无需预先了解 |
| 代码量 | 较多 | 极少 |

## 实战案例

### 案例 1：创建财务管理模型

**用户需求**：分析公司收款付款情况，包含合同信息

**智能工作流执行**：

```bash
# 1. 获取节点列表
python3 scripts/get_nodes.py --list

# 2. 大模型推荐节点
# 推荐：收款登记、付款申请、合同管理、项目信息

# 3. 获取节点详情
python3 scripts/get_nodes.py \
  --node-ids 2148797900 2537727927 2782975184 2148783937 \
  --output scripts/.cache/nodes_info.json

# 4. 大模型设计模型结构
# 返回完整设计方案

# 5. 执行创建
python3 scripts/create_model.py create \
  --name "财务经营管理模型" \
  --nodes "..." \
  --relation "..."
```

### 案例 2：快速原型设计

**用户需求**：先创建一个简单的收款分析模型看看效果

**快速执行**：
```bash
# 直接用智能工作流生成配置
# 大模型根据经验推荐最简配置

# 创建最小可行模型
python3 scripts/create_model.py create \
  --name "收款分析原型" \
  --nodes "project3X:name,code;collectionReg3X:project,amount" \
  --relation "project3X.code:collectionReg3X.project"
```

## 最佳实践

### 1. 从简单开始

先用智能工作流创建基础模型，再逐步完善：

```bash
# 第一步：创建简单模型
python3 scripts/create_model.py create \
  --name "收款分析" \
  --nodes "project3X:name,code;collectionReg3X:project,amount" \
  --relation "project3X.code:collectionReg3X.project"

# 第二步：根据使用反馈添加字段
python3 scripts/update_model.py \
  --model-id 3654347769 \
  --add-fields "collectionReg3X:date,method,payee"
```

### 2. 迭代优化

让大模型基于已有模型提供优化建议：

```
当前模型配置：
{模型详情}

用户需求变化：需要增加付款分析

请提供优化建议：
1. 需要添加哪些节点？
2. 如何建立关联关系？
3. 具体的添加命令
```

### 3. 保存设计方案

将大模型的设计方案保存到缓存目录：

```bash
# 保存设计方案
cat > scripts/.cache/design_proposal.json << 'EOF'
{
  "name": "项目经营分析模型",
  "nodes": [...],
  "relations": [...],
  "createdBy": "AI Assistant",
  "createdAt": "2026-03-19"
}
EOF
```

## 常见问题

### Q: 大模型推荐的字段不存在怎么办？

A: 使用 `get_nodes.py` 获取详细字段列表，让大模型基于真实字段重新推荐

### Q: 如何验证大模型的设计方案？

A: 先用 `create_model.py` 创建测试模型，查看效果后再正式使用

### Q: 可以同时使用多个大模型吗？

A: 可以！可以用不同大模型分别做节点选择、字段设计、配置生成，对比优化

## 下一步

- 📖 [快速开始](QUICKSTART.md) - 手动创建模型指南
- 🔧 [命令速查](QUICK_REFERENCE.md) - 所有命令参考
- ❓ [常见问题](FAQ.md) - 问题解决
