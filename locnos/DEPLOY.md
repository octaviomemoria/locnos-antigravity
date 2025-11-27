# Deployment Guide - Locnos

Sistema de gestão de locações implantado em produção usando Render (backend) e Vercel (frontend).

## 📦 Estrutura do Projeto

```
locnos/
├── backend-python/          # FastAPI Backend
│   ├── app/
│   ├── build.sh            # Script de build Render
│   └── requirements.txt
├── frontend-nextjs/         # Next.js Frontend
│   ├── app/
│   ├── components/
│   └── package.json
├── render.yaml             # Configuração Render
└── vercel.json             # Configuração Vercel
```

---

## 🚀 Deploy Backend (Render)

### 1. Preparação

Certifique-se de que o arquivo `build.sh` tem permissões de execução:
```bash
cd backend-python
chmod +x build.sh
```

### 2. Criar Serviço no Render

1. Acesse [render.com](https://render.com) e faça login
2. Clique em **"New +"** → **"Web Service"**
3. Conecte seu repositório GitHub
4. Configure:
   - **Name:** `locnos-backend`
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Root Directory:** `backend-python`
   - **Environment:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Variáveis de Ambiente

No dashboard do Render, adicione as seguintes variáveis:

```bash
# Database (auto-gerado pelo Render se criar PostgreSQL)
DATABASE_URL=postgresql://user:pass@host/dbname

# Segurança
SECRET_KEY=<gere uma chave secreta forte>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (adicione o domínio do Vercel)
CORS_ORIGINS=https://seu-app.vercel.app,http://localhost:3000
```

**Gerar SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Criar Banco de Dados PostgreSQL

1. No Render, clique em **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name:** `locnos-db`
   - **Database:** `locnos`
   - **User:** `locnos`
   - **Region:** Oregon (mesma do backend)
3. Após criar, copie a **Internal Database URL**
4. Cole em `DATABASE_URL` no serviço backend

### 5. Deploy

O Render fará deploy automaticamente. Monitore os logs em tempo real.

**URL do backend:** `https://locnos-backend.onrender.com`

---

## 🎨 Deploy Frontend (Vercel)

### 1. Preparação

O arquivo `vercel.json` já está configurado na raiz do projeto.

### 2. Deploy via Vercel Dashboard

1. Acesse [vercel.com](https://vercel.com) e faça login
2. Clique em **"Add New..."** → **"Project"**
3. Importe seu repositório GitHub
4. Configure:
   - **Framework Preset:** Next.js
   - **Root Directory:** `frontend-nextjs`
   - **Build Command:** `npm run build` (auto-detectado)
   - **Output Directory:** `.next` (auto-detectado)

### 3. Variáveis de Ambiente

No dashboard da Vercel, em **Settings** → **Environment Variables**, adicione:

```bash
# URL do backend (substitua pela URL do Render)
NEXT_PUBLIC_API_URL=https://locnos-backend.onrender.com
```

### 4. Deploy

A Vercel fará deploy automaticamente a cada push no GitHub.

**URL do frontend:** `https://locnos.vercel.app`

---

## 🔧 Solução de Problemas

### Render: "builder.sh: No such file or directory"

**Causa:** O arquivo `build.sh` não existe ou não tem permissões.

**Solução:**
```bash
cd backend-python
chmod +x build.sh
git add build.sh
git commit -m "Add build script"
git push
```

### Render: Erro ao conectar ao banco

**Causa:** `DATABASE_URL` incorreta ou banco não criado.

**Solução:**
1. Verifique que o PostgreSQL foi criado
2. Use a **Internal Database URL** (não a External)
3. Formato: `postgresql://user:pass@host:5432/dbname`

### Vercel: 404 NOT_FOUND

**Causa:** Configuração incorreta do `vercel.json` ou `NEXT_PUBLIC_API_URL` não definida.

**Solução:**
1. Verifique que `vercel.json` está na raiz
2. Configure `NEXT_PUBLIC_API_URL` nas variáveis de ambiente
3. Faça redeploy: **Deployments** → **...** → **Redeploy**

### Vercel: Erro de CORS ao chamar API

**Causa:** Backend não permite o domínio do Vercel.

**Solução:**
No Render, atualize `CORS_ORIGINS`:
```bash
CORS_ORIGINS=https://seu-app.vercel.app,https://seu-app-*.vercel.app,http://localhost:3000
```

---

## 📝 Checklist de Deploy

### Backend (Render)
- [ ] `build.sh` criado e com permissões
- [ ] PostgreSQL criado
- [ ] `DATABASE_URL` configurada
- [ ] `SECRET_KEY` gerada e configurada
- [ ] `CORS_ORIGINS` com domínio do Vercel
- [ ] Deploy bem-sucedido
- [ ] Endpoint `/health` retorna 200

### Frontend (Vercel)
- [ ] `vercel.json` na raiz
- [ ] `NEXT_PUBLIC_API_URL` configurada
- [ ] Build bem-sucedido
- [ ] App abrindo sem erro 404
- [ ] Login funcionando

---

## 🔄 Deploy Automático

Ambos os serviços fazem deploy automático:

- **Render:** Deploy a cada push na branch `main`
- **Vercel:** Deploy a cada push (produção) e preview para PRs

---

## 📊 Monitoramento

**Render:**
- Logs em tempo real: Dashboard → Logs
- Métricas: Dashboard → Metrics
- Health checks automáticos

**Vercel:**
- Logs: Deployments → Função → Logs
- Analytics: Dashboard → Analytics
- Monitoring: Dashboard → Speed Insights

---

## 💰 Custos (Plano Free)

**Render Free Tier:**
- 750 horas/mês de web service
- PostgreSQL com 1GB storage
- **Limitação:** serviço "dorme" após 15min inativo

**Vercel Free Tier:**
- Bandwidth ilimitado
- 100GB de build time/mês
- Deploys ilimitados

---

## 🔐 Segurança

### Secrets do Render
Nunca commite:
- `DATABASE_URL`
- `SECRET_KEY`
- Credenciais de API

### Secrets da Vercel
- Use `NEXT_PUBLIC_` apenas para variáveis públicas
- API keys privadas: sem o prefixo `NEXT_PUBLIC_`

---

## 🚨 Comandos Úteis

### Verificar saúde do backend
```bash
curl https://locnos-backend.onrender.com/health
```

### Ver logs do Render (via CLI)
```bash
render logs -s locnos-backend -f
```

### Redeploy manual na Vercel
```bash
vercel --prod
```

---

## 📚 Referências

- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

---

**Deploy realizado com sucesso! 🎉**

Backend: `https://locnos-backend.onrender.com`  
Frontend: `https://locnos.vercel.app`
