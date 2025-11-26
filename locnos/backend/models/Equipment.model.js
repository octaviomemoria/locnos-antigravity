const mongoose = require('mongoose');

const equipmentSchema = new mongoose.Schema({
    // Informações básicas
    name: {
        type: String,
        required: [true, 'Nome do equipamento é obrigatório'],
        trim: true,
        maxlength: [200, 'Nome não pode ter mais de 200 caracteres']
    },
    description: {
        type: String,
        required: [true, 'Descrição é obrigatória'],
        maxlength: [2000, 'Descrição não pode ter mais de 2000 caracteres']
    },

    // Categoria
    category: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Category',
        required: [true, 'Categoria é obrigatória']
    },

    // Identificação
    serialNumber: {
        type: String,
        unique: true,
        sparse: true,
        trim: true
    },
    barcode: {
        type: String,
        unique: true,
        sparse: true,
        trim: true
    },
    qrCode: String, // URL ou data do QR code
    internalCode: {
        type: String,
        required: true,
        unique: true,
        trim: true
    },

    // Especificações técnicas
    specifications: {
        brand: String,
        model: String,
        year: Number,
        weight: Number, // em kg
        dimensions: {
            length: Number,
            width: Number,
            height: Number,
            unit: {
                type: String,
                default: 'cm'
            }
        },
        power: String, // ex: "110V", "220V", "Bateria"
        capacity: String,
        custom: [{
            label: String,
            value: String
        }]
    },

    // Imagens
    images: [{
        url: {
            type: String,
            required: true
        },
        alt: String,
        isPrimary: {
            type: Boolean,
            default: false
        },
        order: {
            type: Number,
            default: 0
        }
    }],

    // Preços de locação
    pricing: {
        dailyRate: {
            type: Number,
            required: [true, 'Preço diário é obrigatório'],
            min: 0
        },
        weeklyRate: {
            type: Number,
            min: 0
        },
        monthlyRate: {
            type: Number,
            min: 0
        },
        hourlyRate: {
            type: Number,
            min: 0
        },
        minimumRentalPeriod: {
            value: {
                type: Number,
                default: 1
            },
            unit: {
                type: String,
                enum: ['hour', 'day', 'week', 'month'],
                default: 'day'
            }
        },
        depositRequired: {
            type: Number,
            default: 0,
            min: 0
        },
        replacementValue: Number // Valor de reposição
    },

    // Status e disponibilidade
    status: {
        type: String,
        enum: ['available', 'rented', 'reserved', 'maintenance', 'retired'],
        default: 'available',
        required: true
    },

    // Quantidade (para itens não-únicos)
    quantity: {
        total: {
            type: Number,
            default: 1,
            min: 0
        },
        available: {
            type: Number,
            default: 1,
            min: 0
        },
        rented: {
            type: Number,
            default: 0,
            min: 0
        },
        reserved: {
            type: Number,
            default: 0,
            min: 0
        },
        maintenance: {
            type: Number,
            default: 0,
            min: 0
        }
    },

    // Localização
    location: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Location'
    },
    currentLocation: String, // Descrição da localização atual

    // Dados de aquisição
    acquisition: {
        date: Date,
        cost: Number,
        supplier: String,
        warranty: {
            expirationDate: Date,
            description: String
        }
    },

    // Manutenção
    maintenance: {
        lastMaintenance: Date,
        nextMaintenance: Date,
        maintenanceInterval: Number, // em dias
        totalMaintenanceCost: {
            type: Number,
            default: 0
        },
        maintenanceHistory: [{
            type: mongoose.Schema.Types.ObjectId,
            ref: 'Maintenance'
        }]
    },

    // Estatísticas de uso
    usage: {
        totalRentals: {
            type: Number,
            default: 0
        },
        totalDaysRented: {
            type: Number,
            default: 0
        },
        totalRevenue: {
            type: Number,
            default: 0
        },
        utilizationRate: {
            type: Number,
            default: 0,
            min: 0,
            max: 100
        },
        lastRentalDate: Date
    },

    // Acessórios/Componentes inclusos
    accessories: [{
        name: String,
        quantity: Number,
        required: {
            type: Boolean,
            default: true
        }
    }],

    // Instruções e observações
    instructions: {
        usage: String,
        safety: String,
        maintenance: String
    },
    notes: String, // Observações internas

    // Visibilidade no catálogo
    visible: {
        type: Boolean,
        default: true
    },
    featured: {
        type: Boolean,
        default: false
    },

    // Tags para busca
    tags: [String],

    // Criador/Editor
    createdBy: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    },
    updatedBy: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    }
}, {
    timestamps: true
});

// Índices para performance
equipmentSchema.index({ name: 'text', description: 'text', tags: 'text' });
equipmentSchema.index({ category: 1, status: 1 });
equipmentSchema.index({ barcode: 1 });
equipmentSchema.index({ internalCode: 1 });
equipmentSchema.index({ status: 1, visible: 1 });
equipmentSchema.index({ 'pricing.dailyRate': 1 });

// Virtual para imagem principal
equipmentSchema.virtual('primaryImage').get(function () {
    const primary = this.images.find(img => img.isPrimary);
    return primary ? primary.url : (this.images.length > 0 ? this.images[0].url : null);
});

// Método para verificar disponibilidade
equipmentSchema.methods.isAvailable = function (quantity = 1) {
    return this.status === 'available' && this.quantity.available >= quantity;
};

// Método para calcular preço baseado no período
equipmentSchema.methods.calculatePrice = function (startDate, endDate) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24));

    // Se tem preço mensal e são mais de 25 dias
    if (this.pricing.monthlyRate && days >= 25) {
        const months = Math.ceil(days / 30);
        return this.pricing.monthlyRate * months;
    }

    // Se tem preço semanal e são mais de 5 dias
    if (this.pricing.weeklyRate && days >= 5) {
        const weeks = Math.ceil(days / 7);
        return this.pricing.weeklyRate * weeks;
    }

    // Preço diário padrão
    return this.pricing.dailyRate * days;
};

// Middleware para validar quantidade
equipmentSchema.pre('save', function (next) {
    // Garantir que available + rented + reserved + maintenance = total
    const sum = this.quantity.available + this.quantity.rented +
        this.quantity.reserved + this.quantity.maintenance;

    if (sum !== this.quantity.total) {
        this.quantity.total = sum;
    }

    next();
});

module.exports = mongoose.model('Equipment', equipmentSchema);
