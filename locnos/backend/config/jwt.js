const jwt = require('jsonwebtoken');

/**
 * Gera um token JWT para autenticação
 * @param {string} userId - ID do usuário
 * @param {string} role - Papel do usuário (admin, customer, staff)
 * @returns {string} Token JWT
 */
const generateToken = (userId, role) => {
    return jwt.sign(
        {
            id: userId,
            role: role
        },
        process.env.JWT_SECRET,
        {
            expiresIn: process.env.JWT_EXPIRE || '7d'
        }
    );
};

/**
 * Gera um refresh token
 * @param {string} userId - ID do usuário
 * @returns {string} Refresh token JWT
 */
const generateRefreshToken = (userId) => {
    return jwt.sign(
        { id: userId },
        process.env.JWT_REFRESH_SECRET,
        {
            expiresIn: process.env.JWT_REFRESH_EXPIRE || '30d'
        }
    );
};

/**
 * Verifica e decodifica um token JWT
 * @param {string} token - Token a ser verificado
 * @returns {object} Payload decodificado
 */
const verifyToken = (token) => {
    try {
        return jwt.verify(token, process.env.JWT_SECRET);
    } catch (error) {
        throw new Error('Token inválido ou expirado');
    }
};

/**
 * Verifica um refresh token
 * @param {string} token - Refresh token
 * @returns {object} Payload decodificado
 */
const verifyRefreshToken = (token) => {
    try {
        return jwt.verify(token, process.env.JWT_REFRESH_SECRET);
    } catch (error) {
        throw new Error('Refresh token inválido ou expirado');
    }
};

module.exports = {
    generateToken,
    generateRefreshToken,
    verifyToken,
    verifyRefreshToken
};
