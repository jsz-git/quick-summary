"""
快捷总结笔记 - Web API后端
提供RESTful API给前端调用
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).parent
NOTES_DIR = BASE_DIR / "logs"

@app.route('/api/notes', methods=['GET'])
def get_notes():
    """获取笔记列表"""
    notes = []
    if NOTES_DIR.exists():
        for file in NOTES_DIR.glob("*.md"):
            stat = file.stat()

            # 提取标题（从文件内容）
            title = None
            preview = ""
            try:
                content = file.read_text(encoding='utf-8')
                lines = content.split('\n')

                # 跳过通用标题，寻找更有意义的标题
                skip_titles = ['完成的任务', '已完成的任务', '任务完成', '会话总结']
                found_meaningful_title = False

                for line in lines[:30]:  # 扩大搜索范围
                    line = line.strip()
                    if line.startswith('## ') and not line.replace('## ', '').strip() in skip_titles:
                        title = line.replace('## ', '').strip()
                        found_meaningful_title = True
                        break

                # 如果没找到有意义的标题，尝试从内容中提取关键词
                if not found_meaningful_title:
                    # 查找第一行有实际内容的行
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('#') and not line.startswith('**') and len(line) > 10:
                            preview = line[:80]
                            # 用预览内容的前几个词作为标题
                            words = preview.split()[:5]
                            title = ' '.join(words) + '...'
                            break

                # 提取预览文本
                in_code_block = False
                for line in lines:
                    line = line.strip()
                    if line.startswith('```'):
                        in_code_block = not in_code_block
                        continue
                    if in_code_block:
                        if line and not line.startswith('#') and not line.startswith('**'):
                            preview = line[:100]
                            break
                    elif line and not line.startswith('#') and not line.startswith('**') and not line.startswith('---') and not line.startswith('*') and len(line) > 10:
                        preview = line[:100]
                        break
            except:
                pass

            # 如果没有找到标题，使用文件名
            if not title:
                title = file.name

            notes.append({
                "name": file.name,
                "title": title,
                "preview": preview,
                "size": stat.st_size,
                "modified": int(stat.st_mtime)
            })

    # 按修改时间排序
    notes.sort(key=lambda x: x['modified'], reverse=True)
    return jsonify(notes)

@app.route('/api/note/<filename>', methods=['GET'])
def get_note(filename):
    """读取笔记内容"""
    try:
        note_file = NOTES_DIR / filename
        if not note_file.exists():
            return jsonify({"error": "笔记不存在"}), 404

        content = note_file.read_text(encoding='utf-8')
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/note/<filename>', methods=['DELETE'])
def delete_note(filename):
    """删除笔记"""
    try:
        note_file = NOTES_DIR / filename
        if not note_file.exists():
            return jsonify({"error": "笔记不存在"}), 404

        note_file.unlink()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/summarize', methods=['POST'])
def summarize():
    """触发总结"""
    try:
        import subprocess
        import sys

        # 检查模式参数
        mode = request.args.get('mode', 'manual')  # 默认手动模式

        # 使用完整的Python路径
        python_path = sys.executable

        # 根据模式决定是否添加--no-auto-select参数
        if mode == 'manual':
            # 手动复制模式：禁用自动选中
            cmd = [python_path, 'src/main.py', '--once', '--no-auto-select']
        else:
            # 自动选中模式：启用自动选中
            cmd = [python_path, 'src/main.py', '--once']

        result = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=60
        )

        print(f"模式: {mode}", file=sys.stderr)
        print(f"命令: {' '.join(cmd)}", file=sys.stderr)
        print(f"Python路径: {python_path}", file=sys.stderr)
        print(f"工作目录: {BASE_DIR}", file=sys.stderr)
        print(f"返回码: {result.returncode}", file=sys.stderr)
        print(f"标准输出: {result.stdout[:200]}", file=sys.stderr)
        print(f"标准错误: {result.stderr[:200]}", file=sys.stderr)

        if result.returncode == 0:
            return jsonify({"success": True, "output": result.stdout})
        else:
            return jsonify({"success": False, "error": result.stderr or "未知错误"}), 500
    except subprocess.TimeoutExpired:
        return jsonify({"success": False, "error": "总结超时（60秒）"}), 500
    except Exception as e:
        print(f"API错误: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取配置"""
    try:
        config_file = BASE_DIR / "config" / "config.yaml"
        if config_file.exists():
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return jsonify(config)
        return jsonify({})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/config', methods=['POST'])
def save_config():
    """保存配置"""
    try:
        config = request.json
        config_file = BASE_DIR / "config" / "config.yaml"

        import yaml
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True)

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计数据"""
    try:
        notes = []
        if NOTES_DIR.exists():
            notes = list(NOTES_DIR.glob("*.md"))

        return jsonify({
            "total_notes": len(notes),
            "total_saves": len(notes) * 5,  # 估算节省时间
            "most_used_model": "DeepSeek"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/env', methods=['GET'])
def get_env():
    """获取环境变量(API密钥)"""
    try:
        env_file = BASE_DIR / ".env"
        if env_file.exists():
            content = env_file.read_text(encoding='utf-8')
            # 解析.env文件,提取API密钥
            env_vars = {}
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if 'API_KEY' in key:
                        env_vars[key] = value
            return jsonify(env_vars)
        return jsonify({})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/env', methods=['POST'])
def save_env():
    """保存环境变量(API密钥)"""
    try:
        env_data = request.json
        env_file = BASE_DIR / ".env"

        # 读取现有.env文件
        if env_file.exists():
            lines = env_file.read_text(encoding='utf-8').split('\n')
        else:
            lines = []

        # 更新API密钥
        updated_keys = set()
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and '=' in stripped:
                key = stripped.split('=', 1)[0]
                if key in env_data:
                    lines[i] = f"{key}={env_data[key]}"
                    updated_keys.add(key)

        # 添加新的密钥
        for key, value in env_data.items():
            if key not in updated_keys:
                lines.append(f"{key}={value}")

        # 写回文件
        env_file.write_text('\n'.join(lines), encoding='utf-8')
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("================================================")
    print("  🌐 快捷总结笔记 - Web API服务")
    print("================================================")
    print("")
    print("API地址: http://localhost:5000")
    print("前端地址: http://localhost:8080")
    print("")
    print("按 Ctrl+C 停止服务")
    print("================================================")
    print("")

    app.run(host='0.0.0.0', port=5000, debug=True)
