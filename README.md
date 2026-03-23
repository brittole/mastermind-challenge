# Mastermind Game - Backend API

Implementação de uma API REST completa para o clássico jogo **Mastermind** (quebra-cabeça de cores). O usuário tem 10 tentativas para adivinhar uma sequência de 4 cores.

## Visão Geral

Este projeto implementa o **backend** de um jogo Mastermind com:

- **Arquitetura em camadas** (Controllers → Services → Repositories)
- **Autenticação JWT** segura
- **Banco de dados PostgreSQL** com ORM SQLAlchemy
- **Testes unitários** com pytest (cobertura completa)
- **API Documentation** automática com Swagger/OpenAPI
- **Deploy-ready** com Docker e docker-compose
- **Lógica sólida** e bem testada

---

## Stack Tecnológico

| Camada | Tecnologia |
|--------|-----------|
| **Backend** | Python 3.11 + FastAPI |
| **Database** | PostgreSQL 15 |
| **ORM** | SQLAlchemy 2.0 |
| **Autenticação** | JWT (PyJWT) |
| **Validação** | Pydantic |
| **Testes** | Pytest |
| **Documentação** | Swagger/OpenAPI |
| **Container** | Docker + Docker Compose |

---

## Estrutura do Projeto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application factory
│   ├── config.py                  # Configurações (env vars)
│   ├── dependencies.py            # Injeção de dependências (JWT, DB)
│   │
│   ├── api/                       # CONTROLLERS (API Routes)
│   │   ├── auth.py               # POST /register, /login
│   │   ├── games.py              # POST /start, /attempt, GET /games
│   │   └── rankings.py           # GET /rankings
│   │
│   ├── services/                 # SERVICES (Business Logic)
│   │   └── services.py           # AuthService, GameService, RankingService
│   │
│   ├── repositories/             # REPOSITORIES (Data Access)
│   │   └── repositories.py       # UserRepository, GameRepository, AttemptRepository
│   │
│   ├── models/                   # MODELS (Database)
│   │   └── database.py           # User, Game, Attempt (SQLAlchemy)
│   │
│   ├── schemas/                  # SCHEMAS (Request/Response Validation)
│   │   └── schemas.py            # Pydantic models for API
│   │
│   └── utils/                    # UTILITIES
│       └── mastermind.py         # Lógica core do jogo
│
├── tests/
│   ├── conftest.py              # Pytest fixtures
│   ├── test_mastermind_logic.py # Testes da lógica do jogo
│   ├── test_auth.py             # Testes de autenticação
│   └── test_api.py              # Testes de endpoints
│
├── requirements.txt              # Python dependencies
├── pytest.ini                    # Pytest configuration
├── Dockerfile                    # Docker image
├── wsgi.py                       # WSGI entry point (production)
├── .env.example                  # Environment variables example
└── .gitignore

```

---

## Arquitetura em Camadas

```
REQUEST → API Layer (Controllers) → Service Layer → Repository Layer → Database
RESPONSE ← API Layer (Controllers) ← Service Layer ← Repository Layer ← Database
```

### **Camada 1: API (Controllers)**
- Responsáveis por HTTP (receber requests, retornar responses)
- Validação de entrada com Pydantic
- Autenticação JWT
- **Arquivos**: `api/auth.py`, `api/games.py`, `api/rankings.py`

### **Camada 2: Services**
- Lógica de negócio complexa
- Orquestração de múltiplos repositories
- Validações de regras de negócio
- **Arquivo**: `services/services.py`

### **Camada 3: Repositories**
- Acesso direto ao banco de dados
- Operações CRUD simples
- Queries otimizadas
- **Arquivo**: `repositories/repositories.py`

### **Camada 4: Models**
- Definição de tabelas do banco
- Relacionamentos entre entidades
- **Arquivo**: `models/database.py`

---

## Como Rodar Localmente

### **Pré-requisitos**

- **Python 3.11+**  
- **PostgreSQL 14+** (instalado e rodando)  
- **Git**  
- **pip** ou **poetry**

Verifique as versões:
```bash
python --version        # Python 3.11+
psql --version         # PostgreSQL 14+
```

### **1. Clonar o repositório**

```bash
git clone https://github.com/seu-usuario/mastermind-challenge.git
cd mastermind-challenge/backend
```

### **2. Criar variáveis de ambiente**

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite `.env` com suas credenciais PostgreSQL:

```env
# Database
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/mastermind_db

# JWT
SECRET_KEY=sua-chave-secreta-aqui-use-algo-seguro-em-produção
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

### **3. Criar banco de dados PostgreSQL**

```bash
psql -U postgres
```

```sql
CREATE DATABASE mastermind_db;
\q
```

### **4. Criar ambiente virtual (venv)**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### **5. Instalar dependências**

```bash
pip install -r requirements.txt
```

### **6. Rodar a aplicação**

```bash
python -m uvicorn app.main:app --reload
```

Acesse:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

---

## Executar Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=app tests/

# Apenas testes de lógica
pytest tests/test_mastermind_logic.py -v

# Apenas testes de autenticação
pytest tests/test_auth.py -v

# Apenas testes de API
pytest tests/test_api.py -v
```

> **Nota**: Os testes usam SQLite em memória, então não dependem do PostgreSQL

---

## Rodar com Docker Compose

### **Pré-requisitos**
- Docker
- Docker Compose

### **Comando**

```bash
# Para no diretório raiz do projeto
cd mastermind-challenge

# Iniciar contêineres (PostgreSQL + Backend)
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Parar contêineres
docker-compose down

# Limpar volumes (reset database)
docker-compose down -v
```

Acesse: http://localhost:8000/api/docs

---

## API Endpoints

Base URL: `http://localhost:8000/api`

### **Autenticação**

#### Registrar novo usuário
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "john_doe",
  "password": "securepassword123"
}

Response: 201 Created
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "john_doe",
    "created_at": "2024-03-23T10:00:00Z"
  }
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword123"
}

Response: 200 OK
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {...}
}
```

### **Jogos**

#### Iniciar novo jogo
```http
POST /games/start
Authorization: Bearer {access_token}

Response: 201 Created
{
  "id": "game-uuid",
  "status": "started",
  "started_at": "2024-03-23T10:15:00Z",
  "ended_at": null,
  "attempts_count": 0,
  "final_score": null,
  "attempts": []
}
```

#### Fazer uma tentativa
```http
POST /games/{game_id}/attempt
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "guess": ["red", "blue", "green", "yellow"]
}

Response: 200 OK
{
  "id": "attempt-uuid",
  "attempt_number": 1,
  "guess": ["red", "blue", "green", "yellow"],
  "correct_positions": 2,
  "correct_colors": 1,
  "created_at": "2024-03-23T10:16:00Z"
}
```

**Significado do feedback:**
- `correct_positions`: Número de cores NO LUGAR CORRETO
- `correct_colors`: Número de cores CORRETAS MAS NA POSIÇÃO ERRADA

#### Obter estado do jogo
```http
GET /games/{game_id}
Authorization: Bearer {access_token}
```

#### Abandonar jogo
```http
POST /games/{game_id}/abandon
Authorization: Bearer {access_token}
```

#### Obter resultado do jogo
```http
POST /games/{game_id}/result
Authorization: Bearer {access_token}
```

#### Listar meus jogos
```http
GET /games
Authorization: Bearer {access_token}
```

### **Rankings**

#### Obter ranking global
```http
GET /rankings
```

#### Obter stats de um usuário
```http
GET /rankings/user/{user_id}
```

---

## Regras do Jogo

1. **Objetivo**: Adivinhar uma sequência de 4 cores em no máximo 10 tentativas
2. **Cores disponíveis**: red, blue, green, yellow, white, black
3. **Feedback**: correct_positions (cores no lugar) + correct_colors (cores erradas)
4. **Vitória**: Acertar a sequência exata (4 posições corretas)
5. **Derrota**: Não conseguir em 10 tentativas

---

## Segurança

- **Hashing**: bcrypt (passlib)
- **Autenticação**: JWT com HS256
- **Validação**: Pydantic em toda entrada
- **SQL Injection**: Prevenido via SQLAlchemy ORM

---

## Deploy em Produção

### **Docker**
```bash
docker build -t mastermind-api ./backend
docker run -p 8000:8000 mastermind-api
```

### **Variáveis de Ambiente (Produção)**
```env
DATABASE_URL=postgresql://user:pass@prod-host:5432/db
SECRET_KEY=gere-com-secrets.token_urlsafe(32)
DEBUG=false
```

---

## Decisões Técnicas

- **FastAPI**: Moderno, rápido, documentação automática Swagger
- **SQLAlchemy**: ORM maduro, prevenção SQL injection
- **PostgreSQL**: Robusto, profissional, suporta JSON
- **Arquitetura em Camadas**: Separation of concerns, testabilidade, escalabilidade

---

**Desenvolvido para processo seletivo Jr Full-Stack**
