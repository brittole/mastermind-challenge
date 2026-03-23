# 🚀 Guia de Deployment - Mastermind Challenge

**Objetivo:** Disponibilizar a aplicação em uma URL publica para que o recrutador possa acessar e jogar sem configuração local.

---

## 📋 Opções de Deployment (Do Mais Fácil ao Mais Robusto)

### **Opção 1: Render (⭐ RECOMENDADO - Mais Fácil)**

**Vantagens:**
- Free tier generoso
- Deploy automático do GitHub
- Banco de dados PostgreSQL gratuito
- Suporta Node.js + Python
- SSL certificado automático

**Passos:**

1. **Criar conta em** [render.com](https://render.com)

2. **Conectar GitHub:**
   - Settings → GitHub → Conectar repositório

3. **Criar serviço PostgreSQL:**
   - New → PostgreSQL
   - Nome: `mastermind-db`
   - Region: `São Paulo` ou `US`
   - Copiar connection string

4. **Criar serviço Web para Backend:**
   - New → Web Service
   - Repository: seu repositório
   - Root directory: `backend/`
   - Environment: `Python 3.11`
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn -w 4 app.main:app --timeout 120`

5. **Variáveis de Ambiente:**
   ```env
   DATABASE_URL=postgresql://seu_user:senha@render-db-host/dbname
   ENVIRONMENT=production
   DEBUG=false
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   SECRET_KEY=sua-chave-super-secreta-aqui
   ```

6. **Criar serviço Web para Frontend:**
   - New → Web Service
   - Repository: seu repositório
   - Root directory: `frontend/`
   - Environment: `Node.js`
   - Build command: `npm install && npm run build`
   - Start command: `npm start` ou `npm run serve`

**URL Final:** `https://seu-app.onrender.com`

---

### **Opção 2: Vercel + Railway (Alternativa Moderna)**

**Para o Frontend (Vercel):**
```bash
npm run build
vercel --prod
```

**Para o Backend (Railway):**
1. Conectar GitHub em [railway.app](https://railway.app)
2. Adicionar variáveis de ambiente
3. Deploy automático

---

### **Opção 3: Heroku (Gratuito, Porém com Limitações)**

**NOTA:** Heroku encerrou free tier gratuito em 2022, mas você pode usar:
- **Heroku Eco Dynos** (pago, $5/mês)
- Ou migrar para Render/Railway

---

## 🔧 Configuração Local (Para Testes Antes do Deploy)

### **Backend:**

```bash
cd backend

# 1. Criar ambiente virtual
python -m venv venv
.\venv\Scripts\activate  # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar .env
echo DATABASE_URL=postgresql://user:password@localhost:5432/mastermind > .env
echo SECRET_KEY=sua-chave-aqui >> .env

# 4. Iniciar servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**API disponível em:** `http://localhost:8000`
**Documentação:** `http://localhost:8000/api/docs`

### **Frontend:**

```bash
cd frontend

# 1. Instalar dependências
npm install

# 2. Iniciar servidor
ng serve --open

# ou

npm start
```

**App disponível em:** `http://localhost:4200`

---

## 🐳 Deploy com Docker (Recomendado para Produção)

### **Pré-requisitos:**
- Docker instalado
- Docker Compose instalado

### **Comando:**
```bash
cd mastermind-challenge

# Build das imagens
docker-compose build

# Iniciar containers
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar containers
docker-compose down
```

**Acesso:**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Documentação API: `http://localhost:8000/api/docs`

---

## 📊 Arquitetura de Deployment Recomendada

```
┌─────────────────────────────────────────────────────────┐
│         Render (ou Vercel/Railway/Heroku)              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐      ┌──────────────────┐       │
│  │  Frontend        │      │  Backend API     │       │
│  │  (Angular/React) │←────→│  (FastAPI)       │       │
│  │  https://app...  │      │  https://api...  │       │
│  └──────────────────┘      └──────────────────┘       │
│                                    ↓                    │
│                         ┌──────────────────┐           │
│                         │  PostgreSQL DB   │           │
│                         │  (Render DB)     │           │
│                         └──────────────────┘           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 Variáveis de Ambiente (Produção)

**Backend (.env.production):**
```env
# Banco de dados
DATABASE_URL=postgresql://user:pass@host:5432/mastermind

# Segurança
SECRET_KEY=gerar-com-openssl-rand-hex-32
DEBUG=false
ENVIRONMENT=production

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=https://seu-frontend.com,https://seu-outro-dominio.com

# API
API_HOST=https://sua-api.onrender.com
API_PORT=443
```

**Frontend (environment.prod.ts):**
```typescript
export const environment = {
  production: true,
  API_BASE_URL: 'https://sua-api.onrender.com'
};
```

---

## ✅ Checklist de Deploy

- [ ] Código está em repositório Git (GitHub)
- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados PostgreSQL criado
- [ ] Testes passando localmente (`pytest`)
- [ ] Frontend compilado e testado (`ng build`)
- [ ] CORS autoriza o domínio frontend
- [ ] SSL/HTTPS habilitado
- [ ] Health check funciona (`/health`)
- [ ] Recrutador consegue registrar e jogar
- [ ] Estatísticas e ranking funcionam

---

## 🧪 Testar Antes de Enviar Para Recrutador

### **1. Testar Backend:**
```bash
# Rodar todos os testes
pytest -v

# Testar um endpoint específico
pytest tests/test_api.py::TestAuthEndpoints::test_register_success -v
```

### **2. Testar Frontend:**
```bash
# Build para produção
ng build --configuration production

# Servir localmente
ng serve
```

### **3. Testar Fluxo Completo:**
1. Acessar aplicação
2. Registrar novo usuário
3. Fazer login
4. Iniciar jogo
5. Fazer algumas tentativas
6. Ver resultado
7. Ver ranking / estatísticas

---

## 🆘 Troubleshooting

### **Erro: "Connection refused" (Banco de dados)**
```bash
# Verificar se PostgreSQL está rodando
docker ps | grep postgres

# Verificar DATABASE_URL está correto
echo $DATABASE_URL
```

### **Erro: "CORS policy"**
- Adicionar domínio frontend ao `ALLOWED_ORIGINS`
- Reiniciar backend

### **Erro: "Module not found" (Python)**
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### **Frontend não carrega API**
- Verificar `environment.ts` tem URL correta da API
- Verificar CORS está habilitado no backend
- Abrir DevTools (F12) → Console

---

## 🎯 Próximos Passos

1. **Escolher plataforma de deployment** (Render recomendado)
2. **Criar contas e conectar GitHub**
3. **Fazer deploy automático**
4. **Testar aplicação completa**
5. **Compartilhar URL com recrutador**

---

**Dúvidas?** Veja a documentação completa em cada serviço ou abra uma issue no GitHub.

🚀 **Boa sorte com seu desafio!**
