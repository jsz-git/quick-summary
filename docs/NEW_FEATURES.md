# 新功能说明 v1.1

## 🎉 新增功能

### 1. 自动选中功能 ⭐

**问题**: 之前需要手动选中并复制对话内容，不够便捷

**解决方案**: 现在可以直接按快捷键，自动选中当前焦点区域的内容！

#### 工作原理

```
按快捷键 → 自动全选当前区域 → 自动复制 → AI总结 → 保存
```

#### 配置选项

在 `config/config.yaml` 中：

```yaml
# 自动选中设置
auto_select: true  # 启用自动选中
auto_select_method: "all"  # all: 全选, range: 向前选择多行
auto_select_lines: 50  # 如果选择 range，向前选择50行
```

#### 使用方法

**模式1：全选当前区域**（推荐）
1. 将光标放在要总结的对话区域（输入框、文本编辑器等）
2. 按 `Ctrl+Shift+S`（Mac: `Cmd+Shift+S`）
3. 自动全选并复制当前区域内容
4. 生成总结

**模式2：向前选择多行**
1. 将光标放在对话的末尾
2. 按快捷键
3. 自动向前选择指定行数（默认50行）
4. 生成总结

#### 技术实现

- **macOS**: AppleScript 模拟 `Cmd+A` + `Cmd+C`
- **Windows**: pyautogui 模拟 `Ctrl+A` + `Ctrl+C`
- **Linux**: xdotool 或 pyautogui

#### 权限要求

- **macOS**: 需要授予终端"辅助功能"权限
  - 系统偏好设置 → 安全性与隐私 → 隐私 → 辅助功能 → 添加终端

### 2. 多模型支持 ⭐⭐⭐

**问题**: 之前只支持 Claude，现在需要支持更多模型

**解决方案**: 现已支持 5+ AI模型！

#### 支持的模型

| 提供商 | 模型示例 | API密钥环境变量 | 特点 |
|--------|----------|-----------------|------|
| **DeepSeek** | deepseek-chat | DEEPSEEK_API_KEY | 🇨🇳 国产，性价比高 |
| **通义千问** | qwen-plus, qwen-max | QWEN_API_KEY | 🇨🇳 阿里云，中文优秀 |
| **Claude** | claude-3-5-sonnet | ANTHROPIC_API_KEY | 质量高，价格较贵 |
| **OpenAI** | gpt-4o, gpt-3.5-turbo | OPENAI_API_KEY | 生态完善 |
| **本地模型** | llama2, mistral | 无需 | 完全免费，需本地部署 |

#### 配置方法

**步骤1：选择模型**

编辑 `config/config.yaml`：

```yaml
# 选择 DeepSeek（推荐，性价比高）
ai_provider: "deepseek"
ai_model: "deepseek-chat"

# 或者选择通义千问
# ai_provider: "qwen"
# ai_model: "qwen-plus"

# 或者选择 Claude
# ai_provider: "anthropic"
# ai_model: "claude-3-5-sonnet-20241022"

# 或者选择本地模型
# ai_provider: "local"
# ai_model: "llama2"
```

**步骤2：设置API密钥**

编辑 `.env` 文件：

```bash
# DeepSeek
DEEPSEEK_API_KEY=your_deepseek_key

# 通义千问
QWEN_API_KEY=your_qwen_key

# Claude
ANTHROPIC_API_KEY=your_claude_key

# OpenAI
OPENAI_API_KEY=your_openai_key
```

#### 如何获取API密钥

**DeepSeek** (推荐)
1. 访问 https://platform.deepseek.com/
2. 注册账号
3. 获取 API Key
4. 💰 价格：约 ¥1/百万tokens

**通义千问**
1. 访问 https://dashscope.console.aliyun.com/
2. 开通服务
3. 获取 API Key
4. 💰 新用户有免费额度

**Claude**
1. 访问 https://console.anthropic.com/
2. 获取 API Key
5. 💰 约 $3/百万tokens

**本地模型 (Ollama)**
1. 安装 Ollama: https://ollama.ai/
2. 运行模型: `ollama run llama2`
3. 完全免费！
4. ⚠️ 需要较好的硬件配置

## 📊 模型对比

| 模型 | 质量评分 | 速度 | 价格 | 中文支持 | 推荐场景 |
|------|----------|------|------|----------|----------|
| DeepSeek | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰 | ⭐⭐⭐⭐⭐ | 日常使用（推荐） |
| 通义千问 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 💰 | ⭐⭐⭐⭐⭐ | 中文总结 |
| Claude | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 💰💰💰 | ⭐⭐⭐⭐ | 高质量总结 |
| GPT-4o | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 💰💰 | ⭐⭐⭐⭐ | 通用场景 |
| 本地Llama2 | ⭐⭐⭐ | ⭐⭐⭐ | 🆓 | ⭐⭐⭐ | 隐私敏感 |

## 🚀 快速开始

### 使用 DeepSeek（最推荐）

```bash
# 1. 安装依赖
pip3 install -r requirements.txt

# 2. 配置
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY

# 3. 确认配置
# config.yaml 中已默认设置 ai_provider: "deepseek"

# 4. 启动
python3 src/main.py
```

### 使用通义千问

```bash
# 1. 编辑 config.yaml
ai_provider: "qwen"
ai_model: "qwen-plus"

# 2. 编辑 .env
QWEN_API_KEY=your_qwen_key

# 3. 启动
python3 src/main.py
```

## 🎯 使用示例

### 场景1：在元宝对话中生成总结

```
1. 打开元宝对话页面
2. 将光标放在对话框中
3. 按 Cmd+Shift+S（Mac）或 Ctrl+Shift+S（Windows）
4. 自动全选对话框内容
5. DeepSeek 生成总结
6. 保存到 logs/ 目录
```

### 场景2：在通义千问中生成总结

```
1. 打开通义千问
2. 将光标放在输入框
3. 按快捷键
4. 自动总结（使用通义千问自己的API，很讽刺吧😄）
```

### 场景3：在 Claude Code 中总结

```
1. 在 Claude Code 对话界面
2. 按快捷键
3. 使用本地 Llama2 模型总结（完全免费）
```

## ⚙️ 高级配置

### 禁用自动选中

如果不想使用自动选中功能：

```yaml
# config.yaml
auto_select: false
```

或者启动时使用参数：

```bash
python3 src/main.py --no-auto-select
```

### 调整选中行数

```yaml
auto_select_method: "range"
auto_select_lines: 100  # 向前选择100行
```

### 自定义快捷键

```yaml
hotkey: "ctrl+alt+s"  # Windows/Linux
# hotkey: "cmd+alt+s"  # macOS
```

## 🔧 故障排除

### 自动选中不工作

**macOS**:
- 检查辅助功能权限
- 系统偏好设置 → 安全性与隐私 → 隐私 → 辅助功能
- 添加终端或 Python 到允许列表

**Linux**:
- 安装 xdotool: `sudo apt-get install xdotool`
- 或者安装 pyautogui: `pip install pyautogui`

**Windows**:
- 以管理员权限运行
- 安装 pyautogui: `pip install pyautogui`

### API调用失败

检查：
1. API密钥是否正确
2. 网络连接是否正常
3. API余额是否充足
4. 模型名称是否正确

### 总结质量不佳

尝试：
1. 更换更好的模型（如 qwen-max, claude-3-5-sonnet）
2. 调整 temperature（降低随机性）
3. 增加 max_tokens（生成更详细总结）

## 📝 更新日志

### v1.1.0 (2026-03-21)

**新增功能**:
- ✨ 自动选中并复制功能
- 🤖 支持 DeepSeek
- 🤖 支持通义千问 (Qwen)
- 🤖 支持 OpenAI GPT
- 🤖 支持本地模型 (Ollama)

**改进**:
- 📚 完善文档
- 🎨 优化配置文件
- 🐛 修复多个bug

### v1.0.0 (2026-03-21)

- 🎉 初始版本
- ✅ Claude 支持
- ✅ 基础总结功能

## 🔜 下一版本计划

- [ ] 图形化配置界面
- [ ] 支持更多本地模型
- [ ] 浏览器扩展版本
- [ ] 搜索历史记录
- [ ] 团队协作功能

---

**反馈与建议**: 有任何问题或建议，欢迎提出！
