# 🎨 Guia de Deploy - Vercel Frontend

## 📋 Pré-requisitos

✅ Backend Render já deve estar funcionando
✅ URL do backend: `https://seu-backend.onrender.com`

---

## 🚀 Passos para Deploy

### 1️⃣ Importar Projeto na Vercel

1. Acesse [vercel.com](https://vercel.com)
2. Faça login com GitHub
3. Clique em **"Add New..."** → **"Project"**
4. Selecione o repositório: `octaviomemoria/locnos-antigravity`

---

### 2️⃣ Configurar o Build

**Configure Overrides:**

```yaml
Framework Preset: Next.js (auto-detectado)
Root Directory: locnos/frontend-nextjs  ⚠️ IMPORTANTE!
Build Command: npm run build (auto)
Output Directory: .next (auto)
Install Command: npm install (auto)
Node.js Version: 20.x (recomendado)
```

> **CRÍTICO:** O Root Directory DEVE ser `locnos/frontend-nextjs`

---

### 3️⃣ Adicionar Variável de Ambiente

Em **Environment Variables**, clique em **"Add New"**:

```bash
Key: NEXT_PUBLIC_API_URL
Value: https://seu-backend.onrender.com
```

⚠️ **IMPORTANTE:** 
- Adicione para **Production**, **Preview** e **Development**
- Substitua `seu-backend.onrender.com` pela URL real do Render

---

### 4️⃣ Fazer Deploy

1. Clique em **"Deploy"**
2. Aguarde o build (2-3 minutos)
3. Vercel mostrará a URL do site quando finalizar

---

### 5️⃣ Testar o Frontend

Acesse a URL fornecida pela Vercel:

```
https://seu-app.vercel.app
```

**O que você deve ver:**
- ✅ Página de login
- ✅ Sem erros 404
- ✅ Formulário de login funcionando

---

### 6️⃣ Atualizar CORS no Backend

Agora que o frontend está no ar, atualize o CORS no Render:

1. Vá para o serviço backend no Render
2. **Environment** → Edite `CORS_ORIGINS`
3. Atualize para:

```bash
CORS_ORIGINS=https://seu-app.vercel.app,https://seu-app-*.vercel.app,http://localhost:3000
```

4. Salve e redeploy o backend

---

## 🔧 Troubleshooting

### Erro: 404 NOT_FOUND

**Causa:** Root Directory incorreto

**Solução:**
1. Settings → General → Root Directory
2. Altere para: `locnos/frontend-nextjs`
3. Redeploy

---

### Erro: "NEXT_PUBLIC_API_URL is not defined"

**Causa:** Variável não configurada corretamente

**Solução:**
1. Settings → Environment Variables
2. Adicione `NEXT_PUBLIC_API_URL` para todos os ambientes
3. Redeploy

---

### Erro: CORS ao fazer login

**Causa:** Backend não permite o domínio do Vercel

**Solução:**
1. No Render, atualize `CORS_ORIGINS` (passo 6)
2. Redeploy backend

---

### Build falha: "Module not found"

**Causa:** Dependências não instaladas

**Solução:**
1. Verifique que `package.json` existe em `locnos/frontend-nextjs`
2. Clear build cache e redeploy:
   - Deployments → ... → Redeploy

---

## ✅ Checklist Final

- [ ] Projeto importado do GitHub
- [ ] Root Directory = `locnos/frontend-nextjs`
- [ ] `NEXT_PUBLIC_API_URL` configurada (todos ambientes)
- [ ] Build bem-sucedido
- [ ] Site acessível sem 404
- [ ] CORS atualizado no backend
- [ ] Login funcionando

---

## 🎉 Deploy Completo!

Você terá:

**Backend (Render):**
```
https://locnos-backend.onrender.com
```

**Frontend (Vercel):**
```
https://seu-app.vercel.app
```

**Sistema completo funcionando em produção! 🚀**

---

## 📊 Próximos Passos (Opcional)

1. **Custom Domain:** Adicionar domínio próprio na Vercel
2. **Analytics:** Ativar Vercel Analytics
3. **Monitoring:** Configurar alertas de erro
4. **SSL:** Já incluído automaticamente (Vercel + Render)

---

**Precisando de ajuda? Consulte os logs de deploy!**
