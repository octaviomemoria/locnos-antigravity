const Equipment = require('../models/Equipment.model');
const { asyncHandler, AppError } = require('../middleware/error.middleware');

/**
 * @desc    Listar equipamentos com filtros, busca e paginação
 * @route   GET /api/equipment
 * @access  Public
 */
const getAllEquipment = asyncHandler(async (req, res, next) => {
    const {
        category,
        status,
        search,
        minPrice,
        maxPrice,
        featured,
        page = 1,
        limit = 20,
        sort = '-createdAt'
    } = req.query;

    // Construir query
    const query = {};

    // Apenas equipamentos visíveis para usuários não-admin
    if (!req.user || !['admin', 'super_admin', 'staff'].includes(req.user.role)) {
        query.visible = true;
    }

    if (category) query.category = category;
    if (status) query.status = status;
    if (featured) query.featured = featured === 'true';

    // Filtro de preço
    if (minPrice || maxPrice) {
        query['pricing.dailyRate'] = {};
        if (minPrice) query['pricing.dailyRate'].$gte = parseFloat(minPrice);
        if (maxPrice) query['pricing.dailyRate'].$lte = parseFloat(maxPrice);
    }

    // Busca por texto
    if (search) {
        query.$text = { $search: search };
    }

    // Paginação
    const skip = (page - 1) * limit;

    // Executar query
    const equipment = await Equipment.find(query)
        .populate('category', 'name slug')
        .sort(sort)
        .skip(skip)
        .limit(parseInt(limit))
        .select('-__v');

    // Contar total
    const total = await Equipment.countDocuments(query);

    res.status(200).json({
        success: true,
        data: {
            equipment,
            pagination: {
                total,
                page: parseInt(page),
                pages: Math.ceil(total / limit),
                limit: parseInt(limit)
            }
        }
    });
});

/**
 * @desc    Obter equipamento por ID
 * @route   GET /api/equipment/:id
 * @access  Public
 */
const getEquipmentById = asyncHandler(async (req, res, next) => {
    const equipment = await Equipment.findById(req.params.id)
        .populate('category', 'name slug description')
        .populate('location', 'name address');

    if (!equipment) {
        return next(new AppError('Equipamento não encontrado', 404));
    }

    // Verificar visibilidade
    if (!equipment.visible && (!req.user || !['admin', 'super_admin', 'staff'].includes(req.user.role))) {
        return next(new AppError('Equipamento não encontrado', 404));
    }

    res.status(200).json({
        success: true,
        data: {
            equipment
        }
    });
});

/**
 * @desc    Criar novo equipamento
 * @route   POST /api/equipment
 * @access  Private (Admin/Staff)
 */
const createEquipment = asyncHandler(async (req, res, next) => {
    // Adicionar usuário que criou
    req.body.createdBy = req.user._id;

    // Gerar código interno automático se não fornecido
    if (!req.body.internalCode) {
        const count = await Equipment.countDocuments();
        req.body.internalCode = `EQ${String(count + 1).padStart(6, '0')}`;
    }

    const equipment = await Equipment.create(req.body);

    res.status(201).json({
        success: true,
        message: 'Equipamento criado com sucesso!',
        data: {
            equipment
        }
    });
});

/**
 * @desc    Atualizar equipamento
 * @route   PUT /api/equipment/:id
 * @access  Private (Admin/Staff)
 */
const updateEquipment = asyncHandler(async (req, res, next) => {
    let equipment = await Equipment.findById(req.params.id);

    if (!equipment) {
        return next(new AppError('Equipamento não encontrado', 404));
    }

    // Adicionar usuário que atualizou
    req.body.updatedBy = req.user._id;

    // Não permitir alterar campos sensíveis via este endpoint
    delete req.body.createdBy;
    delete req.body.usage;

    equipment = await Equipment.findByIdAndUpdate(
        req.params.id,
        req.body,
        {
            new: true,
            runValidators: true
        }
    );

    res.status(200).json({
        success: true,
        message: 'Equipamento atualizado com sucesso!',
        data: {
            equipment
        }
    });
});

/**
 * @desc    Deletar equipamento
 * @route   DELETE /api/equipment/:id
 * @access  Private (Admin)
 */
const deleteEquipment = asyncHandler(async (req, res, next) => {
    const equipment = await Equipment.findById(req.params.id);

    if (!equipment) {
        return next(new AppError('Equipamento não encontrado', 404));
    }

    // Verificar se não está em uso
    if (equipment.status === 'rented' || equipment.status === 'reserved') {
        return next(new AppError('Não é possível deletar equipamento em uso', 400));
    }

    await equipment.deleteOne();

    res.status(200).json({
        success: true,
        message: 'Equipamento deletado com sucesso!'
    });
});

/**
 * @desc    Verificar disponibilidade de equipamento
 * @route   POST /api/equipment/:id/check-availability
 * @access  Public
 */
const checkAvailability = asyncHandler(async (req, res, next) => {
    const { startDate, endDate, quantity = 1 } = req.body;

    if (!startDate || !endDate) {
        return next(new AppError('Datas de início e fim são obrigatórias', 400));
    }

    const equipment = await Equipment.findById(req.params.id);

    if (!equipment) {
        return next(new AppError('Equipamento não encontrado', 404));
    }

    // TODO: Verificar reservas conflitantes no banco de contratos
    // Por enquanto, apenas verificar quantidade disponível
    const isAvailable = equipment.quantity.available >= quantity;

    res.status(200).json({
        success: true,
        data: {
            available: isAvailable,
            quantityAvailable: equipment.quantity.available,
            quantityRequested: quantity,
            price: equipment.calculatePrice(startDate, endDate)
        }
    });
});

/**
 * @desc    Obter estatísticas de equipamento
 * @route   GET /api/equipment/:id/stats
 * @access  Private (Admin/Staff)
 */
const getEquipmentStats = asyncHandler(async (req, res, next) => {
    const equipment = await Equipment.findById(req.params.id);

    if (!equipment) {
        return next(new AppError('Equipamento não encontrado', 404));
    }

    // Calcular ROI
    const roi = equipment.acquisition?.cost
        ? ((equipment.usage.totalRevenue - equipment.acquisition.cost - equipment.maintenance.totalMaintenanceCost) / equipment.acquisition.cost * 100).toFixed(2)
        : 0;

    res.status(200).json({
        success: true,
        data: {
            totalRentals: equipment.usage.totalRentals,
            totalDaysRented: equipment.usage.totalDaysRented,
            totalRevenue: equipment.usage.totalRevenue,
            utilizationRate: equipment.usage.utilizationRate,
            acquisitionCost: equipment.acquisition?.cost || 0,
            maintenanceCost: equipment.maintenance.totalMaintenanceCost,
            roi,
            lastRental: equipment.usage.lastRentalDate
        }
    });
});

module.exports = {
    getAllEquipment,
    getEquipmentById,
    createEquipment,
    updateEquipment,
    deleteEquipment,
    checkAvailability,
    getEquipmentStats
};
