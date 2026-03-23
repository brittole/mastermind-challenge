import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { RegisterRequest, LoginRequest } from '../../models/mastermind.models';

/**
 * Componente de Autenticação
 * 
 * Responsável por:
 * - Registro de novos jogadores
 * - Login de usuários existentes
 * - Validação de entrada
 * - Gerenciamento de erros
 */
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  /* Modo de exibição: 'login' ou 'register' */
  modo: 'login' | 'register' = 'login';

  /* Dados do formulário */
  email: string = '';
  senha: string = '';
  confirmarSenha: string = '';
  nome: string = '';

  /* Estados da aplicação */
  carregando: boolean = false;
  erro: string = '';
  sucesso: string = '';

  constructor(
    private apiService: ApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    /* Se já está autenticado, redireciona para o jogo */
    this.apiService.currentUser$.subscribe(usuario => {
      if (usuario) {
        this.router.navigate(['/jogo']);
      }
    });
  }

  /**
   * Alterna entre os modos de login e registro
   */
  alternarModo(): void {
    this.modo = this.modo === 'login' ? 'register' : 'login';
    this.limparFormulario();
  }

  /**
   * Realiza o login do usuário
   */
  fazerLogin(): void {
    this.erro = '';
    this.sucesso = '';

    if (!this.validarFormularioLogin()) {
      return;
    }

    this.carregando = true;

    const credenciais: LoginRequest = {
      email: this.email,
      password: this.senha
    };

    this.apiService.login(credenciais).subscribe({
      next: (resposta) => {
        this.carregando = false;
        this.sucesso = 'Login realizado com sucesso!';
        localStorage.setItem('token', resposta.access_token);
        localStorage.setItem('usuario', JSON.stringify(resposta.user));
        
        setTimeout(() => {
          this.router.navigate(['/jogo']);
        }, 1000);
      },
      error: (err) => {
        this.carregando = false;
        
        if (err.status === 401) {
          this.erro = 'Email ou senha incorretos';
        } else if (err.status === 400) {
          this.erro = err.error.detail || 'Dados inválidos';
        } else {
          this.erro = 'Erro ao tentar fazer login. Tente novamente.';
        }
      }
    });
  }

  /**
   * Registra um novo usuário
   */
  fazerRegistro(): void {
    this.erro = '';
    this.sucesso = '';

    if (!this.validarFormularioRegistro()) {
      return;
    }

    this.carregando = true;

    const novoUsuario: RegisterRequest = {
      email: this.email,
      password: this.senha,
      username: this.nome
    };

    this.apiService.register(novoUsuario).subscribe({
      next: () => {
        this.carregando = false;
        this.sucesso = 'Conta criada com sucesso! Faça login para continuar.';
        
        setTimeout(() => {
          this.modo = 'login';
          this.limparFormulario();
        }, 2000);
      },
      error: (err) => {
        this.carregando = false;
        
        if (err.status === 409) {
          this.erro = 'Este email já está registrado';
        } else if (err.status === 400) {
          this.erro = err.error.detail || 'Dados inválidos';
        } else {
          this.erro = 'Erro ao registrar. Tente novamente.';
        }
      }
    });
  }

  /**
   * Valida o formulário de login
   */
  private validarFormularioLogin(): boolean {
    if (!this.email.trim()) {
      this.erro = 'Por favor, insira seu email';
      return false;
    }

    if (!this.email.includes('@')) {
      this.erro = 'Email inválido';
      return false;
    }

    if (!this.senha) {
      this.erro = 'Por favor, insira sua senha';
      return false;
    }

    if (this.senha.length < 6) {
      this.erro = 'A senha deve ter no mínimo 6 caracteres';
      return false;
    }

    return true;
  }

  /**
   * Valida o formulário de registro
   */
  private validarFormularioRegistro(): boolean {
    if (!this.nome.trim()) {
      this.erro = 'Por favor, insira seu nome';
      return false;
    }

    if (this.nome.length < 3) {
      this.erro = 'Seu nome deve ter no mínimo 3 caracteres';
      return false;
    }

    if (!this.email.trim()) {
      this.erro = 'Por favor, insira seu email';
      return false;
    }

    if (!this.email.includes('@')) {
      this.erro = 'Email inválido';
      return false;
    }

    if (!this.senha) {
      this.erro = 'Por favor, insira uma senha';
      return false;
    }

    if (this.senha.length < 6) {
      this.erro = 'A senha deve ter no mínimo 6 caracteres';
      return false;
    }

    if (this.senha !== this.confirmarSenha) {
      this.erro = 'As senhas não conferem';
      return false;
    }

    return true;
  }

  /**
   * Limpa o formulário
   */
  private limparFormulario(): void {
    this.email = '';
    this.senha = '';
    this.confirmarSenha = '';
    this.nome = '';
  }
}
