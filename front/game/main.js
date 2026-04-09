import { BASE_CONFIG, calculateBattleConfig } from './config.js';
import BattleScene from './scenes/BattleScene.js';

async function initGame() {
    const battleConfig = await loadBattleConfig();
    if (!battleConfig) {
        console.error('Failed to load battle config');
        return;
    }

    const { level, team } = battleConfig;
    const gameConfig = calculateBattleConfig(level, team);

    window.game = new BattleScene(gameConfig);

    document.getElementById('loading-overlay').style.display = 'none';
    document.getElementById('battle-area').style.visibility = 'visible';
}

if (typeof loadBattleConfig === 'function') {
    initGame();
} else {
    window.onload = () => new BattleScene(BASE_CONFIG);
}
