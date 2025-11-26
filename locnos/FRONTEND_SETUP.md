# Frontend Setup Guide - Locnos

Este documento contém instruções para configurar os frontends do Locnos (Admin e Cliente).

## 🎯 Próximos Passos

O backend já está completo e funcional. As próximas etapas são:

### 1. Frontend Admin (Dashboard)

Interface para gestores da locadora gerenciarem todo o negócio.

**Para criar o frontend admin:**

```bash
cd locnos
npx create-next-app@latest frontend-admin --typescript --tailwind --app
```

Escolha as opções:
- ✅ TypeScript
- ✅ ESLint
- ✅ Tailwind CSS
- ✅ `src/` directory
- ✅ App Router
- ✅ Import alias (@/*)

**Funcionalidades principais:**
- Dashboard com métricas
- Gestão de equipamentos (CRUD completo)
- Gestão de contratos
- Gestão de clientes
- Relatórios financeiros
- Configurações

### 2. Frontend Cliente (Portal)

Interface para clientes navegarem catálogo e solicitarem locações.

```bash
cd locnos
npx create-next-app@latest frontend-client --typescript --tailwind --app
```

**Funcionalidades principais:**
- Catálogo de equipamentos com filtros
- Carrinho de solicitação
- Área do cliente
- Histórico de locações
- Acompanhamento de contratos

## 📦 Dependências Recomendadas

### Ambos os Frontends

```bash
# UI Components
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-toast
npm install lucide-react class-variance-authority clsx tailwind-merge

# State Management
npm install zustand

# Forms
npm install react-hook-form zod @hookform/resolvers

# API Client
npm install axios swr

# Dates
npm install date-fns

# Charts (Admin)
npm install recharts

# Tables (Admin)
npm install @tanstack/react-table
```

## 🎨 Design System

### Cores Principais (Tailwind)

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          // ... (use shadcn palette generator)
          600: '#0284c7',
          700: '#0369a1',
        },
        // Adicionar cores específicas da marca Locnos
      }
    }
  }
}
```

### Componentes UI (shadcn/ui)

```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add form
npx shadcn-ui@latest add table
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add select
npx shadcn-ui@latest add toast
```

## 🔗 Conectar com Backend

### 1. Criar serviço de API

`src/lib/api.ts`:
```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### 2. Criar hooks personalizados

`src/hooks/useAuth.ts`:
```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  _id: string;
  name: string;
  email: string;
  role: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuth = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      login: async (email, password) => {
        const response = await api.post('/auth/login', { email, password });
        set({ 
          user: response.data.data.user, 
          token: response.data.data.token 
        });
      },
      logout: () => set({ user: null, token: null }),
    }),
    {
      name: 'auth-storage',
    }
  )
);
```

## 📄 Estrutura de Pastas Sugerida

### Frontend Admin

```
frontend-admin/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   └── layout.tsx
│   │   ├── (dashboard)/
│   │   │   ├── dashboard/
│   │   │   ├── equipments/
│   │   │   ├── contracts/
│   │   │   ├── customers/
│   │   │   ├── financial/
│   │   │   └── layout.tsx
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ui/               # shadcn components
│   │   ├── forms/
│   │   ├── tables/
│   │   └── charts/
│   ├── lib/
│   │   ├── api.ts
│   │   └── utils.ts
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useEquipment.ts
│   │   └── useContracts.ts
│   └── types/
│       └── index.ts
```

### Frontend Cliente

```
frontend-client/
├── src/
│   ├── app/
│   │   ├── page.tsx           # Home/Catálogo
│   │   ├── equipment/
│   │   │   └── [id]/
│   │   ├── cart/
│   │   ├── profile/
│   │   ├── contracts/
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ui/
│   │   ├── catalog/
│   │   ├── cart/
│   │   └── layout/
│   ├── lib/
│   └── hooks/
```

## 🚀 Começar Desenvolvimento

### Ordem Recomendada de Desenvolvimento

#### Frontend Admin:

1. **Setup inicial** (1-2 dias)
   - Configurar Next.js + Tailwind
   - Instalar shadcn/ui
   - Criar sistema de autenticação
   - Layout base com sidebar

2. **Dashboard** (2-3 dias)
   - Cards com métricas
   - Gráficos de faturamento
   - Lista de ações pendentes

3. **Gestão de Equipamentos** (3-4 dias)
   - Listagem com filtros
   - Formulário de criar/editar
   - Upload de imagens
   - Geração de QR code

4. **Gestão de Contratos** (4-5 dias)
   - Listagem de contratos
   - Aprovação de orçamentos
   - Workflow de status
   - Geração de PDF

5. **Gestão Financeira** (3-4 dias)
   - Contas a receber
   - Relatórios
   - Filtros por período

#### Frontend Cliente:

1. **Setup e Home** (1-2 dias)
   - Configuração
   - Landing page
   - Hero section
   - Categorias em destaque

2. **Catálogo** (2-3 dias)
   - Grid de equipamentos
   - Filtros e busca
   - Paginação
   - Página de detalhes

3. **Carrinho e Checkout** (3-4 dias)
   - Adicionar ao carrinho
   - Seleção de datas
   - Formulário de solicitação
   - Confirmação

4. **Área do Cliente** (2-3 dias)
   - Login/Registro
   - Dashboard pessoal
   - Contratos ativos
   - Histórico

## 🎨 Referências de Design

Para inspiração visual:
- **Admin:** [Vercel Analytics](https://vercel.com/analytics), [Tailwind UI Admin](https://tailwindui.com/templates)
- **Cliente:** [Airbnb](https://airbnb.com), Sites de e-commerce modernos

## 📝 Variáveis de Ambiente

### Frontend Admin (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:5000/api
NEXT_PUBLIC_APP_NAME=Locnos Admin
```

### Frontend Cliente (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:5000/api
NEXT_PUBLIC_APP_NAME=Locnos
NEXT_PUBLIC_COMPANY_PHONE=+5511999999999
NEXT_PUBLIC_COMPANY_EMAIL=contato@locnos.com.br
```

## ✅ Checklist de Implementação

### Antes de começar:
- [ ] Backend está rodando
- [ ] Banco de dados populado com seed
- [ ] Testou endpoints via Postman/curl
- [ ] Entendeu a estrutura de dados

### Frontend Admin:
- [ ] Projeto Next.js criado
- [ ] shadcn/ui configurado
- [ ] Sistema de autenticação
- [ ] Layout com sidebar
- [ ] Dashboard com métricas
- [ ] CRUD de equipamentos
- [ ] CRUD de contratos
- [ ] Gestão de clientes
- [ ] Relatórios financeiros

### Frontend Cliente:
- [ ] Projeto Next.js criado
- [ ] Landing page
- [ ] Catálogo de equipamentos
- [ ] Filtros e busca
- [ ] Página de detalhes
- [ ] Carrinho/solicitação
- [ ] Registro e login
- [ ] Área do cliente
- [ ] Acompanhamento de contratos

---

**Status Atual:** ✅ Backend completo e funcionando
**Próximo Passo:** Criar frontend admin ou cliente conforme prioridade

Precisa de ajuda para iniciar? Basta solicitar!
