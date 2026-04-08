# API Reference

数据模型相关 API 接口文档

## 基础 URL

```
https://dev.cloud.hecom.cn/biserver//paas
```

## 公共请求头

所有接口都需要以下请求头：

```
Content-Type: application/json
accessToken: <用户认证令牌>
empCode: <员工编码>
entCode: <企业编码>
uid: <用户 ID>
app: <应用标识>
act: <操作标识>
clientTag: web
```

## 1. 获取节点列表

### 接口

```
POST /bi-app/dataset/list
```

### 请求体

```json
{
  "datasetType": "TABLE"
}
```

`datasetType` 可选值：
- `TABLE`: 表格类型节点
- `BIZ_TYPE`: 业务类型节点
- `OPTION`: 选项类型节点

### 响应结构

```json
{
  "code": 0,
  "data": [
    {
      "datasetId": 2148783937,
      "datasetLabel": "项目信息",
      "datasetName": "project3X",
      "datasetType": "TABLE",
      "fields": [
        {
          "id": 2148783939,
          "fieldLabel": "项目编号",
          "fieldName": "name",
          "fieldType": "Text",
          "nativeType": "TEXT"
        },
        {
          "id": 2148783941,
          "fieldLabel": "编码",
          "fieldName": "code",
          "fieldType": "Text",
          "nativeType": "TEXT"
        }
      ]
    }
  ]
}
```

### 字段说明

**数据集对象**:
| 字段 | 类型 | 说明 |
|------|------|------|
| datasetId | number | 数据集 ID |
| datasetLabel | string | 数据集显示标签 |
| datasetName | string | 数据集名称（用于代码引用） |
| datasetType | string | 数据集类型 |
| fields | array | 字段列表 |

**字段对象**:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | number | 字段 ID |
| fieldLabel | string | 字段显示标签 |
| fieldName | string | 字段名称（用于代码引用） |
| fieldType | string | 字段类型（Text/Number/Date/Join 等） |
| nativeType | string | 原生数据类型（TEXT/INT/DATE 等） |

## 2. 保存数据模型

### 接口

```
POST /app/dataModel/operation/saveModelAll
```

### 请求头

```
app: dataModel
act: operation
```

### 请求体结构

```json
{
  "modelDTO": {
    "name": "模型名称",
    "entCode": "企业编码",
    "std": 0
  },
  "modelRelationDTOList": [
    {
      "sourceModelDataset": {
        "datasetId": 2148783937,
        "datasetLabel": "项目信息",
        "datasetName": "project3X",
        "datasetType": "TABLE",
        "modelTableType": "FACTS_TABLE",
        "entCode": "jidianerlei_demo",
        "key": "project3X",
        "name": "project3X",
        "label": "项目信息"
      },
      "targetModelDataset": {
        "datasetId": 2148797900,
        "datasetLabel": "收款登记",
        "datasetName": "collectionReg3X",
        "datasetType": "TABLE",
        "modelTableType": "FACTS_TABLE",
        "entCode": "jidianerlei_demo",
        "key": "collectionReg3X",
        "name": "collectionReg3X",
        "label": "收款登记"
      },
      "sourceField": {
        "id": 2148783941,
        "fieldLabel": "编码",
        "fieldName": "code",
        "nativeType": "TEXT",
        "fieldType": "Text",
        "entCode": "jidianerlei_demo"
      },
      "targetField": {
        "id": 2148799149,
        "fieldLabel": "项目编号",
        "fieldName": "project",
        "nativeType": "TEXT",
        "fieldType": "Join",
        "entCode": "jidianerlei_demo"
      },
      "relationType": "LEFT_JOIN",
      "to": "collectionReg3X",
      "from": "project3X",
      "entCode": "jidianerlei_demo"
    }
  ],
  "modelDatasetDTOList": [
    {
      "modelTableType": "FACTS_TABLE",
      "datasetType": "TABLE",
      "datasetLabel": "项目信息",
      "datasetName": "project3X",
      "fields": [
        {
          "customVal": false,
          "datasetId": 2148783937,
          "datasetMetaId": 2148783937,
          "datasetName": "project3X",
          "disabled": 0,
          "entCode": "jidianerlei_demo",
          "fieldLabel": "项目编号",
          "fieldMetaId": 2148783937,
          "fieldName": "name",
          "fieldType": "Text",
          "id": 2148783939,
          "nativeType": "TEXT",
          "objId": 2148783939,
          "status": 0,
          "vector": 0
        }
      ]
    }
  ]
}
```

### 请求体说明

**modelDTO**: 模型基本信息
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 模型名称 |
| entCode | string | 是 | 企业编码 |
| std | number | 否 | 是否标准模型（0/1） |

**modelRelationDTOList**: 模型关系列表（节点间关联）
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sourceModelDataset | object | 是 | 源节点信息 |
| targetModelDataset | object | 是 | 目标节点信息 |
| sourceField | object | 是 | 源关联字段 |
| targetField | object | 是 | 目标关联字段 |
| relationType | string | 是 | 关联类型（LEFT_JOIN 等） |
| to | string | 是 | 目标节点名 |
| from | string | 是 | 源节点名 |

**modelDatasetDTOList**: 模型节点列表
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| modelTableType | string | 是 | 表类型（FACTS_TABLE） |
| datasetType | string | 是 | 数据集类型 |
| datasetLabel | string | 是 | 数据集标签 |
| datasetName | string | 是 | 数据集名称 |
| fields | array | 是 | 选择的字段列表 |

### 响应

```json
{
  "code": 0,
  "data": {
    "id": 3654347769,
    "name": "测试模型保存",
    "version": 1
  },
  "message": "success"
}
```

## 4. 更新数据模型

### 接口

```
POST /app/dataModel/operation/updateModelAll
```

### 请求体

与 saveModelAll 相同，但 modelDTO 中需要包含：
- `id`: 模型 ID
- `version`: 模型版本号
- `createdBy`: 创建人
- `createdOn`: 创建时间
- `updatedBy`: 更新人
- `updatedOn`: 更新时间

示例：

```json
{
  "modelDTO": {
    "id": 3654347769,
    "name": "测试模型保存",
    "version": 1,
    "entCode": "jidianerlei_demo",
    "createdBy": "2534969263",
    "createdOn": 1773884802447,
    "updatedBy": "2534969263",
    "updatedOn": 1773884802447,
    "std": 0,
    "status": 0,
    "aiUse": 0
  }
}
```

## 3. 获取模型详情

### 接口

```
POST /app/dataModel/operation/getModelDetail/{model_id}
```

### 请求头

```
app: dataModel
act: operation
```

### 请求体

```json
{
  "id": "3654364378"
}
```

### 响应结构

```json
{
  "code": 0,
  "data": {
    "id": 3654364378,
    "name": "模型名称",
    "entCode": "jidianerlei_demo",
    "version": 1,
    "status": 0,
    "createdBy": "2534969263",
    "createdOn": 1773884802447,
    "updatedBy": "2534969263",
    "updatedOn": 1773884802447,
    "std": 0,
    "aiUse": 0,
    "modelDatasetDTOList": [
      {
        "datasetId": 2148783937,
        "datasetLabel": "项目信息",
        "datasetName": "project3X",
        "datasetType": "TABLE",
        "fields": [
          {
            "id": 2148783939,
            "fieldLabel": "项目编号",
            "fieldName": "name",
            "fieldType": "Text",
            "nativeType": "TEXT"
          }
        ]
      }
    ],
    "modelRelationDTOList": [
      {
        "from": "project3X",
        "to": "invoiceReg3X",
        "sourceField": {
          "fieldName": "code",
          "fieldType": "Text"
        },
        "targetField": {
          "fieldName": "project",
          "fieldType": "Join"
        },
        "relationType": "LEFT_JOIN"
      }
    ]
  },
  "message": "success"
}
```

### 响应说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | number | 模型 ID |
| name | string | 模型名称 |
| entCode | string | 企业编码 |
| version | number | 版本号 |
| status | number | 状态（0-草稿，1-发布） |
| createdOn | number | 创建时间（毫秒时间戳） |
| updatedOn | number | 更新时间（毫秒时间戳） |
| modelDatasetDTOList | array | 节点列表（包含字段信息） |
| modelRelationDTOList | array | 关联关系列表 |

## 错误码

| code | 说明 |
|------|------|
| 0 | 成功 |
| 非 0 | 失败，查看 message 字段 |

## 示例参考

查看项目中的示例文件：
- [createmodel.curl](../../createmodel.curl) - 创建模型示例
- [updatemodel.curl](../../updatemodel.curl) - 更新模型示例
