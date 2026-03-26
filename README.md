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

> **Resumo rapido:** voce vai precisar de **3 terminais abertos** ao final:
> 1. PostgreSQL rodando
> 2. Backend (FastAPI) na porta 8000
> 3. Frontend (Angular) na porta 4200

---

### Passo 1: Clonar o Repositorio

```bash
git clone https://github.com/seu-usuario/mastermind-challenge.git
cd mastermind-challenge
```

---

### Passo 2: Instalar e Configurar o PostgreSQL

O projeto usa **PostgreSQL** como banco de dados. Voce precisa dele instalado e rodando na sua maquina.

#### 2.1 Instalar o PostgreSQL

| Sistema | Comando / Instrucao |
|---------|---------------------|
| **Windows** | Baixe o instalador em https://www.postgresql.org/download/windows/ e siga o wizard. Durante a instalacao, **anote a senha** que voce definir para o usuario `postgres`. Marque a opcao para adicionar ao PATH. |
| **macOS** | `brew install postgresql@15 && brew services start postgresql@15` |
| **Linux (Ubuntu/Debian)** | `sudo apt update && sudo apt install postgresql postgresql-contrib -y && sudo systemctl start postgresql` |

#### 2.2 Verificar se o PostgreSQL esta rodando

```bash
psql -U postgres -c "SELECT version();"
```

Se pedir senha, use a senha que voce definiu na instalacao. Se funcionar, voce vera a versao do PostgreSQL.

> **Windows:** Se o comando `psql` nao for encontrado, adicione o diretorio `bin` do PostgreSQL ao PATH do sistema. O caminho depende da versao instalada:
> - PostgreSQL 15: `C:\Program Files\PostgreSQL\15\bin`
> - PostgreSQL 16: `C:\Program Files\PostgreSQL\16\bin`
> - PostgreSQL 17: `C:\Program Files\PostgreSQL\17\bin`
>
> Para descobrir qual versao voce tem, abra `C:\Program Files\PostgreSQL\` e veja a pasta que existe la dentro.
>
> **Como adicionar ao PATH temporariamente (so nessa sessao do PowerShell):**
> ```powershell
> $env:Path += ";C:\Program Files\PostgreSQL\17\bin"   # troque 17 pela sua versao
> ```
>
> **Como adicionar ao PATH permanentemente:** Pesquise "Variaveis de Ambiente" no menu Iniciar → Edite a variavel `Path` do sistema → Adicione o caminho do `bin`.

#### 2.3 Criar o Banco de Dados

```bash
psql -U postgres
```

Dentro do prompt do PostgreSQL, execute:

```sql
CREATE DATABASE mastermind_db;
\q
```

> **Dica:** Se voce quiser usar um usuario/senha diferente de `postgres`, basta ajustar a `DATABASE_URL` no passo 3.2.

---

### Passo 3: Configurar e Rodar o Backend (FastAPI)

#### 3.1 Entrar no diretorio backend

```bash
cd backend
```

#### 3.2 Criar o arquivo de variaveis de ambiente

Copie o modelo `.env.example` para `.env`:

```bash
# macOS / Linux
cp .env.example .env

# Windows (CMD)
copy .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env
```

Agora abra o arquivo `backend/.env` no seu editor e preencha com os seus dados reais:

```env
# Banco de Dados
# Formato: postgresql://USUARIO:SENHA@HOST:PORTA/NOME_DO_BANCO
# Substitua "SUA_SENHA" pela senha do seu usuario postgres
DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/mastermind_db

# JWT e Seguranca
# Gere uma chave secreta forte (ex: openssl rand -hex 32)
SECRET_KEY=gere-uma-chave-secreta-longa-e-aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Aplicacao
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

| Variavel | O que colocar | Exemplo |
|----------|---------------|---------|
| `DATABASE_URL` | URL de conexao com o PostgreSQL. Troque `SUA_SENHA` pela senha real do usuario `postgres`. | `postgresql://postgres:minhasenha123@localhost:5432/mastermind_db` |
| `SECRET_KEY` | Uma string longa e aleatoria para assinar os tokens JWT. | `a3f8c9e1b7d04...` (use `openssl rand -hex 32` ou `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `ALGORITHM` | Algoritmo de assinatura JWT. Mantenha `HS256`. | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo (em minutos) de validade do token. | `30` |
| `DEBUG` | Modo debug — `true` para desenvolvimento. | `true` |

> **Importante:** O arquivo `.env` ja esta no `.gitignore`. **Nunca suba ele para o repositorio.**

#### 3.3 Criar e ativar o Ambiente Virtual Python

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

Apos ativar, voce deve ver `(.venv)` no inicio da linha do terminal.

> **Nota:** O ambiente virtual e criado na raiz do projeto (`.venv/`), nao dentro de `backend/`. Isso e intencional — o mesmo venv serve para todo o backend.

#### 3.4 Instalar as dependencias Python

```bash
pip install -r requirements.txt
```

Isso instala: FastAPI, Uvicorn, SQLAlchemy, psycopg2, Pydantic, python-jose (JWT), Argon2, Pytest, entre outros.

#### 3.5 Inicializar as tabelas no Banco de Dados

```bash
python setup_database.py
```

Este script conecta no PostgreSQL usando a `DATABASE_URL` do seu `.env` e cria as tabelas:
- `users` — cadastro de jogadores
- `games` — partidas (codigo secreto, status, pontuacao)
- `attempts` — tentativas de cada partida

Voce deve ver a saida:

```
[*] Conectando ao PostgreSQL...
[OK] Conectado ao PostgreSQL!
[OK] Tabela 'users' criada
[OK] Tabela 'games' criada
[OK] Tabela 'attempts' criada
[OK] Indices criados
[SUCESSO] PostgreSQL inicializado com sucesso!
```

> **Se der erro de conexao:** verifique se o PostgreSQL esta rodando, se a senha esta correta no `.env`, e se o banco `mastermind_db` foi criado no passo 2.3.

#### 3.6 Rodar o Backend (modo desenvolvimento)

> **IMPORTANTE:** Voce DEVE estar dentro da pasta `backend/` para rodar este comando. Se rodar da raiz do projeto, vai dar erro `ModuleNotFoundError: No module named 'app'`.

```bash
# Confirme que esta dentro de backend/
cd backend

# Rodar o servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Se tudo estiver certo, voce vera:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Started reloader process
```

> **Se der `ModuleNotFoundError: No module named 'app'`:** voce provavelmente esta no diretorio errado. Rode `cd backend` e tente novamente.

| URL | O que e |
|-----|---------|
| http://localhost:8000 | API rodando |
| http://localhost:8000/docs | Documentacao interativa (Swagger UI) |
| http://localhost:8000/health | Health check da aplicacao |

> **Mantenha este terminal aberto.** O backend precisa ficar rodando.

---

### Passo 4: Configurar e Rodar o Frontend (Angular)

> **Abra um novo terminal** (o backend deve continuar rodando no anterior).

#### 4.1 Entrar no diretorio frontend

```bash
cd frontend
```

> Se voce esta na raiz do projeto: `cd frontend`. Se esta em `backend/`: `cd ../frontend`.

#### 4.2 Instalar as dependencias Node.js

```bash
npm install
```

Isso baixa todas as dependencias do Angular listadas no `package.json`. Pode demorar alguns minutos na primeira vez.

#### 4.3 Rodar o Frontend (modo desenvolvimento)

```bash
npm start
```

Isso executa `ng serve --open`, que compila o Angular e abre o navegador automaticamente.

O frontend estara disponivel em: **http://localhost:4200**

> **Mantenha este terminal aberto tambem.** O frontend precisa ficar rodando.

---

### Checklist Final — Tudo Rodando?

| Servico | URL | Como verificar |
|---------|-----|----------------|
| **PostgreSQL** | localhost:5432 | `psql -U postgres -c "SELECT 1;"` |
| **Backend** | http://localhost:8000 | Abra http://localhost:8000/health no navegador — deve retornar `{"status": "saudável"}` |
| **Frontend** | http://localhost:4200 | Abra no navegador — deve aparecer a tela de login do Mastermind |

Se os 3 estao funcionando, o projeto esta pronto para uso!

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

### Backend (Pytest — testes automatizados)

Os testes do backend sao **100% automatizados** usando **Pytest**. Nao precisam do PostgreSQL real — usam um banco **SQLite em memoria** que e criado e destruido automaticamente.

```bash
cd backend

# Ativar o ambiente virtual (se ainda nao estiver ativo)
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Rodar todos os testes
pytest

# Com relatorio de cobertura de codigo
pytest --cov=app tests/

# Rodar um arquivo de teste especifico
pytest tests/test_mastermind_logic.py -v

# Modo verbose (mostra cada teste individualmente)
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

## Sistema de Pontuacao e Ranking

### Pontuacao por partida

Cada partida comeca com **1000 pontos**. Dois fatores descontam pontos:

| Fator | Regra | Detalhe |
|-------|-------|---------|
| **Tentativas** | -50 pts por tentativa a partir da 3a | As 2 primeiras sao gratis |
| **Tempo** | -1 pt por minuto de jogo | Quanto mais rapido, melhor |

**Formula:** `pontos = max(0, 1000 - max(0, (tentativas - 2) * 50) - (segundos / 60))`

**Exemplos:**

| Cenario | Tentativas | Tempo | Pontos |
|---------|:---:|:---:|:---:|
| Perfeito | 1 | 30s | 999.5 |
| Bom | 3 | 2min | 948.0 |
| Medio | 5 | 5min | 845.0 |
| Dificil | 8 | 10min | 690.0 |
| Limite | 10 | 15min | 585.0 |

- Pontuacao maxima possivel: **1000** (1 tentativa, 0 segundos)
- Pontuacao minima: **0** (nunca fica negativa)

### Ranking global

Os jogadores sao classificados por:
1. **Taxa de vitoria (%)** — quem ganha mais partidas fica acima
2. **Melhor pontuacao** — em caso de empate, quem tem a maior pontuacao fica acima

> Apenas jogos **ganhos** contam para melhor pontuacao e media. Jogos perdidos ou abandonados nao somam pontos no ranking.

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

# Windows (PowerShell como Administrador)
# O nome do servico depende da versao instalada (ex: postgresql-x64-15, postgresql-x64-17)
# Primeiro descubra o nome exato:
Get-Service *postgres*
# Depois inicie com o nome correto:
net start postgresql-x64-17

# macOS
brew services start postgresql@15

# Linux (Ubuntu/Debian)
sudo systemctl start postgresql
sudo systemctl enable postgresql   # para iniciar automaticamente no boot
```

### Erro "password authentication failed"

Sua senha do PostgreSQL esta errada no `.env`. Verifique a variavel `DATABASE_URL`:
```env
DATABASE_URL=postgresql://postgres:SENHA_CORRETA_AQUI@localhost:5432/mastermind_db
```

### Banco "mastermind_db" nao existe

```bash
psql -U postgres -c "CREATE DATABASE mastermind_db;"
```

### Porta 8000 ja em uso

```bash
# Mudar porta do backend
python -m uvicorn app.main:app --reload --port 8001
```

### Porta 4200 ja em uso

```bash
# Mudar porta do frontend
ng serve --port 4201
```

### Modulo Python nao encontrado

```bash
# Garantir que o venv esta ativado
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Reinstalar dependencias
cd backend
pip install -r requirements.txt
```

### `ModuleNotFoundError: No module named 'app'`

Isso acontece quando voce roda o uvicorn fora da pasta `backend/`. O comando precisa ser executado de dentro dela:

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Erro de CORS no frontend

Verifique se o backend esta rodando em http://localhost:8000 e se o frontend aponta para essa URL no arquivo de environment.

---

## Licenca

Este projeto e de codigo aberto e pode ser usado livremente para fins educacionais e comerciais.
