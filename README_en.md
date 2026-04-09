English | [中文](./README.md)

# Card Match 3

A vanilla JavaScript card match-3 battle game using HTML5 Canvas, featuring multi-character teams, skills, and multi-wave BOSS battles.

## Screenshots

> Coming soon

## Project Structure

```
cardgame/
├── front/                     # Frontend (Vanilla JS + HTML5 Canvas + Vite)
│   ├── common/               # Shared modules
│   │   ├── auth.js           # Auth & API wrapper
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
│   ├── characters.html        # Character list
│   ├── team.html             # Team list
│   ├── team-edit.html        # Edit team
│   ├── team-select.html      # Select team
│   ├── level-select.html     # Select level
│   ├── package.json
│   └── vite.config.js
├── server/                   # Backend (Python FastAPI)
│   ├── main.py              # API endpoints
│   ├── database.py          # Database operations
│   ├── init_database.sql     # Database init
│   ├── init_levels.sql       # Level data
│   └── requirements.txt
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
cd server
mysql -uroot -p12345678 Game < init_database.sql
mysql -uroot -p12345678 Game < init_levels.sql
```

### 4. Start Backend

```bash
cd server
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8090
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
- **Skill System**: Each character has passive and active skills; active skills can be triggered manually during battle
- **Level Design**: Multi-wave enemies, BOSS battles

## Tech Stack

- **Frontend**: Vanilla JavaScript (ES6+), HTML5 Canvas, Vite
- **Backend**: Python FastAPI, MySQL, Redis
- **Communication**: REST API + JWT Token

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
