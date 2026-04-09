English | [中文](./README.md)

# Card Match 3

A vanilla JavaScript card match-3 battle game using HTML5 Canvas.

## Screenshots

![Login](./docs/login.png)
![Main Menu](./docs/main.png)
![Team List](./docs/team.png)
![Edit Team](./docs/team-edit.png)
![Select Level](./docs/level-select.png)
![Battle](./docs/battle.png)

## Project Structure

```
cardgame/
├── front/               # Frontend (Vanilla JS + HTML5 Canvas)
│   ├── index.html       # Battle page
│   ├── login.html       # Login page
│   ├── main.html       # Main menu
│   ├── team-edit.html  # Team edit
│   ├── game/
│   │   └── main.js    # Core game logic
│   ├── package.json
│   └── vite.config.js
├── server/              # Backend (Python FastAPI)
│   ├── main.py         # API endpoints
│   ├── database.py     # Database operations
│   ├── init_database.sql  # Database init
│   └── requirements.txt
├── assets/              # Static assets
├── images/              # Image resources
└── pages/               # Additional pages
```

## Deployment

### 1. Start MySQL

```bash
# macOS
brew services start mysql
```

### 2. Start Redis

```bash
# macOS
brew services start redis
```

### 3. Initialize Database

```bash
cd server
mysql -uroot -p12345678 Game < init_database.sql
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
npm run dev      # Visit http://localhost:8080
```

## Test Account

- Username: xcl1989
- Password: 123456

## Code Style

- Classes: PascalCase (e.g., `Game`, `Player`)
- Constants: UPPER_SNAKE_CASE (e.g., `GRID`, `CELL`)
- Variables/Functions: camelCase (e.g., `isDragging`, `createBoard()`)
- CSS classes: kebab-case (e.g., `game-container`)
- Indentation: 4 spaces
