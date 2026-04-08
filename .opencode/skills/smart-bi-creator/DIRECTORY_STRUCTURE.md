# Smart BI Creator 目录结构说明

## 目录组织

```
smart-bi-creator/
├── SKILL.md                      # 技能主文档（入口）
├── .gitignore                    # Git 忽略配置
├── CACHE_INFO.md                 # 缓存机制说明
├── 
├── scripts/                      # 可执行脚本（代码）
│   ├── .cache/                   # 缓存目录（不提交到 Git）
│   ├── header.json               # 认证配置文件
│   ├── add_component.py          # 添加组件脚本
│   ├── create_screen.py          # 创建大屏脚本
│   ├── delete_component.py       # 删除组件脚本
│   ├── get_model_data.py         # 获取模型数据脚本
│   ├── list_screens.py           # 获取大屏列表脚本
│   ├── rename_component.py       # 重命名组件脚本
│   └── update_screen.py          # 更新大屏配置脚本
│
└── references/                   # 参考文档（说明）
    ├── components/               # 组件使用指南
    │   ├── RANKING_COMPONENT_GUIDE.md      # 排名图组件指南
    │   └── HORIZONTAL_BAR_COMPONENT_GUIDE.md # 条形图组件指南
    │
    ├── layouts/                  # 布局与案例
    │   ├── CASE_STUDY.md         # 实战案例：大屏优化全流程
    │   └── case_study.md         # 实战案例（旧版）
    │   └── layout_template.md    # 布局模板参考
    │
    ├── tools/                    # 工具使用文档
    │   ├── QUICKSTART.md         # 5 分钟快速开始
    │   ├── QUICK_REFERENCE.md    # 快速参考手册
    │   ├── WORKFLOW.md           # 智能工作流指南
    │   ├── FAQ.md                # 常见问题与解决方案
    │   ├── DELETE_COMPONENT_USAGE.md # 删除组件使用说明
    │   ├── UPDATE_LOG.md         # 更新日志
    │   └── README_PROBLEMS.md    # 已知问题说明
    │
    └── ...                       # 其他参考文档
        ├── config_structure.md   # 配置结构详解
        ├── required_fields.md    # 必填字段说明
        ├── templates.md          # 示例配置模板
        └── model_api.md          # 数据模型 API 文档
```

## 文件分类说明

### scripts/ - 可执行脚本

存放所有可执行的 Python 脚本和配置文件：

| 文件 | 说明 |
|------|------|
| `add_component.py` | 向已有大屏添加新组件 |
| `create_screen.py` | 创建新大屏（支持 create 和 update） |
| `delete_component.py` | 从大屏中删除组件 |
| `get_model_data.py` | 获取模型列表和详细信息 |
| `list_screens.py` | 获取大屏列表、按名称搜索 |
| `rename_component.py` | 修改组件标题 |
| `update_screen.py` | 查看和更新大屏配置 |
| `header.json` | 认证配置文件（accessToken、entCode 等） |
| `.cache/` | 缓存目录（模型数据、大屏配置等，不提交到 Git） |

### references/components/ - 组件使用指南

存放各类型组件的详细使用说明：

| 文件 | 说明 |
|------|------|
| `RANKING_COMPONENT_GUIDE.md` | 排名图组件使用指南 |
| `HORIZONTAL_BAR_COMPONENT_GUIDE.md` | 条形图组件使用指南 |

**计划添加**：
- `DUAL_AXIS_COMPONENT_GUIDE.md` - 双轴图组件指南
- `FUNNEL_COMPONENT_GUIDE.md` - 漏斗图组件指南
- `GAUGE_COMPONENT_GUIDE.md` - 仪表盘组件指南
- `BAR_COMPONENT_GUIDE.md` - 柱状图组件指南
- `LINE_COMPONENT_GUIDE.md` - 折线图组件指南
- `PIE_COMPONENT_GUIDE.md` - 饼图组件指南
- `METRIC_COMPONENT_GUIDE.md` - 指标卡组件指南

### references/layouts/ - 布局与实战案例

存放布局规划、实战案例等相关文档：

| 文件 | 说明 |
|------|------|
| `CASE_STUDY.md` | 实战案例：大屏优化全流程 |
| `case_study.md` | 实战案例（旧版） |
| `layout_template.md` | 布局模板参考（1920×1080 画布） |

### references/tools/ - 工具使用文档

存放快速开始、工作流、常见问题等工具使用文档：

| 文件 | 说明 |
|------|------|
| `QUICKSTART.md` | 5 分钟快速开始指南 |
| `QUICK_REFERENCE.md` | 快速参考手册 |
| `WORKFLOW.md` | 智能工作流：利用大模型创建大屏 |
| `FAQ.md` | 常见问题与解决方案 |
| `DELETE_COMPONENT_USAGE.md` | 删除组件使用说明 |
| `UPDATE_LOG.md` | 更新日志 |
| `README_PROBLEMS.md` | 已知问题说明 |

### references/ - 其他参考文档

存放配置结构、API 文档等技术参考：

| 文件 | 说明 |
|------|------|
| `config_structure.md` | 大屏 JSON 配置结构详解 |
| `required_fields.md` | dimension/indicator 必填字段说明 |
| `templates.md` | 各类图表配置模板 |
| `model_api.md` | 数据模型 API 文档 |
| `CACHE_INFO.md` | 缓存机制说明（根目录） |

## 引用路径规则

### 从 SKILL.md 引用
```markdown
[组件指南](references/components/RANKING_COMPONENT_GUIDE.md)
[布局案例](references/layouts/CASE_STUDY.md)
[工具文档](references/tools/FAQ.md)
[参考文档](references/config_structure.md)
```

### 从 references/ 子目录引用
```markdown
# 从 components/ 目录
[技能主文档](../../SKILL.md)
[其他组件](./HORIZONTAL_BAR_COMPONENT_GUIDE.md)
[配置结构](../config_structure.md)

# 从 layouts/ 目录
[技能主文档](../../SKILL.md)
[布局模板](./layout_template.md)
[FAQ](../tools/FAQ.md)

# 从 tools/ 目录
[技能主文档](../../SKILL.md)
[实战案例](../layouts/CASE_STUDY.md)
[其他工具](./QUICKSTART.md)
```

## 文件命名规范

### 脚本文件（.py）
- 使用 `snake_case` 命名
- 示例：`add_component.py`, `create_screen.py`

### 文档文件（.md）
- 组件指南：`{组件名}_COMPONENT_GUIDE.md`（全大写）
- 工具文档：全大写，如 `QUICKSTART.md`, `FAQ.md`
- 参考文档：`snake_case`，如 `config_structure.md`
- 案例文档：`CASE_STUDY.md`（全大写）

## 缓存目录（.cache）

`scripts/.cache/` 目录用于存放临时缓存文件：

- `model_list.json` - 模型列表
- `model_info_{id}.json` - 模型详细信息
- `screen_config_{id}.json` - 大屏配置缓存

**注意**：缓存目录已在 `.gitignore` 中配置，不会被提交到 Git。

## 认证配置

`scripts/header.json` 存储 API 认证信息：

```json
{
  "accessToken": "your-access-token",
  "entCode": "your-enterprise-code",
  "uid": "your-user-id",
  "empCode": "your-emp-code",
  "app": "biapp",
  "clientTag": "web"
}
```

**注意**：实际项目中应使用环境变量或加密存储敏感信息。

## 文档维护

### 添加新组件指南
1. 在 `references/components/` 目录创建 `{组件名}_COMPONENT_GUIDE.md`
2. 在 `SKILL.md` 的"组件类型支持"表中添加说明
3. 在 `SKILL.md` 的"参考文档"中添加链接
4. 更新本文档的"计划添加"列表

### 添加新脚本
1. 在 `scripts/` 目录创建脚本文件
2. 确保脚本有 `if __name__ == "__main__":` 块
3. 在 `SKILL.md` 的"脚本工具"表中添加说明
4. 编写使用说明文档（放在 `references/tools/`）

### 更新引用路径
- 使用相对路径引用
- 从子目录向上引用使用 `../`
- 同级目录引用直接使用 `./文件名`

## 版本历史

- **2024-03-19**: 重构目录结构，分离脚本和文档
  - `scripts/` 只存放可执行脚本
  - `references/` 按类型分类存放文档
  - 更新所有引用路径
