-- 关卡表
CREATE TABLE IF NOT EXISTS levels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level_name VARCHAR(100) NOT NULL COMMENT '关卡名称',
    enemy_name VARCHAR(100) NOT NULL DEFAULT '敌人' COMMENT '敌人名称',
    enemy_hp INT NOT NULL DEFAULT 500 COMMENT '敌人血量',
    enemy_attack INT NOT NULL DEFAULT 20 COMMENT '敌人攻击力',
    reward VARCHAR(200) DEFAULT '金币 x100' COMMENT '通关奖励',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入初始关卡数据
INSERT INTO levels (level_name, enemy_name, enemy_hp, enemy_attack, reward) VALUES
('第一关 - 初出茅庐', '哥布林', 300, 15, '金币 x100'),
('第二关 - 森林探险', '森林狼', 500, 20, '金币 x200'),
('第三关 - 黑暗洞穴', '蝙蝠王', 800, 25, '金币 x300'),
('第四关 - 火焰山', '火焰巨人', 1200, 30, '金币 x500'),
('第五关 - 冰封王座', '冰霜巨龙', 2000, 40, '金币 x1000');
