# 🚀 Guia de Instalação e Teste - Locnos Python FastAPI

## 📋 Pré-requisitos

- Python 3.11+ instalado
- pip atualizado

## ⚡ Instalação Rápida

### 1. Navegar para a pasta do projeto Python

```bash
cd locnos/backend-python
```

### 2. Criar ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install fastapi uvicorn python-dotenv pydantic pydantic-settings
```

**Nota:** Por enquanto instalamos apenas as dependências essenciais para testar. Depois instalamos tudo com `pip install -r requirements.txt`

### 4. Criar arquivo .env

```bash
copy .env.example .env
```

Ou crie manualmente um arquivo `.env` com:

```env
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
DEBUG=True
SECRET_KEY=sua_chave_secreta_temporaria
DATABASE_URL=postgresql://teste:teste@localhost:5432/teste
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

### 5. Iniciar servidor

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Ou:

```bash
cd ..
python -m uvicorn backend-python.app.main:app --reload --port 8000
```

## ✅ Testar a API

### Via Navegador

Acesse: **http://localhost:8000**

Verá:
```json
{
  "message": "Bem-vindo à API Locnos!",
  "docs": "/docs",
  "version": "1.0.0",
  "status": "online"
}
```

### Documentação Interativa (Swagger)

Acesse: **http://localhost:8000/docs**

- 📚 Documentação automática gerada pelo FastAPI
- 🧪 Teste endpoints direto no navegador
- 📝 Veja todos os parâmetros e respostas

### Health Check

Acesse: **http://localhost:8000/health**

```json
{
  "status": "healthy",
  "service": "Locnos API",
  "version": "1.0.0",
  "timestamp": "2024-11-24T20:46:00",
  "environment": "development"
}
```

### Endpoint de Teste

Acesse: **http://localhost:8000/api/v1/test**

```json
{
  "message": "API FastAPI funcionando perfeitamente! 🚀",
  "framework": "FastAPI",
  "language": "Python 3.11+",
  "database": "Supabase (PostgreSQL)",
  "features": [...]
}
```

## 🎯 Próximos Passos Após Testar

1. ✅ API básica funcionando
2. ⏳ Instalar todas as dependências: `pip install -r requirements.txt`
3. ⏳ Conectar ao Supabase (configurar DATABASE_URL)
4. ⏳ Criar models SQLAlchemy
5. ⏳ Implementar endpoints de autenticação
6. ⏳ Implementar CRUD de equipamentos

## 🐛 Problemas Comuns

### ModuleNotFoundError

```bash
pip install fastapi uvicorn python-dotenv pydantic pydantic-settings
```

### Porta em uso

Mude no `.env`:
```env
PORT=8001
```

E execute:
```bash
python -m uvicorn app.main:app --reload --port 8001
```

### Import Error

Certifique-se de estar na pasta `backend-python` ao executar o uvicorn.

---

## 📊 Status Atual

**Funcional:**
- ✅ Servidor FastAPI rodando
- ✅ Health check
- ✅ Documentação automática (Swagger)
- ✅ CORS configurado
- ✅ Tratamento de erros

**Pendente:**
- ⏳ Conexão com banco de dados
- ⏳ Models (User, Equipment, etc)
- ⏳ Autenticação JWT
- ⏳ Endpoints de negócio

**Você já pode ver o FastAPI funcionando e a documentação automática! 🚀**
