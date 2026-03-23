#!/bin/bash
# Script para preparar deploy

echo "🚀 Preparando Mastermind Challenge para Deploy..."

# 1. Verificar se está em um repositório Git
if [ ! -d ".git" ]; then
    echo "📌 Inicializando repositório Git..."
    git init
    echo "mastermind-venv/" > .gitignore
    echo ".venv/" >> .gitignore
    echo "*.pyc" >> .gitignore
    echo ".env" >> .gitignore
    echo "node_modules/" >> .gitignore
    echo "dist/" >> .gitignore
    git add .
    git commit -m "Initial commit - Mastermind Challenge"
fi

# 2. Verificar requirements.txt
echo "✅ Verificando requirements.txt..."
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Arquivo requirements.txt não encontrado!"
    exit 1
fi

# 3. Mostrar instruções
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ PRÓXIMOS PASSOS PARA DEPLOY"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "1️⃣  PUSH PARA GITHUB:"
echo "   git remote add origin https://github.com/SEU_USUARIO/mastermind-challenge.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "2️⃣  DEPLOY BACKEND NO RENDER:"
echo "   - Acesse: https://render.com"
echo "   - Clique 'New+' → 'Web Service'"
echo "   - Conecte seu repositório GitHub"
echo "   - Build: pip install -r requirements.txt"
echo "   - Start: python wsgi.py"
echo "   - Copie a URL gerada (ex: https://mastermind-backend.onrender.com)"
echo ""
echo "3️⃣  CRIAR POSTGRESQL NO RENDER:"
echo "   - Clique 'New+' → 'PostgreSQL'"
echo "   - Copie DATABASE_URL"
echo "   - Adicione no Web Service (Environment Variables)"
echo ""
echo "4️⃣  DEPLOY FRONTEND NO VERCEL:"
echo "   - Acesse: https://vercel.com"
echo "   - Conecte seu GitHub"
echo "   - Selecione repositório"
echo "   - Root Dir: frontend"
echo "   - Build: npm run build"
echo "   - Adicione env var: NG_APP_API_URL=https://SEU-BACKEND.onrender.com/api"
echo ""
echo "5️⃣  TESTE:"
echo "   - Frontend: https://seu-frontend.vercel.app"
echo "   - API Docs: https://seu-backend.onrender.com/docs"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "📖 Para mais detalhes, veja: DEPLOY.md"
