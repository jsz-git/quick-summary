"""
AI总结器基类和多模型支持
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os


class BaseSummarizer(ABC):
    """AI总结器基类"""

    def __init__(self, config: Dict[str, Any], api_key: str = None):
        self.config = config
        self.api_key = api_key
        self.model = config.get('ai_model', 'default')
        self.max_tokens = config.get('max_tokens', 2048)
        self.temperature = config.get('temperature', 0.3)

    @abstractmethod
    def summarize(self, conversation_text: str) -> str:
        """
        使用AI生成会话总结

        Args:
            conversation_text: 对话内容

        Returns:
            Markdown格式的总结
        """
        pass

    def _build_prompt(self, text: str) -> str:
        """构建AI提示词（通用）"""
        return f"""请分析以下对话内容，生成一个结构化的会话总结。

要求：
1. 提取完成的主要任务和步骤
2. 列出执行的关键命令（如果有）
3. 识别修改或涉及的文件
4. 总结遇到的问题和解决方案
5. 记录重要的技术决策

对话内容：
{text}

请以Markdown格式输出，包含以下部分：
- 完成的任务
- 执行的命令
- 修改的文件
- 问题与解决方案
- 关键决策

保持简洁明了，突出重点。"""

    def _format_summary(self, summary: str) -> str:
        """格式化总结，添加时间戳等元数据"""
        from utils import get_timestamp
        timestamp = get_timestamp()

        header = f"""# 会话总结

**生成时间**: {timestamp}
**AI模型**: {self.model}

---

"""
        return header + summary

    def _generate_error_summary(self, error: str, original_text: str) -> str:
        """生成错误时的备用总结"""
        from utils import get_timestamp, truncate_text
        timestamp = get_timestamp()

        return f"""# 会话总结（自动生成）

**生成时间**: {timestamp}
**状态**: ⚠️ AI总结失败，使用简化格式

---

## 原始对话

{truncate_text(original_text, max_length=2000)}

---

## 错误信息

{error}
"""


class ClaudeSummarizer(BaseSummarizer):
    """Anthropic Claude 总结器"""

    def __init__(self, config: Dict[str, Any], api_key: str):
        super().__init__(config, api_key)
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError("未安装 anthropic 库，请运行: pip install anthropic")

    def summarize(self, conversation_text: str) -> str:
        """使用 Claude 生成总结"""
        from utils import truncate_text

        truncated_text = truncate_text(conversation_text, max_length=10000)
        prompt = self._build_prompt(truncated_text)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            summary = response.content[0].text
            return self._format_summary(summary)

        except Exception as e:
            print(f"❌ Claude总结失败: {e}")
            return self._generate_error_summary(str(e), conversation_text)


class OpenAISummarizer(BaseSummarizer):
    """OpenAI GPT 总结器"""

    def __init__(self, config: Dict[str, Any], api_key: str):
        super().__init__(config, api_key)
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("未安装 openai 库，请运行: pip install openai")

    def summarize(self, conversation_text: str) -> str:
        """使用 GPT 生成总结"""
        from utils import truncate_text

        truncated_text = truncate_text(conversation_text, max_length=10000)
        prompt = self._build_prompt(truncated_text)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            summary = response.choices[0].message.content
            return self._format_summary(summary)

        except Exception as e:
            print(f"❌ OpenAI总结失败: {e}")
            return self._generate_error_summary(str(e), conversation_text)


class DeepSeekSummarizer(BaseSummarizer):
    """DeepSeek 总结器"""

    def __init__(self, config: Dict[str, Any], api_key: str):
        super().__init__(config, api_key)
        try:
            from openai import OpenAI
            # DeepSeek 使用 OpenAI 兼容接口
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com/v1"
            )
        except ImportError:
            raise ImportError("未安装 openai 库，请运行: pip install openai")

    def summarize(self, conversation_text: str) -> str:
        """使用 DeepSeek 生成总结"""
        from utils import truncate_text

        truncated_text = truncate_text(conversation_text, max_length=10000)
        prompt = self._build_prompt(truncated_text)

        try:
            response = self.client.chat.completions.create(
                model=self.model or "deepseek-chat",
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            summary = response.choices[0].message.content
            return self._format_summary(summary)

        except Exception as e:
            print(f"❌ DeepSeek总结失败: {e}")
            return self._generate_error_summary(str(e), conversation_text)


class QwenSummarizer(BaseSummarizer):
    """通义千问 (Qwen) 总结器"""

    def __init__(self, config: Dict[str, Any], api_key: str):
        super().__init__(config, api_key)
        try:
            from openai import OpenAI
            # 通义千问使用 OpenAI 兼容接口
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
        except ImportError:
            raise ImportError("未安装 openai 库，请运行: pip install openai")

    def summarize(self, conversation_text: str) -> str:
        """使用通义千问生成总结"""
        from utils import truncate_text

        truncated_text = truncate_text(conversation_text, max_length=10000)
        prompt = self._build_prompt(truncated_text)

        try:
            response = self.client.chat.completions.create(
                model=self.model or "qwen-plus",
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            summary = response.choices[0].message.content
            return self._format_summary(summary)

        except Exception as e:
            print(f"❌ 通义千问总结失败: {e}")
            return self._generate_error_summary(str(e), conversation_text)


class LocalModelSummarizer(BaseSummarizer):
    """本地模型总结器（Ollama等）"""

    def __init__(self, config: Dict[str, Any], endpoint: str = "http://localhost:11434"):
        super().__init__(config)
        self.endpoint = endpoint
        try:
            import requests
            self.requests = requests
        except ImportError:
            raise ImportError("未安装 requests 库，请运行: pip install requests")

    def summarize(self, conversation_text: str) -> str:
        """使用本地模型生成总结"""
        from utils import truncate_text

        truncated_text = truncate_text(conversation_text, max_length=10000)
        prompt = self._build_prompt(truncated_text)

        try:
            # Ollama API
            response = self.requests.post(
                f"{self.endpoint}/api/generate",
                json={
                    "model": self.model or "llama2",
                    "prompt": prompt,
                    "stream": False
                }
            )

            if response.status_code == 200:
                result = response.json()
                summary = result.get('response', '')
                return self._format_summary(summary)
            else:
                raise Exception(f"API返回错误: {response.status_code}")

        except Exception as e:
            print(f"❌ 本地模型总结失败: {e}")
            return self._generate_error_summary(str(e), conversation_text)


def create_summarizer(config: Dict[str, Any]) -> BaseSummarizer:
    """
    工厂函数：根据配置创建对应的总结器

    Args:
        config: 配置字典

    Returns:
        BaseSummarizer 实例
    """
    provider = config.get('ai_provider', 'anthropic')
    model = config.get('ai_model', '')

    print(f"🤖 初始化 AI 总结器: {provider} / {model}")

    if provider == 'anthropic' or provider == 'claude':
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("未设置 ANTHROPIC_API_KEY 环境变量")
        return ClaudeSummarizer(config, api_key)

    elif provider == 'openai' or provider == 'gpt':
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("未设置 OPENAI_API_KEY 环境变量")
        return OpenAISummarizer(config, api_key)

    elif provider == 'deepseek':
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            raise ValueError("未设置 DEEPSEEK_API_KEY 环境变量")
        return DeepSeekSummarizer(config, api_key)

    elif provider == 'qwen' or provider == 'tongyi':
        api_key = os.getenv('QWEN_API_KEY') or os.getenv('DASHSCOPE_API_KEY')
        if not api_key:
            raise ValueError("未设置 QWEN_API_KEY 或 DASHSCOPE_API_KEY 环境变量")
        return QwenSummarizer(config, api_key)

    elif provider == 'local' or provider == 'ollama':
        endpoint = config.get('local_endpoint', 'http://localhost:11434')
        return LocalModelSummarizer(config, endpoint)

    else:
        raise ValueError(f"不支持的 AI 提供商: {provider}")


# 为了向后兼容，保留旧的 SessionSummarizer 类名
SessionSummarizer = create_summarizer


if __name__ == "__main__":
    # 测试多模型支持
    from utils import load_config

    print("测试多模型支持...")
    print("\n可用的 AI 提供商:")
    print("1. anthropic (Claude)")
    print("2. openai (GPT)")
    print("3. deepseek")
    print("4. qwen (通义千问)")
    print("5. local (Ollama)")

    config = load_config()
    provider = config.get('ai_provider', 'anthropic')

    print(f"\n当前配置: {provider}")

    try:
        summarizer = create_summarizer(config)
        print(f"✅ 成功创建 {type(summarizer).__name__}")
    except Exception as e:
        print(f"❌ 创建失败: {e}")
