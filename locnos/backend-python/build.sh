#!/usr/bin/env bash
# Build script for Render deployment
# Exit on error
set -o errexit

echo "🐍 Python version:"
python --version

echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip

echo ""
echo "🔧 Installing production dependencies..."
# Use requirements-production.txt para evitar dependências que precisam de compilação
pip install -r requirements-production.txt --no-cache-dir

echo ""
echo "✅ Build completed successfully!"
echo "📊 Installed packages:"
pip list | grep -E "fastapi|uvicorn|sqlalchemy|pydantic"
