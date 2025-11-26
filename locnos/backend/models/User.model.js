// Timestamps
createdAt: {
    type: Date,
        default: Date.now
},
updatedAt: {
    type: Date,
        default: Date.now
},
lastLogin: Date
}, {
    timestamps: true
});

// Índices para busca rápida
userSchema.index({ email: 1 });
userSchema.index({ 'document.number': 1 });
userSchema.index({ role: 1, status: 1 });

// Hash da senha antes de salvar
userSchema.pre('save', async function (next) {
    if (!this.isModified('password')) {
        return next();
    }

    try {
        const salt = await bcrypt.genSalt(parseInt(process.env.BCRYPT_ROUNDS) || 10);
        this.password = await bcrypt.hash(this.password, salt);
        next();
    } catch (error) {
        next(error);
    }
});

// Método para comparar senha
userSchema.methods.comparePassword = async function (candidatePassword) {
    return await bcrypt.compare(candidatePassword, this.password);
};

// Método para gerar objeto público (sem dados sensíveis)
userSchema.methods.toPublicJSON = function () {
    const obj = this.toObject();
    delete obj.password;
    delete obj.resetPasswordToken;
    delete obj.resetPasswordExpire;
    return obj;
};

// Virtual para nome completo da empresa
userSchema.virtual('fullCompanyName').get(function () {
    if (this.document.type === 'CNPJ' && this.company) {
        return this.company.tradeName || this.company.name;
    }
    return null;
});

module.exports = mongoose.model('User', userSchema);
