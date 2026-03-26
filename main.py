#!/usr/bin/env python3
"""
快捷总结笔记 - 主入口
"""

import sys
import os
import argparse

# 获取项目根目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, 'src')
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')

# 添加到 Python 路径
sys.path.insert(0, SRC_DIR)
sys.path.insert(0, CONFIG_DIR)

# 导入模块
from auto_selector import AutoSelector
from summarizer import Summarizer
from utils import (
    get_clipboard_content,
    save_markdown,
    get_config,
    format_timestamp,
)

def run_api_server():
    """启动 API 服务器"""
    from flask import Flask
    from flask_cors import CORS
    import threading
    import time

    app = Flask(__name__)
    CORS(app)

    # API 路由
    @app.route('/api/notes', methods=['GET'])
    def get_notes():
        notes = get_notes_info()
        return {'notes': notes}

    @app.route('/api/note/<filename>', methods=['GET'])
    def get_note(filename):
        content = read_note(filename)
        return {'content': content}

    @app.route('/api/note/<filename>', methods=['DELETE'])
    def delete_note(filename):
        delete_note_file(filename)
        return {'success': True}

    @app.route('/api/config', methods=['GET'])
    def get_config_api():
        return get_config()

    @app.route('/api/summarize', methods=['POST'])
    def summarize():
        content = get_clipboard_content()
        if content:
            config = get_config()
            summarizer = Summarizer(config)
            result = summarizer.summarize(content)
            if result:
                return {'success': True, 'result': result}
        return {'success': False}

    def run():
        app.run(host='0.0.0.0', port=5000,        print(f"[API] 服务器启动在 http://localhost:5000")

    # 在后台线程运行
    server_thread = threading.Thread(target=run)
    server_thread.daemon = True
    server_thread.start()
    return server_thread

def read_note(filename):
    """读取笔记内容"""
    notes_dir = os.path.join(ROOT_DIR, 'logs')
    filepath = os.path.join(notes_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

def delete_note_file(filename):
    """删除笔记"""
    notes_dir = os.path.join(ROOT_DIR, 'logs')
    filepath = os.path.join(notes_dir, filename)
    if os.path.exists(filepath):
        os.remove(filepath)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='快捷总结笔记 - AI对话总结工具')
    parser.add_argument('--mode', type=str, default='gui', choices=['gui', 'cli'], help='运行模式')
    parser.add_argument('--api-only', action='store_true', help='仅启动 API 服务器')
    args = parser.parse_args()

    # 加载配置
    config = get_config()
    print(f"[快捷总结笔记] 启动中...")
    print(f"  AI提供商: {config.get('ai_provider', 'deepseek')}")
    print(f"  AI模型: {config.get('ai_model', 'deepseek-chat')}")

    if args.mode == 'gui' or args.api_only:
        # 启动 API 服务器
        server_thread = run_api_server()

        if args.api_only:
            print("[API] 服务器已启动， 按Ctrl+C 停止")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n[API] 服务器已停止")

    print("[快捷总结笔记] GUI 模式")
    print(f"[API] 服务器运行在 http://localhost:5000")
    print(f"[UI] 访问 http://localhost:5000 使用浏览器界面")

    # 保持运行
    try:
        while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n[快捷总结笔记] 已停止")

if __name__ == '__main__':
    main()
