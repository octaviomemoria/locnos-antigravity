# Locnos Frontend - Next.js 14

Interface web moderna para o sistema de gestão de locadoras de equipamentos.

## 🚀 Stack Tecnológica

- **Framework:** Next.js 14 (App Router)
- **Linguagem:** TypeScript
- **Styling:** Tailwind CSS + shadcn/ui
- **State:** Zustand
- **API:** Axios + React Query
- **Forms:** React Hook Form + Zod

## 📋 Pré-requisitos

- Node.js 18+ instalado
- Backend FastAPI rodando em `http://localhost:8000`

## 🔧 Instalação

```bash
# 1. Instalar dependências
npm install

# 2. Configurar variável de ambiente
# Crie arquivo .env.local com:
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# 3. Iniciar servidor dev
npm run dev
```

## 🌐 Acessar Aplicação

Abra o navegador em: **http://localhost:3000**

### Credenciais de Teste

```
Email: admin@locnos.com.br
Senha: admin123
```

## 📂 Estrutura do Projeto

```
frontend-nextjs/
├── app/
│   ├── page.tsx                 # Home
│   ├── login/page.tsx           # Login
│   ├── dashboard/
│   │   ├── layout.tsx           # Layout c/ sidebar
│   │   └── page.tsx             # Dashboard principal
│   ├── layout.tsx               # Root layout
│   └── providers.tsx            # React Query
├── components/ui/               # shadcn/ui components
├── lib/
│   ├── api/client.ts            # Axios client
│   ├── store/auth.ts            # Zustand store
│   └── utils.ts                 # Helpers
└── types/index.ts               # TypeScript types
```

## ✨ Features Implementadas

- ✅ Autenticação JWT
- ✅ Proteção de rotas
- ✅ Dashboard com KPIs
- ✅ Sidebar navegável
- ✅ Design responsivo
- ✅ Validação de formulários

## 🔄 Próximos Passos

1. Criar CRUD de Equipamentos
2. Criar CRUD de Pessoas
3. Criar CRUD de Categorias
4. Adicionar tabelas com filtros
5. Adicionar gráficos

## 📝 Comandos Úteis

```bash
npm run dev      # Iniciar dev server
npm run build    # Build produção
npm run start    # Rodar produção
npm run lint     # Verificar código
```

## 🎨 Temas e Cores

- Primary: Blue (Tailwind sky-500)
- Success: Green
- Warning: Orange  
- Error: Red

## 🔗 Backend

O frontend consome a API FastAPI em:
- **Base URL:** `http://localhost:8000/api/v1`
- **21 endpoints disponíveis**
- **Autenticação:** JWT Bearer Token

---

**Desenvolvido com ❤️ usando Next.js 14**
