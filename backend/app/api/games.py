"""
Rotas da API de Jogos.
Trata de criação de jogo, tentativas e estado do jogo.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.schemas import GameStart, GameResponse, GameResultResponse, AttemptCreate, AttemptResponse, ErrorResponse
from app.services.services import GameService
from app.repositories.repositories import AttemptRepository
from app.dependencies import get_db, get_current_user
from app.models.database import User


router = APIRouter(
    prefix="/api/games",
    tags=["Jogos"],
    responses={
        400: {"model": ErrorResponse, "description": "Solicitação inválida"},
        401: {"model": ErrorResponse, "description": "Não autorizado"},
        404: {"model": ErrorResponse, "description": "Não encontrado"},
    }
)

game_service = GameService()


@router.get(
    "/active",
    response_model=GameResponse,
    summary="Obter jogo ativo",
    description="Obter o jogo ativo do usuário (se houver)"
)
def get_active_game(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> GameResponse:
    """
    Obter o jogo ativo do usuário.
    
    Args:
        current_user: Usuário autenticado
        db: Sessão de banco de dados
        
    Returns:
        GameResponse: Jogo ativo, ou None se não houver
        
    Raises:
        HTTPException 404: Se nãohouver jogo ativo
    """
    try:
        from app.repositories.repositories import GameRepository
        game = GameRepository.get_active_game(db, current_user.id)
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum jogo ativo encontrado"
            )
        return GameResponse.from_orm(game)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/start",
    response_model=GameResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Iniciar um novo jogo",
    description="Criar e iniciar um novo jogo de Mastermind para o usuário atual"
)
def start_game(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> GameResponse:
    """
    Iniciar um novo jogo.
    
    Args:
        current_user: Usuário autenticado
        db: Sessão de banco de dados
        
    Returns:
        GameResponse: Novo jogo com lista vazia de tentativas
        
    Raises:
        HTTPException 400: Se o usuário já tem um jogo ativo
    """
    try:
        game = game_service.start_game(db, current_user.id)
        
        # Buscar jogo atualizado com tentativas
        game = game_service.get_game(db, game.id)
        
        return GameResponse.from_orm(game)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/{game_id}",
    response_model=GameResponse,
    summary="Obter estado do jogo",
    description="Obter estado atual de um jogo (sem revelar código secreto)"
)
def get_game(
    game_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> GameResponse:
    """
    Obter estado atual do jogo.
    
    Args:
        game_id: ID do jogo
        current_user: Usuário autenticado
        db: Sessão de banco de dados
        
    Returns:
        GameResponse: Estado do jogo com todas as tentativas
        
    Raises:
        HTTPException 404: Se o jogo não for encontrado
        HTTPException 401: Se o jogo não pertence ao usuário
    """
    try:
        game = game_service.get_game(db, game_id)
        
        # Verificar propriedade
        if game.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )
        
        return GameResponse.from_orm(game)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/{game_id}/attempt",
    response_model=AttemptResponse,
    summary="Fazer uma tentativa no jogo",
    description="Submeter uma adivinhar e receber retorno"
)
def make_attempt(
    game_id: str,
    attempt_data: AttemptCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AttemptResponse:
    """
    Fazer uma tentativa/adivinhar em um jogo.
    
    Args:
        game_id: ID do jogo
        attempt_data: Dados de adivinhar (lista de 4 cores)
        current_user: Usuário autenticado
        db: Sessão de banco de dados
        
    Returns:
        AttemptResponse: Retorno sobre a adivinhar
        
    Raises:
        HTTPException 400: Se a adivinhar é inválida ou contador de tentativas excedido
        HTTPException 404: Se o jogo não for encontrado
        HTTPException 401: Se o jogo não pertence ao usuário
    """
    try:
        # Verificar propriedade do jogo
        game = game_service.get_game(db, game_id)
        if game.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )
        
        # Fazer tentativa
        game, correct_positions, correct_colors, is_won = game_service.make_attempt(
            db, game_id, attempt_data.guess
        )
        
        # Obter tentativa mais recente
        attempts = AttemptRepository.get_game_attempts(db, game_id)
        latest_attempt = attempts[-1] if attempts else None
        
        if not latest_attempt:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Falha ao criar tentativa"
            )
        
        return AttemptResponse.from_orm(latest_attempt)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/{game_id}/result",
    response_model=GameResultResponse,
    summary="Obter resultado do jogo (quando finalizado)",
    description="Obter o resultado completo do jogo incluindo o código secreto (apenas quando o jogo está finalizado)"
)
def get_game_result(
    game_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> GameResultResponse:
    """
    Obter resultado completo do jogo com código secreto revelado.
    Só retorna o código secreto quando o jogo está finalizado.
    
    Args:
        game_id: ID do jogo
        current_user: Usuário autenticado
        db: Sessão de banco de dados
        
    Returns:
        GameResultResponse: Jogo com código secreto se finalizado
        
    Raises:
        HTTPException 404: Se o jogo não for encontrado
        HTTPException 401: Se o jogo não pertence ao usuário
        HTTPException 400: Se o jogo ainda está ativo
    """
    try:
        game = game_service.get_game(db, game_id)
        
        # Verificar propriedade
        if game.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )
        
        # Verificar se o jogo está finalizado
        if game.status == "started":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Jogo ainda está ativo"
            )
        
        result = GameResultResponse.from_orm(game)
        result.secret_code = game.secret_code
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/{game_id}/abandon",
    response_model=GameResponse,
    summary="Abandonar um jogo",
    description="Abandonar o jogo atual (jogo será marcado como perdido)"
)
def abandon_game(
    game_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> GameResponse:
    """
    Abandonar um jogo em andamento.
    
    Args:
        game_id: ID do jogo
        current_user: Usuário autenticado
        db: Sessão de banco de dados
        
    Returns:
        GameResponse: Jogo atualizado (marcado como perdido)
        
    Raises:
        HTTPException 400: Se o jogo já está finalizado
        HTTPException 404: Se o jogo não for encontrado
        HTTPException 401: Se o jogo não pertence ao usuário
    """
    try:
        game = game_service.get_game(db, game_id)
        
        # Verificar propriedade
        if game.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )
        
        game = game_service.abandon_game(db, game_id)
        
        return GameResponse.from_orm(game)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "",
    response_model=List[GameResponse],
    summary="Obter jogos do usuário",
    description="Obter todos os jogos do usuário atual"
)
def get_user_games(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[GameResponse]:
    """
    Obter todos os jogos do usuário atual.
    
    Args:
        current_user: Usuário autenticado
        db: Sessão de banco de dados
        
    Returns:
        List[GameResponse]: Lista de todos os jogos do usuário
    """
    games = game_service.get_user_games(db, current_user.id)
    return [GameResponse.from_orm(game) for game in games]
