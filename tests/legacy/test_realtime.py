# -*- coding: utf-8 -*-
"""
实时语音控制测试用例
支持真实的多轮对话和Photoshop API调用
"""

import requests
import json
import time
import re
from typing import Dict, Any


class GemmaLLMClient:
    """Gemma3n LLM客户端 - 真实实现"""

    def __init__(self, model_name: str = "gemma3n:latest", base_url: str = "http://localhost:11434/v1"):
        self.model_name = model_name
        self.base_url = base_url
        self.chat_history = []

    def analyze_intent(self, user_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """分析用户意图，返回结构化JSON"""
        context = context or {}

        # 构建系统prompt
        system_prompt = self._build_system_prompt(context)

        # 构建消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]

        # 调用Gemma API
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

                # 清理响应（移除markdown标记）
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

        prompt = f"""你是一个专业的Photoshop语音助手。用户会用自然语言描述他们的需求，你需要理解并执行。

规则：
1. 返回纯JSON格式，不要任何额外文本
2. 格式：{{"intent_type": "类型", "action": "动作名", "params": {{}}, "complete": true/false, "response": "回复"}}

intent_type说明：
- "new_action": 新动作指令
- "provide_params": 提供参数
- "modify_params": 修改参数
- "ask_question": 需要询问

可用动作：
- smart_sharpen: 智能锐化
  params: amount(0-500, 默认100), radius(0.1-50, 默认3.0), noiseReduction(0-100, 默认20)
- new_document: 新建文档
  params: width(1-300000, 默认800), height(1-300000, 默认600)
- rotate_layer: 旋转图层
  params: angle(-360到360, 默认45)
- create_rectangle: 创建矩形
  params: x(默认100), y(默认100), width(默认100), height(默认100), color({{'red': 255, 'green': 100, 'blue': 100}})

对话状态：
- 待处理动作: {pending_action or '无'}
- 已收集参数: {collected_params}

返回JSON，只返回JSON，不要其他内容！"""

        return prompt


class PhotoshopAPI:
    """Photoshop API执行器 - 真实实现"""

    def __init__(self):
        pass

    def execute(self, action_name: str, params: dict) -> Dict[str, Any]:
        """执行Photoshop API调用"""
        try:
            from photoshop import Session

            with Session() as ps:
                if action_name == 'smart_sharpen':
                    return self._smart_sharpen(ps, params)
                elif action_name == 'new_document':
                    return self._new_document(ps, params)
                elif action_name == 'rotate_layer':
                    return self._rotate_layer(ps, params)
                elif action_name == 'create_rectangle':
                    return self._create_rectangle(ps, params)
                else:
                    return {
                        'success': False,
                        'message': f'未知动作: {action_name}'
                    }
        except Exception as e:
            return {
                'success': False,
                'message': f'API调用失败: {str(e)}',
                'error': str(e)
            }

    def _smart_sharpen(self, ps, params: dict) -> Dict[str, Any]:
        """智能锐化"""
        doc = ps.active_document
        layer = doc.activeLayer

        amount = params.get('amount', 100.0)
        radius = params.get('radius', 3.0)
        noise = params.get('noiseReduction', 20)

        # Action Manager调用
        idsmart_sharpen_id = ps.app.stringIDToTypeID(ps.EventID.SmartSharpen)
        desc = ps.ActionDescriptor()

        # PresetKind
        idpresetKind = ps.app.stringIDToTypeID(ps.EventID.PresetKind)
        idpresetKindType = ps.app.stringIDToTypeID(ps.EventID.PresetKindType)
        idpresetKindCustom = ps.app.stringIDToTypeID(ps.EventID.PresetKindCustom)
        desc.putEnumerated(idpresetKind, idpresetKindType, idpresetKindCustom)

        # Amount
        idAmnt = ps.app.charIDToTypeID("Amnt")
        idPrc = ps.app.charIDToTypeID("Rds ")
        desc.putUnitDouble(idAmnt, idPrc, amount)

        # Radius
        idRds = ps.app.charIDToTypeID("Rds ")
        idPxl = ps.app.charIDToTypeID("#Pxl")
        desc.putUnitDouble(idRds, idPxl, radius)

        # noiseReduction
        idnoiseReduction = ps.app.stringIDToTypeID("noiseReduction")
        desc.putUnitDouble(idnoiseReduction, idPrc, noise)

        # blur type
        idblur = ps.app.charIDToTypeID("blur")
        idblurType = ps.app.stringIDToTypeID("blurType")
        idGsnB = ps.app.charIDToTypeID("GsnB")
        desc.putEnumerated(idblur, idblurType, idGsnB)

        ps.app.ExecuteAction(idsmart_sharpen_id, desc)

        return {
            'success': True,
            'message': f'Smart Sharpen 成功 (amount: {amount}, radius: {radius}, noise: {noise}%)'
        }

    def _new_document(self, ps, params: dict) -> Dict[str, Any]:
        """新建文档"""
        width = params.get('width', 800)
        height = params.get('height', 600)
        doc = ps.app.documents.add(width=width, height=height)

        return {
            'success': True,
            'message': f'文档创建成功 ({width}x{height})'
        }

    def _rotate_layer(self, ps, params: dict) -> Dict[str, Any]:
        """旋转图层"""
        doc = ps.active_document
        angle = params.get('angle', 45)
        layer = doc.activeLayer

        if layer.isBackgroundLayer:
            layer = layer.duplicate()
            layer.isBackgroundLayer = False
            doc.activeLayer = layer

        layer.rotate(angle, ps.AnchorPosition.MiddleCenter)

        return {
            'success': True,
            'message': f'图层旋转成功 ({angle}度)'
        }

    def _create_rectangle(self, ps, params: dict) -> Dict[str, Any]:
        """创建矩形"""
        doc = ps.active_document
        x = params.get('x', 100)
        y = params.get('y', 100)
        width = params.get('width', 100)
        height = params.get('height', 100)
        color_rgb = params.get('color', {'red': 255, 'green': 100, 'blue': 100})

        # 设置颜色
        color = ps.SolidColor()
        color.rgb.red = color_rgb['red']
        color.rgb.green = color_rgb['green']
        color.rgb.blue = color_rgb['blue']
        ps.app.foregroundColor = color

        # 创建矩形选择
        x1, y1 = x, y
        x2, y2 = x + width, y + height
        doc.selection.select([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])

        # 填充
        doc.selection.fill(ps.app.foregroundColor)
        doc.selection.deselect()

        return {
            'success': True,
            'message': f'矩形创建成功 (位置: ({x}, {y}), 大小: {width}x{height})'
        }


class ConversationSession:
    """对话会话管理"""

    def __init__(self):
        self.llm = GemmaLLMClient()
        self.api = PhotoshopAPI()
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

        # 检查是否完整
        if self.context['pending_action'] and self.context['collected_params']:
            action_name = self.context['pending_action']
            params = self.context['collected_params']

            print(f"[执行] 正在执行 {action_name}...")

            # 执行API调用
            api_result = self.api.execute(action_name, params)

            if api_result['success']:
                # 清空上下文
                self.context['pending_action'] = None
                self.context['collected_params'] = {}
                return f"[成功] {api_result['message']}"
            else:
                return f"[失败] {api_result['message']}"

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

    def show_status(self):
        """显示当前状态"""
        print("\n=== 对话状态 ===")
        print(f"待处理动作: {self.context['pending_action']}")
        print(f"已收集参数: {self.context['collected_params']}")
        print("================\n")


def run_test_case():
    """运行测试用例"""
    print("=" * 70)
    print(" Photoshop语音控制 - 实时多轮对话测试")
    print("=" * 70)
    print("\n支持的指令:")
    print("  - '我要锐化图像' / '智能锐化' / 'sharpen'")
    print("  - '新建文档' / '创建文档'")
    print("  - '旋转图层' / 'rotate layer'")
    print("  - '创建矩形' / '画矩形'")
    print("\n输入示例:")
    print("  '我要锐化图像' -> 系统询问参数 -> '强度150，半径5' -> 执行")
    print("\n输入 'quit' 退出")
    print("=" * 70)

    session = ConversationSession()

    # 测试用例演示
    print("\n\n[自动演示 - 场景1: 智能锐化]")
    print("-" * 70)
    demo_conversation = [
        "我要锐化图像",
        "强度150，半径5"
    ]

    for msg in demo_conversation:
        response = session.process_message(msg)
        print(response)
        time.sleep(1)

    session.show_status()

    print("\n[自动演示 - 场景2: 创建矩形]")
    print("-" * 70)
    demo_conversation = [
        "创建一个红色矩形",
        "位置(200, 150)，大小300x200"
    ]

    for msg in demo_conversation:
        response = session.process_message(msg)
        print(response)
        time.sleep(1)

    session.show_status()

    # 交互模式
    print("\n\n[交互模式] 请输入您的指令:")
    print("-" * 70)

    while True:
        try:
            user_input = input("\n> ").strip()
            if user_input.lower() in ['quit', 'exit', 'q', '退出']:
                print("\n[退出] 感谢使用!")
                break

            if not user_input:
                continue

            response = session.process_message(user_input)
            print(response)

        except KeyboardInterrupt:
            print("\n\n[退出] 感谢使用!")
            break
        except Exception as e:
            print(f"\n[错误] {str(e)}")

    print("\n" + "=" * 70)
    print("测试完成!")
    print("=" * 70)


if __name__ == "__main__":
    run_test_case()
