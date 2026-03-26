import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from './services/api.service';
import { User } from './models/mastermind.models';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'Mastermind';
  currentUser: User | null = null;
  isLoading = false;
  isLoginPage = false;

  constructor(
    private apiService: ApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Inscrever nas mudanças de usuário atual
    this.apiService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });

    // Carregar usuário ao inicializar (se estiver logado)
    if (this.apiService.isAuthenticated()) {
      this.currentUser = this.apiService.getCurrentUser();
    }

    // Detectar se está na página de login
    this.router.events.subscribe(() => {
      this.isLoginPage = this.router.url.includes('/login') || this.router.url.includes('/register');
    });
  }

  /**
   * Fazer logout.
   */
  logout(): void {
    if (confirm('Deseja sair?')) {
      this.apiService.logout();
      this.router.navigate(['/login']);
    }
  }

  /**
   * Navegar para início.
   */
  goHome(): void {
    if (this.currentUser) {
      this.router.navigate(['/game']);
    } else {
      this.router.navigate(['/login']);
    }
  }

  /**
   * Navegar para classificações.
   */
  goRankings(): void {
    this.router.navigate(['/rankings']);
  }
}
