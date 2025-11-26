# ✅ GUIA DE INSTALAÇÃO RÁPIDA - Locnos com Supabase

##📦 Pré requisitos

- ✅ Node.js 18+ instalado
- ✅ Conta no Supabase (gratuita): https://supabase.com

## 🚀 Instalação Automática (Windows)

```bash
cd locnos
install.bat
```

## 🚀 Instalação Manual

### 1. Criar Projeto no Supabase

1. Acesse https://supabase.com e faça login
2. Clique em "New Project"
3. Nome: `locnos`
4. Senha do banco: **Escolha uma senha forte e ANOTE!**
5. Região: South America (São Paulo)
6. Aguarde ~2 minutos

### 2. Copiar Credenciais

No Supabase:
- **Settings** → **Database** → **Connection string** → **URI**
- Copie a URL e substitua `[YOUR-PASSWORD]` pela sua senha

Exemplo:
```
postgresql://postgres.abc123:MinhaS3nh4@abc.pooler.supabase.com:5432/postgres
```

### 3. Configurar Projeto

```bash
cd locnos/backend
npm install
cp .env.example .env
```

Edite `.env` e cole sua DATABASE_URL:

```env
DATABASE_URL="postgresql://postgres.abc123:SuaSenha@abc.supabase.com:5432/postgres"
JWT_SECRET=mude_esta_chave_secreta_aqui
```

### 4. Criar Tabelas no Banco

```bash
npx prisma generate
npx prisma db push
```

### 5. Popular Dados de Teste

```bash
npm run seed
```

### 6. Iniciar Servidor

```bash
npm run dev
```

## ✅ Testar

Abra: http://localhost:5000/health

Deve ver:
```json
{
  "success": true,
  "message": "Locnos API está online!"
}
```

## 🔑 Credenciais de Teste

- **Admin:** admin@locnos.com.br / admin123
- **Cliente:** joao@email.com / senha123

## 🎯 Próximos Passos

1. Testar API com Postman
2. Explorar banco com `npx prisma studio`
3. Desenvolver frontend

## ⚠️ Problemas?

### Erro na DATABASE_URL

- Verifique se copiou corretamente
- Substitua `[YOUR-PASSWORD]` pela senha real
- Não deixe espaços extras

### Erro ao criar tabelas

```bash
npx prisma db push --force-reset
```

### Precisa recriar tudo

```bash
npm run seed
```

## 📚 Documentação Completa

- Setup detalhado Supabase: `SUPABASE_SETUP.md`
- Guia da API: `backend/QUICK_START.md`
- Frontend setup: `FRONTEND_SETUP.md`

---

**Projeto configurado com sucesso! 🎉**
