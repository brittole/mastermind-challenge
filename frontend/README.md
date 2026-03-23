# 🎮 Mastermind - Frontend Angular

Frontend em Angular 17 para o jogo Mastermind, uma aplicação de dedução lógica onde o jogador tenta adivinhar uma sequência de cores em até 10 tentativas.

## 🚀 Funcionalidades

- ✅ **Autenticação**: Registro e login de usuários
- ✅ **Jogo Interativo**: Tabuleiro de jogo com seleção de cores
- ✅ **Ranking Global**: Visualização de jogadores e estatísticas
- ✅ **Interface Responsiva**: Funciona em desktop, tablet e móvel
- ✅ **Tema Moderno**: Design com gradiente e animações suaves
- ✅ **Português**: Interface completamente em português

## 🛠️ Requisitos

- **Node.js**: v18.0.0 ou superior
- **npm**: v9.0.0 ou superior
- **Angular CLI**: v17.0.0 ou superior

## 📦 Instalação

### 1. Instalar dependências

```bash
npm install
```

### 2. Configurar variáveis de ambiente

Edite `src/environments/environment.ts` para seu ambiente de desenvolvimento:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

## 🏃 Executar Localmente

### Modo de Desenvolvimento

```bash
ng serve
# ou
npm start
```

Acesse a aplicação em `http://localhost:4200`

### Modo de Produção

```bash
ng serve --configuration production
```

## 🏗️ Build

### Build para Produção

```bash
ng build --configuration production
```

Os arquivos compilados estarão em `dist/mastermind-frontend/`

## 📁 Estrutura do Projeto

```
src/
├── app/
│   ├── components/
│   │   ├── login/              # Componente de autenticação
│   │   ├── game/               # Componente do jogo
│   │   └── ranking/            # Componente de ranking
│   ├── services/
│   │   └── api.service.ts      # Cliente HTTP para backend
│   ├── guards/
│   │   └── auth.guard.ts       # Protetor de rotas
│   ├── models/
│   │   └── mastermind.models.ts # Interfaces TypeScript
│   ├── app.component.*         # Componente raiz
│   ├── app.module.ts           # Módulo principal
│   └── app-routing.module.ts   # Configuração de rotas
├── environments/
│   ├── environment.ts          # Config desenvolvimento
│   └── environment.prod.ts     # Config produção
├── assets/                     # Arquivos estáticos
├── styles.css                  # Estilos globais
├── main.ts                     # Bootstrap
└── index.html                  # HTML raiz
```

## 🎯 Componentes

### LoginComponent
- Formulário de registro
- Formulário de login
- Validações de entrada
- Gerenciamento de erros

### GameComponent
- Tabuleiro de jogo (10 tentativas × 4 posições)
- Seletor de cores (6 cores disponíveis)
- Feedback de acertos e semi-acertos
- Sistema de pontuação

### RankingComponent
- Tabela com top 100 jogadores
- Estatísticas globais
- Taxa de vitória por jogador
- Pontuação média

## 🔐 Autenticação

A autenticação é gerenciada pelo `ApiService` que:
- Armazena o token JWT em `localStorage`
- Usa `BehaviorSubject` para estado reativo
- Protege rotas com `AuthGuard`
- Redireciona para login se não autenticado

## 🎨 Temas e Cores

```css
--primary-color: #667eea
--secondary-color: #764ba2
--success-color: #22C55E
--danger-color: #EF4444
--dark-color: #1F2937
--light-color: #F9FAFB
```

## 📱 Responsividade

A aplicação adapta-se automaticamente para:
- **Desktop**: Layout completo com 2 painéis
- **Tablet**: Layout ajustado (768px)
- **Mobile**: Layout em coluna única (480px)

## 🧪 Testes (Futuro)

```bash
ng test              # Testes unitários
ng e2e              # Testes e2e
```

## 🚀 Deployment

### Render.com (Recomendado)

1. Conecte seu repositório GitHub
2. Configure as build settings:
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
3. Defina a variável de ambiente `API_URL`

### Vercel

1. Importe o projeto do GitHub
2. Configure `apiUrl` em `environment.prod.ts`
3. Deploy automático

### Docker

```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist/mastermind-frontend /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 🔗 Integração com Backend

O frontend se conecta ao backend FastAPI através da `ApiService`:

- Base URL: Configurável em `environment.ts`
- Autenticação: JWT via headers
- CORS: Deve estar configurado no backend

Endpoints principais:
- `POST /auth/register` - Registro
- `POST /auth/login` - Login
- `POST /games/start` - Iniciar jogo
- `POST /games/{id}/attempts` - Fazer palpite
- `GET /rankings` - Ranking global
- `GET /users/{id}/stats` - Estatísticas do usuário

## 🐛 Troubleshooting

### Erro de conexão com backend
- Verifique se o backend está rodando
- Confirme a URL em `environment.ts`
- Verifique CORS no backend

### Token expirado
- O token é armazenado em localStorage
- Login novamente quando necessário
- Implemente refresh tokens no backend

### Build falha
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
ng build
```

## 📚 Documentação

- [Angular Docs](https://angular.io)
- [TypeScript Docs](https://www.typescriptlang.org)
- [RxJS Docs](https://rxjs.dev)

## 👤 Autor

Desenvolvido com ❤️ para o desafio Mastermind

## 📄 Licença

Este projeto está sob licença MIT.
