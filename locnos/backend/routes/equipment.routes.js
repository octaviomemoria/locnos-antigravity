const express = require('express');
const router = express.Router();
const {
    getAllEquipment,
    getEquipmentById,
    createEquipment,
    updateEquipment,
    deleteEquipment,
    checkAvailability,
    getEquipmentStats
} = require('../controllers/equipment.controller');
const { protect, authorize, optionalAuth, checkPermission } = require('../middleware/auth.middleware');

// Rotas públicas (com auth opcional para personalização)
router.get('/', optionalAuth, getAllEquipment);
router.get('/:id', optionalAuth, getEquipmentById);
router.post('/:id/check-availability', checkAvailability);

// Rotas protegidas - Admin/Staff
router.post(
    '/',
    protect,
    authorize('admin', 'super_admin', 'staff'),
    checkPermission('manage_equipment'),
    createEquipment
);

router.put(
    '/:id',
    protect,
    authorize('admin', 'super_admin', 'staff'),
    checkPermission('manage_equipment'),
    updateEquipment
);

router.delete(
    '/:id',
    protect,
    authorize('admin', 'super_admin'),
    checkPermission('manage_equipment'),
    deleteEquipment
);

router.get(
    '/:id/stats',
    protect,
    authorize('admin', 'super_admin', 'staff'),
    checkPermission('view_reports'),
    getEquipmentStats
);

module.exports = router;
