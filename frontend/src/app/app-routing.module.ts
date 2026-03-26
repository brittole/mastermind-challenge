import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { GameComponent } from './components/game/game.component';
import { RankingComponent } from './components/ranking/ranking.component';
import { AuthGuard } from './guards/auth.guard';

const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'jogo',
    component: GameComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'rankings',
    component: RankingComponent,
    canActivate: [AuthGuard]
  },
  {
    path: '',
    redirectTo: '/jogo',
    pathMatch: 'full'
  },
  {
    path: '**',
    redirectTo: '/jogo'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    enableTracing: false /* Mude para true para debug de rotas */
  })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
