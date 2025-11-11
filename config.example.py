# API密钥配置文件（请勿提交到git）
# 复制此文件为 config.py 并填入你的真实API密钥

import os
from typing import Optional

class APIConfig:
    """API配置管理类"""

    # 通义千问API密钥
    QWEN_API_KEY: str = os.environ.get("QWEN_API_KEY", "")

    # OpenAI API密钥
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")

    # Anthropic Claude API密钥
    ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")

    # Google AI API密钥（用于Gemma等模型）
    GOOGLE_API_KEY: str = os.environ.get("GOOGLE_API_KEY", "")

    # 其他模型API密钥
    CUSTOM_API_KEY: str = os.environ.get("CUSTOM_API_KEY", "")
    CUSTOM_API_BASE: str = os.environ.get("CUSTOM_API_BASE", "")

    @classmethod
    def validate_required_keys(cls) -> list[str]:
        """验证必需的API密钥是否存在"""
        missing_keys = []

        # 检查常用的API密钥
        if cls.QWEN_API_KEY:
            print("[OK] QWEN_API_KEY 已配置")
        else:
            missing_keys.append("QWEN_API_KEY")

        if cls.OPENAI_API_KEY:
            print("[OK] OPENAI_API_KEY 已配置")
        else:
            print("[WARN] OPENAI_API_KEY 未配置（可选）")

        if cls.ANTHROPIC_API_KEY:
            print("[OK] ANTHROPIC_API_KEY 已配置")
        else:
            print("[WARN] ANTHROPIC_API_KEY 未配置（可选）")

        return missing_keys

    @classmethod
    def get_qwen_config(cls) -> dict:
        """获取通义千问配置"""
        if not cls.QWEN_API_KEY:
            raise ValueError("QWEN_API_KEY 未配置，请设置环境变量或配置文件")

        return {
            "api_key": cls.QWEN_API_KEY,
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"  # 通义千问默认base_url
        }

    @classmethod
    def get_openai_config(cls) -> dict:
        """获取OpenAI配置"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY 未配置")

        return {
            "api_key": cls.OPENAI_API_KEY,
            "base_url": "https://api.openai.com/v1"
        }

    @classmethod
    def get_anthropic_config(cls) -> dict:
        """获取Anthropic配置"""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY 未配置")

        return {
            "api_key": cls.ANTHROPIC_API_KEY,
            "base_url": "https://api.anthropic.com"
        }

# 全局配置实例
api_config = APIConfig()

# 使用说明：
# 1. 复制此文件为 config.py: cp config.example.py config.py
# 2. 在 config.py 中填入你的真实API密钥
# 3. 或者设置环境变量：
#    export QWEN_API_KEY="your-qwen-api-key"
#    export OPENAI_API_KEY="your-openai-api-key"
#    export ANTHROPIC_API_KEY="your-anthropic-api-key"