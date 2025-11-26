#!/bin/bash

echo "========================================"
echo "  LOCNOS - Instalação Automática"
echo "========================================"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "backend/package.json" ]; then
    echo "❌ ERRO: Execute este script da pasta 'locnos'"
    echo ""
    echo "Caminho correto:"
    echo "  cd locnos"
    echo "  ./install.sh"
    exit 1
fi

echo "📦 [1/4] Instalando dependências do backend..."
cd backend
npm install
if [ $? -ne 0 ]; then
    echo "❌ ERRO: Falha ao instalar dependências"
    exit 1
fi

echo ""
echo "⚙️  [2/4] Criando arquivo .env..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Arquivo .env criado! Configure o MONGODB_URI antes de continuar."
else
    echo "ℹ️  Arquivo .env já existe."
fi

echo ""
read -p "🌱 [3/4] Deseja popular o banco de dados agora? (s/N): " resposta
if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
    echo "Populando banco de dados..."
    npm run seed
fi

echo ""
echo "========================================"
echo "  ✅ INSTALAÇÃO CONCLUÍDA!"
echo "========================================"
echo ""
echo "Próximos passos:"
echo "  1. Configure o arquivo backend/.env"
echo "  2. Execute: cd backend"
echo "  3. Execute: npm run dev"
echo ""
echo "Credenciais de teste:"
echo "  Admin: admin@locnos.com.br / admin123"
echo "  Cliente: joao@email.com / senha123"
echo ""
