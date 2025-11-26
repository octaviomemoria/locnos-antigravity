const User = require('../models/User.model');
const { generateToken, generateRefreshToken } = require('../config/jwt');
const { asyncHandler, AppError } = require('../middleware/error.middleware');

/**
 * @desc    Registrar novo usuário
 * @route   POST /api/auth/register
 * @access  Public
 */
const register = asyncHandler(async (req, res, next) => {
    const {
        name,
        email,
        password,
        phone,
        document,
        address,
        company,
        role = 'customer'
    } = req.body;

    // Verificar se o email já existe
    const existingUser = await User.findOne({ email });
    if (existingUser) {
        return next(new AppError('Email já cadastrado', 400));
    }

    // Verificar se o documento já existe
    if (document && document.number) {
        const existingDoc = await User.findOne({ 'document.number': document.number });
        if (existingDoc) {
            return next(new AppError('Documento já cadastrado', 400));
        }
    }

    // Criar usuário
    const user = await User.create({
        name,
        email,
        password,
        phone,
        document,
        address,
        company,
        role: role === 'customer' ? 'customer' : 'customer', // Force customer no registro público
        status: 'pending' // Requer aprovação
    });

    // Gerar tokens
    const token = generateToken(user._id, user.role);
    const refreshToken = generateRefreshToken(user._id);

    res.status(201).json({
        success: true,
        message: 'Cadastro realizado com sucesso! Aguarde aprovação.',
        data: {
            user: user.toPublicJSON(),
            token,
            refreshToken
        }
    });
});

/**
 * @desc    Login de usuário
 * @route   POST /api/auth/login
 * @access  Public
 */
const login = asyncHandler(async (req, res, next) => {
    const { email, password } = req.body;

    // Validar entrada
    if (!email || !password) {
        return next(new AppError('Por favor, forneça email e senha', 400));
    }

    // Buscar usuário com senha
    const user = await User.findOne({ email }).select('+password');

    if (!user) {
        return next(new AppError('Credenciais inválidas', 401));
    }

    // Verificar senha
    const isPasswordMatch = await user.comparePassword(password);

    if (!isPasswordMatch) {
        return next(new AppError('Credenciais inválidas', 401));
    }

    // Verificar se a conta está ativa
    if (user.status === 'blocked') {
        return next(new AppError('Conta bloqueada. Entre em contato com o suporte.', 403));
    }

    if (user.status === 'inactive') {
        return next(new AppError('Conta inativa. Entre em contato com o suporte.', 403));
    }

    // Atualizar último login
    user.lastLogin = new Date();
    await user.save({ validateBeforeSave: false });

    // Gerar tokens
    const token = generateToken(user._id, user.role);
    const refreshToken = generateRefreshToken(user._id);

    res.status(200).json({
        success: true,
        message: 'Login realizado com sucesso!',
        data: {
            user: user.toPublicJSON(),
            token,
            refreshToken
        }
    });
});

/**
 * @desc    Obter usuário atual
 * @route   GET /api/auth/me
 * @access  Private
 */
const getMe = asyncHandler(async (req, res, next) => {
    const user = await User.findById(req.user._id);

    res.status(200).json({
        success: true,
        data: {
            user: user.toPublicJSON()
        }
    });
});

/**
 * @desc    Atualizar perfil do usuário atual
 * @route   PUT /api/auth/profile
 * @access  Private
 */
const updateProfile = asyncHandler(async (req, res, next) => {
    const {
        name,
        phone,
        whatsapp,
        address,
        company
    } = req.body;

    const user = await User.findById(req.user._id);

    if (!user) {
        return next(new AppError('Usuário não encontrado', 404));
    }

    // Atualizar campos permitidos
    if (name) user.name = name;
    if (phone) user.phone = phone;
    if (whatsapp) user.whatsapp = whatsapp;
    if (address) user.address = { ...user.address, ...address };
    if (company && user.document.type === 'CNPJ') {
        user.company = { ...user.company, ...company };
    }

    await user.save();

    res.status(200).json({
        success: true,
        message: 'Perfil atualizado com sucesso!',
        data: {
            user: user.toPublicJSON()
        }
    });
});

/**
 * @desc    Alterar senha
 * @route   PUT /api/auth/change-password
 * @access  Private
 */
const changePassword = asyncHandler(async (req, res, next) => {
    const { currentPassword, newPassword } = req.body;

    if (!currentPassword || !newPassword) {
        return next(new AppError('Por favor, forneça a senha atual e a nova senha', 400));
    }

    const user = await User.findById(req.user._id).select('+password');

    // Verificar senha atual
    const isPasswordMatch = await user.comparePassword(currentPassword);

    if (!isPasswordMatch) {
        return next(new AppError('Senha atual incorreta', 401));
    }

    // Atualizar senha
    user.password = newPassword;
    await user.save();

    res.status(200).json({
        success: true,
        message: 'Senha alterada com sucesso!'
    });
});

/**
 * @desc    Solicitar redefinição de senha
 * @route   POST /api/auth/forgot-password
 * @access  Public
 */
const forgotPassword = asyncHandler(async (req, res, next) => {
    const { email } = req.body;

    const user = await User.findOne({ email });

    if (!user) {
        // Não revelar se o email existe ou não (segurança)
        return res.status(200).json({
            success: true,
            message: 'Se o email existir, você receberá instruções para redefinir sua senha.'
        });
    }

    // Gerar token de reset
    const crypto = require('crypto');
    const resetToken = crypto.randomBytes(32).toString('hex');

    user.resetPasswordToken = crypto
        .createHash('sha256')
        .update(resetToken)
        .digest('hex');

    user.resetPasswordExpire = Date.now() + 30 * 60 * 1000; // 30 minutos

    await user.save({ validateBeforeSave: false });

    // TODO: Enviar email com o link de reset
    const resetUrl = `${process.env.CLIENT_URL}/reset-password/${resetToken}`;

    console.log('Reset URL:', resetUrl);

    res.status(200).json({
        success: true,
        message: 'Email de redefinição enviado!',
        // Em desenvolvimento, retornar o token
        ...(process.env.NODE_ENV === 'development' && { resetToken, resetUrl })
    });
});

/**
 * @desc    Redefinir senha
 * @route   PUT /api/auth/reset-password/:token
 * @access  Public
 */
const resetPassword = asyncHandler(async (req, res, next) => {
    const crypto = require('crypto');
    const resetPasswordToken = crypto
        .createHash('sha256')
        .update(req.params.token)
        .digest('hex');

    const user = await User.findOne({
        resetPasswordToken,
        resetPasswordExpire: { $gt: Date.now() }
    });

    if (!user) {
        return next(new AppError('Token inválido ou expirado', 400));
    }

    // Definir nova senha
    user.password = req.body.password;
    user.resetPasswordToken = undefined;
    user.resetPasswordExpire = undefined;

    await user.save();

    // Gerar novo token de autenticação
    const token = generateToken(user._id, user.role);

    res.status(200).json({
        success: true,
        message: 'Senha redefinida com sucesso!',
        data: {
            token
        }
    });
});

module.exports = {
    register,
    login,
    getMe,
    updateProfile,
    changePassword,
    forgotPassword,
    resetPassword
};
