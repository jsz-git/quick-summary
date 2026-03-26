#!/bin/bash

# 快捷总结笔记 - 快速安装脚本

# 获取脚本所在目录并切换到该目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "================================================"
echo "  快捷总结笔记 - 安装向导"
echo "================================================"
echo ""
echo "📁 工作目录: $SCRIPT_DIR"
echo ""

# 检查Python版本
echo "🔍 检查Python版本..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ 找到 $PYTHON_VERSION"
else
    echo "❌ 未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi

# 安装依赖
echo ""
echo "📦 安装依赖包..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 配置环境变量
echo ""
echo "⚙️  配置环境变量..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ 已创建 .env 文件"
    echo ""
    echo "⚠️  重要：请编辑 .env 文件，填入你的 ANTHROPIC_API_KEY"
    echo "   vim .env"
    echo "   或"
    echo "   open -e .env"
else
    echo "✅ .env 文件已存在"
fi

# 创建日志目录
echo ""
echo "📁 创建必要目录..."
mkdir -p logs
echo "✅ 日志目录已创建"

# 运行测试
echo ""
echo "🧪 运行基础测试..."
python3 tests/test_basic.py

echo ""
echo "================================================"
echo "  ✅ 安装完成！"
echo "================================================"
echo ""
echo "下一步："
echo "1. 编辑 .env 文件，设置 ANTHROPIC_API_KEY"
echo "2. 启动服务："
echo "   python3 src/main.py"
echo ""
echo "或者执行一次总结："
echo "   python3 src/main.py --once"
echo ""
echo "================================================"
