"""
Esquemas Pydantic para validação de requisição/resposta.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Esquema para registro/criação de usuário."""
    email: EmailStr = Field(..., description="Endereço de email do usuário (deve ser único)")
    username: str = Field(..., min_length=3, max_length=100, description="Nome de usuário para login")
    password: str = Field(..., min_length=6, description="Senha (mínimo 6 caracteres)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "john_doe",
                "password": "secure_password_123"
            }
        }


class UserResponse(BaseModel):
    """Resposta de usuário (sem senha)."""
    id: str
    email: str
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Requisição de login."""
    email: str
    password: str


class TokenResponse(BaseModel):
    """Resposta com token JWT."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class AttemptCreate(BaseModel):
    """Dados para submeter uma tentativa."""
    guess: List[str] = Field(..., min_length=4, max_length=4)


class AttemptResponse(BaseModel):
    """Resposta de uma tentativa com feedback."""
    id: str
    attempt_number: int
    guess: List[str]
    correct_positions: int = Field(..., ge=0, le=4)
    correct_colors: int = Field(..., ge=0, le=4)
    created_at: datetime
    
    class Config:
        from_attributes = True


class GameStart(BaseModel):
    """Esquema para iniciar um novo jogo."""
    pass  # Sem parâmetros necessários - sistema gera tudo


class GameResponse(BaseModel):
    """Informações do jogo (sem revelar o código secreto)."""
    id: str
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    attempts_count: int = Field(..., ge=0, le=10)
    final_score: Optional[float] = None
    attempts: List[AttemptResponse] = Field(default_factory=list)
    
    class Config:
        from_attributes = True


class GameResultResponse(GameResponse):
    """Resultado do jogo com código secreto revelado."""
    secret_code: Optional[List[str]] = None


class PlayerRankingEntry(BaseModel):
    """Entrada de classificação de um jogador."""
    rank: int
    username: str
    email: str
    total_games: int = Field(..., ge=0)
    games_won: int = Field(..., ge=0)
    win_rate: float = Field(..., ge=0, le=100)
    best_score: float
    average_score: float


class RankingResponse(BaseModel):
    """Classificação global."""
    total_players: int
    total_games_played: int
    total_victories: int
    average_win_rate: float
    players: List[PlayerRankingEntry]


class ErrorResponse(BaseModel):
    """Resposta de erro."""
    detail: str
    status_code: int
