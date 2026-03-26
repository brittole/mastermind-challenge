"""
Lógica do jogo Mastermind.
"""

import random
from typing import List, Tuple
from app.config import get_settings


class MastermindGame:
    """
    Lógica principal do jogo Mastermind.
    Código secreto de 4 cores, máximo 10 tentativas.
    """
    
    def __init__(self):
        """Inicializar jogo com configurações."""
        settings = get_settings()
        self.colors = settings.mastermind_colors
        self.code_length = settings.mastermind_code_length
    
    def generate_secret_code(self) -> List[str]:
        """Gerar código secreto aleatório com 4 cores."""
        return [random.choice(self.colors) for _ in range(self.code_length)]
    
    def validate_guess(self, guess: List[str]) -> bool:
        """Validar formato da tentativa. Levanta ValueError se inválida."""
        if not isinstance(guess, list):
            raise ValueError("A tentativa deve ser uma lista de cores")
        
        if len(guess) != self.code_length:
            raise ValueError(f"A tentativa deve conter exatamente {self.code_length} cores")
        
        for color in guess:
            if color not in self.colors:
                raise ValueError(f"Cor inválida: {color}. Deve ser uma de {self.colors}")
        
        return True
    
    def evaluate_guess(self, secret_code: List[str], guess: List[str]) -> Tuple[int, int]:
        """
        Avaliar tentativa contra o código secreto.
        Retorna (posições_corretas, cores_corretas).
        
        Posições corretas = cor certa no lugar certo
        Cores corretas = cor certa no lugar errado
        """
        # Validar formato da tentativa
        self.validate_guess(guess)
        
        # Etapa 1: Contar correspondências exatas (posição correta)
        correct_positions = sum(
            1 for secret_color, guess_color in zip(secret_code, guess)
            if secret_color == guess_color
        )
        
        # Etapa 2: Contar correspondências de cor para elementos restantes (não-exatos)
        # Precisamos usar contagem de frequência para lidar corretamente com duplicatas
        secret_remaining = []
        guess_remaining = []
        
        for i in range(len(secret_code)):
            if secret_code[i] != guess[i]:
                secret_remaining.append(secret_code[i])
                guess_remaining.append(guess[i])
        
        # Contar frequência de cada cor nos elementos restantes
        correct_colors = 0
        secret_freq = {}
        
        # Contar cores do secreto
        for color in secret_remaining:
            secret_freq[color] = secret_freq.get(color, 0) + 1
        
        # Contar correspondências na tentativa
        for guess_color in guess_remaining:
            if guess_color in secret_freq and secret_freq[guess_color] > 0:
                correct_colors += 1
                secret_freq[guess_color] -= 1
        
        return correct_positions, correct_colors
    
    def calculate_score(self, attempts: int, duration_seconds: float) -> float:
        """
        Calcular pontuação baseada em tentativas e duração.
        Base de 1000 pontos, deduzindo por tentativas e tempo.
        """
        if attempts < 1 or attempts > 10:
            raise ValueError("Tentativas devem estar entre 1 e 10")
        
        # Pontuação base
        base_score = 1000.0
        
        # Deduzir por tentativas (50 pontos por tentativa, mas as 2 primeiras são livres)
        attempts_deduction = max(0, (attempts - 2) * 50)
        
        # Deduzir por tempo (1 ponto por minuto)
        time_deduction = duration_seconds / 60
        
        # Calcular pontuação final
        score = base_score - attempts_deduction - time_deduction
        
        # Garantir que pontuação não seja negativa
        return max(0.0, score)