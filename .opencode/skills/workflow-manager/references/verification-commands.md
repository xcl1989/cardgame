# 验证命令

根据项目类型使用这些命令验证工作。

## JavaScript/TypeScript 项目

```bash
# 首先检查 package.json 是否存在
ls package.json

# 如存在，检查可用脚本
npm run lint      # ESLint
npm run typecheck # TypeScript 检查
npm run test      # 运行测试
npm run build     # 构建验证
```

## Python 项目

```bash
# 检查常见配置文件
ls setup.py pyproject.toml requirements.txt

# 运行验证
ruff check .           # Lint（如配置 ruff）
flake8 .               # Lint（如配置 flake）
python -m pytest       # 测试
python -m mypy .       # 类型检查
python -m black --check .  # 格式检查
```

## 通用检查

```bash
# Git 状态（提交前）
git status
git diff

# 文件存在性
ls -la <path>

# 目录结构
tree -L 2 <directory>
```

## 何时运行

- **代码变更后**：运行 lint/typecheck
- **完成功能后**：运行测试
- **最终交付前**：运行所有适用的验证
- **用户要求验证时**：运行相关命令

## 如无测试框架

如未配置测试或 lint：
1. 手动验证代码按预期工作
2. 检查明显错误（拼写、语法）
3. 确认所有需求已满足
4. 如建议自动化验证，告知用户
