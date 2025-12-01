# 🗄️ Configuração Supabase - Guia Completo

Este guia mostra como configurar o Supabase como database para o backend Locnos.

---

## 🎯 Por que Supabase?

✅ **PostgreSQL na nuvem** (gratuito até 500MB)  
✅ **Interface web** para gerenciar dados  
✅ **APIs automáticas** (REST, GraphQL, Realtime)  
✅ **Backups automáticos**  
✅ **Autenticação integrada**

---

## 📋 Passo 1: Criar Conta e Projeto

### 1.1 Criar Conta

1. Acesse [supabase.com](https://supabase.com)
2. Clique em **"Start your project"**
3. Faça login com GitHub

### 1.2 Criar Novo Projeto

1. Clique em **"New Project"**
2. Configure:
   ```yaml
   Name: locnos-db
   Database Password: <crie uma senha forte>
   Region: South America (São Paulo)
   Plan: Free
   ```
3. Clique em **"Create new project"**
4. ⏱️ Aguarde ~2 minutos (criação do database)

---

## 🔑 Passo 2: Obter Credenciais

### 2.1 Database URL

1. No projeto Supabase, vá em **Settings** (⚙️) → **Database**
2. Role até **"Connection string"**
3. Selecione **"URI"**
4. Copie a URL que aparece:

```
postgresql://postgres:[SEU-PASSWORD]@db.xxx.supabase.co:5432/postgres
```

5. **Substitua** `[SEU-PASSWORD]` pela senha que você criou

**Exemplo:**
```
postgresql://postgres:MinhaSenh@123@db.abc123.supabase.co:5432/postgres
```

### 2.2 API Keys

1. Vá em **Settings** → **API**
2. Copie:
   - **Project URL:** `https://xxx.supabase.co`
   - **anon public key:** (chave pública)
   - **service_role key:** (chave privada - SECRETA!)

---

## 🔧 Passo 3: Configurar no Render

### 3.1 Atualizar Variáveis de Ambiente

No Render Dashboard → Seu serviço → **Environment**:

**Edite estas variáveis:**

```bash
# Database - ATUALIZAR
DATABASE_URL=postgresql://postgres:SUA_SENHA@db.xxx.supabase.co:5432/postgres

# Supabase - ADICIONAR (se usar features do Supabase)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=<anon_public_key>
SUPABASE_SERVICE_KEY=<service_role_key>
```

### 3.2 Redeploy

1. Clique em **"Manual Deploy"** → **"Deploy latest commit"**
2. Aguarde o deploy (~2-3 minutos)

---

## 📊 Passo 4: Criar Tabelas (Schema)

### Opção A: Via SQL Editor (Interface Web)

1. No Supabase, vá em **SQL Editor**
2. Clique em **"+ New query"**
3. Cole o SQL abaixo
4. Clique em **"Run"**

```sql
-- Criar tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    role VARCHAR(50) DEFAULT 'user',
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar tabela de categorias
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    color VARCHAR(20),
    icon VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar tabela de equipamentos
CREATE TABLE IF NOT EXISTS equipment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    code VARCHAR(100) UNIQUE,
    brand VARCHAR(100),
    model VARCHAR(100),
    category_id UUID REFERENCES categories(id),
    quantity INTEGER DEFAULT 1,
    unit_value DECIMAL(10,2),
    status VARCHAR(50) DEFAULT 'available',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar tabela de pessoas
CREATE TABLE IF NOT EXISTS persons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    types TEXT[] NOT NULL,
    full_name VARCHAR(200),
    company_name VARCHAR(200),
    cpf VARCHAR(14),
    cnpj VARCHAR(18),
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índices para performance
CREATE INDEX idx_equipment_status ON equipment(status);
CREATE INDEX idx_equipment_category ON equipment(category_id);
CREATE INDEX idx_persons_types ON persons USING GIN(types);
CREATE INDEX idx_users_email ON users(email);

-- Dados iniciais
INSERT INTO users (email, hashed_password, full_name, role) VALUES
('admin@locnos.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Lw7KxN8', 'Admin Locnos', 'admin')
ON CONFLICT (email) DO NOTHING;

INSERT INTO categories (name, description, color, icon) VALUES
('Ferramentas', 'Ferramentas manuais e elétricas', '#3B82F6', 'tool'),
('Equipamentos', 'Equipamentos pesados', '#EF4444', 'truck'),
('Acessórios', 'Acessórios diversos', '#10B981', 'package')
ON CONFLICT DO NOTHING;
```

### Opção B: Via Migrations (Python - Avançado)

Se preferir gerenciar via código, use Alembic:

```bash
# No seu projeto local
cd backend-python
alembic init alembic
alembic revision --autogenerate -m "Initial tables"
alembic upgrade head
```

---

## ✅ Passo 5: Verificar Conexão

### 5.1 Testar no Render

Após redeploy, verifique os logs:

```
✅ Database connected successfully
✅ Tables created
```

### 5.2 Testar Endpoint

```bash
# Criar categoria
curl -X POST https://locnos-antigravity.onrender.com/api/v1/categories \
  -H "Content-Type: application/json" \
  -d '{"name": "Teste", "description": "Categoria teste"}'

# Listar categorias
curl https://locnos-antigravity.onrender.com/api/v1/categories
```

---

## 📊 Passo 6: Gerenciar Dados via Interface

### Table Editor

1. No Supabase, vá em **Table Editor**
2. Selecione uma tabela (ex: `equipment`)
3. Você pode:
   - ✅ Visualizar todos os dados
   - ✅ Adicionar linhas manualmente
   - ✅ Editar dados
   - ✅ Deletar registros

### SQL Editor

Para queries customizadas:

```sql
-- Ver todos equipamentos
SELECT * FROM equipment;

-- Contar por categoria
SELECT c.name, COUNT(e.id) as total
FROM categories c
LEFT JOIN equipment e ON e.category_id = c.id
GROUP BY c.name;

-- Pessoas por tipo
SELECT unnest(types) as tipo, COUNT(*) as total
FROM persons
GROUP BY tipo;
```

---

## 🔐 Segurança

### Row Level Security (RLS)

Para produção, habilite RLS:

```sql
-- Habilitar RLS
ALTER TABLE equipment ENABLE ROW LEVEL SECURITY;
ALTER TABLE persons ENABLE ROW LEVEL SECURITY;

-- Política: usuários autenticados podem ler
CREATE POLICY "Authenticated users can read equipment"
ON equipment FOR SELECT
TO authenticated
USING (true);

-- Política: apenas admins podem inserir
CREATE POLICY "Only admins can insert equipment"
ON equipment FOR INSERT
TO authenticated
WITH CHECK (
  auth.jwt() ->> 'role' = 'admin'
);
```

---

## 📈 Monitoramento

### Dashboard Supabase

**Métricas disponíveis:**
- 📊 Database size
- 🔥 API requests
- ⚡ Query performance
- 👥 Active connections

**Acesse:** Settings → Usage

---

## 🆓 Limites Free Tier

| Recurso | Limite Gratuito |
|---------|----------------|
| Database Size | 500 MB |
| Bandwidth | 5 GB/mês |
| API Requests | Ilimitado |
| Storage | 1 GB |
| Auth Users | 50,000 |

💡 **Upgrade:** $25/mês para 8GB database

---

## 🚨 Troubleshooting

### "Connection refused"

**Causa:** IP não permitido

**Solução:**
1. Settings → Database → **Connection Pooling**
2. Habilite **"Use connection pooling"**
3. Use a **pooler connection string**

### "Too many connections"

**Causa:** Limite de conexões atingido

**Solução:**
```python
# backend-python/app/core/database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=5,          # Reduzir
    max_overflow=10,      # Reduzir
    pool_pre_ping=True
)
```

### "Password authentication failed"

**Causa:** Senha incorreta na URL

**Solução:**
- Verifique a senha no Supabase: Settings → Database → **"Reset database password"**
- Atualize `DATABASE_URL` com nova senha

---

## ✅ Checklist Final

- [ ] Projeto Supabase criado
- [ ] Database password salva
- [ ] Connection string copiada
- [ ] API keys copiadas
- [ ] Variáveis atualizadas no Render
- [ ] Schema SQL executado
- [ ] Tabelas criadas com sucesso
- [ ] Dados iniciais inseridos
- [ ] Conexão testada (logs do Render)
- [ ] Endpoint funcionando

---

**Supabase configurado! 🎉**

Próximo: Deploy do frontend na Vercel
