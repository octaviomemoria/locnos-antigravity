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
echo "🔧 Installing dependencies from requirements.txt..."
pip install -r requirements.txt --no-cache-dir

echo ""
echo "✅ Build completed successfully!"
echo "📊 Installed packages:"
pip list | grep -E "fastapi|uvicorn|sqlalchemy|pydantic"
