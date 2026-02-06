#!/bin/bash

# iframe-server 启动脚本 (使用 uv)

set -e

echo "🚀 Starting iframe-server with uv..."

# 检查 uv 是否安装
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed"
    echo "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
fi

# 检查依赖
if [ ! -f ".venv/pyvenv.cfg" ]; then
    echo "📦 Installing dependencies..."
    uv pip install -e .
fi

# 创建必要的目录
mkdir -p data/projects logs

# 启动服务器
echo "✓ Starting server..."
echo "  Access Web UI at: http://localhost:8001"
echo "  API Documentation: http://localhost:8001/docs"
echo ""

uv run python main.py
