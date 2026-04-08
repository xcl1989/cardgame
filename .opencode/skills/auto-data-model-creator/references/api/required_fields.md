# 必填字段说明

本文档说明模型配置中各对象的必填字段。

## modelDTO（模型基本信息）

### 创建模型时必填

```json
{
  "name": "模型名称",        // 必填
  "entCode": "企业编码",    // 必填
  "std": 0                  // 可选，默认 0
}
```

### 更新模型时必填

```json
{
  "id": 3654347769,         // 必填，模型 ID
  "version": 1,             // 必填，版本号
  "name": "模型名称",        // 必填
  "entCode": "企业编码",    // 必填
  "createdBy": "2534969263",   // 必填，创建人
  "createdOn": 1773884802447,  // 必填，创建时间
  "updatedBy": "2534969263",   // 必填，更新人
  "updatedOn": 1773884802447,  // 必填，更新时间
  "status": 0,              // 必填，状态
  "std": 0,                 // 可选
  "aiUse": 0                // 可选
}
```

## modelRelationDTOList（关联关系）

### 关联关系对象

```json
{
  "sourceModelDataset": {   // 必填
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
  "targetModelDataset": {   // 必填
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
  "sourceField": {          // 必填
    "id": 2148783941,
    "fieldLabel": "编码",
    "fieldName": "code",
    "nativeType": "TEXT",
    "fieldType": "Text",
    "entCode": "jidianerlei_demo"
  },
  "targetField": {          // 必填
    "id": 2148799149,
    "fieldLabel": "项目编号",
    "fieldName": "project",
    "nativeType": "TEXT",
    "fieldType": "Join",
    "entCode": "jidianerlei_demo"
  },
  "relationType": "LEFT_JOIN",  // 必填
  "to": "collectionReg3X",      // 必填
  "from": "project3X",          // 必填
  "entCode": "jidianerlei_demo" // 必填
}
```

### 最小必填字段

实际上，以下字段是核心必填项：

```json
{
  "sourceModelDataset": {
    "datasetId": 2148783937,    // 必填
    "datasetName": "project3X",  // 必填
    "name": "project3X"          // 必填
  },
  "targetModelDataset": {
    "datasetId": 2148797900,     // 必填
    "datasetName": "collectionReg3X",  // 必填
    "name": "collectionReg3X"    // 必填
  },
  "sourceField": {
    "id": 2148783941,           // 必填
    "fieldName": "code"         // 必填
  },
  "targetField": {
    "id": 2148799149,           // 必填
    "fieldName": "project"      // 必填
  },
  "relationType": "LEFT_JOIN",  // 必填
  "to": "collectionReg3X",      // 必填
  "from": "project3X"           // 必填
}
```

## modelDatasetDTOList（模型节点）

### 节点对象

```json
{
  "modelTableType": "FACTS_TABLE",  // 必填
  "datasetType": "TABLE",           // 必填
  "datasetLabel": "项目信息",        // 必填
  "datasetName": "project3X",       // 必填
  "fields": [                       // 必填，至少包含一个字段
    {
      "customVal": false,           // 必填
      "datasetId": 2148783937,      // 必填
      "datasetMetaId": 2148783937,  // 必填
      "datasetName": "project3X",   // 必填
      "disabled": 0,                // 必填
      "entCode": "jidianerlei_demo",// 必填
      "fieldLabel": "项目编号",      // 必填
      "fieldMetaId": 2148783937,    // 必填
      "fieldName": "name",          // 必填
      "fieldType": "Text",          // 必填
      "id": 2148783939,             // 必填
      "nativeType": "TEXT",         // 必填
      "objId": 2148783939,          // 必填
      "status": 0,                  // 必填
      "vector": 0                   // 必填
    }
  ]
}
```

### 字段对象必填项

每个字段对象必须包含以下 14 个字段：

| 字段 | 类型 | 说明 | 来源 |
|------|------|------|------|
| customVal | boolean | 是否自定义值 | 固定 false |
| datasetId | number | 数据集 ID | 节点 API |
| datasetMetaId | number | 数据集元 ID | 同 datasetId |
| datasetName | string | 数据集名称 | 节点 API |
| disabled | number | 是否禁用 | 固定 0 |
| entCode | string | 企业编码 | 配置 |
| fieldLabel | string | 字段标签 | 字段 API |
| fieldMetaId | number | 字段元 ID | 同 datasetId |
| fieldName | string | 字段名称 | 字段 API |
| fieldType | string | 字段类型 | 字段 API |
| id | number | 字段 ID | 字段 API |
| nativeType | string | 原生类型 | 字段 API |
| objId | number | 对象 ID | 同 id |
| status | number | 状态 | 固定 0 |
| vector | number | 向量标识 | 固定 0 |

## 常见错误

### 1. 缺少必填字段

```json
// ❌ 错误：缺少 entCode
{
  "modelDTO": {
    "name": "模型名称"
  }
}

// ✅ 正确
{
  "modelDTO": {
    "name": "模型名称",
    "entCode": "企业编码"
  }
}
```

### 2. 字段对象不完整

```json
// ❌ 错误：缺少必需字段
{
  "fieldName": "name",
  "fieldLabel": "项目编号"
}

// ✅ 正确：包含所有 14 个必需字段
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
```

### 3. 关联关系字段缺失

```json
// ❌ 错误：缺少 to/from 字段
{
  "sourceModelDataset": {...},
  "targetModelDataset": {...},
  "sourceField": {...},
  "targetField": {...},
  "relationType": "LEFT_JOIN"
}

// ✅ 正确
{
  "sourceModelDataset": {...},
  "targetModelDataset": {...},
  "sourceField": {...},
  "targetField": {...},
  "relationType": "LEFT_JOIN",
  "to": "collectionReg3X",
  "from": "project3X",
  "entCode": "jidianerlei_demo"
}
```

## 快速检查清单

创建模型配置后，检查以下项目：

- [ ] modelDTO 包含 name 和 entCode
- [ ] modelRelationDTOList 中每个关联包含 sourceField、targetField、relationType、to、from
- [ ] modelDatasetDTOList 中每个节点包含 datasetName 和 fields 数组
- [ ] fields 数组中每个字段包含所有 14 个必需字段
- [ ] 更新模型时 modelDTO 包含 id、version、createdBy、createdOn、updatedBy、updatedOn
