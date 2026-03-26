#!/bin/bash

# 快捷总结笔记 - 启动器（AppleScript版本）
# 无需管理员权限

cd ~/Desktop/快捷总结笔记

echo "================================================"
echo "  快捷总结笔记 - AppleScript 版本"
echo "================================================"
echo ""
echo "📌 快捷键: Cmd+Shift+S"
echo "🤖 AI模型: DeepSeek"
echo "📁 保存位置: ~/Desktop/快捷总结笔记/logs"
echo ""
echo "⚠️  首次运行需要授予辅助功能权限："
echo "   系统偏好设置 → 安全性与隐私 → 隐私 → 辅助功能"
echo "   添加 '脚本编辑器' 或 'Automator'"
echo ""
echo "按 Cmd+C 停止"
echo "================================================"
echo ""

# 运行 AppleScript
osascript shortcut_summary.applescript
