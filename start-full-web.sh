#!/bin/bash

# 快捷总结笔记 - 完整Web服务启动器

cd ~/Desktop/快捷总结笔记

echo "================================================"
echo "  🌐 快捷总结笔记 - 完整Web服务"
echo "================================================"
echo ""

# 检查依赖
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  正在安装Flask..."
    pip3 install flask flask-cors pyyaml
fi

echo "🚀 启动API服务器 (端口 5000)..."
python3 api_server.py &
API_PID=$!

echo ""
echo "🚀 启动前端服务器 (端口 8080)..."
python3 -m http.server 8080 --directory ui &
FRONTEND_PID=$!

echo ""
echo "================================================"
echo ""
echo "✅ 服务已启动！"
echo ""
echo "📌 前端地址: http://localhost:8080"
echo "📌 API地址:  http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo "================================================"
echo ""

# 等待用户中断
trap "kill $API_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

# 等待子进程
wait
