# 🚀 Guia Completo de Deploy - Mastermind Challenge

## Opção 1: Deploy Fácil com Render + Vercel (Recomendado)

### **PARTE 1: Deploy Backend + Banco de Dados no Render**

#### Passo 1: Criar Conta no Render
1. Acesse: https://render.com
2. Clique em "Sign up"
3. Registre-se com GitHub (mais fácil)

#### Passo 2: Conectar seu Repositório GitHub
1. Push seu código para GitHub:
   ```bash
   cd c:\Users\Leticia\projetos\mastermind-challenge
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/SEU_USUARIO/mastermind-challenge.git
   git push -u origin main
   ```

#### Passo 3: Criar Serviço Web no Render
1. No Render Dashboard, clique **"New +"** → **"Web Service"**
2. Conecte seu repositório GitHub
3. Configure:
   - **Name**: `mastermind-backend`
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python wsgi.py`
   - **Plan**: Free (está bom!)

#### Passo 4: Criar PostgreSQL no Render
1. No Render Dashboard, clique **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `mastermind-db`
   - **Plan**: Free
3. Copie a **DATABASE_URL** gerada

#### Passo 5: Configurar Variáveis de Ambiente
No seu serviço Web (backend), vá em **Environment**:
```
DATABASE_URL = postgresql://user:pass@host:5432/db
SECRET_KEY = sua-chave-secreta-aqui
ENVIRONMENT = production
BACKEND_URL = https://seu-backend-no-render.onrender.com
```

#### Passo 6: Atualizar Backend para Usar DATABASE_URL
Edite `backend/app/config.py`:
```python
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Para PostgreSQL remoto
if DATABASE_URL.startswith("postgresql"):
    # Render adiciona pool de conexão
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300
    )
else:
    engine = create_engine(DATABASE_URL)
```

---

### **PARTE 2: Deploy Frontend no Vercel**

#### Passo 1: Preparar Frontend
Edite `frontend/src/app/services/api.service.ts`:
```typescript
private apiUrl = process.env['NG_APP_API_URL'] || 'http://localhost:8080/api';
```

Crie arquivo `.env`:
```
NG_APP_API_URL=https://seu-backend-no-render.onrender.com/api
```

#### Passo 2: Criar Conta no Vercel
1. Acesse: https://vercel.com
2. Clique "Sign Up"
3. Registre com GitHub

#### Passo 3: Deploy no Vercel
1. Clique **"Add New..."** → **"Project"**
2. Selecione seu repositório GitHub
3. Configure:
   - **Framework**: Angular
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist/frontend`
4. Clique **"Deploy"**

#### Passo 4: Configurar URL da API
No Vercel Dashboard → **Settings** → **Environment Variables**:
```
NG_APP_API_URL = https://seu-backend-no-render.onrender.com/api
```

---

## Opção 2: Deploy Tudo em Um Só Lugar (Railway)

Mais simples, mas custo mínimo (~$5/mês com créditos gratuitos):

1. Acesse: https://railway.app
2. Clique **"New Project"**
3. Conecte GitHub
4. Railway detecta automaticamente:
   - Python (backend)
   - Node/Angular (frontend)
   - PostgreSQL

---

## Opção 3: Docker + VPS (Mais Controle)

Se quiser seu próprio servidor:

### Criar Dockerfile
```dockerfile
# Backend
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["python", "wsgi.py"]

# Frontend
FROM node:18 AS builder
WORKDIR /app
COPY frontend/package*.json .
RUN npm install
COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
```

### Fazer Deploy em VPS (DigitalOcean, Linode, etc.)
```bash
# SSH no servidor
ssh root@seu-servidor.com

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clonar repo, build e rodar
git clone seu-repo
docker-compose up -d
```

---

## 📊 Resumo das Opções

| Aspecto | Render+Vercel | Railway | Docker VPS |
|--------|---------------|---------|-----------|
| **Facilidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Custo** | Gratuito | ~$5/mês | ~$5-10/mês |
| **Setup Time** | 15 min | 10 min | 30 min |
| **Controle** | Limitado | Médio | Total |

---

## ✅ Checklist Final

- [ ] Código commitado no GitHub
- [ ] Variáveis de ambiente configuradas
- [ ] Backend respondendo em: `https://seu-backend.onrender.com`
- [ ] Frontend acessível em: `https://seu-frontend.vercel.app`
- [ ] Frontend conectado ao backend correto
- [ ] CORS configurado (se necessário)
- [ ] Teste a aplicação completa online

---

## 🔗 URLs Finais

Após deploy:
- **Frontend**: `https://seu-frontend.vercel.app`
- **Backend API**: `https://seu-backend.onrender.com/api`
- **Docs API**: `https://seu-backend.onrender.com/docs`

Envie o link do frontend para as pessoas! 🎉
