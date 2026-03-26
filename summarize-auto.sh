#!/bin/bash

# 快捷总结笔记 - 一键总结（带自动选中）

cd ~/Desktop/快捷总结笔记

echo "================================================"
echo "  ⚡ 一键总结（自动选中 + AI总结）"
echo "================================================"
echo ""
echo "使用方法："
echo "1. 将光标放在要总结的对话区域"
echo "2. 运行此脚本"
echo ""
echo "正在自动选中内容并生成总结..."
echo "================================================"
echo ""

# 1. 自动全选并复制（AppleScript）
osascript -e 'tell application "System Events" to keystroke "a" using command down'
sleep 0.1
osascript -e 'tell application "System Events" to keystroke "c" using command down'
sleep 0.2

# 2. 执行总结
python3 src/main.py --once
