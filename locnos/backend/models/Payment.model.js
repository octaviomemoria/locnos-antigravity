const mongoose = require('mongoose');

const paymentSchema = new mongoose.Schema({
    // Referência ao contrato
    contract: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Contract',
        required: [true, 'Contrato é obrigatório']
    },

    // Cliente
    customer: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: [true, 'Cliente é obrigatório']
    },

    // Tipo de pagamento
    type: {
        type: String,
        enum: ['deposit', 'rental', 'late_fee', 'damage', 'additional', 'refund'],
        required: true
    },

    // Método de pagamento
    method: {
        type: String,
        enum: ['cash', 'credit_card', 'debit_card', 'pix', 'boleto', 'bank_transfer'],
        required: true
    },

    // Valores
    amount: {
        type: Number,
        required: [true, 'Valor é obrigatório'],
        min: 0
    },

    // Status
    status: {
        type: String,
        enum: ['pending', 'processing', 'paid', 'failed', 'cancelled', 'refunded'],
        default: 'pending',
        required: true
    },

    // Datas
    dueDate: Date,
    paidAt: Date,
    cancelledAt: Date,
    refundedAt: Date,

    // Informações de pagamento externo
    externalPayment: {
        gateway: String,           // Ex: 'mercadopago', 'pagseguro'
        transactionId: String,     // ID da transação no gateway
        authorizationCode: String,
        paymentLink: String,       // Link do boleto, PIX, etc
        qrCode: String,            // QR Code do PIX
        barcode: String,           // Código de barras do boleto
        pixKey: String,            // Chave PIX
        expiresAt: Date           // Quando expira (boleto/pix)
    },

    // Dados do cartão (nunca salvar número completo)
    cardInfo: {
        brand: String,             // 'visa', 'mastercard', etc
        lastDigits: String,        // Últimos 4 dígitos
        holderName: String,
        installments: {
            type: Number,
            default: 1
        }
    },

    // Comprovante
    receipt: {
        url: String,
        number: String,
        issueDate: Date
    },

    // Nota fiscal relacionada
    invoice: {
        number: String,
        key: String,
        url: String
    },

    // Descrição e observações
    description: String,
    notes: String,

    // Quem registrou o pagamento
    processedBy: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    },

    // Reembolso (se aplicável)
    refund: {
        amount: Number,
        reason: String,
        processedAt: Date,
        processedBy: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'User'
        }
    },

    // Webhook data (para debug)
    webhookData: mongoose.Schema.Types.Mixed
}, {
    timestamps: true
});

// Índices
paymentSchema.index({ contract: 1 });
paymentSchema.index({ customer: 1 });
paymentSchema.index({ status: 1, dueDate: 1 });
paymentSchema.index({ 'externalPayment.transactionId': 1 });
paymentSchema.index({ createdAt: -1 });

// Atualizar status automaticamente quando pago
paymentSchema.pre('save', function (next) {
    if (this.isModified('paidAt') && this.paidAt && this.status === 'pending') {
        this.status = 'paid';
    }
    next();
});

// Método para verificar se está vencido
paymentSchema.methods.isOverdue = function () {
    if (this.status === 'paid') return false;
    if (!this.dueDate) return false;

    return new Date() > new Date(this.dueDate);
};

// Método para gerar descrição automática
paymentSchema.methods.getDescription = function () {
    if (this.description) return this.description;

    const typeLabels = {
        'deposit': 'Caução',
        'rental': 'Aluguel',
        'late_fee': 'Multa por Atraso',
        'damage': 'Danos ao Equipamento',
        'additional': 'Taxa Adicional',
        'refund': 'Reembolso'
    };

    return typeLabels[this.type] || 'Pagamento';
};

module.exports = mongoose.model('Payment', paymentSchema);
