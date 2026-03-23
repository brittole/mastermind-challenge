/**
 * Modelos de dados para a aplicação Mastermind.
 */

export interface User {
  id: string;
  email: string;
  username: string;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Attempt {
  id: string;
  attempt_number: number;
  guess: string[];
  correct_positions: number;
  correct_colors: number;
  created_at: string;
}

export interface Game {
  id: string;
  status: 'started' | 'won' | 'lost';
  started_at: string;
  ended_at?: string;
  attempts_count: number;
  final_score?: number;
  attempts: Attempt[];
}

export interface GameResultResponse extends Game {
  secret_code?: string[];
}

export interface PlayerRankingEntry {
  rank: number;
  username: string;
  email: string;
  total_games: number;
  games_won: number;
  win_rate: number;
  best_score: number;
  average_score: number;
}

export interface RankingResponse {
  total_players: number;
  total_games_played: number;
  total_victories: number;
  average_win_rate: number;
  players: PlayerRankingEntry[];
}

export interface AttemptCreate {
  guess: string[];
}

export const COLORS = [
  'red',
  'blue',
  'green',
  'yellow',
  'white',
  'black'
];

export const COLOR_MAP: { [key: string]: string } = {
  'red': '#EF4444',
  'blue': '#3B82F6',
  'green': '#22C55E',
  'yellow': '#FBBF24',
  'white': '#FFFFFF',
  'black': '#000000'
};
