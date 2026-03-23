"""
Testes de integração para endpoints da API.
"""

import pytest
import json
from app.schemas.schemas import UserCreate
from app.services.services import AuthService


class TestAuthEndpoints:
    """Testar endpoints de autenticação."""
    
    def test_register_success(self, client, db, test_user_data):
        """Testar registro de usuário bem-sucedido."""
        response = client.post(
            "/api/auth/register",
            json=test_user_data
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["access_token"]
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == test_user_data["username"]
        assert data["user"]["email"] == test_user_data["email"]
        assert "password" not in data["user"]
    
    def test_register_invalid_email(self, client):
        """Testar registro com email inválido."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "invalid-email",
                "username": "testuser",
                "password": "password123"
            }
        )
        
        assert response.status_code == 422  # Erro de validação
    
    def test_register_short_password(self, client):
        """Testar registro com senha curta."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "short"
            }
        )
        
        assert response.status_code == 422  # Erro de validação
    
    def test_register_duplicate_email(self, client, db, test_user_data):
        """Testar registro com email duplicado."""
        # Registrar primeiro usuário
        client.post("/api/auth/register", json=test_user_data)
        
        # Tentar registrar com o mesmo email
        response = client.post(
            "/api/auth/register",
            json={
                "email": test_user_data["email"],
                "username": "different_username",
                "password": test_user_data["password"]
            }
        )
        
        assert response.status_code == 400
        assert "já existe" in response.json()["detail"]
    
    def test_login_success(self, client, db, test_user_data):
        """Testar login bem-sucedido."""
        # Registrar usuário
        client.post("/api/auth/register", json=test_user_data)
        
        # Login
        response = client.post(
            "/api/auth/login",
            json={
                "email": test_user_data["username"],
                "password": test_user_data["password"]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["access_token"]
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == test_user_data["username"]
    
    def test_login_with_email(self, client, db, test_user_data):
        """Testar login com email em vez de nome de usuário."""
        # Registrar usuário
        client.post("/api/auth/register", json=test_user_data)
        
        # Login com email
        response = client.post(
            "/api/auth/login",
            json={
                "email": test_user_data["email"],
                "password": test_user_data["password"]
            }
        )
        
        assert response.status_code == 200
        assert response.json()["user"]["email"] == test_user_data["email"]
    
    def test_login_invalid_credentials(self, client, db, test_user_data):
        """Testar login com credenciais inválidas."""
        # Registrar usuário
        client.post("/api/auth/register", json=test_user_data)
        
        # Tentar fazer login com senha errada
        response = client.post(
            "/api/auth/login",
            json={
                "email": test_user_data["username"],
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
        assert "inválidas" in response.json()["detail"].lower()
    
    def test_login_nonexistent_user(self, client):
        """Testar login com usuário inexistente."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent",
                "password": "password"
            }
        )
        
        assert response.status_code == 401


class TestGameEndpoints:
    """Testar endpoints de jogo."""
    
    @pytest.fixture
    def auth_token(self, client, test_user_data):
        """Obter token de autenticação."""
        response = client.post("/api/auth/register", json=test_user_data)
        return response.json()["access_token"]
    
    def test_start_game_success(self, client, auth_token):
        """Testar início de um novo jogo."""
        response = client.post(
            "/api/games/start",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["id"]
        assert data["status"] == "started"
        assert data["attempts_count"] == 0
        assert data["attempts"] == []
    
    def test_start_game_without_auth(self, client):
        """Testar início de jogo sem autenticação."""
        response = client.post("/api/games/start")
        
        assert response.status_code == 403  # Proibido
    
    def test_get_game_success(self, client, auth_token):
        """Testar obtenção de estado do jogo."""
        # Iniciar jogo
        start_response = client.post(
            "/api/games/start",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        game_id = start_response.json()["id"]
        
        # Obter jogo
        response = client.get(
            f"/api/games/{game_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == game_id
        assert data["status"] == "started"
    
    def test_make_attempt_success(self, client, auth_token, db):
        """Testar fazer uma tentativa."""
        # Iniciar jogo
        start_response = client.post(
            "/api/games/start",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        game_id = start_response.json()["id"]
        
        # Fazer tentativa
        response = client.post(
            f"/api/games/{game_id}/attempt",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"guess": ["red", "blue", "green", "yellow"]}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"]
        assert data["attempt_number"] == 1
        assert data["guess"] == ["red", "blue", "green", "yellow"]
        assert "correct_positions" in data
        assert "correct_colors" in data
    
    def test_make_attempt_invalid_guess(self, client, auth_token):
        """Testar fazer tentativa com adivinhar inválida."""
        # Iniciar jogo
        start_response = client.post(
            "/api/games/start",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        game_id = start_response.json()["id"]
        
        # Fazer tentativa inválida (cor errada)
        response = client.post(
            f"/api/games/{game_id}/attempt",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"guess": ["red", "blue", "green", "invalid"]}
        )
        
        assert response.status_code == 400


class TestRankingEndpoints:
    """Testar endpoints de classificação."""
    
    def test_get_global_ranking_empty(self, client):
        """Testar obtenção de classificação sem jogos."""
        response = client.get("/api/rankings")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_players"] == 0
        assert data["players"] == []
    
    def test_get_global_ranking_with_games(self, client, test_user_data):
        """Testar obtenção de classificação com jogadores."""
        # Criar e registrar usuários (precisaria de dados de jogo - simplificado por enquanto)
        response = client.post("/api/auth/register", json=test_user_data)
        
        assert response.status_code == 201
        
        # Obter classificação
        ranking_response = client.get("/api/rankings")
        
        assert ranking_response.status_code == 200


class TestHealthEndpoints:
    """Testar endpoints de verificação de saúde."""
    
    def test_health_check(self, client):
        """Testar endpoint de verificação de saúde."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "saudável"
    
    def test_root_endpoint(self, client):
        """Testar endpoint raiz."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "api" in data
        assert "versao" in data
