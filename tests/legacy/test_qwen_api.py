# -*- coding: utf-8 -*-
"""
交互式测试脚本 - 通义千问API版本
使用通义千问云端API进行意图分析
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from typing import Dict, Any
from openai import OpenAI


class QwenLLMClient:
    """通义千问LLM客户端"""

    def __init__(self, api_key: str, model_name: str = "qwen-plus", base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def analyze_intent(self, user_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """分析用户意图"""
        context = context or {}

        pending_action = context.get('pending_action') or '无'
        collected_params = context.get('collected_params', {})

        system_prompt = f"""你是一个专业的Photoshop语音助手。

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

颜色处理：
- 理解用户颜色表达（如"天蓝色"、"深红色"、"东北银"）
- 必须转换为RGB字典格式：{{"red": 值, "green": 值, "blue": 值}}
- 例如：{{"color": {{"red": 135, "green": 206, "blue": 235}}}}

- 智能猜测规则：
  1. 标准颜色：直接返回RGB字典
  2. 模糊表达：给出最佳猜测，设置complete=false，询问用户确认
  3. 常见颜色联想：
     "东北银" -> 银色: (192,192,192)
     "亮红" -> 红色: (255,0,0)
     "深蓝" -> 蓝色: (0,0,255)
     "淡绿" -> 绿色: (0,255,0)
     "亮黄" -> 黄色: (255,255,0)
     "暗紫" -> 紫色: (128,0,128)

- 询问确认格式：
  {{"intent_type": "create_rectangle", "action": "create_rectangle", "params": {{"color": {{"red": 192, "green": 192, "blue": 192}}}}, "complete": false, "response": "我理解您想要银色，可以吗？如果不对请告诉我具体颜色"}}

- 常用颜色RGB参考：
  红色: (255,0,0)  绿色: (0,255,0)  蓝色: (0,0,255)
  黄色: (255,255,0)  白色: (255,255,255)  黑色: (0,0,0)
  橙色: (255,165,0)  紫色: (128,0,128)  粉色: (255,192,203)
  天蓝色: (135,206,235)  金色: (255,215,0)  银色: (192,192,192)
  灰色: (128,128,128)  青色: (0,255,255)  海军蓝: (0,0,128)

- 只有完全无法理解的情况下才返回unsupported

其他要求：
- 参数名必须使用"angle"（不是"degrees"）
- 如果提供了完整参数，complete设为true
- 如果还需要更多信息，complete设为false
- intent_type为动作名（如"smart_sharpen"）时，直接执行

对话状态：
- 待处理动作: {pending_action}
- 已收集参数: {collected_params}

直接返回JSON，不要其他内容！"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.3
            )

            content = response.choices[0].message.content.strip()

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
        except Exception as e:
            return {
                'success': False,
                'error': f'异常: {str(e)}',
                'raw_response': None
            }


# 导入PhotoshopAPI（从test_interactive_utf8.py）
import sys
sys.path.insert(0, os.path.dirname(__file__))
from test_interactive_utf8 import PhotoshopAPI


class InteractiveSession:
    """交互式对话会话"""

    def __init__(self, qwen_api_key: str):
        self.llm = QwenLLMClient(api_key=qwen_api_key)
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
        print("[分析] 正在调用通义千问模型...")
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
        if intent_type in ['new_action', 'create_rectangle', 'smart_sharpen', 'rotate_layer', 'new_document']:
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
        print(" Photoshop语音控制 - 通义千问API版")
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
        print("  '旋转图片45度'")
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
    # 从配置文件或环境变量获取API密钥
    import sys
    import os

    # 尝试从项目根目录导入配置
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from config import api_config
        qwen_api_key = api_config.QWEN_API_KEY
    except ImportError:
        # 如果无法导入配置文件，则使用环境变量
        qwen_api_key = os.environ.get("QWEN_API_KEY", "")

    if not qwen_api_key:
        print("[ERROR] 请配置 QWEN_API_KEY")
        print("方法1: 复制 config.example.py 为 config.py 并填入API密钥")
        print("方法2: 设置环境变量: export QWEN_API_KEY='your-api-key'")
        return

    session = InteractiveSession(qwen_api_key)
    session.start()


if __name__ == "__main__":
    main()
