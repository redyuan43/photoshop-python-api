# -*- coding: utf-8 -*-
"""
配置管理器 - 统一管理API密钥和配置信息
"""

import os
import yaml
from typing import Dict, Optional, Any
from pathlib import Path


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径，默认为当前目录下的config.yaml
        """
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), 'config.yaml')
        self.config_data: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        """加载配置文件"""
        # 尝试加载YAML配置文件
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config_data = yaml.safe_load(f) or {}
                print(f"[OK] 已加载配置文件: {self.config_path}")
            except Exception as e:
                print(f"[WARN] 加载配置文件失败: {e}")
                self.config_data = {}
        else:
            print(f"[WARN] 配置文件不存在: {self.config_path}")
            print("请复制 config.example.yaml 为 config.yaml 并配置API密钥")
            self.config_data = {}

    def get_api_key(self, provider: str) -> str:
        """
        获取API密钥

        Args:
            provider: 提供商名称 (qwen, openai, anthropic, google等)

        Returns:
            API密钥字符串
        """
        # 优先从环境变量获取
        env_key_map = {
            'qwen': 'QWEN_API_KEY',
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'google': 'GOOGLE_API_KEY',
            'custom': 'CUSTOM_API_KEY'
        }

        env_key = env_key_map.get(provider.lower())
        if env_key:
            api_key = os.environ.get(env_key)
            if api_key:
                return api_key

        # 从配置文件获取
        api_keys = self.config_data.get('api_keys', {})
        config_key_map = {
            'qwen': 'qwen_api_key',
            'openai': 'openai_api_key',
            'anthropic': 'anthropic_api_key',
            'google': 'google_api_key',
            'custom': 'custom_api_key'
        }

        config_key = config_key_map.get(provider.lower())
        if config_key:
            api_key = api_keys.get(config_key, "")
            if api_key:
                return api_key

        # 尝试从项目根目录的config.py获取
        try:
            import sys
            root_path = Path(__file__).parent.parent
            sys.path.insert(0, str(root_path))
            from config import api_config

            attr_map = {
                'qwen': 'QWEN_API_KEY',
                'openai': 'OPENAI_API_KEY',
                'anthropic': 'ANTHROPIC_API_KEY',
                'google': 'GOOGLE_API_KEY',
                'custom': 'CUSTOM_API_KEY'
            }

            attr = attr_map.get(provider.lower())
            if attr:
                api_key = getattr(api_config, attr, "")
                if api_key:
                    return api_key
        except ImportError:
            pass

        return ""

    def get_base_url(self, provider: str) -> str:
        """
        获取API基础URL

        Args:
            provider: 提供商名称

        Returns:
            API基础URL
        """
        # 从配置文件获取
        api_endpoints = self.config_data.get('api_endpoints', {})
        endpoint_map = {
            'qwen': 'qwen_base_url',
            'openai': 'openai_base_url',
            'anthropic': 'anthropic_base_url'
        }

        config_key = endpoint_map.get(provider.lower())
        if config_key:
            base_url = api_endpoints.get(config_key, "")
            if base_url:
                return base_url

        # 默认URL
        default_urls = {
            'qwen': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
            'openai': 'https://api.openai.com/v1',
            'anthropic': 'https://api.anthropic.com',
            'google': 'https://generativelanguage.googleapis.com/v1beta'
        }

        return default_urls.get(provider.lower(), "")

    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """
        获取模型配置

        Args:
            model_name: 模型名称

        Returns:
            模型配置字典
        """
        llm_config = self.config_data.get('llm', {})
        models = llm_config.get('models', {})

        # 查找模型配置
        if model_name in models:
            return models[model_name]

        # 查找默认模型
        default_model = llm_config.get('default_model', 'qwen3-4b')
        if default_model in models:
            return models[default_model]

        # 返回空配置
        return {}

    def validate_config(self) -> Dict[str, bool]:
        """
        验证配置

        Returns:
            各个提供商的配置状态
        """
        providers = ['qwen', 'openai', 'anthropic', 'google']
        status = {}

        for provider in providers:
            api_key = self.get_api_key(provider)
            base_url = self.get_base_url(provider)
            status[provider] = {
                'has_api_key': bool(api_key),
                'has_base_url': bool(base_url),
                'configured': bool(api_key and base_url)
            }

        return status

    def print_status(self):
        """打印配置状态"""
        print("API密钥配置状态:")
        print("=" * 50)

        status = self.validate_config()
        for provider, info in status.items():
            if info['configured']:
                print(f"[OK] {provider.upper()}: 已配置")
            else:
                missing = []
                if not info['has_api_key']:
                    missing.append("API密钥")
                if not info['has_base_url']:
                    missing.append("Base URL")
                print(f"[ERROR] {provider.upper()}: 缺少 {', '.join(missing)}")

        print("=" * 50)


# 全局配置管理器实例
config_manager = ConfigManager()