# -*- coding: utf-8 -*-
"""
实时语音控制测试用例 v2 - 支持完整功能
- 真实Gemma3n调用
- 多轮对话
- 4个核心功能
- "无法实现"处理
"""

import requests
import json
import time
import re
from typing import Dict, Any


class GemmaLLMClient:
    """Gemma3n LLM客户端"""

    def __init__(self, model_name: str = "gemma3n:latest", base_url: str = "http://localhost:11434/v1"):
        self.model_name = model_name
        self.base_url = base_url
        self.supported_actions = ['smart_sharpen', 'new_document', 'rotate_layer', 'create_rectangle']

    def analyze_intent(self, user_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """分析用户意图"""
        context = context or {}

        # 构建系统prompt
        system_prompt = self._build_system_prompt(context)

        # 构建消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]

        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.3
            }
        }

        try:
            url = f"{self.base_url}/chat/completions"
            response = requests.post(url, json=payload, timeout=90)

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()

                # 清理响应
                content = content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                content = content.strip()

                # 尝试解析JSON
                try:
                    parsed = json.loads(content)
                    return {
                        'success': True,
                        'data': parsed,
                        'raw_response': content
                    }
                except json.JSONDecodeError as e:
                    return {
                        'success': False,
                        'error': f'JSON解析失败: {str(e)}',
                        'raw_response': content
                    }
            else:
                return {
                    'success': False,
                    'error': f'API请求失败: {response.status_code}',
                    'raw_response': None
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'异常: {str(e)}',
                'raw_response': None
            }

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """构建系统提示词"""
        pending_action = context.get('pending_action')
        collected_params = context.get('collected_params', {})

        prompt = f"""你是一个专业的Photoshop语音助手。用户会用自然语言描述需求。

重要规则：
1. 如果用户的需求不在以下4个可用动作内，直接回复无法实现
2. 返回JSON格式：{{"intent_type": "类型", "action": "动作名", "params": {{}}, "complete": true/false, "response": "回复"}}

可用动作（只有这4个）：
1. smart_sharpen - 智能锐化图像
   params: amount(0-500, 默认100), radius(0.1-50, 默认3.0), noiseReduction(0-100, 默认20)
2. new_document - 新建文档
   params: width(默认800), height(默认600)
3. rotate_layer - 旋转图层
   params: angle(-360到360, 默认45)
4. create_rectangle - 创建矩形
   params: x(默认100), y(默认100), width(默认100), height(默认100), color(默认红色)

如果用户的需求不在以上4个动作内，intent_type设为"unsupported"，action设为null。

intent_type说明：
- "unsupported": 不支持的功能
- "new_action": 新动作指令
- "provide_params": 提供参数
- "modify_params": 修改参数
- "ask_question": 需要询问

对话状态：
- 待处理动作: {pending_action or '无'}
- 已收集参数: {collected_params}

返回JSON，只返回JSON，不要其他内容！"""

        return prompt


class ConversationSession:
    """对话会话管理"""

    def __init__(self):
        self.llm = GemmaLLMClient()
        self.history = []
        self.context = {
            'pending_action': None,
            'collected_params': {}
        }

    def process_message(self, user_text: str) -> str:
        """处理用户消息"""
        print(f"\n[用户输入] {user_text}")

        # 调用LLM分析
        print("[分析] 正在调用Gemma3n模型...")
        result = self.llm.analyze_intent(user_text, self.context)

        if not result['success']:
            return f"[错误] LLM分析失败: {result['error']}"

        data = result['data']
        print(f"[LLM响应] {json.dumps(data, ensure_ascii=False, indent=2)}")

        # 更新上下文
        self._update_context(data)

        # 检查是否不支持
        if data.get('intent_type') == 'unsupported':
            self.context['pending_action'] = None
            self.context['collected_params'] = {}
            return "[助手] 对不起，该功能暂时无法实现。目前只支持：智能锐化、新建文档、旋转图层、创建矩形。"

        # 检查是否完整
        if self.context['pending_action'] and self.context['collected_params']:
            action_name = self.context['pending_action']
            params = self.context['collected_params']

            print(f"[模拟执行] 正在执行 {action_name}...")

            # 模拟API执行（实际环境需安装photoshop模块）
            api_result = self._simulate_api_execution(action_name, params)

            # 清空上下文
            self.context['pending_action'] = None
            self.context['collected_params'] = {}

            return f"[成功] {api_result['message']}"

        # 返回LLM的回复
        response = data.get('response', '请继续...')
        return f"[助手] {response}"

    def _update_context(self, data: Dict[str, Any]):
        """更新对话上下文"""
        intent_type = data.get('intent_type')
        action = data.get('action')
        params = data.get('params', {})
        complete = data.get('complete', False)

        if intent_type == 'new_action':
            self.context['pending_action'] = action
            self.context['collected_params'] = params
        elif intent_type == 'provide_params':
            self.context['collected_params'].update(params)
        elif intent_type == 'modify_params':
            self.context['collected_params'] = params

    def _simulate_api_execution(self, action_name: str, params: dict) -> Dict[str, Any]:
        """模拟API执行"""
        if action_name == 'smart_sharpen':
            amount = params.get('amount', 100)
            radius = params.get('radius', 3.0)
            noise = params.get('noiseReduction', 20)
            return {
                'success': True,
                'message': f'Smart Sharpen 成功执行 (amount: {amount}, radius: {radius}, noise: {noise}%)'
            }
        elif action_name == 'new_document':
            width = params.get('width', 800)
            height = params.get('height', 600)
            return {
                'success': True,
                'message': f'文档创建成功 ({width}x{height})'
            }
        elif action_name == 'rotate_layer':
            angle = params.get('angle', 45)
            return {
                'success': True,
                'message': f'图层旋转成功 ({angle}度)'
            }
        elif action_name == 'create_rectangle':
            x = params.get('x', 100)
            y = params.get('y', 100)
            width = params.get('width', 100)
            height = params.get('height', 100)
            return {
                'success': True,
                'message': f'矩形创建成功 (位置: ({x}, {y}), 大小: {width}x{height})'
            }
        else:
            return {
                'success': False,
                'message': f'未知动作: {action_name}'
            }

    def show_status(self):
        """显示当前状态"""
        print("\n=== 对话状态 ===")
        print(f"待处理动作: {self.context['pending_action']}")
        print(f"已收集参数: {self.context['collected_params']}")
        print("================\n")


def run_comprehensive_test():
    """运行综合测试"""
    print("=" * 70)
    print(" Photoshop语音控制 - 综合功能测试")
    print("=" * 70)

    session = ConversationSession()

    # 测试用例
    test_cases = [
        # 场景1: 智能锐化
        {
            "title": "场景1: 智能锐化",
            "messages": [
                "我要锐化图像",
                "强度150，半径5"
            ]
        },
        # 场景2: 创建矩形
        {
            "title": "场景2: 创建矩形",
            "messages": [
                "创建一个蓝色矩形",
                "位置(200, 150)，大小300x200"
            ]
        },
        # 场景3: 新建文档
        {
            "title": "场景3: 新建文档",
            "messages": [
                "我想新建一个文档",
                "1200x800像素"
            ]
        },
        # 场景4: 旋转图层
        {
            "title": "场景4: 旋转图层",
            "messages": [
                "旋转图层",
                "30度"
            ]
        },
        # 场景5: 不支持的功能
        {
            "title": "场景5: 不支持的功能（自动回复无法实现）",
            "messages": [
                "我想添加文字",
                "我想删除图层"
            ]
        },
        # 场景6: 混合对话
        {
            "title": "场景6: 混合对话",
            "messages": [
                "撤销上一步",
                "我想锐化",
                "强度200，半径2"
            ]
        }
    ]

    for test_case in test_cases:
        print(f"\n\n{'=' * 70}")
        print(f" {test_case['title']}")
        print('=' * 70)

        for msg in test_case['messages']:
            response = session.process_message(msg)
            print(response)
            time.sleep(1)

        session.show_status()

    print("\n" + "=" * 70)
    print(" 测试完成!")
    print("=" * 70)
    print("\n支持的功能:")
    print("  1. smart_sharpen - 智能锐化")
    print("  2. new_document - 新建文档")
    print("  3. rotate_layer - 旋转图层")
    print("  4. create_rectangle - 创建矩形")
    print("\n其他功能将自动回复: '对不起，该功能暂时无法实现'")
    print("=" * 70)


if __name__ == "__main__":
    run_comprehensive_test()
