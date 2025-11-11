# -*- coding: utf-8 -*-
"""
意图解析器 - 分层降级策略

优先级：
1. YAML + 正则（80%场景，$0成本）
2. 本地LLM（Jetson，15%场景）
3. 云端LLM（Claude，5%场景）
"""

import re
import json
from typing import Dict, Any, Optional
from action_registry import ActionRegistry


class IntentParser:
    """意图解析器"""

    def __init__(self):
        self.registry = ActionRegistry()
        self.usage_stats = {
            'yaml_regex': 0,
            'local_llm': 0,
            'cloud_llm': 0
        }

    def parse(self, user_text: str) -> Dict[str, Any]:
        """解析用户意图 - 分层策略"""
        user_text = user_text.strip()

        # 1. 尝试 YAML + 正则
        result = self._try_yaml_regex(user_text)
        if result and result['confidence'] >= 0.8:
            self.usage_stats['yaml_regex'] += 1
            return result

        # 2. 尝试本地LLM（Jetson）
        result = self._try_local_llm(user_text)
        if result and result['confidence'] >= 0.8:
            self.usage_stats['local_llm'] += 1
            return result

        # 3. 最后才用云端LLM（Claude）
        result = self._try_cloud_llm(user_text)
        self.usage_stats['cloud_llm'] += 1
        return result

    def _try_yaml_regex(self, user_text: str) -> Optional[Dict[str, Any]]:
        """策略1: YAML + 正则匹配"""
        # 通过ActionRegistry查找
        action_name = self.registry.find_by_alias(user_text)

        if not action_name:
            # 尝试直接匹配动作名称（改进的匹配逻辑）
            for name in self.registry.list_actions():
                metadata = self.registry.get_metadata(name)
                aliases = metadata.get('aliases', [])

                # 智能匹配：检查是否包含关键词
                for alias in aliases:
                    if self._text_contains_alias(user_text, alias):
                        action_name = name
                        break

                if action_name:
                    break

        if not action_name:
            return None

        # 提取参数
        params = self._extract_params_regex(user_text, action_name)

        # 计算置信度（基于是否提取到参数）
        confidence = 0.9 if params else 0.8

        return {
            'strategy': 'yaml_regex',
            'action': action_name,
            'params': params,
            'confidence': confidence
        }

    def _text_contains_alias(self, text: str, alias: str) -> bool:
        """检查文本是否包含别名（智能匹配）"""
        text = text.lower()
        alias = alias.lower()

        # 直接匹配
        if alias in text:
            return True

        # 智能匹配：检查别名中的关键词是否都出现在文本中
        # 用于处理"新建一个文档" vs "新建文档"
        alias_keywords = self._split_chinese_phrase(alias)

        if len(alias_keywords) > 1:
            # 检查所有关键词是否都在文本中（不要求连续）
            return all(keyword in text for keyword in alias_keywords)

        return False

    def _split_chinese_phrase(self, phrase: str) -> list:
        """将中文短语拆分为关键词"""
        # 常见分隔符
        separators = ['的', '和', '与', '或', '一', '一个']

        # 如果包含分隔符，尝试拆分
        for sep in separators:
            if sep in phrase:
                parts = phrase.split(sep)
                result = []
                for part in parts:
                    if part.strip():
                        result.append(part.strip())
                return result

        # 如果没有分隔符，尝试按常见词拆分
        common_words = ['新建', '文档', '创建', '矩形', '锐化', '图像', '旋转', '图层']
        result = []
        for word in common_words:
            if word in phrase:
                result.append(word)

        # 如果没找到常见词，返回原短语
        if not result:
            result = [phrase]

        return result

    def _extract_params_regex(self, user_text: str, action_name: str) -> Dict[str, Any]:
        """使用正则表达式提取参数"""
        params = {}

        # 尺寸格式: "200x150"
        size_match = re.search(r'(\d+)x(\d+)', user_text)
        if size_match:
            params['width'] = int(size_match.group(1))
            params['height'] = int(size_match.group(2))

        # 位置格式: "位置100,200"
        pos_match = re.search(r'位置[为]?(\d+)[,，](\d+)', user_text)
        if pos_match:
            params['x'] = int(pos_match.group(1))
            params['y'] = int(pos_match.group(2))

        # 角度格式: "45度"
        angle_match = re.search(r'(\d+(?:\.\d+)?)度', user_text)
        if angle_match:
            params['angle'] = float(angle_match.group(1))

        # 锐化强度: "强度100"
        amount_match = re.search(r'强度[为]?(\d+)', user_text)
        if amount_match:
            params['amount'] = float(amount_match.group(1))

        # 半径: "半径3.0"
        radius_match = re.search(r'半径[为]?(\d+(?:\.\d+)?)', user_text)
        if radius_match:
            params['radius'] = float(radius_match.group(1))

        # 应用默认值
        params = self.registry.extract_params(action_name, params)

        return params

    def _try_local_llm(self, user_text: str) -> Optional[Dict[str, Any]]:
        """策略2: 本地LLM (Jetson)"""
        # TODO: 实现本地LLM调用
        # 这里是占位符，后续实现

        # 模拟实现：
        # 1. 连接到Jetson本地模型API
        # 2. 发送请求
        # 3. 解析响应

        print("[LOCAL_LLM] Jetson本地模型调用 (待实现)")
        return None

    def _try_cloud_llm(self, user_text: str) -> Optional[Dict[str, Any]]:
        """策略3: 云端LLM (Claude)"""
        # TODO: 实现Claude调用
        # 这里是占位符，后续实现

        # 模拟实现：
        # 1. 构建prompt
        # 2. 调用Claude API
        # 3. 解析JSON响应

        print("[CLOUD_LLM] Claude云端模型调用 (待实现)")
        return None

    def get_usage_stats(self) -> Dict[str, int]:
        """获取使用统计"""
        return self.usage_stats.copy()


def test_parser():
    """测试解析器"""
    parser = IntentParser()

    test_cases = [
        "我想锐化图像",
        "创建一个200x150的矩形",
        "新建一个800x600的文档",
        "旋转图层45度",
        "在位置100,200创建一个矩形",
    ]

    print("=" * 60)
    print("意图解析器测试")
    print("=" * 60)

    for text in test_cases:
        print(f"\n输入: {text}")
        result = parser.parse(text)

        if result:
            print(f"  策略: {result['strategy']}")
            print(f"  动作: {result['action']}")
            print(f"  参数: {result['params']}")
            print(f"  置信度: {result['confidence']}")
        else:
            print("  未识别")

    print("\n" + "=" * 60)
    print("使用统计:")
    print(parser.get_usage_stats())
    print("=" * 60)


if __name__ == "__main__":
    test_parser()
