# -*- coding: utf-8 -*-
"""
对话式Photoshop语音控制器

架构：
1. LLM分析对话和意图
2. 管理对话状态
3. 收集必要信息
4. 执行API调用
"""

import json
import time
from typing import Dict, List, Optional, Any
from action_registry import ActionRegistry


class ConversationState:
    """对话状态管理"""

    def __init__(self):
        self.history = []  # 消息历史
        self.pending_action = None  # 待处理动作
        self.collected_params = {}  # 已收集参数
        self.session_start = time.time()

    def add_message(self, role: str, content: str):
        """添加消息到历史"""
        self.history.append({
            'role': role,
            'content': content,
            'timestamp': time.time()
        })

    def set_pending_action(self, action_name: str):
        """设置待处理动作"""
        self.pending_action = action_name
        self.collected_params = {}

    def update_params(self, params: dict):
        """更新参数"""
        self.collected_params.update(params)

    def get_state_summary(self) -> dict:
        """获取状态摘要"""
        return {
            'pending_action': self.pending_action,
            'collected_params': self.collected_params,
            'message_count': len(self.history),
            'session_duration': time.time() - self.session_start
        }

    def clear(self):
        """清空状态"""
        self.pending_action = None
        self.collected_params = {}


class LLMInterface:
    """统一LLM接口 - 兼容OpenAI API"""

    def __init__(self, config: dict = None):
        self.config = config or {
            'model': 'gpt-4',
            'api_key': None,
            'base_url': 'https://api.openai.com/v1'
        }
        self.client = None
        self._init_client()

    def _init_client(self):
        """初始化客户端"""
        # 实际实现中，这里会创建OpenAI客户端
        # import openai
        # self.client = openai.OpenAI(
        #     api_key=self.config['api_key'],
        #     base_url=self.config.get('base_url')
        # )
        pass

    def analyze_intent(self, user_text: str, state: ConversationState) -> dict:
        """分析用户意图和对话状态"""
        # 构建system prompt
        system_prompt = self._build_system_prompt(state)
        user_prompt = f"用户说：{user_text}"

        # 构建消息
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]

        # 调用LLM
        # response = self.client.chat.completions.create(
        #     model=self.config['model'],
        #     messages=messages,
        #     temperature=0.3,
        #     response_format={'type': 'json_object'}
        # )

        # 模拟响应（实际调用时替换为真实API）
        return self._mock_llm_response(user_text, state)

    def _build_system_prompt(self, state: ConversationState) -> str:
        """构建系统提示词"""
        return f"""
你是一个专业的Photoshop语音助手。你需要理解用户的意图，并帮助他们完成Photoshop操作。

对话状态：
- 待处理动作: {state.pending_action or '无'}
- 已收集参数: {state.collected_params}
- 历史消息数: {len(state.history)}

用户可能会：
1. 提供新指令
2. 提供缺失的参数
3. 修改之前的参数
4. 询问如何操作
5. 撤销操作

请分析用户输入并返回JSON格式：
{{
    "intent_type": "new_action|provide_params|modify_params|ask_question|undo_action",
    "action": "动作名称（如果适用）",
    "complete": true/false,  // 指令是否完整可执行
    "question": "需要询问的问题（如果适用）",
    "clarification": "需要澄清的内容（如果适用）",
    "response": "直接回复用户的内容",
    "action_params": {{动作参数（如果提供）}}
}}

可用动作：
{self._get_available_actions()}
"""

    def _get_available_actions(self) -> str:
        """获取可用动作列表"""
        registry = ActionRegistry()
        actions = []
        for name in registry.list_actions():
            info = registry.get_action_info(name)
            actions.append(f"- {name}: {info['description']}")
        return '\n'.join(actions)

    def _mock_llm_response(self, user_text: str, state: ConversationState) -> dict:
        """模拟LLM响应（实际使用时会调用真实API）"""
        # 简化实现：根据关键词判断
        user_lower = user_text.lower()

        # 检查是否是常见动作
        if '锐化' in user_text or 'sharpen' in user_lower:
            if state.pending_action and state.pending_action != 'smart_sharpen':
                # 用户改变主意了
                return {
                    'intent_type': 'new_action',
                    'action': 'smart_sharpen',
                    'complete': False,
                    'question': '请指定锐化强度（0-500）和半径',
                    'clarification': None,
                    'response': '好的，我们来锐化图像。请告诉我强度和半径。',
                    'action_params': {}
                }
            elif not state.pending_action:
                # 新动作，需要参数
                return {
                    'intent_type': 'new_action',
                    'action': 'smart_sharpen',
                    'complete': False,
                    'question': '请指定锐化强度（0-500）和半径',
                    'clarification': None,
                    'response': '好的，我们来锐化图像。请告诉我强度和半径。',
                    'action_params': {}
                }
            else:
                # 已经在收集参数，尝试提取
                return {
                    'intent_type': 'provide_params',
                    'action': 'smart_sharpen',
                    'complete': False,
                    'question': None,
                    'clarification': None,
                    'response': '请提供锐化参数',
                    'action_params': self._extract_params(user_text)
                }

        elif '强度' in user_text and state.pending_action == 'smart_sharpen':
            # 用户提供了参数
            params = self._extract_params(user_text)
            return {
                'intent_type': 'provide_params',
                'action': 'smart_sharpen',
                'complete': len(params) > 0,
                'question': None,
                'clarification': None,
                'response': '收到参数' if params else '请提供有效参数',
                'action_params': params
            }

        return {
            'intent_type': 'ask_question',
            'action': None,
            'complete': False,
            'question': '请用中文说明您想做什么操作',
            'clarification': None,
            'response': '我不太理解，请换一种说法或直接告诉我您想做什么',
            'action_params': {}
        }

    def _extract_params(self, user_text: str) -> dict:
        """从用户文本中提取参数（简化版）"""
        params = {}
        import re

        # 提取数字参数
        numbers = re.findall(r'(\d+(?:\.\d+)?)', user_text)
        if numbers:
            if len(numbers) >= 1:
                params['amount'] = float(numbers[0])
            if len(numbers) >= 2:
                params['radius'] = float(numbers[1])

        return params


class ConversationalController:
    """对话式Photoshop控制器"""

    def __init__(self, llm_config: dict = None):
        self.state = ConversationState()
        self.llm = LLMInterface(llm_config)
        self.registry = ActionRegistry()
        self.api_executor = APIExecutor()

    def process_message(self, user_text: str) -> str:
        """处理用户消息"""
        # 1. 添加到历史
        self.state.add_message('user', user_text)

        # 2. LLM分析意图
        analysis = self.llm.analyze_intent(user_text, self.state)

        # 3. 根据意图类型处理
        if analysis['intent_type'] == 'new_action':
            self.state.set_pending_action(analysis['action'])

        elif analysis['intent_type'] == 'provide_params':
            if analysis['action_params']:
                self.state.update_params(analysis['action_params'])

        # 4. 检查是否完整
        if self.state.pending_action and self.state.collected_params:
            action_info = self.registry.get_action_info(self.state.pending_action)
            required_params = [p for p in action_info.get('params', {}).keys()
                             if action_info['params'][p].get('required', False)]

            if all(p in self.state.collected_params for p in required_params):
                # 5. 执行动作
                result = self._execute_current_action()
                self.state.add_message('assistant', f"执行完成: {result}")
                self.state.clear()
                return f"✅ {result}"

        # 6. 返回LLM建议的回复
        self.state.add_message('assistant', analysis['response'])
        return analysis['response']

    def _execute_current_action(self) -> str:
        """执行当前待处理动作"""
        action_name = self.state.pending_action
        params = self.state.collected_params

        # 调用API执行器
        result = self.api_executor.execute(action_name, params)
        return result

    def get_state_info(self) -> dict:
        """获取当前状态信息"""
        return {
            'pending_action': self.state.pending_action,
            'collected_params': self.state.collected_params,
            'history_count': len(self.state.history),
            'available_models': self.llm.list_models() if hasattr(self.llm, 'list_models') else []
        }


class APIExecutor:
    """API执行器"""

    def __init__(self):
        # 加载API实现
        self.implementations = {
            'smart_sharpen': self._api_smart_sharpen,
            'new_document': self._api_new_document,
            'rotate_layer': self._api_rotate_layer,
            'create_rectangle': self._api_create_rectangle,
        }

    def execute(self, action_name: str, params: dict) -> str:
        """执行动作"""
        if action_name not in self.implementations:
            return f"未实现的动作: {action_name}"

        try:
            result = self.implementations[action_name](params)
            return result
        except Exception as e:
            return f"执行失败: {str(e)}"

    def _api_smart_sharpen(self, params: dict) -> str:
        """智能锐化 - 真实API实现"""
        try:
            from photoshop import Session

            with Session() as ps:
                doc = ps.active_document
                layer = doc.activeLayer

                # 获取参数
                amount = params.get('amount', 100.0)
                radius = params.get('radius', 3.0)
                noise = params.get('noiseReduction', 20)

                # 使用Action Manager调用SmartSharpen
                idsmart_sharpen_id = ps.app.stringIDToTypeID(ps.EventID.SmartSharpen)
                desc = ps.ActionDescriptor()

                # 设置PresetKind为Custom
                idpresetKind = ps.app.stringIDToTypeID(ps.EventID.PresetKind)
                idpresetKindType = ps.app.stringIDToTypeID(ps.EventID.PresetKindType)
                idpresetKindCustom = ps.app.stringIDToTypeID(ps.EventID.PresetKindCustom)
                desc.putEnumerated(idpresetKind, idpresetKindType, idpresetKindCustom)

                # 设置Amount (percentage)
                idAmnt = ps.app.charIDToTypeID("Amnt")
                idPrc = ps.app.charIDToTypeID("Rds ")
                desc.putUnitDouble(idAmnt, idPrc, amount)

                # 设置Radius (pixels)
                idRds = ps.app.charIDToTypeID("Rds ")
                idPxl = ps.app.charIDToTypeID("#Pxl")
                desc.putUnitDouble(idRds, idPxl, radius)

                # 设置noiseReduction (percentage)
                idnoiseReduction = ps.app.stringIDToTypeID("noiseReduction")
                idPrcNoise = ps.app.charIDToTypeID("#Prc")
                desc.putUnitDouble(idnoiseReduction, idPrcNoise, noise)

                # 设置blur type为Gaussian
                idblur = ps.app.charIDToTypeID("blur")
                idblurType = ps.app.stringIDToTypeID("blurType")
                idGsnB = ps.app.charIDToTypeID("GsnB")
                desc.putEnumerated(idblur, idblurType, idGsnB)

                # 执行Action
                ps.app.ExecuteAction(idsmart_sharpen_id, desc)

                return f"Smart Sharpen applied (amount: {amount}, radius: {radius}, noise: {noise}%)"
        except Exception as e:
            return f"Smart Sharpen failed: {str(e)}"

    def _api_new_document(self, params: dict) -> str:
        """新建文档 - 真实API实现"""
        try:
            from photoshop import Session

            with Session() as ps:
                width = params.get('width', 800)
                height = params.get('height', 600)
                doc = ps.app.documents.add(width=width, height=height)
                return f"Document created {width}x{height}"
        except Exception as e:
            return f"Create document failed: {str(e)}"

    def _api_rotate_layer(self, params: dict) -> str:
        """旋转图层 - 真实API实现"""
        try:
            from photoshop import Session

            with Session() as ps:
                doc = ps.active_document
                angle = params.get('angle', 45)

                # 获取当前图层
                layer = doc.activeLayer

                # 检查是否是背景图层（背景图层不能直接旋转）
                if layer.isBackgroundLayer:
                    # 如果是背景图层，先复制一份
                    layer = layer.duplicate()
                    layer.isBackgroundLayer = False
                    doc.activeLayer = layer

                # 旋转图层
                layer.rotate(angle, ps.AnchorPosition.MiddleCenter)

                return f"Layer rotated {angle} degrees"
        except Exception as e:
            return f"Rotate layer failed: {str(e)}"

    def _api_create_rectangle(self, params: dict) -> str:
        """创建矩形 - 真实API实现"""
        try:
            from photoshop import Session

            with Session() as ps:
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

                # 创建矩形选择区域
                x1, y1 = x, y
                x2, y2 = x + width, y + height
                doc.selection.select([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])

                # 填充颜色
                doc.selection.fill(ps.app.foregroundColor)

                # 取消选择
                doc.selection.deselect()

                return f"Rectangle created at ({x}, {y}) size {width}x{height}"
        except Exception as e:
            return f"Create rectangle failed: {str(e)}"


def demo():
    """演示对话流程"""
    controller = ConversationalController()

    # 模拟对话
    conversation = [
        "我要锐化一下",
        "强度100，半径3",
        "好的",
        "我想新建一个文档",
        "500x600",
    ]

    print("=" * 60)
    print("Photoshop 对话式语音助手 - 演示")
    print("=" * 60)

    for user_input in conversation:
        print(f"\n用户: {user_input}")
        response = controller.process_message(user_input)
        print(f"助手: {response}")

        state = controller.get_state_info()
        if state['pending_action']:
            print(f"   [状态] 待执行: {state['pending_action']}, 参数: {state['collected_params']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()
