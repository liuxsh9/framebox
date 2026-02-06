#!/bin/bash

# framebox 启动脚本 (使用 uv)

set -e

echo "🚀 Starting framebox with uv..."

# 检查 uv 是否安装
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed"
    echo "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 同步依赖（自动创建虚拟环境并安装依赖）
echo "📦 Syncing dependencies..."
uv sync

# 创建必要的目录
mkdir -p data/projects logs

# 启动服务器
echo "✓ Starting server..."
echo "  Access Web UI at: http://localhost:8000"
echo "  API Documentation: http://localhost:8000/docs"
echo ""

uv run python main.py
