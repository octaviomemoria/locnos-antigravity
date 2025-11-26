# 🚀 Locnos Backend Python FastAPI - Guia Completo

## ✅ Backend 100% Implementado!

Sistema completo de gestão de locadoras com Python FastAPI + Supabase PostgreSQL.

---

## 📋 O Que Foi Implementado

### 🗄️ **Database (SQLAlchemy Models)**
- ✅ `User` - Usuários com roles (customer, staff, admin, super_admin)
- ✅ `Equipment` - Equipamentos com pricing e controle de estoque
- ✅ `Category` - Categorias hierárquicas

### 📝 **Schemas Pydantic (Validação)**
- ✅ Auth (login, register, tokens)
- ✅ User (CRUD completo)
- ✅ Equipment (CRUD + paginação)

### 🔐 **Autenticação & Segurança**
- ✅ JWT access + refresh tokens
- ✅ Password hashing (bcrypt)
- ✅ Role-based access control (RBAC)
- ✅ Permission checking
- ✅ Protected routes

### 🌐 **API Endpoints (10+)**

**Autenticação (`/api/v1/auth`):**
- `POST /register` - Registrar usuário
- `POST /login` - Login com JWT
- `GET /me` - Obter perfil
- `PUT /change-password` - Alterar senha

**Equipamentos (`/api/v1/equipment`):**
- `GET /` - Listar (paginado, com filtros)
- `GET /{id}` - Detalhes
- `POST /` - Criar (staff+)
- `PUT /{id}` - Atualizar (staff+)
- `DELETE /{id}` - Deletar soft (staff+)

---

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
cd backend-python

# Ativar ambiente virtual
venv\Scripts\activate

# Instalar TODAS as dependências
pip install -r requirements.txt
```

### 2. Configurar Supabase

Edite `.env` e adicione sua URL do Supabase:

```env
DATABASE_URL=postgresql://postgres:SUA_SENHA@SEU_PROJETO.supabase.co:5432/postgres
```

### 3. Criar Tabelas no Banco

```bash
# Opção 1: Via SQLAlchemy
python -m app.db_init

# Opção 2: Instalar Alembic (migrations)
# alembic init alembic
# alembic revision --autogenerate -m "initial"
# alembic upgrade head
```

### 4. Popular Banco com Dados de Teste

```bash
python -m app.seed
```

Isso cria:
- 2 usuários (admin + cliente)
- 4 categorias
- 6 equipamentos

### 5. Iniciar Servidor

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Ou:

```bash
# Se estiver na pasta raiz do projeto
cd ..
python -m uvicorn backend-python.app.main:app --reload --port 8000
```

---

## 🧪 Testar a API

### Via Swagger UI (Recomendado)

Acesse: **http://localhost:8000/docs**

1. **Login:**
   - Clique em `POST /api/v1/auth/login`
   - "Try it out"
   - Use: `admin@locnos.com.br` / `admin123`
   - Execute
   - Copie o `access_token` da resposta

2. **Autorizar:**
   - Clique no botão "Authorize" (cadeado verde no topo)
   - Cole o token
   - Clique "Authorize"

3. **Testar Endpoints Protegidos:**
   - Agora pode testar `GET /api/v1/auth/me`
   - Criar equipamentos `POST /api/v1/equipment`
   - Etc.

### Via cURL

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@locnos.com.br","password":"admin123"}'

# Salve o token retornado
TOKEN="seu_access_token_aqui"

# Listar equipamentos (público)
curl http://localhost:8000/api/v1/equipment

# Obter perfil (protegido)
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"

# Criar equipamento (requer staff+)
curl -X POST http://localhost:8000/api/v1/equipment \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Furadeira Profissional",
    "description": "Furadeira de impacto 1000W",
    "category_id": "COLE_ID_CATEGORIA_AQUI",
    "internal_code": "EQ000007",
    "daily_rate": 35.00
  }'
```

---

## 📊 Credenciais de Teste

| Tipo | Email | Senha | Role |
|------|-------|-------|------|
| Admin | admin@locnos.com.br | admin123 | super_admin |
| Cliente | joao@email.com | senha123 | customer |

---## 🔧 Estrutura do Projeto

```
backend-python/
├── app/
│   ├── core/
│   │   ├── config.py          # Configurações
│   │   ├── database.py        # SQLAlchemy
│   │   └── security.py        # JWT + bcrypt
│   ├── models/
│   │   ├── user.py            # Model User
│   │   ├── equipment.py       # Model Equipment
│   │   └── category.py        # Model Category
│   ├── schemas/
│   │   ├── auth.py            # Schemas autenticação
│   │   ├── user.py            # Schemas user
│   │   └── equipment.py       # Schemas equipment
│   ├── api/
│   │   ├── deps.py            # Dependencies (auth)
│   │   └── v1/
│   │       ├── auth.py        # Router auth
│   │       └── equipment.py   # Router equipment
│   ├── main.py                # FastAPI app
│   ├── db_init.py             # Criar tabelas
│   └── seed.py                # Popular banco
├── requirements.txt            # Dependências
├── .env                        # Variáveis ambiente
└── TESTE_COMPLETO.md          # Este arquivo
```

---

## 🎯 Endpoints Disponíveis

### Públicos (sem autenticação)

- `GET /` - Boas-vindas
- `GET /health` - Health check
- `GET /docs` - Documentação Swagger
- `GET /api/v1/equipment` - Listar equipamentos
- `GET /api/v1/equipment/{id}` - Detalhes equipamento
- `POST /api/v1/auth/register` - Registrar cliente
- `POST /api/v1/auth/login` - Login

### Protegidos (requer autenticação)

- `GET /api/v1/auth/me` - Meu perfil
- `PUT /api/v1/auth/change-password` - Alterar senha

### Staff/Admin Apenas

- `POST /api/v1/equipment` - Criar equipamento
- `PUT /api/v1/equipment/{id}` - Atualizar equipamento
- `DELETE /api/v1/equipment/{id}` - Deletar equipamento

---

## 🚨 Troubleshooting

### Erro: "ModuleNotFoundError"

```bash
pip install -r requirements.txt
```

### Erro: "Connection refused" (banco)

Verifique se a `DATABASE_URL` no `.env` está correta.

### Erro ao criar tabelas

```bash
# Deletar e recriar
python -m app.db_init
python -m app.seed
```

### Servidor não inicia

```bash
# Certifique-se que está na pasta correta
cd backend-python

# Ative o venv
venv\Scripts\activate

# Tente novamente
python -m uvicorn app.main:app --reload
```

---

## 📈 Próximos Passos

1. ✅ **Backend completo**
2. ⏳ Implementar Contracts e Payments
3. ⏳ Frontend Admin (Next.js)
4. ⏳ Frontend Cliente (Next.js)
5. ⏳ Deploy (Vercel + Supabase)

---

## 🎓 Stack Tecnológica

- **Framework:** FastAPI 0.108
- **ORM:** SQLAlchemy 2.0
- **Database:** Supabase (PostgreSQL)
- **Validação:** Pydantic 2.5
- **Auth:** python-jose (JWT)
- **Password:** passlib (bcrypt)
- **Docs:** OpenAPI 3.1 (Swagger)

---

**Backend Python FastAPI 100% Funcional! 🎉**
