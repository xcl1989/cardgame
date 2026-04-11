import {
    BALL_COLORS, GRID, CELL,
    CANVAS_WIDTH, CANVAS_HEIGHT
} from '../utils/constants.js';

export default class BattleRenderer {
    constructor(ctx, scene) {
        this.ctx = ctx;
        this.scene = scene;
    }

    render() {
        const s = this.scene;
        const a = s.anim;

        if (s.isVictory || s.isGameOver) {
            if (a.victoryAlpha !== undefined) {
                this.renderBoard();
                this.renderOverlay();
            }
            return;
        }

        this.renderBoard();
    }

    renderBoard() {
        const s = this.scene;
        const a = s.anim;
        const ctx = this.ctx;
        const grid = s.board.grid;

        ctx.fillStyle = '#2a2a4e';
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

        this.renderHpBar();
        this.renderTimeBar();

        ctx.fillStyle = '#252545';
        ctx.fillRect(s.startX - 5, s.startY + 5, GRID * CELL + 10, GRID * CELL + 10);

        for (let r = 0; r < GRID; r++) {
            for (let c = 0; c < GRID; c++) {
                ctx.strokeStyle = '#3a3a5e';
                ctx.strokeRect(s.startX + c * CELL, s.startY + r * CELL, CELL, CELL);
            }
        }

        const dropAnim = {};
        if (s.board.dropInfo) {
            const p = s.board.dropProgress;
            const ease = p * p * (3 - 2 * p);
            for (const d of s.board.dropInfo) {
                const startY = s._getY(d.r) - d.distance * CELL;
                const endY = s._getY(d.r);
                dropAnim[`${d.r},${d.c}`] = { type: d.type, y: startY + (endY - startY) * ease };
            }
        }

        for (let r = 0; r < GRID; r++) {
            for (let c = 0; c < GRID; c++) {
                let type = grid[r][c];

                if (s.board.dropInfo) {
                    const key = `${r},${c}`;
                    if (dropAnim[key]) type = dropAnim[key].type;
                }

                if (type === null) continue;

                let x = s._getX(c);
                let y = s._getY(r);

                if (s.board.dropInfo) {
                    const key = `${r},${c}`;
                    if (dropAnim[key]) y = dropAnim[key].y;
                }

                if (s.dragBall && r === s.dragBall.r && c === s.dragBall.c && s.isDragging) {
                    x = s.dragX;
                    y = s.dragY;
                    ctx.shadowColor = BALL_COLORS[type];
                    ctx.shadowBlur = 20;
                }

                let radius = CELL / 2 - 4;
                let alpha = 1;

                const clearingIdx = a.clearingCells.findIndex(cc => cc.r === r && cc.c === c);
                const convertIdx = a.convertingCells.findIndex(cc => cc.r === r && cc.c === c);

                if (clearingIdx !== -1 && a.clearingStartTime > 0) {
                    const elapsed = Date.now() - a.clearingStartTime;
                    const progress = Math.min(elapsed / 300, 1);
                    radius = (CELL / 2 - 4) * (1 - progress);
                    alpha = progress < 0.5 ? 1 : (1 - (progress - 0.5) * 2);
                    const ballColor = BALL_COLORS[a.clearingCells[clearingIdx].type] || BALL_COLORS[type];
                    if (Math.floor(progress * 6) % 2 === 0) {
                        ctx.fillStyle = '#fff';
                    } else {
                        ctx.fillStyle = ballColor;
                    }
                    ctx.shadowColor = ballColor;
                    ctx.shadowBlur = 15 * (1 - progress);
                } else if (convertIdx !== -1 && a.convertingStartTime > 0 && type === 4) {
                    const elapsed = Date.now() - a.convertingStartTime;
                    const progress = Math.min(elapsed / 350, 1);
                    const targetColor = BALL_COLORS[a.convertingTargetType] || '#fff';
                    if (progress < 0.4) {
                        ctx.fillStyle = '#fff';
                        ctx.shadowColor = '#fff';
                        ctx.shadowBlur = 20 * (1 - progress / 0.4);
                        radius = (CELL / 2 - 4) * (1 + progress * 0.5);
                    } else {
                        const t = (progress - 0.4) / 0.6;
                        const r1 = parseInt(targetColor.slice(1, 3), 16);
                        const g1 = parseInt(targetColor.slice(3, 5), 16);
                        const b1 = parseInt(targetColor.slice(5, 7), 16);
                        ctx.fillStyle = `rgb(${Math.floor(255 + (r1 - 255) * t)},${Math.floor(255 + (g1 - 255) * t)},${Math.floor(255 + (b1 - 255) * t)})`;
                        ctx.shadowColor = targetColor;
                        ctx.shadowBlur = 10 * (1 - t);
                        radius = (CELL / 2 - 4) * (1 + 0.2 * (1 - t));
                    }
                } else {
                    ctx.fillStyle = BALL_COLORS[type];
                }

                ctx.globalAlpha = alpha;
                ctx.beginPath();
                ctx.arc(x, y, Math.max(0, radius), 0, Math.PI * 2);
                ctx.fill();
                ctx.globalAlpha = 1;
                ctx.shadowBlur = 0;

                if (type === 4 && clearingIdx === -1 && convertIdx === -1) {
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

        this.renderCombo();
        this.renderDamageTexts();
        this.renderChainLightning();
    }

    renderHpBar() {
        const s = this.scene;
        const a = s.anim;
        const ctx = this.ctx;

        ctx.fillStyle = '#333';
        ctx.fillRect(s.startX, 10, GRID * CELL, 18);
        ctx.fillStyle = '#44ff44';
        if (a.playerHpFlash && Date.now() - a.playerHpFlash < 400) {
            if (Math.floor((Date.now() - a.playerHpFlash) / 80) % 2 === 0) {
                ctx.fillStyle = '#ff4444';
            }
        }
        ctx.fillRect(s.startX, 10, (s.playerHp / s.config.playerHp) * GRID * CELL, 18);
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`${Math.floor(s.playerHp)}/${s.config.playerHp}`, s.startX + (GRID * CELL) / 2, 24);
    }

    renderTimeBar() {
        const s = this.scene;
        const ctx = this.ctx;

        ctx.fillStyle = '#444';
        ctx.fillRect(s.startX, 32, GRID * CELL, 6);
        const timeRatio = s.timeLeft / s.config.timeLimit;
        if (timeRatio < 0.2 && s.isTimerRunning) {
            ctx.fillStyle = Math.floor(Date.now() / 200) % 2 === 0 ? '#ff4444' : '#ff8800';
        } else {
            ctx.fillStyle = '#4488ff';
        }
        ctx.fillRect(s.startX, 32, timeRatio * GRID * CELL, 6);
    }

    renderCombo() {
        const a = this.scene.anim;
        const ctx = this.ctx;

        if (a.showCombo > 0 && Date.now() - a.showComboTime < 1500) {
            const alpha = 1 - (Date.now() - a.showComboTime) / 1500;
            ctx.fillStyle = `rgba(255,255,0,${alpha})`;
            ctx.font = 'bold 20px Arial';
            ctx.textAlign = 'right';
            ctx.fillText(`${a.showCombo} Combo!`, 300, 30);
        }
    }

    renderDamageTexts() {
        const ctx = this.ctx;
        const a = this.scene.anim;

        for (let i = a.damageTexts.length - 1; i >= 0; i--) {
            const dt = a.damageTexts[i];
            dt.y += dt.vy;
            dt.alpha -= 0.02;
            if (dt.alpha <= 0) {
                a.damageTexts.splice(i, 1);
                continue;
            }
            if (dt.isHeal) {
                ctx.fillStyle = `rgba(68,255,68,${dt.alpha})`;
            } else {
                ctx.fillStyle = `rgba(255,68,68,${dt.alpha})`;
            }
            ctx.font = `bold ${dt.isHeal ? 20 : 24}px Arial`;
            ctx.textAlign = 'center';
            ctx.fillText(dt.text, dt.x, dt.y);
        }
    }

    renderChainLightning() {
        const a = this.scene.anim;
        const ctx = this.ctx;

        if (a.chainLightningActive && a._lightningData) {
            const elapsed = Date.now() - a._lightningData.startTime;
            if (elapsed < 400) {
                const alpha = 1 - elapsed / 400;
                ctx.strokeStyle = `rgba(255,255,100,${alpha})`;
                ctx.lineWidth = 3;
                ctx.shadowColor = '#ffff66';
                ctx.shadowBlur = 10 * alpha;
                for (const seg of a._lightningData.segments) {
                    ctx.beginPath();
                    ctx.moveTo(seg.x1, seg.y1);
                    ctx.lineTo(seg.x2, seg.y2);
                    ctx.stroke();
                }
                ctx.shadowBlur = 0;
                ctx.lineWidth = 1;
            } else {
                a.chainLightningActive = false;
                a._lightningData = null;
            }
        }
    }

    renderOverlay() {
        const a = this.scene.anim;
        const ctx = this.ctx;
        const elapsed = Date.now() - a.overlayStartTime;
        const progress = Math.min(elapsed / 600, 1);

        ctx.fillStyle = `rgba(0,0,0,${0.8 * Math.min(progress * 2, 1)})`;
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

        ctx.save();
        ctx.translate(CANVAS_WIDTH / 2, a.overlayY);
        let scale;
        if (progress < 0.6) {
            scale = (progress / 0.6) * 1.2;
        } else {
            scale = 1.2 - (progress - 0.6) / 0.4 * 0.2;
        }
        ctx.scale(scale, scale);
        ctx.textAlign = 'center';
        if (this.scene.isVictory) {
            ctx.fillStyle = '#ff4';
            ctx.font = 'bold 36px Arial';
            ctx.fillText('关卡完成！', 0, 0);
            ctx.font = 'bold 18px Arial';
            ctx.fillStyle = '#fff';
            ctx.fillText('点击返回主界面', 0, 40);
        } else {
            ctx.fillStyle = '#f44';
            ctx.font = 'bold 36px Arial';
            ctx.fillText('挑战失败', 0, 0);
            ctx.font = 'bold 16px Arial';
            ctx.fillStyle = '#fff';
            ctx.fillText('重新挑战', 0, 50);
            ctx.fillStyle = '#aaa';
            ctx.font = 'bold 14px Arial';
            ctx.fillText('点击任意处返回主界面', 0, 75);
        }
        ctx.restore();
    }
}