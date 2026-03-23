# 🚀 Guia de Desenvolvimento - Mastermind

## Setup Local Completo

### 1️⃣ Backend (Python FastAPI)

```bash
# Navegar para backend
cd backend

# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Instalar dependências (se necessário)
pip install -r requirements.txt

# Executar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**URL do Backend**: http://localhost:8000  
**Documentação API**: http://localhost:8000/api/docs

### 2️⃣ Frontend (Angular)

```bash
# Navegar para frontend
cd frontend

# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm start
# Abre automaticamente em http://localhost:4200
```

### ✅ Testes

**Backend - Testes Unitários**:
```bash
cd backend
pytest tests/ -v
```

**Frontend - Testes Unitários**:
```bash
cd frontend
npm test
```

## 🔧 Troubleshooting

### Erro: "Cannot find module '@angular/router'"
```bash
cd frontend
npm install
```

### Erro: "Import 'fastapi.cors' could not be resolved"
```bash
cd backend
pip install "fastapi[all]" python-multipart pydantic-settings
```

### Erro: "Não é permitido usar '&' sem aspas"
Correto ❌: `npm install& python script.py`  
Correto ✅: `npm install; cd folder`

### Porta 8000 já em uso?
```bash
# Usar outra porta
uvicorn app.main:app --reload --port 8001
```

## 📁 Estrutura do Projeto

```
mastermind-challenge/
├── backend/               # API FastAPI
│   ├── app/
│   │   ├── main.py       # Aplicação principal
│   │   ├── config.py     # Configurações
│   │   ├── models/       # Modelos SQLAlchemy
│   │   ├── services/     # Lógica de negócios
│   │   ├── api/          # Endpoints
│   │   └── utils/        # Utilitários
│   ├── tests/            # Testes
│   ├── requirements.txt  # Dependências Python
│   └── .env              # Variáveis de ambiente
│
├── frontend/             # App Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/   # Componentes
│   │   │   ├── services/     # Serviços
│   │   │   ├── guards/       # Auth guards
│   │   │   ├── models/       # Interfaces
│   │   │   └── app.*         # Core
│   │   ├── environments/     # Config env
│   │   ├── assets/           # Arquivos estáticos
│   │   ├── styles.css        # Estilos globais
│   │   ├── main.ts           # Bootstrap
│   │   └── index.html        # HTML raiz
│   ├── package.json      # Dependências npm
│   ├── angular.json      # Config Angular
│   ├── tsconfig.json     # Config TypeScript
│   └── README.md         # Documentação
│
├── DEPLOYMENT.md         # Guia de deployment
├── README.md             # Documentação geral
└── .venv/               # Ambiente virtual Python
```

## 🎯 Fluxo de Desenvolvimento

1. **Backend** deve rodar primeiro (porta 8000)
2. **Frontend** conecta ao backend via http://localhost:8000/api
3. Qualquer erro de CORS → verificar main.py (CORSMiddleware)

## 📝 Commits e Versionamento

```bash
# Backend
git add backend/
git commit -m "feat(backend): adicionar novo endpoint"

# Frontend
git add frontend/
git commit -m "feat(frontend): criar componente login"
```

## 🚀 Build para Produção

**Backend**:
```bash
# Build Docker
docker build -t mastermind-api .
docker run -p 8000:8000 mastermind-api
```

**Frontend**:
```bash
npm run build
# Arquivos em: dist/mastermind-frontend/
```

## 🔐 Variáveis de Ambiente

**Backend (.env)**:
```
DATABASE_URL=postgresql://user:password@localhost/mastermind
DEBUG=False
SECRET_KEY=sua-chave-secreta-aqui
```

**Frontend (environment.prod.ts)**:
```typescript
apiUrl: 'https://seu-api.onrender.com/api'
```

## 📞 Suporte

- **Backend erros**: Ver logs em `backend/logs/`
- **Frontend erros**: Ver console do navegador (F12)
- **Database erros**: Ver arquivo `.env` e settings

---

**Dica**: Use terminal separados para backend e frontend durante desenvolvimento!

```bash
# Terminal 1 - Backend
cd backend && .\.venv\Scripts\Activate.ps1 && uvicorn app.main:app --reload

# Terminal 2 - Frontend  
cd frontend && npm start
```
