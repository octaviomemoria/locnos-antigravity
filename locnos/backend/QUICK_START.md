# Guia de Início Rápido - Locnos Backend

Este guia vai te ajudar a configurar e executar o backend do Locnos em poucos minutos.

## 📋 Pré-requisitos

- Node.js 18+ instalado
- MongoDB instalado localmente OU conta no MongoDB Atlas (gratuito)
- Git (opcional)

## 🚀 Passo a Passo

### 1. Instalar Dependências

```bash
cd locnos/backend
npm install
```

### 2. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Edite o arquivo `.env` criado e configure pelo menos:

```env
# Obrigatório
MONGODB_URI=mongodb://localhost:27017/locnos

# Ou para MongoDB Atlas:
# MONGODB_URI=mongodb+srv://seu_usuario:sua_senha@cluster.mongodb.net/locnos

# Recomendado
JWT_SECRET=mude_este_secret_para_algo_seguro_em_producao
```

### 3. Popular o Banco de Dados (Seed)

```bash
npm run seed
```

Este comando irá criar:
- 2 usuários de teste (admin e cliente)
- 4 categorias de equipamentos
- 6 equipamentos de exemplo

**Credenciais criadas:**
- **Admin:** admin@locnos.com.br / admin123
- **Cliente:** joao@email.com / senha123

### 4. Iniciar o Servidor

```bash
npm run dev
```

O servidor iniciará em: `http://localhost:5000`

### 5. Testar a API

Acesse o health check:
```
http://localhost:5000/health
```

Deve retornar:
```json
{
  "success": true,
  "message": "Locnos API está online!",
  "timestamp": "2024-11-24T...",
  "environment": "development"
}
```

## 🧪 Testando Endpoints

### Fazer Login (Admin)

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@locnos.com.br",
    "password": "admin123"
  }'
```

Copie o `token` retornado.

### Listar Equipamentos

```bash
curl http://localhost:5000/api/equipment
```

### Criar Novo Equipamento (requer autenticação)

```bash
curl -X POST http://localhost:5000/api/equipment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "name": "Furadeira Elétrica",
    "description": "Furadeira de impacto 650W",
    "category": "ID_DA_CATEGORIA",
    "pricing": {
      "dailyRate": 20,
      "depositRequired": 50
    }
  }'
```

## 📁 Estrutura de Pastas

```
backend/
├── config/          # Configurações (DB, JWT)
├── models/          # Modelos do MongoDB
├── controllers/     # Lógica de negócio
├── routes/          # Definição de rotas
├── middleware/      # Middlewares (auth, erro)
├── services/        # Serviços auxiliares (em breve)
├── utils/           # Utilitários (em breve)
├── server.js        # Arquivo principal
├── seed.js          # Popular banco de dados
└── .env             # Variáveis de ambiente
```

## 🔐 Rotas Disponíveis

### Autenticação (`/api/auth`)
- `POST /register` - Registrar novo usuário
- `POST /login` - Fazer login
- `GET /me` - Obter usuário atual (protegido)
- `PUT /profile` - Atualizar perfil (protegido)
- `PUT /change-password` - Alterar senha (protegido)
- `POST /forgot-password` - Solicitar reset de senha
- `PUT /reset-password/:token` - Redefinir senha

### Equipamentos (`/api/equipment`)
- `GET /` - Listar equipamentos
- `GET /:id` - Obter equipamento por ID
- `POST /` - Criar equipamento (admin)
- `PUT /:id` - Atualizar equipamento (admin)
- `DELETE /:id` - Deletar equipamento (admin)
- `POST /:id/check-availability` - Verificar disponibilidade
- `GET /:id/stats` - Estatísticas do equipamento (admin)

## 🛠️ Comandos Úteis

```bash
# Desenvolvimento com auto-reload
npm run dev

# Produção
npm start

# Popular banco novamente
npm run seed

# Testes (quando implementados)
npm test
```

## ⚠️ Problemas Comuns

### MongoDB não conecta

**Problema:** `Error: connect ECONNREFUSED 127.0.0.1:27017`

**Solução:** 
- Verifique se o MongoDB está rodando: `mongod --version`
- No Windows, inicie o serviço MongoDB
- Ou use MongoDB Atlas (nuvem gratuita)

### Token inválido

**Problema:** `401 Unauthorized`

**Solução:**
- Certifique-se de que o token está no formato: `Bearer SEU_TOKEN`
- Verifique se o token não expirou (padrão: 7 dias)
- Faça login novamente para obter um novo token

### Porta já em uso

**Problema:** `Error: listen EADDRINUSE: address already in use :::5000`

**Solução:**
- Mude a porta no `.env`: `PORT=3001`
- Ou finalize o processo que está usando a porta 5000

## 📚 Próximos Passos

1. ✅ Backend funcionando
2. ⏳ Criar frontend admin (Next.js)
3. ⏳ Criar frontend cliente (Next.js)
4. ⏳ Implementar módulo de contratos
5. ⏳ Implementar módulo de pagamentos
6. ⏳ Integrar com gateways de pagamento
7. ⏳ Implementar geração de PDF
8. ⏳ Implementar envio de emails

## 🤝 Ajuda

Se encontrar problemas, verifique:
1. Logs do console para mensagens de erro
2. Arquivo `.env` está configurado corretamente
3. MongoDB está rodando
4. Todas as dependências foram instaladas

---

**Desenvolvido para Locnos** 🚀
