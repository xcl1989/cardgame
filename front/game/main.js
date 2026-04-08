// 卡牌消除游戏
// 核心：手指按下→滑动到另一珠子→松手=交换位置→检查消除→掉落→连锁

const BALL_COLORS = ['#ff4444', '#4488ff', '#44ff44', '#ffff44', '#888888'];
const BALL_TYPES = ['melee', 'ranged', 'heal', 'magic', 'invalid'];
const GRID = 5;
const CELL = 60;

const TYPE_MAP = { 1: 'melee', 2: 'ranged', 3: 'magic' };
const TYPE_NAMES = { 1: '战士', 2: '弓箭手', 3: '法师' };
const TYPE_COLORS = { 1: '#ff4444', 2: '#4488ff', 3: '#ffff44' };

const BASE_CONFIG = {
    playerHp: 100,
    playerDefense: 0,
    timeLimit: 5000,
    baseDamage: { melee: 6, ranged: 5, magic: 5 },
    baseHeal: 5,
    ballProbability: { melee: 0.2, ranged: 0.2, heal: 0.2, magic: 0.2, invalid: 0.2 },
    chainLightningBonus: false,
    enemyHp: 500,
    enemyName: '敌人',
    enemyAttack: 20,
};

class Game {
    constructor(config = GAME_CONFIG) {
        this.config = config;
        this.container = document.querySelector('#board-section');
        if (!this.container) {
            console.error('board-section not found!');
            return;
        }
        
        window.addEventListener('beforeunload', () => this.stopTimer());
        
        this.characters = this.config.characters.map(c => ({ ...c, hp: 100 }));
        this.canvas = document.createElement('canvas');
        this.canvas.width = 310;
        this.canvas.height = 350;
        this.ctx = this.canvas.getContext('2d');
        this.container.appendChild(this.canvas);
        
        this.board = [];
        this.playerHp = this.config.playerHp;
        this.enemies = this.config.enemies || [{ enemy_name: '敌人', hp: 500, attack: 20, defense: 0 }];
        this.currentEnemyIndex = 0;
        this.enemyHp = this.enemies[0].hp;
        this.enemyName = this.enemies[0].enemy_name;
        this.enemyAttack = this.enemies[0].attack;
        this.enemyDefense = this.enemies[0].defense || 0;
        this.startX = (310 - GRID * CELL) / 2;
        this.startY = 40;
        
        this.isSwapping = false;
        this.swapBall1 = null;
        this.swapBall2 = null;
        this.swapProgress = 0;
        
        this.combo = 0;
        this.showCombo = 0;
        this.showComboTime = 0;
        
        this.isDragging = false;
        this.dragBall = null;
        this.dragX = 0;
        this.dragY = 0;
        this.lastCell = null;
        
        this.isProcessing = false;
        
        this.isDropping = false;
        this.dropData = null;
        
        this.isTimerRunning = false;
        this.timeLeft = this.config.timeLimit;
        this.timeBarStart = 0;
        
        this.damageTexts = [];
        
        this.isVictory = false;
        this.isGameOver = false;
        this.skillUsed = [false, false, false, false];
        this.attackMultiplier = 1;
        this.enemyDefenseReduction = 0;
        
        this.init();
    }
    
    init() {
        this.updateCharacterDisplay();
        this.createBoard();
        this.draw();
        
        this.canvas.style.touchAction = 'none';
        this.canvas.onpointerdown = e => this.onDown(e);
        this.canvas.onpointermove = e => this.onMove(e);
        this.canvas.onpointerup = e => this.onUp(e);
        this.canvas.onpointercancel = e => this.onUp(e);
        this.canvas.onpointerleave = e => this.onUp(e);
        
        for (let i = 0; i < 4; i++) {
            const charBox = document.getElementById(`char-${i}`);
            if (charBox) {
                charBox.onclick = () => this.onCharBoxClick(i);
            }
        }
    }
    
    onCharBoxClick(index) {
        if (this.isProcessing || this.isVictory || this.isGameOver) return;
        const char = this.characters[index];
        if (char && char.active_skill && !this.skillUsed[index]) {
            showSkillModal(index);
        }
    }
    
    useActiveSkill(charIndex) {
        const char = this.characters[charIndex];
        if (!char || !char.active_skill || this.skillUsed[charIndex]) return;
        
        this.skillUsed[charIndex] = true;
        this.updateCharacterDisplay();
        
        const skillName = char.active_skill.name;
        let skillText = '';
        
        if (skillName.includes('战士专精')) {
            let targetType = 0;
            let changed = 0;
            for (let r = 0; r < GRID; r++) {
                for (let c = 0; c < GRID; c++) {
                    if (this.board[r][c] === 4) {
                        this.board[r][c] = targetType;
                        changed++;
                    }
                }
            }
            skillText = changed > 0 ? '技能发动！' : '没有无效珠子';
        } else if (skillName.includes('弓箭手专精')) {
            let targetType = 1;
            let changed = 0;
            for (let r = 0; r < GRID; r++) {
                for (let c = 0; c < GRID; c++) {
                    if (this.board[r][c] === 4) {
                        this.board[r][c] = targetType;
                        changed++;
                    }
                }
            }
            skillText = changed > 0 ? '技能发动！' : '没有无效珠子';
        } else if (skillName.includes('法师专精')) {
            let targetType = 3;
            let changed = 0;
            for (let r = 0; r < GRID; r++) {
                for (let c = 0; c < GRID; c++) {
                    if (this.board[r][c] === 4) {
                        this.board[r][c] = targetType;
                        changed++;
                    }
                }
            }
            skillText = changed > 0 ? '技能发动！' : '没有无效珠子';
        } else if (skillName === '回复') {
            const healAmount = Math.floor(this.config.playerHp * 0.6);
            this.playerHp = Math.min(this.config.playerHp, this.playerHp + healAmount);
            skillText = `回复 ${healAmount} HP！`;
            this.updateCharacterDisplay();
        } else if (skillName === '暴击') {
            this.attackMultiplier = 3;
            skillText = '暴击激活！本回合伤害x3';
        } else if (skillName === '精确打击') {
            this.enemyDefenseReduction = 5;
            this.updateEnemyHpDisplay();
            skillText = '精确打击！敌人防御-5';
        }
        
        if (skillText) {
            this.showSkillEffect(skillText);
        }
        this.draw();
    }
    
    showSkillEffect(text) {
        const ctx = this.ctx;
        ctx.fillStyle = 'rgba(0,0,0,0.5)';
        ctx.fillRect(0, 0, 310, 350);
        ctx.fillStyle = '#ffff44';
        ctx.font = 'bold 24px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(text, 155, 175);
        setTimeout(() => this.draw(), 800);
    }

    delay(ms) { return new Promise(r => setTimeout(r, ms)); }
    
    updateCharacterDisplay() {
        for (let i = 0; i < this.characters.length; i++) {
            const char = this.characters[i];
            const el = document.getElementById(`char-${i}`);
            if (el) {
                el.querySelector('.char-name').textContent = char.name;
                el.querySelector('.char-name').style.color = char.color;
                el.style.borderColor = char.color;
                
                el.classList.remove('has-skill', 'skill-used');
                let indicator = el.querySelector('.skill-indicator');
                if (!indicator) {
                    indicator = document.createElement('div');
                    indicator.className = 'skill-indicator';
                    el.appendChild(indicator);
                }
                indicator.style.display = 'none';
                
                if (char.active_skill) {
                    if (this.skillUsed[i]) {
                        el.classList.add('skill-used');
                        indicator.style.display = 'block';
                        indicator.style.background = '#666';
                    } else {
                        el.classList.add('has-skill');
                        indicator.style.display = 'block';
                        indicator.style.background = '#ffff44';
                    }
                }
            }
        }
        this.updateEnemyHpDisplay();
    }
    
    updateEnemyHpDisplay() {
        const fill = document.getElementById('enemy-hp-fill');
        const text = document.getElementById('enemy-hp-text');
        const label = document.querySelector('.enemy-hp-label');
        const stats = document.getElementById('enemy-stats');
        const currentEnemy = this.enemies[this.currentEnemyIndex];
        if (fill && text) {
            const percent = Math.max(0, (this.enemyHp / currentEnemy.hp) * 100);
            fill.style.width = `${percent}%`;
            text.textContent = `${Math.max(0, this.enemyHp)} / ${currentEnemy.hp}`;
            if (label) label.textContent = `${this.enemyName} (${this.currentEnemyIndex + 1}/${this.enemies.length})`;
            if (stats) {
                const effectiveDef = this.enemyDefense - this.enemyDefenseReduction;
                const defText = effectiveDef !== this.enemyDefense ? `${effectiveDef}(-${this.enemyDefenseReduction})` : `${this.enemyDefense}`;
                stats.textContent = `ATK: ${this.enemyAttack} | DEF: ${defText}`;
            }
        }
    }
    
    createBoard() {
        const prob = this.config.ballProbability;
        const types = ['melee', 'ranged', 'heal', 'magic', 'invalid'];
        const getRandomType = () => {
            let r = Math.random();
            let cumulative = 0;
            for (let i = 0; i < types.length; i++) {
                cumulative += prob[types[i]];
                if (r < cumulative) return i;
            }
            return 4;
        };
        
        for (let r = 0; r < GRID; r++) {
            this.board[r] = [];
            for (let c = 0; c < GRID; c++) {
                let type;
                do {
                    type = getRandomType();
                } while (this.wouldMatch(r, c, type));
                this.board[r][c] = type;
            }
        }
    }
    
    wouldMatch(r, c, type) {
        if (c >= 2 && this.board[r][c-1] === type && this.board[r][c-2] === type) return true;
        if (r >= 2 && this.board[r-1][c] === type && this.board[r-2][c] === type) return true;
        return false;
    }
    
    getCell(x, y) {
        const c = Math.floor((x - this.startX) / CELL);
        const r = Math.floor((y - this.startY) / CELL);
        if (r >= 0 && r < GRID && c >= 0 && c < GRID) return {r, c};
        return null;
    }
    
    onDown(e) {
        e.preventDefault();
        if (this.isProcessing || this.isSwapping) return;
        
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const cell = this.getCell(x, y);
        if (!cell) return;
        
        const type = this.board[cell.r][cell.c];
        if (type === null) return;
        
        this.isDragging = true;
        this.dragBall = {r: cell.r, c: cell.c, type: type};
        this.lastCell = {r: cell.r, c: cell.c};
        this.dragX = x;
        this.dragY = y;
        this.hasMoved = false;
        this.originalBoard = this.board.map(row => [...row]);
        
        this.draw();
    }
    
    onMove(e) {
        e.preventDefault();
        if (!this.isDragging || !this.dragBall) return;
        
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        this.dragX = x;
        this.dragY = y;
        
        const cell = this.getCell(x, y);
        if (!cell) {
            this.draw();
            return;
        }
        
        const {r, c} = cell;
        const last = this.lastCell;
        
        if (r === last.r && c === last.c) {
            this.draw();
            return;
        }
        
        const dr = Math.abs(last.r - r);
        const dc = Math.abs(last.c - c);
        const isAdjacent = (dr === 1 && dc === 0) || (dr === 0 && dc === 1) || (dr === 1 && dc === 1);
        
        if (isAdjacent) {
            const type2 = this.board[r][c];
            if (type2 !== null) {
                this.board[last.r][last.c] = type2;
                this.board[r][c] = this.dragBall.type;
                this.lastCell = {r, c};
                this.dragBall.r = r;
                this.dragBall.c = c;
                
                if (!this.hasMoved && !this.isTimerRunning) {
                    this.hasMoved = true;
                    this.startTimer();
                }
            }
        }
        
        this.draw();
    }
    
    onUp(e) {
        e.preventDefault();
        if (!this.isDragging) return;
        
        this.isDragging = false;
        this.dragBall = null;
        this.lastCell = null;
        
        if (this.hasMoved) {
            this.stopTimer();
            this.draw();
            this.process();
        } else if (this.originalBoard) {
            this.board = this.originalBoard;
            this.originalBoard = null;
            this.draw();
        }
    }
    
    startTimer() {
        this.isTimerRunning = true;
        this.timeLeft = this.config.timeLimit;
        this.timeBarStart = Date.now();
        this.timerInterval = setInterval(() => {
            this.timeLeft = Math.max(0, this.config.timeLimit - (Date.now() - this.timeBarStart));
            this.draw();
            if (this.timeLeft <= 0) {
                this.stopTimer();
                if (this.hasMoved) {
                    this.isDragging = false;
                    this.dragBall = null;
                    this.lastCell = null;
                    this.process();
                }
            }
        }, 50);
    }
    
    stopTimer() {
        this.isTimerRunning = false;
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }
    
    getX(c) { return this.startX + c * CELL + CELL/2; }
    getY(r) { return this.startY + r * CELL + CELL/2; }
    
    async process() {
        this.isProcessing = true;
        this.combo = 0;
        this.stopTimer();
        this.hasMoved = false;
        this.timeLeft = this.config.timeLimit;
        
        await this.chain();
        
        if (this.combo === 0 && this.originalBoard) {
            this.board = this.originalBoard;
            this.originalBoard = null;
            this.draw();
        }
        
        if (this.enemyHp <= 0) {
            this.enemyHp = 0;
            if (this.currentEnemyIndex < this.enemies.length - 1) {
                this.nextEnemy();
            } else {
                this.showVictory();
            }
        }
        this.isProcessing = false;
    }
    
    nextEnemy() {
        this.currentEnemyIndex++;
        const nextEnemyData = this.enemies[this.currentEnemyIndex];
        this.enemyHp = nextEnemyData.hp;
        this.enemyName = nextEnemyData.enemy_name;
        this.enemyAttack = nextEnemyData.attack;
        this.enemyDefense = nextEnemyData.defense || 0;
        this.attackMultiplier = 1;
        this.enemyDefenseReduction = 0;
        this.updateEnemyHpDisplay();
        this.showNextEnemyText();
    }
    
    showNextEnemyText() {
        const ctx = this.ctx;
        ctx.fillStyle = 'rgba(0,0,0,0.6)';
        ctx.fillRect(0, 0, 310, 350);
        ctx.fillStyle = '#ff4';
        ctx.font = 'bold 24px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`下一波: ${this.enemyName}`, 155, 160);
        this.draw();
    }
    
    async chain() {
        const combos = [];
        this.originalBoard = null;
        
        while (true) {
            const matchGroups = this.findAllMatchGroups();
            if (matchGroups.length === 0) break;
            
            for (const group of matchGroups) {
                this.combo++;
                const ballType = BALL_TYPES[group.type];
                const colorNames = { melee: '红', ranged: '蓝', heal: '绿', magic: '黄', invalid: '灰' };
                const colorName = colorNames[ballType] || '灰';
                
                if (ballType === 'heal') {
                    combos.push([colorName, group.cells.length, 'heal']);
                } else if (ballType !== 'invalid') {
                    combos.push([colorName, group.cells.length, ballType]);
                }
                
                for (const {r, c} of group.cells) {
                    this.board[r][c] = null;
                }
                
                this.showCombo = this.combo;
                this.showComboTime = Date.now();
                this.updateCharacterDisplay();
                this.draw();
                await this.delay(500);
            }
            
            this.showCombo = this.combo;
            this.showComboTime = Date.now();
            this.updateCharacterDisplay();
            this.draw();
            await this.delay(200);
            
            await this.drop();
        }
        
        if (this.combo > 0) {
            const comboMultiplier = 1 + (this.combo - 1) * 0.1;
            const chainLightningMultiplier = (this.combo >= 4 && this.config.chainLightningBonus) ? 1.5 : 1;
            let totalDamage = 0;
            const effectiveDefense = this.enemyDefense - this.enemyDefenseReduction;
            
            for (const [color, count, ballType] of combos) {
                if (ballType === 'heal') continue;
                let baseDamage = this.config.baseDamage[ballType];
                if (ballType === 'melee') {
                    baseDamage *= this.attackMultiplier;
                }
                const countMultiplier = 1 + (count - 3) * 0.3;
                const ballDamage = baseDamage * countMultiplier * comboMultiplier * chainLightningMultiplier;
                totalDamage += Math.max(0, ballDamage - effectiveDefense);
            }
            
            if (totalDamage > 0) {
                this.enemyHp -= Math.floor(totalDamage);
                this.updateEnemyHpDisplay();
                this.showDamageText(`-${Math.floor(totalDamage)}`);
            }
            
            let totalHeal = 0;
            for (const [color, count, ballType] of combos) {
                if (ballType !== 'heal') continue;
                const countMultiplier = 1 + (count - 3) * 0.3;
                totalHeal += this.config.baseHeal * countMultiplier * comboMultiplier;
            }
            
            if (totalHeal > 0) {
                this.playerHp = Math.min(this.config.playerHp, this.playerHp + Math.floor(totalHeal));
                this.updateCharacterDisplay();
                this.showHealText(`+${Math.floor(totalHeal)}`);
                this.draw();
            }
            
            this.attackMultiplier = 1;
            this.enemyDefenseReduction = 0;
            
            await this.delay(800);
            if (this.enemyHp <= 0) return;
            const damage = Math.max(0, this.enemyAttack - this.config.playerDefense);
            this.playerHp = Math.max(0, this.playerHp - damage);
            this.updateCharacterDisplay();
            if (damage > 0) {
                this.damageTexts.push({
                    text: `-${damage}`,
                    x: this.startX + (GRID * CELL) / 2,
                    y: 15,
                    alpha: 1,
                    vy: 0,
                    isHeal: false
                });
                this.animateDamageText();
            }
            this.draw();
            
            if (this.playerHp <= 0) {
                this.showGameOver();
            }
            
        }
    }
    
    showGameOver() {
        const ctx = this.ctx;
        ctx.fillStyle = 'rgba(0,0,0,0.8)';
        ctx.fillRect(0, 0, 310, 350);
        ctx.fillStyle = '#f44';
        ctx.font = 'bold 36px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('💀 挑战失败', 155, 140);
        ctx.font = 'bold 16px Arial';
        ctx.fillStyle = '#fff';
        ctx.fillText('重新挑战', 155, 200);
        ctx.fillStyle = '#aaa';
        ctx.font = 'bold 14px Arial';
        ctx.fillText('点击任意处返回主界面', 155, 240);
        
        this.isGameOver = true;
        this.canvas.onclick = (e) => {
            if (!this.isGameOver) return;
            
            const rect = this.canvas.getBoundingClientRect();
            const y = e.clientY - rect.top;
            
            if (y >= 180 && y <= 220) {
                this.restartBattle();
            } else {
                window.location.href = 'main.html';
            }
        };
    }
    
    restartBattle() {
        this.playerHp = this.config.playerHp;
        this.currentEnemyIndex = 0;
        this.enemyHp = this.enemies[0].hp;
        this.enemyName = this.enemies[0].enemy_name;
        this.enemyAttack = this.enemies[0].attack;
        this.enemyDefense = this.enemies[0].defense || 0;
        this.isGameOver = false;
        this.isVictory = false;
        this.combo = 0;
        this.showCombo = 0;
        this.hasMoved = false;
        this.stopTimer();
        this.timeLeft = this.config.timeLimit;
        this.characters = this.config.characters.map(c => ({ ...c, hp: 100 }));
        this.damageTexts = [];
        this.skillUsed = [false, false, false, false];
        this.attackMultiplier = 1;
        this.enemyDefenseReduction = 0;
        this.createBoard();
        this.updateEnemyHpDisplay();
        this.updateCharacterDisplay();
        this.draw();
    }
    
    showDamageText(text) {
        const el = document.getElementById('damage-text');
        if (!el) return;
        el.textContent = text;
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
        
        let startY = 0;
        const animate = () => {
            startY -= 1.5;
            el.style.transform = `translateY(${startY}px)`;
            el.style.opacity = `${1 - Math.abs(startY) / 80}`;
            if (Math.abs(startY) < 80) {
                requestAnimationFrame(animate);
            } else {
                el.textContent = '';
            }
        };
        requestAnimationFrame(animate);
    }
    
    showHealText(text) {
        this.damageTexts.push({
            text: text,
            x: this.startX + (GRID * CELL) / 2,
            y: 15,
            alpha: 1,
            vy: 0,
            isHeal: true
        });
        this.animateDamageText();
    }
    
    animateDamageText() {
        if (this._damageAnimating) return;
        this._damageAnimating = true;
        
        const animate = () => {
            this.draw();
            const hasActive = this.damageTexts.some(dt => dt.alpha > 0);
            if (hasActive) {
                requestAnimationFrame(animate);
            } else {
                this._damageAnimating = false;
            }
        };
        requestAnimationFrame(animate);
    }
    
    findAllMatchGroups() {
        const allMatches = [];
        
        for (let r = 0; r < GRID; r++) {
            let c = 0;
            while (c < GRID) {
                const type = this.board[r][c];
                if (type !== null) {
                    let count = 1;
                    while (c + count < GRID && this.board[r][c + count] === type) count++;
                    if (count >= 3) {
                        const cells = [];
                        for (let i = 0; i < count; i++) cells.push({r, c: c + i});
                        allMatches.push({type, cells});
                    }
                    c += count;
                } else {
                    c++;
                }
            }
        }
        
        for (let c = 0; c < GRID; c++) {
            let r = 0;
            while (r < GRID) {
                const type = this.board[r][c];
                if (type !== null) {
                    let count = 1;
                    while (r + count < GRID && this.board[r + count][c] === type) count++;
                    if (count >= 3) {
                        const cells = [];
                        for (let i = 0; i < count; i++) cells.push({r: r + i, c});
                        allMatches.push({type, cells});
                    }
                    r += count;
                } else {
                    r++;
                }
            }
        }
        
        if (allMatches.length === 0) return [];
        
        const groups = [];
        const cellToGroup = new Map();
        
        for (const match of allMatches) {
            const matchSet = new Set(match.cells.map(c => `${c.r},${c.c}`));
            const touchingGroups = [];
            
            for (const key of matchSet) {
                if (cellToGroup.has(key)) {
                    const gid = cellToGroup.get(key);
                    if (!touchingGroups.includes(gid)) touchingGroups.push(gid);
                }
            }
            
            if (touchingGroups.length === 0) {
                const newGroup = {type: match.type, cells: [...match.cells]};
                groups.push(newGroup);
                const gid = groups.length - 1;
                for (const c of match.cells) cellToGroup.set(`${c.r},${c.c}`, gid);
            } else {
                let mainGroup;
                if (touchingGroups.length === 1) {
                    mainGroup = groups[touchingGroups[0]];
                } else {
                    mainGroup = groups[touchingGroups[0]];
                    for (let i = 1; i < touchingGroups.length; i++) {
                        const oldGroup = groups[touchingGroups[i]];
                        for (const c of oldGroup.cells) {
                            cellToGroup.set(`${c.r},${c.c}`, touchingGroups[0]);
                        }
                        mainGroup.cells = mainGroup.cells.concat(oldGroup.cells);
                    }
                }
                for (const c of match.cells) {
                    if (!cellToGroup.has(`${c.r},${c.c}`)) {
                        cellToGroup.set(`${c.r},${c.c}`, touchingGroups[0]);
                    }
                }
                mainGroup.cells = mainGroup.cells.concat(match.cells);
            }
        }
        
        return groups;
    }
    
    async drop() {
        const dropInfo = [];
        const newBoard = [];
        
        for (let c = 0; c < GRID; c++) {
            const nonNull = [];
            for (let r = 0; r < GRID; r++) {
                if (this.board[r][c] !== null) {
                    nonNull.push({ type: this.board[r][c], fromR: r });
                }
            }
            
            const ballsToAdd = GRID - nonNull.length;
            const newBalls = [];
            for (let i = 0; i < ballsToAdd; i++) {
                newBalls.push({ type: Math.floor(Math.random() * 5), fromR: -(i + 1) });
            }
            
            const column = [...newBalls, ...nonNull];
            
            newBoard[c] = [];
            for (let r = 0; r < GRID; r++) {
                const ball = column[r];
                let distance;
                if (ball.fromR >= 0) {
                    distance = r - ball.fromR;
                } else {
                    distance = r + 1 - ball.fromR;
                }
                dropInfo.push({
                    r: r,
                    c: c,
                    type: ball.type,
                    distance: distance
                });
                newBoard[c][r] = ball.type;
            }
        }
        
        this.dropData = dropInfo;
        this.isDropping = true;
        
        const duration = 400;
        const start = Date.now();
        
        await new Promise(resolve => {
            const animate = () => {
                const elapsed = Date.now() - start;
                const p = Math.min(1, elapsed / duration);
                this.dropData.progress = p;
                this.draw();
                if (p < 1) {
                    requestAnimationFrame(animate);
                } else {
                    this.isDropping = false;
                    this.dropData = null;
                    for (let c = 0; c < GRID; c++) {
                        for (let r = 0; r < GRID; r++) {
                            this.board[r][c] = newBoard[c][r];
                        }
                    }
                    resolve();
                }
            };
            requestAnimationFrame(animate);
        });
    }
    
    draw() {
        if (this.isVictory || this.isGameOver) return;
        
        const ctx = this.ctx;
        ctx.fillStyle = '#2a2a4e';
        ctx.fillRect(0, 0, 310, 350);
        
        ctx.fillStyle = '#333';
        ctx.fillRect(this.startX, 10, GRID * CELL, 18);
        ctx.fillStyle = '#44ff44';
        ctx.fillRect(this.startX, 10, (this.playerHp / this.config.playerHp) * GRID * CELL, 18);
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`${Math.floor(this.playerHp)}/${this.config.playerHp}`, this.startX + (GRID * CELL) / 2, 24);
        
        ctx.fillStyle = '#444';
        ctx.fillRect(this.startX, 32, GRID * CELL, 6);
        ctx.fillStyle = '#4488ff';
        ctx.fillRect(this.startX, 32, (this.timeLeft / this.config.timeLimit) * GRID * CELL, 6);
        
        ctx.fillStyle = '#252545';
        ctx.fillRect(this.startX - 5, this.startY + 5, GRID * CELL + 10, GRID * CELL + 10);
        
        for (let r = 0; r < GRID; r++) {
            for (let c = 0; c < GRID; c++) {
                ctx.strokeStyle = '#3a3a5e';
                ctx.strokeRect(this.startX + c * CELL, this.startY + r * CELL, CELL, CELL);
            }
        }
        
        let offset1 = {x: 0, y: 0};
        let offset2 = {x: 0, y: 0};
        if (this.isSwapping && this.swapBall1 && this.swapBall2) {
            const p = this.swapProgress;
            const ease = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
            offset1.x = (this.swapBall2.x - this.swapBall1.x) * ease;
            offset1.y = (this.swapBall2.y - this.swapBall1.y) * ease;
            offset2.x = (this.swapBall1.x - this.swapBall2.x) * ease;
            offset2.y = (this.swapBall1.y - this.swapBall2.y) * ease;
        }
        
        const dropAnim = {};
        if (this.isDropping && this.dropData) {
            const p = this.dropData.progress;
            const ease = p * p * (3 - 2 * p);
            for (const d of this.dropData) {
                const startY = this.getY(d.r) - d.distance * CELL;
                const endY = this.getY(d.r);
                dropAnim[`${d.r},${d.c}`] = {
                    type: d.type,
                    y: startY + (endY - startY) * ease
                };
            }
        }
        
        for (let r = 0; r < GRID; r++) {
            for (let c = 0; c < GRID; c++) {
                let type = this.board[r][c];
                
                if (this.isDropping && this.dropData) {
                    const key = `${r},${c}`;
                    if (dropAnim[key]) {
                        type = dropAnim[key].type;
                    }
                }
                
                if (type === null) continue;
                
                let x = this.getX(c);
                let y = this.getY(r);
                
                if (this.isDropping && this.dropData) {
                    const key = `${r},${c}`;
                    if (dropAnim[key]) {
                        y = dropAnim[key].y;
                    }
                }
                
                if (this.isSwapping) {
                    if (this.swapBall1 && r === this.swapBall1.r && c === this.swapBall1.c) {
                        x += offset1.x;
                        y += offset1.y;
                    } else if (this.swapBall2 && r === this.swapBall2.r && c === this.swapBall2.c) {
                        x += offset2.x;
                        y += offset2.y;
                    }
                }
                
                if (this.dragBall && r === this.dragBall.r && c === this.dragBall.c) {
                    if (this.isDragging) {
                        x = this.dragX;
                        y = this.dragY;
                        ctx.shadowColor = BALL_COLORS[type];
                        ctx.shadowBlur = 20;
                    }
                }
                
                ctx.fillStyle = BALL_COLORS[type];
                ctx.beginPath();
                ctx.arc(x, y, CELL/2 - 4, 0, Math.PI * 2);
                ctx.fill();
                ctx.shadowBlur = 0;
                
                if (type === 4) {
                    ctx.strokeStyle = '#555';
                    ctx.lineWidth = 3;
                    ctx.beginPath();
                    ctx.moveTo(x - 8, y - 8);
                    ctx.lineTo(x + 8, y + 8);
                    ctx.moveTo(x + 8, y - 8);
                    ctx.lineTo(x - 8, y + 8);
                    ctx.stroke();
                }
            }
        }
        
        if (this.showCombo > 0 && Date.now() - this.showComboTime < 1500) {
            const alpha = 1 - (Date.now() - this.showComboTime) / 1500;
            ctx.fillStyle = `rgba(255,255,0,${alpha})`;
            ctx.font = 'bold 20px Arial';
            ctx.textAlign = 'right';
            ctx.fillText(`${this.showCombo} Combo!`, 300, 30);
        }
        
        for (let i = this.damageTexts.length - 1; i >= 0; i--) {
            const dt = this.damageTexts[i];
            dt.y += dt.vy;
            dt.alpha -= 0.02;
            if (dt.alpha <= 0) {
                this.damageTexts.splice(i, 1);
                continue;
            }
            ctx.fillStyle = `rgba(255,68,68,${dt.alpha})`;
            ctx.font = 'bold 24px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(dt.text, dt.x, dt.y);
        }
    }
    
    showVictory() {
        const ctx = this.ctx;
        ctx.fillStyle = 'rgba(0,0,0,0.8)';
        ctx.fillRect(0, 0, 310, 350);
        ctx.fillStyle = '#ff4';
        ctx.font = 'bold 36px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('🎉 关卡完成！', 155, 160);
        ctx.font = 'bold 18px Arial';
        ctx.fillText('点击返回主界面', 155, 200);

        this.isVictory = true;

        fetch(`/api/levels/${this.config.levelId}/complete`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        }).then(res => res.json()).then(data => {
            console.log('Level completed:', data);
        }).catch(err => {
            console.error('Failed to mark level complete:', err);
        });

        this.canvas.onclick = () => {
            if (this.isVictory) {
                window.location.href = 'main.html';
            }
        };
    }
    
    delay(ms) { return new Promise(r => setTimeout(r, ms)); }
}

function calculateBattleConfig(level, team) {
    const typeNames = { 1: '战士', 2: '弓箭手', 3: '法师' };
    const typeColors = { 1: '#ff4444', 2: '#4488ff', 3: '#ffff44' };
    const ballTypeMap = { 1: 'melee', 2: 'ranged', 3: 'magic' };
    
    const characters = [];
    let totalHp = 0;
    let totalDefense = 0;
    let totalTimeBonus = 0;
    let totalMeleeDamage = 0;
    let totalRangedDamage = 0;
    let totalMagicDamage = 0;
    let totalMeleeSkillBonus = 0;
    let totalRangedSkillBonus = 0;
    let totalMagicSkillBonus = 0;
    let totalHeal = 0;
    const typeCount = { 1: 0, 2: 0, 3: 0 };
    let chainLightningEquipped = false;
    
    function parseSkillEffect(skillName, effectValue) {
        const result = { hpBonus: 0, damageBonus: 0, healBonus: 0, timeBonus: 0, defenseBonus: 0, isChainLightning: false };
        if (!skillName) return result;
        if (!effectValue) return result;
        const val = parseFloat(effectValue) || 0;
        if (skillName.includes('力量增强')) { result.damageBonus = val; }
        else if (skillName.includes('耐打')) { result.hpBonus = val; }
        else if (skillName.includes('操作优化')) { result.timeBonus = val; }
        else if (skillName.includes('回复强化')) { result.healBonus = val; }
        else if (skillName.includes('连锁闪电')) { result.isChainLightning = true; }
        return result;
    }
    
    for (let i = 0; i < 4; i++) {
        const char = team.characters.find(c => c.slot_position === i);
        if (char) {
            const typeId = char.character_type_id;
            const type = ballTypeMap[typeId] || 'melee';
            typeCount[typeId] = (typeCount[typeId] || 0) + 1;
            
            const passiveEffect = parseSkillEffect(char.passive_skill_name, char.passive_effect_value);
            const activeEffect = parseSkillEffect(char.active_skill_name, char.active_effect_value);
            
            characters.push({
                type: type,
                name: char.character_name,
                color: typeColors[typeId] || '#ff4444',
                hp: char.hp || 100,
                typeId: typeId,
                defense: char.defense || 0,
                operation_time: char.operation_time || 1000,
                base_attack: char.base_attack || 5,
                passive_skill: char.passive_skill_name ? {
                    name: char.passive_skill_name,
                    desc: char.passive_skill_desc || '',
                    effect: passiveEffect
                } : null,
                active_skill: char.active_skill_name ? {
                    name: char.active_skill_name,
                    desc: char.active_skill_desc || '',
                    effect: activeEffect
                } : null
            });
            
            const hpBonus = passiveEffect.hpBonus + activeEffect.hpBonus;
            const damageBonus = passiveEffect.damageBonus + activeEffect.damageBonus;
            const healBonus = passiveEffect.healBonus + activeEffect.healBonus;
            const timeBonus = passiveEffect.timeBonus + activeEffect.timeBonus;
            
            if ((passiveEffect.isChainLightning || activeEffect.isChainLightning) && !chainLightningEquipped) {
                chainLightningEquipped = true;
            }
            
            totalHp += (char.hp || 100) + hpBonus;
            totalDefense += char.defense || 0;
            totalTimeBonus += timeBonus;
            totalHeal += healBonus;
            
            if (type === 'melee') {
                totalMeleeDamage += char.base_attack || 5;
                totalMeleeSkillBonus += damageBonus;
            } else if (type === 'ranged') {
                totalRangedDamage += char.base_attack || 5;
                totalRangedSkillBonus += damageBonus;
            } else if (type === 'magic') {
                totalMagicDamage += char.base_attack || 5;
                totalMagicSkillBonus += damageBonus;
            }
        }
    }
    
    if (characters.length === 0) {
        return {
            ...BASE_CONFIG,
            enemies: level.enemies || [{ enemy_name: '敌人', hp: 500, attack: 20 }],
            characters: [
                { type: 'melee', name: '战士', color: '#ff4444' },
                { type: 'melee', name: '战士', color: '#ff4444' },
                { type: 'ranged', name: '弓箭手', color: '#4488ff' },
                { type: 'magic', name: '魔法师', color: '#ffff44' }
            ]
        };
    }
    
    const ballProbability = {
        melee: 0.2,
        ranged: 0.2,
        heal: 0.2,
        magic: 0.2,
        invalid: 0.2
    };
    
    return {
        playerHp: totalHp,
        playerDefense: totalDefense,
        timeLimit: 5000 + totalTimeBonus,
        baseDamage: { 
            melee: Math.max(1, totalMeleeDamage + totalMeleeSkillBonus), 
            ranged: Math.max(1, totalRangedDamage + totalRangedSkillBonus), 
            magic: Math.max(1, totalMagicDamage + totalMagicSkillBonus) 
        },
        baseHeal: 5 + totalHeal,
        ballProbability: ballProbability,
        chainLightningBonus: chainLightningEquipped,
        enemies: level.enemies || [{ enemy_name: '敌人', hp: 500, attack: 20 }],
        levelId: level.id,
        characters: characters
    };
}

async function initGame() {
    const battleConfig = await loadBattleConfig();
    if (!battleConfig) {
        console.error('Failed to load battle config');
        return;
    }

    const { level, team } = battleConfig;
    const gameConfig = calculateBattleConfig(level, team);

    window.game = new Game(gameConfig);
    
    document.getElementById('loading-overlay').style.display = 'none';
    document.getElementById('battle-area').style.visibility = 'visible';
}

if (typeof loadBattleConfig === 'function') {
    initGame();
} else {
    window.onload = () => new Game(BASE_CONFIG);
}
