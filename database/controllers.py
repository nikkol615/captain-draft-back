from database.db import create_session
from models.lobby import Lobby
from models.player import Player
from models.team import Team
import uuid
from sqlalchemy.orm import Session
from datetime import datetime


@create_session
async def get_lobby_by_code(lobby_code: str, db: Session):
    lobby = db.query(Lobby).filter(Lobby.lobby_code == lobby_code).first()
    return lobby

@create_session
async def add_player(player_name: str, player_id: str, db: Session):
    player_id_int = int(player_id)
    # Проверяем, существует ли игрок
    existing_player = db.query(Player).filter(Player.id == player_id_int).first()
    if existing_player:
        # Обновляем имя если изменилось
        existing_player.player_name = player_name
        db.commit()
        db.refresh(existing_player)
        return existing_player
    
    # Создаем нового игрока
    player = Player(id=player_id_int, player_name=player_name, status="inactive")
    db.add(player)
    db.commit()
    db.refresh(player)
    return player

@create_session
async def get_lobby_players(lobby_id: str, db: Session):
    lobby_id_int = int(lobby_id)
    players = db.query(Player).filter(Player.lobby_id == lobby_id_int).all()
    return players

@create_session
async def get_lobby_teams(lobby_id: str, db: Session):
    lobby_id_int = int(lobby_id)
    teams = db.query(Team).filter(Team.lobby_id == lobby_id_int).all()
    return teams


@create_session
async def create_lobby(organizer_id: str, db: Session):
    lobby_code = uuid.uuid4().hex[:6].upper()
    organizer_id_int = int(organizer_id)
    
    # Проверяем существование игрока
    player = db.query(Player).filter(Player.id == organizer_id_int).first()
    if not player:
        raise Exception("Player not found")
    
    # Создаем лобби
    lobby = Lobby(organizer_id=organizer_id_int, lobby_code=lobby_code)
    db.add(lobby)
    db.flush()  # Сохраняем лобби чтобы получить ID
    
    # Добавляем организатора в лобби
    player.status = "out_of_team"
    player.lobby_id = lobby.id
    
    db.commit()
    db.refresh(lobby)
    db.refresh(player)
    return lobby

@create_session
async def join_lobby(lobby_code: str, player_id: str, db: Session):
    player_id_int = int(player_id)
    lobby = db.query(Lobby).filter(Lobby.lobby_code == lobby_code).first()
    if not lobby:
        raise Exception("No lobby found")
    player = db.query(Player).filter(Player.id == player_id_int).first()
    if not player:
        raise Exception("Player not found")
    player.status = "out_of_team"
    player.lobby_id = lobby.id
    db.commit()
    db.refresh(lobby)
    db.refresh(player)
    return lobby

@create_session
async def create_team(lobby_id: str, team_name: str, team_leader_id: str, db: Session):
    lobby_id_int = int(lobby_id)
    team_leader_id_int = int(team_leader_id)
    team = Team(lobby_id=lobby_id_int, team_name=team_name, team_leader_id=team_leader_id_int)
    db.add(team)
    db.flush()  # Получаем ID команды
    
    player = db.query(Player).filter(Player.id == team_leader_id_int).first()
    if not player:
        raise Exception("No player found")
    if player.lobby_id != lobby_id_int:
        raise Exception("Player is not in the lobby")
    if player.status != "out_of_team":
        raise Exception("Player is not out of team")
    player.status = "leader"
    player.player_team_id = team.id
    
    db.commit()
    db.refresh(team)
    db.refresh(player)
    return team

@create_session
async def add_player_to_team(team_id: str, player_id: str, db: Session):
    team_id_int = int(team_id)
    player_id_int = int(player_id)
    team = db.query(Team).filter(Team.id == team_id_int).first()
    if not team:
        raise Exception("No team found")
    player = db.query(Player).filter(Player.id == player_id_int).first()
    if not player:
        raise Exception("No player found")
    if team.lobby_id != player.lobby_id:
        raise Exception("Player is not in the lobby")
    if player.status != "out_of_team":
        raise Exception("Player is not out of team")
    player.status = "player"
    player.player_team_id = team.id
    db.commit()
    db.refresh(player)
    return player