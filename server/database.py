import os
import uuid
import random
from contextlib import contextmanager
from typing import Optional, List, Dict, Any

import pymysql
from dbutils.pooled_db import PooledDB
from dotenv import load_dotenv
from passlib.hash import bcrypt

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "Game")

_pool = PooledDB(
    pymysql,
    maxconnections=10,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=False,
)


@contextmanager
def get_db():
    conn = _pool.connection()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def verify_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, nickname, password, max_teams FROM users WHERE username=%s",
                (username,),
            )
            user = cursor.fetchone()
            if not user:
                return None
            if not bcrypt.verify(password, user["password"]):
                return None
            return {
                "id": user["id"],
                "username": user["username"],
                "nickname": user["nickname"],
                "max_teams": user["max_teams"],
            }


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            return cursor.fetchone()


def get_user_characters(user_id: str) -> list:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT pc.id, pc.character_type_id, pc.character_name, pc.rarity,
                          pc.attack_bonus, pc.defense_bonus, pc.recovery_bonus,
                          pc.hp_bonus, pc.operation_time_bonus, pc.bound_passive_skill_id,
                          s.name as bound_skill_name, s.description as bound_skill_desc,
                          pc.created_at
                   FROM player_characters pc
                   LEFT JOIN skills s ON pc.bound_passive_skill_id = s.id
                   WHERE pc.user_id=%s ORDER BY pc.created_at""",
                (user_id,),
            )
            return list(cursor.fetchall())


def get_legendary_skills() -> list:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, description, effect_value FROM skills WHERE id IN (12, 13, 14, 15)"
            )
            return list(cursor.fetchall())


def get_random_name() -> str:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM name_pool ORDER BY RAND() LIMIT 1")
            row = cursor.fetchone()
            return row["name"] if row else f"角色{random.randint(100, 999)}"


def create_character(
    user_id: str,
    character_type_id: int,
    character_name: str,
    rarity: str,
    bonuses: dict,
    bound_passive_skill_id=None,
) -> dict:
    with get_db() as conn:
        with conn.cursor() as cursor:
            type_names = {1: "战士", 2: "弓箭手", 3: "法师"}
            cursor.execute(
                """INSERT INTO player_characters
                   (user_id, character_type_id, character_name, rarity,
                    attack_bonus, defense_bonus, recovery_bonus, hp_bonus, operation_time_bonus, bound_passive_skill_id)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    user_id,
                    character_type_id,
                    character_name,
                    rarity,
                    bonuses["attack_bonus"],
                    bonuses["defense_bonus"],
                    bonuses["recovery_bonus"],
                    bonuses["hp_bonus"],
                    bonuses["operation_time_bonus"],
                    bound_passive_skill_id,
                ),
            )
            conn.commit()
            char_id = cursor.lastrowid
            cursor.execute(
                """SELECT pc.*, s.name as bound_skill_name, s.description as bound_skill_desc
                   FROM player_characters pc
                   LEFT JOIN skills s ON pc.bound_passive_skill_id = s.id
                   WHERE pc.id=%s""",
                (char_id,),
            )
            return cursor.fetchone()


def get_user_teams(user_id: str) -> list:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT t.*, tcm.slot_position, tcm.character_id,
                          CASE WHEN pc.bound_passive_skill_id IS NOT NULL THEN pc.bound_passive_skill_id ELSE tcm.passive_skill_id END as effective_passive_skill_id,
                          tcm.active_skill_id,
                          pc.character_name, pc.character_type_id, pc.rarity,
                          pc.attack_bonus, pc.defense_bonus, pc.recovery_bonus,
                          pc.hp_bonus, pc.operation_time_bonus, pc.bound_passive_skill_id,
                          ct.type_name, ct.base_attack, ct.hp, ct.operation_time, ct.defense,
                          pas.name as passive_skill_name, pas.description as passive_skill_desc, pas.effect_value as passive_effect_value,
                          act.name as active_skill_name, act.description as active_skill_desc, act.effect_value as active_effect_value
                   FROM teams t
                   LEFT JOIN team_character_map tcm ON t.id = tcm.team_id
                   LEFT JOIN player_characters pc ON tcm.character_id = pc.id
                   LEFT JOIN character_types ct ON pc.character_type_id = ct.id
                   LEFT JOIN skills pas ON (CASE WHEN pc.bound_passive_skill_id IS NOT NULL THEN pc.bound_passive_skill_id ELSE tcm.passive_skill_id END) = pas.id
                   LEFT JOIN skills act ON tcm.active_skill_id = act.id
                   WHERE t.user_id=%s
                   ORDER BY t.created_at, tcm.slot_position""",
                (user_id,),
            )
            rows = cursor.fetchall()

            teams_map: Dict[int, dict] = {}
            for row in rows:
                team_id = row["id"]
                if team_id not in teams_map:
                    teams_map[team_id] = {
                        "id": row["id"],
                        "user_id": row["user_id"],
                        "team_name": row["team_name"],
                        "created_at": row["created_at"],
                        "characters": [],
                    }
                if row["character_id"]:
                    char = {
                        "slot_position": row["slot_position"],
                        "character_id": row["character_id"],
                        "passive_skill_id": row["effective_passive_skill_id"],
                        "active_skill_id": row["active_skill_id"],
                        "character_name": row["character_name"],
                        "character_type_id": row["character_type_id"],
                        "rarity": row["rarity"],
                        "attack_bonus": row["attack_bonus"],
                        "defense_bonus": row["defense_bonus"],
                        "recovery_bonus": row["recovery_bonus"],
                        "hp_bonus": row["hp_bonus"],
                        "operation_time_bonus": row["operation_time_bonus"],
                        "bound_passive_skill_id": row["bound_passive_skill_id"],
                        "type_name": row["type_name"],
                        "base_attack": row["base_attack"],
                        "hp": row["hp"],
                        "operation_time": row["operation_time"],
                        "defense": row["defense"],
                        "passive_skill_name": row["passive_skill_name"],
                        "passive_skill_desc": row["passive_skill_desc"],
                        "passive_effect_value": row["passive_effect_value"],
                        "active_skill_name": row["active_skill_name"],
                        "active_skill_desc": row["active_skill_desc"],
                        "active_effect_value": row["active_effect_value"],
                    }
                    teams_map[team_id]["characters"].append(char)
            return list(teams_map.values())


def get_team(team_id: int) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM teams WHERE id=%s", (team_id,))
            return cursor.fetchone()


def create_team(user_id: str, team_name: str) -> int:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO teams (user_id, team_name) VALUES (%s, %s)",
                (user_id, team_name),
            )
            conn.commit()
            return cursor.lastrowid


def update_team_characters(team_id: int, characters: list):
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM team_character_map WHERE team_id=%s", (team_id,)
            )
            for char in characters:
                cursor.execute(
                    """INSERT INTO team_character_map (team_id, character_id, slot_position, passive_skill_id, active_skill_id)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (
                        team_id,
                        char["character_id"],
                        char["slot_position"],
                        char.get("passive_skill_id"),
                        char.get("active_skill_id"),
                    ),
                )
            conn.commit()


def delete_team(team_id: int):
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM team_character_map WHERE team_id=%s", (team_id,)
            )
            cursor.execute("DELETE FROM teams WHERE id=%s", (team_id,))
            conn.commit()


def get_character_types() -> list:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM character_types")
            return list(cursor.fetchall())


def get_skills() -> list:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM skills")
            return list(cursor.fetchall())


def get_skill(skill_id: int) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM skills WHERE id=%s", (skill_id,))
            return cursor.fetchone()


def get_skills_by_character_type(character_type_id: int) -> list:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT s.* FROM skills s
                   JOIN skill_character_map scm ON s.id = scm.skill_id
                   WHERE (scm.character_type = %s OR scm.character_type IN ('0', 0)) AND s.skill_type = '被动'""",
                (str(character_type_id),),
            )
            return list(cursor.fetchall())


def get_active_skills_by_character_type(character_type_id: int) -> list:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT s.* FROM skills s
                   JOIN skill_character_map scm ON s.id = scm.skill_id
                   WHERE (scm.character_type = %s OR scm.character_type IN ('0', 0)) AND s.skill_type = '主动'""",
                (str(character_type_id),),
            )
            return list(cursor.fetchall())


def get_levels() -> list:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT l.*, lem.slot_position, lem.enemy_id, e.enemy_name, e.hp, e.attack, e.defense
                   FROM levels l
                   LEFT JOIN level_enemy_map lem ON l.id = lem.level_id
                   LEFT JOIN enemies e ON lem.enemy_id = e.id
                   ORDER BY l.id, lem.slot_position""",
            )
            rows = cursor.fetchall()

            levels_map: Dict[int, dict] = {}
            for row in rows:
                level_id = row["id"]
                if level_id not in levels_map:
                    levels_map[level_id] = {
                        "id": row["id"],
                        "level_name": row["level_name"],
                        "enemies": [],
                    }
                if row["enemy_id"]:
                    enemy = {
                        "slot_position": row["slot_position"],
                        "enemy_name": row["enemy_name"],
                        "hp": row["hp"],
                        "attack": row["attack"],
                        "defense": row["defense"],
                    }
                    levels_map[level_id]["enemies"].append(enemy)
            return list(levels_map.values())


def get_level(level_id: int) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT l.*, lem.slot_position, e.enemy_name, e.hp, e.attack, e.defense
                   FROM levels l
                   LEFT JOIN level_enemy_map lem ON l.id = lem.level_id
                   LEFT JOIN enemies e ON lem.enemy_id = e.id
                   WHERE l.id=%s
                   ORDER BY lem.slot_position""",
                (level_id,),
            )
            rows = cursor.fetchall()
            if not rows:
                return None

            level = {
                "id": rows[0]["id"],
                "level_name": rows[0]["level_name"],
                "enemies": [],
            }
            for row in rows:
                if row["enemy_name"]:
                    level["enemies"].append(
                        {
                            "slot_position": row["slot_position"],
                            "enemy_name": row["enemy_name"],
                            "hp": row["hp"],
                            "attack": row["attack"],
                            "defense": row["defense"],
                        }
                    )
            return level


def get_user_level_progress(user_id: str) -> list:
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT level_id, completed_at FROM user_level_progress WHERE user_id=%s",
                (user_id,),
            )
            return list(cursor.fetchall())


def complete_level(user_id: str, level_id: int):
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """INSERT INTO user_level_progress (user_id, level_id) 
                   VALUES (%s, %s)
                   ON DUPLICATE KEY UPDATE completed_at=CURRENT_TIMESTAMP""",
                (user_id, level_id),
            )
            conn.commit()
