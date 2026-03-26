"""
Modelos de banco de dados (SQLAlchemy ORM).
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import json


def parse_json_field(value):
    """Helper para fazer parse de campos JSON que podem ser strings."""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except:
            return value
    return value

Base = declarative_base()


class User(Base):
    """Modelo de usuário/jogador."""
    
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    games = relationship("Game", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class Game(Base):
    """Modelo de jogo (uma sessão de jogo)."""
    
    __tablename__ = "games"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    secret_code = Column(JSON, nullable=False)  # Array like ["red", "blue", "green", "yellow"]
    status = Column(String(20), default="started", nullable=False)  # started, won, lost
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    final_score = Column(Float, nullable=True)
    attempts_count = Column(Integer, default=0, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="games")
    attempts = relationship("Attempt", back_populates="game", cascade="all, delete-orphan")
    
    def __getattribute__(self, name):
        """Override para fazer parse de secret_code automaticamente."""
        value = super().__getattribute__(name)
        if name == 'secret_code':
            return parse_json_field(value)
        return value
    
    def get_duration_seconds(self) -> float:
        """Calcular duração do jogo em segundos."""
        end_time = self.ended_at or datetime.utcnow()
        return (end_time - self.started_at).total_seconds()
    
    def __repr__(self):
        return f"<Game(id={self.id}, user_id={self.user_id}, status={self.status})>"


class Attempt(Base):
    """Modelo de tentativa numa partida."""
    
    __tablename__ = "attempts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    game_id = Column(String(36), ForeignKey("games.id"), nullable=False, index=True)
    guess = Column(JSON, nullable=False)  # Array like ["red", "blue", "green", "yellow"]
    correct_positions = Column(Integer, default=0, nullable=False)  # Black pegs
    correct_colors = Column(Integer, default=0, nullable=False)  # White pegs
    attempt_number = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    game = relationship("Game", back_populates="attempts")
    
    def __getattribute__(self, name):
        """Override para fazer parse de guess automaticamente."""
        value = super().__getattribute__(name)
        if name == 'guess':
            return parse_json_field(value)
        return value
    
    def __repr__(self):
        return f"<Attempt(game_id={self.game_id}, attempt={self.attempt_number}, correct_positions={self.correct_positions})>"
