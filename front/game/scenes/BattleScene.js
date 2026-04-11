import {
    BALL_TYPES, GRID, CELL,
    CANVAS_WIDTH, CANVAS_HEIGHT
} from '../utils/constants.js';
import { delay } from '../utils/helpers.js';
import Board from '../objects/Board.js';
import AnimationManager from '../effects/AnimationManager.js';
import BattleRenderer from '../effects/BattleRenderer.js';

class BattleScene {
    constructor(config) {
        this.config = config;
        this.container = document.querySelector('#board-section');
        if (!this.container) {
            console.error('board-section not found!');
            return;
        }

        window.addEventListener('beforeunload', () => this.stopTimer());

        this.characters = this.config.characters.map(c => ({ ...c, hp: 100 }));
        this.canvas = document.createElement('canvas');
        this.canvas.width = CANVAS_WIDTH;
        this.canvas.height = CANVAS_HEIGHT;
        this.ctx = this.canvas.getContext('2d');
        this.container.appendChild(this.canvas);

        this.board = new Board(this.config.ballProbability);
        this.board.create();
        this.healFromInvalidBonus = this.config.healFromInvalidBonus || false;

        this.playerHp = this.config.playerHp;
        this.enemies = this.config.enemies || [{ enemy_name: '敌人', hp: 500, attack: 20, defense: 0 }];
        this.currentEnemyIndex = 0;
        this.enemyHp = this.enemies[0].hp;
        this.enemyName = this.enemies[0].enemy_name;
        this.enemyAttack = this.enemies[0].attack;
        this.enemyDefense = this.enemies[0].defense || 0;
        this.startX = (CANVAS_WIDTH - GRID * CELL) / 2;
        this.startY = 40;

        this.isSwapping = false;
        this.swapBall1 = null;
        this.swapBall2 = null;
        this.swapProgress = 0;

        this.combo = 0;

        this.isDragging = false;
        this.dragBall = null;
        this.dragX = 0;
        this.dragY = 0;
        this.lastCell = null;

        this.isProcessing = false;
        this._dirty = true;
        this._renderRafId = null;
        this._timerRafId = null;
        this.isTimerRunning = false;
        this.timeLeft = this.config.timeLimit;
        this.timeBarStart = 0;

        this.anim = new AnimationManager();
        this.renderer = new BattleRenderer(this.ctx, this);

        this.isVictory = false;
        this.isGameOver = false;
        this.skillUsed = [false, false, false, false];
        this.attackMultiplier = 1;
        this.enemyDefenseReduction = 0;

        this._initEvents();
        this.updateCharacterDisplay();
        this._startRenderLoop();
        this._playIntro();
    }

    async _playIntro() {
        this.anim.introAnimating = true;
        const savedGrid = this.board.grid.map(row => [...row]);
        for (let r = 0; r < GRID; r++) {
            for (let c = 0; c < GRID; c++) {
                this.board.grid[r][c] = null;
            }
        }
        this.draw();

        for (let c = 0; c < GRID; c++) {
            const dropInfo = [];
            for (let r = 0; r < GRID; r++) {
                dropInfo.push({ r, c, type: savedGrid[r][c], distance: GRID + 2 });
            }
            this.board.dropInfo = dropInfo;
            this.board.dropProgress = 0;

            await new Promise(resolve => {
                const start = Date.now();
                const duration = 300;
                const animate = () => {
                    const elapsed = Date.now() - start;
                    this.board.dropProgress = Math.min(elapsed / duration, 1);
                    this.draw();
                    if (elapsed < duration) {
                        requestAnimationFrame(animate);
                    } else {
                        resolve();
                    }
                };
                requestAnimationFrame(animate);
            });

            for (let r = 0; r < GRID; r++) {
                this.board.grid[r][c] = savedGrid[r][c];
            }
            this.board.dropInfo = null;
            this.board.dropProgress = 0;
        }

        this.anim.introAnimating = false;
        this.draw();
    }

    _startRenderLoop() {
        const loop = () => {
            if (this._dirty || this.anim.isAnimating(this.board)) {
                this._dirty = false;
                this.renderer.render();
            }
            this._renderRafId = requestAnimationFrame(loop);
        };
        this._renderRafId = requestAnimationFrame(loop);
    }

    draw() {
        this._dirty = true;
    }

    _getX(c) { return this.startX + c * CELL + CELL / 2; }
    _getY(r) { return this.startY + r * CELL + CELL / 2; }

    _initEvents() {
        this.canvas.style.touchAction = 'none';
        this.canvas.onpointerdown = e => this._onDown(e);
        this.canvas.onpointermove = e => this._onMove(e);
        this.canvas.onpointerup = e => this._onUp(e);
        this.canvas.onpointercancel = e => this._onUp(e);
        this.canvas.onpointerleave = e => this._onUp(e);

        for (let i = 0; i < 4; i++) {
            const charBox = document.getElementById(`char-${i}`);
            if (charBox) {
                charBox.onclick = () => this._onCharBoxClick(i);
            }
        }
    }

    _onCharBoxClick(index) {
        if (this.isProcessing || this.isVictory || this.isGameOver) return;
        const char = this.characters[index];
        if (char && char.active_skill && !this.skillUsed[index]) {
            if (typeof showSkillModal === 'function') {
                showSkillModal(index);
            }
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
            this._convertBallsAnimated(0);
            return;
        } else if (skillName.includes('弓箭手专精')) {
            this._convertBallsAnimated(1);
            return;
        } else if (skillName.includes('法师专精')) {
            this._convertBallsAnimated(3);
            return;
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
            this._updateEnemyHpDisplay();
            skillText = '精确打击！敌人防御-5';
        }

        if (skillText) this._showSkillEffect(skillText);
        this.draw();
    }

    async _convertBallsAnimated(targetType) {
        const targetCells = [];
        for (let r = 0; r < GRID; r++) {
            for (let c = 0; c < GRID; c++) {
                if (this.board.grid[r][c] === 4) {
                    targetCells.push({ r, c });
                }
            }
        }

        const skillText = targetCells.length > 0 ? '技能发动！' : '没有无效珠子';
        this._showSkillEffect(skillText);

        if (targetCells.length === 0) return;

        this.anim.startConverting(targetCells, targetType);

        await delay(350);

        for (const { r, c } of targetCells) {
            this.board.grid[r][c] = targetType;
        }
        this.anim.endConverting();
        this.draw();
    }

    _showSkillEffect(text) {
        const ctx = this.ctx;
        ctx.fillStyle = 'rgba(0,0,0,0.5)';
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
        ctx.fillStyle = '#ffff44';
        ctx.font = 'bold 24px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(text, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2);
        setTimeout(() => this.draw(), 800);
    }

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
        this._updateEnemyHpDisplay();
    }

    _applyHealFromInvalid() {
        if (!this.healFromInvalidBonus) return;
        const invalidPositions = [];
        for (let r = 0; r < this.board.grid.length; r++) {
            for (let c = 0; c < this.board.grid[r].length; c++) {
                if (this.board.grid[r][c] === 4) {
                    invalidPositions.push({ r, c });
                }
            }
        }
        if (invalidPositions.length === 0) return;
        const shuffle = invalidPositions.sort(() => Math.random() - 0.5);
        const count = Math.min(shuffle.length, Math.floor(Math.random() * 2) + 1);
        for (let i = 0; i < count; i++) {
            const { r, c } = shuffle[i];
            this.board.grid[r][c] = 2;
        }
    }

    _shakeEnemy() {
        const container = document.querySelector('.enemy-hp-container');
        if (!container) return;
        container.classList.remove('shake');
        void container.offsetWidth;
        container.classList.add('shake');
        setTimeout(() => container.classList.remove('shake'), 400);
    }

    _updateEnemyHpDisplay() {
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
                const defText = effectiveDef !== this.enemyDefense
                    ? `${effectiveDef}(-${this.enemyDefenseReduction})`
                    : `${this.enemyDefense}`;
                stats.textContent = `ATK: ${this.enemyAttack} | DEF: ${defText}`;
            }
        }
    }

    _onDown(e) {
        e.preventDefault();
        if (this.isProcessing || this.isSwapping || this.anim.introAnimating) return;

        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const cell = this.board.getCell(x, y, this.startX, this.startY);
        if (!cell) return;

        const type = this.board.grid[cell.r][cell.c];
        if (type === null) return;

        this.isDragging = true;
        this.dragBall = { r: cell.r, c: cell.c, type };
        this.lastCell = { r: cell.r, c: cell.c };
        this.dragX = x;
        this.dragY = y;
        this.hasMoved = false;
        this.originalBoard = this.board.clone();

        this.draw();
    }

    _onMove(e) {
        e.preventDefault();
        if (!this.isDragging || !this.dragBall) return;

        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        this.dragX = x;
        this.dragY = y;

        const cell = this.board.getCell(x, y, this.startX, this.startY);
        if (!cell) { this.draw(); return; }

        const { r, c } = cell;
        const last = this.lastCell;
        if (r === last.r && c === last.c) { this.draw(); return; }

        const dr = Math.abs(last.r - r);
        const dc = Math.abs(last.c - c);
        const isAdjacent = (dr === 1 && dc === 0) || (dr === 0 && dc === 1) || (dr === 1 && dc === 1);

        if (isAdjacent) {
            const type2 = this.board.grid[r][c];
            if (type2 !== null) {
                this.board.grid[last.r][last.c] = type2;
                this.board.grid[r][c] = this.dragBall.type;
                this.lastCell = { r, c };
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

    _onUp(e) {
        e.preventDefault();
        if (!this.isDragging) return;

        this.isDragging = false;
        this.dragBall = null;
        this.lastCell = null;

        if (this.hasMoved) {
            this.process();
        } else if (this.originalBoard) {
            this.board.grid = this.originalBoard;
            this.originalBoard = null;
            this.draw();
        } else {
            this.draw();
        }
    }

    _forceProcess() {
        this.isDragging = false;
        this.dragBall = null;
        this.lastCell = null;
        this.process();
    }

    startTimer() {
        this.isTimerRunning = true;
        this.timeLeft = this.config.timeLimit;
        this.timeBarStart = Date.now();

        const tick = () => {
            if (!this.isTimerRunning) return;
            this.timeLeft = Math.max(0, this.config.timeLimit - (Date.now() - this.timeBarStart));
            this._dirty = true;
            if (this.timeLeft <= 0) {
                this.stopTimer();
                if (this.hasMoved) {
                    this._forceProcess();
                }
                return;
            }
            this._timerRafId = requestAnimationFrame(tick);
        };
        this._timerRafId = requestAnimationFrame(tick);
    }

    stopTimer() {
        this.isTimerRunning = false;
        if (this._timerRafId) {
            cancelAnimationFrame(this._timerRafId);
            this._timerRafId = null;
        }
    }

    async process() {
        this.isProcessing = true;
        this.combo = 0;
        this.stopTimer();
        this.hasMoved = false;
        this.timeLeft = this.config.timeLimit;

        await this._chain();

        if (this.combo === 0 && this.originalBoard) {
            this.board.grid = this.originalBoard;
            this.originalBoard = null;
        }

        if (this.enemyHp <= 0) {
            this.enemyHp = 0;
            if (this.currentEnemyIndex < this.enemies.length - 1) {
                await this._nextEnemy();
            } else {
                this._showVictory();
            }
        }
        this.isProcessing = false;
    }

    async _nextEnemy() {
        this.currentEnemyIndex++;
        const nextEnemyData = this.enemies[this.currentEnemyIndex];
        this.enemyHp = nextEnemyData.hp;
        this.enemyName = nextEnemyData.enemy_name;
        this.enemyAttack = nextEnemyData.attack;
        this.enemyDefense = nextEnemyData.defense || 0;
        this.attackMultiplier = 1;
        this.enemyDefenseReduction = 0;
        this._updateEnemyHpDisplay();

        const ctx = this.ctx;
        let alpha = 0;
        const fadeOut = () => new Promise(resolve => {
            const step = () => {
                alpha += 0.05;
                if (alpha >= 0.7) { alpha = 0.7; resolve(); return; }
                ctx.fillStyle = `rgba(0,0,0,${alpha})`;
                ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
                requestAnimationFrame(step);
            };
            step();
        });
        await fadeOut();

        ctx.fillStyle = 'rgba(0,0,0,0.7)';
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
        ctx.fillStyle = '#ff4';
        ctx.font = 'bold 24px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`下一波: ${this.enemyName}`, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2);
        await delay(1200);
        this.draw();
    }

    async _chain() {
        const combos = [];
        this.originalBoard = null;

        while (true) {
            const matchGroups = this.board.findAllMatchGroups();
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

                this.anim.startClearing(group.cells.map(({ r, c }) => ({ r, c, type: this.board.grid[r][c] })));
                this.anim.showComboText(this.combo);

                if (this.combo >= 4 && this.config.chainLightningBonus) {
                    this.anim.startChainLightning(group.cells, this._getX.bind(this), this._getY.bind(this));
                }
                this.updateCharacterDisplay();
                this.draw();
                await delay(300);

                for (const { r, c } of group.cells) {
                    this.board.grid[r][c] = null;
                }
                this.anim.endClearing();
                this.draw();
                await delay(200);
            }

            this.anim.showComboText(this.combo);
            this.updateCharacterDisplay();
            this.draw();
            await delay(200);

            await this.board.drop();
        }

        if (this.combo > 0) {
            await this._applyDamageAndHeal(combos);
        }
    }

    async _applyDamageAndHeal(combos) {
        const comboMultiplier = 1 + (this.combo - 1) * 0.1;
        const chainLightningMultiplier = (this.combo >= 4 && this.config.chainLightningBonus) ? 1.5 : 1;
        const effectiveDefense = this.enemyDefense - this.enemyDefenseReduction;

        let totalDamage = 0;
        for (const [, count, ballType] of combos) {
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
            this._updateEnemyHpDisplay();
            this._shakeEnemy();
            this._showDamageText(`-${Math.floor(totalDamage)}`);
        }

        let totalHeal = 0;
        for (const [, count, ballType] of combos) {
            if (ballType !== 'heal') continue;
            const countMultiplier = 1 + (count - 3) * 0.3;
            totalHeal += this.config.baseHeal * countMultiplier * comboMultiplier;
        }

        if (totalHeal > 0) {
            this.playerHp = Math.min(this.config.playerHp, this.playerHp + Math.floor(totalHeal));
            this.updateCharacterDisplay();
            this.anim.addDamageText(`+${Math.floor(totalHeal)}`, this.startX + (GRID * CELL) / 2, 20, true);
            this.draw();
        }

        this.attackMultiplier = 1;
        this.enemyDefenseReduction = 0;

        await delay(800);
        if (this.enemyHp <= 0) return;

        const damage = Math.max(0, this.enemyAttack - this.config.playerDefense);
        this.playerHp = Math.max(0, this.playerHp - damage);
        this.anim.flashPlayerHp();
        this.updateCharacterDisplay();
        if (damage > 0) {
            this.anim.addDamageText(`-${damage}`, this.startX + (GRID * CELL) / 2, 15, false);
        }
        this.draw();

        if (this.playerHp <= 0) {
            this._showGameOver();
            return;
        }
        this._applyHealFromInvalid();
    }

    _showGameOver() {
        this.isGameOver = true;
        this.anim.showVictoryOverlay(CANVAS_HEIGHT / 2 - 20);
        this._dirty = true;

        this.canvas.onclick = (e) => {
            if (!this.isGameOver) return;
            const rect = this.canvas.getBoundingClientRect();
            const y = e.clientY - rect.top;
            if (y >= 180 && y <= 220) {
                this._restartBattle();
            } else {
                window.location.href = 'main.html';
            }
        };
    }

    _restartBattle() {
        this.playerHp = this.config.playerHp;
        this.currentEnemyIndex = 0;
        this.enemyHp = this.enemies[0].hp;
        this.enemyName = this.enemies[0].enemy_name;
        this.enemyAttack = this.enemies[0].attack;
        this.enemyDefense = this.enemies[0].defense || 0;
        this.isGameOver = false;
        this.isVictory = false;
        this.combo = 0;
        this.hasMoved = false;
        this.stopTimer();
        this.timeLeft = this.config.timeLimit;
        this.characters = this.config.characters.map(c => ({ ...c, hp: 100 }));
        this.anim.reset();
        this.skillUsed = [false, false, false, false];
        this.attackMultiplier = 1;
        this.enemyDefenseReduction = 0;
        this.board.create();
        this._updateEnemyHpDisplay();
        this.updateCharacterDisplay();
        this.draw();
    }

    _showDamageText(text) {
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

    _showVictory() {
        this.isVictory = true;
        this.anim.showVictoryOverlay(CANVAS_HEIGHT / 2 - 20);
        this._dirty = true;

        fetch(`/api/levels/${this.config.levelId}/complete`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        }).then(res => res.json()).then(data => {
            console.log('Level completed:', data);
        }).catch(err => {
            console.error('Failed to mark level complete:', err);
        });

        this.canvas.onclick = () => {
            if (this.isVictory) window.location.href = 'main.html';
        };
    }
}

export default BattleScene;