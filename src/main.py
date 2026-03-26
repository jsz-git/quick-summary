"""
快捷总结笔记 - 主程序（增强版）
通过快捷键触发的AI对话总结工具
支持自动选中、多AI模型
"""
import os
import sys
import signal
from pathlib import Path
from dotenv import load_dotenv

# 添加项目路径到系统路径
sys.path.insert(0, str(Path(__file__).parent))

from utils import load_config, expand_path, generate_filename, save_markdown, notify
from summarizer import create_summarizer
from auto_selector import AutoSelector

# 加载环境变量
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)


class SessionSummaryTool:
    """会话总结工具主类（增强版）"""

    def __init__(self):
        self.config = None
        self.summarizer = None
        self.auto_selector = None

        self._load_config()
        self._init_summarizer()
        self._init_auto_selector()

    def _load_config(self):
        """加载配置"""
        try:
            config_path = Path(__file__).parent.parent / "config" / "config.yaml"
            self.config = load_config(str(config_path))
            print("✅ 配置加载成功")
        except Exception as e:
            print(f"❌ 配置加载失败: {e}")
            sys.exit(1)

    def _init_summarizer(self):
        """初始化AI总结器"""
        try:
            self.summarizer = create_summarizer(self.config)
            print("✅ AI总结器初始化成功")
        except Exception as e:
            print(f"❌ AI总结器初始化失败: {e}")
            sys.exit(1)

    def _init_auto_selector(self):
        """初始化自动选择器"""
        if self.config.get('auto_select', True):
            try:
                self.auto_selector = AutoSelector()
                print("✅ 自动选择器初始化成功")
            except Exception as e:
                print(f"⚠️  自动选择器初始化失败: {e}")
                print("💡 将使用手动复制模式")
                self.auto_selector = None
        else:
            print("ℹ️  自动选中功能已禁用")

    def trigger_summary(self):
        """触发总结（快捷键或命令行调用）"""
        print("\n" + "="*50)
        print("🎯 触发会话总结...")
        print("="*50)

        # 步骤1: 自动选中并复制（如果启用）
        if self.auto_selector and self.config.get('auto_select', True):
            print("📍 自动选中模式")
            method = self.config.get('auto_select_method', 'all')

            if method == 'all':
                success = self.auto_selector.select_and_copy()
            else:  # range
                lines = self.config.get('auto_select_lines', 50)
                success = self.auto_selector.select_range(lines)

            if not success:
                print("⚠️  自动选中失败，尝试读取剪贴板")

            # 给系统一点时间完成复制操作
            import time
            time.sleep(0.2)

        # 步骤2: 读取剪贴板
        try:
            import pyperclip
            clipboard_text = pyperclip.paste()

            if not clipboard_text or len(clipboard_text.strip()) < 10:
                print("⚠️  剪贴板内容太少或为空")
                print("💡 请先复制对话内容到剪贴板，或确保焦点在正确的区域")
                return

            print(f"📋 读取到剪贴板内容 ({len(clipboard_text)} 字符)")

        except Exception as e:
            print(f"❌ 读取剪贴板失败: {e}")
            print("💡 确保已安装 pyperclip: pip install pyperclip")
            return

        # 步骤3: 生成总结
        print("🤖 正在生成AI总结...")
        try:
            summary = self.summarizer.summarize(clipboard_text)
            print("✅ 总结生成成功")
        except Exception as e:
            print(f"❌ 总结生成失败: {e}")
            return

        # 步骤4: 保存文件
        output_dir = expand_path(self.config.get('output_dir', '~/session-logs'))
        filename = generate_filename(prefix="session", ext="md")

        try:
            filepath = save_markdown(summary, output_dir, filename)
            print(f"💾 总结已保存: {filepath}")
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return

        # 步骤5: 发送通知
        if self.config.get('enable_notification', True):
            notify("快捷总结笔记", "会话总结已生成并保存！")

        print("="*50)
        print("✅ 完成！")
        print("="*50 + "\n")

    def run_with_keyboard(self):
        """使用键盘快捷键运行"""
        try:
            import keyboard
        except ImportError:
            print("❌ 未安装 keyboard 库")
            print("💡 安装方法: pip install keyboard")
            print("\n或者使用命令行模式:")
            print("   python3 src/main.py --once")
            sys.exit(1)

        hotkey = self.config.get('hotkey', 'ctrl+shift+s')

        print("\n" + "="*50)
        print("🚀 快捷总结笔记工具已启动")
        print("="*50)
        print(f"📌 快捷键: {hotkey}")
        print(f"📁 保存位置: {self.config.get('output_dir')}")
        print(f"🤖 AI模型: {self.config.get('ai_provider')} / {self.config.get('ai_model')}")

        if self.auto_selector:
            method = self.config.get('auto_select_method', 'all')
            if method == 'all':
                print("✨ 自动选中: 全选")
            else:
                lines = self.config.get('auto_select_lines', 50)
                print(f"✨ 自动选中: 前{lines}行")
        else:
            print("📋 模式: 手动复制")

        print("="*50)
        print("\n使用方法:")
        if self.auto_selector:
            print("1. 将光标放在要总结的对话区域")
            print("2. 按快捷键自动选中并生成总结")
        else:
            print("1. 在任何AI对话工具中选中对话内容")
            print("1. 复制到剪贴板 (Ctrl/Cmd + C)")
            print("3. 按快捷键触发总结")
        print("4. 自动生成并保存Markdown总结")
        print("\n按 Ctrl+C 退出程序")
        print("="*50 + "\n")

        # 注册快捷键
        keyboard.add_hotkey(hotkey, self.trigger_summary)

        # 设置信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        self.running = True

        # 保持运行
        try:
            keyboard.wait()
        except KeyboardInterrupt:
            self._shutdown()

    def _signal_handler(self, signum, frame):
        """信号处理器"""
        print("\n\n收到退出信号...")
        self._shutdown()

    def _shutdown(self):
        """清理并退出"""
        print("正在关闭...")
        self.running = False
        print("👋 再见！")
        sys.exit(0)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='快捷总结笔记工具')
    parser.add_argument('--once', action='store_true', help='执行一次总结后退出')
    parser.add_argument('--config', type=str, help='指定配置文件路径')
    parser.add_argument('--no-auto-select', action='store_true', help='禁用自动选中，使用手动复制')

    args = parser.parse_args()

    tool = SessionSummaryTool()

    # 如果命令行指定禁用自动选中
    if args.no_auto_select:
        tool.auto_selector = None
        print("ℹ️  已禁用自动选中（命令行参数）")

    if args.once:
        # 单次执行模式
        tool.trigger_summary()
    else:
        # 快捷键监听模式
        tool.run_with_keyboard()


if __name__ == "__main__":
    main()
