English | [中文](./README.md)

# Card Match 3

A vanilla JavaScript card match-3 battle game using HTML5 Canvas, featuring multi-character teams, skills, and multi-wave BOSS battles.

## Screenshots

![Login](./docs/login.png)
![Main Menu](./docs/main.png)
![Characters](./docs/characters.png)
![Team List](./docs/team.png)
![Edit Team](./docs/team-edit.png)
![Select Level](./docs/level-select.png)
![Battle](./docs/battle.png)

## Project Structure

```
cardgame/
├── front/                     # Frontend (Vanilla JS + HTML5 Canvas + Vite)
│   ├── common/               # Shared modules
│   │   ├── auth.js           # Auth & API wrapper (JWT Token)
│   │   ├── common.css        # Global styles & layout
│   │   └── utils.js          # Utilities (XSS escaping, loading, etc.)
│   ├── game/                 # Core game modules
│   │   ├── config.js        # Battle config calculation
│   │   ├── main.js           # Game entry point
│   │   ├── objects/          # Game objects
│   │   │   └── Board.js      # Board logic (create, match, drop)
│   │   ├── scenes/           # Scenes
│   │   │   └── BattleScene.js # Battle scene (rendering, interaction, skills)
│   │   └── utils/            # Utilities
│   │       ├── constants.js  # Constants (colors, types, dimensions)
│   │       └── helpers.js    # Helper functions
│   ├── index.html            # Battle page
│   ├── login.html            # Login page
│   ├── main.html             # Main menu
│   ├── characters.html       # Character list & summon
│   ├── team.html             # Team list
│   ├── team-edit.html        # Edit team
│   ├── team-select.html      # Select team
│   ├── level-select.html     # Select level
│   ├── package.json
│   └── vite.config.js
├── server/                   # Backend (Python FastAPI + SQLModel ORM)
│   ├── main.py              # API endpoints
│   ├── database.py          # Database operations (SQLModel ORM)
│   ├── models.py            # Database model definitions (11 tables)
│   ├── init_database.sql     # Database init (with seed data)
│   ├── requirements.txt
│   └── alembic/             # Database migrations
└── AGENTS.md                 # Development guidelines
```

## Quick Start

### 1. Start MySQL

```bash
brew services start mysql
```

### 2. Start Redis

```bash
brew services start redis
```

### 3. Initialize Database

```bash
mysql -uroot -pYOUR_PW Game < server/init_database.sql
```

### 4. Start Backend

```bash
cd server
cp .env.example .env          # edit MYSQL_PASSWORD etc.
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8090 --reload
```

### 5. Start Frontend

```bash
cd front
npm install
npm run dev      # Dev mode, visit http://localhost:8080
npm run build    # Production build
```

## Gameplay

- **Core Mechanic**: 5×5 grid, swap adjacent balls to trigger match-3
- **Ball Types**: Red (Warrior), Blue (Archer), Green (Heal), Yellow (Mage), Gray (Invalid)
- **Battle Flow**: Swap → Timer starts → Match chain → Damage/heal calc → Balls drop → Repeat
- **Character System**: Summon characters with rarity (Normal/Advanced/Rare/Legendary), stat bonuses, and unique bound skills for legendaries
- **Skill System**: Each character has passive and active skills
- **Team System**: 4-character parties, each character can be assigned passive and active skills
- **Level Design**: Multi-wave enemies, BOSS battles

## Tech Stack

- **Frontend**: Vanilla JavaScript (ES6+), HTML5 Canvas, Vite
- **Backend**: Python FastAPI, SQLModel ORM, MySQL, Redis
- **Communication**: REST API + JWT Token (Vite proxy /api → backend)

## Database Schema

| Table | Description | Primary Key |
|-------|-------------|-------------|
| users | Users | id (UUID) |
| character_types | Character types (Warrior/Archer/Mage) | id |
| skills | Skills | id |
| skill_character_map | Skill-character type mapping | (skill_id, character_type) |
| player_characters | Player characters | id (auto-increment) |
| teams | Teams | id (auto-increment) |
| team_character_map | Team-character mapping | (team_id, character_id, slot_position) |
| levels | Levels | id (auto-increment) |
| enemies | Enemies | id (auto-increment) |
| level_enemy_map | Level-enemy mapping | (level_id, enemy_id, slot_position) |
| name_pool | Random name pool | id (auto-increment) |
| user_level_progress | User level progress | id (auto-increment) |

## Code Style

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `Game`, `Board` |
| Constants | UPPER_SNAKE_CASE | `GRID`, `CELL` |
| Variables/Functions | camelCase | `isDragging`, `createBoard()` |
| CSS classes | kebab-case | `game-container` |
| Indentation | 4 spaces | — |

## Test Account

- Username: `xcl1989`
- Password: `123456`