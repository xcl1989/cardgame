import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import func
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=50)
    password: str = Field(max_length=100)
    nickname: str = Field(default="玩家", max_length=50)
    max_teams: int = Field(default=2)
    max_characters: int = Field(default=50)
    created_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )

    characters: List["PlayerCharacter"] = Relationship(back_populates="user")
    teams: List["Team"] = Relationship(back_populates="user")
    level_progress: List["UserLevelProgress"] = Relationship(back_populates="user")


class CharacterType(SQLModel, table=True):
    __tablename__ = "character_types"

    id: int = Field(primary_key=True)
    type_name: str = Field(max_length=20)
    base_attack: int = Field(default=5)
    hp: int = Field(default=100)
    operation_time: int = Field(default=5000)
    defense: int = Field(default=0)


class Skill(SQLModel, table=True):
    __tablename__ = "skills"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    skill_type: str = Field(max_length=20)
    description: Optional[str] = Field(default=None, max_length=255)
    effect_value: float = Field(default=0.0)


class SkillCharacterMap(SQLModel, table=True):
    __tablename__ = "skill_character_map"

    skill_id: int = Field(foreign_key="skills.id", primary_key=True)
    character_type: str = Field(max_length=50, primary_key=True)


class PlayerCharacter(SQLModel, table=True):
    __tablename__ = "player_characters"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    character_type_id: int = Field(foreign_key="character_types.id")
    character_name: str = Field(max_length=50)
    rarity: str = Field(default="normal", max_length=20)
    attack_bonus: int = Field(default=0)
    defense_bonus: int = Field(default=0)
    recovery_bonus: int = Field(default=0)
    hp_bonus: int = Field(default=0)
    operation_time_bonus: int = Field(default=0)
    bound_passive_skill_id: Optional[int] = Field(default=None, foreign_key="skills.id")
    status: int = Field(default=1)
    dismissed_at: Optional[datetime] = Field(default=None)
    created_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"server_default": func.now()}
    )

    user: Optional[User] = Relationship(back_populates="characters")
    char_type: Optional[CharacterType] = Relationship()
    bound_skill: Optional[Skill] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[PlayerCharacter.bound_passive_skill_id]"
        }
    )


class Team(SQLModel, table=True):
    __tablename__ = "teams"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    team_name: str = Field(max_length=100)
    created_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"server_default": func.now()}
    )

    user: Optional[User] = Relationship(back_populates="teams")
    character_maps: List["TeamCharacterMap"] = Relationship(back_populates="team")


class TeamCharacterMap(SQLModel, table=True):
    __tablename__ = "team_character_map"

    team_id: int = Field(foreign_key="teams.id", primary_key=True)
    character_id: int = Field(foreign_key="player_characters.id", primary_key=True)
    slot_position: int = Field(primary_key=True)
    passive_skill_id: Optional[int] = Field(default=None, foreign_key="skills.id")
    active_skill_id: Optional[int] = Field(default=None, foreign_key="skills.id")

    team: Optional[Team] = Relationship(back_populates="character_maps")
    character: Optional[PlayerCharacter] = Relationship()
    passive_skill: Optional[Skill] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[TeamCharacterMap.passive_skill_id]"}
    )
    active_skill: Optional[Skill] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[TeamCharacterMap.active_skill_id]"}
    )


class Chapter(SQLModel, table=True):
    __tablename__ = "chapters"

    id: int = Field(default=None, primary_key=True)
    chapter_name: str = Field(max_length=50)
    chapter_order: int = Field(default=0)

    levels: List["Level"] = Relationship(back_populates="chapter")


class Level(SQLModel, table=True):
    __tablename__ = "levels"

    id: int = Field(default=None, primary_key=True)
    level_name: str = Field(max_length=50)
    level_order: int = Field(default=0)
    chapter_id: Optional[int] = Field(default=None, foreign_key="chapters.id")

    chapter: Optional[Chapter] = Relationship(back_populates="levels")
    enemy_maps: List["LevelEnemyMap"] = Relationship(back_populates="level")


class Enemy(SQLModel, table=True):
    __tablename__ = "enemies"

    id: int = Field(default=None, primary_key=True)
    enemy_name: str = Field(max_length=50)
    hp: int = Field(default=100)
    attack: int = Field(default=0)
    defense: int = Field(default=0)


class LevelEnemyMap(SQLModel, table=True):
    __tablename__ = "level_enemy_map"

    level_id: int = Field(foreign_key="levels.id", primary_key=True)
    enemy_id: int = Field(foreign_key="enemies.id", primary_key=True)
    slot_position: int = Field(primary_key=True)

    level: Optional[Level] = Relationship(back_populates="enemy_maps")
    enemy: Optional[Enemy] = Relationship()


class NamePool(SQLModel, table=True):
    __tablename__ = "name_pool"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=50)


class UserLevelProgress(SQLModel, table=True):
    __tablename__ = "user_level_progress"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    level_id: int = Field(foreign_key="levels.id")
    completed_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"server_default": func.now()}
    )

    user: Optional[User] = Relationship(back_populates="level_progress")
