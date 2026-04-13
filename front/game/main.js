import { BASE_CONFIG, calculateBattleConfig } from './config.js';
import BattleScene from './scenes/BattleScene.js';

async function initGame() {
    const battleConfig = await loadBattleConfig();
    if (!battleConfig) {
        console.error('Failed to load battle config');
        return;
    }

    const { level, team, battleSession } = battleConfig;
    const gameConfig = calculateBattleConfig(level, team);

    window.game = new BattleScene(gameConfig, battleSession);

    if (!battleSession) {
        window.game._onIntroComplete = async () => {
            const grid = window.game.board.grid.map(row => [...row]);
            const firstEnemy = gameConfig.enemies[0];
            const payload = {
                level_id: gameConfig.levelId,
                team_id: gameConfig.teamId,
                enemy_hp: firstEnemy.hp,
                player_hp: gameConfig.playerHp,
                board_grid: JSON.stringify(grid),
            };
            console.log('[InitGame] Creating session, board_grid sample:', JSON.stringify(grid).slice(0, 100));
            try {
                const res = await fetch('/api/battle-sessions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    },
                    body: JSON.stringify(payload),
                });
                if (res.ok) {
                    const bs = await res.json();
                    window.game.sessionId = bs.id;
                    console.log('[InitGame] Session created, id:', bs.id);
                } else {
                    console.error('[InitGame] Failed to create session:', res.status, await res.text());
                }
            } catch (e) {
                console.error('Failed to create battle session:', e);
            }
        };
    }

    document.getElementById('loading-overlay').style.display = 'none';
    document.getElementById('battle-area').style.visibility = 'visible';
}

if (typeof loadBattleConfig === 'function') {
    initGame();
} else {
    window.onload = () => new BattleScene(BASE_CONFIG);
}