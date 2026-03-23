"""
Módulo de lógica do jogo Mastermind.
Implementa os mecanismos principais do jogo e validação.
"""

import random
from typing import List, Tuple
from app.config import get_settings


class MastermindGame:
    """
    Lógica principal do jogo Mastermind.
    
    Regras:
    - Código secreto: 4 cores de uma paleta
    - Máximo 10 tentativas para adivinhar
    - Feedback: número de acertos exatos e correspondências de cor
    
    Atributos:
        colors: Cores disponíveis para o jogo
        code_length: Comprimento do código secreto (padrão 4)
    """
    
    def __init__(self):
        """Inicializar jogo com configurações."""
        settings = get_settings()
        self.colors = settings.mastermind_colors
        self.code_length = settings.mastermind_code_length
    
    def generate_secret_code(self) -> List[str]:
        """
        Gerar um código secreto aleatório.
        
        Retorna:
            List[str]: Uma lista de 4 cores selecionadas aleatoriamente de cores disponíveis.
            
        Exemplo:
            >>> game = MastermindGame()
            >>> code = game.generate_secret_code()
            >>> len(code)
            4
            >>> all(color in game.colors for color in code)
            True
        """
        return [random.choice(self.colors) for _ in range(self.code_length)]
    
    def validate_guess(self, guess: List[str]) -> bool:
        """
        Validar se uma tentativa está no formato correto.
        
        Args:
            guess: A tentativa do jogador (lista de cores)
            
        Retorna:
            bool: True se válido, False caso contrário
            
        Levanta:
            ValueError: Se tentativa for inválida
        """
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
        Avaliar uma tentativa contra o código secreto.
        
        Esta é a lógica principal do jogo. Compara a tentativa com o código secreto
        e retorna feedback na forma de:
        - Posições corretas (peças pretas): correspondências exatas
        - Cores corretas (peças brancas): cor certa mas posição errada
        
        Algoritmo:
        1. Contar correspondências exatas (posição correta)
        2. Para posições restantes, encontrar correspondências de cor por contagem de frequência
        
        Args:
            secret_code: O código secreto (lista de 4 cores)
            guess: A tentativa do jogador (lista de 4 cores)
            
        Retorna:
            Tuple[int, int]: (posições_corretas, cores_corretas)
                - posições_corretas: Número de cores na posição certa (0-4)
                - cores_corretas: Número de cores corretas na posição errada (0-4)
                
        Exemplo:
            >>> game = MastermindGame()
            >>> secret = ["red", "blue", "green", "yellow"]
            >>> guess = ["red", "blue", "green", "white"]
            >>> positions, colors = game.evaluate_guess(secret, guess)
            >>> positions  # 3 primeiras correspondem
            3
            >>> colors  # Sem correspondências de cor em outras posições
            0
            
            >>> guess2 = ["blue", "red", "yellow", "green"]
            >>> positions2, colors2 = game.evaluate_guess(secret, guess2)
            >>> positions2  # Sem correspondências exatas
            0
            >>> colors2  # Todas as 4 cores presentes mas em posições erradas
            4
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
        Calcular pontuação do jogo baseada em tentativas e duração.
        
        Fórmula de pontuação:
        - Pontuação base: 1000 pontos
        - Dedução por tentativa: 50 pontos (máx 500 para 10 tentativas)
        - Dedução por tempo: 1 ponto por minuto (máx ~100 para ~100 minutos)
        
        Args:
            attempts: Número de tentativas usadas (1-10)
            duration_seconds: Duração do jogo em segundos
            
        Retorna:
            float: Pontuação final (0-1000)
            
        Exemplo:
            >>> game = MastermindGame()
            >>> score = game.calculate_score(attempts=1, duration_seconds=60)
            >>> score  # 1000 - 0 (perfeito) - 1 (1 minuto) = 999
            999.0
            
            >>> score = game.calculate_score(attempts=10, duration_seconds=600)
            >>> score  # 1000 - 450 (10 tentativas) - 10 (10 minutos) = 540
            540.0
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


# Casos de teste (podem ser executados com pytest)
if __name__ == "__main__":
    game = MastermindGame()
    
    # Teste 1: Tentativa perfeita
    secret = ["red", "blue", "green", "yellow"]
    guess = ["red", "blue", "green", "yellow"]
    pos, col = game.evaluate_guess(secret, guess)
    print(f"Teste 1 (Perfeita): posições={pos}, cores={col}")
    assert pos == 4 and col == 0, "Tentativa perfeita deve ter 4 posições corretas"
    
    # Teste 2: Todas as cores na posição errada
    secret = ["red", "blue", "green", "yellow"]
    guess = ["blue", "red", "yellow", "green"]
    pos, col = game.evaluate_guess(secret, guess)
    print(f"Teste 2 (Tudo errado): posições={pos}, cores={col}")
    assert pos == 0 and col == 4, "Todas as cores presentes mas em posições erradas"
    
    # Teste 3: Alguns corretos, alguns errados
    secret = ["red", "blue", "green", "yellow"]
    guess = ["red", "blue", "white", "white"]
    pos, col = game.evaluate_guess(secret, guess)
    print(f"Teste 3 (Alguns corretos): posições={pos}, cores={col}")
    assert pos == 2 and col == 0, "Duas posições corretas"
    
    # Teste 4: Manipulação de duplicatas
    secret = ["red", "red", "blue", "blue"]
    guess = ["red", "blue", "red", "yellow"]
    pos, col = game.evaluate_guess(secret, guess)
    print(f"Teste 4 (Duplicatas): posições={pos}, cores={col}")
    assert pos == 1, "Deve lidar com duplicatas corretamente"
    
    print("\nTodos os testes passaram!")