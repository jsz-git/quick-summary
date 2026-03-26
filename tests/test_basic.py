"""
基础功能测试
"""
import sys
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import load_config, expand_path, generate_filename, get_timestamp


def test_config_loading():
    """测试配置加载"""
    print("测试 1: 配置加载")
    try:
        config = load_config()
        assert 'hotkey' in config
        assert 'output_dir' in config
        print("✅ 配置加载成功")
        print(f"   快捷键: {config['hotkey']}")
        print(f"   输出目录: {config['output_dir']}")
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False
    return True


def test_path_expansion():
    """测试路径扩展"""
    print("\n测试 2: 路径扩展")
    try:
        path = expand_path("~/Desktop")
        assert str(path).startswith("/Users")
        print(f"✅ 路径扩展成功: {path}")
    except Exception as e:
        print(f"❌ 路径扩展失败: {e}")
        return False
    return True


def test_filename_generation():
    """测试文件名生成"""
    print("\n测试 3: 文件名生成")
    try:
        filename = generate_filename(prefix="test", ext="md")
        assert filename.startswith("test-")
        assert filename.endswith(".md")
        print(f"✅ 文件名生成成功: {filename}")
    except Exception as e:
        print(f"❌ 文件名生成失败: {e}")
        return False
    return True


def test_timestamp():
    """测试时间戳"""
    print("\n测试 4: 时间戳生成")
    try:
        timestamp = get_timestamp()
        assert len(timestamp) > 0
        print(f"✅ 时间戳生成成功: {timestamp}")
    except Exception as e:
        print(f"❌ 时间戳生成失败: {e}")
        return False
    return True


def test_dependencies():
    """测试依赖包"""
    print("\n测试 5: 依赖包检查")
    dependencies = {
        'anthropic': 'Anthropic SDK',
        'pyperclip': '剪贴板操作',
        'keyboard': '键盘监听',
        'yaml': 'YAML解析',
        'dotenv': '环境变量'
    }

    all_ok = True
    for module, name in dependencies.items():
        try:
            if module == 'yaml':
                __import__('yaml')
            elif module == 'dotenv':
                __import__('dotenv')
            else:
                __import__(module)
            print(f"✅ {name} ({module})")
        except ImportError:
            print(f"❌ {name} ({module}) - 未安装")
            all_ok = False

    return all_ok


def run_all_tests():
    """运行所有测试"""
    print("="*50)
    print("🧪 开始运行测试")
    print("="*50)

    tests = [
        test_config_loading,
        test_path_expansion,
        test_filename_generation,
        test_timestamp,
        test_dependencies
    ]

    results = [test() for test in tests]

    print("\n" + "="*50)
    print("📊 测试结果")
    print("="*50)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")

    if passed == total:
        print("✅ 所有测试通过！")
        print("\n下一步:")
        print("1. 配置API密钥: cp .env.example .env")
        print("2. 编辑 .env 填入 ANTHROPIC_API_KEY")
        print("3. 启动服务: python3 src/main.py")
    else:
        print("⚠️  部分测试失败，请检查依赖安装")
        print("安装依赖: pip3 install -r requirements.txt")

    print("="*50)


if __name__ == "__main__":
    run_all_tests()
