# 脚本组件使用指南

## 概述

脚本组件允许使用 **JavaScript** 和 **ECharts** 代码创建完全自定义的图表。当大屏提供的基础组件无法满足需求时，可以使用脚本组件实现复杂的可视化效果。

## 核心变量

| 变量 | 说明 |
|------|------|
| `Data` | 数据数组，格式为 `[[维度, 指标1, 指标2, ...], ...]` |
| `myChart` | ECharts 实例 |
| `option` | ECharts 配置对象（最后调用 `myChart.setOption(option)`） |

## 基础用法

### 默认脚本示例

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type script \
  --top 200 --left 50 \
  --width 600 --height 400 \
  --view-name "收款趋势"
```

**默认脚本代码**（不指定 --script-code 时）：
```javascript
var xAxisData = Data.map(function(item) { return item[0]; });
var seriesData = Data.map(function(item) { return item[1]; });

option = {
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: xAxisData, axisLabel: { color: '#fff' } },
    yAxis: { type: 'value', axisLabel: { color: '#fff' } },
    series: [{ type: 'bar', data: seriesData, itemStyle: { color: '#0088FE' } }]
};

myChart.setOption(option);
```

### 自定义脚本示例

```bash
python3 scripts/add_component.py \
  --screen-id 3654239893 \
  --model-id 2597080602 \
  --dimension-field receivingDate \
  --indicator-field receivingAmount \
  --chart-type script \
  --top 200 --left 700 \
  --width 600 --height 400 \
  --view-name "累计收款表" \
  --script-code '
// 转换为累计值
var cumulativeData = Data.map(function(item, idx) {
    var sum = 0;
    for (var i = 0; i <= idx; i++) { sum += Data[i][1]; }
    return [item[0], sum];
});

var tabledata = cumulativeData.map(function(item) {
    return { value: [item[0], "收款金额", item[1], 1] };
});

option = {
    tooltip: { trigger: "item", formatter: function(item) { return item.value[2]; } },
    xAxis: { type: "category", data: cumulativeData.map(function(item) { return item[0]; }), show: false },
    yAxis: { type: "category", data: ["收款金额"], show: false },
    series: [{
        type: "custom",
        renderItem: function(params, api) {
            var width = api.size([1, 0])[0];
            var height = api.size([0, 1])[1];
            var x = api.coord([api.value(0), 0])[0];
            var y = api.coord([0, api.value(1)])[1];
            return {
                type: "group",
                children: [
                    { type: "rect", shape: { x: x, y: y, width: width, height: height }, style: { fill: "#08143E", stroke: "#334979", lineWidth: 1 } },
                    { type: "text", position: [x, y], style: { text: api.value(2), fontSize: 14, textAlign: "center", textVerticalAlign: "middle", fill: "#fff" } }
                ]
            };
        },
        data: tabledata
    }]
};
myChart.setOption(option);'
```

## 进阶技巧

### 1. 多指标数据

当配置多个指标时，Data 格式为 `[[维度, 指标1, 指标2], ...]`

```javascript
var xAxisData = Data.map(function(item) { return item[0]; });
var data1 = Data.map(function(item) { return item[1]);  // 第一个指标
var data2 = Data.map(function(item) { return item[2]);  // 第二个指标
```

### 2. 自定义渲染

使用 `type: 'custom'` 和 `renderItem` 实现完全自定义的图形

```javascript
series: [{
    type: 'custom',
    renderItem: function(params, api) {
        // api.coord([x, y]) 转换为画布坐标
        // api.size([width, height]) 获取尺寸
        return { type: 'group', children: [...] };
    },
    data: [...]
}]
```

### 3. 深色主题配色

在大屏深色背景下，文字建议使用白色 `#fff` 或浅灰色

```javascript
var C = {
    bg: "#0F0F1A",
    primary: "#6366F1",
    accent: "#22D3EE",
    text: "#F1F5F9",
    muted: "#64748B"
};
```

### 4. 动态轮播效果

使用 `setInterval` 实现自动轮播高亮

```javascript
var currentIdx = 0;
var chartType = 0;

function buildOpt(idx) {
    // ... 构建 option
    return option;
}

myChart.setOption(buildOpt(0));

setInterval(function() {
    currentIdx = (currentIdx + 1) % Data.length;
    myChart.setOption(buildOpt(currentIdx));
}, 3000);
```

### 5. 点击交互

使用 `myChart.getZr().on("click", ...)` 监听画布点击

```javascript
myChart.getZr().on("click", function(params) {
    var ex = params.offsetX, ey = params.offsetY;
    // 判断点击位置，执行相应操作
});
```

## 平台 API

### registerMap - 加载地图

**必须使用 `registerMap` 方法加载地图数据**，否则地图无法显示。

```javascript
registerMap({
    adcode: 100000,           // 地区编码
    adName: "中国",           // 地区名称
    callback: function(mapJson) {
        echarts.registerMap("中国", mapJson);
        // 在回调中设置 option
    }
});
```

**重要**：
- 必须在 `callback` 回调函数中调用 `myChart.setOption(option)`
- 支持 `geo` 坐标系，**不支持 `geo3D`**
- 使用 ES5 语法（`var`/普通函数）避免兼容性问题

**adcode 参考值**：

| adcode | 地区名称 | adcode | 地区名称 |
|--------|----------|--------|----------|
| 100000 | 中国 | 450000 | 广西壮族自治区 |
| 110000 | 北京市 | 460000 | 海南省 |
| 120000 | 天津市 | 500000 | 重庆市 |
| 130000 | 河北省 | 510000 | 四川省 |
| 140000 | 山西省 | 520000 | 贵州省 |
| 150000 | 内蒙古自治区 | 530000 | 云南省 |
| 210000 | 辽宁省 | 540000 | 西藏自治区 |
| 220000 | 吉林省 | 610000 | 陕西省 |
| 230000 | 黑龙江省 | 620000 | 甘肃省 |
| 310000 | 上海市 | 630000 | 青海省 |
| 320000 | 江苏省 | 640000 | 宁夏回族自治区 |
| 330000 | 浙江省 | 650000 | 新疆维吾尔自治区 |
| 340000 | 安徽省 | 710000 | 台湾省 |
| 350000 | 福建省 | 810000 | 香港特别行政区 |
| 360000 | 江西省 | 820000 | 澳门特别行政区 |
| 370000 | 山东省 | 371300 | 临沂市（地级市） |
| 410000 | 河南省 | 440100 | 广州市 |
| 420000 | 湖北省 | 440300 | 深圳市 |
| 430000 | 湖南省 | 330200 | 宁波市 |
| 440000 | 广东省 | 330100 | 杭州市 |

### 中国地图使用示例

```bash
python3 scripts/add_component.py \
  --screen-id 3654958357 \
  --model-id 2597080602 \
  --dimension-field province \
  --indicator-field receivingAmount \
  --chart-type script \
  --top 198 --left 445 \
  --width 1030 --height 610 \
  --view-name "收款分布地图" \
  --script-code '
registerMap({
    adcode: 100000,
    adName: "中国",
    callback: function(mapJson) {
        echarts.registerMap("中国", mapJson);
        
        var mapData = Data.map(function(item) {
            return { name: item[0], value: item[1] };
        });
        
        var maxVal = Math.max.apply(null, Data.map(function(d) { return d[1] || 0; }));
        
        option = {
            backgroundColor: "transparent",
            tooltip: {
                trigger: "item",
                formatter: function(params) {
                    return params.name + "<br>金额: " + (params.value || 0) + "万元";
                },
                backgroundColor: "rgba(48, 52, 103, 0.95)",
                borderColor: "#177DDC",
                textStyle: { color: "#fff" }
            },
            geo: {
                map: "中国",
                roam: false,
                zoom: 1.2,
                center: [105, 36],
                itemStyle: {
                    normal: {
                        areaColor: "#1a2a6c",
                        borderColor: "#00d2ff",
                        borderWidth: 1
                    },
                    emphasis: {
                        areaColor: "#00d2ff"
                    }
                },
                label: {
                    normal: { show: true, color: "#fff", fontSize: 10 },
                    emphasis: { show: true, color: "#fff", fontSize: 10 }
                }
            },
            visualMap: {
                min: 0,
                max: maxVal || 1000,
                text: ["高", "低"],
                textStyle: { color: "#A6ADD0" },
                calculable: true,
                left: 20,
                bottom: 30,
                inRange: {
                    color: ["#177DDC", "#00F5FF", "#00FF88"]
                }
            },
            series: [{
                name: "收款分布",
                type: "effectScatter",
                coordinateSystem: "geo",
                showEffectOn: "render",
                rippleEffect: { brushType: "stroke", scale: 4, period: 3 },
                itemStyle: {
                    normal: {
                        color: function(params) {
                            var val = params.value || 0;
                            return val > maxVal * 0.7 ? "#00F5FF" : val > maxVal * 0.3 ? "#177DDC" : "#1DBB6A";
                        },
                        shadowBlur: 10,
                        shadowColor: "#00d2ff"
                    }
                },
                emphasis: { scale: 3, color: "#ff0000" },
                data: mapData,
                symbolSize: 12
            }]
        };
        
        myChart.setOption(option);
    }
});'
```

**数据格式要求**：`[[省份名称, 金额], ...]` 如 `[["北京", 850], ["上海", 720], ...]`

### 省市地图示例（以临沂市为例）

```bash
python3 scripts/add_component.py \
  --screen-id 3654958357 \
  --model-id 2597080602 \
  --dimension-field city \
  --indicator-field receivingAmount \
  --chart-type script \
  --top 198 --left 445 \
  --width 1030 --height 610 \
  --view-name "临沂市项目分布" \
  --script-code '
registerMap({
    adcode: 371300,
    adName: "临沂市",
    callback: function(mapJson) {
        echarts.registerMap("临沂市", mapJson);
        
        var mapData = Data.map(function(item) {
            return { name: item[0], value: [item[5], item[6], item[1], item[2], item[3], item[4]] };
        });
        
        option = {
            backgroundColor: "transparent",
            tooltip: {
                trigger: "item",
                formatter: function(params) {
                    return params.name + "<br>金额: " + params.value[2] + "万元";
                },
                backgroundColor: "rgba(48, 52, 103, 0.95)",
                borderColor: "#177DDC",
                textStyle: { color: "#fff" }
            },
            geo: {
                map: "临沂市",
                roam: false,
                zoom: 1.2,
                itemStyle: {
                    normal: {
                        areaColor: "#1a2a6c",
                        borderColor: "#00d2ff",
                        borderWidth: 1
                    },
                    emphasis: {
                        areaColor: "#00d2ff"
                    }
                },
                label: {
                    normal: { show: true, color: "#fff", fontSize: 10 },
                    emphasis: { show: true, color: "#fff", fontSize: 10 }
                }
            },
            series: [{
                name: "项目",
                type: "effectScatter",
                coordinateSystem: "geo",
                showEffectOn: "render",
                rippleEffect: { brushType: "stroke", scale: 4, period: 3 },
                itemStyle: {
                    normal: {
                        color: function(params) {
                            var status = params.value[2];
                            return {
                                "未实施": "#727881",
                                "正常进行": "#1DBB6A",
                                "即将逾期": "#D9A802",
                                "滞后": "#E86452"
                            }[status] || "#00d2ff";
                        },
                        shadowBlur: 10,
                        shadowColor: "#00d2ff"
                    }
                },
                emphasis: { scale: 3, color: "#ff0000" },
                data: mapData,
                symbolSize: 14
            }]
        };
        
        myChart.setOption(option);
    }
});'
```

**数据格式要求**：`[[名称, 指标1, 指标2, ..., 经度, 纬度], ...]`

## 视觉效果增强技巧

### 1. 渐变填充

使用 `areaColor` + 线性渐变模拟立体感

```javascript
areaColor: {
    type: "linear",
    x: 0, y: 0, x2: 0, y2: 1,
    colorStops: [
        { offset: 0, color: "rgba(99,102,241,0.4)" },
        { offset: 1, color: "rgba(26,42,108,0.6)" }
    ]
}
```

### 2. 发光边框

设置 `shadowBlur` + `shadowColor` 实现霓虹效果

```javascript
itemStyle: {
    shadowBlur: 15,
    shadowColor: "rgba(0,245,255,0.3)"
}
```

### 3. 脉冲涟漪

`rippleEffect` 让数据点有呼吸动画

```javascript
rippleEffect: { brushType: "stroke", scale: 5, period: 4 }
```

### 4. 渐变散点

使用 `radialGradient` 让散点有光晕效果

```javascript
color: {
    type: "radial",
    x: 0.5, y: 0.5, r: 0.6,
    colorStops: [
        { offset: 0, color: "#fff" },
        { offset: 0.3, color: "#00F5FF" },
        { offset: 1, color: "#6366F1" }
    ]
}
```

## 常见问题

### Q1: 脚本报错 "Cannot read properties of undefined"

- 检查变量是否正确声明
- 确保使用 `var` 而不是 `const/let`
- 使用普通函数而不是箭头函数

### Q2: 图表不显示

- 检查 `myChart.setOption(option)` 是否被调用
- 确保 `option` 结构完整
- 检查坐标轴配置是否正确

### Q3: 动画不生效

- 检查 `animation` 配置
- 确保 `setInterval` 在组件初始化后执行

### Q4: 地图显示空白

- 检查 `registerMap` 是否正确加载
- 确认 adcode 是否正确
- 检查 `geo` 配置的 `map` 名称是否与注册名称一致

## 参考资源

- [SKILL.md](../../SKILL.md) - 技能主文档
- [add_component.py](../scripts/add_component.py) - 组件添加脚本
