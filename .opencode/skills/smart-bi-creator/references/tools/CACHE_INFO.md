# 缓存目录说明

## 目录结构

```
smart-bi-creator/
├── scripts/
│   ├── .cache/          # 缓存目录（自动创建）
│   │   ├── model_list.json
│   │   └── model_info_xxx.json
│   ├── get_model_data.py
│   └── ...
├── .gitignore           # 忽略缓存文件
└── ...
```

## 缓存文件位置

### 默认位置
```
/path/to/smart-bi-creator/.opencode/skills/smart-bi-creator/scripts/.cache/
```

### 文件说明
| 文件 | 说明 | 生成方式 |
|------|------|----------|
| `model_list.json` | 所有模型列表 | `get_model_data.py --list` |
| `model_info_xxx.json` | 模型详细信息 | `get_model_data.py --model-ids xxx` |

## 为什么不用 /tmp/？

### 之前的问题
```bash
# ❌ 使用 /tmp/ 的问题
- 需要系统权限确认（macOS 每次询问）
- 系统重启后可能被清理
- 全局临时目录，不安全
- 多个用户可能冲突
```

### 现在的优势
```bash
# ✅ 使用项目目录下的 .cache/
- 无需权限确认
- 持久保存，不会丢失
- 项目私有，更安全
- 已在 .gitignore 中，不会提交到 Git
```

## 使用方法

### 1. 不指定输出路径（推荐）
```bash
# 自动保存到 .cache/ 目录
python3 scripts/get_model_data.py --list
python3 scripts/get_model_data.py --model-ids 2597080602

# 输出：
# 已保存 283 个模型到 .../scripts/.cache/model_list.json
# 已保存 1 个模型的详细信息到 .../scripts/.cache/model_info_2597080602.json
```

### 2. 指定自定义路径
```bash
# 保存到指定位置
python3 scripts/get_model_data.py \
  --model-ids 2597080602 \
  --output /path/to/my/output.json
```

## 清理缓存

### 手动清理
```bash
# 删除所有缓存文件
rm -rf scripts/.cache/*
```

### 保留常用缓存
建议保留 `model_list.json` 和常用模型的详细信息，避免重复请求 API。

## 注意事项

1. **缓存目录自动创建** - 第一次运行时会自动创建 `.cache/` 目录
2. **不会被 Git 追踪** - `.cache/` 已在 `.gitignore` 中
3. **建议定期清理** - 避免缓存文件占用过多空间
4. **模型 ID 命名** - 详细缓存文件会以模型 ID 命名，方便查找

## 文件示例

### model_list.json
```json
[
  {"id": 2597080602, "name": "收款登记模型 1219"},
  {"id": 2537727927, "name": "付款申请"},
  ...
]
```

### model_info_2597080602.json
```json
[
  {
    "id": 2597080602,
    "name": "收款登记模型 1219",
    "fields_summary": {
      "date_fields": [...],
      "category_fields": [...],
      "amount_fields": [...]
    }
  }
]
```
