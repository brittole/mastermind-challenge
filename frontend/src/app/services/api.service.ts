/**
 * Serviço HTTP para comunicação com a API do Mastermind.
 * Responsável por todas as requisições REST para o backend.
 */

import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';
import {
  User,
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  Game,
  GameResultResponse,
  Attempt,
  RankingResponse,
  AttemptCreate
} from '../models/mastermind.models';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8080/api';
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadCurrentUser();
  }

  /**
   * Obter token armazenado localmente.
   */
  getToken(): string | null {
    return localStorage.getItem('authToken');
  }

  /**
   * Registrar novo usuário.
   */
  register(data: RegisterRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/auth/register`, data).pipe(
      tap(response => {
        localStorage.setItem('authToken', response.access_token);
        this.currentUserSubject.next(response.user);
      })
    );
  }

  /**
   * Fazer login.
   */
  login(data: LoginRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/auth/login`, data).pipe(
      tap(response => {
        localStorage.setItem('authToken', response.access_token);
        this.currentUserSubject.next(response.user);
      })
    );
  }

  /**
   * Fazer logout.
   */
  logout(): void {
    localStorage.removeItem('authToken');
    this.currentUserSubject.next(null);
  }

  /**
   * Carregar usuário atual do localStorage.
   */
  private loadCurrentUser(): void {
    const token = this.getToken();
    if (token) {
      // Em produção, você deveria validar o token no backend
      const userStr = localStorage.getItem('currentUser');
      if (userStr) {
        this.currentUserSubject.next(JSON.parse(userStr));
      }
    }
  }

  /**
   * Iniciar novo jogo.
   */
  startGame(): Observable<Game> {
    return this.http.post<Game>(`${this.apiUrl}/games/start`, {}, this.getHttpOptions());
  }

  /**
   * Obter jogo ativo do usuário.
   */
  getActiveGame(): Observable<Game> {
    return this.http.get<Game>(`${this.apiUrl}/games/active`, this.getHttpOptions());
  }

  /**
   * Obter estado atual do jogo.
   */
  getGame(gameId: string): Observable<Game> {
    return this.http.get<Game>(`${this.apiUrl}/games/${gameId}`, this.getHttpOptions());
  }

  /**
   * Fazer uma tentativa no jogo.
   */
  makeAttempt(gameId: string, guess: string[]): Observable<Attempt> {
    const data: AttemptCreate = { guess };
    return this.http.post<Attempt>(
      `${this.apiUrl}/games/${gameId}/attempt`,
      data,
      this.getHttpOptions()
    );
  }

  /**
   * Obter resultado completo do jogo (com código secreto).
   */
  getGameResult(gameId: string): Observable<GameResultResponse> {
    return this.http.get<GameResultResponse>(
      `${this.apiUrl}/games/${gameId}/result`,
      this.getHttpOptions()
    );
  }

  /**
   * Abandonar um jogo.
   */
  abandonGame(gameId: string): Observable<Game> {
    return this.http.post<Game>(
      `${this.apiUrl}/games/${gameId}/abandon`,
      {},
      this.getHttpOptions()
    );
  }

  /**
   * Obter todos os jogos do usuário.
   */
  getUserGames(): Observable<Game[]> {
    return this.http.get<Game[]>(`${this.apiUrl}/games`, this.getHttpOptions());
  }

  /**
   * Obter classificação global.
   */
  getGlobalRanking(limit: number = 100): Observable<RankingResponse> {
    return this.http.get<RankingResponse>(`${this.apiUrl}/rankings?limit=${limit}`);
  }

  /**
   * Obter estatísticas de um usuário.
   */
  getUserStats(userId: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/rankings/user/${userId}`);
  }

  /**
   * Obter opções HTTP com token de autorização.
   */
  private getHttpOptions() {
    const token = this.getToken();
    if (!token) {
      return {};
    }
    return {
      headers: new HttpHeaders({
        Authorization: `Bearer ${token}`
      })
    };
  }

  /**
   * Verificar se o usuário está autenticado.
   */
  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }

  /**
   * Obter usuário atual.
   */
  getCurrentUser(): User | null {
    return this.currentUserSubject.value;
  }
}
