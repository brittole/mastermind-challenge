"""
Modelos de banco de dados para o jogo Mastermind.
Usa SQLAlchemy ORM para operações com banco de dados.
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
    """
    Modelo de Usuário - representa um jogador no jogo.
    
    Atributos:
        id: Identificador único do usuário (UUID)
        email: Endereço de email do usuário (único)
        username: Nome de usuário para login (único)
        password_hash: Senha com hash (nunca armazenar em texto puro)
        created_at: Timestamp de criação da conta
        updated_at: Timestamp da última atualização
        games: Relacionamento com todos os jogos jogados por este usuário
    """
    
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
    """
    Modelo de Jogo - representa uma única sessão de jogo.
    
    Atributos:
        id: Identificador único do jogo (UUID)
        user_id: Referência ao jogador (chave estrangeira)
        secret_code: A resposta correta (armazenada como array JSON de cores)
        status: Status atual do jogo (iniciado, vencido, perdido)
        started_at: Timestamp de início do jogo
        ended_at: Timestamp de término do jogo (nulo se em andamento)
        final_score: Pontuação final do jogo baseada em tentativas e tempo
        attempts_count: Número de tentativas realizadas
        attempts: Relacionamento com todas as tentativas neste jogo
        user: Relacionamento de volta para o usuário
    """
    
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
    """
    Modelo de Tentativa - representa uma única tentativa num jogo.
    
    Atributos:
        id: Identificador único da tentativa (UUID)
        game_id: Referência ao jogo (chave estrangeira)
        guess: A tentativa do jogador (armazenada como array JSON de cores)
        correct_positions: Número de cores na posição correta (peças pretas)
        correct_colors: Número de cores corretas mas na posição errada (peças brancas)
        attempt_number: Número sequencial da tentativa (1 a 10)
        created_at: Timestamp da tentativa
        game: Relacionamento de volta para o jogo
    """
    
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
