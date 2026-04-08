# 必填字段说明 (Required Fields)

## dimension 字段结构 (32 个字段)

```json
{
  "customVal": false,
  "datasetId": 2148783937,
  "datasetMetaId": 2148783937,
  "datasetName": "project3X",
  "disabled": 0,
  "entCode": "jidianerlei_demo",
  "fieldLabel": "项目名称",
  "fieldMetaId": 2148783937,
  "fieldName": "projectNo",
  "fieldType": "Text",
  "id": 2152803528,
  "nativeType": "TEXT",
  "objId": 2152803528,
  "status": 0,
  "vector": 0,
  "fieldId": 2152803528,
  "datasetLabel": "项目信息",
  "datasetType": "TABLE",
  "displayFields": ["projectNo", "receivingAmount"],
  "dummy": false,
  "fields": [...],
  "label": "项目信息",
  "modelTableType": "FACTS_TABLE",
  "name": "project3X",
  "origLabel": "项目信息",
  "styleJson": "{}",
  "unionDataSets": [],
  "uuid": "project3X-projectNo-<uuid>",
  "modelDatasetLabel": "项目信息",
  "modelDatasetName": "project3X",
  "newFieldLabel": "项目名称",
  "nodeInfo": {...}
}
```

### 关键字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| fields | ✅ | 模型所有字段的完整数组 |
| nodeInfo | ✅ | 包含字段信息的对象 |
| uuid | ✅ | 唯一标识符，格式：`{datasetName}-{fieldName}-{uuid}` |
| datasetMetaId | ✅ | 数据集元数据 ID |
| fieldMetaId | ✅ | 字段元数据 ID |
| fieldId | ✅ | 字段 ID |

## indicator 字段结构 (35 个字段)

在 dimension 基础上增加以下字段：

```json
{
  ...dimension 字段...,
  "metricType": "SUM",
  "valueFormat": {
    "isPercentage": 0,
    "decimalPlaces": 2,
    "useThousandsSeparator": 0
  },
  "orderType": "desc"
}
```

### 聚合类型

| metricType | 说明 |
|------------|------|
| SUM | 求和 |
| AVG | 平均 |
| COUNT | 计数 |
| MAX | 最大值 |
| MIN | 最小值 |

## fields 数组格式

```json
"fields": [
  {
    "customVal": false,
    "datasetId": 2148783937,
    "datasetMetaId": 2148783937,
    "datasetName": "project3X",
    "disabled": 0,
    "entCode": "jidianerlei_demo",
    "fieldLabel": "项目名称",
    "fieldMetaId": 2148783937,
    "fieldName": "projectNo",
    "fieldType": "Text",
    "id": 2152803528,
    "nativeType": "TEXT",
    "objId": 2152803528,
    "status": 0,
    "vector": 0,
    "fieldId": 2152803528
  },
  {
    "customVal": false,
    "datasetId": 2148783937,
    "datasetMetaId": 2148783937,
    "datasetName": "project3X",
    "disabled": 0,
    "entCode": "jidianerlei_demo",
    "fieldLabel": "中标金额",
    "fieldMetaId": 2148783937,
    "fieldName": "biddingAmount",
    "fieldType": "Number",
    "id": 2157604772,
    "nativeType": "INT",
    "objId": 2157604772,
    "status": 0,
    "vector": 0,
    "fieldId": 2157604772
  },
  {
    "customVal": false,
    "datasetId": 2148797900,
    "datasetMetaId": 2148797900,
    "datasetName": "collectionReg3X",
    "disabled": 0,
    "entCode": "jidianerlei_demo",
    "fieldLabel": "收款金额",
    "fieldMetaId": 2148797900,
    "fieldName": "receivingAmount",
    "fieldType": "Number",
    "id": 2148799372,
    "nativeType": "INT",
    "objId": 2148799372,
    "status": 0,
    "vector": 0,
    "fieldId": 2148799372
  }
]
```

**注意**: `fields` 数组必须包含模型的所有字段，而不仅仅是当前使用的字段。

## nodeInfo 结构

```json
"nodeInfo": {
  "datasetId": 2148783937,
  "datasetLabel": "项目信息",
  "datasetName": "project3X",
  "datasetType": "TABLE",
  "displayFields": ["projectNo", "receivingAmount"],
  "dummy": false,
  "entCode": "jidianerlei_demo",
  "fields": [...],
  "label": "项目信息",
  "modelTableType": "FACTS_TABLE",
  "name": "project3X",
  "origLabel": "项目信息",
  "styleJson": "{}",
  "unionDataSets": []
}
```

**注意**: `nodeInfo.fields` 也必须包含模型的所有字段。

## 常见错误

### 错误 1: 组件不显示配置

```
错误原因：缺少 fields 数组或 nodeInfo 对象
解决：确保 dimension 和 indicator 都包含完整的 fields 和 nodeInfo
```

### 错误 2: fieldMetaId 不匹配

```
错误原因：fieldMetaId 应该与 datasetMetaId 相同（对于基础字段）
解决：检查 fieldMetaId 是否正确设置
```

### 错误 3: uuid 格式错误

```
错误原因：uuid 格式不正确
正确格式：project3X-projectNo-a00ec32a-b904-43df-bed2-224234588539
```
