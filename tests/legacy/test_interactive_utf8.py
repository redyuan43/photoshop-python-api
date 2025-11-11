# -*- coding: utf-8 -*-
"""
交互式测试脚本 - UTF-8编码版本
解决Windows CMD乱码问题
使用方式：
1. 双击 run_test.bat
2. 或在PowerShell中: $env:PYTHONIOENCODING="utf-8"
"""

import sys
import os

# 添加项目根目录到路径 - 使用与voice_to_api_REAL.py相同的方式
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json
import time
from typing import Dict, Any


class GemmaLLMClient:
    """Gemma3n LLM客户端"""

    def __init__(self, model_name: str = "gemma3n:latest", base_url: str = "http://localhost:11434/v1"):
        self.model_name = model_name
        self.base_url = base_url

    def analyze_intent(self, user_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """分析用户意图"""
        context = context or {}

        pending_action = context.get('pending_action') or '无'
        collected_params = context.get('collected_params', {})

        system_prompt = f"""你是一个Photoshop助手。用户说"锐化"或"锐化图像"就是smart_sharpen动作。

规则：
- 返回JSON：{{"intent_type": "类型", "action": "动作名", "params": {{}}, "complete": true/false, "response": "回复"}}

关键词匹配：
- "锐化" "锐化图像" "清晰化" -> smart_sharpen
- "新建文档" "创建文档" -> new_document
- "旋转图层" "rotate" -> rotate_layer
- "矩形" "创建矩形" -> create_rectangle

其他 -> unsupported

状态: 待处理{pending_action}

直接返回JSON："""

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


class PhotoshopAPI:
    """Photoshop API执行器 - 使用voice_to_api_REAL.py中的真实API"""

    def __init__(self):
        self.has_photoshop = False

        try:
            # 测试导入photoshop模块
            import photoshop
            self.has_photoshop = True
            print("[INFO] 检测到Photoshop模块，将执行真实API调用")
            print(f"[DEBUG] 模块位置: {photoshop.__file__}")
        except (ImportError, ModuleNotFoundError) as e:
            print("[WARN] 未检测到Photoshop模块，将模拟执行")
            print(f"[DEBUG] 导入错误: {e}")
            print()  # 空行分隔

    def execute(self, action_name: str, params: dict) -> Dict[str, Any]:
        """执行Photoshop API调用 - 直接调用voice_to_api_REAL.py中的真实API"""
        if not self.has_photoshop:
            # 模拟执行
            return self._simulate_execution(action_name, params)

        try:
            # 直接调用voice_to_api_REAL.py中的真实API
            from voice_to_api_REAL import execute_api

            result = execute_api(action_name, params)

            if result.get('success'):
                return {
                    'success': True,
                    'message': result['message']
                }
            else:
                return {
                    'success': False,
                    'message': result.get('message', '执行失败')
                }

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'message': f'API调用失败: {str(e)}',
                'error': str(e)
            }

    def _simulate_execution(self, action_name: str, params: dict) -> Dict[str, Any]:
        """模拟API执行"""
        if action_name == 'smart_sharpen':
            amount = params.get('amount', 100)
            radius = params.get('radius', 3.0)
            noise = params.get('noiseReduction', 20)
            return {
                'success': True,
                'message': f'[模拟] Smart Sharpen (amount: {amount}, radius: {radius}, noise: {noise}%)'
            }
        elif action_name == 'new_document':
            width = params.get('width', 800)
            height = params.get('height', 600)
            return {
                'success': True,
                'message': f'[模拟] 文档创建 ({width}x{height})'
            }
        elif action_name == 'rotate_layer':
            angle = params.get('angle', 45)
            return {
                'success': True,
                'message': f'[模拟] 图层旋转 ({angle}度)'
            }
        elif action_name == 'create_rectangle':
            x = params.get('x', 100)
            y = params.get('y', 100)
            width = params.get('width', 100)
            height = params.get('height', 100)
            return {
                'success': True,
                'message': f'[模拟] 矩形创建 (位置: ({x}, {y}), 大小: {width}x{height})'
            }
        else:
            return {
                'success': False,
                'message': f'未知动作: {action_name}'
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


class InteractiveSession:
    """交互式对话会话"""

    def __init__(self):
        self.llm = GemmaLLMClient()
        self.api = PhotoshopAPI()
        self.context = {
            'pending_action': None,
            'collected_params': {}
        }

    def process_message(self, user_text: str) -> str:
        """处理用户消息"""
        print(f"\n{'=' * 70}")
        print(f"[用户输入] {user_text}")
        print('=' * 70)

        # 调用LLM分析
        print("[分析] 正在调用Gemma3n模型...")
        result = self.llm.analyze_intent(user_text, self.context)

        if not result['success']:
            return f"[错误] LLM分析失败: {result['error']}"

        data = result['data']
        print(f"\n[LLM响应] {json.dumps(data, ensure_ascii=False, indent=2)}")

        # 更新上下文
        self._update_context(data)

        # 检查是否不支持
        if data.get('intent_type') == 'unsupported':
            self.context['pending_action'] = None
            self.context['collected_params'] = {}
            return "[助手] 对不起，该功能暂时无法实现。目前只支持：智能锐化、新建文档、旋转图层、创建矩形。"

        # 检查是否完整（优先检查complete标志位）
        complete = data.get('complete', False)
        if complete or (self.context['pending_action'] and self.context['collected_params']):
            # 如果complete=true，使用当前data中的action和params
            if complete:
                action_name = data.get('action')
                params = data.get('params', {})
            else:
                action_name = self.context['pending_action']
                params = self.context['collected_params']

            print(f"\n[执行] 正在执行 {action_name}...")

            # 执行API调用
            api_result = self.api.execute(action_name, params)

            # 清空上下文
            self.context['pending_action'] = None
            self.context['collected_params'] = {}

            if api_result['success']:
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

        # 处理intent_type为动作名的情况（如 'create_rectangle', 'smart_sharpen' 等）
        if intent_type in ['new_action', 'create_rectangle', 'smart_sharpen', 'rotate_layer']:
            self.context['pending_action'] = action
            self.context['collected_params'] = params
        elif intent_type in ['provide_params', 'modiify_params']:
            self.context['collected_params'].update(params)

    def show_status(self):
        """显示当前状态"""
        print("\n" + "=" * 70)
        print(" [对话状态]")
        print(f" 待处理动作: {self.context['pending_action']}")
        print(f" 已收集参数: {self.context['collected_params']}")
        print("=" * 70)

    def start(self):
        """开始交互"""
        print("=" * 70)
        print(" Photoshop语音控制 - 交互式人工测试")
        print("=" * 70)
        print("\n支持的功能:")
        print("  1. smart_sharpen - 智能锐化图像")
        print("  2. new_document - 新建文档")
        print("  3. rotate_layer - 旋转图层")
        print("  4. create_rectangle - 创建矩形")
        print("\n其他功能将自动回复无法实现")
        print("\n输入示例:")
        print("  '我要锐化图像'")
        print("  '强度150，半径5'")
        print("  '创建一个红色矩形'")
        print("  '位置(200, 150) 大小300x200'")
        print("\n输入 'quit' 退出")
        print("输入 'status' 查看当前状态")
        print("=" * 70)

        while True:
            try:
                user_input = input("\n> ").strip()

                if user_input.lower() in ['quit', 'exit', 'q', '退出']:
                    print("\n[退出] 感谢使用!")
                    break

                if user_input.lower() in ['status', '状态']:
                    self.show_status()
                    continue

                if not user_input:
                    continue

                response = self.process_message(user_input)
                print(f"\n{response}")

            except KeyboardInterrupt:
                print("\n\n[退出] 感谢使用!")
                break
            except Exception as e:
                print(f"\n[错误] {str(e)}")

        print("\n" + "=" * 70)
        print("测试结束!")
        print("=" * 70)


def main():
    """主函数"""
    session = InteractiveSession()
    session.start()


if __name__ == "__main__":
    main()
