# 常见问题与解决方案 (FAQ)

## 问题汇总与解决方法

### 0. 数据模型原则（重要！）

**一个大屏可以用多个数据模型，但每个组件内只能使用一个数据模型！**

**错误示例**：
- 组件的 `indicators` 使用收款模型的字段
- 但 `filter` 筛选配置却设置成了付款模型的 datasetId/fieldId

**正确做法**：
- 组件内所有配置（indicators、filter、dimensions）必须使用同一个数据模型
- 如果组件使用了支付记录模型，那筛选配置中的 datasetId、fieldId、value 等都必须是对应支付记录模型的

**验证方法**：
```python
# 检查组件的 modelId
comp['modelId']  # 应该是 2593236659（支付记录模型）

# 检查 indicators 的 datasetId
comp['indicators'][0]['datasetId']  # 必须与 modelId 一致

# 检查 filter 的 datasetId
comp['filter'][0]['datasetId']  # 必须与 modelId 一致！
```

---

### 1. API 路径错误导致获取大屏配置失败

**问题描述**: 调用 API 时返回 404 Not Found

**错误尝试**:
```python
# ❌ 错误路径
url = f"https://dev.cloud.hecom.cn/biserver/paas/app/screen/detail/{screen_id}"
```

**原因**: BI 大屏使用的是 `/bi-app/largeScreen/` 路径，不是 `/app/screen/`

**正确路径**:
```python
# ✅ 正确路径
url = f"https://dev.cloud.hecom.cn/biserver/paas/bi-app/largeScreen/get/{screen_id}"
```

**重要区分**:
| 用途 | 路径 |
|------|------|
| 获取大屏配置 | `/bi-app/largeScreen/get/{screen_id}` |
| 更新大屏配置 | `/bi-app/largeScreen/update/{screen_id}` |
| 创建新大屏 | `/bi-app/largeScreen/save` |

---

### 0.1 样式字段结构误解

**问题描述**: 想更新指标卡样式，但不知道样式字段在哪里

**常见误解**:
- 以为样式在 `styleJson.basic.metricStyle`（预设样式名称）
- 以为所有组件都有统一的 `metricStyle` 字段

**实际情况**:
- 指标卡的实际样式定义在 `styleJson` 的各个子字段中：`metricName`、`metricValue`、`drawSettings`、`title`、`card`
- 没有统一的 `metricStyle` 预设名称字段，只有预设样式的完整 JSON 配置

**示例 - 收入合同金额指标卡的实际样式**:
```json
{
  "metricName": {
    "isExtra": true,
    "textSetMap": {
      "textItalic": false,
      "textBold": false,
      "fontSize": 20,
      "textColor": "#B8C5E8"
    }
  },
  "metricValue": {
    "suffixFontSize": 14,
    "textSetMap": {
      "textItalic": false,
      "textBold": true,
      "fontSize": 38,
      "textColor": "#00F5FF"
    },
    "prefixFontSize": 28
  },
  "drawSettings": {
    "gap": 10,
    "iconColor": "#00D4FF",
    "iconPositionMap": { "position": "left" },
    "position": "bottom"
  },
  "title": {
    "isExtra": true,
    "textSetMap": {
      "textItalic": false,
      "textBold": true,
      "fontSize": 18,
      "textColor": "#E0E6FF"
    }
  },
  "card": {
    "border": "rgba(70, 130, 220, 0.8)",
    "padding": 16,
    "cardBackgroundColor": "rgba(40, 60, 120, 0.9)",
    "lineWidthMap": { "width": 2, "style": "solid" }
  }
}
```

**解决方法**: 使用 `update_screen.py --update-style` 命令更新样式，详见下方「5. 批量更新指标卡样式」

---

### 0. 指标卡显示分组数据而不是总计

**问题描述**: 指标卡显示的是按日期分组的数据，而不是总计值

**原因**: 指标卡的维度字段 `groupBy` 参数为 `True`，导致数据按维度分组

**解决方法**:
```bash
cd .opencode/skills/smart-bi-creator
python3 -c "
import json
import requests
from pathlib import Path

header_file = Path('scripts/header.json')
with open(header_file) as f:
    headers_data = json.load(f)

headers = {
    'Accept': '*/*',
    'Content-Type': 'application/json',
    'clientTag': 'web',
    'app': 'biapp',
    'user-locale': 'zh-CN',
}
headers.update(headers_data)

screen_id = 你的大屏 ID
url = f'https://dev.cloud.hecom.cn/biserver/paas/bi-app/largeScreen/get/{screen_id}'
resp = requests.get(url, headers=headers)
config = resp.json()['data']

# 修复所有指标卡
for uuid, comp in config['componentMap'].items():
    if 'metric-uuid' in uuid:
        for dim in comp.get('dimensions', []):
            dim['groupBy'] = False

update_url = f'https://dev.cloud.hecom.cn/biserver/paas/bi-app/largeScreen/update/{screen_id}'
config['id'] = screen_id
requests.post(update_url, json=config, headers=headers)
print('✅ 已修复所有指标卡')
"
```

**2024-03-18 更新**: `add_component.py` 已修复，新添加的指标卡会自动设置 `groupBy: False`。现有大屏可使用上述脚本修复。

---

### 1. 指标卡高度不够，数值显示不全

**问题描述**: 指标卡的数值被截断，显示不完整

**原因**: 默认高度 90-110px 不够

**解决方法**:
```bash
# 增加指标卡高度到 130-140px
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:metric-uuid:xxx" \
  --top 30 --left 20 \
  --width 220 --height 140
```

**推荐尺寸**: 
- 最小高度：130px
- 推荐高度：140px
- 宽度：220-240px

---

### 2. 中间图表左右太空

**问题描述**: 中间主图表宽度不够，左右留有大量空白

**原因**: 默认宽度 850px 在 1920px 画布中显得太窄

**解决方法**:
```bash
# 加宽中间图表到 1100px，并调整位置使其居中
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:bar-uuid:xxx" \
  --top 200 --left 410 \
  --width 1100 --height 500
```

**计算方法**:
```
画布宽度：1920px
图表宽度：1100px
居中位置：left = (1920 - 1100) / 2 = 410px
```

---

### 3. 图表标题显示为"柱图 1"等默认名称

**问题描述**: 图表标题没有使用自定义名称，显示为"柱图 1"、"饼图 1"等

**原因**: `update_screen.py` 的 `--name` 参数修改的是大屏名称，不是组件标题

**解决方法**: 需要同时修改 3 个位置的 title 字段

```bash
# 使用 Python 脚本直接修改组件标题
cd .opencode/skills/smart-bi-creator
python3 -c "
import json
import requests
from pathlib import Path

# 加载认证
header_file = Path('scripts/header.json')
with open(header_file) as f:
    headers_data = json.load(f)

headers = {
    'Accept': '*/*',
    'Content-Type': 'application/json',
    'clientTag': 'web',
    'app': 'biapp',
    'user-locale': 'zh-CN',
}
headers.update(headers_data)

# 获取大屏配置
screen_id = 3654218321
url = f'https://dev.cloud.hecom.cn/biserver/paas/bi-app/largeScreen/get/{screen_id}'
resp = requests.get(url, headers=headers)
data = resp.json()
config = data['data']

# 修改组件标题
uuid = 'grid-type:bar-uuid:1773823950771'
new_title = '月度收款趋势分析'

# 1. 修改 layer 中的 title
for layer in config['config']['layers']:
    if layer['uuid'] == uuid:
        layer['title'] = new_title

# 2. 修改 componentMap 中的 viewName
if uuid in config['componentMap']:
    config['componentMap'][uuid]['viewName'] = new_title

# 3. 修改 layout 中的 title
for layout in config['layouts']:
    if layout['uuid'] == uuid:
        layout['title'] = new_title

# 提交更新
update_url = f'https://dev.cloud.hecom.cn/biserver/paas/bi-app/largeScreen/update/{screen_id}'
config['id'] = screen_id
resp = requests.post(update_url, json=config, headers=headers)
print(f'更新结果：{resp.json()}')
"
```

**关键点**: 必须同时修改以下 3 个位置：
1. `config.layers[].title` - 图层标题
2. `componentMap[uuid].viewName` - 组件视图名称
3. `layouts[].title` - 布局标题

**建议**: 将上述代码保存为 `scripts/rename_component.py`，方便重复使用：

```bash
python3 scripts/rename_component.py \
  --screen-id 3654218321 \
  --uuid "grid-type:bar-uuid:xxx" \
  --title "月度收款趋势分析"
```

---

### 4. 底部图表宽度不均匀

**问题描述**: 底部 4 个图表宽度不一致，最后一个特别窄

**原因**: 手动调整时未计算好等分宽度

**解决方法**: 平均分配宽度

```bash
# 计算等分宽度：(1920 - 边距*2 - 间距*3) / 4
# (1920 - 40 - 60) / 4 = 455 ≈ 460px

python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:pie-uuid:xxx" \
  --top 720 --left 20 \
  --width 460 --height 300 && \
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:line-uuid:xxx" \
  --top 720 --left 500 \
  --width 460 --height 300 && \
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:line-uuid:xxx" \
  --top 720 --left 980 \
  --width 460 --height 300 && \
python3 scripts/update_screen.py \
  --screen-id 3654218321 \
  --uuid "grid-type:bar-uuid:xxx" \
  --top 720 --left 1460 \
  --width 460 --height 300
```

**布局公式**:
```
画布宽度：1920px
图表数量：4 个
图表宽度：460px
间距：20px
左边距：20px

位置计算:
- 图 1: left = 20
- 图 2: left = 20 + 460 + 20 = 500
- 图 3: left = 500 + 460 + 20 = 980
- 图 4: left = 980 + 460 + 20 = 1460
```

---

### 5. 组件重叠问题

**问题描述**: 组件之间相互覆盖，显示不全

**原因**: 坐标计算错误或未预留足够间距

**解决方法**:
```bash
# 1. 先查看当前所有组件位置
python3 scripts/update_screen.py --screen-id 3654218321 --show-info

# 2. 根据输出调整重叠组件的位置
```

**安全间距原则**:
- 组件之间至少留 20px 间距
- 顶部指标卡：top=30, height=140 → 底部在 170px
- 主图表：top≥200 (与指标卡留 30px)
- 底部图表：top=720 (与主图表留 20px，假设主图表 height=500, top=200)

---

### 6. update_screen.py 不支持样式更新

**问题描述**: 想修改指标卡样式（颜色、背景等），但 `update_screen.py` 只支持位置和大小更新

**原因**: 早期版本的 `update_screen.py` 只实现了位置/大小更新功能

**解决方法**: 2024-03-20 起，`update_screen.py` 已支持 `--update-style` 参数更新样式

```bash
# 更新单个指标卡样式
python3 scripts/update_screen.py \
  --screen-id 3654939432 \
  --uuid "grid-type:metric-uuid:1773967415673" \
  --update-style

# 批量更新所有指标卡为同一样式
python3 scripts/update_screen.py \
  --screen-id 3654939432 \
  --uuid "grid-type:metric-uuid:1773967404738" \
  --clone-style-to "grid-type:metric-uuid:1773967415673" \
                   "grid-type:metric-uuid:1773967417343" \
                   "grid-type:metric-uuid:1773967420268"
```

详细用法见下方「5. 批量更新指标卡样式」

---

### 7. 添加组件时发生覆盖

**问题**: 并行执行多个 `add_component.py` 命令时，后面的组件会覆盖前面的

**原因**: `add_component.py` 的工作流程是：获取配置 → 添加组件 → 更新配置。并行执行时，多个命令同时获取旧配置，导致覆盖。

**错误示例**:
```bash
# ❌ 这样会导致组件丢失！
python3 scripts/add_component.py ... &
python3 scripts/add_component.py ... &
```

**正确做法**:
```bash
# ✅ 使用 && 串行执行
python3 scripts/add_component.py ... && \
python3 scripts/add_component.py ... && \
python3 scripts/add_component.py ...
```

---

## 实用脚本模板

### 5. 批量更新指标卡样式

**问题场景**: 大屏中多个指标卡样式不统一，需要将它们改成同一个样式

**解决方法**: 使用 `update_screen.py --clone-style-from` 参数

```bash
# 1. 先查看大屏所有组件，找出要复制的样式和要更新的组件
python3 scripts/update_screen.py --screen-id 3654939432 --show-info

# 2. 假设收入合同金额指标卡(UUID: grid-type:metric-uuid:1773967404738)的样式是正确的
#    要把其他指标卡都改成这个样式

# 3. 执行批量更新
python3 scripts/update_screen.py \
  --screen-id 3654939432 \
  --clone-style-from "grid-type:metric-uuid:1773967404738" \
  --clone-style-to "grid-type:metric-uuid:1773967415673" \
                   "grid-type:metric-uuid:1773967417343" \
                   "grid-type:metric-uuid:1773967421429" \
                   "grid-type:metric-uuid:1773967418709" \
                   "grid-type:metric-uuid:1773967420268" \
                   "grid-type:metric-uuid:1773967516482" \
                   "grid-type:metric-uuid:1773967517394"
```

**工作原理**: 
1. 从 `--clone-style-from` 指定的组件读取 `styleJson`
2. 将该样式应用到 `--clone-style-to` 指定的所有组件
3. 保留目标组件的 `screenPosition`，只更新样式

**注意**: 
- `--clone-style-from` 和 `--clone-style-to` 不能同时只有一个
- 目标组件的原有位置/尺寸信息不会被覆盖
- 这个命令只更新 `styleJson` 字段，不影响数据配置

### 批量修改组件名称脚本

保存为 `scripts/rename_component.py`:

```python
#!/usr/bin/env python3
"""批量修改大屏组件标题"""
import json
import requests
import argparse
from pathlib import Path

def rename_component(screen_id, uuid, new_title, base_url="https://dev.cloud.hecom.cn/biserver"):
    # 加载认证
    header_file = Path(__file__).parent / "header.json"
    with open(header_file) as f:
        headers_data = json.load(f)
    
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'clientTag': 'web',
        'app': 'biapp',
        'user-locale': 'zh-CN',
    }
    headers.update(headers_data)
    
    # 获取大屏配置
    url = f"{base_url}/paas/bi-app/largeScreen/get/{screen_id}"
    resp = requests.get(url, headers=headers)
    data = resp.json()
    config = data['data']
    
    # 修改三个位置的标题
    modified = False
    
    # 1. 修改 layer 中的 title
    for layer in config['config']['layers']:
        if layer['uuid'] == uuid:
            layer['title'] = new_title
            modified = True
    
    # 2. 修改 componentMap 中的 viewName
    if uuid in config['componentMap']:
        config['componentMap'][uuid]['viewName'] = new_title
        modified = True
    
    # 3. 修改 layout 中的 title
    for layout in config['layouts']:
        if layout['uuid'] == uuid:
            layout['title'] = new_title
            modified = True
    
    if not modified:
        print(f"❌ 未找到 UUID 为 {uuid} 的组件")
        return False
    
    # 提交更新
    update_url = f"{base_url}/paas/bi-app/largeScreen/update/{screen_id}"
    config['id'] = screen_id
    resp = requests.post(update_url, json=config, headers=headers)
    result = resp.json()
    
    if result.get('result') == '0':
        print(f"✅ 组件标题已修改为：{new_title}")
        print(f"访问 URL: {base_url}/largescreenpreview?id={screen_id}")
        return True
    else:
        print(f"❌ 更新失败：{result.get('desc')}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="修改大屏组件标题")
    parser.add_argument("--screen-id", type=int, required=True, help="大屏 ID")
    parser.add_argument("--uuid", required=True, help="组件 UUID")
    parser.add_argument("--title", required=True, help="新标题")
    parser.add_argument("--base-url", default="https://dev.cloud.hecom.cn/biserver", help="API 基础 URL")
    args = parser.parse_args()
    
    rename_component(args.screen_id, args.uuid, args.title, args.base_url)
```

使用方式:
```bash
python3 scripts/rename_component.py \
  --screen-id 3654218321 \
  --uuid "grid-type:bar-uuid:1773823950771" \
  --title "月度收款趋势分析"
```

---

## 最佳实践总结

### 布局规划模板 (1920×1080)

```
┌────────────────────────────────────────────────────────────┐
│ 顶部区域：top=30, height=140                               │
│ [8 个指标卡] 220×140, 间距 20px                            │
├────────────────────────────────────────────────────────────┤
│ 中部区域：top=200, height=500                              │
│         [主图表] 1100×500 (居中，left=410)                 │
├────────────────────────────────────────────────────────────┤
│ 底部区域：top=720, height=300                              │
│ [4 个图表并排] 每个 460×300, 间距 20px                     │
└────────────────────────────────────────────────────────────┘
```

### 坐标计算公式

```python
# 居中计算
center_left = (canvas_width - component_width) // 2

# 等分布局
margin = 20  # 边距
gap = 20     # 间距
count = 4    # 组件数量
width = (1920 - margin * 2 - gap * (count - 1)) // count

for i in range(count):
    left = margin + i * (width + gap)
    print(f"组件{i+1}: left={left}, width={width}")
```

### 常用组件尺寸参考

| 组件类型 | 宽度 | 高度 | 说明 |
|---------|------|------|------|
| 指标卡 | 220 | 140 | 顶部展示，高度要足够 |
| 主图表 | 1100 | 500 | 视觉焦点，居中 |
| 底部图表 | 460 | 300 | 4 个并排，均匀分布 |
| 侧边图表 | 550 | 300 | 2-3 个并排 |

### 检查清单

创建大屏前检查：
- [ ] 规划好所有组件位置和尺寸
- [ ] 计算好坐标，确保不重叠
- [ ] 预留足够间距（至少 20px）
- [ ] 准备好组件名称列表
- [ ] 确认指标卡高度≥140px

创建后检查：
- [ ] 使用 `--show-info` 查看所有组件位置
- [ ] 检查是否有重叠
- [ ] 确认图表标题正确
- [ ] 验证数据是否正常显示
