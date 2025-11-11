# -*- coding: utf-8 -*-
"""
改进的Gemma Prompt测试
"""

import requests
import json


def test_improved_prompt():
    """测试改进的Prompt"""
    print("=" * 60)
    print("Gemma 改进Prompt测试")
    print("=" * 60)

    url = "http://localhost:11434/v1/chat/completions"

    # 改进的Prompt - 要求纯JSON
    system_prompt = """你是一个Photoshop语音助手。

规则：
1. 理解用户需求
2. 返回纯JSON格式，不要任何额外文本
3. 格式：{"action": "动作名", "params": {}, "complete": true/false}

可用动作：
- smart_sharpen: 智能锐化
- new_document: 新建文档
- rotate_layer: 旋转图层
- create_rectangle: 创建矩形"""

    test_cases = [
        "我要锐化一下",
        "创建一个200x150的矩形",
        "新建一个800x600的文档",
        "旋转图层45度"
    ]

    for text in test_cases:
        print(f"\n[测试] {text}")

        payload = {
            "model": "gemma3n:latest",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            "stream": False,
            "options": {
                "temperature": 0.3  # 降低随机性
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=90)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']

                print(f"响应: {content}")

                # 清理响应（移除可能的markdown标记）
                content = content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                content = content.strip()

                # 尝试解析
                try:
                    parsed = json.loads(content)
                    print(f"  [OK] JSON解析成功")
                    print(f"      动作: {parsed.get('action')}")
                    print(f"      参数: {parsed.get('params')}")
                    print(f"      完整: {parsed.get('complete')}")
                except json.JSONDecodeError as e:
                    print(f"  [WARN] JSON解析失败: {str(e)[:50]}")
                    print(f"      原始内容: {content[:100]}")
            else:
                print(f"[FAIL] 请求失败: {response.status_code}")
        except Exception as e:
            print(f"[FAIL] 异常: {e}")


def test_json_only_mode():
    """测试严格JSON模式"""
    print("\n" + "=" * 60)
    print("Gemma 严格JSON模式")
    print("=" * 60)

    url = "http://localhost:11434/v1/chat/completions"

    # 严格的JSON Prompt
    strict_prompt = """只返回JSON，不要任何其他文本。

{"action": "值", "params": {}, "complete": true/false}

理解："""

    test_text = "锐化图像"

    payload = {
        "model": "gemma3n:latest",
        "messages": [
            {"role": "system", "content": strict_prompt},
            {"role": "user", "content": test_text}
        ],
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=90)
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()

            print(f"输入: {test_text}")
            print(f"输出: {content}")

            try:
                parsed = json.loads(content)
                print(f"[OK] 严格JSON模式成功！")
                print(f"解析结果: {parsed}")
            except:
                print(f"[WARN] 严格模式也失败")

    except Exception as e:
        print(f"[FAIL] {e}")


def benchmark_performance():
    """性能基准测试"""
    print("\n" + "=" * 60)
    print("Gemma 性能基准")
    print("=" * 60)

    url = "http://localhost:11434/v1/chat/completions"

    # 测试5次取平均
    times = []
    for i in range(5):
        payload = {
            "model": "gemma3n:latest",
            "messages": [
                {"role": "user", "content": "简单回答：ok"}
            ],
            "stream": False
        }

        import time
        start = time.time()
        try:
            response = requests.post(url, json=payload, timeout=120)
            elapsed = time.time() - start

            if response.status_code == 200:
                times.append(elapsed)
                print(f"第{i+1}次: {elapsed:.2f}秒")
            else:
                print(f"第{i+1}次: 失败")
        except:
            print(f"第{i+1}次: 超时/错误")

    if times:
        avg = sum(times) / len(times)
        print(f"\n平均响应时间: {avg:.2f}秒")

        if avg < 5:
            print("[OK] 性能优秀 (<5秒)")
        elif avg < 10:
            print("[OK] 性能良好 (5-10秒)")
        else:
            print("[WARN] 性能一般 (>10秒)")


def main():
    """主函数"""
    # 1. 测试改进的Prompt
    test_improved_prompt()

    # 2. 测试严格JSON模式
    test_json_only_mode()

    # 3. 性能基准
    benchmark_performance()

    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print("\nGemma3n 评估:")
    print("  优点: 本地免费，理解能力强")
    print("  缺点: 响应速度较慢，需要改进Prompt")
    print("\n建议:")
    print("  1. 作为备选LLM（非主要）")
    print("  2. 优化Prompt以获得更好JSON格式")
    print("  3. 考虑更快模型如 Qwen2-7B")


if __name__ == "__main__":
    main()
