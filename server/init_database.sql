-- 卡牌三消游戏数据库初始化脚本
-- 执行: mysql -uroot -p12345678 Game < server/init_database.sql

-- ============================================
-- 创建表
-- ============================================

CREATE DATABASE IF NOT EXISTS Game CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE Game;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    nickname VARCHAR(50) DEFAULT '玩家',
    max_teams INT DEFAULT 2,
    max_characters INT DEFAULT 50,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 角色类型表
CREATE TABLE IF NOT EXISTS character_types (
    id INT PRIMARY KEY,
    type_name VARCHAR(20) NOT NULL,
    base_attack INT DEFAULT 5,
    hp INT DEFAULT 100,
    operation_time INT DEFAULT 5000,
    defense INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 技能表
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    skill_type VARCHAR(20) NOT NULL,
    description VARCHAR(255) DEFAULT NULL,
    effect_value DECIMAL(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 技能-角色类型关联表
CREATE TABLE IF NOT EXISTS skill_character_map (
    skill_id INT NOT NULL,
    character_type VARCHAR(50) NOT NULL,
    PRIMARY KEY (skill_id, character_type),
    FOREIGN KEY (skill_id) REFERENCES skills(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 玩家角色表
CREATE TABLE IF NOT EXISTS player_characters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    character_type_id INT NOT NULL,
    character_name VARCHAR(50) NOT NULL,
    rarity VARCHAR(20) DEFAULT 'normal',
    attack_bonus INT DEFAULT 0,
    defense_bonus INT DEFAULT 0,
    recovery_bonus INT DEFAULT 0,
    hp_bonus INT DEFAULT 0,
    operation_time_bonus INT DEFAULT 0,
    bound_passive_skill_id INT DEFAULT NULL,
    status INT DEFAULT 1,
    dismissed_at TIMESTAMP NULL DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (character_type_id) REFERENCES character_types(id),
    FOREIGN KEY (bound_passive_skill_id) REFERENCES skills(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 队伍表
CREATE TABLE IF NOT EXISTS teams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    team_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 队伍角色关联表
CREATE TABLE IF NOT EXISTS team_character_map (
    team_id INT NOT NULL,
    character_id INT NOT NULL,
    slot_position INT NOT NULL,
    passive_skill_id INT DEFAULT NULL,
    active_skill_id INT DEFAULT NULL,
    PRIMARY KEY (team_id, character_id, slot_position),
    FOREIGN KEY (team_id) REFERENCES teams(id),
    FOREIGN KEY (character_id) REFERENCES player_characters(id),
    FOREIGN KEY (passive_skill_id) REFERENCES skills(id),
    FOREIGN KEY (active_skill_id) REFERENCES skills(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 关卡表
CREATE TABLE IF NOT EXISTS levels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level_name VARCHAR(50) NOT NULL,
    level_order INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 敌人表
CREATE TABLE IF NOT EXISTS enemies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enemy_name VARCHAR(50) NOT NULL,
    hp INT DEFAULT 100,
    attack INT DEFAULT 0,
    defense INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 关卡-敌人关联表
CREATE TABLE IF NOT EXISTS level_enemy_map (
    level_id INT NOT NULL,
    enemy_id INT NOT NULL,
    slot_position INT NOT NULL,
    PRIMARY KEY (level_id, enemy_id, slot_position),
    FOREIGN KEY (level_id) REFERENCES levels(id),
    FOREIGN KEY (enemy_id) REFERENCES enemies(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 名字池表
CREATE TABLE IF NOT EXISTS name_pool (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户关卡进度表
CREATE TABLE IF NOT EXISTS user_level_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    level_id INT NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (level_id) REFERENCES levels(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 插入基础数据
-- ============================================

-- 角色类型
INSERT INTO character_types (id, type_name, base_attack, hp, operation_time, defense) VALUES
(1, '战士', 3, 25, 1250, 2),
(2, '弓箭手', 5, 25, 1250, 0),
(3, '法师', 5, 25, 1250, 0);

-- 技能
INSERT INTO skills (id, name, skill_type, description, effect_value) VALUES
(1, '力量增强', '被动', '基础伤害+2', 2),
(2, '耐打', '被动', '基础hp+30', 30),
(3, '操作优化', '被动', '操作时间+500ms', 500),
(4, '回复强化', '被动', '基础回复+1', 1),
(5, '连锁闪电', '被动', '当combo数达到4及以上时，当前回合的红蓝黄珠子的基础伤害提高50%', 0.5),
(6, '战士专精', '主动', '将当前棋盘中的无效珠子变成红色珠子', 0),
(7, '弓箭手专精', '主动', '将当前棋盘中的无效珠子变成蓝色珠子', 0),
(8, '法师专精', '主动', '将当前棋盘中的无效珠子变成黄色珠子', 0),
(9, '回复', '主动', '回复最大血量50%的生命值', 0.5),
(10, '暴击', '主动', '本回合红色珠子基础攻击力变为3倍', 3),
(11, '精确打击', '主动', '本回合敌人防御下降5', -5),
(12, '法天象地', '被动', '总血量翻倍', 2),
(13, '三头六臂', '被动', '操作时长翻倍', 2),
(14, '苟延残喘', '被动', '每回合随机将1-2颗无效珠子转变为绿色回复珠子', 0),
(15, '神机妙算', '被动', '降低无效珠子生成概率至12%，其他珠子概率变为22%', 0);

-- 技能-角色关联 (0=所有职业)
INSERT INTO skill_character_map (skill_id, character_type) VALUES
(1, '1'), (2, '1'),
(3, '2'), (3, '3'), (4, '2'), (4, '3'),
(5, '0'),
(6, '1'), (9, '1'),
(7, '2'), (10, '2'),
(8, '3'), (9, '3');

-- 名字池
INSERT IGNORE INTO name_pool (name) VALUES
('牛顿'),('欧拉'),('高斯'),('爱因斯坦'),('达尔文'),
('居里夫人'),('特斯拉'),('霍金'),('费曼'),('玻尔'),
('薛定谔'),('海森堡'),('狄拉克'),('泡利'),('玻恩'),
('普朗克'),('法拉第'),('麦克斯韦'),('赫兹'),('安培'),
('伏特'),('欧姆'),('库仑'),('韦伯'),('楞次'),
('焦耳'),('开尔文'),('卡诺'),('克劳修斯'),('玻尔兹曼'),
('吉布斯'),('亥姆霍兹'),('哈密顿'),('拉格朗日'),('傅里叶'),
('拉普拉斯'),('泊松'),('柯西'),('黎曼'),('伽罗瓦'),
('阿贝尔'),('庞加莱'),('希尔伯特'),('哥德尔'),('图灵'),
('冯诺依曼'),('香农'),('维纳'),('纳什'),('门捷列夫'),
('道尔顿'),('阿伏伽德罗'),('波义耳'),('查理'),('盖吕萨克'),
('卡文迪许'),('胡克'),('托里拆利'),('帕斯卡'),('伯努利'),
('泰勒'),('麦克劳林'),('斯特林'),('贝叶斯'),('马尔可夫'),
('切比雪夫'),('洛必达'),('雅可比'),('阿达马'),('刘维尔'),
('魏尔斯特拉斯'),('康托尔'),('戴德金'),('克莱因'),('诺特'),
('埃米'),('闵可夫斯基'),('洛伦兹'),('菲涅尔'),('托马斯杨'),
('夫琅禾费'),('多普勒'),('哈勃'),('开普勒'),('哥白尼'),
('托勒密'),('阿基米德'),('毕达哥拉斯'),('亚里士多德'),('欧几里得'),
('笛卡尔'),('莱布尼茨'),('巴斯德'),('孟德尔'),('摩尔根'),
('沃森'),('克里克'),('费马'),('伦福德'),('卡塞尔');

-- 测试用户 (密码: 123456 的 bcrypt hash)
INSERT INTO users (id, username, password, nickname, max_teams) VALUES
('a855635a-322e-11f1-9cbd-df2001a53a33', 'xcl1989', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36Kz2a.taYbI9dwOVrNCrG', 'gamemaster', 2);

-- 玩家角色
INSERT INTO player_characters (id, user_id, character_type_id, character_name, rarity, attack_bonus, defense_bonus, recovery_bonus, hp_bonus, operation_time_bonus, bound_passive_skill_id) VALUES
(1, 'a855635a-322e-11f1-9cbd-df2001a53a33', 1, '阿基米德', 'normal', 0, 0, 0, 0, 0, NULL),
(2, 'a855635a-322e-11f1-9cbd-df2001a53a33', 1, '帕利卡', 'normal', 0, 0, 0, 0, 0, NULL),
(3, 'a855635a-322e-11f1-9cbd-df2001a53a33', 2, '古斯特', 'normal', 0, 0, 0, 0, 0, NULL),
(4, 'a855635a-322e-11f1-9cbd-df2001a53a33', 2, '莱昂拉多', 'advanced', 1, 0, 0, 0, 0, NULL),
(5, 'a855635a-322e-11f1-9cbd-df2001a53a33', 3, '加百列', 'rare', 1, 0, 1, 0, 0, NULL),
(6, 'a855635a-322e-11f1-9cbd-df2001a53a33', 3, '克洛', 'legendary', 2, 1, 0, 5, 0, 5);

-- 关卡
INSERT INTO levels (id, level_name, level_order) VALUES
(1, '0-1', 0),
(2, '0-2', 1),
(3, '0-3', 2);

-- 敌人
INSERT INTO enemies (id, enemy_name, hp, attack, defense) VALUES
(1, '普通敌人', 200, 10, 0),
(2, '中级敌人', 300, 15, 0),
(3, '高级敌人', 500, 20, 0);

-- 关卡-敌人关联
INSERT INTO level_enemy_map (level_id, enemy_id, slot_position) VALUES
(1, 1, 0),
(2, 1, 0), (2, 2, 1),
(3, 2, 0), (3, 3, 1);

-- 队伍
INSERT INTO teams (id, user_id, team_name) VALUES
(1, 'a855635a-322e-11f1-9cbd-df2001a53a33', '队伍1'),
(2, 'a855635a-322e-11f1-9cbd-df2001a53a33', '队伍2');

-- 队伍角色关联
INSERT INTO team_character_map (team_id, character_id, slot_position, passive_skill_id, active_skill_id) VALUES
(1, 1, 0, 11, 5),
(1, 2, 1, 2, 9),
(1, 3, 2, 3, 6),
(1, 6, 3, 4, 8),
(2, 6, 0, 4, 7),
(2, 3, 1, 4, 10),
(2, 4, 2, 4, 6),
(2, 5, 3, 3, 8);