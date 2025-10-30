from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Float,
    BigInteger,
    DateTime,
)
from datetime import datetime

from database.db import SqlAlchemyBase


class Player(SqlAlchemyBase):
    __tablename__ = "players"

    id = Column(BigInteger, unique=True, primary_key=True, nullable=False)
    player_name = Column(String, nullable=False)
    player_team_id = Column(BigInteger, ForeignKey("teams.id"))
    lobby_id = Column(BigInteger, ForeignKey("lobbies.id"))
    status = Column(String, nullable=False, default="inactive") # inactive, leader, player, out_of_team


