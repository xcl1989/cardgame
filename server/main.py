import os
import uuid
import time
import random
import logging

import redis
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

from database import (
    verify_user,
    get_user_by_username,
    get_user_characters,
    get_user_teams,
    get_team,
    create_team,
    update_team_characters,
    delete_team,
    get_character_types,
    get_skills,
    get_skills_by_character_type,
    get_active_skills_by_character_type,
    get_levels,
    get_level,
    get_skill,
    get_user_level_progress,
    complete_level,
    get_legendary_skills,
    create_character,
    get_random_name,
)

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:8080").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "1"))
TOKEN_EXPIRE = int(os.getenv("TOKEN_EXPIRE", "86400"))

try:
    r = redis.Redis(
        host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
    )
    r.ping()
except redis.exceptions.ConnectionError:
    logger.warning("Redis connection failed, token auth will not work")
    r = None


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    username: str
    nickname: str
    max_teams: int


class TokenData(BaseModel):
    username: str
    nickname: str
    max_teams: int
    created_at: float


class TeamCreateRequest(BaseModel):
    team_name: str


class TeamCharacter(BaseModel):
    character_id: str
    slot_position: int
    passive_skill_id: Optional[int] = None
    active_skill_id: Optional[int] = None


class TeamUpdateRequest(BaseModel):
    team_name: Optional[str] = None
    characters: List[TeamCharacter]


async def get_current_user(authorization: Optional[str] = Header(None)) -> TokenData:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    data = verify_token(authorization[7:])
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return data


async def get_current_user_with_record(user: TokenData = Depends(get_current_user)):
    record = get_user_by_username(user.username)
    if not record:
        raise HTTPException(status_code=404, detail="User not found")
    return user, record


def verify_token(token: str) -> Optional[TokenData]:
    if not r:
        return None
    data = r.get(f"token:{token}")
    if not data:
        return None
    return TokenData.model_validate_json(str(data))


def create_token(username: str, nickname: str, max_teams: int) -> str:
    if not r:
        raise HTTPException(status_code=500, detail="Redis not available")
    old_token = r.get(f"user:token:{username}")
    if old_token:
        r.delete(f"token:{old_token}")
    token = str(uuid.uuid4())
    data = TokenData(
        username=username,
        nickname=nickname,
        max_teams=max_teams,
        created_at=time.time(),
    )
    r.setex(f"token:{token}", TOKEN_EXPIRE, data.model_dump_json())
    r.setex(f"user:token:{username}", TOKEN_EXPIRE, token)
    return token


def delete_token(token: str):
    if r:
        data = verify_token(token)
        if data:
            r.delete(f"user:token:{data.username}")
        r.delete(f"token:{token}")


@app.post("/login")
def login(req: LoginRequest):
    try:
        user = verify_user(req.username, req.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        token = create_token(req.username, user["nickname"], user["max_teams"])
        return LoginResponse(
            token=token,
            username=req.username,
            nickname=user["nickname"],
            max_teams=user["max_teams"],
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/logout")
def logout(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    delete_token(authorization[7:])
    return {"message": "Logged out"}


@app.get("/verify")
def verify(user: TokenData = Depends(get_current_user)):
    return {"username": user.username, "nickname": user.nickname}


RARITY_WEIGHTS = {"normal": 60, "advanced": 25, "rare": 12, "legendary": 3}
BONUS_ATTRIBUTES = [
    "attack_bonus",
    "defense_bonus",
    "recovery_bonus",
    "hp_bonus",
    "operation_time_bonus",
]
BONUS_RANGES = {
    "normal": {},
    "advanced": {
        "attack_bonus": (1, 2),
        "defense_bonus": (1, 2),
        "recovery_bonus": (1, 2),
        "hp_bonus": (5, 5),
        "operation_time_bonus": (250, 500),
    },
    "rare": {
        "attack_bonus": (2, 3),
        "defense_bonus": (2, 3),
        "recovery_bonus": (2, 2),
        "hp_bonus": (5, 10),
        "operation_time_bonus": (500, 500),
    },
    "legendary": {
        "attack_bonus": (3, 5),
        "defense_bonus": (3, 5),
        "recovery_bonus": (3, 3),
        "hp_bonus": (8, 15),
        "operation_time_bonus": (500, 750),
    },
}


@app.post("/characters/summon")
def summon_character(
    user_record=Depends(get_current_user_with_record),
):
    character_type_id = random.choice([1, 2, 3])
    character_name = get_random_name()

    roll = random.randint(1, 100)
    cumulative = 0
    rarity = "normal"
    for r, w in RARITY_WEIGHTS.items():
        cumulative += w
        if roll <= cumulative:
            rarity = r
            break

    bonuses = {attr: 0 for attr in BONUS_ATTRIBUTES}
    bonus_count = {"advanced": 1, "rare": 2, "legendary": 2}.get(rarity, 0)
    if bonus_count > 0:
        ranges = BONUS_RANGES[rarity]
        chosen = random.sample(list(ranges.keys()), bonus_count)
        for attr in chosen:
            lo, hi = ranges[attr]
            bonuses[attr] = random.randint(lo, hi)

    bound_passive_skill_id = None
    if rarity == "legendary":
        legendary_skills = get_legendary_skills()
        if legendary_skills:
            skill = random.choice(legendary_skills)
            bound_passive_skill_id = skill["id"]

    char = create_character(
        user_id=user_record[1]["id"],
        character_type_id=character_type_id,
        character_name=character_name,
        rarity=rarity,
        bonuses=bonuses,
        bound_passive_skill_id=bound_passive_skill_id,
    )
    return char


@app.get("/characters")
def get_characters(
    _: TokenData = Depends(get_current_user),
    user_record=Depends(get_current_user_with_record),
):
    return get_user_characters(user_record[1]["id"])


@app.get("/teams")
def get_teams(user_record=Depends(get_current_user_with_record)):
    return get_user_teams(user_record[1]["id"])


@app.post("/teams")
def create_new_team(
    req: TeamCreateRequest,
    user: TokenData = Depends(get_current_user),
    user_record=Depends(get_current_user_with_record),
):
    teams = get_user_teams(user_record[1]["id"])
    if len(teams) >= user.max_teams:
        raise HTTPException(
            status_code=400, detail=f"最多只能创建{user.max_teams}个队伍"
        )

    team_id = create_team(user_record[1]["id"], req.team_name)
    return {"id": team_id, "team_name": req.team_name}


@app.post("/teams/{team_id}/update")
def update_existing_team(
    team_id: int,
    req: TeamUpdateRequest,
    user_record=Depends(get_current_user_with_record),
):
    logger.info(f"Update team request: team_id={team_id}, body={req}")
    team = get_team(team_id)
    if not team or team["user_id"] != user_record[1]["id"]:
        raise HTTPException(
            status_code=403, detail="Not authorized to modify this team"
        )

    if req.characters:
        update_team_characters(team_id, [c.model_dump() for c in req.characters])

    return {"message": "Team updated"}


@app.post("/teams/{team_id}/delete")
def delete_existing_team(
    team_id: int,
    user_record=Depends(get_current_user_with_record),
):
    team = get_team(team_id)
    if not team or team["user_id"] != user_record[1]["id"]:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this team"
        )

    delete_team(team_id)
    return {"message": "Team deleted"}


@app.get("/character-types")
def get_types(_: TokenData = Depends(get_current_user)):
    return get_character_types()


@app.get("/skills")
def get_all_skills(_: TokenData = Depends(get_current_user)):
    return get_skills()


@app.get("/skills/{character_type_id}")
def get_skills_for_character(
    character_type_id: int,
    _: TokenData = Depends(get_current_user),
):
    return get_skills_by_character_type(character_type_id)


@app.get("/skills/{character_type_id}/active")
def get_active_skills_for_character(
    character_type_id: int,
    _: TokenData = Depends(get_current_user),
):
    return get_active_skills_by_character_type(character_type_id)


@app.get("/")
def root():
    return {"message": "Card Game API"}


@app.get("/levels")
def get_all_levels(user_record=Depends(get_current_user_with_record)):
    levels = get_levels()
    progress = get_user_level_progress(user_record[1]["id"])
    completed_levels = {p["level_id"] for p in progress}

    return [
        {
            "id": level["id"],
            "level_name": level["level_name"],
            "enemy_name": level["enemies"][-1]["enemy_name"]
            if level.get("enemies")
            else "敌人",
            "enemy_hp": level["enemies"][-1]["hp"] if level.get("enemies") else 0,
            "enemy_attack": level["enemies"][-1]["attack"]
            if level.get("enemies")
            else 20,
            "enemy_defense": level["enemies"][-1]["defense"]
            if level.get("enemies")
            else 0,
            "is_unlocked": True,
            "is_completed": level["id"] in completed_levels,
        }
        for level in levels
    ]


@app.get("/levels/{level_id}")
def get_single_level(
    level_id: int,
    _: TokenData = Depends(get_current_user),
):
    level = get_level(level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")

    return {
        "id": level["id"],
        "level_name": level["level_name"],
        "enemies": level.get("enemies", []),
    }


@app.post("/levels/{level_id}/complete")
def mark_level_complete(
    level_id: int,
    user_record=Depends(get_current_user_with_record),
):
    complete_level(user_record[1]["id"], level_id)
    return {"message": "Level completed"}
