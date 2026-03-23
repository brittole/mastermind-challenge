"""
Módulo de configuração da aplicação FastAPI.
Gerencia variáveis de ambiente e configurações da aplicação.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas de variáveis de ambiente.
    Usa pydantic-settings para validação e conversão de tipos.
    """
    
    # Configuração do Banco de Dados
    database_url: str = "postgresql://user:password@localhost/mastermind_db"
    
    # Configuração JWT
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Configuração da Aplicação
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Configuração do Jogo
    mastermind_code_length: int = 4
    mastermind_colors: list = ["red", "blue", "green", "yellow", "white", "black"]
    max_attempts: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Obtém instância de configurações em cache.
    Esta função é cacheada para evitar ler variáveis de ambiente múltiplas vezes.
    
    Retorna:
        Settings: Instância das configurações da aplicação
    """
    return Settings()
