# 业务系统 API 接口规范

## 基础信息

- Base URL: `http://127.0.0.1:8000`
- 认证方式：Bearer Token
- 数据格式：JSON

## 接口列表

### 1. 创建用户信息

**接口**: `POST /api/person`

**请求体**:
```json
{
  "name": "张三",
  "birth_date": "1990-01-15",
  "gender": "男",
  "address": "北京市朝阳区 XX 街道 XX 号",
  "id_card": "110101199001151234",
  "photo_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "photo_filename": "id_card.jpg"
}
```

### 2. 创建合同信息

**接口**: `POST /api/contract`

**请求体**:
```json
{
  "contract_name": "产品销售合同",
  "party_a": "北京科技有限公司",
  "party_b": "上海贸易有限公司",
  "amount": 150000.00,
  "remarks": "首批货物交付期限为 30 天",
  "photo_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "photo_filename": "contract_001.jpg"
}
```

## 使用流程

1. **分析图片** - 大模型直接分析图片内容
2. **判断类型** - 身份证 or 合同
3. **提取信息** - 按对应格式提取字段
4. **获取 Token** - 从 Redis (`user:admin:tokens`)
5. **调用 API** - 发送请求

## 提示词模板

### 身份证识别提示词

```
请分析这张图片：

1. 判断是否为中华人民共和国居民身份证
2. 如果是，提取以下信息并以 JSON 格式返回：
{
  "name": "姓名",
  "birth_date": "出生年月日，格式 YYYY-MM-DD",
  "gender": "性别",
  "address": "住址",
  "id_card": "公民身份号码"
}

只返回 JSON 数据，不要其他内容。
```

### 合同识别提示词

```
请分析这张图片：

1. 判断是否为商业合同文档
2. 如果是，提取以下信息并以 JSON 格式返回：
{
  "contract_name": "合同名称",
  "party_a": "甲方名称",
  "party_b": "乙方名称",
  "amount": 合同金额（数字）,
  "remarks": "备注或重要条款"
}

只返回 JSON 数据，不要其他内容。
```
