"""
Módulo de repositório para acesso ao banco de dados.
Implementa o padrão Repository para abstrair lógica de acesso a dados.
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.models.database import User, Game, Attempt
from app.schemas.schemas import UserCreate
from typing import List, Optional, Tuple
from datetime import datetime


class UserRepository:
    """Repositório para operações de banco de dados de Usuário."""
    
    @staticmethod
    def create(db: Session, user_data: UserCreate, password_hash: str) -> User:
        """
        Criar um novo usuário no banco de dados.
        
        Args:
            db: Sessão SQLAlchemy
            user_data: Dados de criação do usuário
            password_hash: Senha com hash
            
        Returns:
            User: Objeto do usuário criado
        """
        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=password_hash
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_by_id(db: Session, user_id: str) -> Optional[User]:
        """Obter usuário por ID."""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        """Obter usuário por nome de usuário."""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Obter usuário por email."""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Obter todos os usuários com paginação."""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def user_exists(db: Session, email: str = None, username: str = None) -> bool:
        """Verificar se usuário existe por email ou nome de usuário."""
        query = db.query(User)
        if email:
            query = query.filter(User.email == email)
        if username:
            query = query.filter(User.username == username)
        return query.first() is not None


class GameRepository:
    """Repositório para operações de banco de dados de Jogo."""
    
    @staticmethod
    def create(db: Session, user_id: str, secret_code: List[str]) -> Game:
        """
        Criar um novo jogo para um usuário.
        
        Args:
            db: Sessão SQLAlchemy
            user_id: ID do usuário
            secret_code: Código secreto como uma lista
            
        Returns:
            Game: Objeto do jogo criado
        """
        game = Game(
            user_id=user_id,
            secret_code=secret_code,
            status="started"
        )
        db.add(game)
        db.commit()
        db.refresh(game)
        return game
    
    @staticmethod
    def get_by_id(db: Session, game_id: str) -> Optional[Game]:
        """Obter jogo por ID."""
        return db.query(Game).filter(Game.id == game_id).first()
    
    @staticmethod
    def get_active_game(db: Session, user_id: str) -> Optional[Game]:
        """Obter o jogo ativo (iniciado) para um usuário."""
        return db.query(Game).filter(
            Game.user_id == user_id,
            Game.status == "started"
        ).first()
    
    @staticmethod
    def get_user_games(db: Session, user_id: str, limit: int = 50) -> List[Game]:
        """Obter todos os jogos de um usuário, ordenados por mais recente."""
        return db.query(Game).filter(
            Game.user_id == user_id
        ).order_by(desc(Game.started_at)).limit(limit).all()
    
    @staticmethod
    def end_game(db: Session, game_id: str, status: str, score: float) -> Game:
        """
        Finalizar um jogo com pontuação e status final.
        
        Args:
            db: Sessão SQLAlchemy
            game_id: ID do jogo
            status: Status final (won ou lost)
            score: Pontuação final
            
        Returns:
            Game: Objeto do jogo atualizado
        """
        game = db.query(Game).filter(Game.id == game_id).first()
        if game:
            game.status = status
            game.ended_at = datetime.utcnow()
            game.final_score = score
            db.commit()
            db.refresh(game)
        return game
    
    @staticmethod
    def update_attempt_count(db: Session, game_id: str) -> None:
        """Atualizar o contador de tentativas para um jogo."""
        game = db.query(Game).filter(Game.id == game_id).first()
        if game:
            game.attempts_count = db.query(Attempt).filter(
                Attempt.game_id == game_id
            ).count()
            db.commit()


class AttemptRepository:
    """Repositório para operações de banco de dados de Tentativa."""
    
    @staticmethod
    def create(db: Session, game_id: str, attempt_data: dict) -> Attempt:
        """
        Criar uma nova tentativa em um jogo.
        
        Args:
            db: Sessão SQLAlchemy
            game_id: ID do jogo
            attempt_data: Dicionário com guess, correct_positions, correct_colors, attempt_number
            
        Returns:
            Attempt: Objeto da tentativa criada
        """
        attempt = Attempt(
            game_id=game_id,
            guess=attempt_data["guess"],
            correct_positions=attempt_data["correct_positions"],
            correct_colors=attempt_data["correct_colors"],
            attempt_number=attempt_data["attempt_number"]
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        return attempt
    
    @staticmethod
    def get_by_id(db: Session, attempt_id: str) -> Optional[Attempt]:
        """Obter tentativa por ID."""
        return db.query(Attempt).filter(Attempt.id == attempt_id).first()
    
    @staticmethod
    def get_game_attempts(db: Session, game_id: str) -> List[Attempt]:
        """Obter todas as tentativas de um jogo, ordenadas por número de tentativa."""
        return db.query(Attempt).filter(
            Attempt.game_id == game_id
        ).order_by(Attempt.attempt_number).all()
    
    @staticmethod
    def get_attempt_count(db: Session, game_id: str) -> int:
        """Obter o número de tentativas feitas em um jogo."""
        return db.query(Attempt).filter(Attempt.game_id == game_id).count()
