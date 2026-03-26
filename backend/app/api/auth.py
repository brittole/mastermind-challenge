"""
Rotas de autenticação (registro e login).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.schemas.schemas import UserCreate, LoginRequest, TokenResponse, UserResponse, ErrorResponse
from app.services.services import AuthService
from app.dependencies import get_db, create_access_token
from app.config import get_settings


router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticação"],
    responses={
        400: {"model": ErrorResponse, "description": "Solicitação inválida"},
        401: {"model": ErrorResponse, "description": "Não autorizado"},
    }
)


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
    description="Criar uma nova conta de usuário e receber um token de acesso"
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """Registrar novo usuário e retornar token."""
    try:
        # Criar usuário
        user = AuthService.create_user(db, user_data)
        
        # Gerar token
        settings = get_settings()
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.from_orm(user)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login do usuário",
    description="Autenticar usuário com nome de usuário/email e senha"
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """Fazer login e retornar token."""
    # Autenticar usuário
    user = AuthService.authenticate_user(db, credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    
    # Gerar token
    settings = get_settings()
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )
