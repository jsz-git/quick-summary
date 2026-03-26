#!/bin/bash

# 快捷总结笔记 - Tauri开发模式

cd ~/Desktop/快捷总结笔记

echo "================================================"
echo "  🖥️  快捷总结笔记 - Tauri开发模式"
echo "================================================"
echo ""

# 检查Rust
if ! command -v cargo &> /dev/null; then
    echo "❌ 未安装Rust"
    echo ""
    echo "安装方法："
    echo "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi

# 检查Tauri CLI
if ! cargo --list | grep -q "tauri"; then
    echo "⚠️  未安装Tauri CLI，正在安装..."
    cargo install tauri-cli --version "^2.0.0"
fi

echo "🚀 启动开发服务器..."
echo ""

# 启动Tauri开发模式
cargo tauri dev
