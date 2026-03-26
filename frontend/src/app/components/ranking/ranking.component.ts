import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { PlayerRankingEntry, RankingResponse } from '../../models/mastermind.models';

@Component({
  selector: 'app-ranking',
  templateUrl: './ranking.component.html',
  styleUrls: ['./ranking.component.css']
})
export class RankingComponent implements OnInit {
  /* Dados de ranking */
  dados: RankingResponse | null = null;
  jogadores: PlayerRankingEntry[] = [];

  /* Estados */
  carregando: boolean = true;
  erro: string = '';
  periodo: 'global' | 'mes' | 'semana' = 'global';

  /* Para usar Math no template */
  Math = Math;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.carregarRanking();
  }

  /**
   * Carrega o ranking do servidor
   */
  carregarRanking(): void {
    this.carregando = true;
    this.erro = '';

    this.apiService.getGlobalRanking(100).subscribe({
      next: (dados) => {
        this.dados = dados;
        this.jogadores = dados.players || [];
        this.carregando = false;
      },
      error: () => {
        this.carregando = false;
        this.erro = 'Erro ao carregar o ranking. Tente novamente.';
      }
    });
  }

  /**
   * Retornaaa a posição visual do jogador
   */
  obterPosicao(indice: number): number {
    return indice + 1;
  }

  /**
   * Retorna o emoji da medalha por posição
   */
  obterMedalha(posicao: number): string {
    switch (posicao) {
      case 1:
        return '🥇';
      case 2:
        return '🥈';
      case 3:
        return '🥉';
      default:
        return '';
    }
  }

  /**
   * Formata um número para exibição
   */
  formatarNumero(numero: number | undefined | null): string {
    if (numero === undefined || numero === null) {
      return '0';
    }
    return numero.toLocaleString('pt-BR');
  }

  /**
   * Retorna a classe CSS para a linha, destacando o usuário
   */
  obterClasseLinha(_jogador: PlayerRankingEntry, indice: number): string {
    let classes = 'linha-ranking';

    if (indice < 3) {
      classes += ' top-3';
    }

    return classes;
  }
}
