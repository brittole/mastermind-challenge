# 🎮 RODAR LOCALMENTE - PASSO A PASSO

## ⏱️ Tempo Total: ~5 minutos

---

## 📋 PRÉ-REQUISITOS

- PostgreSQL 15 rodando na máquina
- Node.js 18+ instalado
- Python 3.11+ instalado

---

## 🚀 PASSO 1: Iniciar PostgreSQL

**No Windows**, abra **Services** (pressione `Win + R`, digite `services.msc`):
- Procure por `PostgreSQL`
- Clique direito → **Start** (se não estiver rodando)

**OU use PowerShell** (se instalou via `pg_ctl`):
```powershell
# Achar a instalação do PostgreSQL
cd "C:\Program Files\PostgreSQL\15\bin"
.\pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start
```

✅ PostgreSQL deve estar em `localhost:5432`

---

## ⚙️ PASSO 2: Iniciar Backend

Abra um **PowerShell** e execute:

```powershell
cd c:\Users\Leticia\projetos\mastermind-challenge\backend
python wsgi.py
```

Espere aparecer:
```
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

✅ Backend rodando em `http://localhost:8080`

---

## 🌐 PASSO 3: Iniciar Frontend

Abra **OUTRO PowerShell** e execute:

```powershell
cd c:\Users\Leticia\projetos\mastermind-challenge\frontend
npm start -- --poll 2000
```

Espere aparecer:
```
✔ Compiled successfully.
```

✅ Frontend rodando em `http://localhost:4200`

---

## 🎮 PRONTO! JOGUE AGORA

1. Abra o navegador: **http://localhost:4200**
2. Clique em **"Register"**
3. Crie uma conta
4. Faça login
5. Inicie um jogo e jogue! 🎉

---

## 📊 URLs úteis:

- **Jogo**: http://localhost:4200
- **API**: http://localhost:8080/api
- **Swagger Docs**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

---

## ⚠️ TROUBLESHOOTING

### Erro: "Connection refused" no backend
- PostgreSQL não está rodando
- **Solução**: Inicie o PostgreSQL (Passo 1)

### Erro: "Port 8080 already in use"
- Outro processo está usando a porta
- **Solução**: 
```powershell
netstat -ano | findstr :8080
taskkill /PID xxxxx /F  # xxxxx = PID do processo
```

### Erro: "npm not found"
- Node.js não está instalado
- **Solução**: Baixe em https://nodejs.org

### Erro: "python not found"
- Python não está no PATH
- **Solução**: Reinstale Python marcando "Add to PATH"

### Frontend não conecta ao backend
- **Solução**: Verifica se backend está rodando em 8080
- Se não funcionar, reinicia tudo

---

## 🎯 CTRL+C para parar

Para parar cada serviço, pressione `CTRL+C` no PowerShell correspondente.

---

**Tudo pronto? Boa sorte! 🚀**
