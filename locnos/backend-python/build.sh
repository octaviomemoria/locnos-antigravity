#!/usr/bin/env bash
# Build script for Render deployment
# Exit on error
set -o errexit

echo "🐍 Python version:"
python --version

echo ""
echo "🧹 Cleaning pip cache..."
pip cache purge || true

echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip

echo ""
echo "🔧 Installing production dependencies..."
pip install -r requirements-production.txt --no-cache-dir --force-reinstall

echo ""
echo "✅ Build completed successfully!"
echo "📊 Installed packages:"
pip list | grep -E "fastapi|uvicorn|sqlalchemy|pydantic"
