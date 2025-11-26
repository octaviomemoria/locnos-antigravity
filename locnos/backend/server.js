require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const { connectDB } = require('./config/database');
const { errorHandler, notFound } = require('./middleware/error.middleware');

// Inicializar Express
const app = express();

// Conectar ao banco de dados
connectDB();

// ===== MIDDLEWARES DE SEGURANÇA =====

// Helmet - Headers de segurança
app.use(helmet());

// CORS - Controle de acesso
const corsOptions = {
    origin: [
        process.env.CLIENT_URL,
        process.env.ADMIN_URL,
        'http://localhost:3000',
        'http://localhost:3001'
    ],
    credentials: true
};
app.use(cors(corsOptions));

// Rate limiting - Prevenir ataques de força bruta
const limiter = rateLimit({
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW) * 60 * 1000 || 15 * 60 * 1000,
    max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS) || 100,
    message: 'Muitas requisições deste IP, tente novamente mais tarde.'
});
app.use('/api', limiter);

// Rate limiting mais restritivo para autenticação
const authLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutos
    max: 5, // 5 tentativas
    message: 'Muitas tentativas de login, tente novamente em 15 minutos.'
});
app.use('/api/auth/login', authLimiter);
app.use('/api/auth/register', authLimiter);

// ===== MIDDLEWARES DE PARSING =====

// Body parser
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// ===== ROTAS =====

// Rota de health check
app.get('/health', (req, res) => {
    res.status(200).json({
        success: true,
        message: 'Locnos API está online!',
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV
    });
});

// Rotas da API
app.use('/api/auth', require('./routes/auth.routes'));
app.use('/api/equipment', require('./routes/equipment.routes'));
// TODO: Adicionar mais rotas
// app.use('/api/contracts', require('./routes/contract.routes'));
// app.use('/api/customers', require('./routes/customer.routes'));
// app.use('/api/payments', require('./routes/payment.routes'));

// ===== TRATAMENTO DE ERROS =====

// Rota não encontrada
app.use(notFound);

// Handler de erros global
app.use(errorHandler);

// ===== INICIAR SERVIDOR =====

const PORT = process.env.PORT || 5000;

const server = app.listen(PORT, () => {
    console.log(`
  ╔═══════════════════════════════════════════════════════╗
  ║                                                       ║
  ║   🚀 Locnos API Server                               ║
  ║                                                       ║
  ║   Environment: ${process.env.NODE_ENV?.padEnd(36) || 'development'.padEnd(36)}║
  ║   Port: ${String(PORT).padEnd(42)}║
  ║   URL: http://localhost:${PORT.toString().padEnd(27)}║
  ║                                                       ║
  ║   📚 Health Check: http://localhost:${PORT}/health${' '.repeat(10)}║
  ║                                                       ║
  ╚═══════════════════════════════════════════════════════╝
  `);
});

// Tratamento de erros não capturados
process.on('unhandledRejection', (err) => {
    console.error('❌ UNHANDLED REJECTION! Encerrando...');
    console.error(err);
    server.close(() => {
        process.exit(1);
    });
});

process.on('uncaughtException', (err) => {
    console.error('❌ UNCAUGHT EXCEPTION! Encerrando...');
    console.error(err);
    process.exit(1);
});

module.exports = app;
