"""
Configurações da aplicação via variáveis de ambiente.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações carregadas de variáveis de ambiente."""
    
    # Banco de Dados
    database_url: str = "postgresql://user:password@localhost/mastermind_db"
    
    # JWT
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # App
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Jogo
    mastermind_code_length: int = 4
    mastermind_colors: list = ["red", "blue", "green", "yellow", "white", "black"]
    max_attempts: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Instância de configurações em cache."""
    return Settings()
