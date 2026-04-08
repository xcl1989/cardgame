# 命令速查手册

快速参考所有可用命令

## 认证配置

```bash
# 编辑认证配置
vim scripts/header.json

# 示例配置
{
  "accessToken": "your-access-token",
  "entCode": "your-enterprise-code",
  "uid": "your-user-id",
  "empCode": "your-employee-code"
}
```

## 获取节点信息

```bash
# 获取所有节点列表
python3 scripts/get_nodes.py --list

# 获取节点详情
python3 scripts/get_nodes.py detail \
  --node-ids 2148783937 2148795131 \
  --output scripts/.cache/nodes_info.json

# 搜索节点（模糊匹配）
python3 scripts/get_nodes.py --search "开票"
```

## 获取模型信息

```bash
# 获取所有模型列表
python3 scripts/list_models.py --list

# 搜索模型（模糊匹配）
python3 scripts/list_models.py --search "开票"

# 查看模型详情
python3 scripts/list_models.py detail \
  --model-id 3654361441
```

## 创建模型

```bash
# 创建单节点模型
python3 scripts/create_model.py create \
  --name "模型名称" \
  --nodes "节点名：字段 1，字段 2"

# 创建多节点模型（带关联）
python3 scripts/create_model.py create \
  --name "项目开票模型" \
  --nodes "project3X:name,code;invoiceReg3X:project,name,invoiceCode" \
  --relation "project3X.code:invoiceReg3X.project"

# 指定企业编码（可选）
python3 scripts/create_model.py create \
  --name "模型名称" \
  --nodes "节点名：字段 1，字段 2" \
  --ent-code custom_ent_code
```

## 参数格式说明

### --nodes 参数

**格式**: `节点 1:字段 1，字段 2;节点 2:字段 1，字段 2`

**示例**:
```bash
--nodes "project3X:name,code,projectType;invoiceReg3X:project,name,invoiceCode,taxAmount"
```

**注意**:
- 使用分号 `;` 分隔不同节点
- 使用冒号 `:` 分隔节点名和字段列表
- 使用逗号 `,` 分隔多个字段
- 使用 **fieldName**（不是 fieldLabel）

### --relation 参数

**格式**: `源节点。源字段：目标节点。目标字段`

**示例**:
```bash
--relation "project3X.code:invoiceReg3X.project"
```

**注意**:
- 源节点 = 主表（如 project3X）
- 源字段 = Text 类型字段（如 code）
- 目标节点 = 关联表（如 invoiceReg3X）
- 目标字段 = Join 类型字段（如 project）

## 常用节点和字段

### 项目信息 (project3X)

| 字段名 | 字段标签 | 类型 | 用途 |
|--------|---------|------|------|
| name | 项目编号 | Text | 项目名称 |
| code | 编码 | Text | **用于关联** |
| projectType | 项目类别 | Join | 项目类型 |
| planStartDate | 计划开工日期 | Time | 开始时间 |
| planEndDate | 计划竣工日期 | Time | 结束时间 |

### 开票登记 (invoiceReg3X)

| 字段名 | 字段标签 | 类型 | 用途 |
|--------|---------|------|------|
| project | 项目编号 (ID) | Join | **用于关联** |
| name | 发票号码 | Text | 发票编号 |
| invoiceCode | 发票代码 | Text | 发票代码 |
| invoiceType | 发票类型 | Join | 发票类型 |
| invoiceDate | 开票日期 | Time | 开票时间 |
| taxAmount | 含税金额 | Number | 含税总额 |
| noTaxAmount | 无税金额 | Number | 不含税金额 |

### 收款登记 (collectionReg3X)

| 字段名 | 字段标签 | 类型 | 用途 |
|--------|---------|------|------|
| project | 项目编号 | Join | **用于关联** |
| amount | 收款金额 | Number | 收款总额 |
| date | 收款日期 | Time | 收款时间 |
| method | 支付方式 | Join | 支付方式 |

### 合同管理 (contract3X)

| 字段名 | 字段标签 | 类型 | 用途 |
|--------|---------|------|------|
| code | 合同编号 | Text | 合同编码 |
| name | 合同名称 | Text | 合同名称 |
| amount | 合同金额 | Number | 合同总额 |
| projectCode | 项目编码 | Text | **用于关联** |

## 典型场景命令

### 场景 1：简单项目模型

```bash
python3 scripts/create_model.py create \
  --name "项目基本信息" \
  --nodes "project3X:name,code,manager"
```

### 场景 2：项目开票关联模型

```bash
python3 scripts/create_model.py create \
  --name "项目开票分析" \
  --nodes "project3X:name,code,projectType;invoiceReg3X:project,name,taxAmount" \
  --relation "project3X.code:invoiceReg3X.project"
```

### 场景 3：项目收款关联模型

```bash
python3 scripts/create_model.py create \
  --name "项目收款分析" \
  --nodes "project3X:name,code,manager;collectionReg3X:project,amount,date" \
  --relation "project3X.code:collectionReg3X.project"
```

### 场景 4：项目合同关联模型

```bash
python3 scripts/create_model.py create \
  --name "项目合同分析" \
  --nodes "project3X:name,code;contract3X:code,name,amount,projectCode" \
  --relation "project3X.code:contract3X.projectCode"
```

### 场景 5：多节点经营分析模型

```bash
# 先创建基础模型
python3 scripts/create_model.py create \
  --name "经营分析模型" \
  --nodes "project3X:name,code,manager"

# 然后添加其他节点（需要 add_node.py 脚本）
# python3 scripts/add_node.py ...
```

## 帮助命令

```bash
# 查看脚本帮助
python3 scripts/create_model.py --help
python3 scripts/get_nodes.py --help
python3 scripts/list_models.py --help
```

## 缓存目录

所有缓存文件保存在 `scripts/.cache/` 目录：

- `nodes_list.json`: 节点列表
- `nodes_info_<ID>.json`: 节点详情
- `models_list.json`: 模型列表
- `models_info_<ID>.json`: 模型详情

**管理缓存**:
```bash
# 查看缓存
ls -la scripts/.cache/

# 清除缓存
rm scripts/.cache/*.json
```

## 注意事项

### ⚠️ 使用 fieldName

```bash
# ✅ 正确：使用 fieldName
--nodes "project3X:name,code"

# ❌ 错误：使用 fieldLabel
--nodes "project3X:项目编号，编码"
```

### ⚠️ 模型名称唯一

```bash
# ✅ 正确：添加日期后缀
--name "项目开票模型_20260319"

# ❌ 错误：可能重复
--name "项目开票模型"
```

### ⚠️ 关联字段类型匹配

```bash
# ✅ 正确：Text → Join
--relation "project3X.code:invoiceReg3X.project"

# ❌ 错误：类型不匹配
--relation "project3X.code:invoiceReg3X.code"
```

## 故障排查

### 问题：节点不存在

```bash
# 查看可用节点
python3 scripts/get_nodes.py --list

# 搜索节点
python3 scripts/get_nodes.py --search "开票"
```

### 问题：字段不存在

```bash
# 查看节点详情
python3 scripts/get_nodes.py detail --node-ids 2148783937
```

### 问题：认证失败

```bash
# 1. 检查 header.json 格式
cat scripts/header.json

# 2. 更新 accessToken
vim scripts/header.json

# 3. 重新测试
python3 scripts/get_nodes.py --list
```
