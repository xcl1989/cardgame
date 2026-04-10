import os
import random
from datetime import datetime
from typing import Optional, List, Dict, Any, Generator

from sqlalchemy import func, case, or_, select
from sqlmodel import Session as SQLModelSession
from passlib.hash import bcrypt
from dotenv import load_dotenv

from models import (
    User,
    CharacterType,
    Skill,
    SkillCharacterMap,
    PlayerCharacter,
    Team,
    TeamCharacterMap,
    Level,
    Enemy,
    LevelEnemyMap,
    NamePool,
    UserLevelProgress,
    Chapter,
)

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "Game")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"

from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)


def get_db() -> Generator[SQLModelSession, None, None]:
    session = SQLModelSession(engine)
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def verify_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    session = SQLModelSession(engine)
    try:
        user = (
            session.exec(select(User).where(User.username == username))
            .scalars()
            .first()
        )
        if not user:
            return None
        if not bcrypt.verify(password, user.password):
            return None
        return {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "max_teams": user.max_teams,
        }
    finally:
        session.close()


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    session = SQLModelSession(engine)
    try:
        user = (
            session.exec(select(User).where(User.username == username))
            .scalars()
            .first()
        )
        if not user:
            return None
        return {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "nickname": user.nickname,
            "max_teams": user.max_teams,
            "max_characters": user.max_characters,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
    finally:
        session.close()


def get_user_characters(user_id: str) -> list:
    session = SQLModelSession(engine)
    try:
        chars = (
            session.exec(
                select(PlayerCharacter)
                .where(PlayerCharacter.user_id == user_id)
                .where(PlayerCharacter.status == 1)
                .order_by(PlayerCharacter.created_at)
            )
            .scalars()
            .all()
        )
        result = []
        for c in chars:
            d = {
                "id": c.id,
                "character_type_id": c.character_type_id,
                "character_name": c.character_name,
                "rarity": c.rarity,
                "attack_bonus": c.attack_bonus,
                "defense_bonus": c.defense_bonus,
                "recovery_bonus": c.recovery_bonus,
                "hp_bonus": c.hp_bonus,
                "operation_time_bonus": c.operation_time_bonus,
                "bound_passive_skill_id": c.bound_passive_skill_id,
                "created_at": c.created_at,
                "bound_skill_name": None,
                "bound_skill_desc": None,
            }
            if c.bound_passive_skill_id:
                skill = session.get(Skill, c.bound_passive_skill_id)
                if skill:
                    d["bound_skill_name"] = skill.name
                    d["bound_skill_desc"] = skill.description
            result.append(d)
        return result
    finally:
        session.close()


def get_legendary_skills() -> list:
    session = SQLModelSession(engine)
    try:
        skills = (
            session.exec(select(Skill).where(Skill.id.in_([12, 13, 14, 15])))
            .scalars()
            .all()
        )
        return [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "effect_value": s.effect_value,
            }
            for s in skills
        ]
    finally:
        session.close()


def get_random_name() -> str:
    session = SQLModelSession(engine)
    try:
        name = (
            session.exec(select(NamePool.name).order_by(func.rand()).limit(1))
            .scalars()
            .first()
        )
        return name if name else f"角色{random.randint(100, 999)}"
    finally:
        session.close()


def create_character(
    user_id: str,
    character_type_id: int,
    character_name: str,
    rarity: str,
    bonuses: dict,
    bound_passive_skill_id=None,
) -> dict:
    session = SQLModelSession(engine)
    try:
        char = PlayerCharacter(
            user_id=user_id,
            character_type_id=character_type_id,
            character_name=character_name,
            rarity=rarity,
            attack_bonus=bonuses["attack_bonus"],
            defense_bonus=bonuses["defense_bonus"],
            recovery_bonus=bonuses["recovery_bonus"],
            hp_bonus=bonuses["hp_bonus"],
            operation_time_bonus=bonuses["operation_time_bonus"],
            bound_passive_skill_id=bound_passive_skill_id,
        )
        session.add(char)
        session.commit()
        session.refresh(char)

        result = {
            "id": char.id,
            "user_id": char.user_id,
            "character_type_id": char.character_type_id,
            "character_name": char.character_name,
            "rarity": char.rarity,
            "attack_bonus": char.attack_bonus,
            "defense_bonus": char.defense_bonus,
            "recovery_bonus": char.recovery_bonus,
            "hp_bonus": char.hp_bonus,
            "operation_time_bonus": char.operation_time_bonus,
            "bound_passive_skill_id": char.bound_passive_skill_id,
            "status": char.status,
            "dismissed_at": char.dismissed_at,
            "created_at": char.created_at,
            "bound_skill_name": None,
            "bound_skill_desc": None,
        }

        if char.bound_passive_skill_id:
            skill = session.get(Skill, char.bound_passive_skill_id)
            if skill:
                result["bound_skill_name"] = skill.name
                result["bound_skill_desc"] = skill.description
        return result
    finally:
        session.close()


def get_user_character_count(user_id: str) -> int:
    session = SQLModelSession(engine)
    try:
        count = session.scalar(
            select(func.count())
            .select_from(PlayerCharacter)
            .where(PlayerCharacter.user_id == user_id)
            .where(PlayerCharacter.status == 1)
        )
        return count or 0
    finally:
        session.close()


def get_user_max_characters(user_id: str) -> int:
    session = SQLModelSession(engine)
    try:
        user = session.get(User, user_id)
        return user.max_characters if user else 50
    finally:
        session.close()


def increase_max_characters(user_id: str, amount: int = 5) -> int:
    session = SQLModelSession(engine)
    try:
        user = session.get(User, user_id)
        if not user:
            return 50
        user.max_characters = user.max_characters + amount
        session.add(user)
        session.commit()
        session.refresh(user)
        return user.max_characters
    finally:
        session.close()


def delete_character(user_id: str, character_id: int) -> bool:
    session = SQLModelSession(engine)
    try:
        char = session.get(PlayerCharacter, character_id)
        if not char or char.user_id != user_id or char.status != 1:
            return False
        char.status = 0
        char.dismissed_at = datetime.now()
        session.add(char)
        session.commit()
        return True
    finally:
        session.close()


def get_user_teams(user_id: str) -> list:
    session = SQLModelSession(engine)
    try:
        teams = (
            session.exec(
                select(Team).where(Team.user_id == user_id).order_by(Team.created_at)
            )
            .scalars()
            .all()
        )

        result = []
        for team in teams:
            maps = (
                session.exec(
                    select(TeamCharacterMap)
                    .where(TeamCharacterMap.team_id == team.id)
                    .order_by(TeamCharacterMap.slot_position)
                )
                .scalars()
                .all()
            )

            chars_data = []
            for m in maps:
                pc = session.get(PlayerCharacter, m.character_id)
                if not pc or pc.status != 1:
                    continue

                effective_passive_id = (
                    pc.bound_passive_skill_id
                    if pc.bound_passive_skill_id
                    else m.passive_skill_id
                )

                ct = session.get(CharacterType, pc.character_type_id)
                passive_skill = (
                    session.get(Skill, effective_passive_id)
                    if effective_passive_id
                    else None
                )
                active_skill = (
                    session.get(Skill, m.active_skill_id) if m.active_skill_id else None
                )

                chars_data.append(
                    {
                        "slot_position": m.slot_position,
                        "character_id": m.character_id,
                        "passive_skill_id": effective_passive_id,
                        "active_skill_id": m.active_skill_id,
                        "character_name": pc.character_name,
                        "character_type_id": pc.character_type_id,
                        "rarity": pc.rarity,
                        "attack_bonus": pc.attack_bonus,
                        "defense_bonus": pc.defense_bonus,
                        "recovery_bonus": pc.recovery_bonus,
                        "hp_bonus": pc.hp_bonus,
                        "operation_time_bonus": pc.operation_time_bonus,
                        "bound_passive_skill_id": pc.bound_passive_skill_id,
                        "type_name": ct.type_name if ct else "",
                        "base_attack": ct.base_attack if ct else 0,
                        "hp": ct.hp if ct else 0,
                        "operation_time": ct.operation_time if ct else 0,
                        "defense": ct.defense if ct else 0,
                        "passive_skill_name": passive_skill.name
                        if passive_skill
                        else None,
                        "passive_skill_desc": passive_skill.description
                        if passive_skill
                        else None,
                        "passive_effect_value": passive_skill.effect_value
                        if passive_skill
                        else None,
                        "active_skill_name": active_skill.name
                        if active_skill
                        else None,
                        "active_skill_desc": active_skill.description
                        if active_skill
                        else None,
                        "active_effect_value": active_skill.effect_value
                        if active_skill
                        else None,
                    }
                )

            result.append(
                {
                    "id": team.id,
                    "user_id": team.user_id,
                    "team_name": team.team_name,
                    "created_at": team.created_at,
                    "characters": chars_data,
                }
            )
        return result
    finally:
        session.close()


def get_team(team_id: int) -> Optional[Dict[str, Any]]:
    session = SQLModelSession(engine)
    try:
        team = session.get(Team, team_id)
        if not team:
            return None
        return {
            "id": team.id,
            "user_id": team.user_id,
            "team_name": team.team_name,
            "created_at": team.created_at,
        }
    finally:
        session.close()


def create_team(user_id: str, team_name: str) -> int:
    session = SQLModelSession(engine)
    try:
        team = Team(user_id=user_id, team_name=team_name)
        session.add(team)
        session.commit()
        session.refresh(team)
        return team.id
    finally:
        session.close()


def update_team_characters(team_id: int, characters: list):
    session = SQLModelSession(engine)
    try:
        existing = (
            session.exec(
                select(TeamCharacterMap).where(TeamCharacterMap.team_id == team_id)
            )
            .scalars()
            .all()
        )
        for e in existing:
            session.delete(e)
        session.flush()

        for char in characters:
            m = TeamCharacterMap(
                team_id=team_id,
                character_id=int(char["character_id"]),
                slot_position=char["slot_position"],
                passive_skill_id=char.get("passive_skill_id"),
                active_skill_id=char.get("active_skill_id"),
            )
            session.add(m)
        session.commit()
    finally:
        session.close()


def delete_team(team_id: int):
    session = SQLModelSession(engine)
    try:
        maps = (
            session.exec(
                select(TeamCharacterMap).where(TeamCharacterMap.team_id == team_id)
            )
            .scalars()
            .all()
        )
        for m in maps:
            session.delete(m)

        team = session.get(Team, team_id)
        if team:
            session.delete(team)
        session.commit()
    finally:
        session.close()


def get_character_types() -> list:
    session = SQLModelSession(engine)
    try:
        types = session.exec(select(CharacterType)).scalars().all()
        return [
            {
                "id": t.id,
                "type_name": t.type_name,
                "base_attack": t.base_attack,
                "hp": t.hp,
                "operation_time": t.operation_time,
                "defense": t.defense,
            }
            for t in types
        ]
    finally:
        session.close()


def get_skills() -> list:
    session = SQLModelSession(engine)
    try:
        skills = session.exec(select(Skill)).scalars().all()
        return [
            {
                "id": s.id,
                "name": s.name,
                "skill_type": s.skill_type,
                "description": s.description,
                "effect_value": s.effect_value,
            }
            for s in skills
        ]
    finally:
        session.close()


def get_skill(skill_id: int) -> Optional[Dict[str, Any]]:
    session = SQLModelSession(engine)
    try:
        s = session.get(Skill, skill_id)
        if not s:
            return None
        return {
            "id": s.id,
            "name": s.name,
            "skill_type": s.skill_type,
            "description": s.description,
            "effect_value": s.effect_value,
        }
    finally:
        session.close()


def _get_skills_by_character_type_and_type(
    character_type_id: int, skill_type: str
) -> list:
    session = SQLModelSession(engine)
    try:
        char_type_str = str(character_type_id)
        skills = (
            session.exec(
                select(Skill)
                .join(SkillCharacterMap, Skill.id == SkillCharacterMap.skill_id)
                .where(
                    or_(
                        SkillCharacterMap.character_type == char_type_str,
                        SkillCharacterMap.character_type == "0",
                    )
                )
                .where(Skill.skill_type == skill_type)
            )
            .scalars()
            .all()
        )
        return [
            {
                "id": s.id,
                "name": s.name,
                "skill_type": s.skill_type,
                "description": s.description,
                "effect_value": s.effect_value,
            }
            for s in skills
        ]
    finally:
        session.close()


def get_skills_by_character_type(character_type_id: int) -> list:
    return _get_skills_by_character_type_and_type(character_type_id, "被动")


def get_active_skills_by_character_type(character_type_id: int) -> list:
    return _get_skills_by_character_type_and_type(character_type_id, "主动")


def get_levels() -> list:
    session = SQLModelSession(engine)
    try:
        levels = session.exec(select(Level).order_by(Level.id)).scalars().all()
        result = []
        for level in levels:
            maps = (
                session.exec(
                    select(LevelEnemyMap)
                    .where(LevelEnemyMap.level_id == level.id)
                    .order_by(LevelEnemyMap.slot_position)
                )
                .scalars()
                .all()
            )
            enemies = []
            for m in maps:
                e = session.get(Enemy, m.enemy_id)
                if e:
                    enemies.append(
                        {
                            "slot_position": m.slot_position,
                            "enemy_name": e.enemy_name,
                            "hp": e.hp,
                            "attack": e.attack,
                            "defense": e.defense,
                        }
                    )
            result.append(
                {
                    "id": level.id,
                    "level_name": level.level_name,
                    "chapter_id": level.chapter_id,
                    "enemies": enemies,
                }
            )
        return result
    finally:
        session.close()


def get_chapters() -> list:
    session = SQLModelSession(engine)
    try:
        chapters = (
            session.exec(select(Chapter).order_by(Chapter.chapter_order))
            .scalars()
            .all()
        )
        return [
            {
                "id": c.id,
                "chapter_name": c.chapter_name,
                "chapter_order": c.chapter_order,
            }
            for c in chapters
        ]
    finally:
        session.close()


def get_level(level_id: int) -> Optional[Dict[str, Any]]:
    session = SQLModelSession(engine)
    try:
        level = session.get(Level, level_id)
        if not level:
            return None

        maps = (
            session.exec(
                select(LevelEnemyMap)
                .where(LevelEnemyMap.level_id == level_id)
                .order_by(LevelEnemyMap.slot_position)
            )
            .scalars()
            .all()
        )

        enemies = []
        for m in maps:
            e = session.get(Enemy, m.enemy_id)
            if e:
                enemies.append(
                    {
                        "slot_position": m.slot_position,
                        "enemy_name": e.enemy_name,
                        "hp": e.hp,
                        "attack": e.attack,
                        "defense": e.defense,
                    }
                )

        return {
            "id": level.id,
            "level_name": level.level_name,
            "enemies": enemies,
        }
    finally:
        session.close()


def get_user_level_progress(user_id: str) -> list:
    session = SQLModelSession(engine)
    try:
        records = (
            session.exec(
                select(UserLevelProgress).where(UserLevelProgress.user_id == user_id)
            )
            .scalars()
            .all()
        )
        return [
            {"level_id": r.level_id, "completed_at": r.completed_at} for r in records
        ]
    finally:
        session.close()


def complete_level(user_id: str, level_id: int):
    session = SQLModelSession(engine)
    try:
        existing = (
            session.exec(
                select(UserLevelProgress)
                .where(UserLevelProgress.user_id == user_id)
                .where(UserLevelProgress.level_id == level_id)
            )
            .scalars()
            .first()
        )
        if existing:
            existing.completed_at = datetime.now()
            session.add(existing)
        else:
            record = UserLevelProgress(user_id=user_id, level_id=level_id)
            session.add(record)
        session.commit()
    finally:
        session.close()
