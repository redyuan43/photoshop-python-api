# -*- coding: utf-8 -*-
"""
动作注册表系统

功能：
1. 加载YAML动作定义
2. 基于动作名称查找API实现
3. 参数验证和默认值处理
"""

import json
import glob
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


class ActionRegistry:
    """动作注册表"""

    def __init__(self, actions_dir: str = None):
        self.actions_dir = Path(actions_dir) if actions_dir else Path(__file__).parent / "actions"
        self.artifacts_dir = Path(__file__).parent / "artifacts"

        # 加载动作定义
        self.actions = self._load_actions()

        # 加载metadata
        self.metadata = self._load_metadata()

        # 加载OpenAI functions
        self.functions = self._load_functions()

    def _load_actions(self) -> Dict[str, Any]:
        """从YAML文件加载动作定义"""
        actions = {}
        yaml_files = glob.glob(str(self.actions_dir / "*.yaml"))

        for file in yaml_files:
            with open(file, 'r', encoding='utf-8') as f:
                actions_in_file = yaml.safe_load(f)
                for action in actions_in_file:
                    actions[action['name']] = action

        return actions

    def _load_metadata(self) -> Dict[str, Any]:
        """加载metadata.json"""
        metadata_file = self.artifacts_dir / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _load_functions(self) -> list:
        """加载openai_functions.json"""
        functions_file = self.artifacts_dir / "openai_functions.json"
        if functions_file.exists():
            with open(functions_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def get_action(self, name: str) -> Optional[Dict[str, Any]]:
        """获取动作定义"""
        return self.actions.get(name)

    def get_metadata(self, name: str) -> Optional[Dict[str, Any]]:
        """获取动作元数据"""
        return self.metadata.get(name)

    def list_actions(self, category: str = None) -> list:
        """列出所有动作，可按类别过滤"""
        if not category:
            return list(self.actions.keys())
        return [name for name, action in self.actions.items()
                if action.get('category') == category]

    def get_categories(self) -> list:
        """获取所有类别"""
        categories = set()
        for action in self.actions.values():
            categories.add(action.get('category', 'unknown'))
        return sorted(categories)

    def extract_params(self, action_name: str, user_params: Dict[str, Any]) -> Dict[str, Any]:
        """提取并验证参数"""
        action = self.get_action(action_name)
        if not action:
            return user_params

        # 获取参数配置
        param_configs = action.get('params', {})
        result = {}

        for param_name, param_config in param_configs.items():
            # 使用用户提供的值或默认值
            if param_name in user_params:
                result[param_name] = user_params[param_name]
            elif 'default' in param_config:
                result[param_name] = param_config['default']

        return result

    def find_by_alias(self, text: str) -> Optional[str]:
        """根据别名查找动作"""
        text = text.lower().strip()

        for name, action in self.actions.items():
            aliases = action.get('aliases', [])
            for alias in aliases:
                if alias.lower() in text:
                    return name

        return None

    def get_action_info(self, name: str) -> Dict[str, Any]:
        """获取动作完整信息"""
        action = self.get_action(name)
        metadata = self.get_metadata(name)

        if not action:
            return {}

        return {
            'name': name,
            'category': action.get('category', ''),
            'description': action.get('description', ''),
            'aliases': action.get('aliases', []),
            'params': action.get('params', {}),
            'metadata': metadata.get(name, {}) if metadata else {}
        }


# 全局注册表实例
registry = ActionRegistry()


if __name__ == "__main__":
    # 测试代码
    print("动作注册表测试")
    print("=" * 60)

    # 列出所有类别
    print("\n类别列表:")
    for cat in registry.get_categories():
        print(f"  - {cat}")

    # 列出所有动作
    print("\n动作列表:")
    for name, info in sorted([(n, registry.get_action_info(n)) for n in registry.list_actions()]):
        print(f"  {name}: {info['description']}")

    # 测试查找
    print("\n测试别名查找:")
    test_texts = ["锐化图像", "新建文档", "旋转图层45度"]
    for text in test_texts:
        action = registry.find_by_alias(text)
        print(f"  '{text}' -> {action}")
