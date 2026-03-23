import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { Game, Attempt, COLOR_MAP, COLORS } from '../../models/mastermind.models';

/**
 * Componente do Tabuleiro de Jogo
 * 
 * Responsável por:
 * - Iniciar novo jogo
 * - Exibir histórico de tentativas
 * - Permitir seleção de cores para palpites
 * - Mostrar feedback das tentativas
 * - Gerenciar estado do jogo
 */
@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit {
  /* Jogo atual */
  jogoAtual: Game | null = null;
  tentativas: Attempt[] = [];

  /* Jogo ativo anterior (em conflito) */
  jogoAnterior: Game | null = null;

  /* Seleção de cores */
  cores = COLORS;
  coreSelecionadas: string[] = [];
  corMapaUI = COLOR_MAP;

  /* Estados da aplicação */
  carregando: boolean = false;
  erro: string = '';
  mensagem: string = '';
  jogoTerminado: boolean = false;
  jogadorVenceu: boolean = false;
  mostrando_conflito: boolean = false;

  /* Constantes do jogo */
  TAMANHO_SEQUENCIA = 4;
  NUM_TENTATIVAS_MAX = 10;

  constructor(
    private apiService: ApiService,
    public router: Router
  ) {}

  ngOnInit(): void {
    this.iniciarNovoJogo();
  }

  /**
   * Inicia um novo jogo
   */
  iniciarNovoJogo(): void {
    this.carregando = true;
    this.erro = '';
    this.mensagem = '';
    this.coreSelecionadas = [];
    this.tentativas = [];
    this.jogoTerminado = false;
    this.jogadorVenceu = false;
    this.mostrando_conflito = false;

    this.apiService.startGame().subscribe({
      next: (jogo) => {
        this.jogoAtual = jogo;
        this.jogoAnterior = null;
        this.carregando = false;
        this.mensagem = 'Novo jogo iniciado! Adivinhe a sequência em até 10 tentativas.';
      },
      error: (error) => {
        this.carregando = false;
        // Verificar se é erro de jogo ativo
        if (error.status === 400 && error.error?.detail?.includes('jogo ativo')) {
          this.mostrando_conflito = true;
          this.buscarJogoAtivo();
        } else {
          this.erro = 'Erro ao iniciar o jogo. Tente novamente.';
        }
      }
    });
  }

  /**
   * Busca e exibe o jogo ativo anterior
   */
  private buscarJogoAtivo(): void {
    this.carregando = true;
    this.apiService.getActiveGame().subscribe({
      next: (jogo) => {
        this.jogoAnterior = jogo;
        this.carregando = false;
        this.erro = '';
      },
      error: () => {
        this.carregando = false;
        this.erro = 'Erro ao recuperar jogo ativo. Tente novamente.';
      }
    });
  }

  /**
   * Abandona o jogo anterior e inicia um novo
   */
  abandonarAnterioreIniciarNovo(): void {
    if (!this.jogoAnterior) {
      return;
    }

    this.carregando = true;
    this.apiService.abandonGame(this.jogoAnterior.id).subscribe({
      next: () => {
        this.jogoAnterior = null;
        this.mostrando_conflito = false;
        this.iniciarNovoJogo();
      },
      error: () => {
        this.carregando = false;
        this.erro = 'Erro ao abandonar o jogo anterior.';
      }
    });
  }

  /**
   * Continua jogando o jogo anterior
   */
  continuarJogoAnterior(): void {
    if (!this.jogoAnterior) {
      return;
    }

    this.jogoAtual = this.jogoAnterior;
    this.jogoAnterior = null;
    this.mostrando_conflito = false;
    this.carregando = true;
    this.erro = '';
    this.mensagem = '';

    // Carregar tentativas do jogo
    this.apiService.getGame(this.jogoAtual.id).subscribe({
      next: (jogo) => {
        this.jogoAtual = jogo;
        this.tentativas = jogo.attempts || [];
        this.carregando = false;
        this.mensagem = `Continuando seu jogo anterior (${this.tentativas.length}/${this.NUM_TENTATIVAS_MAX} tentativas).`;
      },
      error: () => {
        this.carregando = false;
        this.erro = 'Erro ao carregar jogo anterior.';
      }
    });
  }

  /**
   * Adiciona uma cor à seleção atual
   */
  adicionarCor(cor: string): void {
    if (this.jogoTerminado) {
      return;
    }

    if (this.coreSelecionadas.length < this.TAMANHO_SEQUENCIA) {
      this.coreSelecionadas.push(cor);
    }
  }

  /**
   * Remove a última cor da seleção
   */
  removerUltimaCor(): void {
    if (this.coreSelecionadas.length > 0) {
      this.coreSelecionadas.pop();
    }
  }

  /**
   * Limpa a seleção de cores
   */
  limparSelecao(): void {
    this.coreSelecionadas = [];
  }

  /**
   * Faz um palpite com as cores selecionadas
   */
  fazerPalpite(): void {
    if (!this.jogoAtual) {
      this.erro = 'Nenhum jogo ativo.';
      return;
    }

    if (this.coreSelecionadas.length !== this.TAMANHO_SEQUENCIA) {
      this.erro = `Selecione ${this.TAMANHO_SEQUENCIA} cores para fazer um palpite.`;
      return;
    }

    this.carregando = true;
    this.erro = '';

    this.apiService.makeAttempt(this.jogoAtual.id, this.coreSelecionadas).subscribe({
      next: (tentativa) => {
        this.carregando = false;
        this.tentativas.unshift(tentativa);
        this.coreSelecionadas = [];

        /* Verifica se acertou */
        if (tentativa.correct_positions === this.TAMANHO_SEQUENCIA) {
          this.jogoTerminado = true;
          this.jogadorVenceu = true;
          this.mensagem = `🎉 Parabéns! Você acertou em ${this.tentativas.length} ${this.tentativas.length === 1 ? 'tentativa' : 'tentativas'}!`;
        } else if (this.tentativas.length >= this.NUM_TENTATIVAS_MAX) {
          this.jogoTerminado = true;
          this.jogadorVenceu = false;
          this.obterRespostaCorreta();
        } else {
          this.mensagem = `Tentativa ${this.tentativas.length}: ${tentativa.correct_positions} acertos e ${tentativa.correct_colors} posições corretas.`;
        }
      },
      error: () => {
        this.carregando = false;
        this.erro = 'Erro ao fazer o palpite. Tente novamente.';
      }
    });
  }

  /**
   * Obtém a resposta correta ao perder
   */
  private obterRespostaCorreta(): void {
    if (!this.jogoAtual) {
      return;
    }

    this.apiService.getGameResult(this.jogoAtual.id).subscribe({
      next: (resultado) => {
        this.mensagem = `Que pena! A sequência correta era: ${resultado.secret_code?.join(', ')}`;
      },
      error: () => {
        this.mensagem = 'Fim de jogo. Você não conseguiu adivinhar a sequência.';
      }
    });
  }

  /**
   * Abandona o jogo atual
   */
  abandonarJogo(): void {
    if (!this.jogoAtual) {
      return;
    }

    if (confirm('Tem certeza que deseja abandonar este jogo?')) {
      this.carregando = true;

      this.apiService.abandonGame(this.jogoAtual.id).subscribe({
        next: () => {
          this.carregando = false;
          this.router.navigate(['/rankings']);
        },
        error: () => {
          this.carregando = false;
          this.erro = 'Erro ao abandonar o jogo.';
        }
      });
    }
  }

  /**
   * Obtém o nome exibível da cor
   */
  obterNomeCor(cor: string): string {
    const mapa: { [key: string]: string } = {
      'vermelho': 'Vermelho',
      'azul': 'Azul',
      'verde': 'Verde',
      'amarelo': 'Amarelo',
      'roxo': 'Roxo',
      'laranja': 'Laranja'
    };
    return mapa[cor] || cor;
  }

  /**
   * Retorna a cor CSS para exibição
   */
  obterCorCSS(cor: string): string {
    return this.corMapaUI[cor as keyof typeof COLOR_MAP] || '#DDD';
  }
}
