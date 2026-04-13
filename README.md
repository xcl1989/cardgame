[English](./README_en.md) | 中文

# 卡牌三消游戏 (Card Match 3)

基于 HTML5 Canvas 和原生 JavaScript 的卡牌三消对战游戏，支持多角色、多技能、多关卡 BOSS 战。

## 截图

![登录页面](./docs/login.png)
![主菜单](./docs/main.png)
![角色列表](./docs/characters.png)
![队伍列表](./docs/team.png)
![编辑队伍](./docs/team-edit.png)
![选择关卡](./docs/level-select.png)
![战斗画面](./docs/battle.png)

## 项目结构

```
cardgame/
├── front/                     # 前端 (原生 JS + HTML5 Canvas + Vite)
│   ├── common/               # 公共模块
│   │   ├── auth.js           # 认证 & API 封装 (JWT Token)
│   │   ├── common.css         # 全局样式 & 布局
│   │   └── utils.js           # 工具函数 (XSS转义、loading等)
│   ├── game/                 # 游戏核心模块
│   │   ├── config.js         # 战斗配置计算
│   │   ├── main.js           # 游戏入口
│   │   ├── objects/           # 游戏对象
│   │   │   └── Board.js      # 棋盘逻辑 (创建、匹配、掉落)
│   │   ├── scenes/           # 场景
│   │   │   └── BattleScene.js # 战斗场景 (游戏逻辑)
│   │   ├── effects/          # 渲染 & 动画
│   │   │   ├── BattleRenderer.js  # Canvas 渲染
│   │   │   └── AnimationManager.js # 动画状态管理
│   │   └── utils/            # 工具
│   │       ├── constants.js  # 常量 (颜色、类型、尺寸)
│   │       └── helpers.js    # 辅助函数
│   ├── index.html            # 战斗页面
│   ├── login.html            # 登录页面
│   ├── main.html             # 主菜单
│   ├── characters.html       # 角色列表 & 召唤
│   ├── team.html             # 队伍列表
│   ├── team-edit.html        # 编辑队伍
│   ├── team-select.html      # 选择队伍
│   ├── level-select.html     # 选择关卡
│   ├── package.json
│   └── vite.config.js
├── server/                   # 后端 (Python FastAPI + SQLModel ORM)
│   ├── main.py              # API 接口 (含战斗进度持久化)
│   ├── database.py          # 数据库操作 (SQLModel ORM)
│   ├── models.py            # 数据库模型定义 (13张表)
│   ├── init_database.sql     # 数据库初始化 (含种子数据)
│   ├── requirements.txt
│   └── alembic/             # 数据库迁移
└── AGENTS.md                 # 开发规范文档
```

## 快速启动

### 1. 启动 MySQL

```bash
brew services start mysql
```

### 2. 启动 Redis

```bash
brew services start redis
```

### 3. 初始化数据库

```bash
mysql -uroot -pYOUR_PW Game < server/init_database.sql
```

### 4. 启动后端

```bash
cd server
cp .env.example .env          # 编辑 MYSQL_PASSWORD 等
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8090 --reload
```

### 5. 启动前端

```bash
cd front
npm install
npm run dev      # 开发模式，访问 http://localhost:8080
npm run build    # 生产构建
```

## 游戏玩法

- **核心机制**: 5×5 棋盘，滑动交换相邻珠子触发三消
- **珠子类型**: 红色(战士)、蓝色(弓箭手)、绿色(回复)、黄色(法师)、灰色(无效)
- **战斗流程**: 滑动 → 计时开始 → 三消连锁 → 伤害/回复计算 → 珠子掉落 → 重复
- **角色系统**: 召唤角色，角色有稀有度(普通/高级/稀有/传说)、属性加成、专属技能
- **技能系统**: 每个角色有被动技能和主动技能，传说角色绑定专属被动技能
- **队伍系统**: 4人编队，每个角色可配置被动和主动技能
- **关卡设计**: 多波次敌人，BOSS 战
- **章节系统**: 关卡按章节分组（新手村、哥布林森林等）
- **战斗进度**: 中途退出可继续，刷新页面自动恢复棋盘和血量状态
- **动画效果**: 消除闪光、受击震动、连锁闪电、敌人换波过渡、时间条闪烁等

## 技术栈

- **前端**: 原生 JavaScript (ES6+)、HTML5 Canvas、Vite
- **后端**: Python FastAPI、SQLModel ORM、MySQL、Redis
- **通信**: REST API + JWT Token (Vite 代理 /api → 后端)

## 数据库架构

| 表 | 说明 | 主键 |
|---|------|------|
| users | 用户 | id (UUID) |
| character_types | 角色类型 (战士/弓箭手/法师) | id |
| skills | 技能 | id |
| skill_character_map | 技能-角色类型关联 | (skill_id, character_type) |
| player_characters | 玩家角色 | id (自增) |
| teams | 队伍 | id (自增) |
| team_character_map | 队伍-角色关联 | (team_id, character_id, slot_position) |
| levels | 关卡 | id (自增) |
| enemies | 敌人 | id (自增) |
| level_enemy_map | 关卡-敌人关联 | (level_id, enemy_id, slot_position) |
| name_pool | 随机名字池 | id (自增) |
| user_level_progress | 用户关卡进度 | id (自增) |
| chapters | 章节 | id (自增) |
| battle_sessions | 战斗进度存档 | id (自增) |

## 代码规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 类名 | PascalCase | `Game`, `Board` |
| 常量 | UPPER_SNAKE_CASE | `GRID`, `CELL` |
| 变量/函数 | camelCase | `isDragging`, `createBoard()` |
| CSS 类名 | kebab-case | `game-container` |
| 缩进 | 4 空格 | — |

## 测试账号

- 用户名: `xcl1989`
- 密码: `123456`