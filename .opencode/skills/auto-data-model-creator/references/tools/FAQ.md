# 常见问题与解决方案

## 认证相关

### 1. 认证文件不存在

**错误信息**:
```
❌ 错误：认证文件不存在：scripts/header.json
```

**解决方案**:
1. 复制示例文件：`cp scripts/header.json.example scripts/header.json`
2. 编辑 `scripts/header.json`，填入你的认证信息
3. 认证信息从浏览器开发者工具中获取（见 [快速开始](QUICKSTART.md)）

### 2. accessToken 过期

**错误信息**:
```
API 请求失败：401
```

**解决方案**:
1. 重新登录系统
2. 从浏览器开发者工具中获取新的 accessToken
   - 打开系统网页
   - 按 F12 打开开发者工具
   - 切换到 Network 标签
   - 找到任意 API 请求
   - 复制请求头中的 accessToken
3. 更新 `scripts/header.json`

### 3. 认证信息格式错误

**错误信息**:
```
API 请求失败：401
```

**解决方案**:
- 确保 `header.json` 是有效的 JSON 格式
- 检查是否有额外的空格或引号
- 确认所有必需字段都存在：accessToken, entCode, uid, empCode

## 节点和字段相关

### 4. 节点不存在

**错误信息**:
```
⚠️  警告：节点 xxx 不在可用节点列表中
```

**解决方案**:
1. 运行 `python3 scripts/get_nodes.py --list` 查看所有可用节点
2. 检查节点名称是否正确（使用 datasetName，如 project3X）
3. 确认节点类型（TABLE/BIZ_TYPE/OPTION）

### 5. 字段不存在

**错误信息**:
```
⚠️  警告：字段 xxx 不在节点 yyy 中
```

**解决方案**:
1. 运行 `python3 scripts/get_nodes.py detail --node-ids <节点 ID>` 查看字段详情
2. **重要**: 检查使用的是 fieldName 而不是 fieldLabel
   - fieldName: `code`, `name`, `project` (用于代码引用)
   - fieldLabel: `编码`, `项目编号`, `项目编号 (ID)` (显示标签)
3. 确认字段确实存在于该节点

### 6. 获取节点列表为空

**错误信息**:
```
✓ 已保存 0 个节点
```

**解决方案**:
1. 检查认证信息是否正确
2. 确认网络连接正常
3. 检查 API 响应：`curl -X POST ...` 手动测试 API

## 关联关系相关

### 7. 关联关系不生效

**原因**: 关联字段类型不匹配

**解决方案**:
- 主表字段应为 Text 类型（如 code）
- 外表字段应为 Join 类型（如 project）
- 检查 to/from 设置是否正确

**示例**:
```bash
# ✅ 正确：Text → Join
--relation "project3X.code:invoiceReg3X.project"

# ❌ 错误：Text → Text
--relation "project3X.code:invoiceReg3X.code"
```

### 8. 关联字段不存在

**错误信息**:
```
⚠️  警告：关联字段不存在 - project3X.xxx 或 invoiceReg3X.yyy
```

**解决方案**:
1. 检查字段名称是否使用 fieldName
2. 运行 `get_nodes.py` 查看实际字段列表
3. 确保关联的两个字段都存在

## 模型创建相关

### 9. 模型名称重复

**错误信息**:
```
保存失败：模型名称重复
```

**解决方案**:
- 使用唯一名称，如添加日期戳
- 示例：`"项目开票模型_20260319"` 或 `"项目开票模型_001"`

### 10. 数据集已被删除

**错误信息**:
```
保存失败：【项目信息】所对应的数据集已被删除，请检查配置！
```

**解决方案**:
1. 检查 datasetId 是否正确
2. 确认节点名称使用正确的 datasetName
3. 确保 `modelDatasetDTOList` 中包含 `datasetId` 字段
4. 重新获取节点列表：`python3 scripts/get_nodes.py --list`

### 11. 创建后模型不显示

**原因**: 可能创建失败或缓存问题

**解决方案**:
1. 运行 `python3 scripts/list_models.py --list` 刷新列表
2. 检查是否有错误信息
3. 查看详细日志确认是否成功

### 12. 模型详情显示字段数为 0

**说明**: 这是正常的。`listModelAll` 接口返回的模型详情中，字段数组可能为空，但模型结构已正确保存。

**验证方法**:
- 在系统中打开模型查看实际字段
- 检查 `modelDatasetDTOList` 中是否包含正确的节点配置

## 脚本执行相关

### 13. 脚本执行权限问题

**错误信息**:
```
Permission denied: ./scripts/create_model.py
```

**解决方案**:
```bash
# 添加执行权限
chmod +x scripts/*.py

# 或者直接用 python3 执行
python3 scripts/create_model.py ...
```

### 14. Python 版本问题

**错误信息**:
```
SyntaxError: invalid syntax
```

**解决方案**:
- 确保使用 Python 3.7+
- 检查版本：`python3 --version`
- 升级 Python（如需要）

### 15. 依赖库缺失

**错误信息**:
```
ModuleNotFoundError: No module named 'requests'
```

**解决方案**:
```bash
# 安装依赖
pip3 install requests
```

### 16. 缓存文件找不到

**错误信息**:
```
❌ 错误：文件不存在：scripts/.cache/xxx.json
```

**解决方案**:
1. 运行对应的 list/detail 命令生成缓存
2. 缓存目录可能被误删，重新执行命令即可
3. 缓存文件不是必需的，可以重新生成

### 17. 缓存数据过期

**问题**: 缓存的节点列表或模型列表不是最新的

**解决方案**:
- 删除缓存文件：`rm scripts/.cache/*.json`
- 重新运行 list 命令获取最新数据
- 缓存目录已在 `.gitignore` 中，删除不影响

## API 相关

### 18. API 响应没有 code 字段

**问题**: 某些 API 响应可能没有 `code` 字段，导致脚本判断失败

**解决方案**:
- 脚本已更新，不再依赖 `code` 字段
- 直接检查响应中是否包含 `data` 字段
- 如有问题，更新脚本到最新版本

### 19. API 返回未知错误

**错误信息**:
```
保存失败：未知错误
```

**解决方案**:
1. 检查详细的错误响应（使用 debug 模式）
2. 常见错误码：
   - `10005`: 模型中节点 name 重复
   - `10006`: 模型名称重复
   - `10011`: 数据集已被删除
3. 根据具体错误信息解决

## 最佳实践

### 20. 如何避免配置错误？

**推荐做法**:
1. ✅ 使用脚本自动构建配置（而不是手动编写 JSON）
2. ✅ 先用小数据量测试，确认无误后再正式使用
3. ✅ 保存设计方案和配置到缓存目录
4. ✅ 定期更新缓存，保持数据最新

### 21. 如何调试配置问题？

**调试步骤**:
1. 运行 `python3 scripts/get_nodes.py --list` 查看可用节点
2. 运行 `python3 scripts/get_nodes.py detail --node-ids <ID>` 查看字段详情
3. 检查 [配置结构文档](../api/config_structure.md) 确认配置格式
4. 查看详细错误日志

### 22. 如何快速修复配置？

**快速修复方法**:
1. 删除有问题的配置部分
2. 使用脚本重新生成：`python3 scripts/create_model.py create ...`
3. 或者逐步添加节点测试

### 23. 智能工作流中的常见问题

**Q: 大模型推荐的字段不存在怎么办？**

A: 使用 `get_nodes.py` 获取详细字段列表，让大模型基于真实字段重新推荐

**Q: 如何验证大模型的设计方案？**

A: 先用 `create_model.py` 创建测试模型，查看效果后再正式使用

**Q: 大模型推荐的关联关系不正确怎么办？**

A: 
1. 提供字段的类型信息（Text/Number/Join 等）
2. 说明关联规则：主表用 Text 字段，外表用 Join 字段
3. 示例提示词：
```
关联关系规则：
- 主表使用 Text 类型的编码字段（如 code）
- 外表使用 Join 类型的引用字段（如 project）
- 示例：project3X.code → invoiceReg3X.project
```

## 需要更多帮助？

- 📖 [快速开始](QUICKSTART.md) - 5 分钟入门
- 🔧 [命令速查](QUICK_REFERENCE.md) - 所有命令参考
- 🧠 [智能工作流](WORKFLOW.md) - 利用大模型能力
- 📚 [完整文档](../SKILL.md) - 详细使用说明

## 反馈问题

如果遇到以上未列出的问题，请：
1. 记录详细的错误信息（包括完整错误消息）
2. 保存相关的命令行输出
3. 检查认证信息是否正确
4. 查看 [配置结构文档](../api/config_structure.md) 确认配置格式
5. 尝试使用最新的脚本版本
