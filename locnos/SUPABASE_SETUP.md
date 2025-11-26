# Guia de Setup do Supabase - Locnos

Este guia mostra como configurar o Supabase para usar como banco de dados do Locnos.

## 🎯 Por que Supabase?

- ✅ PostgreSQL gerenciado (gratuito até 500MB)
- ✅ Autenticação embutida
- ✅ Storage para imagens
- ✅ APIs automáticas
- ✅ Dashboard visual
- ✅ Backups automáticos

## 📋 Passo a Passo

### 1. Criar Conta no Supabase

1. Acesse: https://supabase.com
2. Clique em "Start your project"
3. Crie uma conta (gratuita)

### 2. Criar Novo Projeto

1. No dashboard, clique em "New Project"
2. Escolha um nome: `locnos`
3. Defina uma senha forte para o banco de dados (SALVE ESTA SENHA!)
4. Escolha a região mais próxima (ex: South America - São Paulo)
5. Clique em "Create new project"

⏱️ Aguarde ~2 minutos enquanto o Supabase provisiona seu banco.

### 3. Obter Credenciais

Após o projeto estar pronto:

1. No menu lateral, vá em **Settings** (⚙️) → **Database**
2. Role até **Connection string** → **URI**
3. Copie a string de conexão (ela será algo assim):

```
postgresql://postgres.abc123:SUA-SENHA@abc-123-def.pooler.supabase.com:5432/postgres
```

4. **IMPORTANTE:** Substitua `[YOUR-PASSWORD]` pela senha que você definiu no passo 2

### 4. Configurar Variáveis de Ambiente

No seu projeto Locnos, edite o arquivo `backend/.env`:

```env
# Substitua com sua URL do Supabase
DATABASE_URL="postgresql://postgres.abc123:SUA-SENHA@abc-123-def.pooler.supabase.com:5432/postgres"

# Opcional - Para usar features do Supabase (auth, storage)
SUPABASE_URL=https://abc123def.supabase.co
SUPABASE_ANON_KEY=sua_chave_anon_aqui
SUPABASE_SERVICE_ROLE_KEY=sua_service_role_key_aqui
```

**Onde encontrar as chaves:**
- No menu lateral: **Settings** → **API**
- `Project URL` = SUPABASE_URL
- `anon public` = SUPABASE_ANON_KEY  
- `service_role` = SUPABASE_SERVICE_ROLE_KEY (⚠️ NUNCA exponha publicamente!)

### 5. Instalar Dependências

```bash
cd locnos/backend
npm install
```

Isso instalará:
- `@prisma/client` - Cliente do Prisma ORM
- `prisma` - CLI do Prisma
- `@supabase/supabase-js` - Cliente Supabase (para storage/auth)

### 6. Executar Migrações do Prisma

```bash
# Gerar o cliente Prisma
npx prisma generate

# Criar as tabelas no banco de dados
npx prisma migrate dev --name initial_migration

# Ou fazer push direto (sem histórico de migrations)
npx prisma db push
```

Isso criará todas as tabelas no seu banco Supabase!

### 7. Popular Banco com Dados de Teste

```bash
npm run seed
```

### 8. Iniciar Servidor

```bash
npm run dev
```

## ✅ Verificar se Funcionou

### Via Navegador

Acesse: http://localhost:5000/health

Deve retornar:
```json
{
  "success": true,
  "message": "Locnos API está online!",
  ...
}
```

### Via Supabase Dashboard

1. No Supabase, vá no menu **Table Editor**
2. Você verá as tabelas criadas:
   - users
   - equipment
   - contracts
   - payments
   - categories
   - etc.

3. Clique em `users` → verá os usuários criados pelo seed

## 🗄️ Explorar o Banco de Dados

### Prisma Studio (Recomendado)

```bash
npx prisma studio
```

Abrirá uma interface visual em http://localhost:5555 onde você pode:
- Ver todos os dados
- Editar registros
- Criar novos registros
- Ver relacionamentos

### Supabase Dashboard

No menu **Table Editor** você pode:
- Ver e editar dados
- Executar queries SQL
- Configurar políticas de segurança (RLS)
- Ver logs

## 📊 Estrutura do Banco

O Prisma criou as seguintes tabelas:

| Tabela | Descrição |
|--------|-----------|
| `users` | Usuários (clientes, admin, staff) |
| `equipment` | Equipamentos disponíveis |
| `categories` | Categorias dos equipamentos |
| `contracts` | Contratos de locação |
| `contract_items` | Itens de cada contrato |
| `payments` | Pagamentos dos contratos |
| `maintenance` | Registros de manutenção |
| `locations` | Filiais/localizações |

## 🔧 Comandos Úteis do Prisma

```bash
# Ver schema visual
npx prisma studio

# Gerar cliente após mudanças no schema
npx prisma generate

# Criar nova migration
npx prisma migrate dev --name nome_da_migration

# Reset completo do banco (⚠️ apaga tudo!)
npx prisma migrate reset

# Aplicar migrations em produção
npx prisma migrate deploy

# Formatar schema.prisma
npx prisma format
```

## 📝 Editar o Schema

O arquivo de schema está em: `backend/prisma/schema.prisma`

Após fazer mudanças:

1. Gerar nova migration:
```bash
npx prisma migrate dev --name descricao_da_mudanca
```

2. Ou fazer push direto (sem migration):
```bash
npx prisma db push
```

3. Gerar cliente atualizado:
```bash
npx prisma generate
```

## 🖼️ Configurar Supabase Storage (para Imagens)

1. No Supabase, vá em **Storage**
2. Clique em "Create a new bucket"
3. Nome: `equipamentos`
4. Public: ✅ (para permitir acesso às imagens)
5. Clique em "Create bucket"

Agora você pode fazer upload de imagens dos equipamentos!

## 🔐 Segurança - Row Level Security (RLS)

Por padrão, o Supabase tem RLS desativado. Para ambientes de produção:

1. Vá em **Authentication** → **Policies**
2. Para cada tabela, configure políticas de acesso
3. Exemplos:
   - `Select`: Público pode ver equipamentos visíveis
   - `Insert/Update/Delete`: Apenas admin/staff

**Para desenvolvimento, pode deixar RLS desativado.**

## 🚨 Problemas Comuns

### Erro: "Can't reach database server"

- Verifique se copiou a URL correta
- Verifique se substituiu `[YOUR-PASSWORD]` pela senha real
- Sem espaços extras na string de conexão

### Erro: "Invalid database URL"

- URL deve começar com `postgresql://`
- Verifique se não tem caracteres especiais não codificados na senha

### Tabelas não foram criadas

```bash
npx prisma db push --force-reset
```

## 📊 Limites do Plano Gratuito

- ✅ 500MB de armazenamento (banco de dados)
- ✅ 1GB de armazenamento (storage de arquivos)
- ✅ 50.000 usuários autenticados/mês
- ✅ 2GB de transferência de dados/mês
- ✅ Backups automáticos por 7 dias

Para a maioria dos projetos iniciais, isso é mais que suficiente!

## 🎓 Próximos Passos

1. ✅ Supabase configurado
2. ✅ Tabelas criadas
3. ✅ Dados de teste populados
4. ✅ Servidor funcionando

**Agora você está pronto para:**
- Testar a API
- Desenvolver os frontends
- Integrar funcionalidades avançadas

---

## 🔗 Links Úteis

- Documentação Supabase: https://supabase.com/docs
- Documentação Prisma: https://www.prisma.io/docs
- Dashboard Supabase: https://app.supabase.com

**Dúvidas? Consulte a documentação ou peça ajuda!** 🚀
