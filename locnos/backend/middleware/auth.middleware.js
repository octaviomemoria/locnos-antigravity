const { verifyToken } = require('../config/jwt');
const User = require('../models/User.model');

/**
 * Middleware para proteger rotas que requerem autenticação
 */
const protect = async (req, res, next) => {
    try {
        let token;

        // Verificar se o token está no header
        if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
            token = req.headers.authorization.split(' ')[1];
        }

        // Verificar se o token existe
        if (!token) {
            return res.status(401).json({
                success: false,
                message: 'Acesso não autorizado. Token não fornecido.'
            });
        }

        try {
            // Verificar e decodificar o token
            const decoded = verifyToken(token);

            // Buscar o usuário (sem a senha)
            const user = await User.findById(decoded.id).select('-password');

            if (!user) {
                return res.status(401).json({
                    success: false,
                    message: 'Usuário não encontrado'
                });
            }

            // Verificar se a conta está ativa
            if (user.status === 'blocked') {
                return res.status(403).json({
                    success: false,
                    message: 'Conta bloqueada. Entre em contato com o suporte.'
                });
            }

            // Adicionar o usuário à requisição
            req.user = user;
            next();

        } catch (error) {
            return res.status(401).json({
                success: false,
                message: 'Token inválido ou expirado'
            });
        }

    } catch (error) {
        console.error('Erro no middleware de autenticação:', error);
        res.status(500).json({
            success: false,
            message: 'Erro no servidor'
        });
    }
};

/**
 * Middleware para restringir acesso baseado em roles
 * @param  {...string} roles - Roles permitidas
 */
const authorize = (...roles) => {
    return (req, res, next) => {
        if (!roles.includes(req.user.role)) {
            return res.status(403).json({
                success: false,
                message: `Acesso negado. Apenas ${roles.join(', ')} podem acessar esta rota.`
            });
        }
        next();
    };
};

/**
 * Middleware para verificar permissões específicas
 * @param  {...string} permissions - Permissões necessárias
 */
const checkPermission = (...permissions) => {
    return (req, res, next) => {
        // Super admin sempre tem acesso
        if (req.user.role === 'super_admin') {
            return next();
        }

        // Verificar se o usuário tem as permissões necessárias
        const hasPermission = permissions.some(permission =>
            req.user.permissions && req.user.permissions.includes(permission)
        );

        if (!hasPermission) {
            return res.status(403).json({
                success: false,
                message: 'Você não tem permissão para realizar esta ação'
            });
        }

        next();
    };
};

/**
 * Middleware para verificar se o usuário é dono do recurso ou admin
 */
const ownerOrAdmin = (resourceUserField = 'user') => {
    return (req, res, next) => {
        // Admin/staff sempre pode acessar
        if (['admin', 'super_admin', 'staff'].includes(req.user.role)) {
            return next();
        }

        // Verificar se o usuário é o dono do recurso
        const resourceUserId = req[resourceUserField] || req.body[resourceUserField];

        if (resourceUserId && resourceUserId.toString() === req.user._id.toString()) {
            return next();
        }

        return res.status(403).json({
            success: false,
            message: 'Você não tem permissão para acessar este recurso'
        });
    };
};

/**
 * Middleware opcional - não bloqueia se não houver token
 */
const optionalAuth = async (req, res, next) => {
    try {
        let token;

        if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
            token = req.headers.authorization.split(' ')[1];
        }

        if (token) {
            try {
                const decoded = verifyToken(token);
                const user = await User.findById(decoded.id).select('-password');
                if (user) {
                    req.user = user;
                }
            } catch (error) {
                // Token inválido, mas não bloqueia a requisição
                console.log('Token inválido em optionalAuth');
            }
        }

        next();
    } catch (error) {
        next();
    }
};

module.exports = {
    protect,
    authorize,
    checkPermission,
    ownerOrAdmin,
    optionalAuth
};
