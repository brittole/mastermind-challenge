/**
 * Componente raiz da aplicação Mastermind.
 */

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
  title = 'Mastermind - Quebra-Código';
  currentUser: User | null = null;
  isLoading = false;

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
