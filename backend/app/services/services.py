"""
Módulo de serviços - Camada de lógica de negócio.
Os serviços orquestram repositórios e implementam a lógica de negócio.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Dict
import logging
from app.models.database import User, Game, Attempt
from app.repositories.repositories import UserRepository, GameRepository, AttemptRepository
from app.schemas.schemas import UserCreate, PlayerRankingEntry
from app.utils.mastermind import MastermindGame

logger = logging.getLogger(__name__)


# Configuração de hash de senha - usando Argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class AuthService:
    """Serviço para autenticação e gerenciamento de usuários."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash uma senha usando bcrypt.
        
        Args:
            password: Senha em texto plano
            
        Returns:
            str: Senha com hash
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verificar uma senha em texto plano contra um hash.
        
        Args:
            plain_password: Senha em texto plano
            hashed_password: Senha com hash
            
        Returns:
            bool: True se a senha corresponde
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Criar uma nova conta de usuário.
        
        Args:
            db: Sessão de banco de dados
            user_data: Dados de criação do usuário
            
        Returns:
            User: Usuário criado
            
        Raises:
            ValueError: Se um usuário com esse email ou nome de usuário já existe
        """
        # Verificar se o usuário já existe
        if UserRepository.user_exists(db, email=user_data.email):
            raise ValueError(f"Usuário com email '{user_data.email}' já existe")
        
        if UserRepository.user_exists(db, username=user_data.username):
            raise ValueError(f"Usuário com nome de usuário '{user_data.username}' já existe")
        
        # Hash da senha e criar usuário
        password_hash = AuthService.hash_password(user_data.password)
        return UserRepository.create(db, user_data, password_hash)
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """
        Autenticar um usuário por nome de usuário e senha.
        
        Args:
            db: Sessão de banco de dados
            username: Nome de usuário ou email
            password: Senha em texto plano
            
        Returns:
            User: Objeto do usuário se autenticação bem-sucedida, None caso contrário
        """
        # Tentar encontrar usuário por nome de usuário ou email
        user = UserRepository.get_by_username(db, username)
        if not user:
            user = UserRepository.get_by_email(db, username)
        
        if not user:
            return None
        
        # Verificar senha
        if not AuthService.verify_password(password, user.password_hash):
            return None
        
        return user


class GameService:
    """Serviço para gerenciar jogos e lógica de jogo."""
    
    def __init__(self):
        """Inicializar serviço de jogo com lógica de Mastermind."""
        self.mastermind = MastermindGame()
    
    def start_game(self, db: Session, user_id: str) -> Game:
        """
        Iniciar um novo jogo para um usuário.
        
        Um usuário pode ter apenas um jogo ativo por vez.
        
        Args:
            db: Sessão de banco de dados
            user_id: ID do usuário
            
        Returns:
            Game: Novo objeto do jogo
            
        Raises:
            ValueError: Se usuário já tem um jogo ativo
        """
        # Verificar se usuário tem jogo ativo
        active_game = GameRepository.get_active_game(db, user_id)
        if active_game:
            raise ValueError("Usuário já tem um jogo ativo. Termine ou abandone o jogo atual primeiro.")
        
        # Gerar código secreto
        secret_code = self.mastermind.generate_secret_code()
        
        # Criar jogo
        return GameRepository.create(db, user_id, secret_code)
    
    def make_attempt(self, db: Session, game_id: str, guess: List[str]) -> Tuple[Game, int, int, bool]:
        """
        Processar uma tentativa do jogador.
        
        Args:
            db: Sessão de banco de dados
            game_id: ID do jogo
            guess: Tentativa do jogador (lista de 4 cores)
            
        Returns:
            Tuple contendo:
                - Game: Objeto do jogo atualizado
                - correct_positions: Número de posições corretas
                - correct_colors: Número de cores corretas na posição errada
                - is_won: Se o jogo foi ganho
                
        Raises:
            ValueError: Se o jogo é inválido ou a tentativa é inválida
        """
        # Obter jogo
        game = GameRepository.get_by_id(db, game_id)
        if not game:
            raise ValueError(f"Jogo {game_id} não encontrado")
        
        secret_code = game.secret_code
        if isinstance(secret_code, str):
            import json
            try:
                secret_code = json.loads(secret_code)
            except:
                pass
        
        if game.status != "started":
            raise ValueError(f"Jogo já está {game.status}")
        
        # Verificar contador de tentativas
        if game.attempts_count >= 10:
            raise ValueError("Número máximo de tentativas (10) atingido")
        
        # Validar e avaliar tentativa
        self.mastermind.validate_guess(guess)
        correct_positions, correct_colors = self.mastermind.evaluate_guess(
            secret_code, guess
        )
        
        # Verificar se ganhou
        is_won = correct_positions == 4
        
        # Salvar tentativa
        attempt_number = game.attempts_count + 1
        attempt_data = {
            "guess": guess,
            "correct_positions": correct_positions,
            "correct_colors": correct_colors,
            "attempt_number": attempt_number
        }
        AttemptRepository.create(db, game_id, attempt_data)
        
        # Atualizar contador de tentativas
        GameRepository.update_attempt_count(db, game_id)
        
        # Verificar se jogo foi ganho ou perdido
        if is_won:
            # Jogo ganho
            duration = (datetime.utcnow() - game.started_at).total_seconds()
            score = self.mastermind.calculate_score(attempt_number, duration)
            GameRepository.end_game(db, game_id, "won", score)
        elif attempt_number >= 10:
            # Jogo perdido (tentativas máximas atingidas)
            duration = (datetime.utcnow() - game.started_at).total_seconds()
            score = self.mastermind.calculate_score(10, duration)
            GameRepository.end_game(db, game_id, "lost", score)
        
        # Atualizar jogo para obter dados atualizados
        game = GameRepository.get_by_id(db, game_id)
        
        return game, correct_positions, correct_colors, is_won
    
    def abandon_game(self, db: Session, game_id: str) -> Game:
        """
        Abandonar um jogo em andamento.
        
        Args:
            db: Sessão de banco de dados
            game_id: ID do jogo
            
        Returns:
            Game: Objeto do jogo atualizado
        """
        game = GameRepository.get_by_id(db, game_id)
        if not game:
            raise ValueError(f"Jogo {game_id} não encontrado")
        
        if game.status != "started":
            raise ValueError(f"Não é possível abandonar um jogo {game.status}")
        
        # Calcular pontuação para jogo abandonado
        duration = (datetime.utcnow() - game.started_at).total_seconds()
        score = self.mastermind.calculate_score(game.attempts_count + 1, duration)
        
        return GameRepository.end_game(db, game_id, "lost", score)
    
    def get_game(self, db: Session, game_id: str) -> Game:
        """Obter jogo por ID."""
        game = GameRepository.get_by_id(db, game_id)
        if not game:
            raise ValueError(f"Jogo {game_id} não encontrado")
        return game
    
    def get_active_game(self, db: Session, user_id: str) -> Game:
        """Obter jogo ativo do usuário."""
        game = GameRepository.get_active_game(db, user_id)
        if not game:
            raise ValueError("Nenhum jogo ativo encontrado")
        return game
    
    def get_user_games(self, db: Session, user_id: str) -> List[Game]:
        """Obter todos os jogos de um usuário."""
        return GameRepository.get_user_games(db, user_id)


class RankingService:
    """Serviço para calcular e recuperar classificações."""
    
    @staticmethod
    def get_global_ranking(db: Session, limit: int = 100) -> List[PlayerRankingEntry]:
        """
        Obter classificação global de todos os jogadores.
        
        Classificação baseada em:
        1. Taxa de vitória (percentual de jogos ganhos)
        2. Melhor pontuação
        3. Pontuação média
        
        Args:
            db: Sessão de banco de dados
            limit: Número máximo de jogadores a retornar
            
        Returns:
            List[PlayerRankingEntry]: Lista ordenada de classificações de jogadores
        """
        # Obter todos os usuários
        users = UserRepository.get_all(db, limit=limit)
        
        rankings = []
        
        for user in users:
            # Obter jogos do usuário
            games = GameRepository.get_user_games(db, user.id, limit=1000)
            
            if not games:
                continue
            
            # Calcular estatísticas
            total_games = len(games)
            games_won = sum(1 for game in games if game.status == "won")
            win_rate = (games_won / total_games * 100) if total_games > 0 else 0
            
            # Obter pontuações
            scores = [game.final_score for game in games if game.final_score is not None]
            best_score = max(scores) if scores else 0
            average_score = sum(scores) / len(scores) if scores else 0
            
            ranking = PlayerRankingEntry(
                rank=0,  # Será definido após ordenação
                username=user.username,
                email=user.email,
                total_games=total_games,
                games_won=games_won,
                win_rate=round(win_rate, 2),
                best_score=round(best_score, 2),
                average_score=round(average_score, 2)
            )
            rankings.append(ranking)
        
        # Ordenar por taxa de vitória (descendente), depois melhor pontuação (descendente)
        rankings.sort(
            key=lambda x: (x.win_rate, x.best_score),
            reverse=True
        )
        
        # Atribuir posições
        for i, ranking in enumerate(rankings, 1):
            ranking.rank = i
        
        return rankings
    
    @staticmethod
    def get_user_stats(db: Session, user_id: str) -> Dict:
        """
        Obter estatísticas para um usuário específico.
        
        Args:
            db: Sessão de banco de dados
            user_id: ID do usuário
            
        Returns:
            Dict com estatísticas do usuário
        """
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise ValueError(f"Usuário {user_id} não encontrado")
        
        games = GameRepository.get_user_games(db, user_id, limit=1000)
        
        total_games = len(games)
        games_won = sum(1 for game in games if game.status == "won")
        games_lost = sum(1 for game in games if game.status == "lost")
        
        scores = [game.final_score for game in games if game.final_score is not None]
        
        return {
            "user_id": user_id,
            "username": user.username,
            "email": user.email,
            "total_games": total_games,
            "games_won": games_won,
            "games_lost": games_lost,
            "win_rate": round((games_won / total_games * 100) if total_games > 0 else 0, 2),
            "best_score": round(max(scores), 2) if scores else 0,
            "average_score": round(sum(scores) / len(scores), 2) if scores else 0,
            "total_attempts": sum(game.attempts_count for game in games),
            "average_attempts": round(sum(game.attempts_count for game in games) / total_games, 2) if total_games > 0 else 0
        }
