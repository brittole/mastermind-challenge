import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { GameComponent } from './components/game/game.component';
import { RankingComponent } from './components/ranking/ranking.component';

/**
 * Módulo Principal da Aplicação
 * 
 * Declara e configura:
 * - Componentes
 * - Módulos necessários (HttpClient, Forms, etc)
 * - Serviços
 * - Rotas
 */
@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    GameComponent,
    RankingComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    CommonModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
