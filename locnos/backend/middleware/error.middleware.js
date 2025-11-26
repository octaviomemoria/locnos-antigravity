/**
 * Middleware centralizado de tratamento de erros
 */

// Classe de erro personalizada
class AppError extends Error {
    constructor(message, statusCode) {
        super(message);
        this.statusCode = statusCode;
        this.isOperational = true;

        Error.captureStackTrace(this, this.constructor);
    }
}

// Handler de erros do Mongoose
const handleCastErrorDB = (err) => {
    const message = `Recurso inválido: ${err.path} = ${err.value}`;
    return new AppError(message, 400);
};

const handleDuplicateFieldsDB = (err) => {
    const field = Object.keys(err.keyValue)[0];
    const value = err.keyValue[field];
    const message = `${field} '${value}' já está em uso. Use outro valor.`;
    return new AppError(message, 400);
};

const handleValidationErrorDB = (err) => {
    const errors = Object.values(err.errors).map(el => el.message);
    const message = `Dados de formulário inválidos: ${errors.join('. ')}`;
    return new AppError(message, 400);
};

const handleJWTError = () =>
    new AppError('Token inválido. Por favor, faça login novamente.', 401);

const handleJWTExpiredError = () =>
    new AppError('Token expirado. Por favor, faça login novamente.', 401);

// Enviar erro em desenvolvimento (com stack trace)
const sendErrorDev = (err, res) => {
    res.status(err.statusCode).json({
        success: false,
        error: err,
        message: err.message,
        stack: err.stack
    });
};

// Enviar erro em produção (sem informações sensíveis)
const sendErrorProd = (err, res) => {
    // Erro operacional confiável: enviar mensagem ao cliente
    if (err.isOperational) {
        res.status(err.statusCode).json({
            success: false,
            message: err.message
        });
    }
    // Erro de programação ou desconhecido: não vazar detalhes
    else {
        console.error('ERROR 💥', err);
        res.status(500).json({
            success: false,
            message: 'Algo deu errado no servidor!'
        });
    }
};

// Middleware principal de erro
const errorHandler = (err, req, res, next) => {
    err.statusCode = err.statusCode || 500;

    if (process.env.NODE_ENV === 'development') {
        sendErrorDev(err, res);
    } else {
        let error = { ...err };
        error.message = err.message;

        // Erros específicos do Mongoose
        if (err.name === 'CastError') error = handleCastErrorDB(err);
        if (err.code === 11000) error = handleDuplicateFieldsDB(err);
        if (err.name === 'ValidationError') error = handleValidationErrorDB(err);
        if (err.name === 'JsonWebTokenError') error = handleJWTError();
        if (err.name === 'TokenExpiredError') error = handleJWTExpiredError();

        sendErrorProd(error, res);
    }
};

// Middleware para rotas não encontradas
const notFound = (req, res, next) => {
    const error = new AppError(
        `Rota ${req.originalUrl} não encontrada neste servidor`,
        404
    );
    next(error);
};

// Handler para erros assíncronos
const asyncHandler = (fn) => {
    return (req, res, next) => {
        Promise.resolve(fn(req, res, next)).catch(next);
    };
};

module.exports = {
    AppError,
    errorHandler,
    notFound,
    asyncHandler
};
