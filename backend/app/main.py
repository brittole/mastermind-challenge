"""
Factory da aplicação FastAPI.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import logging
from app.config import get_settings
from app.models.database import Base
from app.api import auth, games, rankings
from app.dependencies import get_db as _get_db


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Engine do banco de dados e factory de sessões globais
engine = None
SessionLocal = None


def initialize_database():
    """Inicializa conexão com banco de dados e cria tabelas."""
    global engine, SessionLocal
    
    settings = get_settings()
    
    # Criar engine de banco de dados
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
    
    # Criar factory de sessões
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    
    logger.info("Banco de dados inicializado com sucesso")


def get_db():
    """Dependência para obter sessão de banco de dados."""
    if SessionLocal is None:
        raise RuntimeError("Banco de dados não inicializado. Chamar initialize_database() primeiro.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def setup_dependencies():
    """Configurar a dependência get_db com SessionLocal da app."""
    import app.dependencies as deps
    deps.SessionLocal = SessionLocal


def create_app() -> FastAPI:
    """Criar e configurar a aplicação FastAPI."""
    settings = get_settings()
    
    # Criar instância FastAPI
    app = FastAPI(
        title="API do Jogo Mastermind",
        description="API RESTful para o jogo Mastermind",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json"
    )
    
    # Inicializar banco de dados
    initialize_database()
    setup_dependencies()
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:4200",  # Porta padrão Angular
            "http://127.0.0.1:3000",
            "http://127.0.0.1:4200",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Registrar routers
    app.include_router(auth.router)
    app.include_router(games.router)
    app.include_router(rankings.router)
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Tratar ValueError."""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc), "status_code": 400}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Tratar exceções inesperadas."""
        logger.error(f"Erro inesperado: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Erro interno do servidor", "status_code": 500}
        )
    
    # Endpoint de verificação de saúde
    @app.get("/health")
    async def health_check():
        """Endpoint de verificação de saúde da API."""
        return {
            "status": "saudável",
            "mensagem": "API Mastermind está em funcionamento"
        }
    
    # Endpoint raiz com informações da API
    @app.get("/")
    async def root():
        """Endpoint raiz com informações da API."""
        return {
            "api": "API do Jogo Mastermind",
            "versao": "1.0.0",
            "docs": "/api/docs",
            "health": "/health"
        }
    
    # Evento de inicialização
    @app.on_event("startup")
    async def startup_event():
        logger.info("Aplicação iniciada")
    
    # Evento de encerramento
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Aplicação encerrada")
    
    return app


# Criar instância da aplicação
app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
