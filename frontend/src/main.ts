import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

/**
 * Bootstrap da Aplicação Angular
 * 
 * Ponto de entrada da aplicação que carrega o módulo principal
 */
platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.error(err));
