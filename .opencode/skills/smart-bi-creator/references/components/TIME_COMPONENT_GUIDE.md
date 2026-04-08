# 时间组件 (Time Component)

## 概述

时间组件用于在大屏上显示当前日期和时间。

## 添加时间组件

```bash
python3 scripts/add_component.py \
  --screen-id 3659018572 \
  --chart-type time \
  --view-name "当前时间" \
  --top 5 --left 1600 \
  --width 300 --height 50 \
  --font-size 20
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--screen-id` | 是 | 大屏 ID |
| `--chart-type` | 是 | 设为 `time` |
| `--view-name` | 否 | 组件名称，默认 "时间" |
| `--top` | 否 | 顶部位置，默认 100 |
| `--left` | 否 | 左侧位置，默认 100 |
| `--width` | 否 | 宽度，默认 440 |
| `--height` | 否 | 高度，默认 36 |
| `--font-size` | 否 | 字体大小，默认 24 |
| `--align` | 否 | 对齐方式：`left`/`center`/`right`，默认 `left` |

## 更新时间组件

### 更新字体大小

```bash
python3 scripts/update_screen.py \
  --screen-id 3659018572 \
  --uuid "grid-type:time-uuid:1774513034458" \
  --font-size 28
```

### 更新文字颜色

```bash
python3 scripts/update_screen.py \
  --screen-id 3659018572 \
  --uuid "grid-type:time-uuid:1774513034458" \
  --time-color "#FF6B6B"
```

### 更新时间格式

```bash
# 仅显示日期
python3 scripts/update_screen.py \
  --screen-id 3659018572 \
  --uuid "grid-type:time-uuid:1774513034458" \
  --time-format date

# 仅显示时间
python3 scripts/update_screen.py \
  --screen-id 3659018572 \
  --uuid "grid-type:time-uuid:1774513034458" \
  --time-format time

# 显示日期+时间
python3 scripts/update_screen.py \
  --screen-id 3659018572 \
  --uuid "grid-type:time-uuid:1774513034458" \
  --time-format dateAndTime
```

## 组件结构

```json
{
  "viewName": "当前时间",
  "styleJson": {
    "screenPosition": {
      "position": {
        "x": 1600,
        "y": 5,
        "w": 300,
        "h": 50
      }
    },
    "cardSet": {
      "textSetMap": {
        "fontSize": 20,
        "textColor": "#FF6B6B",
        "textBold": true,
        "textItalic": false
      },
      "text": "LCDFont"
    },
    "timeType": {
      "type": "dateAndTime",
      "date": "yyyy-MM-dd",
      "time": "hh:mm:ss"
    }
  }
}
```

## timeType 类型

| 类型 | 说明 | 日期格式 | 时间格式 |
|------|------|----------|----------|
| `dateAndTime` | 日期 + 时间 | yyyy-MM-dd | hh:mm:ss |
| `date` | 仅日期 | yyyy-MM-dd | (空) |
| `time` | 仅时间 | (空) | hh:mm:ss |

## 支持的字体

- `LCDFont` - LCD 数字字体（默认）
- `Arial`
- `Georgia`
- `Times New Roman`
