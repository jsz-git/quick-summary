"""
自动选择器模块 - 自动选中并复制内容
"""
import subprocess
import sys
from typing import Optional


class AutoSelector:
    """自动选择器 - 模拟键盘操作自动选中内容"""

    def __init__(self, platform: str = None):
        """
        初始化自动选择器

        Args:
            platform: 操作系统平台 (darwin, linux, windows)
        """
        self.platform = platform or sys.platform

    def select_and_copy(self) -> bool:
        """
        自动选中当前焦点区域的内容并复制到剪贴板

        Returns:
            bool: 是否成功
        """
        try:
            if self.platform == 'darwin':  # macOS
                return self._macos_select_and_copy()
            elif self.platform.startswith('linux'):
                return self._linux_select_and_copy()
            elif self.platform == 'win32':
                return self._windows_select_and_copy()
            else:
                print(f"⚠️  不支持的平台: {self.platform}")
                return False
        except Exception as e:
            print(f"❌ 自动选中失败: {e}")
            return False

    def _macos_select_and_copy(self) -> bool:
        """macOS: 使用 AppleScript 模拟键盘操作"""
        try:
            # 方法1: 使用 AppleScript (更可靠)
            applescript = '''
            tell application "System Events"
                -- 全选
                keystroke "a" using command down
                delay 0.1
                -- 复制
                keystroke "c" using command down
            end tell
            '''

            subprocess.run(
                ['osascript', '-e', applescript],
                check=True,
                capture_output=True
            )

            print("✅ macOS: 已自动选中并复制内容")
            return True

        except subprocess.CalledProcessError as e:
            print(f"⚠️  AppleScript 执行失败，尝试备用方法")
            return self._fallback_select_and_copy()

    def _linux_select_and_copy(self) -> bool:
        """Linux: 使用 xdotool 或 pyautogui"""
        try:
            # 方法1: xdotool
            subprocess.run(
                ['xdotool', 'key', 'ctrl+a', 'ctrl+c'],
                check=True,
                capture_output=True
            )
            print("✅ Linux: 已自动选中并复制内容")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # 方法2: pyautogui
            return self._fallback_select_and_copy()

    def _windows_select_and_copy(self) -> bool:
        """Windows: 使用 pyautogui"""
        try:
            import pyautogui
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('ctrl', 'c')
            print("✅ Windows: 已自动选中并复制内容")
            return True
        except Exception as e:
            print(f"❌ Windows 自动选中失败: {e}")
            return False

    def _fallback_select_and_copy(self) -> bool:
        """备用方法：使用 pyautogui"""
        try:
            import pyautogui
            import time

            # macOS/Linux 使用 Cmd，Windows 使用 Ctrl
            modifier = 'command' if self.platform == 'darwin' else 'ctrl'

            # 全选
            pyautogui.hotkey(modifier, 'a')
            time.sleep(0.1)

            # 复制
            pyautogui.hotkey(modifier, 'c')
            time.sleep(0.1)

            print("✅ 已自动选中并复制内容（备用方法）")
            return True

        except ImportError:
            print("❌ 未安装 pyautogui，无法使用备用方法")
            print("💡 安装方法: pip install pyautogui")
            return False
        except Exception as e:
            print(f"❌ 备用方法失败: {e}")
            return False

    def select_range(self, lines: int = 50) -> bool:
        """
        选中指定行数范围的内容（向前选择）

        Args:
            lines: 要选中的行数

        Returns:
            bool: 是否成功
        """
        try:
            import pyautogui
            import time

            # macOS/Linux 使用 Cmd，Windows 使用 Ctrl
            modifier = 'command' if self.platform == 'darwin' else 'ctrl'

            # 先将光标移动到行首
            if self.platform == 'darwin':
                pyautogui.hotkey('command', 'left')
            else:
                pyautogui.hotkey('home')

            time.sleep(0.05)

            # Shift + 上箭头 向前选择多行
            for _ in range(lines):
                pyautogui.hotkey('shift', 'up')

            time.sleep(0.05)

            # 复制选中内容
            pyautogui.hotkey(modifier, 'c')

            print(f"✅ 已选中前 {lines} 行并复制")
            return True

        except Exception as e:
            print(f"❌ 范围选择失败: {e}")
            return False


if __name__ == "__main__":
    # 测试
    print("测试自动选择器...")
    print("请在5秒内切换到一个文本编辑器")
    import time
    time.sleep(5)

    selector = AutoSelector()
    success = selector.select_and_copy()

    if success:
        print("✅ 测试成功！")
        # 读取剪贴板验证
        try:
            import pyperclip
            content = pyperclip.paste()
            print(f"📋 剪贴板内容（前100字符）: {content[:100]}")
        except:
            pass
    else:
        print("❌ 测试失败")
