"""
Testes de autenticação.
"""

import pytest
from app.schemas.schemas import UserCreate
from app.services.services import AuthService


class TestAuthService:
    """Testes para o serviço de autenticação."""
    
    def test_hash_password(self):
        """Testar hash de senha."""
        password = "mysecurepassword"
        hashed = AuthService.hash_password(password)
        
        # Senha com hash deve ser diferente da original
        assert hashed != password
        
        # Hash deve ter tamanho razoável
        assert len(hashed) > 20
    
    def test_verify_password_correct(self):
        """Testar verificação de senha com senha correta."""
        password = "mysecurepassword"
        hashed = AuthService.hash_password(password)
        
        # Verificação deve ser bem-sucedida
        assert AuthService.verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Testar verificação de senha com senha incorreta."""
        password = "mysecurepassword"
        hashed = AuthService.hash_password(password)
        
        # Verificação com senha errada deve falhar
        assert AuthService.verify_password("wrongpassword", hashed) is False
    
    def test_create_user_success(self, db, test_user_data):
        """Testar criação bem-sucedida de usuário."""
        user_data = UserCreate(**test_user_data)
        
        user = AuthService.create_user(db, user_data)
        
        assert user is not None
        assert user.email == test_user_data["email"]
        assert user.username == test_user_data["username"]
        assert user.password_hash != test_user_data["password"]
        assert user.id is not None
    
    def test_create_user_duplicate_email(self, db, test_user_data):
        """Testar que email duplicado lança erro."""
        user_data = UserCreate(**test_user_data)
        
        # Criar primeiro usuário
        AuthService.create_user(db, user_data)
        
        # Tentar criar outro com mesmo email
        with pytest.raises(ValueError, match="já existe"):
            AuthService.create_user(db, user_data)
    
    def test_create_user_duplicate_username(self, db, test_user_data):
        """Testar que username duplicado lança erro."""
        user_data1 = UserCreate(**test_user_data)
        user_data2 = UserCreate(
            email="different@example.com",
            username=test_user_data["username"],
            password=test_user_data["password"]
        )
        
        # Criar primeiro usuário
        AuthService.create_user(db, user_data1)
        
        # Tentar criar outro com mesmo username
        with pytest.raises(ValueError, match="já existe"):
            AuthService.create_user(db, user_data2)
    
    def test_authenticate_user_success(self, db, test_user_data):
        """Testar autenticação bem-sucedida."""
        user_data = UserCreate(**test_user_data)
        AuthService.create_user(db, user_data)
        
        # Autenticar com username
        user = AuthService.authenticate_user(
            db,
            test_user_data["username"],
            test_user_data["password"]
        )
        
        assert user is not None
        assert user.username == test_user_data["username"]
    
    def test_authenticate_user_with_email(self, db, test_user_data):
        """Testar autenticação com email em vez de username."""
        user_data = UserCreate(**test_user_data)
        AuthService.create_user(db, user_data)
        
        # Autenticar com email
        user = AuthService.authenticate_user(
            db,
            test_user_data["email"],
            test_user_data["password"]
        )
        
        assert user is not None
        assert user.email == test_user_data["email"]
    
    def test_authenticate_user_wrong_password(self, db, test_user_data):
        """Testar autenticação com senha errada."""
        user_data = UserCreate(**test_user_data)
        AuthService.create_user(db, user_data)
        
        # Tentar autenticar com senha errada
        user = AuthService.authenticate_user(
            db,
            test_user_data["username"],
            "wrongpassword"
        )
        
        assert user is None
    
    def test_authenticate_user_nonexistent(self, db):
        """Testar autenticação de usuário não existente."""
        user = AuthService.authenticate_user(
            db,
            "nonexistent",
            "password"
        )
        
        assert user is None
