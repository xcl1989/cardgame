# 组件联动使用指南

组件联动功能允许用户点击一个有维度的组件时，自动过滤其他组件的数据，实现多组件联动交互。

## 快速开始

```bash
# 添加柱图并联动到已有的饼图
python3 scripts/add_component.py \
  --screen-id 3654572744 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type bar \
  --top 200 --left 50 \
  --width 450 --height 300 \
  --view-name "收款趋势" \
  --linkage "grid-type:pie-uuid:12345678"
```

## 联动规则

### 1. 只有设置了维度的组件才能联动

以下组件类型**不支持联动**（因为没有维度概念）：
- `time` - 时间组件
- `text` - 文本组件
- `decorate` - 装饰组件
- `head` - 头部组件
- `card` - 卡片组件
- `icon` - 图标组件

### 2. 被联动的组件必须使用相同数据模型

所有联动组件必须使用相同的数据模型（modelId），否则会报错：

```
ValueError: 联动目标组件 UUID=xxx 使用的数据模型(ID:123)与当前组件(ID:456)不同，联动组件必须使用相同数据模型
```

### 3. 目标组件 UUID 必须存在

如果指定的联动目标 UUID 不存在，会报错：

```
ValueError: 联动目标组件 UUID不存在: xxx
```

## 配置结构

联动配置存储在组件的 `interaction` 字段中：

```json
{
  "component": {
    "modelId": 2597080602,
    "interaction": {
      "linkage": {
        "sameModels": [
          "grid-type:pie-uuid:12345678",
          "grid-type:line-uuid:87654321"
        ]
      }
    }
  }
}
```

## 使用场景

### 典型场景 1：按月份联动

1. 创建柱图（按月份展示收款趋势）
2. 创建饼图（按收款项类型展示占比）
3. 创建折线图（按月份展示趋势）
4. 设置柱图联动到饼图和折线图
5. 用户点击柱图中某个月份，饼图和折线图自动过滤到该月份

### 典型场景 2：按分类联动

1. 创建饼图（按部门展示占比）
2. 创建柱图（按部门展示收款金额）
3. 设置饼图联动到柱图
4. 用户点击饼图中某个部门，柱图自动过滤到该部门

## 命令行参数

| 参数 | 说明 |
|------|------|
| `--linkage` | 联动目标组件的 UUID 列表（支持多个，用空格分隔） |

### 示例

```bash
# 单个联动目标
--linkage "grid-type:pie-uuid:12345678"

# 多个联动目标
--linkage "grid-type:pie-uuid:12345678" "grid-type:line-uuid:87654321" "grid-type:bar-uuid:11223344"
```

## 查看组件 UUID

使用 `update_screen.py --show-info` 查看大屏中所有组件的 UUID：

```bash
python3 scripts/update_screen.py --screen-id 3654572744 --show-info
```

输出示例：
```
=== 大屏组件列表 ===
UUID: grid-type:bar-uuid:11111111
  标题: 收款趋势
  类型: bar
  位置: top=200, left=50, 450x300

UUID: grid-type:pie-uuid:22222222
  标题: 收款项占比
  类型: pie
  位置: top=200, left=500, 400x300

UUID: grid-type:line-uuid:33333333
  标题: 月度趋势
  类型: line
  位置: top=520, left=50, 880x300
```

## 常见问题

### Q: 联动不生效怎么办？

1. 确认两个组件使用相同的数据模型
2. 确认目标组件 UUID 正确
3. 确认触发联动的组件有维度字段
4. 检查浏览器控制台是否有错误

### Q: 可以动态更新联动关系吗？

目前联动关系在创建时设置。如需更新，需要修改组件的 `interaction.linkage.sameModels` 字段。

### Q: 哪些组件类型支持联动？

所有有维度字段的组件类型都支持联动，包括：
- `bar` / `bar3d` - 柱状图
- `line` - 折线图
- `pie` - 饼图
- `table` - 表格
- `radar` - 雷达图
- `ranking` - 排名图
- `horizontalBar` - 条形图
- `map` - 地图
- 等

### Q: 可以设置多层联动吗？

是的，例如：
- 柱图 A 联动到饼图 B 和折线图 C
- 饼图 B 也可以联动到柱图 A（交叉联动）
