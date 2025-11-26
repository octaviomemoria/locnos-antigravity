const { PrismaClient } = require('@prisma/client');

// Criar instância única do Prisma Client (singleton)
const prisma = new PrismaClient({
  log: process.env.NODE_ENV === 'development'
    ? ['query', 'info', 'warn', 'error']
    : ['error'],
});

// Testar conexão
const connectDB = async () => {
  try {
    await prisma.$connect();
    console.log('✅ Supabase (PostgreSQL) conectado via Prisma');
  } catch (error) {
    console.error('❌ Erro ao conectar ao Supabase:', error.message);
    process.exit(1);
  }
};

// Graceful shutdown
process.on('SIGINT', async () => {
  await prisma.$disconnect();
  console.log('Prisma desconectado do Supabase');
  process.exit(0);
});

process.on('SIGTERM', async () => {
  await prisma.$disconnect();
  console.log('Prisma desconectado do Supabase');
  process.exit(0);
});

module.exports = { prisma, connectDB };
