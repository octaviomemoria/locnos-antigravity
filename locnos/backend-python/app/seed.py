"""
Seed do banco de dados com dados de exemplo atualizados
Popula: Users, Categories, Subcategorias, Persons (múltiplos tipos), Equipment (expandido)
"""

import sys
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole, UserStatus, DocumentType
from app.models.category import Category
# from app.models.subcategoria import Subcategoria
from app.models.person import Person, PersonType, PersonDocumentType, PersonStatus
from app.models.equipment import Equipment, EquipmentStatus


def seed_database():
    """Popular banco com dados de exemplo"""
    db = SessionLocal()
    
    try:
        print("🌱 Iniciando seed do banco de dados...")
        
        # ============================================================================
        # LIMPAR DADOS ANTIGOS
        # ============================================================================
        print("\n🗑️  Limpando dados antigos...")
        db.query(Equipment).delete()
        # db.query(Subcategoria).delete()
        db.query(Person).delete()
        db.query(Category).delete()
        db.query(User).delete()
        db.commit()
        print("✅ Dados antigos removidos")
        
        # ============================================================================
        # USUÁRIOS
        # ============================================================================
        print("\n👥 Criando usuários...")
        
        admin_user = User(
            email="admin@locnos.com.br",
            name="Administrador Sistema",
            password=get_password_hash("admin123"),
            role=UserRole.SUPER_ADMIN,
            status=UserStatus.ACTIVE,
            document_type=DocumentType.CPF,
            document_number="00000000000"
        )
        
        gerente_user = User(
            email="gerente@locnos.com.br",
            name="João Gerente",
            password=get_password_hash("gerente123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            document_type=DocumentType.CPF,
            document_number="11111111111"
        )
        
        atendente_user = User(
            email="atendente@locnos.com.br",
            name="Maria Atendente",
            password=get_password_hash("atendente123"),
            role=UserRole.STAFF,
            status=UserStatus.ACTIVE,
            document_type=DocumentType.CPF,
            document_number="22222222222"
        )
        
        db.add_all([admin_user, gerente_user, atendente_user])
        db.commit()
        db.refresh(admin_user)
        db.refresh(gerente_user)
        db.refresh(atendente_user)
        print(f"✅ {3} usuários criados")
        
        # ============================================================================
        # CATEGORIAS
        # ============================================================================
        print("\n📂 Criando categorias...")
        
        categorias_data = [
            {
                "name": "Construção Civil",
                "slug": "construcao-civil",
                "description": "Equipamentos para construção e reforma",
                "icon": "🏗️"
            },
            {
                "name": "Festas e Eventos",
                "slug": "festas-eventos",
                "description": "Equipamentos para festas, casamentos e eventos",
                "icon": "🎉"
            },
            {
                "name": "Equipamentos Médicos",
                "slug": "equipamentos-medicos",
                "description": "Equipamentos médicos e hospitalares",
                "icon": "🏥"
            },
            {
                "name": "Jardinagem",
                "slug": "jardinagem",
                "description": "Ferramentas e equipamentos para jardinagem",
                "icon": "🌿"
            }
        ]
        
        categorias = []
        for cat_data in categorias_data:
            cat = Category(**cat_data)
            db.add(cat)
            categorias.append(cat)
        
        db.commit()
        for cat in categorias:
            db.refresh(cat)
        print(f"✅ {len(categorias)} categorias criadas")
        
        # ============================================================================
        # SUBCATEGORIAS (Agora são Categorias com parent_id)
        # ============================================================================
        print("\n📑 Criando subcategorias...")
        
        subcategorias_data = [
            # Construção Civil
            {"name": "Ferramentas Elétricas", "slug": "ferramentas-eletricas", "parent_id": categorias[0].id, "order": 1},
            {"name": "Andaimes e Escadas", "slug": "andaimes-escadas", "parent_id": categorias[0].id, "order": 2},
            {"name": "Betoneiras e Misturadores", "slug": "betoneiras-misturadores", "parent_id": categorias[0].id, "order": 3},
            
            # Festas e Eventos
            {"name": "Iluminação", "slug": "iluminacao", "parent_id": categorias[1].id, "order": 1},
            {"name": "Som e Áudio", "slug": "som-audio", "parent_id": categorias[1].id, "order": 2},
            {"name": "Mobiliário", "slug": "mobiliario", "parent_id": categorias[1].id, "order": 3},
            
            # Equipamentos Médicos
            {"name": "Oxigenoterapia", "slug": "oxigenoterapia", "parent_id": categorias[2].id, "order": 1},
            {"name": "Mobilidade", "slug": "mobilidade", "parent_id": categorias[2].id, "order": 2},
            
            # Jardinagem
            {"name": "Corte e Poda", "slug": "corte-poda", "parent_id": categorias[3].id, "order": 1},
            {"name": "Limpeza", "slug": "limpeza", "parent_id": categorias[3].id, "order": 2},
        ]
        
        subcategorias = []
        for sub_data in subcategorias_data:
            sub = Category(**sub_data)
            db.add(sub)
            subcategorias.append(sub)
        
        db.commit()
        for sub in subcategorias:
            db.refresh(sub)
        print(f"✅ {len(subcategorias)} subcategorias criadas")
        
        # ============================================================================
        # PESSOAS (com múltiplos tipos)
        # ============================================================================
        print("\n👤 Criando pessoas...")
        
        # Pessoa 1: Cliente simples (PF)
        pessoa1 = Person(
            types=["client"],
            primary_type=PersonType.CLIENT,
            document_type=PersonDocumentType.CPF,
            full_name="Carlos Silva Santos",
            cpf="12345678901",
            rg="123456789",
            email="carlos.silva@email.com",
            phone="(11) 98765-4321",
            whatsapp="(11) 98765-4321",
            address={
                "cep": "01310-100",
                "street": "Av Paulista",
                "number": "1578",
                "complement": "Apto 10",
                "neighborhood": "Bela Vista",
                "city": "São Paulo",
                "state": "SP"
            },
            references=[
                {"id": "ref1", "name": "João Silva", "phone": "(11) 91234-5678", "relationship": "Irmão"},
                {"id": "ref2", "name": "Maria Santos", "phone": "(11) 99876-5432", "relationship": "Mãe"}
            ],
            status=PersonStatus.APPROVED,
            approved_by_id=admin_user.id,
            approved_at=datetime.utcnow(),
            customer_since=datetime.utcnow()
        )
        
        # Pessoa 2: Cliente + Freteiro (PF - múltiplos tipos!)
        pessoa2 = Person(
            types=["client", "driver"],
            primary_type=PersonType.CLIENT,
            document_type=PersonDocumentType.CPF,
            full_name="Pedro Oliveira Transportes",
            cpf="98765432109",
            rg="987654321",
            email="pedro.transportes@email.com",
            phone="(11) 97777-8888",
            whatsapp="(11) 97777-8888",
            address={
                "cep": "04543-907",
                "street": "Av Brigadeiro Faria Lima",
                "number": "3477",
                "neighborhood": "Itaim Bibi",
                "city": "São Paulo",
                "state": "SP"
            },
            references=[
                {"id": "ref1", "name": "Ana Oliveira", "phone": "(11) 96666-7777", "relationship": "Esposa"},
                {"id": "ref2", "name": "José Oliveira", "phone": "(11) 95555-6666", "relationship": "Pai"}
            ],
            driver_data={
                "vehicle_type": "Fiorino Furgão",
                "license_plate": "ABC-1D34",
                "drivers_license": "12345678901",
                "license_category": "B",
                "license_expiration": "2027-12-31",
                "available": True
            },
            status=PersonStatus.APPROVED,
            approved_by_id=admin_user.id,
            approved_at=datetime.utcnow(),
            customer_since=datetime.utcnow(),
            credit_limit=Decimal("5000.00")
        )
        
        # Pessoa 3: Fornecedor (PJ)
        pessoa3 = Person(
            types=["supplier"],
            primary_type=PersonType.SUPPLIER,
            document_type=PersonDocumentType.CNPJ,
            company_name="Equipamentos S Silva Ltda",
            trade_name="Silva Equipamentos",
            cnpj="12345678000190",
            state_registration="123456789",
            email="contato@silvaequipamentos.com.br",
            phone="(11) 3333-4444",
            address={
                "cep": "01310-200",
                "street": "Rua Augusta",
                "number": "2000",
                "neighborhood": "Consolação",
                "city": "São Paulo",
                "state": "SP"
            },
            supplier_data={
                "products": ["Betoneiras", "Andaimes", "Ferramentas Elétricas"],
                "bank": "Banco do Brasil",
                "agency": "1234-5",
                "account": "123456-7",
                "payment_terms": "30 dias"
            },
            status=PersonStatus.APPROVED,
            approved_by_id=admin_user.id,
            approved_at=datetime.utcnow()
        )
        
        # Pessoa 4: Freteiro puro (PF)
        pessoa4 = Person(
            types=["driver"],
            primary_type=PersonType.DRIVER,
            document_type=PersonDocumentType.CPF,
            full_name="Roberto Caminhoneiro",
            cpf="11122233344",
            email="roberto.frete@email.com",
            phone="(11) 94444-5555",
            driver_data={
                "vehicle_type": "Caminhão Baú",
                "license_plate": "XYZ-9876",
                "drivers_license": "98765432109",
                "license_category": "D",
                "license_expiration": "2026-06-30",
                "available": True
            },
            status=PersonStatus.APPROVED,
            approved_by_id=admin_user.id,
            approved_at=datetime.utcnow()
        )
        
        db.add_all([pessoa1, pessoa2, pessoa3, pessoa4])
        db.commit()
        print(f"✅ {4} pessoas criadas (com múltiplos tipos)")
        
        # ============================================================================
        # EQUIPAMENTOS (com períodos flexíveis!)
        # ============================================================================
        print("\n🔧 Criando equipamentos...")
        
        equipamentos_data = [
            {
                "name": "Betoneira 400L Profissional",
                "description": "Betoneira de 400 litros, motor 2HP, ideal para obras de médio porte. Mixer de alta qualidade com estrutura reforçada.",
                "category_id": subcategorias[2].id,  # Betoneiras (Subcategoria)
                # "subcategory_id": subcategorias[2].id,
                "brand": "Maqtron",
                "internal_code": "BET-001",
                "serial_number": "BET2024001",
                "barcode": "7891234567890",
                "purchase_value": Decimal("3500.00"),
                "sale_value": Decimal("2800.00"),
                "suggested_deposit": Decimal("500.00"),
                "rental_periods": [
                    {"description": "1 dia", "days": 1, "value": 80.00},
                    {"description": "Até 3 dias", "days": 3, "value": 210.00},
                    {"description": "Semanal (7 dias)", "days": 7, "value": 450.00},
                    {"description": "Quinzenal (15 dias)", "days": 15, "value": 800.00},
                    {"description": "Mensal (30 dias)", "days": 30, "value": 1400.00}
                ],
                "specifications": {
                    "Capacidade": "400 litros",
                    "Motor": "2HP monofásico",
                    "Peso": "150 kg",
                    "Voltagem": "220V"
                },
                "images": [
                    {"url": "https://placeholder.com/betoneira1.jpg", "isPrimary": True, "order": 1},
                    {"url": "https://placeholder.com/betoneira2.jpg", "isPrimary": False, "order": 2}
                ],
                "external_media": [
                    {"type": "video", "title": "Como operar a betoneira", "url": "https://youtube.com/watch?v=exemplo1"},
                    {"type": "manual", "title": "Manual do fabricante", "url": "https://maqtron.com.br/manual-betoneira.pdf"}
                ],
                "specific_clauses": [
                    "Equipamento deve ser devolvido limpo",
                    "Locatário responsável por manutenção básica durante locação",
                    "Danos por mau uso serão cobrados do depósito"
                ],
                "quantity_total": 3,
                "quantity_available": 3,
                "status": EquipmentStatus.AVAILABLE,
                "tags": ["construção", "concreto", "mixer"]
            },
            {
                "name": "Furadeira de Impacto Makita 1000W",
                "description": "Furadeira de impacto profissional 1000W, ideal para concreto e alvenaria. Inclui maleta e kit de brocas.",
                "category_id": subcategorias[0].id,  # Ferramentas Elétricas
                # "subcategory_id": subcategorias[0].id,
                "brand": "Makita",
                "internal_code": "FUR-002",
                "serial_number": "MAK2024045",
                "purchase_value": Decimal("850.00"),
                "sale_value": Decimal("650.00"),
                "suggested_deposit": Decimal("200.00"),
                "rental_periods": [
                    {"description": "Diária", "days": 1, "value": 35.00},
                    {"description": "3 dias", "days": 3, "value": 90.00},
                    {"description": "Semanal", "days": 7, "value": 180.00},
                    {"description": "Quinzenal", "days": 15, "value": 320.00}
                ],
                "specifications": {
                    "Potência": "1000W",
                    "Voltagem": "220V",
                    "Rotação": "0-3000 RPM",
                    "Impactos": "48.000 IPM"
                },
                "external_media": [
                    {"type": "video", "title": "Tutorial de uso", "url": "https://youtube.com/watch?v=exemplo2"},
                    {"type": "link", "title": "Site do fabricante", "url": "https://makita.com.br"}
                ],
                "quantity_total": 5,
                "quantity_available": 4,
                "quantity_rented": 1,
                "status": EquipmentStatus.AVAILABLE,
                "tags": ["ferramentas", "furadeira", "construção"]
            },
            {
                "name": "Kit Iluminação LED Festa (8 Refletores)",
                "description": "Kit completo de iluminação LED para festas e eventos. 8 refletores RGB controláveis, tripés ajustáveis e mesa controladora DMX.",
                "category_id": subcategorias[3].id,  # Iluminação
                # "subcategory_id": subcategorias[3].id,
                "brand": "PLS",
                "internal_code": "ILU-003",
                "purchase_value": Decimal("4500.00"),
                "suggested_deposit": Decimal("800.00"),
                "rental_periods": [
                    {"description": "1 dia (evento)", "days": 1, "value": 280.00},
                    {"description": "Final de semana", "days": 3, "value": 450.00},
                    {"description": "Semanal", "days": 7, "value": 700.00}
                ],
                "specifications": {
                    "Quantidade": "8 refletores LED",
                    "Potência por LED": "200W",
                    "Cores": "RGB completo",
                    "Controle": "Mesa DMX 512 inclusa"
                },
                "external_media": [
                    {"type": "video", "title": "Setup rápido", "url": "https://youtube.com/watch?v=exemplo3"},
                    {"type": "manual", "title": "Manual DMX", "url": "https://pls.com.br/manual-dmx.pdf"}
                ],
                "specific_clauses": [
                    "Equipamento frágil - cuidado no transporte",
                    "Teste obrigatório antes do evento",
                    "Quebra de lâmpadas será cobrada R$ 150 por unidade"
                ],
                "quantity_total": 2,
                "quantity_available": 2,
                "status": EquipmentStatus.AVAILABLE,
                "tags": ["festa", "iluminação", "led", "evento"]
            },
            {
                "name": "Cadeira de Rodas Motorizada Premium",
                "description": "Cadeira de rodas motorizada de alta qualidade, bateria de longa duração, controle joystick, assento confortável.",
                "category_id": subcategorias[7].id,  # Mobilidade
                # "subcategory_id": subcategorias[7].id,
                "brand": "Ortobras",
                "internal_code": "MED-004",
                "purchase_value": Decimal("8500.00"),
                "suggested_deposit": Decimal("1500.00"),
                "rental_periods": [
                    {"description": "Diária", "days": 1, "value": 120.00},
                    {"description": "Semanal", "days": 7, "value": 600.00},
                    {"description": "Quinzenal", "days": 15, "value": 1000.00},
                    {"description": "Mensal", "days": 30, "value": 1800.00},
                    {"description": "Trimestral (90 dias)", "days": 90, "value": 4500.00}
                ],
                "specifications": {
                    "Autonomia": "25 km",
                    "Velocidade máxima": "6 km/h",
                    "Peso suportado": "120 kg",
                    "Bateria": "12V 50Ah"
                },
                "external_media": [
                    {"type": "manual", "title": "Manual de uso", "url": "https://ortobras.com.br/manual-cadeira.pdf"},
                    {"type": "video", "title": "Como carregar a bateria", "url": "https://youtube.com/watch?v=exemplo4"}
                ],
                "specific_clauses": [
                    "Locatário deve manter bateria sempre carregada",
                    "Uso exclusivo para pessoa com mobilidade reduzida",
                    "Danos elétricos não cobertos - uso por conta e risco"
                ],
                "quantity_total": 4,
                "quantity_available": 3,
                "quantity_rented": 1,
                "status": EquipmentStatus.AVAILABLE,
                "tags": ["médico", "cadeira-rodas", "mobilidade"]
            }
        ]
        
        equipamentos = []
        for eq_data in equipamentos_data:
            eq = Equipment(**eq_data)
            db.add(eq)
            equipamentos.append(eq)
        
        db.commit()
        print(f"✅ {len(equipamentos)} equipamentos criados (com períodos flexíveis)")
        
        # ============================================================================
        # RESUMO
        # ============================================================================
        print("\n" + "="*60)
        print("✅ SEED CONCLUÍDO COM SUCESSO!")
        print("="*60)
        print(f"\n📊 Resumo dos dados criados:")
        print(f"  • Usuários: {3}")
        print(f"  • Categorias: {len(categorias)}")
        print(f"  • Subcategorias: {len(subcategorias)}")
        print(f"  • Pessoas: {4} (incluindo múlt. tipos)")
        print(f"  • Equipamentos: {len(equipamentos)}")
        print(f"\n🔑 Credenciais:")
        print(f"  Admin: admin@locnos.com.br / admin123")
        print(f"  Gerente: gerente@locnos.com.br / gerente123")
        print(f"  Atendente: atendente@locnos.com.br / atendente123")
        print(f"\n🌐 Acesse: http://localhost:8000/docs")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Erro no seed: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
