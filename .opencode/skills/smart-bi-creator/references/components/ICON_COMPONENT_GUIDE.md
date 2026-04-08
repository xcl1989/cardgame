# 图标组件 (Icon Component)

## 概述

图标组件是装饰组件的一种，用于在大屏上显示装饰性图标，让大屏更加丰富好看。

## 特点

- 不需要数据源配置
- 支持 14 种图标样式
- 可调整位置和大小
- 纯装饰性组件

## 添加图标组件

```bash
python3 scripts/add_component.py \
  --screen-id 3659018572 \
  --chart-type icon \
  --view-name "图标1" \
  --top 5 --left 30 \
  --width 80 --height 80 \
  --decorate-index 2
```

### 参数说明

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| `--screen-id` | 是 | 大屏 ID | 3659018572 |
| `--chart-type` | 是 | 固定为 `icon` | icon |
| `--view-name` | 否 | 图标名称 | "图标1" |
| `--top` | 是 | 顶部位置 | 5 |
| `--left` | 是 | 左侧位置 | 30 |
| `--width` | 否 | 宽度，默认 80 | 80 |
| `--height` | 否 | 高度，默认 80 | 80 |
| `--decorate-index` | 否 | 图标样式编号（1-14），默认 1 | 2 |

## 可用图标样式

图标样式编号支持 1-25，使用 `--decorate-index` 参数指定。

示例：`--decorate-index 5` 表示使用 `iconDecorate5.png`

## 典型应用场景

### 1. 头部装饰

```bash
# 左侧图标 + 标题
python3 scripts/add_component.py \
  --screen-id 3659018572 \
  --chart-type icon \
  --view-name "图标1" \
  --top 5 --left 30 \
  --width 60 --height 60 \
  --decorate-index 3
```

### 2. 指标卡搭配

```bash
# 在指标卡旁边添加图标
python3 scripts/add_component.py \
  --screen-id 3659018572 \
  --chart-type icon \
  --view-name "图标" \
  --top 80 --left 30 \
  --width 50 --height 50 \
  --decorate-index 7
```

### 3. 角落装饰

```bash
# 右下角装饰图标
python3 scripts/add_component.py \
  --screen-id 3659018572 \
  --chart-type icon \
  --view-name "图标" \
  --top 1000 --left 1800 \
  --width 80 --height 80 \
  --decorate-index 14
```

## 更新图标样式

使用 `--decorate-index` 重新创建，或通过界面调整。

## 组件结构

```json
{
  "viewName": "图标1",
  "styleJson": {
    "screenPosition": {
      "position": {
        "x": 30,
        "y": 5,
        "w": 80,
        "h": 80
      }
    },
    "decorate": {},
    "decorateStyle": {
      "rotate": {
        "angle": 0,
        "verMirrored": false,
        "levelMirrored": false
      },
      "selectedDecorate": "iconDecorate/iconDecorate2.png"
    }
  }
}
```

## 与其他装饰组件对比

| 组件类型 | 用途 | 可调整大小 | 数据依赖 |
|---------|------|-----------|---------|
| icon | 图标装饰 | ✅ 可调整 | ❌ 无需数据 |
| decorate (square) | 方形装饰 | ❌ 固定 | ❌ 无需数据 |
| decorate (bar) | 条形装饰 | ❌ 固定 | ❌ 无需数据 |
| decorate (base) | 基础装饰 | ❌ 固定 | ❌ 无需数据 |
| head | 头部装饰 | ❌ 固定 | ❌ 无需数据 |
| card | 卡片容器 | ✅ 可调整 | ❌ 无需数据 |

## 注意事项

1. **图标会拉伸** - 设置的宽高会应用于图标图片，可能会拉伸变形
2. **选择合适大小** - 根据放置位置选择合适的尺寸
3. **颜色协调** - 确保图标颜色与整体大屏风格协调
4. **适度使用** - 图标用于点缀，不宜过多
