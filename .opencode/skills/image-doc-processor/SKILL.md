---
name: image-doc-processor
description: 分析用户上传的身份证件或合同图片，根据用户选择录入系统或单纯分析。图片数据从 MySQL 数据库获取，Token 从 Redis 获取。
license: Proprietary
---

# 图片文档处理器

## 概述

当用户上传身份证件或合同图片时，此技能会：
1. 识别图片类型（身份证/合同/其他）
2. **判断用户意图**：
   - 如果用户在上传时已明确表达意图（如"帮我录入这个身份证"或"分析一下这张图片"），**直接按用户要求执行**，不要再次询问
   - 如果用户意图不明确，**直接询问用户选择**：录入系统 或 单纯分析
3. 如选择录入，从数据库获取最新一条图片数据
4. 从 Redis 获取 Token
5. 调用 API 创建单据

## 完整工作流程

```
步骤 1: 用户上传图片 → 存入数据库 conversation_images 表
       ↓
步骤 2: 大模型分析图片，判断类型
       ├─ 身份证 → 继续
       ├─ 合同   → 继续
       └─ 其他   → 告知用户不支持，结束
       ↓
步骤 3: 判断用户意图
       ├─ 用户已明确要录入 → 步骤 4（直接执行录入）
       ├─ 用户已明确只分析 → 直接返回分析结果，结束
       └─ 用户意图不明确 → 直接询问用户选择
           ├─ 录入系统 → 步骤 4
           └─ 单纯分析 → 直接返回分析结果，结束
       ↓
步骤 4: 从对话上下文获取图片分析内容
       （姓名、身份证号、合同名称等）
       ↓
步骤 5: 从 MySQL 数据库查询最新一条图片数据
       ↓
步骤 6: 从 Redis 获取 Token
       ↓
步骤 7: 调用 API 创建单据
       ↓
步骤 8: 返回录入结果
```

## 图片类型判断

### 身份证件
识别字段：姓名、性别、出生日期、身份证号、住址

### 合同文档
识别字段：合同名称、甲方、乙方、金额、日期、条款

### 其他图片
告知用户："抱歉，我目前只支持身份证和合同图片的处理。"

## 数据源配置

### MySQL 数据库（图片数据）
**连接信息:**
- 主机：`127.0.0.1`
- 端口：`3306`
- 用户：`root`
- 密码：`12345678`
- 数据库：`ANALYSE`

**表结构:**
```sql
CREATE TABLE conversation_images (
  id INT,
  message_id BIGINT,
  filename VARCHAR(255),
  mime_type VARCHAR(50),
  base64_data LONGTEXT,
  size INT,
  created_at TIMESTAMP
);
```

**查询方式:**
```sql
SELECT * FROM conversation_images
ORDER BY created_at DESC
LIMIT 1
```

### Redis（Token 数据）
**连接信息:**
- 主机：`localhost`
- 端口：`6379`
- Key：`user:admin:tokens`
- 数据类型：Set

**获取方式:**
```python
token = redis_client.smembers("user:admin:tokens").pop()
```

## 业务系统 API

### 创建用户信息
**接口**: `POST http://127.0.0.1:8000/api/person`

**请求体**:
```json
{
  "name": "姓名",
  "birth_date": "YYYY-MM-DD",
  "gender": "男/女",
  "address": "住址",
  "id_card": "身份证号",
  "photo_base64": "base64 图片",
  "photo_filename": "文件名"
}
```

### 创建合同信息
**接口**: `POST http://127.0.0.1:8000/api/contract`

**请求体**:
```json
{
  "contract_name": "合同名称",
  "party_a": "甲方",
  "party_b": "乙方",
  "amount": 合同金额，
  "remarks": "备注",
  "photo_base64": "base64 图片",
  "photo_filename": "文件名"
}
```

## 资源

- `scripts/process_db_image.py` - 从数据库获取最新图片并调用 API

## 使用方法

### 大模型工作流示例

**场景 1：用户明确要求录入系统**

```
用户：[上传身份证图片] 帮我录入这个身份证

助手：好的，这是一张居民身份证（姓名：xxx，身份证号：xxx）。
     正在为您录入系统...
     [从上下文获取提取的身份证信息]
     [运行脚本：python3 process_db_image.py --data '{...}']

助手：✅ 已成功录入系统，用户 ID: 3
```

**场景 2：用户明确要求只分析**

```
用户：[上传合同图片] 分析一下这份合同

助手：好的，这是一份销售合同，主要信息如下：
     - 合同名称：xxx
     - 甲方：xxx
     - 乙方：xxx
     - 金额：xxx
     （不调用 API，直接返回分析结果）
```

**场景 3：用户意图不明确**

```
用户：[上传身份证图片]

助手：这是一张居民身份证，您希望如何处理？
     请选择：
     - 录入系统（将信息保存到业务系统）
     - 单纯分析（仅提取信息，不保存）

用户：录入系统

助手：好的，正在处理...
     [从上下文获取提取的身份证信息]
     [运行脚本：python3 process_db_image.py --data '{...}']

助手：✅ 已成功录入系统，用户 ID: 3
```

### 命令行调用

```bash
cd .opencode/skills/image-doc-processor

# 录入身份证信息
python3 scripts/process_db_image.py \
  --data '{"name":"韦小宝","birth_date":"1654-12-20","gender":"男","address":"北京市东城区景山前街 4 号紫禁城敬事房","id_card":"11204416541220243X"}'

# 录入合同信息
python3 scripts/process_db_image.py \
  --data '{"contract_name":"销售合同","party_a":"甲方公司","party_b":"乙方公司","amount":100000}'
```

## 示例输出

```
2026-03-11 10:30:00 - INFO - 成功获取图片：id_card.png
2026-03-11 10:30:00 - INFO - 成功获取 Token
2026-03-11 10:30:00 - INFO - 调用用户信息 API: http://127.0.0.1:8000/api/person
2026-03-11 10:30:01 - INFO - 用户信息 API 调用成功
{
  "success": true,
  "status_code": 200,
  "data": {
    "success": true,
    "data": {"id": 3},
    "error": null
  }
}
```

## 工具使用限制

**重要：** 使用此技能时，请遵守以下限制：

| 工具 | 是否允许 | 说明 |
|------|----------|------|
| `bash` | ✅ 允许 | 用于执行 Python 脚本 |
| `question` | ❌ 禁用 | 不要使用，直接询问用户 |
| `write` | ❌ 禁止 | 不得修改任何脚本文件 |
| `edit` | ❌ 禁止 | 不得修改任何脚本文件 |

### 正确使用示例
```bash
# ✓ 通过参数传入并运行脚本
python3 scripts/process_db_image.py --data '{...}'
```

### 错误使用示例
```
✗ 使用 write 工具修改脚本
✗ 使用 edit 工具修改脚本
✗ 使用 question 工具（应该直接询问用户）
```

## 错误处理

脚本会处理以下常见错误：
- 数据库连接失败
- 图片数据不存在（表为空）
- Redis 连接失败
- Token 获取失败（Key 不存在）
- API 调用失败

所有错误通过日志输出，失败时返回非零退出码。

## 依赖安装

```bash
pip install pymysql redis requests
```
