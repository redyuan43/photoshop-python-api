# -*- coding: utf-8 -*-
"""
简化的Gemma 3n测试脚本
"""

import requests
import json
import time


def test_gemma_basic():
    """基础测试"""
    print("=" * 60)
    print("测试 Gemma3n 基础功能")
    print("=" * 60)

    url = "http://localhost:11434/v1/chat/completions"

    payload = {
        "model": "gemma3n:latest",
        "messages": [
            {"role": "user", "content": "你好"}
        ],
        "stream": False
    }

    try:
        start = time.time()
        response = requests.post(url, json=payload, timeout=60)
        elapsed = time.time() - start

        if response.status_code == 200:
            result = response.json()

            # 提取响应（Ollama格式）
            if 'choices' in result:
                content = result['choices'][0]['message']['content']
            else:
                content = result.get('response', 'No content')

            print(f"\n[OK] 响应时间: {elapsed:.2f}秒")
            print(f"内容: {content[:100]}...")

            # 测试JSON输出
            print("\n测试JSON格式输出:")
            json_payload = {
                "model": "gemma3n:latest",
                "messages": [
                    {"role": "system", "content": "以JSON格式回答"},
                    {"role": "user", "content": "返回格式: {\"action\": \"test\", \"params\": {}}"}
                ],
                "stream": False
            }

            response2 = requests.post(url, json=json_payload, timeout=60)
            if response2.status_code == 200:
                result2 = response2.json()
                content2 = result2['choices'][0]['message']['content']
                print(f"JSON响应: {content2}")

                # 尝试解析
                try:
                    parsed = json.loads(content2)
                    print("[OK] JSON解析成功")
                except:
                    print("[WARN] JSON解析失败，需要改进Prompt")

            return True
        else:
            print(f"[FAIL] 错误: {response.status_code}")
            return False

    except Exception as e:
        print(f"[FAIL] 异常: {e}")
        return False


def test_photoshop_intent():
    """测试Photoshop意图理解"""
    print("\n" + "=" * 60)
    print("测试 Photoshop 意图理解")
    print("=" * 60)

    url = "http://localhost:11434/v1/chat/completions"

    test_cases = [
        "我要锐化一下",
        "创建一个200x150的矩形",
        "新建一个文档"
    ]

    for text in test_cases:
        print(f"\n[测试] {text}")

        payload = {
            "model": "gemma3n:latest",
            "messages": [
                {"role": "system", "content": "你是一个Photoshop助手。返回JSON: {\"action\": \"动作\", \"params\": {}, \"complete\": true/false}"},
                {"role": "user", "content": text}
            ],
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"响应: {content}")

                # 尝试解析
                try:
                    parsed = json.loads(content)
                    print(f"  -> 动作: {parsed.get('action')}")
                    print(f"  -> 完整: {parsed.get('complete')}")
                except:
                    print("  [WARN] 不是有效JSON")
            else:
                print(f"[FAIL] 请求失败")
        except Exception as e:
            print(f"[FAIL] {e}")


def main():
    """主函数"""
    # 测试基础功能
    if test_gemma_basic():
        # 测试Photoshop意图
        test_photoshop_intent()

        print("\n" + "=" * 60)
        print("测试完成")
        print("=" * 60)
        print("\n建议:")
        print("1. 如果响应时间 < 3秒，适合使用")
        print("2. 如果JSON解析成功率高，适合结构化输出")
        print("3. 可以集成到语音控制系统中")


if __name__ == "__main__":
    main()
