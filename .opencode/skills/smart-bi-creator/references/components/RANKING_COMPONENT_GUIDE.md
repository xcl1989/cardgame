# 排名图组件使用指南

## 概述

排名图（Ranking Chart）用于展示数据的 Top N 排行榜，适合展示：
- 项目收款/付款排名
- 部门业绩排名
- 产品销售排名
- 区域业绩排行

## 组件特点

### 1. 排名图标
- 前三名显示特殊图标（金牌🥇、银牌🥈、铜牌🥉）
- 使用 WebP 格式图片：`rank_2_1.webp`, `rank_2_2.webp`, `rank_2_3.webp`
- 可自定义图标样式

### 2. 滚动效果
- 支持平滑滚动循环显示
- 可配置滚动速度和范围
- 默认显示所有数据

### 3. 视觉样式
- 渐变色条形（蓝紫色系）
- 透明卡片背景
- 白色文字显示
- 粗体强调数值

## 使用方法

### 基础示例

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type ranking \
  --top 120 --left 1495 \
  --width 411 --height 277 \
  --view-name "项目收款排名"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654239893 |
| --model-id | 是 | 数据模型 ID | 2597080602 |
| --dimension-field | 是 | 维度字段（用于分组） | projectNo |
| --indicator-field | 是 | 指标字段（用于排序） | receivingAmount |
| --chart-type | 是 | 图表类型，固定为 `ranking` | ranking |
| --top | 是 | Y 坐标 | 120 |
| --left | 是 | X 坐标 | 1495 |
| --width | 是 | 组件宽度 | 411 |
| --height | 是 | 组件高度 | 277 |
| --view-name | 否 | 视图标题 | "项目收款排名" |

### 尺寸建议

| 场景 | 推荐宽度 | 推荐高度 | 说明 |
|------|---------|---------|------|
| 侧边排名 | 400-450 | 270-300 | 适合单侧展示 |
| 主排名区 | 500-600 | 350-400 | 视觉焦点区域 |
| 小型排名 | 300-350 | 200-250 | 辅助展示 |

## 样式配置

### 完整样式结构

```json
{
  "screenPosition": {
    "position": {"x": 1495, "y": 120, "w": 411, "h": 277}
  },
  "legend": {
    "textSetMap": {"textColor": "#177DDC"}
  },
  "name": {
    "textSetMap": {
      "textItalic": false,
      "textBold": true,
      "fontSize": 14,
      "textColor": "#fff"
    }
  },
  "scroll": {
    "isExtra": true,
    "range": "all",
    "type": "smooth",
    "speed": 3
  },
  "tooltip": {
    "backgroundColor": "#303467",
    "textSetMap": {"textColor": "#A6ADD0"}
  },
  "rank": {
    "icon": "{\"val\":\"img2\",\"label\":[\"rank_2_1.webp\",\"rank_2_2.webp\",\"rank_2_3.webp\"]}",
    "textSetMap": {
      "textItalic": false,
      "textBold": true,
      "fontSize": 18,
      "textColor": "#fff"
    }
  },
  "draw": {
    "colorSettingMap": {
      "color": "linear-gradient(90deg, rgb(52,113,232) 0%, rgb(31,64,128) 100%)",
      "colorType": "singleColor"
    }
  },
  "title": {
    "isExtra": true,
    "show": false,
    "textSetMap": {
      "textItalic": false,
      "textBold": true,
      "fontSize": 16,
      "textColor": "#FEFEFE"
    }
  },
  "value": {
    "isExtra": true,
    "textSetMap": {
      "textItalic": false,
      "textBold": true,
      "fontSize": 18,
      "textColor": "#fff"
    }
  },
  "card": {
    "border": "rgba(30, 39, 55, 0.8)",
    "padding": 12,
    "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
    "lineWidthMap": {"width": 1, "style": "solid"}
  }
}
```

### 标准卡片样式（深蓝半透明）

新创建的组件默认使用以下卡片样式：

```json
"card": {
  "border": "rgba(30, 39, 55, 0.8)",
  "padding": 12,
  "cardBackgroundColor": "rgba(13, 24, 44, 0.8)",
  "lineWidthMap": {"width": 1, "style": "solid"}
}
```

**使用 update_screen.py 更新现有组件样式**:
```bash
python3 scripts/update_screen.py \
  --screen-id 3657066337 \
  --uuid "grid-type:ranking-uuid:xxx" \
  --card-background-color "rgba(13, 24, 44, 0.8)" \
  --card-border "rgba(30, 39, 55, 0.8)" \
  --card-padding 12
```

### 关键样式说明

#### 1. 排名图标配置
```json
"rank": {
  "icon": "{\"val\":\"img2\",\"label\":[\"rank_2_1.webp\",\"rank_2_2.webp\",\"rank_2_3.webp\"]}",
  "textSetMap": {
    "textBold": true,
    "fontSize": 18,
    "textColor": "#fff"
  }
}
```
- `val`: 图标样式版本
- `label`: 排名图标文件数组

#### 2. 滚动配置
```json
"scroll": {
  "isExtra": true,
  "range": "all",      // 滚动范围：all=全部，visible=可见区域
  "type": "smooth",    // 滚动类型：smooth=平滑，step=步进
  "speed": 3           // 滚动速度：1-10，数值越大越快
}
```

#### 3. 条形渐变色
```json
"draw": {
  "colorSettingMap": {
    "color": "linear-gradient(90deg, rgb(52,113,232) 0%, rgb(31,64,128) 100%)",
    "colorType": "singleColor"
  }
}
```
- 使用 CSS 线性渐变语法
- 可自定义颜色组合

## 实战案例

### 案例 1：项目收款 Top10 排名

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type ranking \
  --top 120 --left 1495 \
  --width 411 --height 277 \
  --view-name "项目收款 Top10"
```

### 案例 2：部门业绩排名（多个排名组合）

```bash
# 收款排名
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field deptName \
  --indicator-field receivingAmount \
  --chart-type ranking \
  --top 120 --left 100 \
  --width 400 --height 300 \
  --view-name "部门收款排名" && \

# 付款排名
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2537727927 \
  --dimension-field deptName \
  --indicator-field paymentAmount \
  --chart-type ranking \
  --top 120 --left 520 \
  --width 400 --height 300 \
  --view-name "部门付款排名"
```

### 案例 3：配合指标卡使用

```bash
# 先添加指标卡显示总计
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type metric \
  --top 20 --left 20 \
  --width 230 --height 130 \
  --view-name "累计收款" && \

# 再添加排名图显示明细
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type ranking \
  --top 180 --left 20 \
  --width 450 --height 350 \
  --view-name "项目收款排名"
```

## 注意事项

### 1. 数据排序
- 排名图默认按指标值降序排列
- `indicator.orderType: "desc"` 控制排序方向

### 2. 显示条数
- 默认显示前 10 条（`limit.value: 10`）
- 可通过 `limit` 参数调整

### 3. 滚动配置
- 数据条数超过显示区域时自动滚动
- 调整 `scroll.speed` 控制滚动速度

### 4. 兼容性
- 排名图需要大屏主题支持
- 深色主题效果最佳

## 与其他组件配合

### 推荐组合

```
+----------------------------------+
| [指标卡 1] [指标卡 2] [指标卡 3]  |  ← 顶部关键指标
+----------------------------------+
|                                  |
|  [柱图]      [排名图]   [饼图]    |  ← 中部分析图表
|                                  |
+----------------------------------+
|        [底部明细表格]             |  ← 底部详细数据
+----------------------------------+
```

### 布局建议

1. **指标卡 + 排名图**：上方显示总计，下方显示排名明细
2. **多个排名图并列**：对比不同维度的排名
3. **排名图 + 趋势图**：展示排名变化和趋势

## 常见问题

### Q1: 排名图标不显示？
- 检查图标文件是否存在
- 确保 `rank.icon` 配置正确（JSON 字符串格式）

### Q2: 数据不滚动？
- 检查 `scroll.isExtra: true`
- 调整 `scroll.range: "all"`

### Q3: 条形颜色不对？
- 修改 `draw.colorSettingMap.color` 渐变色
- `colorType: "singleColor"` 单色或 `"gradient"` 渐变

### Q4: 如何显示更多排名？
- 调整 `limit.value` 参数
- 增加组件高度以容纳更多数据

## 参考资源

- [SKILL.md](../../SKILL.md) - 技能主文档
- [add_component.py](./add_component.py) - 组件添加脚本
- [config_structure.md](../config_structure.md) - 配置结构详解
