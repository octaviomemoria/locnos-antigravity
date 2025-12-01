# 📝 Quick Reference - Deploy Commands

## 🔑 Gerar SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🧪 Testar Backend Local

```bash
cd backend-python
pip install -r requirements-production.txt
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000/docs

## 🧪 Testar Frontend Local

```bash
cd frontend-nextjs
npm install
npm run dev
```

Acesse: http://localhost:3000

## 📊 Verificar Deploy

### Backend (Render)

```bash
# Health check
curl https://SEU-APP.onrender.com/health

# API Docs
https://SEU-APP.onrender.com/docs

# Test login
curl -X POST https://SEU-APP.onrender.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"senha123"}'
```

### Frontend (Vercel)

```bash
# Abrir no navegador
https://SEU-APP.vercel.app

# Verificar variável
console.log(process.env.NEXT_PUBLIC_API_URL)
```

## 🔧 Comandos Git Úteis

```bash
# Status
git status

# Ver último commit
git log -1

# Ver mudanças
git diff

# Push
git push origin main
```

## 📦 Estrutura de Diretórios

```
Root Directory Render:  locnos/backend-python
Root Directory Vercel:  locnos/frontend-nextjs
```

## ⚡ Variáveis de Ambiente

### Render (Backend)
```bash
SECRET_KEY=<usar comando acima>
DATABASE_URL=<Internal Database URL>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://seu-app.vercel.app,http://localhost:3000
```

### Vercel (Frontend)
```bash
NEXT_PUBLIC_API_URL=https://seu-backend.onrender.com
```

## 🚀 Deploy Rápido

1. ✅ Configure Root Directory no Render e Vercel
2. ✅ Adicione variáveis de ambiente
3. ✅ Clique em Deploy
4. ✅ Aguarde build (~3-5 min)
5. ✅ Teste os endpoints

---

**Guias completos:**
- RENDER_CHECKLIST.md
- VERCEL_SETUP.md
