import {
    BALL_COLORS, BALL_TYPES, GRID, CELL,
    CANVAS_WIDTH, CANVAS_HEIGHT
} from '../utils/constants.js';
import { delay } from '../utils/helpers.js';
import Board from '../objects/Board.js';

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
        this.showCombo = 0;
        this.showComboTime = 0;

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

        this.damageTexts = [];

        this.isVictory = false;
        this.isGameOver = false;
        this.skillUsed = [false, false, false, false];
        this.attackMultiplier = 1;
        this.enemyDefenseReduction = 0;

        this._initEvents();
        this.updateCharacterDisplay();
        this._startRenderLoop();
        this.draw();
    }

    _startRenderLoop() {
        const loop = () => {
            const hasAnimation = this.board.dropInfo
                || (this.showCombo > 0 && Date.now() - this.showComboTime < 1500)
                || this.damageTexts.length > 0;
            if (this._dirty || hasAnimation) {
                this._dirty = false;
                this._render();
            }
            this._renderRafId = requestAnimationFrame(loop);
        };
        this._renderRafId = requestAnimationFrame(loop);
    }

    draw() {
        this._dirty = true;
    }

    _render() {
        if (this.isVictory || this.isGameOver) return;

        const ctx = this.ctx;
        const grid = this.board.grid;

        ctx.fillStyle = '#2a2a4e';
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

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

        const dropAnim = {};
        if (this.board.dropInfo) {
            const p = this.board.dropProgress;
            const ease = p * p * (3 - 2 * p);
            for (const d of this.board.dropInfo) {
                const startY = this._getY(d.r) - d.distance * CELL;
                const endY = this._getY(d.r);
                dropAnim[`${d.r},${d.c}`] = { type: d.type, y: startY + (endY - startY) * ease };
            }
        }

        for (let r = 0; r < GRID; r++) {
            for (let c = 0; c < GRID; c++) {
                let type = grid[r][c];

                if (this.board.dropInfo) {
                    const key = `${r},${c}`;
                    if (dropAnim[key]) type = dropAnim[key].type;
                }

                if (type === null) continue;

                let x = this._getX(c);
                let y = this._getY(r);

                if (this.board.dropInfo) {
                    const key = `${r},${c}`;
                    if (dropAnim[key]) y = dropAnim[key].y;
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
                ctx.arc(x, y, CELL / 2 - 4, 0, Math.PI * 2);
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
            skillText = this._convertBalls(0);
        } else if (skillName.includes('弓箭手专精')) {
            skillText = this._convertBalls(1);
        } else if (skillName.includes('法师专精')) {
            skillText = this._convertBalls(3);
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

    _convertBalls(targetType) {
        let changed = 0;
        for (let r = 0; r < GRID; r++) {
            for (let c = 0; c < GRID; c++) {
                if (this.board.grid[r][c] === 4) {
                    this.board.grid[r][c] = targetType;
                    changed++;
                }
            }
        }
        return changed > 0 ? '技能发动！' : '没有无效珠子';
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

    _getX(c) { return this.startX + c * CELL + CELL / 2; }
    _getY(r) { return this.startY + r * CELL + CELL / 2; }

    _onDown(e) {
        e.preventDefault();
        if (this.isProcessing || this.isSwapping) return;

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
                this._nextEnemy();
            } else {
                this._showVictory();
            }
        }
        this.isProcessing = false;
    }

    _nextEnemy() {
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
        ctx.fillStyle = 'rgba(0,0,0,0.6)';
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
        ctx.fillStyle = '#ff4';
        ctx.font = 'bold 24px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`下一波: ${this.enemyName}`, CANVAS_WIDTH / 2, 160);
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

                for (const { r, c } of group.cells) {
                    this.board.grid[r][c] = null;
                }

                this.showCombo = this.combo;
                this.showComboTime = Date.now();
                this.updateCharacterDisplay();
                this.draw();
                await delay(500);
            }

            this.showCombo = this.combo;
            this.showComboTime = Date.now();
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
            this._showHealText(`+${Math.floor(totalHeal)}`);
            this.draw();
        }

        this.attackMultiplier = 1;
        this.enemyDefenseReduction = 0;

        await delay(800);
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
            this._animateDamageText();
        }
        this.draw();

        if (this.playerHp <= 0) {
            this._showGameOver();
        }
    }

    _showGameOver() {
        const ctx = this.ctx;
        ctx.fillStyle = 'rgba(0,0,0,0.8)';
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
        ctx.fillStyle = '#f44';
        ctx.font = 'bold 36px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('挑战失败', CANVAS_WIDTH / 2, 140);
        ctx.font = 'bold 16px Arial';
        ctx.fillStyle = '#fff';
        ctx.fillText('重新挑战', CANVAS_WIDTH / 2, 200);
        ctx.fillStyle = '#aaa';
        ctx.font = 'bold 14px Arial';
        ctx.fillText('点击任意处返回主界面', CANVAS_WIDTH / 2, 240);

        this.isGameOver = true;
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
        this.showCombo = 0;
        this.hasMoved = false;
        this.stopTimer();
        this.timeLeft = this.config.timeLimit;
        this.characters = this.config.characters.map(c => ({ ...c, hp: 100 }));
        this.damageTexts = [];
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

    _showHealText(text) {
        this.damageTexts.push({
            text,
            x: this.startX + (GRID * CELL) / 2,
            y: 15,
            alpha: 1,
            vy: 0,
            isHeal: true
        });
        this._animateDamageText();
    }

    _animateDamageText() {
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

    _showVictory() {
        const ctx = this.ctx;
        ctx.fillStyle = 'rgba(0,0,0,0.8)';
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
        ctx.fillStyle = '#ff4';
        ctx.font = 'bold 36px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('关卡完成！', CANVAS_WIDTH / 2, 160);
        ctx.font = 'bold 18px Arial';
        ctx.fillText('点击返回主界面', CANVAS_WIDTH / 2, 200);

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
            if (this.isVictory) window.location.href = 'main.html';
        };
    }
}

export default BattleScene;
