# 🎨 Deploy Frontend Vercel - Guia Completo

Este guia mostra como fazer deploy do frontend Next.js na Vercel.

---

## 🎯 Por que Vercel?

✅ **Otimizado para Next.js** (criadores do framework)  
✅ **Deploy automático** a cada push  
✅ **CDN global** (ultra rápido)  
✅ **SSL automático** (HTTPS grátis)  
✅ **Preview deployments** para cada PR  
✅ **Free tier generoso**

---

## 📋 Passo 1: Preparar Repositório

### 1.1 Verificar Estrutura

Confirme que seu repositório tem:

```
locnos-antigravity/
└── locnos/
    └── frontend-nextjs/   ← Aqui está o Next.js
        ├── app/
        ├── components/
        ├── lib/
        ├── package.json   ← Importante!
        └── next.config.js
```

### 1.2 Commit Final

```bash
cd locnos
git add .
git commit -m "chore: Prepare for Vercel deployment"
git push origin main
```

---

## 🚀 Passo 2: Importar Projeto na Vercel

### 2.1 Criar Conta

1. Acesse [vercel.com](https://vercel.com)
2. Clique em **"Sign Up"**
3. **Login com GitHub** (recomendado)
4. Autorize a Vercel no GitHub

### 2.2 Importar Repositório

1. No dashboard Vercel, clique em **"Add New..."** → **"Project"**
2. Na lista, encontre: **`octaviomemoria/locnos-antigravity`**
3. Clique em **"Import"**

---

## ⚙️ Passo 3: Configurar Build

### 3.1 Configurações do Projeto

**IMPORTANTE:** Configure estas opções:

```yaml
Framework Preset: Next.js
Root Directory: locnos/frontend-nextjs  ⚠️ CRÍTICO!
Build Command: npm run build (auto-detectado)
Output Directory: .next (auto-detectado)
Install Command: npm install (auto-detectado)
Node.js Version: 20.x (recomendado)
```

### 3.2 Setar Root Directory

1. Clique em **"Edit"** ao lado de Root Directory
2. Digite: `locnos/frontend-nextjs`
3. Confirme

---

## 🔐 Passo 4: Variáveis de Ambiente

### 4.1 Adicionar NEXT_PUBLIC_API_URL

1. Role até **"Environment Variables"**
2. Clique em **"Add"**
3. Configure:

```bash
Name: NEXT_PUBLIC_API_URL
Value: https://locnos-antigravity.onrender.com
```

4. **Selecione TODOS os ambientes:**
   - ✅ Production
   - ✅ Preview  
   - ✅ Development

5. Clique em **"Add"**

### 4.2 Variáveis Opcionais (se usar)

```bash
# Se usar Supabase no frontend
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<sua_chave_publica>
```

---

## 🎉 Passo 5: Deploy!

### 5.1 Iniciar Deploy

1. Revise todas configurações
2. Clique em **"Deploy"**
3. ⏱️ Aguarde build (2-4 minutos)

### 5.2 Acompanhar Build

Você verá:

```
▲ Vercel
Building...
  ✓ Linting and checking validity of types
  ✓ Creating an optimized production build
  ✓ Compiling Client Components
  ✓ Collecting page data
  ✓ Generating static pages (5/5)
  ✓ Finalizing page optimization

✅ Build completed successfully
```

### 5.3 Deploy Concluído!

Quando finalizar, você verá:

```
🎉 Your project has been deployed!

https://locnos.vercel.app
```

---

## 🧪 Passo 6: Testar Frontend

### 6.1 Acessar Site

Abra a URL fornecida (ex: `https://locnos.vercel.app`)

**Deve aparecer:**
- ✅ Página de login
- ✅ Sem erro 404
- ✅ Estilos carregando

### 6.2 Testar API Connection

Abra o console do navegador (F12) e veja se:

```javascript
// Deve aparecer a URL correta
console.log(process.env.NEXT_PUBLIC_API_URL)
// → https://locnos-antigravity.onrender.com
```

### 6.3 Testar Login

1. Tente fazer login
2. Se der erro de CORS → Vá para Passo 7

---

## 🔧 Passo 7: Configurar CORS no Backend

### 7.1 Atualizar CORS_ORIGINS no Render

1. Vá para o dashboard do Render
2. Seu serviço → **Environment**
3. Edite `CORS_ORIGINS`:

```bash
CORS_ORIGINS=https://locnos.vercel.app,https://locnos-*.vercel.app,http://localhost:3000
```

**Nota:** Substitua `locnos` pelo nome real do seu app Vercel

### 7.2 Redeploy Backend

1. No Render: **Manual Deploy** → **"Deploy latest commit"**
2. Aguarde ~2 minutos

### 7.3 Testar Novamente

Volte ao frontend e teste o login. Deve funcionar! 🎉

---

## 🌐 Passo 8: Custom Domain (Opcional)

### 8.1 Adicionar Domínio Próprio

Se você tem um domínio (ex: `locnos.com.br`):

1. No Vercel, vá em **Settings** → **Domains**
2. Clique em **"Add"**
3. Digite seu domínio: `locnos.com.br`
4. Siga instruções para configurar DNS

### 8.2 Atualizar CORS

Adicione seu domínio ao `CORS_ORIGINS`:

```bash
CORS_ORIGINS=https://locnos.com.br,https://locnos.vercel.app,http://localhost:3000
```

---

## 🔄 Passo 9: Deploy Automático

### 9.1 Como Funciona

A partir de agora:

1. **Push para `main`** → Deploy automático em produção
2. **Push para outras branches** → Deploy de preview
3. **Pull Requests** → Deploy de preview com URL única

### 9.2 Ver Deployments

No dashboard Vercel:
- **Deployments** → Lista de todos os deploys
- Cada deploy tem URL única
- Pode comparar versões

### 9.3 Rollback

Se algo der errado:

1. **Deployments** → Selecione deploy anterior
2. **...** → **"Promote to Production"**

---

## 📊 Passo 10: Analytics e Monitoring

### 10.1 Vercel Analytics

Habilite analytics gratuito:

1. Settings → **Analytics**
2. Clique em **"Enable"**

**Métricas disponíveis:**
- 📊 Page views
- ⚡ Performance score
- 🌍 Geographic distribution
- 📱 Device breakdown

### 10.2 Speed Insights

1. Settings → **Speed Insights**
2. Clique em **"Enable"**

Mostra performance real dos usuários (Core Web Vitals)

---

## 🚨 Troubleshooting

### Erro: 404 NOT_FOUND

**Causa:** Root Directory incorreto

**Solução:**
1. Settings → General → **Root Directory**
2. Altere para: `locnos/frontend-nextjs`
3. Redeploy

---

### Erro: NEXT_PUBLIC_API_URL is undefined

**Causa:** Variável não configurada

**Solução:**
1. Settings → **Environment Variables**
2. Adicione `NEXT_PUBLIC_API_URL` para **TODOS** ambientes
3. Redeploy

---

### Erro: CORS policy

**Causa:** Backend não permite domínio Vercel

**Solução:**
No Render, atualize `CORS_ORIGINS`:
```bash
CORS_ORIGINS=https://seu-app.vercel.app,https://seu-app-*.vercel.app
```

---

### Build falha: Module not found

**Causa:** Dependência faltando ou import incorreto

**Solução:**
1. Verifique `package.json`
2. Veja logs de build para detalhes
3. Corrija localmente e push

---

## 💡 Dicas de Performance

### 1. Image Optimization

Use o componente `Image` do Next.js:

```jsx
import Image from 'next/image'

<Image 
  src="/logo.png" 
  width={200} 
  height={100}
  alt="Logo"
/>
```

### 2. Lazy Loading

```jsx
import dynamic from 'next/dynamic'

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>
})
```

### 3. API Route Caching

```javascript
// app/api/data/route.js
export const revalidate = 60 // Revalidate a cada 60s

export async function GET() {
  const data = await fetchData()
  return Response.json(data)
}
```

---

## 📈 Limites Free Tier

| Recurso | Limite Gratuito |
|---------|----------------|
| Bandwidth | 100 GB/mês |
| Build Time | 6000 min/mês |
| Deployments | Ilimitado |
| Serverless Functions | 100 GB-Hours |
| Team Members | 1 |

💡 **Upgrade:** $20/mês por membro para times

---

## ✅ Checklist Final

### Configuração
- [ ] Repositório no GitHub
- [ ] Projeto importado na Vercel
- [ ] Root Directory: `locnos/frontend-nextjs`
- [ ] `NEXT_PUBLIC_API_URL` configurada (todos ambientes)
- [ ] Deploy bem-sucedido

### Teste
- [ ] Site acessível (sem 404)
- [ ] Página de login aparecendo
- [ ] Console sem erros
- [ ] API URL correta (F12 → Console)

### Integração
- [ ] CORS atualizado no Render
- [ ] Login funcionando
- [ ] Chamadas API funcionando

### Opcional
- [ ] Analytics habilitado
- [ ] Speed Insights habilitado
- [ ] Custom domain configurado

---

## 🎊 URLs Finais

**Frontend:** `https://seu-app.vercel.app`  
**Backend:** `https://locnos-antigravity.onrender.com`  
**Database:** Supabase

---

**Frontend deployado! Sistema completo online! 🚀**
