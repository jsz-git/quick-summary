"""
工具函数模块
"""
import os
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


def load_config(config_path: str = None) -> Dict[str, Any]:
    """加载配置文件"""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "config.yaml"

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def expand_path(path: str) -> Path:
    """扩展路径：支持 ~ 展开和相对路径（相对于项目目录）"""
    p = Path(path)

    # 如果是相对路径，基于项目根目录解析
    if not p.is_absolute() and not str(path).startswith('~'):
        # 获取项目根目录（utils.py 所在目录的父目录）
        project_root = Path(__file__).parent.parent
        p = project_root / p

    return p.expanduser()


def ensure_dir(path: Path) -> None:
    """确保目录存在"""
    path.mkdir(parents=True, exist_ok=True)


def generate_filename(prefix: str = "session", ext: str = "md") -> str:
    """生成带时间戳的文件名"""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    return f"{prefix}-{timestamp}.{ext}"


def get_timestamp() -> str:
    """获取格式化的时间戳"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def save_markdown(content: str, output_dir: Path, filename: str) -> Path:
    """保存Markdown文件"""
    ensure_dir(output_dir)
    filepath = output_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def notify(title: str, message: str) -> None:
    """发送系统通知（macOS）"""
    try:
        os.system(f'''osascript -e 'display notification "{message}" with title "{title}"' ''')
    except Exception as e:
        print(f"通知发送失败: {e}")


def extract_code_blocks(text: str) -> list:
    """从文本中提取代码块"""
    import re
    pattern = r'```[\s\S]*?```'
    return re.findall(pattern, text)


def extract_commands(text: str) -> list:
    """从文本中提取命令行"""
    import re
    # 匹配 bash 命令
    bash_pattern = r'```bash\n(.*?)```'
    commands = re.findall(bash_pattern, text, re.DOTALL)
    return commands


def truncate_text(text: str, max_length: int = 1000) -> str:
    """截断文本到指定长度"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


if __name__ == "__main__":
    # 测试
    config = load_config()
    print("配置加载成功:", config)

    timestamp = get_timestamp()
    print("当前时间:", timestamp)

    filename = generate_filename()
    print("生成文件名:", filename)
