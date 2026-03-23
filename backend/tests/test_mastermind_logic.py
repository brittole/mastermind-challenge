"""
Testes unitários para a lógica do jogo Mastermind.
Testa os mecanismos principais do jogo e pontuação.
"""

import pytest
from app.utils.mastermind import MastermindGame


class TestMastermindLogic:
    """Suite de testes para lógica do jogo Mastermind."""
    
    @pytest.fixture
    def game(self):
        """Criar instância de jogo para testes."""
        return MastermindGame()
    
    def test_generate_secret_code_length(self, game):
        """Testar que código secreto tem comprimento correto."""
        code = game.generate_secret_code()
        assert len(code) == 4
    
    def test_generate_secret_code_valid_colors(self, game):
        """Testar que código secreto contém apenas cores válidas."""
        code = game.generate_secret_code()
        assert all(color in game.colors for color in code)
    
    def test_validate_guess_valid(self, game):
        """Testar validação de tentativa válida."""
        valid_guess = ["red", "blue", "green", "yellow"]
        assert game.validate_guess(valid_guess) is True
    
    def test_validate_guess_invalid_length(self, game):
        """Testar que validação rejeita comprimento errado."""
        with pytest.raises(ValueError, match="deve conter exatamente 4"):
            game.validate_guess(["red", "blue"])
    
    def test_validate_guess_invalid_color(self, game):
        """Testar que validação rejeita cor inválida."""
        with pytest.raises(ValueError, match="Cor inválida"):
            game.validate_guess(["red", "blue", "green", "invalid"])
    
    def test_validate_guess_not_list(self, game):
        """Testar que validação rejeita entrada não-lista."""
        with pytest.raises(ValueError, match="deve ser uma lista"):
            game.validate_guess("not a list")
    
    def test_perfect_guess(self, game):
        """Testar avaliação de tentativa perfeita."""
        secret = ["red", "blue", "green", "yellow"]
        guess = ["red", "blue", "green", "yellow"]
        
        positions, colors = game.evaluate_guess(secret, guess)
        
        assert positions == 4
        assert colors == 0
    
    def test_all_wrong_positions(self, game):
        """Testar quando todas as cores estão corretas mas posições erradas."""
        secret = ["red", "blue", "green", "yellow"]
        guess = ["blue", "green", "yellow", "red"]
        
        positions, colors = game.evaluate_guess(secret, guess)
        
        assert positions == 0
        assert colors == 4
    
    def test_partial_match(self, game):
        """Testar avaliação de correspondência parcial."""
        secret = ["red", "blue", "green", "yellow"]
        guess = ["red", "blue", "white", "white"]
        
        positions, colors = game.evaluate_guess(secret, guess)
        
        assert positions == 2
        assert colors == 0
    
    def test_complete_miss(self, game):
        """Testar quando nenhuma cor corresponde."""
        secret = ["red", "blue", "green", "yellow"]
        guess = ["white", "white", "white", "white"]
        
        positions, colors = game.evaluate_guess(secret, guess)
        
        assert positions == 0
        assert colors == 0
    
    def test_duplicate_colors_handling(self, game):
        """Testar manipulação correta de cores duplicadas."""
        secret = ["red", "red", "blue", "blue"]
        guess = ["red", "blue", "red", "blue"]
        
        positions, colors = game.evaluate_guess(secret, guess)
        
        # red na posição 0 correto
        # blue na posição 1 - posição errada
        # red na posição 2 - posição errada (um red já foi pareado)
        # blue na posição 3 correto
        assert positions == 2
        assert colors == 2
    
    def test_duplicate_colors_partial_match(self, game):
        """Testar cores duplicadas com pareamento parcial."""
        secret = ["red", "red", "blue", "green"]
        guess = ["red", "blue", "red", "yellow"]
        
        positions, colors = game.evaluate_guess(secret, guess)
        
        # Posição 0: red - correto
        # Posição 1: blue - correspondência de cor (1 blue restante no secreto)
        # Posição 2: red - correspondência de cor (1 red restante no secreto)
        # Posição 3: yellow - sem correspondência
        assert positions == 1
        assert colors == 2
    
    def test_score_perfect_game(self, game):
        """Testar cálculo de pontuação para jogo perfeito."""
        # 1 tentativa, 60 segundos (1 minuto)
        score = game.calculate_score(attempts=1, duration_seconds=60)
        
        # 1000 - 0 (tentativas) - 1 (tempo) = 999
        assert score == 999.0
    
    def test_score_quick_game(self, game):
        """Testar pontuação para jogo rápido."""
        # 2 tentativas, 30 segundos (2 primeiras são livres)
        score = game.calculate_score(attempts=2, duration_seconds=30)
        
        # 1000 - 0 (2 tentativas livres) - 0.5 (0.5 minuto) = 999.5
        assert score == 999.5
    
    def test_score_slow_game(self, game):
        """Testar pontuação para jogo lento."""
        # 5 tentativas, 600 segundos (10 minutos)
        score = game.calculate_score(attempts=5, duration_seconds=600)
        
        # 1000 - 150 (3 tentativas acima do livre) - 10 (tempo) = 840
        assert score == 840.0
    
    def test_score_failed_game(self, game):
        """Testar pontuação para jogo perdido (10 tentativas)."""
        # 10 tentativas, 1200 segundos (20 minutos)
        score = game.calculate_score(attempts=10, duration_seconds=1200)
        
        # 1000 - 400 (8 tentativas acima do livre) - 20 (tempo) = 580
        assert score == 580.0
    
    def test_score_minimum_not_negative(self, game):
        """Testar que pontuação nunca fica abaixo de 0."""
        # Jogo muito longo
        score = game.calculate_score(attempts=10, duration_seconds=10000)
        
        assert score >= 0


class TestMastermindEdgeCases:
    """Teste casos extremos e cenários complexos."""
    
    @pytest.fixture
    def game(self):
        """Criar instância de jogo para testes."""
        return MastermindGame()
    
    def test_all_same_color(self, game):
        """Testar quando secreto tem todas as cores iguais."""
        secret = ["red", "red", "red", "red"]
        guess = ["red", "red", "red", "red"]
        
        positions, colors = game.evaluate_guess(secret, guess)
        
        assert positions == 4
        assert colors == 0
    
    def test_all_same_color_partial(self, game):
        """Testar quando secreto tem todas as cores iguais e tentativa tem algumas."""
        secret = ["red", "red", "red", "red"]
        guess = ["red", "red", "blue", "blue"]
        
        positions, colors = game.evaluate_guess(secret, guess)
        
        assert positions == 2
        assert colors == 0
    
    def test_complex_scenario(self, game):
        """Testar cenário complexo com múltiplas correspondências."""
        secret = ["red", "blue", "red", "green"]
        guess = ["red", "green", "blue", "red"]
        
        positions, colors = game.evaluate_guess(secret, guess)
        
        # Posição 0: red - correto
        # Posição 1: green - correspondência de cor
        # Posição 2: blue - correspondência de cor
        # Posição 3: red - correspondência de cor (um red restante)
        assert positions == 1
        assert colors == 3
