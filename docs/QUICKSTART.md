# 快速开始指南

## 第一步：安装依赖

打开终端，进入项目目录：

```bash
cd ~/Desktop/快捷总结笔记
```

运行安装脚本：

```bash
./install.sh
```

或手动安装：

```bash
pip3 install -r requirements.txt
```

## 第二步：配置API密钥

1. 复制环境变量模板：

```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的API密钥：

```bash
open -e .env  # macOS
# 或
vim .env      # Linux/Windows
```

3. 修改这一行：

```
ANTHROPIC_API_KEY=your_api_key_here
```

改为你的实际密钥：

```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
```

### 如何获取API密钥？

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 登录/注册账号
3. 进入 API Keys 页面
4. 创建新的API密钥

## 第三步：测试安装

运行测试脚本：

```bash
python3 tests/test_basic.py
```

确保所有测试通过。

## 第四步：启动服务

### 方式1：快捷键模式（推荐）

```bash
python3 src/main.py
```

程序会常驻后台，监听快捷键。

### 方式2：单次执行模式

```bash
# 先复制对话内容到剪贴板，然后运行：
python3 src/main.py --once
```

执行一次总结后自动退出。

## 第五步：使用工具

1. 在任何AI对话工具中（元宝、千问、Claude Code等）
2. 选中对话内容
3. 复制到剪贴板（Cmd+C / Ctrl+C）
4. 按快捷键（默认：Ctrl+Shift+S）
5. 自动生成总结并保存到 `logs/` 目录

## 自定义配置

编辑 `config/config.yaml` 文件：

### 修改快捷键

```yaml
hotkey: "cmd+shift+s"  # macOS
# hotkey: "ctrl+alt+s"  # Windows/Linux
```

### 修改输出目录

```yaml
output_dir: "~/Documents/我的总结笔记"
```

### 修改AI模型

```yaml
ai_model: "claude-3-5-sonnet-20241022"
# 或使用更便宜的模型
# ai_model: "claude-3-5-haiku-20241022"
```

## 开机自启动（可选）

### macOS

创建 launchd 服务：

```bash
# 创建 plist 文件
cat > ~/Library/LaunchAgents/com.user.sessionsummary.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.sessionsummary</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/jszpc/Desktop/快捷总结笔记/src/main.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# 加载服务
launchctl load ~/Library/LaunchAgents/com.user.sessionsummary.plist
```

### Linux (systemd)

创建服务文件：

```bash
sudo nano /etc/systemd/system/session-summary.service
```

内容：

```ini
[Unit]
Description=Session Summary Tool
After=network.target

[Service]
Type=simple
User=你的用户名
ExecStart=/usr/bin/python3 /home/你的用户名/Desktop/快捷总结笔记/src/main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl enable session-summary
sudo systemctl start session-summary
```

## 常见问题

### Q: 快捷键不工作？

A: 检查是否有其他软件占用了该快捷键。尝试修改配置文件中的 `hotkey` 设置。

### Q: 提示找不到API密钥？

A: 确保 `.env` 文件在项目根目录，且已正确设置 `ANTHROPIC_API_KEY`。

### Q: 剪贴板读取失败？

A: macOS需要授予终端辅助功能权限：
   系统偏好设置 → 安全性与隐私 → 隐私 → 辅助功能

### Q: 生成的总结太短？

A: 修改配置文件中的 `max_tokens` 参数（默认2048，可增加到4096）。

### Q: 想用其他AI模型？

A: 修改 `config.yaml` 中的 `ai_model`，或等待后续版本支持多AI后端。

## 下一步

- 查看生成的总结：`open logs/` (macOS) 或 `nautilus logs/` (Linux)
- 自定义总结模板：编辑 `src/summarizer.py` 中的提示词
- 添加新功能：查看 `docs/DEVELOPMENT.md`（待创建）

## 反馈与贡献

遇到问题或有建议？欢迎反馈！
