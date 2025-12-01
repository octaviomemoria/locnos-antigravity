# ✅ Checklist de Deploy - Render Backend

## 📋 Status Atual

✅ Arquivos corrigidos e enviados ao GitHub:
- `runtime.txt` - Python 3.11.6
- `requirements.txt` - Pillow 10.4.0
- `build.sh` - Script melhorado

---

## 🎯 Próximos Passos

### 1️⃣ Configurar o Serviço no Render

Acesse o dashboard do Render e configure:

**Configurações Básicas:**
```yaml
Name: locnos-backend
Region: Oregon
Branch: main
Root Directory: locnos/backend-python  ⚠️ CRÍTICO!
```

**Build & Deploy:**
```bash
Build Command: chmod +x build.sh && ./build.sh
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

### 2️⃣ Criar PostgreSQL Database

1. Dashboard Render → **"New +"** → **"PostgreSQL"**
2. Configure:
   ```yaml
   Name: locnos-db
   Database: locnos
   User: locnos
   Region: Oregon (mesma do backend!)
   Plan: Free
   ```
3. Após criar, copie a **Internal Database URL**

---

### 3️⃣ Adicionar Variáveis de Ambiente

No serviço backend, vá em **Environment** e adicione:

#### SECRET_KEY (Obrigatório)
Gere uma chave forte:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Copie o resultado e adicione:
```
Name: SECRET_KEY
Value: <cole_a_chave_gerada>
```

#### DATABASE_URL (Obrigatório)
```
Name: DATABASE_URL
Value: <cole_a_Internal_Database_URL_do_PostgreSQL>
```
Formato: `postgresql://user:pass@host:5432/locnos`

#### Outras Variáveis
```
Name: ALGORITHM
Value: HS256

Name: ACCESS_TOKEN_EXPIRE_MINUTES
Value: 30

Name: CORS_ORIGINS
Value: http://localhost:3000
```

> **Nota:** Atualize `CORS_ORIGINS` depois com a URL do Vercel

---

### 4️⃣ Fazer Deploy

1. Clique em **"Manual Deploy"**
2. Selecione **"Deploy latest commit"**
3. Acompanhe os logs em tempo real

**Logs esperados:**
```bash
🐍 Python version: 3.11.6
📦 Upgrading pip...
🔧 Installing dependencies...
✅ Build completed successfully!
==> Your service is live 🎉
```

---

### 5️⃣ Testar o Backend

Após deploy bem-sucedido:

```bash
# Health check
curl https://seu-servico.onrender.com/health

# Resposta esperada:
{
  "status": "ok",
  "timestamp": "2025-12-01T..."
}
```

---

## 🚨 Troubleshooting

### Erro: "No such file or directory"
✅ **Solução:** Verifique que Root Directory = `locnos/backend-python`

### Erro: "Pillow build failed"
✅ **Solução:** Já corrigido - runtime.txt força Python 3.11.6

### Erro: "Database connection refused"
✅ **Solução:** 
- Use Internal Database URL (não External)
- Backend e database na mesma região (Oregon)

### Erro: "SECRET_KEY not found"
✅ **Solução:** Adicione todas as variáveis de ambiente listadas acima

---

## 📊 URLs Importantes

**Repositório GitHub:**
```
https://github.com/octaviomemoria/locnos-antigravity
```

**Commit com correções:**
```
77f9085 - fix: Add runtime.txt and update dependencies
```

**Render Dashboard:**
```
https://dashboard.render.com/
```

---

## ✅ Checklist Final

Antes de fazer deploy, confirme:

- [ ] Root Directory = `locnos/backend-python`
- [ ] Build Command = `chmod +x build.sh && ./build.sh`
- [ ] Start Command = `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] PostgreSQL criado na mesma região
- [ ] DATABASE_URL configurada (Internal URL)
- [ ] SECRET_KEY gerada e configurada
- [ ] ALGORITHM = HS256
- [ ] ACCESS_TOKEN_EXPIRE_MINUTES = 30
- [ ] CORS_ORIGINS configurado

---

**Depois destes passos, seu backend estará online! 🚀**

Próximo: Configurar Frontend na Vercel
