# -*- coding: utf-8 -*-
"""
测试 qwen3:4b 模型性能
比较与 gemma3n:latest 的差异
"""

import requests
import json
import time


def test_qwen3_4b_performance():
    """测试 qwen3:4b 性能"""
    print("=" * 60)
    print("测试 Qwen3-4B 模型性能")
    print("=" * 60)

    url = "http://localhost:11434/v1/chat/completions"

    # 测试3次取平均
    times = []
    for i in range(3):
        payload = {
            "model": "qwen3:4b",
            "messages": [
                {"role": "user", "content": "简单回答：ok"}
            ],
            "stream": False
        }

        start = time.time()
        try:
            response = requests.post(url, json=payload, timeout=120)
            elapsed = time.time() - start

            if response.status_code == 200:
                times.append(elapsed)
                print(f"第{i+1}次: {elapsed:.2f}秒")
            else:
                print(f"第{i+1}次: 失败 ({response.status_code})")
        except Exception as e:
            print(f"第{i+1}次: 异常 - {e}")

    if times:
        avg = sum(times) / len(times)
        print(f"\n平均响应时间: {avg:.2f}秒")

        # 与 gemma 对比
        print("\n性能对比:")
        print(f"  qwen3:4b:    {avg:.2f}秒")
        print(f"  gemma3n:     6.38秒 (之前测试)")
        print(f"  速度提升:    {(6.38 - avg) / 6.38 * 100:.1f}%")

        if avg < 3:
            print("[OK] 性能优秀 (<3秒)")
            print("  建议: 适合作为主要本地LLM")
        elif avg < 5:
            print("[OK] 性能良好 (3-5秒)")
            print("  建议: 可作为主要本地LLM")
        else:
            print("[WARN] 性能一般 (>5秒)")
            print("  建议: 仍可作为备选")


def test_qwen3_4b_json():
    """测试 qwen3:4b JSON输出能力"""
    print("\n" + "=" * 60)
    print("测试 Qwen3-4B JSON格式输出")
    print("=" * 60)

    url = "http://localhost:11434/v1/chat/completions"

    # 测试用例
    test_cases = [
        "我要锐化图像",
        "创建一个200x150的矩形",
        "新建一个800x600的文档"
    ]

    for text in test_cases:
        print(f"\n[测试] {text}")

        payload = {
            "model": "qwen3:4b",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个Photoshop语音助手。只返回JSON: {\"action\": \"值\", \"params\": {}, \"complete\": true/false}"
                },
                {"role": "user", "content": text}
            ],
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, timeout=90)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()

                # 过滤thinking标签内容（qwen模型特性）
                import re
                content = re.sub(r'<thinking>.*?</thinking>', '', content, flags=re.DOTALL).strip()

                print(f"响应: {content[:60]}...")

                # 尝试解析JSON
                try:
                    parsed = json.loads(content)
                    print("  [OK] JSON解析成功")
                except:
                    print("  [WARN] JSON解析失败")
            else:
                print(f"[FAIL] 请求失败: {response.status_code}")
        except Exception as e:
            print(f"[FAIL] 异常: {e}")


def test_qwen3_4b_photoshop_intent():
    """测试 qwen3:4b 对Photoshop意图的理解"""
    print("\n" + "=" * 60)
    print("测试 Qwen3-4B Photoshop意图理解")
    print("=" * 60)

    url = "http://localhost:11434/v1/chat/completions"

    system_prompt = """你是一个Photoshop语音助手。

规则：
1. 直接返回JSON，不要任何其他文本
2. 不要使用<thinking>标签
3. 格式：{"action": "动作名", "params": {}, "complete": true/false}

可用动作：
- smart_sharpen: 智能锐化
- new_document: 新建文档
- rotate_layer: 旋转图层
- create_rectangle: 创建矩形"""

    test_cases = [
        ("我要锐化一下", "smart_sharpen"),
        ("创建一个200x150的矩形", "create_rectangle"),
        ("新建一个800x600的文档", "new_document"),
        ("旋转图层45度", "rotate_layer")
    ]

    correct = 0
    for text, expected in test_cases:
        print(f"\n[测试] '{text}' -> {expected}")

        payload = {
            "model": "qwen3:4b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 512,  # 限制输出长度
                "stop": ["<thinking>", "\n\n"]  # 停止词
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=90)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']

                # 过滤thinking标签（qwen模型特性）
                import re
                content = re.sub(r'<thinking>.*?</thinking>', '', content, flags=re.DOTALL).strip()

                # 清理响应
                content = content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                content = content.strip()

                try:
                    parsed = json.loads(content)
                    action = parsed.get('action', '')
                    if action == expected:
                        print(f"  [OK] 识别正确: {action}")
                        correct += 1
                    else:
                        print(f"  [WARN] 识别错误: 期望{expected}, 实际{action}")
                except Exception as e:
                    print(f"  [FAIL] JSON解析失败: {str(e)[:50]}")
            else:
                print(f"[FAIL] 请求失败: {response.status_code}")
        except Exception as e:
            print(f"[FAIL] 异常: {e}")

    accuracy = correct / len(test_cases) * 100
    print(f"\n准确率: {correct}/{len(test_cases)} = {accuracy:.1f}%")


def main():
    """主函数"""
    # 1. 性能测试
    test_qwen3_4b_performance()

    # 2. JSON测试
    test_qwen3_4b_json()

    # 3. 意图理解测试
    test_qwen3_4b_photoshop_intent()

    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print("\nQwen3-4B 评估:")
    print("  优点: 模型更小，推理更快")
    print("  缺点: 可能准确性略低于大模型")
    print("\n建议:")
    print("  1. 如果性能优秀，替换 gemma3n 作为主要本地LLM")
    print("  2. 仍保持 gemma3n 作为备选")
    print("  3. 根据测试结果选择最适合的模型")


if __name__ == "__main__":
    main()
