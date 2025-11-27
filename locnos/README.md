# Locnos-Antigravity - Equipment Rental Management System

Sistema completo de gestão para locadoras de equipamentos com portal para clientes.

## 🎯 Visão Geral

Locnos-Antigravity é uma plataforma moderna de gestão de locadoras que oferece:

- **Para Gestores**: Controle completo de estoque, contratos, financeiro e clientes
- **Para Clientes**: Catálogo online, solicitação de orçamentos e acompanhamento de contratos

## 🛠️ Tecnologias

### Backend
- Node.js + Express.js
- Supabase (PostgreSQL)
- Prisma ORM
- JWT Authentication
- Multer (upload de arquivos)
- PDFKit (geração de documentos)

### Frontend Admin
- React.js + Next.js
- Tailwind CSS
- shadcn/ui components
- React Query
- Zustand (state management)

### Frontend Cliente
- React.js + Next.js
- Tailwind CSS
- Responsive design
- PWA ready

## 📁 Estrutura do Projeto

```
locnos/
├── backend/          # API REST Node.js
├── frontend-admin/   # Dashboard administrativo
├── frontend-client/  # Portal do cliente
└── docs/            # Documentação
```

## 🚀 Início Rápido

### Backend

```bash
cd locnos/backend
npm install
cp .env.example .env
# Configure as variáveis de ambiente (principalmente MONGODB_URI)
npm run seed    # Popular banco de dados com dados de teste
npm run dev     # Iniciar servidor de desenvolvimento
```

### Frontend Admin (Em breve)

```bash
cd locnos/frontend-admin
npm install
npm run dev
```

### Frontend Cliente (Em breve)

```bash
cd locnos/frontend-client
npm install
npm run dev
```

## 📋 Funcionalidades Principais

### Módulo Admin
- ✅ Gestão de equipamentos (CRUD completo)
- ✅ Controle de disponibilidade em tempo real
- ✅ Gestão de contratos e orçamentos
- ✅ CRM de clientes
- ✅ Dashboard financeiro
- ✅ Relatórios gerenciais
- ✅ Controle de manutenção
- ✅ Multi-usuário com permissões

### Módulo Cliente
- ✅ Catálogo de equipamentos com filtros
- ✅ Solicitação de orçamentos online
- ✅ Acompanhamento de contratos
- ✅ Histórico de locações
- ✅ Perfil do usuário
- ✅ Notificações

## 🔒 Segurança

- Autenticação JWT
- Bcrypt para senhas
- Rate limiting
- Validação de entrada
- CORS configurado
- HTTPS obrigatório em produção

## 📝 Licença

Propriedade da Locnos © 2024

## 👥 Autores

Desenvolvido para modernizar a gestão de locadoras de equipamentos no Brasil.
