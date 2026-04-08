# AGENTS.md

## Project Overview
This is a **vanilla JavaScript card-matching game** (卡牌消除游戏) using HTML5 Canvas.
No build system, testing framework, or linting is currently configured.

---

## Build & Run Commands

### Frontend (front/)
```bash
cd front
npm install
npm run dev      # Visit http://localhost:8080
```

### Backend (server/)
```bash
cd server
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8090
```

---

## Code Style Guidelines

### General
- **Language**: Vanilla JavaScript (ES6+), HTML5 Canvas
- **Indentation**: 4 spaces (verify with your editor)
- **Line endings**: LF

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `class Game`, `class Player` |
| Constants | UPPER_SNAKE_CASE | `const GRID = 5`, `const CELL = 60` |
| Variables/Functions | camelCase | `this.isDragging`, `createBoard()` |
| Private members | prefix with `_` | `this._cache` (optional) |
| CSS classes | kebab-case | `game-container`, `btn-green` |

### File Structure
```
cardgame/
├── front/
│   ├── index.html          # Battle page
│   ├── login.html          # Login page
│   ├── main.html           # Main menu
│   ├── game/
│   │   └── main.js         # Core game logic
│   ├── package.json
│   └── vite.config.js
├── server/
│   ├── main.py             # Backend API
│   ├── database.py         # Database operations
│   └── requirements.txt
└── AGENTS.md
```
├── assets/             # Static assets
├── images/             # Image resources
└── test.html           # Manual test page
```

### JavaScript Patterns
- **Class structure**: Use `class` with constructor for game objects
- **Event handling**: Use arrow functions for callbacks to preserve `this`
  ```javascript
  this.canvas.addEventListener('mousedown', e => this.onDown(e));
  ```
- **Async code**: Use `async/await` with `delay()` helper for animations
  ```javascript
  async process() {
      await this.delay(300);
      await this.drop();
  }
  ```
- **Canvas drawing**: Get context once, reuse `this.ctx`
- **Touch support**: Handle both mouse and touch events with same handlers

### Canvas Guidelines
- Fixed canvas size: 375×667 (mobile-first)
- Use `devicePixelRatio` scaling if needed for retina displays
- Cache calculations (e.g., `scaleX`, `scaleY`) in `getPos()`
- Use `ctx.save()`/`ctx.restore()` for complex drawings

### Error Handling
- Guard early returns for invalid states
  ```javascript
  onDown(e) {
      if (this.isProcessing) return;
      // ...
  }
  ```
- Validate array bounds before access
  ```javascript
  if (r >= 0 && r < GRID && c >= 0 && c < GRID) return {r, c};
  ```
- Use `Math.max(0, ...)` to prevent negative visual values

### Performance Tips
- Minimize canvas state changes (batch similar draw operations)
- Use `Set` for visited tracking in pathfinding
  ```javascript
  const visited = new Set();
  ```
- Avoid creating objects in hot loops (game loop)
- Use `requestAnimationFrame` for smooth animations if extending

### HTML/CSS Guidelines
- Use semantic HTML5 elements
- CSS: Use shorthand properties where possible
  ```css
  * { margin: 0; padding: 0; box-sizing: border-box; }
  ```
- Mobile-first viewport: `<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">`
- Use `passive: true` for touch event listeners where applicable

---

## Future Improvements (If Adding Tooling)

### Recommended additions for production:
1. **ESLint + Prettier** for code quality
2. **Jest or Vitest** for unit testing
3. **Vite or Rollup** for bundling
4. **TypeScript** for type safety

### Example ESLint config (.eslintrc.js):
```javascript
module.exports = {
  env: { browser: true, es2021: true },
  extends: 'eslint:recommended',
  parserOptions: { ecmaVersion: 'latest', sourceType: 'module' },
  rules: { indent: ['error', 4], quotes: ['error', 'single'] }
};
```

### Example test command (if Jest added):
```bash
npx jest --testPathPattern="game/"    # Run game tests
npx jest --testNamePattern="process"  # Run single test
```
