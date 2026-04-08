-- 创建技能表（如果不存在）
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '技能名称',
    skill_type VARCHAR(20) NOT NULL COMMENT '技能类型：主动/被动',
    description TEXT COMMENT '技能描述',
    effect_value VARCHAR(50) DEFAULT '0' COMMENT '效果值',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建技能-角色类型关联表（如果不存在）
CREATE TABLE IF NOT EXISTS skill_character_map (
    id INT AUTO_INCREMENT PRIMARY KEY,
    skill_id INT NOT NULL,
    character_type INT NOT NULL COMMENT '0=所有职业, 1=战士, 2=弓箭手, 3=法师, 4=牧师',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_skill_char (skill_id, character_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 检查技能是否已存在
SELECT @exists := COUNT(*) FROM skills WHERE name = '连锁闪电';

-- 如果不存在，则添加
INSERT INTO skills (name, skill_type, description, effect_value) 
SELECT '连锁闪电', '被动', '当combo数达到4及以上时，当前回合的红蓝黄珠子的基础伤害提高50%', '0.5'
WHERE @exists = 0;

-- 获取技能ID并添加关联 (character_type = 0 表示所有职业)
INSERT INTO skill_character_map (skill_id, character_type)
SELECT LAST_INSERT_ID(), 0
WHERE @exists = 0;

SELECT '连锁闪电技能已添加' AS result;