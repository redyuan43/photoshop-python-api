# -*- coding: utf-8 -*-
"""
LLM模型配置和管理

支持多种大模型：
1. OpenAI GPT-4/3.5
2. Anthropic Claude
3. 本地模型（Ollama等）
4. 其他兼容OpenAI API的模型
"""

import json
from typing import Dict, List, Optional, Union


class ModelConfig:
    """模型配置"""

    def __init__(self,
                 name: str,
                 model: str,
                 base_url: str,
                 api_key: Optional[str] = None,
                 description: str = "",
                 cost_per_token: float = 0.0,
                 max_tokens: int = 4096,
                 supports_json: bool = True):
        self.name = name
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.description = description
        self.cost_per_token = cost_per_token
        self.max_tokens = max_tokens
        self.supports_json = supports_json

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'name': self.name,
            'model': self.model,
            'base_url': self.base_url,
            'description': self.description,
            'cost_per_token': self.cost_per_token,
            'max_tokens': self.max_tokens,
            'supports_json': self.supports_json
        }


class ModelManager:
    """模型管理器"""

    def __init__(self):
        self.models = {}
        self.current_model = None
        self._init_default_models()

    def _init_default_models(self):
        """初始化默认模型"""
        # OpenAI Models
        self.register_model(ModelConfig(
            name="GPT-4",
            model="gpt-4",
            base_url="https://api.openai.com/v1",
            description="OpenAI GPT-4 - 最强通用模型",
            cost_per_token=0.03
        ))

        self.register_model(ModelConfig(
            name="GPT-3.5-Turbo",
            model="gpt-3.5-turbo",
            base_url="https://api.openai.com/v1",
            description="OpenAI GPT-3.5 - 性价比高",
            cost_per_token=0.002
        ))

        # Anthropic Claude
        self.register_model(ModelConfig(
            name="Claude-3-Sonnet",
            model="claude-3-sonnet-20240229",
            base_url="https://api.anthropic.com/v1",
            description="Anthropic Claude 3 Sonnet - 专业可靠",
            cost_per_token=0.015
        ))

        # Local Models (Ollama)
        self.register_model(ModelConfig(
            name="Qwen-14B (本地)",
            model="qwen:14b-chat",
            base_url="http://localhost:11434/v1",
            description="阿里云通义千问 14B - 本地部署",
            cost_per_token=0.0,
            supports_json=False
        ))

        self.register_model(ModelConfig(
            name="Llama2-13B (本地)",
            model="llama2:13b-chat",
            base_url="http://localhost:11434/v1",
            description="Meta Llama2 13B - 本地部署",
            cost_per_token=0.0,
            supports_json=False
        ))

        self.register_model(ModelConfig(
            name="ChatGLM3-13B (本地)",
            model="chatglm3:13b",
            base_url="http://localhost:11434/v1",
            description="智谱 ChatGLM3 13B - 本地部署",
            cost_per_token=0.0,
            supports_json=False
        ))

        self.register_model(ModelConfig(
            name="Gemma3n-Latest (本地)",
            model="gemma3n:latest",
            base_url="http://localhost:11434/v1",
            description="Google Gemma 3 - 最新版本",
            cost_per_token=0.0,
            supports_json=False
        ))

        self.register_model(ModelConfig(
            name="Qwen3-4B (本地)",
            model="qwen3:4b",
            base_url="http://localhost:11434/v1",
            description="阿里云通义千问3 4B - 速度快，需thinking提取",
            cost_per_token=0.0,
            supports_json=True,
            max_tokens=512
        ))

        # 设置默认模型
        self.set_current_model("GPT-4")

    def register_model(self, config: ModelConfig):
        """注册模型"""
        self.models[config.name] = config

    def set_current_model(self, name: str) -> bool:
        """设置当前模型"""
        if name in self.models:
            self.current_model = name
            return True
        return False

    def get_current_model(self) -> Optional[ModelConfig]:
        """获取当前模型"""
        if self.current_model:
            return self.models[self.current_model]
        return None

    def list_models(self) -> List[ModelConfig]:
        """列出所有模型"""
        return list(self.models.values())

    def get_model(self, name: str) -> Optional[ModelConfig]:
        """获取指定模型"""
        return self.models.get(name)

    def load_from_config(self, config_file: str):
        """从配置文件加载模型"""
        with open(config_file, 'r', encoding='utf-8') as f:
            configs = json.load(f)

        for config_dict in configs:
            config = ModelConfig(**config_dict)
            self.register_model(config)

    def save_to_config(self, config_file: str):
        """保存配置到文件"""
        configs = [model.to_dict() for model in self.models.values()]
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(configs, f, ensure_ascii=False, indent=2)

    def estimate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """估算成本"""
        model = self.get_current_model()
        if not model:
            return 0.0

        total_tokens = prompt_tokens + completion_tokens
        return total_tokens * model.cost_per_token


class LLMClient:
    """LLM客户端 - 兼容OpenAI API"""

    def __init__(self, model_config: ModelConfig, api_key: Optional[str] = None):
        self.config = model_config
        self.api_key = api_key or model_config.api_key
        self.client = self._create_client()

    def _create_client(self):
        """创建客户端"""
        # 实际实现中根据base_url创建不同客户端
        # import openai
        # if 'openai.com' in self.config.base_url:
        #     return openai.OpenAI(api_key=self.api_key, base_url=self.config.base_url)
        # else:
        #     # 其他兼容OpenAI API的服务
        #     return openai.OpenAI(api_key=self.api_key, base_url=self.config.base_url)
        return None

    def chat(self, messages: list, temperature: float = 0.3, max_tokens: int = None) -> dict:
        """发送聊天请求"""
        # 实际调用
        # response = self.client.chat.completions.create(
        #     model=self.config.model,
        #     messages=messages,
        #     temperature=temperature,
        #     max_tokens=max_tokens or self.config.max_tokens,
        #     response_format={'type': 'json_object'} if self.config.supports_json else None
        # )
        #
        # return {
        #     'content': response.choices[0].message.content,
        #     'model': response.model,
        #     'usage': response.usage.dict() if response.usage else None,
        #     'cost': self.config.cost_per_token * (response.usage.total_tokens if response.usage else 0)
        # }

        # 模拟响应
        return {
            'content': '{"intent_type": "new_action", "action": "smart_sharpen", "complete": false}',
            'model': self.config.model,
            'usage': {'total_tokens': 100, 'prompt_tokens': 80, 'completion_tokens': 20},
            'cost': self.config.cost_per_token * 100
        }

    def switch_model(self, new_config: ModelConfig):
        """切换模型"""
        self.config = new_config
        self.client = self._create_client()


def create_client(model_name: str, api_key: Optional[str] = None) -> LLMClient:
    """创建LLM客户端的便捷函数"""
    manager = ModelManager()
    model_config = manager.get_model(model_name)

    if not model_config:
        raise ValueError(f"Unknown model: {model_name}")

    return LLMClient(model_config, api_key)


def demo():
    """演示模型管理"""
    manager = ModelManager()

    print("=" * 60)
    print("LLM模型管理演示")
    print("=" * 60)

    # 列出所有模型
    print("\n可用模型:")
    for model in manager.list_models():
        print(f"  - {model.name}: {model.description}")
        print(f"    成本: ${model.cost_per_token}/token")

    # 切换模型
    print("\n切换到 GPT-3.5-Turbo")
    manager.set_current_model("GPT-3.5-Turbo")
    current = manager.get_current_model()
    print(f"当前模型: {current.name}")

    # 估算成本
    print("\n成本估算:")
    cost = manager.estimate_cost(100, 50)
    print(f"100 prompt + 50 completion 令牌成本: ${cost:.4f}")

    # 保存配置
    print("\n保存配置到 models.json")
    manager.save_to_config("models.json")

    # 创建客户端
    print("\n创建客户端")
    client = create_client("GPT-4", "your-api-key")

    # 发送请求
    print("\n发送测试请求")
    response = client.chat([
        {'role': 'system', 'content': '你是一个助手'},
        {'role': 'user', 'content': '你好'}
    ])

    print(f"响应: {response}")
    print(f"成本: ${response['cost']:.4f}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()
