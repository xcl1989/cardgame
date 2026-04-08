# 模型配置结构详解

## 完整模型配置示例

```json
{
  "modelDTO": {
    "name": "测试模型保存",
    "entCode": "jidianerlei_demo",
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
        },
        {
          "customVal": false,
          "datasetId": 2148783937,
          "datasetMetaId": 2148783937,
          "datasetName": "project3X",
          "disabled": 0,
          "entCode": "jidianerlei_demo",
          "fieldLabel": "编码",
          "fieldMetaId": 2148783937,
          "fieldName": "code",
          "fieldType": "Text",
          "id": 2148783941,
          "nativeType": "TEXT",
          "objId": 2148783941,
          "status": 0,
          "vector": 0
        },
        {
          "customVal": false,
          "datasetId": 2148783937,
          "datasetMetaId": 2148783937,
          "datasetName": "project3X",
          "disabled": 0,
          "entCode": "jidianerlei_demo",
          "fieldLabel": "版本",
          "fieldMetaId": 2148783937,
          "fieldName": "version",
          "fieldType": "Number",
          "id": 2148783945,
          "nativeType": "INT",
          "objId": 2148783945,
          "status": 0,
          "vector": 0
        }
      ]
    },
    {
      "modelTableType": "FACTS_TABLE",
      "datasetType": "TABLE",
      "datasetLabel": "收款登记",
      "datasetName": "collectionReg3X",
      "fields": [
        {
          "customVal": false,
          "datasetId": 2148797900,
          "datasetMetaId": 2148797900,
          "datasetName": "collectionReg3X",
          "disabled": 0,
          "entCode": "jidianerlei_demo",
          "fieldLabel": "项目编号",
          "fieldMetaId": 2148797900,
          "fieldName": "project",
          "fieldType": "Join",
          "id": 2148799149,
          "nativeType": "TEXT",
          "objId": 2148799149,
          "status": 0,
          "vector": 0
        }
      ]
    }
  ]
}
```

## 各部分详解

### 1. modelDTO - 模型基本信息

```json
{
  "name": "模型名称",
  "entCode": "企业编码",
  "std": 0
}
```

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| name | 是 | 模型名称 | "测试模型保存" |
| entCode | 是 | 企业编码 | "jidianerlei_demo" |
| std | 否 | 是否标准模型 | 0=否，1=是 |

### 2. modelRelationDTOList - 模型关系（节点关联）

定义节点之间的关联关系。

```json
{
  "sourceModelDataset": { ... },
  "targetModelDataset": { ... },
  "sourceField": { ... },
  "targetField": { ... },
  "relationType": "LEFT_JOIN",
  "to": "collectionReg3X",
  "from": "project3X",
  "entCode": "jidianerlei_demo"
}
```

**关键字段**:
- `sourceModelDataset`: 源节点（主表）信息
- `targetModelDataset`: 目标节点（外表）信息
- `sourceField`: 源节点的关联字段
- `targetField`: 目标节点的关联字段
- `relationType`: 关联类型，常用 `LEFT_JOIN`
- `to`: 目标节点名（datasetName）
- `from`: 源节点名（datasetName）

**数据集对象字段**:
```json
{
  "datasetId": 2148783937,
  "datasetLabel": "项目信息",
  "datasetName": "project3X",
  "datasetType": "TABLE",
  "modelTableType": "FACTS_TABLE",
  "entCode": "jidianerlei_demo",
  "key": "project3X",
  "name": "project3X",
  "label": "项目信息"
}
```

| 字段 | 来源 | 说明 |
|------|------|------|
| datasetId | 节点 API | 节点 ID |
| datasetLabel | 节点 API | 节点显示标签 |
| datasetName | 节点 API | 节点名称 |
| datasetType | 固定 | "TABLE" |
| modelTableType | 固定 | "FACTS_TABLE" |
| entCode | 配置 | 企业编码 |
| key | 同 name | 节点名称 |
| name | 同 datasetName | 节点名称 |
| label | 同 datasetLabel | 节点标签 |

**关联字段对象**:
```json
{
  "id": 2148783941,
  "fieldLabel": "编码",
  "fieldName": "code",
  "nativeType": "TEXT",
  "fieldType": "Text",
  "entCode": "jidianerlei_demo"
}
```

| 字段 | 来源 | 说明 |
|------|------|------|
| id | 字段 API | 字段 ID |
| fieldLabel | 字段 API | 字段标签 |
| fieldName | 字段 API | 字段名称 |
| nativeType | 字段 API | 原生类型 |
| fieldType | 字段 API | 字段类型 |
| entCode | 配置 | 企业编码 |

### 3. modelDatasetDTOList - 模型节点列表

定义模型包含的节点及每个节点选择的字段。

```json
{
  "modelTableType": "FACTS_TABLE",
  "datasetType": "TABLE",
  "datasetLabel": "项目信息",
  "datasetName": "project3X",
  "fields": [ ... ]
}
```

**字段对象** (fields 数组中的每个元素):
```json
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

| 字段 | 固定值/来源 | 说明 |
|------|-------------|------|
| customVal | false | 是否自定义值 |
| datasetId | 节点 ID | 数据集 ID |
| datasetMetaId | 同 datasetId | 数据集元 ID |
| datasetName | 节点名称 | 数据集名称 |
| disabled | 0 | 是否禁用 |
| entCode | 配置 | 企业编码 |
| fieldLabel | 字段 API | 字段标签 |
| fieldMetaId | 同 datasetId | 字段元 ID |
| fieldName | 字段 API | 字段名称 |
| fieldType | 字段 API | 字段类型 |
| id | 字段 ID | 字段 ID |
| nativeType | 字段 API | 原生类型 |
| objId | 同 id | 对象 ID |
| status | 0 | 状态 |
| vector | 0 | 向量标识 |

## 字段映射规则

从节点 API 获取字段后，映射到 modelDatasetDTOList 的 fields 数组：

```
API 字段          → 配置字段
id               → id, objId
fieldLabel       → fieldLabel
fieldName        → fieldName
fieldType        → fieldType
nativeType       → nativeType
datasetId        → datasetId, datasetMetaId, fieldMetaId
datasetName      → datasetName
(entCode 配置)   → entCode
(固定值)         → customVal=false, disabled=0, status=0, vector=0
```

## 关联关系建立规则

1. **确定主表和外表**: 通常业务主体为主表（如项目），相关业务为外表（如收款）
2. **查找关联字段**: 
   - 主表：通常使用编码字段（code）
   - 外表：通常使用引用字段（如 project，类型为 Join）
3. **设置 relationType**: 通常为 `LEFT_JOIN`
4. **设置 to/from**: to=外表名，from=主表名

## 更新模型时的额外字段

更新模型时，modelDTO 需要包含额外信息：

```json
{
  "id": 3654347769,
  "version": 1,
  "createdBy": "2534969263",
  "createdOn": 1773884802447,
  "updatedBy": "2534969263",
  "updatedOn": 1773884802447,
  "status": 0,
  "aiUse": 0
}
```

这些字段从已有模型信息或创建响应中获取。
