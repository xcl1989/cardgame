[English](./README_en.md) | 中文

# 卡牌消除游戏 (Card Game)

基于 HTML5 Canvas 和原生 JavaScript 的卡牌消除对战游戏。

## 截图

![登录页面](./docs/login.png)
![主菜单](./docs/main.png)
![队伍列表](./docs/team.png)
![编辑队伍](./docs/team-edit.png)
![选择关卡](./docs/level-select.png)

## 项目结构

```
cardgame/
├── front/               # 前端 (原生 JS + HTML5 Canvas)
│   ├── index.html       # 对战页面
│   ├── login.html       # 登录页面
│   ├── main.html      # 主菜单
│   ├── team-edit.html # 队伍编辑
│   ├── game/
│   │   └── main.js   # 核心游戏逻辑
│   ├── package.json
│   └── vite.config.js
├── server/             # 后端 (Python FastAPI)
│   ├── main.py         # API 接口
│   ├── database.py    # 数据库操作
│   ├── init_database.sql  # 数据库初始化
│   └── requirements.txt
├── assets/             # 静态资源
├── images/             # 图片资源
└── pages/             # 其他页面
```

## 部署

### 1. 启动 MySQL

```bash
# macOS
brew services start mysql
# 或其他方式启动 MySQL
```

### 2. 启动 Redis

```bash
# macOS
brew services start redis
# 或其他方式启动 Redis
```

### 3. 初始化数据库

```bash
cd server
mysql -uroot -p12345678 Game < init_database.sql
```

### 4. 启动后端

```bash
cd server
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8090
```

### 5. 启动前端

```bash
cd front
npm install
npm run dev      # 访问 http://localhost:8080
```

## 代码规范

- 类名: PascalCase (如 `Game`, `Player`)
- 常量: UPPER_SNAKE_CASE (如 `GRID`, `CELL`)
- 变量/函数: camelCase (如 `isDragging`, `createBoard()`)
- CSS 类名: kebab-case (如 `game-container`)
- 缩进: 4 空格

## 测试账号

- 用户名: 17380534281
- 密码: 123456
