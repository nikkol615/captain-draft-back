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


class Lobby(SqlAlchemyBase):
    __tablename__ = "lobbies"

    id = Column(BigInteger, unique=True, primary_key=True, nullable=False, autoincrement=True)
    lobby_code = Column(String, nullable=False, unique=True)
    organizer_id = Column(BigInteger, ForeignKey("players.id"))

