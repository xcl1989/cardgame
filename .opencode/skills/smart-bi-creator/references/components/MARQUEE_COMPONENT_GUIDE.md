# 走马灯组件使用指南

## 概述

走马灯（Marquee）用于滚动显示文字内容，适合：
- 公告滚动播放
- 新闻信息展示
- 通知提示滚动
- 欢迎语展示

## 组件特点

### 1. 滚动效果
- 文字自动从右向左滚动
- 可设置滚动速度
- 支持单行或多行内容

### 2. 内容配置
- 支持静态文字内容
- 支持数据绑定动态内容
- 可设置滚动方向

### 3. 适用场景
- 系统公告滚动播放
- 重要消息通知
- 欢迎语/问候语
- 实时数据播报

## 使用方法

### 基础示例

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type marquee \
  --top 20 --left 100 \
  --width 800 --height 40 \
  --view-name "公告滚动"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| --screen-id | 是 | 大屏 ID | 3654239893 |
| --model-id | 是 | 数据模型 ID | 2597080602 |
| --dimension-field | 是 | 维度字段 | projectNo |
| --indicator-field | 是 | 指标字段 | receivingAmount |
| --chart-type | 是 | 图表类型，固定为 `marquee` | marquee |
| --top | 是 | Y 坐标 | 20 |
| --left | 是 | X 坐标 | 100 |
| --width | 是 | 组件宽度 | 800 |
| --height | 是 | 组件高度 | 40 |
| --view-name | 否 | 视图标题 | "公告滚动" |

### 尺寸建议

| 场景 | 推荐宽度 | 推荐高度 | 说明 |
|------|---------|---------|------|
| 顶部横幅 | 1920 | 40-50 | 全宽滚动 |
| 区域滚动 | 400-600 | 30-40 | 局部公告 |
| 底部滚动 | 1920 | 30-40 | 全宽消息 |

## 样式配置

### 完整样式结构

```json
{
  "screenPosition": {
    "position": {"x": 100, "y": 20, "w": 800, "h": 40}
  },
  "textData": {
    "show": true,
    "content": "欢迎访问公司经营分析系统"
  },
  "content": {
    "textContent": "欢迎访问公司经营分析系统",
    "textSetMap": {
      "size": 16,
      "fontFamily": "Microsoft YaHei",
      "textAlign": "left",
      "textColor": "#FFFFFF",
      "textBold": false,
      "textItalic": false
    }
  },
  "marqueeStyle": {
    "direction": "left",
    "speed": 50,
    "loop": true,
    "pauseOnHover": true
  }
}
```

## 进阶配置

### 设置滚动方向

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field projectNo \
  --indicator-field receivingAmount \
  --chart-type marquee \
  --top 20 --left 100 \
  --width 800 --height 40 \
  --view-name "公告滚动" \
  --marquee-direction left
```

### 滚动参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| direction | 滚动方向 | left/right/up/down |
| speed | 滚动速度（数字越大越快） | 10-100 |
| loop | 是否循环滚动 | true/false |

## 常见问题

### Q1: 如何设置静态文字内容？

**A**: 走马灯组件需要绑定数据模型。如果只需要显示静态文字，可以：
1. 创建一个仅包含一条数据的虚拟模型
2. 或者使用文本组件配合 CSS 动画

### Q2: 滚动速度太快/太慢？

**A**: 调整 `marqueeStyle.speed` 参数，值越大速度越快，建议 30-80。

### Q3: 如何实现暂停效果？

**A**: 设置 `pauseOnHover: true`，鼠标悬停时暂停滚动。

## 相关文档

- [文本组件](TEXT_COMPONENT_GUIDE.md)
- [头部组件](HEAD_COMPONENT_GUIDE.md)
- [时间组件](TIME_COMPONENT_GUIDE.md)
