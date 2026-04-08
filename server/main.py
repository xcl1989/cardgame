from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import redis
import uuid
import time
from database import (
    verify_user,
    get_user_by_username,
    get_user_characters,
    get_user_teams,
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
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 1
TOKEN_EXPIRE = 86400

try:
    r = redis.Redis(
        host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
    )
    r.ping()
except:
    r = None


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    username: str
    max_teams: int


class TokenData(BaseModel):
    username: str
    max_teams: int
    created_at: float


def verify_token(token: str) -> Optional[TokenData]:
    if not r:
        return None
    data = r.get(f"token:{token}")
    if not data:
        return None
    return TokenData.model_validate_json(str(data))


def create_token(username: str, max_teams: int) -> str:
    if not r:
        raise HTTPException(status_code=500, detail="Redis not available")
    old_token = r.get(f"user:token:{username}")
    if old_token:
        r.delete(f"token:{old_token}")
    token = str(uuid.uuid4())
    data = TokenData(username=username, max_teams=max_teams, created_at=time.time())
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
        token = create_token(req.username, user["max_teams"])
        return LoginResponse(
            token=token, username=req.username, max_teams=user["max_teams"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/logout")
def logout(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization[7:]
    delete_token(token)
    return {"message": "Logged out"}


@app.get("/verify")
def verify(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization[7:]
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"username": data.username}


@app.get("/characters")
def get_characters(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization[7:]
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    chars = get_user_characters(user["id"])
    return chars


class TeamCreateRequest(BaseModel):
    team_name: str


class TeamUpdateRequest(BaseModel):
    team_name: Optional[str] = None
    characters: list


@app.get("/teams")
def get_teams(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization[7:]
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return get_user_teams(user["id"])


@app.post("/teams")
def create_new_team(
    req: TeamCreateRequest, authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization[7:]
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    teams = get_user_teams(user["id"])
    if len(teams) >= data.max_teams:
        raise HTTPException(
            status_code=400, detail=f"最多只能创建{data.max_teams}个队伍"
        )

    team_id = create_team(user["id"], req.team_name)
    return {"id": team_id, "team_name": req.team_name}


@app.put("/teams/{team_id}")
def update_existing_team(
    team_id: int, req: TeamUpdateRequest, authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization[7:]
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if req.characters:
        update_team_characters(team_id, req.characters)

    return {"message": "Team updated"}


@app.delete("/teams/{team_id}")
def delete_existing_team(team_id: int, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization[7:]
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    delete_team(team_id)
    return {"message": "Team deleted"}


@app.get("/character-types")
def get_types(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization[7:]
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return get_character_types()


@app.get("/skills")
def get_all_skills(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization[7:]
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return get_skills()


@app.get("/skills/{character_type_id}")
def get_skills_for_character(
    character_type_id: int, authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization[7:]
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return get_skills_by_character_type(character_type_id)


@app.get("/skills/{character_type_id}/active")
def get_active_skills_for_character(
    character_type_id: int, authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization[7:]
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return get_active_skills_by_character_type(character_type_id)


@app.get("/")
def root():
    return {"message": "Card Game API"}


@app.get("/levels")
def get_all_levels(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization[7:]
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    levels = get_levels()
    progress = get_user_level_progress(user["id"])
    completed_levels = {p["level_id"] for p in progress}

    return [
        {
            "id": level["id"],
            "level_name": level["level_name"],
            "enemy_name": level["enemies"][0]["enemy_name"]
            if level.get("enemies")
            else "敌人",
            "enemy_hp": sum(e["hp"] for e in level.get("enemies", [])),
            "enemy_attack": level["enemies"][0]["attack"]
            if level.get("enemies")
            else 20,
            "is_unlocked": True,
            "is_completed": level["id"] in completed_levels,
        }
        for level in levels
    ]


@app.get("/levels/{level_id}")
def get_single_level(level_id: int, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization[7:]
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    level = get_level(level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")

    return {
        "id": level["id"],
        "level_name": level["level_name"],
        "enemies": level.get("enemies", []),
    }


@app.post("/levels/{level_id}/complete")
def mark_level_complete(level_id: int, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization[7:]
    data = verify_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    complete_level(user["id"], level_id)
    return {"message": "Level completed"}
