# 快速开始

5 分钟创建你的第一个数据模型

## 前置准备

### 1. 配置认证信息

编辑 `scripts/header.json` 文件，填入你的认证信息：

```json
{
  "accessToken": "your-access-token",
  "entCode": "your-enterprise-code",
  "uid": "your-user-id",
  "empCode": "your-employee-code"
}
```

**如何获取认证信息？**

从浏览器开发者工具中获取：
1. 打开系统网页
2. 按 F12 打开开发者工具
3. 切换到 Network 标签
4. 刷新页面，找到任意 API 请求
5. 查看请求头中的 `accessToken`、`entCode`、`uid`、`empCode`

或者从已有的 curl 文件中复制（如 `createmodel.curl`）

### 2. 验证配置

```bash
# 获取节点列表，验证认证是否有效
python3 scripts/get_nodes.py --list
```

如果看到节点列表（如 220 个节点），说明配置成功！

## 第一步：查看可用节点

```bash
# 获取所有表格类型节点
python3 scripts/get_nodes.py --list

# 输出示例：
# === 节点列表 (共 220 个) ===
# ID              名称                              类型        字段数
# ------------------------------------------------------------------------------------------
#                 计划明细 (CustomObject125)              TABLE        25
#                 支出合同 (expContract3X)                TABLE        94
#                 项目信息 (project3X)                    TABLE        89
#                 开票登记 (invoiceReg3X)                 TABLE        49
# ...
```

## 第二步：选择节点和字段

根据业务需求选择节点，例如创建一个"项目开票分析模型"：

**主表**: 项目信息 (project3X)
- 选择字段：name (项目编号), code (编码), projectType (项目类别), planStartDate (计划开工日期), planEndDate (计划竣工日期)

**关联表**: 开票登记 (invoiceReg3X)
- 选择字段：project (项目编号), name (发票号码), invoiceCode (发票代码), invoiceType (发票类型), invoiceDate (开票日期), taxAmount (含税金额), noTaxAmount (无税金额)

**关联关系**: project3X.code → invoiceReg3X.project

> **注意**: 使用 fieldName（如 `name`, `code`），不是 fieldLabel（如 `项目编号`, `编码`）

## 第三步：创建模型

### 方式一：单次创建（推荐新手）

```bash
python3 scripts/create_model.py create \
  --name "项目开票分析模型_20260319" \
  --nodes "project3X:name,code,projectType,planStartDate,planEndDate;invoiceReg3X:project,name,invoiceCode,invoiceType,invoiceDate,taxAmount,noTaxAmount" \
  --relation "project3X.code:invoiceReg3X.project"
```

**参数说明**：
- `--name`: 模型名称（必须唯一，建议添加日期）
- `--nodes`: 节点和字段配置，格式：`节点 1:字段 1，字段 2;节点 2:字段 1，字段 2`
- `--relation`: 关联关系，格式：`节点 1.字段：节点 2.字段`

**执行输出**：
```
🚀 开始创建模型：项目开票分析模型_20260319
📡 正在获取可用节点列表...
✓ 已加载 220 个节点
📋 模型配置:
   名称：项目开票分析模型_20260319
   节点：2 个
      - project3X: 5 个字段
      - invoiceReg3X: 7 个字段
   关联：project3X.code → invoiceReg3X.project
🔧 正在构建模型配置...
💾 正在保存模型...
✅ 模型创建成功！
   模型 ID: 3654361441
   包含节点：2 个
   关联关系：1 个
```

### 方式二：分步创建（推荐复杂场景）

#### 步骤 1：创建基础模型（单节点）

```bash
python3 scripts/create_model.py create \
  --name "项目管理模型" \
  --nodes "project3X:name,code,projectType,manager"
```

#### 步骤 2：添加关联节点

```bash
# 注意：add_node.py 脚本需要实现，目前建议使用单次创建方式
python3 scripts/add_node.py \
  --model-id 3654361441 \
  --node-name invoiceReg3X \
  --fields project,name,invoiceCode,taxAmount \
  --relation "project3X.code:invoiceReg3X.project"
```

## 第四步：查看模型

```bash
# 查看模型列表
python3 scripts/list_models.py --list

# 搜索模型
python3 scripts/list_models.py --search "开票"

# 查看模型详情
python3 scripts/list_models.py detail --model-id 3654361441
```

**输出示例**：
```
=== 模型详情 ===
ID: 3654361441
名称：项目开票分析模型_20260319
企业编码：jidianerlei_demo
版本：1

包含节点 (2 个):
  - 项目信息 (project3X): 5 个字段
  - 开票登记 (invoiceReg3X): 7 个字段

关联关系 (1 个):
  - project3X.code → invoiceReg3X.project (LEFT_JOIN)
```

## 第五步：更新模型（可选）

### 添加字段

```bash
# 注意：update_model.py 脚本需要实现
python3 scripts/update_model.py \
  --model-id 3654361441 \
  --add-fields "project3X:startDate,endDate;invoiceReg3X:buyerTaxpayerNumber"
```

### 修改模型名称

目前需要在系统中手动修改，或重新创建模型。

## 下一步

- 📖 [查看命令速查](QUICK_REFERENCE.md) - 所有命令快速参考
- 🧠 [智能工作流](WORKFLOW.md) - 利用大模型自动设计模型
- ❓ [常见问题](FAQ.md) - 问题解决指南

## 示例场景

### 场景 1：创建合同管理模型

```bash
python3 scripts/create_model.py create \
  --name "合同管理模型" \
  --nodes "contract3X:code,name,amount,signDate;project3X:code,name" \
  --relation "project3X.code:contract3X.projectCode"
```

### 场景 2：创建收款分析模型

```bash
python3 scripts/create_model.py create \
  --name "收款分析模型" \
  --nodes "project3X:name,code,manager;collectionReg3X:project,amount,date,method" \
  --relation "project3X.code:collectionReg3X.project"
```

### 场景 3：使用智能工作流

```bash
# 1. 获取节点列表
python3 scripts/get_nodes.py --list

# 2. 将输出复制给大模型，让它推荐节点
# 提示词："用户需求：分析公司项目开票情况。从以下 220 个节点中选择最相关的 2-3 个，并推荐字段和关联关系..."

# 3. 获取推荐节点的详情
python3 scripts/get_nodes.py \
  --node-ids 2148783937 2148795131 \
  --output scripts/.cache/nodes_info.json

# 4. 将节点详情给大模型设计模型
# 提示词："根据以下节点信息，设计一个数据模型，包含字段选择和关联关系..."

# 5. 根据设计方案创建模型
python3 scripts/create_model.py create \
  --name "智能推荐模型" \
  --nodes "..." \
  --relation "..."
```

## 参数格式详解

### --nodes 参数

格式：`节点 1:字段 1，字段 2，字段 3;节点 2:字段 1，字段 2`

示例：
```bash
--nodes "project3X:name,code,projectType;invoiceReg3X:project,name,invoiceCode,taxAmount"
```

**注意**:
- 使用分号 `;` 分隔不同节点
- 使用冒号 `:` 分隔节点名和字段列表
- 使用逗号 `,` 分隔同一节点的多个字段
- 使用 **fieldName**（不是 fieldLabel）

### --relation 参数

格式：`源节点。源字段：目标节点。目标字段`

示例：
```bash
--relation "project3X.code:invoiceReg3X.project"
```

**注意**:
- 源节点是主表（如 project3X）
- 源字段通常是 Text 类型的编码字段（如 code）
- 目标节点是关联表（如 invoiceReg3X）
- 目标字段通常是 Join 类型的引用字段（如 project）
- 使用英文句点 `.` 连接节点和字段
- 使用英文冒号 `:` 分隔源和目标

## 常用字段参考

### 项目信息 (project3X)

| 字段名 | 字段标签 | 类型 | 说明 |
|--------|---------|------|------|
| name | 项目编号 | Text | 项目名称 |
| code | 编码 | Text | 项目编码（用于关联） |
| projectType | 项目类别 | Join | 项目类型 |
| planStartDate | 计划开工日期 | Time | 计划开始时间 |
| planEndDate | 计划竣工日期 | Time | 计划结束时间 |

### 开票登记 (invoiceReg3X)

| 字段名 | 字段标签 | 类型 | 说明 |
|--------|---------|------|------|
| project | 项目编号 (ID) | Join | 关联项目（用于关联） |
| name | 发票号码 | Text | 发票编号 |
| invoiceCode | 发票代码 | Text | 发票代码 |
| invoiceType | 发票类型 | Join | 发票类型 |
| invoiceDate | 开票日期 | Time | 开票时间 |
| taxAmount | 含税金额 | Number | 含税总额 |
| noTaxAmount | 无税金额 | Number | 不含税金额 |

## 常见问题快速解决

### 问题：字段不存在

```
⚠️  警告：字段 xxx 不在节点 yyy 中
```

**解决**: 确保使用 fieldName，运行以下命令查看实际字段：
```bash
python3 scripts/get_nodes.py detail --node-ids 2148783937
```

### 问题：模型名称重复

```
保存失败：模型名称重复
```

**解决**: 添加日期后缀，如 `"项目开票模型_20260319"`

### 问题：认证失败

```
API 请求失败：401
```

**解决**: 更新 `scripts/header.json` 中的 accessToken

## 需要帮助？

- 查看 [完整文档](../SKILL.md)
- 查看 [常见问题](FAQ.md)
- 查看 [智能工作流](WORKFLOW.md) 使用大模型辅助设计
