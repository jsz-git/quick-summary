#!/bin/bash

# 快捷总结笔记 - Web界面启动器

cd ~/Desktop/快捷总结笔记

echo "================================================"
echo "  🌐 快捷总结笔记 - Web界面版"
echo "================================================"
echo ""
echo "✨ 启动中..."
echo ""
echo "📌 访问地址: http://localhost:8080"
echo "📁 文件目录: ~/Desktop/快捷总结笔记/ui"
echo ""
echo "⚠️  注意: Web版功能受限，推荐使用Tauri桌面版"
echo ""
echo "按 Ctrl+C 停止服务"
echo "================================================"
echo ""

# 启动HTTP服务器
python3 -m http.server 8080 --directory ui
