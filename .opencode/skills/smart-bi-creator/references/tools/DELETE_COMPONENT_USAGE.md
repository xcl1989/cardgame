# delete_component.py - 删除大屏组件脚本

## 功能说明

用于通过 API 删除大屏中的一个或多个组件。

## 使用方式

### 1. 查看大屏组件列表

```bash
python3 scripts/delete_component.py --screen-id 3654239893 --list
```

输出示例：
```
=== 大屏基本信息 ===
名称：项目收付款财务分析大屏
ID: 3654239893

=== 图层数量：13 ===
1. N/A
   UUID: grid-type:bar-uuid:1773839023554
   位置：top=600, left=480
   大小：width=960, height=400

=== 数据组件数量：13 ===
组件：累计收款 (metric)
  UUID: grid-type:metric-uuid:1773839035863
  模型 ID: 2597080602
...
```

### 2. 删除单个组件

```bash
python3 scripts/delete_component.py \
  --screen-id 3654239893 \
  --uuid "grid-type:bar-uuid:1773839023554"
```

### 3. 删除多个组件

```bash
python3 scripts/delete_component.py \
  --screen-id 3654239893 \
  --uuid "grid-type:bar-uuid:xxx" \
  --uuid "grid-type:line-uuid:yyy" \
  --uuid "grid-type:pie-uuid:zzz"
```

## 参数说明

| 参数 | 说明 | 是否必需 |
|------|------|---------|
| `--screen-id` | 大屏 ID | 是 |
| `--uuid` | 要删除的组件 UUID（可重复指定多个） | 否（与 --list 互斥） |
| `--list` | 列出所有组件 | 否（与 --uuid 互斥） |

## 完整工作流

### 场景 1：删除不需要的组件

```bash
# 步骤 1：查看当前所有组件
python3 scripts/delete_component.py --screen-id 3654239893 --list

# 步骤 2：复制要删除的组件 UUID

# 步骤 3：执行删除
python3 scripts/delete_component.py \
  --screen-id 3654239893 \
  --uuid "grid-type:line-uuid:1773839049855" \
  --uuid "grid-type:bar-uuid:1773839050380"

# 步骤 4：验证删除结果
python3 scripts/delete_component.py --screen-id 3654239893 --list
```

### 场景 2：批量清理组件

```bash
# 一次性删除多个组件
python3 scripts/delete_component.py --screen-id 3654239893 \
  --uuid "grid-type:xxx" \
  --uuid "grid-type:yyy" \
  --uuid "grid-type:zzz"
```

## 与其他脚本配合使用

```bash
# 1. 先查看组件
python3 scripts/update_screen.py --screen-id 3654239893 --show-info

# 2. 删除不需要的组件
python3 scripts/delete_component.py --screen-id 3654239893 \
  --uuid "grid-type:xxx"

# 3. 添加新组件
python3 scripts/add_component.py --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type bar \
  --top 200 --left 20 \
  --width 460 --height 320 \
  --view-name "新组件"

# 4. 调整组件位置
python3 scripts/update_screen.py --screen-id 3654239893 \
  --uuid "grid-type:bar-uuid:xxx" \
  --top 200 --left 20
```

## 注意事项

1. **删除前备份**：删除操作不可逆，建议先导出大屏配置
2. **组件依赖**：删除组件不会影响其他组件
3. **权限要求**：需要有大屏编辑权限
4. **认证配置**：确保 `header.json` 已正确配置

## 脚本位置

```
.opencode/skills/smart-bi-creator/scripts/
├── delete_component.py      # 删除组件脚本（新增）
├── add_component.py         # 添加组件脚本
├── update_screen.py         # 更新大屏配置脚本
├── create_screen.py         # 创建大屏脚本
├── rename_component.py      # 重命名组件脚本
└── header.json              # 认证配置文件
```
