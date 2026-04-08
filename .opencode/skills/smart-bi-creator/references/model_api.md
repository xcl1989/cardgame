# 数据模型 API (Model API)

## 获取模型列表

### 请求

```bash
curl 'https://dev.cloud.hecom.cn/biserver/paas/app/dataModel/operation/list' \
  -H 'Content-Type: application/json' \
  -H 'accessToken: <token>' \
  -H 'entCode: <ent-code>' \
  -H 'uid: <uid>' \
  -H 'empCode: <emp-code>' \
  --data-raw '{"modelName":"","pageNo":1,"pageSize":999999,"sortParam":{"field":"id","asc":0}}'
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| modelName | string | 否 | 模型名称过滤 |
| pageNo | number | 是 | 页码，从 1 开始 |
| pageSize | number | 是 | 每页数量，最大 999999 |
| sortParam.field | string | 否 | 排序字段 |
| sortParam.asc | number | 否 | 升序 1/降序 0 |

### 响应示例

```json
{
  "data": {
    "list": [
      {
        "id": 3562329848,
        "name": "项目的收款登记",
        "apiName": "biModelApi90",
        "createdBy": "谢聪凌",
        "createdOn": 1772242243372,
        "entCode": "jidianerlei_demo"
      }
    ]
  },
  "desc": "请求成功",
  "result": "0"
}
```

## 获取模型详情

### 请求

```bash
curl 'https://dev.cloud.hecom.cn/biserver/paas/app/dataModel/operation/listModelAll/<modelId>' \
  -H 'Content-Type: application/json' \
  -H 'accessToken: <token>' \
  --data-raw '{"id":<modelId>}'
```

### 响应示例

```json
{
  "data": {
    "modelDTO": {
      "id": 3562329848,
      "name": "项目的收款登记",
      "description": "可以分析项目的中标金额，收款金额",
      "version": 1
    },
    "modelDatasetDTOList": [
      {
        "datasetId": 2148783937,
        "datasetLabel": "项目信息",
        "datasetName": "project3X",
        "datasetType": "TABLE",
        "fields": [
          {
            "fieldName": "projectNo",
            "fieldLabel": "项目名称",
            "fieldType": "Text",
            "id": 2152803528,
            "nativeType": "TEXT"
          },
          {
            "fieldName": "biddingAmount",
            "fieldLabel": "中标金额",
            "fieldType": "Number",
            "id": 2157604772,
            "nativeType": "INT"
          }
        ]
      },
      {
        "datasetId": 2148797900,
        "datasetLabel": "收款登记",
        "datasetName": "collectionReg3X",
        "fields": [
          {
            "fieldName": "receivingAmount",
            "fieldLabel": "收款金额",
            "fieldType": "Number",
            "id": 2148799372,
            "nativeType": "INT"
          }
        ]
      }
    ]
  }
}
```

## 字段类型说明

| fieldType | nativeType | 说明 |
|-----------|------------|------|
| Text | TEXT | 文本类型 |
| Number | INT/DECIMAL | 数字类型 |
| Time | DATE | 日期时间类型 |
| Join | TEXT | 关联字段 |

## 使用示例

```python
# Python 示例：获取模型所有字段
import requests

def get_model_fields(model_id, headers):
    url = f'https://dev.cloud.hecom.cn/biserver/paas/app/dataModel/operation/listModelAll/{model_id}'
    response = requests.post(url, json={'id': model_id}, headers=headers)
    data = response.json()
    
    all_fields = []
    for ds in data['data']['modelDatasetDTOList']:
        for field in ds['fields']:
            field['datasetId'] = ds['datasetId']
            field['datasetName'] = ds['datasetName']
            all_fields.append(field)
    
    return all_fields
```
