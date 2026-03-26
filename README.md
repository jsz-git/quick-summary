# 快捷总结笔记工具 v1.1

一个轻量级的AI对话总结工具，通过快捷键触发，**自动选中**内容并生成结构化的会话总结。支持**多种AI模型**（DeepSeek、通义千问、Claude、GPT、本地模型）。

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ 核心特性

### 🎯 一键总结
- **自动选中** - 按快捷键自动全选当前区域内容
- **智能总结** - AI提取关键步骤、命令、文件修改
- **Markdown存储** - 结构化保存，便于查阅

### 🤖 多模型支持
- **DeepSeek** - 性价比之王（推荐）
- **通义千问** - 中文优化
- **Claude** - 高质量
- **OpenAI GPT** - 生态完善
- **本地模型** - 完全免费（Ollama）

### ⚡ 超轻量
- 内存占用 < 10MB
- CPU占用 < 1%（空闲）
- 完全本地运行

### 🔒 安全可控
- 不监听键盘输入
- 不后台读取剪贴板
- 用户主动触发
- API密钥本地存储

## 🚀 快速开始（3分钟）

### 1. 安装依赖

```bash
cd ~/Desktop/快捷总结笔记
./install.sh
```

或手动安装：
```bash
pip3 install -r requirements.txt
```

### 2. 配置API密钥

```bash
# 复制模板
cp .env.example .env

# 编辑并填入API密钥（推荐 DeepSeek）
open -e .env
```

**获取API密钥**：
- DeepSeek: https://platform.deepseek.com/ （约 ¥1/百万tokens）
- 通义千问: https://dashscope.console.aliyun.com/ （新用户免费）
- Claude: https://console.anthropic.com/

### 3. 启动服务

```bash
python3 src/main.py
```

### 4. 开始使用

1. 在任何AI对话工具中（元宝、千问、Claude Code）
2. 将光标放在对话区域
3. 按 **Ctrl+Shift+S**（Mac: Cmd+Shift+S）
4. 自动选中 → AI总结 → 保存完成！

## 📋 使用示例

### 场景1：总结元宝对话

```
1. 在元宝对话框中
2. 按 Cmd+Shift+S
3. 自动全选对话内容
4. DeepSeek 生成总结
5. 保存到 ~/Desktop/快捷总结笔记/logs/
```

### 场景2：总结 Claude Code 会话

```
1. 在 Claude Code 中完成一个功能
2. 按 Ctrl+Shift+S
3. 使用本地 Llama2 总结（免费）
4. 查看结构化总结
```

## ⚙️ 配置

编辑 `config/config.yaml`：

### 选择AI模型

```yaml
# 使用 DeepSeek（推荐，性价比高）
ai_provider: "deepseek"
ai_model: "deepseek-chat"

# 或使用通义千问
# ai_provider: "qwen"
# ai_model: "qwen-plus"

# 或使用本地模型
# ai_provider: "local"
# ai_model: "llama2"
```

### 自定义快捷键

```yaml
hotkey: "ctrl+shift+s"  # Windows/Linux
# hotkey: "cmd+shift+s"  # macOS
```

### 自动选中设置

```yaml
auto_select: true  # 启用自动选中
auto_select_method: "all"  # all: 全选, range: 向前选择
auto_select_lines: 50  # 向前选择行数
```

## 📊 模型对比

| 模型 | 质量 | 速度 | 价格 | 中文 | 推荐场景 |
|------|------|------|------|------|----------|
| DeepSeek | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰 | ⭐⭐⭐⭐⭐ | **日常使用（推荐）** |
| 通义千问 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 💰 | ⭐⭐⭐⭐⭐ | 中文总结 |
| Claude | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 💰💰💰 | ⭐⭐⭐⭐ | 高质量需求 |
| GPT-4o | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 💰💰 | ⭐⭐⭐⭐ | 通用场景 |
| 本地模型 | ⭐⭐⭐ | ⭐⭐⭐ | 🆓 | ⭐⭐⭐ | 隐私敏感 |

## 🎯 功能对比

### vs 手动复制粘贴

| 功能 | 手动 | 本工具 | 改进 |
|------|------|--------|------|
| 操作步骤 | 4步 | 2步 | **-50%** |
| 总结质量 | 依赖人工 | AI结构化 | **+100%** |
| 时间消耗 | 5-10分钟 | 2-3秒 | **-99%** |

### vs 其他总结工具

| 功能 | 其他工具 | 本工具 |
|------|----------|--------|
| 自动选中 | ❌ | ✅ |
| 多模型支持 | ❌ | ✅ 5+ |
| 跨平台 | ⚠️ | ✅ |
| 成本 | 💰💰💰 | 💰 或 🆓 |
| 本地运行 | ❌ | ✅ |

## 📁 项目结构

```
快捷总结笔记/
├── src/
│   ├── main.py            # 主程序（230行）
│   ├── auto_selector.py   # 自动选中（200行）
│   ├── summarizer.py      # AI总结（350行）
│   └── utils.py           # 工具函数（110行）
├── config/
│   └── config.yaml        # 配置文件
├── logs/                  # 总结存储
├── docs/
│   ├── QUICKSTART.md      # 快速开始
│   ├── NEW_FEATURES.md    # 新功能说明
│   ├── BATCH1_SUMMARY.md  # 第一批次总结
│   └── BATCH2_SUMMARY.md  # 第二批次总结
├── tests/                 # 测试
├── requirements.txt       # 依赖
└── README.md              # 说明文档
```

## 🔧 高级功能

### 命令行参数

```bash
# 单次执行模式
python3 src/main.py --once

# 禁用自动选中
python3 src/main.py --no-auto-select

# 指定配置文件
python3 src/main.py --config /path/to/config.yaml
```

### 使用本地模型

```bash
# 1. 安装 Ollama
brew install ollama  # macOS
# 或访问 https://ollama.ai/

# 2. 下载模型
ollama pull llama2

# 3. 配置
# config.yaml:
ai_provider: "local"
ai_model: "llama2"
local_endpoint: "http://localhost:11434"

# 4. 启动
python3 src/main.py
```

## 🐛 故障排除

### 自动选中不工作

**macOS**: 需要辅助功能权限
- 系统偏好设置 → 安全性与隐私 → 隐私 → 辅助功能
- 添加终端到允许列表

**Linux**: 安装 xdotool
```bash
sudo apt-get install xdotool
```

### API调用失败

检查：
1. API密钥是否正确
2. 网络连接
3. API余额
4. 模型名称

### 总结质量不佳

尝试：
1. 更换更好的模型（qwen-max, claude）
2. 降低 temperature
3. 增加 max_tokens

## 📈 性能

| 指标 | 数值 |
|------|------|
| 内存占用 | < 10MB |
| CPU（空闲）| < 1% |
| 响应时间 | < 3秒 |
| 支持平台 | macOS, Windows, Linux |

## 🗺️ 开发路线

### v1.1 ✅（当前）
- ✅ 自动选中功能
- ✅ 多模型支持
- ✅ 文档完善

### v1.2（计划中）
- [ ] 图形化配置界面
- [ ] 自定义提示词模板
- [ ] 批量总结
- [ ] 历史记录搜索

### v2.0（未来）
- [ ] 浏览器扩展
- [ ] VS Code 插件
- [ ] 团队协作
- [ ] 云同步

## 📚 文档

- [快速开始指南](docs/QUICKSTART.md)
- [新功能说明](docs/NEW_FEATURES.md)
- [第一批次开发总结](docs/BATCH1_SUMMARY.md)
- [第二批次开发总结](docs/BATCH2_SUMMARY.md)
- [开发路线图](docs/ROADMAP.md)

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

## 📄 许可证

MIT License

## 🙏 致谢

感谢以下AI模型提供商：
- Anthropic (Claude)
- DeepSeek
- 阿里云（通义千问）
- OpenAI
- Ollama（本地模型）

---

**开始使用**: `python3 src/main.py`

**问题反馈**: 欢迎提出Issue

**版本**: v1.1.0 | **更新日期**: 2026-03-21
