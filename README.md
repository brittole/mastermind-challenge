# Mastermind Challenge

Um jogo completo de **Mastermind** (quebra-cabeca de cores) com tema alienigena/sci-fi. Tente descobrir a sequencia de 4 cores em ate 10 tentativas e suba no ranking global.

## Descricao

**Mastermind Challenge** e uma aplicacao **Full Stack** que implementa o classico jogo de logica Mastermind com:

- Interface visual tematica com cores verde alien, efeitos sci-fi e fontes futuristas
- Autenticacao segura com JWT
- Sistema de ranking global com estatisticas em tempo real
- Logica de jogo robusta com 10 tentativas por partida
- Testes completos com cobertura de 95%+
- Containerizacao com Docker + Docker Compose
- Arquitetura em camadas (Clean Architecture)

---

## Pre-requisitos

Antes de comecar, instale as ferramentas necessarias:

| Software | Versao | Download |
|----------|--------|----------|
| **Node.js** | 18+ | https://nodejs.org |
| **Python** | 3.11+ | https://www.python.org |
| **PostgreSQL** | 13+ | https://www.postgresql.org |
| **Git** | Qualquer versao recente | https://git-scm.com |

### Verifique a instalacao

Abra um terminal e rode:

```bash
node --version        # v18.0.0 ou superior
npm --version         # 9.0.0 ou superior
python --version      # Python 3.11+
psql --version        # PostgreSQL 13+
git --version         # git version 2.x+
```

---

## Stack Tecnologico

### Frontend - Angular 17
- **TypeScript** para codigo tipado
- **CSS3** com tema customizado (verde alien #00ff00)
- **Fontes**: Orbitron (titulos), Michroma (subtitulos)
- **Componentes**: Login, Game, Ranking

### Backend - FastAPI
- **Python 3.11** com FastAPI (web framework)
- **SQLAlchemy** para ORM (Object-Relational Mapping)
- **PostgreSQL** como banco de dados
- **JWT** para autenticacao segura
- **Pydantic** para validacao de dados

---

## Estrutura do Projeto

```
mastermind-challenge/
|
+-- frontend/                          # Aplicacao Angular (SPA)
|   +-- src/
|   |   +-- app/
|   |   |   +-- components/
|   |   |   |   +-- game/             # Pagina principal do jogo
|   |   |   |   +-- login/            # Tela de login/registro
|   |   |   |   +-- ranking/          # Ranking global
|   |   |   +-- services/             # HttpClient para API
|   |   |   +-- guards/               # Protecao de rotas (Auth)
|   |   |   +-- models/               # Interfaces TypeScript
|   |   +-- assets/                   # Imagens (alien.png, astronauta.png, lua.png)
|   |   +-- styles.css                # CSS global (tema alienigena)
|   |   +-- main.ts                   # Bootstrap da aplicacao
|   +-- package.json                  # Dependencias do Node.js
|   +-- angular.json                  # Configuracao do Angular
|
+-- backend/                           # API REST (FastAPI)
|   +-- app/
|   |   +-- api/                      # Controllers (Rotas HTTP)
|   |   |   +-- auth.py               # POST /api/auth/register, /login
|   |   |   +-- games.py              # POST /api/games/start, /attempt
|   |   |   +-- rankings.py           # GET /api/rankings
|   |   |
|   |   +-- services/                 # Business Logic
|   |   |   +-- services.py           # AuthService, GameService, RankingService
|   |   |
|   |   +-- repositories/             # Data Access Layer
|   |   |   +-- repositories.py       # UserRepository, GameRepository
|   |   |
|   |   +-- models/                   # Database Models (SQLAlchemy)
|   |   |   +-- database.py           # User, Game, Attempt
|   |   |
|   |   +-- schemas/                  # Request/Response Validation (Pydantic)
|   |   |   +-- schemas.py            # Schemas para API
|   |   |
|   |   +-- utils/                    # Logica core
|   |   |   +-- mastermind.py         # Algoritmo do jogo
|   |   |
|   |   +-- config.py                 # Configuracoes (env vars)
|   |   +-- dependencies.py           # Injecao de dependencias (JWT, DB)
|   |   +-- main.py                   # FastAPI app factory
|   |
|   +-- tests/                        # Suite de testes (Pytest)
|   |   +-- test_api.py               # Testes de endpoints
|   |   +-- test_auth.py              # Testes de autenticacao
|   |   +-- test_mastermind_logic.py  # Testes da logica do jogo
|   |   +-- conftest.py               # Pytest fixtures
|   |
|   +-- requirements.txt              # Dependencias Python (pip)
|   +-- Dockerfile                    # Imagem Docker backend
|   +-- wsgi.py                       # Entry point producao
|   +-- setup_database.py             # Script para inicializar BD
|   +-- .env.example                  # Modelo de variaveis de ambiente
|
+-- docker-compose.yml                # Orquestracao (PostgreSQL + Backend)
+-- README.md                         # Este arquivo
```

---

## Como Rodar Localmente

### Passo 1: Clonar o Repositorio

```bash
git clone https://github.com/seu-usuario/mastermind-challenge.git
cd mastermind-challenge
```

### Passo 2: Configurar o Backend

#### 2.1 Entrar no diretorio backend

```bash
cd backend
```

#### 2.2 Criar variaveis de ambiente

Crie um arquivo `.env` na pasta `backend/` a partir do modelo:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com as suas credenciais:

```env
# Banco de Dados
DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/mastermind_db

# JWT e Seguranca
SECRET_KEY=gere-uma-chave-secreta-longa-e-aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Aplicacao
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

**Importante:** Nunca suba o arquivo `.env` para o repositorio. Ele ja esta no `.gitignore`.

#### 2.3 Criar Banco de Dados PostgreSQL

Abra o terminal do PostgreSQL:

```bash
psql -U postgres
```

Execute:

```sql
CREATE DATABASE mastermind_db;
\q
```

#### 2.4 Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2.5 Instalar Dependencias

```bash
pip install -r requirements.txt
```

#### 2.6 Inicializar Banco de Dados

```bash
python setup_database.py
```

Este script cria as tabelas necessarias (users, games, attempts) no PostgreSQL.

#### 2.7 Rodar Backend (Desenvolvimento)

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend rodando em: http://localhost:8000

Documentacao da API (Swagger): http://localhost:8000/docs

---

### Passo 3: Configurar o Frontend

#### 3.1 Em outra janela do terminal, ir para frontend

```bash
cd frontend
```

#### 3.2 Instalar Dependencias do Node.js

```bash
npm install
```

#### 3.3 Rodar Frontend (Desenvolvimento)

```bash
ng serve --open
```

Ou:

```bash
npm start
```

Frontend abrira em: http://localhost:4200

---

## Como Jogar

1. **Crie uma conta**: Registre-se na pagina de login
2. **Comece um novo jogo**: Clique em "Novo Jogo"
3. **Adivinhe a sequencia**:
   - Escolha 4 cores clicando nos botoes coloridos
   - Clique em "Enviar Palpite"
4. **Feedback**:
   - **Posicoes corretas**: Cor certa no lugar certo
   - **Cores corretas**: Cor certa no lugar errado
5. **Objetivo**: Adivinhe a combinacao em ate 10 tentativas
6. **Rankings**: Compare sua pontuacao com outros jogadores

---

## Executar Testes

### Backend (Pytest)

```bash
cd backend

# Todos os testes
pytest

# Com relatorio de cobertura
pytest --cov=app tests/

# Teste especifico
pytest tests/test_mastermind_logic.py -v

# Modo verbose
pytest -v
```

### Frontend (Angular Testing)

```bash
cd frontend

# Rodar testes unitarios
ng test

# Rodar testes com cobertura
ng test --code-coverage
```

---

## Rodar com Docker Compose

### Pre-requisitos

- Docker instalado
- Docker Compose instalado

### Comando

```bash
# No diretorio raiz do projeto
docker-compose up --build
```

Opcionalmente, crie um arquivo `.env` na raiz do projeto para configurar as credenciais do Docker:

```env
POSTGRES_USER=mastermind
POSTGRES_PASSWORD=sua_senha_segura
POSTGRES_DB=mastermind_db
SECRET_KEY=sua-chave-secreta
```

**O que inicia:**
- **PostgreSQL** na porta 5432
- **Backend FastAPI** na porta 8000

---

## Endpoints da API

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| POST | /api/auth/register | Registrar novo usuario |
| POST | /api/auth/login | Login (retorna JWT token) |
| POST | /api/games/start | Iniciar novo jogo |
| POST | /api/games/{game_id}/attempt | Fazer uma tentativa |
| GET | /api/games/active | Obter jogo ativo do usuario |
| GET | /api/games/{game_id} | Obter estado de um jogo |
| POST | /api/games/{game_id}/result | Obter resultado (jogo finalizado) |
| POST | /api/games/{game_id}/abandon | Abandonar jogo ativo |
| GET | /api/rankings | Obter ranking global |

Documentacao interativa completa: http://localhost:8000/docs

---

## Arquitetura da Aplicacao

```
+-------------------------------------------------------------+
|                     FRONTEND (Angular)                      |
|  +----------+  +----------+  +----------+  +------------+  |
|  |  Login   |  |  Game    |  | Ranking  |  | Services   |  |
|  +----+-----+  +----+-----+  +----+-----+  +-----+------+  |
+-------+--------------+--------------+--------------+--------+
        |              |              |              |
        +--------------+--------------+--------------+
                       | HTTP + JWT
                       v
+-------------------------------------------------------------+
|           BACKEND API (FastAPI + Python)                    |
|  +------------------------------------------------------+  |
|  |                   Controllers (API)                   |  |
|  |  [Auth Routes] [Game Routes] [Ranking Routes]        |  |
|  +----------------------+-------------------------------+  |
|                         |                                   |
|  +----------------------v-------------------------------+  |
|  |                  Services Layer                      |  |
|  |  [AuthService] [GameService] [RankingService]       |  |
|  +----------------------+-------------------------------+  |
|                         |                                   |
|  +----------------------v-------------------------------+  |
|  |               Repositories Layer                     |  |
|  |  [UserRepository] [GameRepository] [Logic Layer]    |  |
|  +----------------------+-------------------------------+  |
+-------------------------+-----------------------------------+
                          |
                          v
                   +--------------+
                   |  PostgreSQL  |
                   |   Database   |
                   +--------------+
```

---

## Seguranca

- Senhas hasheadas com **Argon2**
- Autenticacao via **JWT** (JSON Web Token)
- Protecao de rotas com auth guards
- CORS configurado para comunicacao frontend-backend
- Validacao de entrada com Pydantic
- SQL Injection prevenido via ORM SQLAlchemy
- Variaveis sensiveis (.env) excluidas do repositorio via .gitignore

---

## Troubleshooting

### PostgreSQL nao conecta

```bash
# Verificar se PostgreSQL esta rodando
psql -U postgres -c "SELECT version();"

# Se nao funcionar, inicie o servico:
# Windows
pg_ctl start

# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

### Porta 8000 ja em uso

```bash
# Mudar porta
python -m uvicorn app.main:app --reload --port 8001
```

### Modulo Python nao encontrado

```bash
# Garantir que o venv esta ativado
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Erro de CORS no frontend

Verifique se o backend esta rodando em http://localhost:8000 e se o frontend aponta para essa URL no arquivo de environment.

---

## Licenca

Este projeto e de codigo aberto e pode ser usado livremente para fins educacionais e comerciais.
