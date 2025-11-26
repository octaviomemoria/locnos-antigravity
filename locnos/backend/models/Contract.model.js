const mongoose = require('mongoose');

const contractSchema = new mongoose.Schema({
    // Número do contrato
    contractNumber: {
        type: String,
        required: true,
        unique: true
    },

    // Cliente
    customer: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: [true, 'Cliente é obrigatório']
    },

    // Status do contrato
    status: {
        type: String,
        enum: [
            'quotation',      // Orçamento solicitado
            'pending',        // Aguardando aprovação
            'approved',       // Aprovado, aguardando retirada
            'active',         // Ativo (equipamento com cliente)
            'completed',      // Concluído (devolvido)
            'cancelled',      // Cancelado
            'overdue'         // Atrasado
        ],
        default: 'quotation',
        required: true
    },

    // Itens do contrato
    items: [{
        equipment: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'Equipment',
            required: true
        },
        quantity: {
            type: Number,
            required: true,
            min: 1,
            default: 1
        },
        unitPrice: {
            type: Number,
            required: true,
            min: 0
        },
        subtotal: {
            type: Number,
            required: true,
            min: 0
        },
        // Acessórios específicos para este item
        accessories: [{
            name: String,
            quantity: Number,
            returned: {
                type: Boolean,
                default: false
            }
        }],
        // Condição no momento da retirada
        condition: {
            type: String,
            enum: ['excellent', 'good', 'fair', 'poor'],
            default: 'good'
        },
        conditionNotes: String,
        // Condição na devolução
        returnCondition: {
            type: String,
            enum: ['excellent', 'good', 'fair', 'poor', 'damaged']
        },
        returnNotes: String,
        damageCost: {
            type: Number,
            default: 0
        }
    }],

    // Período de locação
    rentalPeriod: {
        startDate: {
            type: Date,
            required: [true, 'Data de início é obrigatória']
        },
        endDate: {
            type: Date,
            required: [true, 'Data de término é obrigatória']
        },
        actualStartDate: Date, // Data real de retirada
        actualEndDate: Date,   // Data real de devolução
        rentalDays: Number,
        extraDays: {
            type: Number,
            default: 0
        }
    },

    // Valores financeiros
    financial: {
        subtotal: {
            type: Number,
            required: true,
            min: 0
        },
        discount: {
            amount: {
                type: Number,
                default: 0,
                min: 0
            },
            percentage: {
                type: Number,
                default: 0,
                min: 0,
                max: 100
            },
            reason: String
        },
        deposit: {
            type: Number,
            default: 0,
            min: 0
        },
        lateFees: {
            type: Number,
            default: 0,
            min: 0
        },
        damageFees: {
            type: Number,
            default: 0,
            min: 0
        },
        additionalFees: [{
            description: String,
            amount: Number
        }],
        total: {
            type: Number,
            required: true,
            min: 0
        },
        totalPaid: {
            type: Number,
            default: 0,
            min: 0
        },
        balance: {
            type: Number,
            default: 0
        }
    },

    // Pagamento
    paymentStatus: {
        type: String,
        enum: ['pending', 'partial', 'paid', 'overdue', 'refunded'],
        default: 'pending'
    },
    paymentMethod: {
        type: String,
        enum: ['cash', 'credit_card', 'debit_card', 'pix', 'boleto', 'bank_transfer', 'multiple'],
        default: 'cash'
    },
    payments: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Payment'
    }],

    // Logística
    delivery: {
        required: {
            type: Boolean,
            default: false
        },
        address: {
            street: String,
            number: String,
            complement: String,
            neighborhood: String,
            city: String,
            state: String,
            zipCode: String
        },
        scheduledDate: Date,
        completedDate: Date,
        cost: {
            type: Number,
            default: 0
        },
        instructions: String,
        deliveredBy: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'User'
        },
        proof: String // URL da foto/assinatura de entrega
    },

    pickup: {
        required: {
            type: Boolean,
            default: false
        },
        scheduledDate: Date,
        completedDate: Date,
        cost: {
            type: Number,
            default: 0
        },
        pickedUpBy: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'User'
        },
        proof: String
    },

    // Documentos
    documents: {
        contract: String,      // URL do PDF do contrato
        invoice: String,       // URL da nota fiscal
        receipt: String,       // URL do recibo
        deliveryReceipt: String,
        returnReceipt: String
    },

    // Notas fiscais
    fiscalNotes: [{
        type: {
            type: String,
            enum: ['NFe', 'NFSe', 'Remessa', 'Devolução']
        },
        number: String,
        key: String,
        issueDate: Date,
        xmlUrl: String,
        pdfUrl: String
    }],

    // Termos e condições
    terms: {
        accepted: {
            type: Boolean,
            default: false
        },
        acceptedAt: Date,
        acceptedIp: String,
        customTerms: String,
        signature: String // URL da assinatura digital
    },

    // Observações
    notes: String,
    internalNotes: String, // Visível apenas para staff

    // Responsáveis
    createdBy: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    },
    approvedBy: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    },
    approvedAt: Date,

    // Renovações
    renewedFrom: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Contract'
    },
    renewedTo: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Contract'
    }
}, {
    timestamps: true
});

// Índices
contractSchema.index({ contractNumber: 1 });
contractSchema.index({ customer: 1, status: 1 });
contractSchema.index({ status: 1, 'rentalPeriod.endDate': 1 });
contractSchema.index({ 'rentalPeriod.startDate': 1, 'rentalPeriod.endDate': 1 });
contractSchema.index({ createdAt: -1 });

// Gerar número de contrato automaticamente
contractSchema.pre('save', async function (next) {
    if (!this.contractNumber) {
        const year = new Date().getFullYear();
        const month = String(new Date().getMonth() + 1).padStart(2, '0');

        // Buscar o último contrato do mês
        const lastContract = await this.constructor
            .findOne({ contractNumber: new RegExp(`^${year}${month}`) })
            .sort({ contractNumber: -1 })
            .select('contractNumber');

        let sequence = 1;
        if (lastContract) {
            const lastSequence = parseInt(lastContract.contractNumber.slice(-4));
            sequence = lastSequence + 1;
        }

        this.contractNumber = `${year}${month}${String(sequence).padStart(4, '0')}`;
    }

    // Calcular dias de locação
    if (this.rentalPeriod.startDate && this.rentalPeriod.endDate) {
        const start = new Date(this.rentalPeriod.startDate);
        const end = new Date(this.rentalPeriod.endDate);
        this.rentalPeriod.rentalDays = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
    }

    // Calcular dias extras se houver devolução com atraso
    if (this.rentalPeriod.actualEndDate && this.rentalPeriod.endDate) {
        const planned = new Date(this.rentalPeriod.endDate);
        const actual = new Date(this.rentalPeriod.actualEndDate);
        const extraDays = Math.ceil((actual - planned) / (1000 * 60 * 60 * 24));
        if (extraDays > 0) {
            this.rentalPeriod.extraDays = extraDays;
        }
    }

    // Calcular balanço
    this.financial.balance = this.financial.total - this.financial.totalPaid;

    next();
});

// Método para verificar se está atrasado
contractSchema.methods.isOverdue = function () {
    if (this.status !== 'active') return false;

    const now = new Date();
    const endDate = new Date(this.rentalPeriod.endDate);
    return now > endDate;
};

// Método para calcular multa por atraso
contractSchema.methods.calculateLateFee = function (lateFeePerDay = 0) {
    if (!this.isOverdue()) return 0;

    const now = new Date();
    const endDate = new Date(this.rentalPeriod.endDate);
    const daysLate = Math.ceil((now - endDate) / (1000 * 60 * 60 * 24));

    return daysLate * lateFeePerDay;
};

// Virtual para check-in/check-out
contractSchema.virtual('isCheckedOut').get(function () {
    return this.rentalPeriod.actualStartDate !== undefined;
});

contractSchema.virtual('isCheckedIn').get(function () {
    return this.rentalPeriod.actualEndDate !== undefined;
});

module.exports = mongoose.model('Contract', contractSchema);
