"""
Script de teste rápido para verificar se o CORS está funcionando.
Execute: python test_cors.py
"""

from app.core.config import settings

print("=" * 60)
print("🔍 Testando Configuração CORS")
print("=" * 60)

print(f"\n📋 BACKEND_CORS_ORIGINS:")
for origin in settings.BACKEND_CORS_ORIGINS:
    print(f"  ✅ {origin}")

print(f"\n🌐 API URL: {settings.API_V1_STR}")
print(f"🔐 Secret Key presente: {'Sim' if settings.SECRET_KEY else 'Não'}")
print(f"🗄️  Database URL: {settings.DATABASE_URL[:30]}...")

if not settings.BACKEND_CORS_ORIGINS:
    print("\n⚠️  AVISO: Nenhuma origem CORS configurada!")
    print("   Adicione no .env: BACKEND_CORS_ORIGINS=[\"http://localhost:3000\"]")
elif "http://localhost:3000" in settings.BACKEND_CORS_ORIGINS:
    print("\n✅ localhost:3000 permitido no CORS!")
else:
    print("\n❌ localhost:3000 NÃO está na lista CORS!")

print("=" * 60)
