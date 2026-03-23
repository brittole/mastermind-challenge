"""
Esquemas Pydantic para validação de requisição/resposta e documentação da API.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


# ============================================================================
# ESQUEMAS DE USUÁRIO
# ============================================================================

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
    """Esquema para resposta de usuário (nunca inclui senha)."""
    id: str = Field(..., description="Identificador único do usuário")
    email: str = Field(..., description="Email do usuário")
    username: str = Field(..., description="Nome de usuário")
    created_at: datetime = Field(..., description="Timestamp de criação da conta")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "username": "john_doe",
                "created_at": "2024-03-23T10:15:00Z"
            }
        }


# ============================================================================
# ESQUEMAS DE AUTENTICAÇÃO
# ============================================================================

class LoginRequest(BaseModel):
    """Esquema para requisição de login."""
    email: str = Field(..., description="Email do usuário ou nome de usuário")
    password: str = Field(..., description="Senha do usuário")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "secure_password_123"
            }
        }


class TokenResponse(BaseModel):
    """Esquema para resposta de token de autenticação."""
    access_token: str = Field(..., description="Token de acesso JWT")
    token_type: str = Field(default="bearer", description="Tipo de token (sempre 'bearer')")
    user: UserResponse = Field(..., description="Informações do usuário")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "user@example.com",
                    "username": "john_doe",
                    "created_at": "2024-03-23T10:15:00Z"
                }
            }
        }


# ============================================================================
# ESQUEMAS DE TENTATIVA
# ============================================================================

class AttemptCreate(BaseModel):
    """Esquema para submeter uma tentativa/adivinhar do jogo."""
    guess: List[str] = Field(..., min_items=4, max_items=4, description="Array de 4 cores (ex: ['red', 'blue', 'green', 'yellow'])")
    
    class Config:
        json_schema_extra = {
            "example": {
                "guess": ["red", "blue", "green", "yellow"]
            }
        }


class AttemptResponse(BaseModel):
    """Esquema para resposta de tentativa com retorno."""
    id: str = Field(..., description="Identificador único da tentativa")
    attempt_number: int = Field(..., description="Número sequencial da tentativa (1-10)")
    guess: List[str] = Field(..., description="Adivinhar do jogador")
    correct_positions: int = Field(..., ge=0, le=4, description="Número de cores na posição correta (peças pretas)")
    correct_colors: int = Field(..., ge=0, le=4, description="Número de cores corretas mas na posição errada (peças brancas)")
    created_at: datetime = Field(..., description="Timestamp da tentativa")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "attempt_number": 1,
                "guess": ["red", "blue", "green", "yellow"],
                "correct_positions": 2,
                "correct_colors": 1,
                "created_at": "2024-03-23T10:16:00Z"
            }
        }


# ============================================================================
# ESQUEMAS DE JOGO
# ============================================================================

class GameStart(BaseModel):
    """Esquema para iniciar um novo jogo."""
    pass  # Sem parâmetros necessários - sistema gera tudo


class GameResponse(BaseModel):
    """Esquema para informações do jogo (sem revelar o código secreto)."""
    id: str = Field(..., description="Identificador único do jogo")
    status: str = Field(..., description="Status do jogo: started, won, lost")
    started_at: datetime = Field(..., description="Timestamp de início do jogo")
    ended_at: Optional[datetime] = Field(None, description="Timestamp de fim do jogo")
    attempts_count: int = Field(..., ge=0, le=10, description="Número de tentativas feitas")
    final_score: Optional[float] = Field(None, description="Pontuação final do jogo")
    attempts: List[AttemptResponse] = Field(default_factory=list, description="Todas as tentativas neste jogo")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440002",
                "status": "started",
                "started_at": "2024-03-23T10:15:00Z",
                "ended_at": None,
                "attempts_count": 2,
                "final_score": None,
                "attempts": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440001",
                        "attempt_number": 1,
                        "guess": ["red", "blue", "green", "yellow"],
                        "correct_positions": 2,
                        "correct_colors": 1,
                        "created_at": "2024-03-23T10:16:00Z"
                    }
                ]
            }
        }


class GameResultResponse(GameResponse):
    """Esquema para resultado do jogo (mostrado apenas quando o jogo termina)."""
    secret_code: Optional[List[str]] = Field(None, description="O código secreto (revelado apenas no fim do jogo)")


# ============================================================================
# ESQUEMAS DE CLASSIFICAÇÃO
# ============================================================================

class PlayerRankingEntry(BaseModel):
    """Esquema para entrada de classificação de um jogador."""
    rank: int = Field(..., description="Posição do jogador")
    username: str = Field(..., description="Nome de usuário do jogador")
    email: str = Field(..., description="Email do jogador")
    total_games: int = Field(..., ge=0, description="Total de jogos jogados")
    games_won: int = Field(..., ge=0, description="Jogos ganhos")
    win_rate: float = Field(..., ge=0, le=100, description="Percentual de vitórias")
    best_score: float = Field(..., description="Melhor pontuação do jogo")
    average_score: float = Field(..., description="Pontuação média em todos os jogos")
    
    class Config:
        json_schema_extra = {
            "example": {
                "rank": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "total_games": 15,
                "games_won": 12,
                "win_rate": 80.0,
                "best_score": 950.5,
                "average_score": 850.3
            }
        }


class RankingResponse(BaseModel):
    """Esquema para classificação global."""
    total_players: int = Field(..., description="Número total de jogadores")
    total_games_played: int = Field(..., description="Número total de jogos jogados")
    total_victories: int = Field(..., description="Número total de vitórias")
    average_win_rate: float = Field(..., description="Taxa média de vitória (%)")
    players: List[PlayerRankingEntry] = Field(..., description="Lista de jogadores classificados")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_players": 5,
                "total_games_played": 50,
                "total_victories": 35,
                "average_win_rate": 70.0,
                "players": [
                    {
                        "rank": 1,
                        "username": "john_doe",
                        "email": "john@example.com",
                        "total_games": 15,
                        "games_won": 12,
                        "win_rate": 80.0,
                        "best_score": 950.5,
                        "average_score": 850.3
                    }
                ]
            }
        }


# ============================================================================
# ESQUEMAS DE ERRO
# ============================================================================

class ErrorResponse(BaseModel):
    """Esquema para respostas de erro."""
    detail: str = Field(..., description="Mensagem de erro")
    status_code: int = Field(..., description="Código de status HTTP")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Credenciais inválidas",
                "status_code": 401
            }
        }
