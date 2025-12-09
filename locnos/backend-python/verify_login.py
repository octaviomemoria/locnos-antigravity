
import sys
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.user import User
from app.core.security import verify_password

def verify_login(email, password):
    print(f"🔍 Verificando login para: {email}")
    
    db = SessionLocal()
    try:
        # 1. Buscar usuário
        print("📊 Buscando usuário no banco...")
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print("❌ Usuário NÃO encontrado!")
            return False
            
        print(f"✅ Usuário encontrado: {user.name} (ID: {user.id})")
        print(f"   Status: {user.status}")
        print(f"   Role: {user.role}")
        print(f"   Hash no banco: {user.password[:10]}...")
        
        # 2. Verificar senha
        print("🔑 Verificando senha...")
        is_valid = verify_password(password, user.password)
        
        if is_valid:
            print("✅ Senha CORRETA! Login deve funcionar.")
            return True
        else:
            print("❌ Senha INCORRETA!")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao conectar/consultar banco: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    email = "admin@locnos.com.br"
    password = "admin123"
    verify_login(email, password)
