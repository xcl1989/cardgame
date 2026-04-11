export default class AnimationManager {
    constructor() {
        this.clearingCells = [];
        this.clearingStartTime = 0;
        this.isClearing = false;

        this.convertingCells = [];
        this.convertingStartTime = 0;
        this.isConverting = false;
        this.convertingTargetType = null;

        this.chainLightningActive = false;
        this._lightningData = null;

        this.damageTexts = [];
        this._damageAnimating = false;

        this.showCombo = 0;
        this.showComboTime = 0;

        this.playerHpFlash = 0;

        this.introAnimating = false;

        this.victoryAlpha = undefined;
        this.overlayStartTime = 0;
        this.overlayY = 0;
    }

    reset() {
        this.clearingCells = [];
        this.clearingStartTime = 0;
        this.isClearing = false;
        this.convertingCells = [];
        this.convertingStartTime = 0;
        this.isConverting = false;
        this.convertingTargetType = null;
        this.chainLightningActive = false;
        this._lightningData = null;
        this.damageTexts = [];
        this._damageAnimating = false;
        this.showCombo = 0;
        this.showComboTime = 0;
        this.playerHpFlash = 0;
        this.introAnimating = false;
        this.victoryAlpha = undefined;
        this.overlayStartTime = 0;
    }

    isAnimating(board) {
        return !!(board && board.dropInfo)
            || (this.showCombo > 0 && Date.now() - this.showComboTime < 1500)
            || this.damageTexts.length > 0
            || this.isClearing
            || this.isConverting
            || this.chainLightningActive
            || (this.playerHpFlash && Date.now() - this.playerHpFlash < 400)
            || this.introAnimating
            || (this.victoryAlpha !== undefined);
    }

    startClearing(cells) {
        this.clearingCells = cells.map(({ r, c, type }) => ({ r, c, type }));
        this.clearingStartTime = Date.now();
        this.isClearing = true;
    }

    endClearing() {
        this.clearingCells = [];
        this.clearingStartTime = 0;
        this.isClearing = false;
    }

    startConverting(cells, targetType) {
        this.convertingCells = cells.map(({ r, c }) => ({ r, c }));
        this.convertingStartTime = Date.now();
        this.isConverting = true;
        this.convertingTargetType = targetType;
    }

    endConverting() {
        this.convertingCells = [];
        this.convertingStartTime = 0;
        this.isConverting = false;
        this.convertingTargetType = null;
    }

    startChainLightning(cells, getX, getY) {
        if (cells.length < 2) return;
        const segments = [];
        for (let i = 1; i < cells.length; i++) {
            segments.push({
                x1: getX(cells[i - 1].c),
                y1: getY(cells[i - 1].r),
                x2: getX(cells[i].c),
                y2: getY(cells[i].r),
            });
        }
        if (cells.length > 3) {
            segments.push({
                x1: getX(cells[cells.length - 1].c),
                y1: getY(cells[cells.length - 1].r),
                x2: getX(cells[0].c),
                y2: getY(cells[0].r),
            });
        }
        this.chainLightningActive = true;
        this._lightningData = { startTime: Date.now(), segments };
    }

    addDamageText(text, x, y, isHeal) {
        this.damageTexts.push({
            text,
            x, y,
            alpha: 1,
            vy: isHeal ? -0.8 : 0,
            isHeal
        });
        this._startDamageTextAnimation();
    }

    flashPlayerHp() {
        this.playerHpFlash = Date.now();
    }

    showVictoryOverlay(y) {
        this.victoryAlpha = 0;
        this.overlayStartTime = Date.now();
        this.overlayY = y;
    }

    showComboText(combo) {
        this.showCombo = combo;
        this.showComboTime = Date.now();
    }

    _startDamageTextAnimation(drawCallback) {
        if (this._damageAnimating) return;
        this._damageAnimating = true;
        if (drawCallback) drawCallback();
    }
}