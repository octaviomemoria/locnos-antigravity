require('dotenv').config();
const { prisma } = require('./config/database');
const bcrypt = require('bcryptjs');

async function main() {
    try {
        console.log('🌱 Iniciando seed do banco de dados Supabase...\n');

        // Limpar dados existentes (apenas em desenvolvimento)
        if (process.env.NODE_ENV === 'development') {
            console.log('🗑️  Limpando dados antigos...');
            await prisma.contractItem.deleteMany({});
            await prisma.payment.deleteMany({});
            await prisma.contract.deleteMany({});
            await prisma.maintenance.deleteMany({});
            await prisma.equipment.deleteMany({});
            await prisma.category.deleteMany({});
            await prisma.location.deleteMany({});
            await prisma.user.deleteMany({});
            console.log('✅ Dados antigos removidos\n');
        }

        // === CRIAR USUÁRIOS ===
        console.log('👥 Criando usuários...');

        const hashedPassword = await bcrypt.hash('admin123', 10);
        const hashedPasswordCustomer = await bcrypt.hash('senha123', 10);

        const superAdmin = await prisma.user.create({
            data: {
                name: 'Super Admin',
                email: 'admin@locnos.com.br',
                password: hashedPassword,
                role: 'SUPER_ADMIN',
                phone: '+5511999999999',
                documentType: 'CPF',
                documentNumber: '12345678900',
                documentVerified: true,
                status: 'ACTIVE',
                permissions: [
                    'manage_equipment',
                    'manage_contracts',
                    'manage_customers',
                    'manage_financial',
                    'manage_users',
                    'manage_settings',
                    'view_reports'
                ]
            }
        });

        const customer = await prisma.user.create({
            data: {
                name: 'João Silva',
                email: 'joao@email.com',
                password: hashedPasswordCustomer,
                role: 'CUSTOMER',
                phone: '+5511988888888',
                documentType: 'CPF',
                documentNumber: '98765432100',
                documentVerified: true,
                addressStreet: 'Rua das Flores',
                addressNumber: '123',
                addressNeighborhood: 'Centro',
                addressCity: 'São Paulo',
                addressState: 'SP',
                addressZipCode: '01234567',
                addressCountry: 'Brasil',
                status: 'ACTIVE'
            }
        });

        console.log(`✅ ${superAdmin.name} (${superAdmin.email})`);
        console.log(`✅ ${customer.name} (${customer.email})\n`);

        // === CRIAR CATEGORIAS ===
        console.log('📦 Criando categorias...');

        const categorias = await Promise.all([
            prisma.category.create({
                data: {
                    name: 'Construção Civil',
                    slug: 'construcao-civil',
                    description: 'Equipamentos para construção e reforma',
                    icon: 'construction',
                    order: 1,
                    active: true
                }
            }),
            prisma.category.create({
                data: {
                    name: 'Festas e Eventos',
                    slug: 'festas-e-eventos',
                    description: 'Equipamentos para festas, casamentos e eventos',
                    icon: 'celebration',
                    order: 2,
                    active: true
                }
            }),
            prisma.category.create({
                data: {
                    name: 'Equipamentos Médicos',
                    slug: 'equipamentos-medicos',
                    description: 'Equipamentos hospitalares e de saúde',
                    icon: 'medical',
                    order: 3,
                    active: true
                }
            }),
            prisma.category.create({
                data: {
                    name: 'Utilidades Domésticas',
                    slug: 'utilidades-domesticas',
                    description: 'Equipamentos para uso doméstico',
                    icon: 'home',
                    order: 4,
                    active: true
                }
            })
        ]);

        categorias.forEach(cat => console.log(`✅ ${cat.name}`));
        console.log('');

        // === CRIAR EQUIPAMENTOS ===
        console.log('🔧 Criando equipamentos...\n');

        const equipamentos = await Promise.all([
            // Construção Civil
            prisma.equipment.create({
                data: {
                    name: 'Betoneira 400L',
                    description: 'Betoneira profissional com capacidade de 400 litros, ideal para obras de médio porte.',
                    categoryId: categorias[0].id,
                    internalCode: 'EQ000001',
                    barcode: '7894561230001',
                    specifications: {
                        brand: 'Maqmix',
                        model: 'BT-400',
                        power: '220V Monofásico',
                        capacity: '400 litros',
                        motorPower: '2 CV',
                        rotation: '25 RPM'
                    },
                    images: [
                        {
                            url: 'https://via.placeholder.com/800x600.png?text=Betoneira+400L',
                            alt: 'Betoneira 400L',
                            isPrimary: true,
                            order: 0
                        }
                    ],
                    dailyRate: 80,
                    weeklyRate: 400,
                    monthlyRate: 1200,
                    depositRequired: 500,
                    minimumRentalValue: 1,
                    minimumRentalUnit: 'day',
                    status: 'AVAILABLE',
                    quantityTotal: 3,
                    quantityAvailable: 3,
                    quantityRented: 0,
                    visible: true,
                    featured: true,
                    tags: ['construção', 'betoneira', 'obra', 'concreto'],
                    createdById: superAdmin.id
                }
            }),

            prisma.equipment.create({
                data: {
                    name: 'Andaime Metálico 2m',
                    description: 'Andaime tubular metálico com 2 metros de altura, seguro e resistente.',
                    categoryId: categorias[0].id,
                    internalCode: 'EQ000002',
                    specifications: {
                        brand: 'Fermar',
                        model: 'AND-200',
                        dimensions: { length: 200, width: 100, height: 200, unit: 'cm' },
                        weight: 45
                    },
                    images: [
                        {
                            url: 'https://via.placeholder.com/800x600.png?text=Andaime+Metalico',
                            alt: 'Andaime Metálico',
                            isPrimary: true,
                            order: 0
                        }
                    ],
                    dailyRate: 30,
                    weeklyRate: 150,
                    monthlyRate: 450,
                    depositRequired: 300,
                    status: 'AVAILABLE',
                    quantityTotal: 5,
                    quantityAvailable: 4,
                    quantityRented: 1,
                    visible: true,
                    tags: ['construção', 'andaime', 'altura', 'segurança'],
                    createdById: superAdmin.id
                }
            }),

            // Festas e Eventos
            prisma.equipment.create({
                data: {
                    name: 'Mesa Redonda 1,50m',
                    description: 'Mesa redonda de plástico resistente com 1,50m de diâmetro, ideal para eventos.',
                    categoryId: categorias[1].id,
                    internalCode: 'EQ000003',
                    specifications: {
                        brand: 'Plasútil',
                        dimensions: { length: 150, width: 150, height: 75, unit: 'cm' },
                        capacity: 'Até 8 pessoas'
                    },
                    images: [
                        {
                            url: 'https://via.placeholder.com/800x600.png?text=Mesa+Redonda',
                            alt: 'Mesa Redonda',
                            isPrimary: true,
                            order: 0
                        }
                    ],
                    dailyRate: 25,
                    weeklyRate: 100,
                    depositRequired: 50,
                    status: 'AVAILABLE',
                    quantityTotal: 20,
                    quantityAvailable: 15,
                    quantityRented: 5,
                    visible: true,
                    featured: true,
                    tags: ['festa', 'evento', 'mesa', 'casamento'],
                    createdById: superAdmin.id
                }
            }),

            prisma.equipment.create({
                data: {
                    name: 'Cadeira de Plástico',
                    description: 'Cadeira plástica branca, empilhável, resistente e confortável.',
                    categoryId: categorias[1].id,
                    internalCode: 'EQ000004',
                    specifications: {
                        brand: 'Tramontina',
                        weight: 3,
                        maxWeight: '120 kg',
                        color: 'Branca'
                    },
                    images: [
                        {
                            url: 'https://via.placeholder.com/800x600.png?text=Cadeira+Plastica',
                            alt: 'Cadeira Plástica',
                            isPrimary: true,
                            order: 0
                        }
                    ],
                    dailyRate: 5,
                    weeklyRate: 20,
                    depositRequired: 10,
                    status: 'AVAILABLE',
                    quantityTotal: 100,
                    quantityAvailable: 80,
                    quantityRented: 20,
                    visible: true,
                    tags: ['festa', 'evento', 'cadeira', 'assento'],
                    createdById: superAdmin.id
                }
            }),

            // Equipamentos Médicos
            prisma.equipment.create({
                data: {
                    name: 'Cadeira de Rodas Dobrável',
                    description: 'Cadeira de rodas dobrável, leve e resistente, com aros de propulsão.',
                    categoryId: categorias[2].id,
                    internalCode: 'EQ000005',
                    specifications: {
                        brand: 'Ortobras',
                        model: 'CR-1012',
                        weight: 15,
                        maxWeight: '120 kg',
                        material: 'Aço carbono',
                        seatWidth: '46 cm'
                    },
                    images: [
                        {
                            url: 'https://via.placeholder.com/800x600.png?text=Cadeira+de+Rodas',
                            alt: 'Cadeira de Rodas',
                            isPrimary: true,
                            order: 0
                        }
                    ],
                    dailyRate: 15,
                    weeklyRate: 70,
                    monthlyRate: 200,
                    depositRequired: 100,
                    status: 'AVAILABLE',
                    quantityTotal: 8,
                    quantityAvailable: 6,
                    quantityRented: 2,
                    visible: true,
                    featured: true,
                    tags: ['saúde', 'médico', 'cadeira', 'mobilidade'],
                    createdById: superAdmin.id
                }
            }),

            // Utilidades Domésticas
            prisma.equipment.create({
                data: {
                    name: 'Lavadora de Alta Pressão',
                    description: 'Lavadora de alta pressão profissional 1800W, ideal para limpeza de pisos, muros e veículos.',
                    categoryId: categorias[3].id,
                    internalCode: 'EQ000006',
                    specifications: {
                        brand: 'Karcher',
                        model: 'K3',
                        power: '110V',
                        maxPressure: '120 bar',
                        flow: '380 L/h',
                        motorPower: '1800W'
                    },
                    images: [
                        {
                            url: 'https://via.placeholder.com/800x600.png?text=Lavadora+Alta+Pressao',
                            alt: 'Lavadora de Alta Pressão',
                            isPrimary: true,
                            order: 0
                        }
                    ],
                    dailyRate: 45,
                    weeklyRate: 200,
                    monthlyRate: 600,
                    depositRequired: 200,
                    status: 'AVAILABLE',
                    quantityTotal: 4,
                    quantityAvailable: 3,
                    quantityRented: 1,
                    visible: true,
                    tags: ['limpeza', 'lavadora', 'pressão', 'doméstico'],
                    createdById: superAdmin.id
                }
            })
        ]);

        equipamentos.forEach(eq => console.log(`✅ ${eq.name} (${eq.internalCode})`));

        console.log(`\n✅ Seed concluído com sucesso!`);
        console.log(`\n📊 Resumo:`);
        console.log(`   - ${await prisma.user.count()} usuários`);
        console.log(`   - ${await prisma.category.count()} categorias`);
        console.log(`   - ${await prisma.equipment.count()} equipamentos`);
        console.log(`\n🔑 Credenciais de acesso:`);
        console.log(`   Admin: admin@locnos.com.br / admin123`);
        console.log(`   Cliente: joao@email.com / senha123`);
        console.log(`\n💡 Explore o banco: npx prisma studio\n`);

    } catch (error) {
        console.error('❌ Erro no seed:', error);
        throw error;
    } finally {
        await prisma.$disconnect();
    }
}

main()
    .catch((e) => {
        console.error(e);
        process.exit(1);
    });
