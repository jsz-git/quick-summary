# 快捷总结笔记 - 使用指南

## 🎯 两个版本选择

### 版本1：单次执行模式（推荐） ⭐
**最简单，无需权限，立即可用**

#### 使用方法
```bash
cd ~/Desktop/快捷总结笔记
./summarize-once.sh
```

**步骤**：
1. 在任意AI对话工具中选中对话内容
2. 复制到剪贴板（Cmd+C）
3. 运行脚本
4. 查看生成的总结（logs/目录）

#### 创建快捷方式（可选）
在终端中创建别名：
```bash
echo 'alias summary="cd ~/Desktop/快捷总结笔记 && ./summarize-once.sh"' >> ~/.zshrc
source ~/.zshrc
```

之后只需输入 `summary` 即可！

---

### 版本2：自动选中模式 ⚡
**自动全选 + 复制 + 总结**

#### 使用方法
```bash
cd ~/Desktop/快捷总结笔记
./summarize-auto.sh
```

**步骤**：
1. 将光标放在对话区域（无需选中）
2. 运行脚本
3. 自动全选、复制、生成总结

**首次使用需要授予权限**：
- 系统偏好设置 → 安全性与隐私 → 隐私 → 辅助功能
- 添加"终端"或"iTerm"

---

### 版本3：macOS Automator 快速操作（最便捷） 🌟

**通过右键菜单或快捷键触发**

#### 创建步骤

1. **打开 Automator**
   ```bash
   open -a Automator
   ```

2. **选择"快速操作"**

3. **添加操作**
   - 搜索"运行 Shell 脚本"
   - 拖到右侧
   - 粘贴以下内容：
   ```bash
   cd ~/Desktop/快捷总结笔记
   python3 src/main.py --once
   ```

4. **保存**
   - 文件 → 存储
   - 命名为"生成对话总结"

5. **设置快捷键**
   - 系统偏好设置 → 键盘 → 快捷键 → 服务
   - 找到"生成对话总结"
   - 设置快捷键（如 Cmd+Shift+S）

#### 使用方法
1. 选中对话内容并复制
2. 按快捷键或右键菜单选择"生成对话总结"

---

## 🚀 推荐使用流程

### 方案A：终端别名（最简单）
```bash
# 1. 设置别名
echo 'alias summary="cd ~/Desktop/快捷总结笔记 && python3 src/main.py --once"' >> ~/.zshrc
source ~/.zshrc

# 2. 使用
# 复制对话内容
# 在终端输入: summary
```

### 方案B：Automator（最便捷）
按照上面的步骤创建快速操作，之后只需按快捷键

### 方案C：脚本文件
```bash
# 手动复制对话后运行
cd ~/Desktop/快捷总结笔记
./summarize-once.sh
```

---

## 📝 实际使用示例

### 场景1：总结 Claude Code 会话
```bash
# 1. 在 Claude Code 中选中对话历史
# 2. Cmd+C 复制
# 3. 打开终端，输入：
summary

# 4. 总结自动生成到 logs/ 目录
```

### 场景2：总结元宝对话
```bash
# 1. 在元宝对话框中按 Cmd+A 全选
# 2. Cmd+C 复制
# 3. 运行脚本：
cd ~/Desktop/快捷总结笔记 && ./summarize-once.sh

# 4. 查看生成的总结
open logs/
```

### 场景3：使用自动选中
```bash
# 1. 将光标放在对话区域
# 2. 运行：
cd ~/Desktop/快捷总结笔记 && ./summarize-auto.sh

# 3. 自动完成全选、复制、总结
```

---

## ⚙️ 配置

### 修改 AI 模型
编辑 `config/config.yaml`：
```yaml
ai_provider: "deepseek"  # 或 qwen, claude, openai
ai_model: "deepseek-chat"
```

### 修改输出目录
```yaml
output_dir: "~/Documents/我的总结"
```

### 查看生成的总结
```bash
# 打开日志目录
open ~/Desktop/快捷总结笔记/logs/

# 查看最新的总结
ls -lt ~/Desktop/快捷总结笔记/logs/ | head -5
```

---

## 🔧 故障排除

### 问题1：提示权限不足
**解决**：
```bash
chmod +x ~/Desktop/快捷总结笔记/*.sh
```

### 问题2：自动选中不工作
**解决**：
- 系统偏好设置 → 安全性与隐私 → 隐私 → 辅助功能
- 添加终端到允许列表
- 重启终端

### 问题3：API调用失败
**检查**：
1. API密钥是否正确（.env文件）
2. 网络连接是否正常
3. API余额是否充足

---

## 💡 使用技巧

### 技巧1：批量总结
创建一个脚本批量处理多个对话：
```bash
for file in ~/Desktop/conversations/*.txt; do
    cat "$file" | pbcopy
    python3 ~/Desktop/快捷总结笔记/src/main.py --once
    sleep 2
done
```

### 技巧2：定时总结
使用 crontab 定时总结：
```bash
# 每天晚上10点总结今天的对话
0 22 * * * cd ~/Desktop/快捷总结笔记 && python3 src/main.py --once
```

### 技巧3：集成到工作流
在你的工作脚本中添加：
```bash
# 完成任务后自动总结
function finish-task() {
    echo "任务完成，正在生成总结..."
    cd ~/Desktop/快捷总结笔记
    python3 src/main.py --once
    echo "总结已生成！"
}
```

---

## 📊 版本对比

| 特性 | 版本1（单次） | 版本2（自动） | 版本3（Automator） |
|------|--------------|--------------|-------------------|
| 易用性 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 需要权限 | ❌ | ✅ | ❌ |
| 快捷键 | ⚠️ 需配置 | ⚠️ 需配置 | ✅ 原生支持 |
| 自动选中 | ❌ | ✅ | ❌ |
| 推荐度 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎯 立即开始

**最简单的方式**：
```bash
cd ~/Desktop/快捷总结笔记
./summarize-once.sh
```

**最便捷的方式**：
创建 Automator 快速操作，设置快捷键

---

**问题反馈**：遇到任何问题随时告诉我！
