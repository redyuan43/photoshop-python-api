# -*- coding: utf-8 -*-
"""
自然语言测试脚本 - 扩展版
支持所有106个功能
基于YAML配置和LLM的自然语言理解
"""

import sys
import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import OpenAI
from photoshop_api_extended import PhotoshopAPIExtended


class ExtendedNaturalLanguageProcessor:
    """扩展自然语言处理器 - 支持所有106个功能"""

    def __init__(self, qwen_api_key: str):
        self.api_key = qwen_api_key
        self.client = OpenAI(
            api_key=qwen_api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.api = PhotoshopAPIExtended()
        self.all_actions = self._load_all_actions()
        self.context = {
            'pending_action': None,
            'collected_params': {}
        }

    def _load_all_actions(self) -> Dict[str, Dict]:
        """加载所有动作定义"""
        actions = {}
        actions_dir = Path(__file__).parent / "actions" / "core"

        # 加载8个YAML文件
        yaml_files = [
            "01_documents.yaml",
            "02_layers.yaml",
            "03_selections.yaml",
            "04_transforms.yaml",
            "05_adjustments.yaml",
            "06_filters.yaml",
            "07_shapes.yaml",
            "08_text.yaml"
        ]

        for file_name in yaml_files:
            file_path = actions_dir / file_name
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    for action in data:
                        actions[action['name']] = action

        return actions

    def _build_system_prompt(self) -> str:
        """构建LLM系统提示，包含所有106个功能"""
        categories = {
            'document': '文档操作',
            'layer': '图层操作',
            'selection': '选择操作',
            'transform': '变换操作',
            'adjustment': '图像调整',
            'filter': '滤镜效果',
            'shape': '形状绘制',
            'text': '文本操作'
        }

        # 按类别组织功能
        actions_by_category = {}
        for name, action in self.all_actions.items():
            cat = action['category']
            if cat not in actions_by_category:
                actions_by_category[cat] = []
            actions_by_category[cat].append(action)

        prompt = f"""你是一个专业的Photoshop语音助手，支持{len(self.all_actions)}个功能。

用户会用各种自然语言表达他们的需求，你需要理解并转换为正确的Photoshop操作。

可用功能（按类别组织）：

"""

        for cat, cat_name in categories.items():
            if cat in actions_by_category:
                prompt += f"\n【{cat_name}】\n"
                for action in actions_by_category[cat]:
                    aliases = action.get('aliases', [])
                    prompt += f"{len(prompt)}. {action['name']} - {action['description']}\n"
                    if aliases:
                        prompt += f"   别名: {', '.join(aliases[:3])}\n"
                    prompt += f"   类别: {cat}\n"
                    prompt += f"   参数: {', '.join(action.get('params', {}).keys())}\n"

        prompt += """
重要规则：
1. 参数解析规则：
   - 文本内容：提取引号内的文字或冒号后的内容
   - 颜色：理解各种颜色表达，转换为RGB字典格式
   - 数值：支持范围检查，默认值已在定义中
   - 坐标：x, y为左上角坐标（像素）
   - 角度：使用"angle"参数名（不是degrees）

2. 颜色处理：
   - 标准颜色：red, green, blue, yellow, white, black等
   - 自然语言颜色：天蓝色、深红色、东北银、亮黄等
   - RGB字典格式：{"red": 255, "green": 0, "blue": 0}

3. 文本内容提取：
   - 输入"创建文字：你好" → text: "你好"
   - 输入"添加文字：2025年春季之行" → text: "2025年春季之行"
   - 引号内容自动提取

4. 缺失参数处理：
   - 如果缺少必需参数，返回complete=false并询问
   - 如果所有参数都存在，complete=true并执行

5. 对话状态：
   - 如果complete=false，记录pending_action和collected_params
   - 下次输入会基于已收集的参数继续执行

6. 找不到匹配功能时：
   - intent_type设为"unsupported"
   - response说明当前支持的功能范围

颜色RGB参考：
- 红色: (255,0,0)  绿色: (0,255,0)  蓝色: (0,0,255)
- 黄色: (255,255,0)  白色: (255,255,255)  黑色: (0,0,0)
- 橙色: (255,165,0)  紫色: (128,0,128)  粉色: (255,192,203)
- 天蓝色: (135,206,235)  金色: (255,215,0)  银色: (192,192,192)
- 灰色: (128,128,128)  青色: (0,255,255)  海军蓝: (0,0,128)

返回JSON格式：
{"intent_type": "功能名", "action": "功能名", "params": {参数}, "complete": true/false, "response": "回复"}

直接返回JSON，不要其他内容！"""

        return prompt

    def analyze_intent(self, user_text: str) -> Dict[str, Any]:
        """分析用户意图"""
        system_prompt = self._build_system_prompt()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]

        try:
            response = self.client.chat.completions.create(
                model="qwen-plus",
                messages=messages,
                temperature=0.3
            )

            content = response.choices[0].message.content.strip()
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

    def process_message(self, user_text: str) -> str:
        """处理用户消息"""
        print(f"\n{'=' * 70}")
        print(f"[用户输入] {user_text}")
        print('=' * 70)

        print("[分析] 正在调用通义千问模型...")
        result = self.analyze_intent(user_text)

        if not result['success']:
            return f"[错误] LLM分析失败: {result['error']}"

        data = result['data']
        print(f"\n[LLM解析结果]")
        print(f"  intent_type: {data.get('intent_type')}")
        print(f"  action: {data.get('action')}")
        print(f"  params: {json.dumps(data.get('params', {}), ensure_ascii=False, indent=4)}")
        print(f"  complete: {data.get('complete')}")
        print(f"  response: {data.get('response')}")

        # 更新上下文
        self._update_context(data)

        # 检查是否不支持
        if data.get('intent_type') == 'unsupported':
            self.context['pending_action'] = None
            self.context['collected_params'] = {}
            supported_actions = list(self.all_actions.keys())[:10]  # 只显示前10个
            return f"[助手] 该功能暂时无法实现。当前支持的106个功能包括：{', '.join(supported_actions)}等。\n您可以尝试：\n  - '创建文字：你好世界'\n  - '新建文档 1920x1080'\n  - '智能锐化'\n  - '画个红色矩形'"

        # 检查是否完整
        complete = data.get('complete', False)
        if complete or (self.context['pending_action'] and self.context['collected_params']):
            if complete:
                action_name = data.get('action')
                params = data.get('params', {})
            else:
                action_name = self.context['pending_action']
                params = self.context['collected_params']

            print(f"\n[执行] 正在执行 Photoshop API: {action_name}")
            print(f"  参数: {json.dumps(params, ensure_ascii=False, indent=4)}")

            api_result = self.api.execute(action_name, params)

            self.context['pending_action'] = None
            self.context['collected_params'] = {}

            if api_result['success']:
                return f"[成功] {api_result['message']}"
            else:
                return f"[失败] {api_result['message']}"

        response = data.get('response', '请继续...')
        return f"[助手] {response}"

    def _update_context(self, data: Dict[str, Any]):
        """更新对话上下文"""
        intent_type = data.get('intent_type')
        action = data.get('action')
        params = data.get('params', {})

        if intent_type in self.all_actions:
            self.context['pending_action'] = action
            self.context['collected_params'] = params

    def show_status(self):
        """显示当前状态"""
        print("\n" + "=" * 70)
        print(" [对话状态]")
        print(f" 待处理动作: {self.context['pending_action']}")
        print(f" 已收集参数: {self.context['collected_params']}")
        print("=" * 70)

    def interactive_mode(self):
        """开始交互模式"""
        print("=" * 70)
        print(" Photoshop语音控制 - 扩展版（支持106个功能）")
        print("=" * 70)
        print(f"\n当前支持 {len(self.all_actions)} 个功能，包括：")
        print("  - 文档操作: 新建、保存、打开")
        print("  - 图层操作: 复制、重命名、混合模式")
        print("  - 文本操作: 创建文字、设置字体、颜色")
        print("  - 形状绘制: 矩形、圆形、多边形")
        print("  - 滤镜效果: 锐化、模糊、浮雕")
        print("  - 图像调整: 亮度、色阶、曲线")
        print("\n示例:")
        print("  '创建文字：2025年春季之行'")
        print("  '新建文档 1920x1080'")
        print("  '智能锐化'")
        print("  '画个蓝色圆形'")
        print("  '设置文字颜色为红色'")
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

    processor = ExtendedNaturalLanguageProcessor(qwen_api_key)
    processor.interactive_mode()


if __name__ == "__main__":
    main()
