from fastapi import APIRouter, Header, HTTPException
from fastapi.encoders import jsonable_encoder

from database import controllers

router = APIRouter()

@router.post("/add_player")
async def add_player(player_name: str, player_id: str):
    player = await controllers.add_player(player_name, player_id)
    return jsonable_encoder(player)

@router.post("/join_lobby")
async def join_lobby(lobby_code: str, player_id: str):
    lobby = await controllers.join_lobby(lobby_code, player_id)
    players = await controllers.get_lobby_players(str(lobby.id))
    teams = await controllers.get_lobby_teams(str(lobby.id))
    return jsonable_encoder({
        "lobby": lobby,
        "players": players,
        "teams": teams
    })

@router.get("/get_lobby_by_code")
async def get_lobby_by_code(lobby_code: str):
    lobby = await controllers.get_lobby_by_code(lobby_code)
    if not lobby:
        raise HTTPException(status_code=404, detail="Lobby not found")
    players = await controllers.get_lobby_players(str(lobby.id))
    teams = await controllers.get_lobby_teams(str(lobby.id))
    return jsonable_encoder({
        "lobby": lobby,
        "players": players,
        "teams": teams
    })

@router.post("/create_lobby")
async def create_lobby(player_id: str):
    lobby = await controllers.create_lobby(player_id)
    return {
        "id": lobby.id,
        "lobby_code": lobby.lobby_code,
        "organizer_id": lobby.organizer_id
    }

@router.post("/create_team")
async def create_team(lobby_id: str, team_name: str, team_leader_id: str):
    team = await controllers.create_team(lobby_id, team_name, team_leader_id)
    return jsonable_encoder(team)

@router.post("/add_player_to_team")
async def add_player_to_team(team_id: str, player_id: str):
    player = await controllers.add_player_to_team(team_id, player_id)
    return jsonable_encoder(player)