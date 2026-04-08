---
name: auto-data-model-creator
description: 根据用户自然语言描述自动创建和更新数据模型。支持：(1) 解析用户需求自动选择表格/业务类型/选项节点，(2) 自动选择合适的字段，(3) 自动建立节点间关联关系，(4) 调用 saveModelAll/updateModelAll 接口执行创建或更新。当用户需要创建或修改数据模型时使用此 skill。
---

# 数据模型自动创建 (Auto Data Model Creator)

---

## 🎯 决策指引：用什么方式？

| 场景 | 方式 | 命令 |
|------|------|------|
| 用户需求明确（如"项目收款模型"） | **直接创建** | 一条 create 命令 |
| 用户不确定用什么节点 | 智能工作流 | 先 get_nodes 探索 |

---

## ⚡ 标准命令（需求明确时用这条）

```bash
# 创建模型
python3 scripts/create_model.py create \
  --name "模型名称" \
  --nodes "节点:字段1,字段2;节点2:字段1,字段2" \
  --relation "主表.关联字段:外表.关联字段"
```

**示例：创建项目收款模型**

```bash
python3 scripts/create_model.py create \
  --name "项目收款分析" \
  --nodes "project3X:name,code,projectType,biddingAmount;CustomObject181:field1,field2,field3" \
  --relation "project3X.code:CustomObject181.field1"
```

---

## 📋 命令速查

### 创建模型
```bash
python3 scripts/create_model.py create \
  --name "模型名称" \
  --nodes "节点:字段1,字段2" \
  --relation "主表.字段:外表.字段"
```

### 查看模型
```bash
python3 scripts/list_models.py list              # 列出所有模型
python3 scripts/list_models.py detail --model-id ID  # 查看模型详情
```

### 探索节点（需求不明确时）
```bash
python3 scripts/get_nodes.py list                # 获取所有节点
python3 scripts/get_nodes.py detail --node-ids ID1 ID2  # 获取节点详情
```

---

## 🔧 格式说明

### --nodes 参数格式
```
节点名:字段1,字段2,字段3
```
- 多节点用 `;` 分隔
- 字段名用 `,` 分隔

### --relation 参数格式
```
主表.主表关联字段:外表外表关联字段
```
- 只支持一个关联关系
- 关联类型固定为 LEFT_JOIN

---

## ⚠️ 重要限制

1. **一次只能创建一个关联关系** - 多节点多关联需要分步创建
2. **使用 fieldName 不是 fieldLabel** - 如 `code` 不是 `编码`

---

## 📚 常用节点速查

| 业务 | 节点名 | 主要字段 |
|------|--------|---------|
| 项目信息 | project3X | name, code, projectType, biddingAmount, field55__c(收入合同金额), field25__c(累计回款) |
| 工程款收款 | CustomObject181 | field1(项目ID), field2(到账金额), field3(到账日期) |
| 往来收款 | currentCollection3X | project(项目), receiptAmount(金额), paymentDate(日期) |
| 支出合同 | expContract3X | project, name, contractAmount, taxContractAmount |

---

## 🔄 完整工作流

### 场景A：需求明确（推荐）

用户说"创建项目收款模型"，直接执行：

```bash
python3 scripts/create_model.py create \
  --name "项目收款分析" \
  --nodes "project3X:name,code,projectType,biddingAmount,field55__c,field25__c;CustomObject181:field1,field2,field3" \
  --relation "project3X.code:CustomObject181.field1"
```

### 场景B：需求模糊

用户不确定用什么节点，先探索：

```bash
# 1. 获取节点列表
python3 scripts/get_nodes.py list

# 2. 查看节点详情
python3 scripts/get_nodes.py detail --node-ids 节点ID1 节点ID2

# 3. 根据详情创建模型
python3 scripts/create_model.py create \
  --name "xxx分析" \
  --nodes "..." \
  --relation "..."
```

---

## 认证配置

认证信息在 `scripts/header.json`：

```json
{
  "accessToken": "your-access-token",
  "entCode": "your-enterprise-code",
  "uid": "your-user-id",
  "empCode": "your-employee-code"
}
```

**获取方式**：浏览器 F12 → Network → 任意请求头

---

## 常见问题

| 错误 | 解决 |
|------|------|
| `accessToken 过期` | 重新登录，更新 header.json |
| `模型名称重复` | 使用唯一名称如 `项目收款_20260319` |
| `字段不存在` | 使用 fieldName，不是 fieldLabel |
| `配置有误` | 检查关联字段类型是否匹配（Text→Join） |

---

## 参考文档

- [QUICKSTART.md](references/tools/QUICKSTART.md) - 5分钟入门
- [WORKFLOW.md](references/tools/WORKFLOW.md) - 完整工作流
- [FAQ.md](references/tools/FAQ.md) - 常见问题
