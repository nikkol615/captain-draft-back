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


class Team(SqlAlchemyBase):
    __tablename__ = "teams"

    id = Column(BigInteger, unique=True, primary_key=True, nullable=False, autoincrement=True)
    lobby_id = Column(BigInteger, ForeignKey("lobbies.id"))
    team_name = Column(String, nullable=False)
    team_leader_id = Column(BigInteger, ForeignKey("players.id"))


