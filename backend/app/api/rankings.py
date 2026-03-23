"""
Rotas da API de Classificações.
Trata de recuperação de classificação e estatísticas.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.schemas import RankingResponse, ErrorResponse
from app.services.services import RankingService
from app.dependencies import get_db, get_current_user
from app.models.database import User


router = APIRouter(
    prefix="/api/rankings",
    tags=["Classificações"],
    responses={
        400: {"model": ErrorResponse, "description": "Solicitação inválida"},
        404: {"model": ErrorResponse, "description": "Não encontrado"},
    }
)


@router.get(
    "",
    response_model=RankingResponse,
    summary="Obter classificação global",
    description="Obter a classificação global de todos os jogadores com base no desempenho"
)
def get_global_ranking(
    limit: int = 100,
    db: Session = Depends(get_db)
) -> RankingResponse:
    """
    Obter classificação global.
    
    A classificação é calculada baseada em:
    1. Taxa de vitória (percentual de jogos ganhos)
    2. Melhor pontuação
    3. Pontuação média
    
    Args:
        limit: Número máximo de jogadores a retornar
        db: Sessão de banco de dados
        
    Returns:
        RankingResponse: Lista classificada de jogadores
    """
    try:
        players = RankingService.get_global_ranking(db, limit=limit)
        
        # Calcular estatísticas globais
        total_games_played = sum(player.total_games for player in players)
        total_victories = sum(player.games_won for player in players)
        average_win_rate = (
            sum(player.win_rate for player in players) / len(players)
            if len(players) > 0
            else 0.0
        )
        
        return RankingResponse(
            total_players=len(players),
            total_games_played=total_games_played,
            total_victories=total_victories,
            average_win_rate=round(average_win_rate, 2),
            players=players
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/user/{user_id}",
    summary="Obter estatísticas do usuário",
    description="Obter estatísticas detalhadas para um usuário específico"
)
def get_user_stats(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Obter estatísticas de um usuário.
    
    Retorna:
        Dicionário com estatísticas do usuário incluindo:
        - Total de jogos jogados
        - Jogos ganhos/perdidos
        - Taxa de vitória
        - Melhor e pontuação média
        - Tentativas médias por jogo
        
    Args:
        user_id: ID do usuário
        db: Sessão de banco de dados
        
    Returns:
        dict: Estatísticas do usuário
        
    Raises:
        HTTPException 404: Se o usuário não for encontrado
    """
    try:
        stats = RankingService.get_user_stats(db, user_id)
        return stats
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
