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

function calculateBattleConfig(level, team) {
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
    let chainLightningEquipped = false;
    let hpDoubleEquipped = false;
    let timeDoubleEquipped = false;
    let healFromInvalidEquipped = false;
    let reducedInvalidEquipped = false;

    function parseSkillEffect(skillName, effectValue) {
        const result = { hpBonus: 0, damageBonus: 0, healBonus: 0, timeBonus: 0, defenseBonus: 0, isChainLightning: false, isHpDouble: false, isTimeDouble: false, isHealFromInvalid: false, isReducedInvalid: false };
        if (!skillName || effectValue == null) return result;
        const val = parseFloat(effectValue) || 0;
        if (skillName.includes('力量增强')) { result.damageBonus = val; }
        else if (skillName.includes('耐打')) { result.hpBonus = val; }
        else if (skillName.includes('操作优化')) { result.timeBonus = val; }
        else if (skillName.includes('回复强化')) { result.healBonus = val; }
        else if (skillName.includes('连锁闪电')) { result.isChainLightning = true; }
        else if (skillName.includes('法天象地')) { result.isHpDouble = true; }
        else if (skillName.includes('三头六臂')) { result.isTimeDouble = true; }
        else if (skillName.includes('苟延残喘')) { result.isHealFromInvalid = true; }
        else if (skillName.includes('神机妙算')) { result.isReducedInvalid = true; }
        return result;
    }

    for (let i = 0; i < 4; i++) {
        const char = team.characters.find(c => c.slot_position === i);
        if (char) {
            const typeId = char.character_type_id;
            const type = ballTypeMap[typeId] || 'melee';

            const passiveEffect = parseSkillEffect(char.passive_skill_name, char.passive_effect_value);
            const activeEffect = parseSkillEffect(char.active_skill_name, char.active_effect_value);

            characters.push({
                type,
                name: char.character_name,
                color: typeColors[typeId] || '#ff4444',
                hp: (char.hp || 100) + (char.hp_bonus || 0),
                typeId,
                defense: (char.defense || 0) + (char.defense_bonus || 0),
                operation_time: (char.operation_time || 1000) + (char.operation_time_bonus || 0),
                base_attack: char.base_attack || 5,
                recovery_bonus: char.recovery_bonus || 0,
                rarity: char.rarity || 'normal',
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
            if (passiveEffect.isHpDouble || activeEffect.isHpDouble) {
                hpDoubleEquipped = true;
            }
            if (passiveEffect.isTimeDouble || activeEffect.isTimeDouble) {
                timeDoubleEquipped = true;
            }
            if (passiveEffect.isHealFromInvalid || activeEffect.isHealFromInvalid) {
                healFromInvalidEquipped = true;
            }
            if (passiveEffect.isReducedInvalid || activeEffect.isReducedInvalid) {
                reducedInvalidEquipped = true;
            }

            totalHp += (char.hp || 100) + (char.hp_bonus || 0) + hpBonus;
            totalDefense += (char.defense || 0) + (char.defense_bonus || 0);
            totalTimeBonus += timeBonus + (char.operation_time_bonus || 0);
            totalHeal += healBonus + (char.recovery_bonus || 0);

            const charAttack = (char.base_attack || 5) + (char.attack_bonus || 0);
            if (type === 'melee') {
                totalMeleeDamage += charAttack;
                totalMeleeSkillBonus += damageBonus;
            } else if (type === 'ranged') {
                totalRangedDamage += charAttack;
                totalRangedSkillBonus += damageBonus;
            } else if (type === 'magic') {
                totalMagicDamage += charAttack;
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

    if (hpDoubleEquipped) {
        totalHp *= 2;
    }

    const ballProbability = reducedInvalidEquipped
        ? { melee: 0.22, ranged: 0.22, heal: 0.22, magic: 0.22, invalid: 0.12 }
        : { melee: 0.2, ranged: 0.2, heal: 0.2, magic: 0.2, invalid: 0.2 };

    let finalTimeLimit = 5000 + totalTimeBonus;
    if (timeDoubleEquipped) {
        finalTimeLimit *= 2;
    }

    return {
        playerHp: totalHp,
        playerDefense: totalDefense,
        timeLimit: finalTimeLimit,
        baseDamage: {
            melee: Math.max(0, totalMeleeDamage + totalMeleeSkillBonus),
            ranged: Math.max(0, totalRangedDamage + totalRangedSkillBonus),
            magic: Math.max(0, totalMagicDamage + totalMagicSkillBonus)
        },
        baseHeal: 5 + totalHeal,
        ballProbability,
        chainLightningBonus: chainLightningEquipped,
        healFromInvalidBonus: healFromInvalidEquipped,
        enemies: level.enemies || [{ enemy_name: '敌人', hp: 500, attack: 20 }],
        levelId: level.id,
        characters
    };
}

export { BASE_CONFIG, calculateBattleConfig };
