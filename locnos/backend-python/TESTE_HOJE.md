# 🚀 Teste Rápido - Backend Atual (Inglês)

## ✅ O Que Fazer Agora (Hoje - 24/11/2024)

Você pode **testar o backend funcionando** enquanto preparo a tradução para amanhã!

### 1. Popular o Banco com Dados

```bash
cd backend-python
venv\Scripts\activate
python -m app.seed
```

Isso cria:
- 2 usuários (admin + cliente)
- 4 categorias
- 6 equipamentos

### 2. Iniciar o Servidor

```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 3. Acessar a Documentação

Abra: **http://localhost:8000/docs**

### 4. Testar a API

**Login:**
1. Clique em `POST /api/v1/auth/login`
2. "Try it out"
3. Use:
   ```json
   {
     "email": "admin@locnos.com.br",
     "password": "admin123"
   }
   ```
4. Execute
5. Copie o `access_token`

**Autorizar:**
1. Clique no botão "Authorize" (cadeado verde)
2. Cole o token
3. Click "Authorize"

**Testar Endpoints:**
- GET /api/v1/auth/me - Ver seu perfil
- GET /api/v1/equipment - Listar equipamentos
- POST /api/v1/equipment - Criar equipamento (precisa ser staff+)

---

## 📊 Dados de Teste

| Usuário | Email | Senha | Role |
|---------|-------|-------|------|
| Admin | admin@locnos.com.br | admin123 | super_admin |
| Cliente | joao@email.com | senha123 | customer |

---

## 🗓️ Amanhã (25/11/2024)

Vou implementar a **tradução completa** para português:

✅ **O Que Será Traduzido:**
- Nomes de tabelas (`users` → `usuarios`)
- Colunas (`name` → `nome`, `email` → `email`)
- Código Python (variáveis, funções)
- Comentários
- Mensagens de erro
- Dados de exemplo

⏱️ **Tempo:** ~3 horas  
📋 **Plano:** Ver `implementation_plan.md`

**Por Hoje:** Teste e explore a API funcionando! 🎉

---

## 🐛 Se Der Erro

```bash
# Recriar banco
python -m app.db_init

# Popular novamente
python -m app.seed

# Iniciar servidor
python -m uvicorn app.main:app --reload --port 8000
```

---

**Status:** Backend 100% funcional em inglês  
**Próximo:** Tradução completa para português (amanhã)
