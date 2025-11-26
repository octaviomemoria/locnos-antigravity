const mongoose = require('mongoose');

const categorySchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, 'Nome da categoria é obrigatório'],
        trim: true,
        maxlength: [100, 'Nome não pode ter mais de 100 caracteres']
    },
    slug: {
        type: String,
        required: true,
        unique: true,
        lowercase: true,
        trim: true
    },
    description: {
        type: String,
        maxlength: [500, 'Descrição não pode ter mais de 500 caracteres']
    },
    icon: String, // Nome do ícone ou URL
    image: String, // URL da imagem da categoria

    // Categoria pai (para subcategorias)
    parent: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Category',
        default: null
    },

    // Ordem de exibição
    order: {
        type: Number,
        default: 0
    },

    // Status
    active: {
        type: Boolean,
        default: true
    },

    // Metadados
    metadata: {
        totalEquipment: {
            type: Number,
            default: 0
        },
        popularityScore: {
            type: Number,
            default: 0
        }
    }
}, {
    timestamps: true
});

// Índices
categorySchema.index({ slug: 1 });
categorySchema.index({ parent: 1 });
categorySchema.index({ active: 1, order: 1 });

// Método para gerar slug automaticamente
categorySchema.pre('save', function (next) {
    if (this.isModified('name') && !this.slug) {
        this.slug = this.name
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '') // Remove acentos
            .replace(/[^a-z0-9\s-]/g, '')
            .replace(/\s+/g, '-')
            .replace(/-+/g, '-')
            .trim();
    }
    next();
});

module.exports = mongoose.model('Category', categorySchema);
