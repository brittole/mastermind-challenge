# 🚀 GUIA DE DEPLOY - 100% GRATUITO E SIMPLES

## ⏱️ Tempo Total: ~20 minutos

---

## 📝 PASSO 1: Criar Conta GitHub (2 min)

1. Acesse: https://github.com/signup
2. Registre com email
3. Confirme email
4. Pronto! ✅

---

## 📤 PASSO 2: Fazer Push do Código para GitHub (3 min)

**NO SEU COMPUTADOR**, abra PowerShell:

```powershell
cd c:\Users\Leticia\projetos\mastermind-challenge

# Configurar Git
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Inicializar
git init
git add .
git commit -m "Initial commit - Mastermind Challenge"
```

**Depois, no GitHub:**

1. Clique **"+"** (canto superior direito)
2. **"New repository"**
3. Nome: `mastermind-challenge`
4. Descrição: `Jogo Mastermind com Angular + FastAPI`
5. Clique **"Create repository"**
6. Copie a URL que aparecer (algo como: `https://github.com/SEU_USUARIO/mastermind-challenge.git`)

**Volte ao PowerShell:**

```powershell
# Trocar AQUI pela URL que você copiou
git remote add origin https://github.com/SEU_USUARIO/mastermind-challenge.git
git branch -M main
git push -u origin main
```

Pronto! ✅ Seu código está no GitHub

---

## 🛠️ PASSO 3: Deploy Backend no Render (5 min)

### 3.1 - Criar Conta
1. Acesse: https://render.com
2. Clique **"Sign up"**
3. **"Continue with GitHub"**
4. Autorize o Render
5. Pronto! ✅

### 3.2 - Criar Banco de Dados PostgreSQL
1. No Render Dashboard, clique **"New +"** (canto superior esquerdo)
2. Selecione **"PostgreSQL"**
3. Configure:
   - **Name**: `mastermind-db`
   - **Database**: `mastermind_db`
   - **User**: `mastermind_user` (não pode ser "postgres")
   - **Plan**: `Free`
4. Clique **"Create Database"**
5. **AGUARDE CRIAR** (~2 min)
6. Quando estiver pronto, você verá uma **Internal Database URL** (algo em cinza)
7. **COPIE ESSA URL** (você vai usar no próximo passo)

### 3.3 - Deploy do Backend
1. Clique **"New +"** → **"Web Service"**
2. Conecte seu GitHub (selecione `mastermind-challenge`)
3. Configure:
   - **Name**: `mastermind-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python -m alembic upgrade head 2>/dev/null || true`
   - **Start Command**: `gunicorn "app.main:app" --bind 0.0.0.0:$PORT --workers 1`
   - **Plan**: `Free`
4. Clique **"Create Web Service"**

### 3.4 - Adicionar Variáveis de Ambiente
1. Quando o serviço estiver criado, vá em **"Environment"**
2. Clique **"Add Environment Variable"**
3. Adicione estas variáveis:

```
DATABASE_URL = [COLE A URL DO POSTGRESQL AQUI]
SECRET_KEY = mastermind-secret-key-12345678901234567890
ENVIRONMENT = production
BACKEND_URL = https://mastermind-api.onrender.com
```

Para `DATABASE_URL`, cole a URL interna do banco (da etapa 3.2)

### 3.5 - Fazer Deploy
1. Após adicionar as variáveis, o backend vai fazer deploy automaticamente
2. Aguarde até aparecer **"Live"** (verde)
3. Copie a URL: `https://mastermind-api.onrender.com` (você vai precisar)

✅ Backend deployado!

---

## 🎨 PASSO 4: Deploy Frontend no Vercel (5 min)

### 4.1 - Criar Conta
1. Acesse: https://vercel.com/signup
2. **"Continue with GitHub"**
3. Autorize
4. Escolha seu nome de usuário
5. Pronto! ✅

### 4.2 - Fazer Deploy
1. No Vercel Dashboard, clique **"Add New..."** → **"Project"**
2. Selecione seu repositório `mastermind-challenge`
3. Configure:
   - **Framework Preset**: deixe vazio
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Install Command**: `npm install`
4. Clique **"Deploy"**

### 4.3 - Adicionar Variável de Ambiente
1. Aguarde o deploy terminar
2. Vá em **"Settings"** → **"Environment Variables"**
3. Adicione:
   - **Name**: `NG_APP_API_URL`
   - **Value**: `https://mastermind-api.onrender.com/api` (a URL do backend que você copiou)
4. Clique **"Add"**
5. Clique no botão **"Redeploy"** (vai fazer deploy novamente com a variável)

### 4.4 - Aguardar Deploy
Espere aparecer **"Production"** com status verde

Copie a URL final (algo como: `https://mastermind-challenge.vercel.app`)

✅ Frontend deployado!

---

## ✅ PRONTO! 🎉

Você agora tem:

```
🌐 FRONTEND (compartilhe isso):
   https://mastermind-challenge.vercel.app

⚙️ BACKEND:
   https://mastermind-api.onrender.com

📊 API DOCS:
   https://mastermind-api.onrender.com/docs
```

---

## 🧪 Testar a Aplicação

1. Abra: https://mastermind-challenge.vercel.app
2. Clique **"Register"**
3. Crie uma conta
4. Faça login
5. Inicie um jogo
6. Jogue! 🎮

---

## ⚠️ Possíveis Problemas

### "504 Gateway Timeout"
- Backend Render está "dormindo" (inatividade > 15 min)
- **Solução**: Espere 30s e tente novamente (vai acordar)

### Frontend não conecta ao backend
- **Solução**: Volta ao Passo 4.3 e verifica se a URL está correta
- Clica em **"Redeploy"** novamente

### Erro ao fazer login
- **Solução**: Aguarde 1 min (backend estava dormindo)
- Tente novamente

---

## 🎯 Próximas Vezes

Para fazer mudanças no código:

1. Faça as mudanças localmente
2. Git push:
   ```powershell
   git add .
   git commit -m "Descrição das mudanças"
   git push
   ```
3. Backend e Frontend fazem auto-deploy automaticamente! 🚀

---

## 📞 Precisa de Ajuda?

Se algo não funcionar:
1. Verifica se está logado no GitHub/Render/Vercel
2. Tenta fazer o deploy novamente
3. Verifica as variáveis de ambiente (copia/cola certinho)
4. Aguarda ~5 min e tenta de novo

---

**Pronto para começar? Segue o guia acima em ordem!** 🚀
