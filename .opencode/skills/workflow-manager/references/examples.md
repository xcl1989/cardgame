# 子代理分配实战示例

何时以及如何启动子代理的真实世界示例。

---

## 示例 1：全栈功能开发

**用户请求：**
> "添加一个用户个人资料页面，显示他们的订单历史并允许更新账户设置"

### 分析：
- **识别的子任务：**
  1. 研究现有 UI 组件模式
  2. 查找用户 API 端点
  3. 查找订单 API 端点
  4. 定位现有认证代码
  5. 实现前端组件
  6. 实现 API 集成
  7. 添加表单验证
  8. 测试功能

- **独立子任务：** 1-4（全部研究/探索）
- **依赖子任务：** 5-7（需要 1-4 的信息）
- **并行化评分：** 20/25（高）

### 子代理启动：

```
<launch_parallel_subagents>

**子代理 1：UI 组件研究**
- type: general
- description: 研究个人资料 UI 模式
- prompt: 研究 React 中用户个人资料页的最佳实践。查找：(1) 个人信息显示，(2) 可编辑表单字段，(3) 订单历史表格。返回推荐的组件结构及 shadcn/ui 或类似库的代码示例。

**子代理 2：用户 API 探索**
- type: explore
- description: 查找用户 API 代码
- thoroughness: medium
- prompt: 在代码库中搜索用户相关的 API 端点。查找：(1) 包含"user"和"api"或"route"的文件，(2) getUser、updateUser 函数，(3) 用户 schema 或模型定义。返回文件路径和端点 URL。

**子代理 3：订单 API 探索**
- type: explore
- description: 查找订单 API 代码
- thoroughness: medium
- prompt: 在代码库中搜索订单相关的 API 端点。查找：(1) 包含"order"和"api"或"route"的文件，(2) getOrders、getOrderHistory 函数，(3) 订单 schema 或模型定义。返回文件路径和端点 URL。

**子代理 4：认证模式发现**
- type: explore
- description: 查找认证代码
- thoroughness: quick
- prompt: 查找此代码库中如何处理认证。查找：(1) 认证中间件或守卫，(2) 会话/令牌管理代码，(3) 受保护路由示例。返回文件路径和关键函数名。

</launch_parallel_subagents>
```

### 子代理返回后：

1. **综合**：合并所有收集的信息
2. **规划**：为实现创建待办列表
3. **执行**：使用研究构建功能
4. **验证**：测试完整功能

**节省时间：** 约 25 分钟（顺序研究需要 30+ 分钟，并行约 8 分钟）

---

## 示例 2：代码库迁移分析

**用户请求：**
> "我们想从 Redux 迁移到 Zustand。分析我们的代码库并创建迁移计划"

### 分析：
- **识别的子任务：**
  1. 统计代码库中 Redux 使用情况
  2. 查找所有 Redux slice/reducer
  3. 识别 Redux selector 使用
  4. 识别 Redux dispatch 模式
  5. 研究 Zustand 迁移模式
  6. 创建迁移策略

- **独立子任务：** 1-5（全部分析/研究）
- **依赖子任务：** 6（需要所有前面的分析）
- **并行化评分：** 22/25（非常高）

### 子代理启动：

```
<launch_parallel_subagents>

**子代理 1：Redux Slice 发现**
- type: explore
- description: 查找 Redux slice
- thoroughness: very thorough
- prompt: 查找代码库中的所有 Redux slice/reducer。搜索：(1) 包含 createSlice 的文件，(2) configureStore 使用，(3) store 设置文件。返回所有 slice 的完整列表，包含文件路径和导出的 action。

**子代理 2：Redux Selector 映射**
- type: explore
- description: 查找 Redux selector
- thoroughness: very thorough
- prompt: 查找所有 Redux selector 使用。搜索：(1) 从 store 或 slice 导入的文件，(2) useSelector hooks，(3) createSelector 使用。返回所有 selector 的列表及使用位置。

**子代理 3：Redux Action/Dispatch 分析**
- type: explore
- description: 查找 dispatch 模式
- thoroughness: very thorough
- prompt: 查找所有 Redux dispatch 使用。搜索：(1) useDispatch hooks，(2) dispatch() 调用，(3) action creator。返回整个代码库中如何 dispatch action 的示例。

**子代理 4：Zustand 迁移研究**
- type: general
- description: 研究 Redux 到 Zustand
- prompt: 研究从 Redux 到 Zustand 的迁移模式。提供：(1) Redux slice 与 Zustand store 的比较，(2) 常见模式的迁移示例，(3) 陷阱和最佳实践。包含展示 before/after 的代码示例。

</launch_parallel_subagents>
```

### 子代理返回后：

1. **编译**：创建全面的代码库分析文档
2. **策略**：制定分阶段迁移计划
3. **估算**：提供每个阶段的时间估算
4. **呈现**：向用户交付迁移计划

**节省时间：** 约 40 分钟（全面代码库探索顺序需要 50+ 分钟，并行约 15 分钟）

---

## 示例 3：多源数据分析

**用户请求：**
> "分析我们 Q4 在销售、市场和客户支持方面的表现，发现趋势和洞察"

### 分析：
- **识别的子任务：**
  1. 加载并分析销售数据
  2. 加载并分析市场数据
  3. 加载并分析支持数据
  4. 查找部门间相关性
  5. 创建可视化
  6. 编写洞察报告

- **独立子任务：** 1-3（每个数据集独立）
- **依赖子任务：** 4-6（需要所有分析完成）
- **并行化评分：** 18/25（中高）

### 子代理启动：

```
<launch_parallel_subagents>

**子代理 1：销售数据分析**
- type: general
- description: 分析 Q4 销售数据
- prompt: 分析 sales_q4.csv 中的 Q4 销售数据。执行：(1) 数据清洗和验证，(2) 计算关键指标（收入、增长、平均交易规模），(3) 识别顶级表现者和趋势，(4) 注意任何异常。返回带数字的摘要统计和关键发现。

**子代理 2：市场数据分析**
- type: general
- description: 分析 Q4 市场数据
- prompt: 分析 marketing_q4.csv 中的 Q4 市场数据。执行：(1) 数据清洗和验证，(2) 计算指标（CAC、各渠道 ROI、转化率），(3) 识别表现最佳渠道，(4) 注意趋势。返回带数字的摘要统计和关键发现。

**子代理 3：支持数据分析**
- type: general
- description: 分析 Q4 支持数据
- prompt: 分析 support_q4.csv 中的 Q4 客户支持数据。执行：(1) 数据清洗和验证，(2) 计算指标（工单量、解决时间、CSAT），(3) 识别常见问题，(4) 注意趋势。返回带数字的摘要统计和关键发现。

</launch_parallel_subagents>
```

### 子代理返回后：

1. **交叉引用**：查找相关性（如市场投入 → 销售增长）
2. **可视化**：创建显示趋势的图表
3. **综合**：编写全面洞察报告
4. **推荐**：基于发现建议行动

**节省时间：** 约 20 分钟（每个分析约 10 分钟，并行执行约 12 分钟 vs 顺序 30 分钟）

---

## 示例 4：API 集成项目

**用户请求：**
> "集成 Twilio SMS API 发送订单确认消息"

### 分析：
- **识别的子任务：**
  1. 研究 Twilio SMS API
  2. 查找订单 webhook/触发点
  3. 查找现有 API 集成模式
  4. 实现 Twilio 客户端
  5. 创建消息模板
  6. 添加错误处理
  7. 测试集成

- **独立子任务：** 1-3（全部研究）
- **依赖子任务：** 4-7（需要研究完成）
- **并行化评分：** 16/25（中等）

### 子代理启动：

```
<launch_parallel_subagents>

**子代理 1：Twilio API 研究**
- type: general
- description: 研究 Twilio SMS API
- prompt: 研究 Twilio 的 SMS API 发送消息。提供：(1) 认证设置，(2) 发送 SMS 的代码示例，(3) 必需参数，(4) 错误处理最佳实践，(5) 定价考虑。使用官方 Twilio 文档。

**子代理 2：订单触发发现**
- type: explore
- description: 查找订单完成代码
- thoroughness: medium
- prompt: 查找代码库中订单标记为完成或确认的位置。搜索：(1) 名为"completeOrder"、"confirmOrder"、"placeOrder"的函数，(2) 支付成功的 webhook 处理器，(3) 订单状态变更事件。返回文件路径和函数名。

**子代理 3：API 集成模式**
- type: explore
- description: 查找现有 API 集成
- thoroughness: quick
- prompt: 查找此代码库中如何集成外部 API。搜索：(1) 第三方 SDK 导入的文件，(2) API 客户端配置，(3) API 密钥的环境变量使用。返回现有集成模式示例。

</launch_parallel_subagents>
```

### 子代理返回后：

1. **设计**：规划集成架构
2. **实现**：编写 Twilio 集成代码
3. **测试**：用测试消息验证
4. **文档**：添加使用文档

**节省时间：** 约 15 分钟（研究阶段并行化）

---

## 示例 5：安全审计

**用户请求：**
> "审计我们的代码库是否有安全漏洞，特别是认证和数据处理方面"

### 分析：
- **识别的子任务：**
  1. 查找认证实现
  2. 搜索硬编码密钥
  3. 查找数据验证模式
  4. 检查 SQL 注入风险
  5. 检查 XSS 风险
  6. 研究安全最佳实践
  7. 编译发现和建议

- **独立子任务：** 1-6（全部探索/研究）
- **依赖子任务：** 7（需要所有发现）
- **并行化评分：** 23/25（非常高）

### 子代理启动：

```
<launch_parallel_subagents>

**子代理 1：认证实现审查**
- type: explore
- description: 查找认证代码
- thoroughness: very thorough
- prompt: 查找所有认证相关代码。搜索：(1) 登录/登出函数，(2) 会话管理，(3) 密码哈希，(4) JWT 处理，(5) OAuth 实现。返回文件路径并注意任何令人担忧的模式（明文密码、弱哈希等）。

**子代理 2：密钥检测**
- type: explore
- description: 搜索硬编码密钥
- thoroughness: very thorough
- prompt: 搜索硬编码密钥或 API 密钥。查找：(1) 类似 apiKey=、password=、secret= 的模式，(2) 看起来像 token 的长字母数字字符串，(3) 有实际值的.env 文件或配置文件。返回文件路径和可疑行。

**子代理 3：输入验证分析**
- type: explore
- description: 查找输入验证
- thoroughness: very thorough
- prompt: 查找输入验证代码。搜索：(1) 验证库（joi、yup、zod），(2) 手动验证函数，(3) 无验证的区域（直接数据库查询、文件上传）。返回验证模式示例和差距。

**子代理 4：SQL 注入风险评估**
- type: explore
- description: 查找 SQL 查询模式
- thoroughness: very thorough
- prompt: 查找数据库查询代码。搜索：(1) 原始 SQL 查询，(2) 查询中的字符串拼接，(3) 参数化查询使用。标记任何带字符串插值的原始 SQL 为高风险。返回文件路径和代码片段。

**子代理 5：XSS 风险评估**
- type: explore
- description: 查找 XSS 风险
- thoroughness: very thorough
- prompt: 查找潜在 XSS 漏洞。搜索：(1) dangerouslySetInnerHTML 使用，(2) v-html 指令，(3) 未转义用户输入渲染，(4) innerHTML 赋值。返回带风险评估的文件路径和代码片段。

**子代理 6：安全最佳实践研究**
- type: general
- description: 研究安全标准
- prompt: 研究 Web 应用的当前安全最佳实践。涵盖：(1) OWASP Top 10，(2) 认证安全，(3) 数据保护，(4) 常见漏洞。提供审计检查清单。

</launch_parallel_subagents>
```

### 子代理返回后：

1. **编译**：创建全面的安全报告
2. **优先级**：按严重程度排序漏洞
3. **推荐**：提供修复步骤
4. **呈现**：向用户交付审计发现

**节省时间：** 约 45 分钟（全面安全审计顺序需要 60+ 分钟，并行约 20 分钟）

---

## 关键要点

1. **研究和探索最适合并行** - 多个搜索/研究线索是独立的
2. **实现保持顺序** - 编写代码通常需要完整上下文
3. **复杂任务启动 3-5 个子代理** - 足够节省时间，又不会混乱
4. **编写具体提示** - 模糊的提示浪费子代理的潜力
5. **始终综合** - 你负责合并和呈现结果
