# 🚀 Guia Rápido de Deploy - Configuração Correta

> **Estrutura do repositório:** Os arquivos estão em `locnos/` dentro do repositório.

---

## 📋 Configuração Render (Backend)

### 1. Criar Web Service

1. Acesse [render.com](https://render.com) → **New +** → **Web Service**
2. Conecte o repositório: `octaviomemoria/locnos-antigravity`

### 2. Configurações do Serviço

```yaml
Name: locnos-backend
Region: Oregon
Branch: main
Root Directory: locnos/backend-python  ⚠️ IMPORTANTE!
Environment: Python 3.11
Build Command: ./build.sh
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 3. Variáveis de Ambiente

```bash
# Gere uma chave secreta forte
SECRET_KEY=<execute: python -c "import secrets; print(secrets.token_urlsafe(32))">

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database - será preenchido após criar PostgreSQL
DATABASE_URL=postgresql://user:pass@host:5432/locnos

# CORS - adicione depois o domínio do Vercel
CORS_ORIGINS=http://localhost:3000
```

### 4. Criar PostgreSQL

1. **New +** → **PostgreSQL**
2. Configurar:
   - Name: `locnos-db`
   - Database: `locnos`
   - Region: Oregon (mesma do backend)
3. Após criar, copie a **Internal Database URL**
4. Cole em `DATABASE_URL` no web service

---

## 📋 Configuração Vercel (Frontend)

### 1. Importar Projeto

1. Acesse [vercel.com](https://vercel.com) → **Add New...** → **Project**
2. Importe: `octaviomemoria/locnos-antigravity`

### 2. Configurações do Build

```yaml
Framework Preset: Next.js
Root Directory: locnos/frontend-nextjs  ⚠️ IMPORTANTE!
Build Command: npm run build (auto)
Output Directory: .next (auto)
Install Command: npm install (auto)
```

### 3. Variável de Ambiente

Em **Environment Variables**, adicione:

```bash
# Substitua pela URL do Render
NEXT_PUBLIC_API_URL=https://locnos-backend.onrender.com
```

**Importante:** Adicione para **Production**, **Preview** e **Development**.

---

## ✅ Verificação Pós-Deploy

### Backend (Render)

```bash
# Health check
curl https://locnos-backend.onrender.com/health

# Resposta esperada:
{"status":"ok","timestamp":"..."}
```

### Frontend (Vercel)

1. Acesse a URL fornecida pela Vercel
2. Deve aparecer a página de login
3. Não deve haver erro 404

---

## 🔧 Atualizar CORS

Após deploy do frontend, atualize no Render:

```bash
CORS_ORIGINS=https://seu-app.vercel.app,http://localhost:3000
```

Redeploy o backend para aplicar.

---

## 📊 Resumo das Configurações

| Serviço | Root Directory | URL Exemplo |
|---------|---------------|-------------|
| **Render** | `locnos/backend-python` | `https://locnos-backend.onrender.com` |
| **Vercel** | `locnos/frontend-nextjs` | `https://locnos.vercel.app` |

---

**Pronto para deploy! 🎉**
