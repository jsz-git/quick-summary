#!/usr/bin/osascript

-- 快捷总结笔记 - AppleScript 版本（无需管理员权限）
-- 监听快捷键 Cmd+Shift+S，触发总结功能

property HOTKEY : "s" -- 快捷键字母
property MODIFIERS : {command down, shift down} -- 修饰键

on run
    display notification "快捷总结笔记已启动！按 Cmd+Shift+S 开始总结" with title "快捷总结笔记" sound name "Glass"

    -- 启动快捷键监听
    tell application "System Events"
        repeat
            try
                -- 检测 Cmd+Shift+S
                if (key code 1 using {command down, shift down}) then -- S 键的 key code 是 1
                    triggerSummary()
                    delay 1 -- 防止重复触发
                end if
            on error errMsg
                -- 忽略错误，继续监听
            end try
            delay 0.1 -- 减少CPU占用
        end repeat
    end tell
end run

on triggerSummary()
    display notification "正在生成总结..." with title "快捷总结笔记" sound name "Glass"

    try
        -- 1. 自动全选并复制（模拟 Cmd+A, Cmd+C）
        tell application "System Events"
            keystroke "a" using command down
            delay 0.1
            keystroke "c" using command down
            delay 0.2
        end tell

        -- 2. 调用 Python 脚本生成总结
        set scriptPath to (POSIX path of (path to me) as string) & "../src/main.py"
        do shell script "cd ~/Desktop/快捷总结笔记 && python3 src/main.py --once 2>&1"

        display notification "总结已生成！" with title "快捷总结笔记" sound name "Glass"

    on error errMsg
        display notification "生成失败：" & errMsg with title "快捷总结笔记" sound name "Basso"
    end try
end triggerSummary
