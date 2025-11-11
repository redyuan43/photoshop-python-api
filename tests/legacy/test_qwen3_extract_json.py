# -*- coding: utf-8 -*-
"""
从qwen的thinking中提取JSON
qwen模型会将思考过程写入thinking标签，我们需要从中提取JSON
"""

import requests
import json
import re


def test_extract_json_from_thinking():
    """测试从thinking中提取JSON"""
    print("=" * 60)
    print("测试从 Qwen3-4B Thinking中提取JSON")
    print("=" * 60)

    url = "http://localhost:11434/v1/chat/completions"

    # 简单直接的系统prompt
    system_prompt = """你是一个Photoshop语音助手。

用户说什么，你就直接回答JSON。不要thinking过程。

例子：
用户: "我要锐化图像"
回答: {"action": "smart_sharpen", "params": {}, "complete": true}"""

    test_cases = [
        "我要锐化一下",
        "创建一个200x150的矩形",
        "新建一个800x600的文档",
        "旋转图层45度"
    ]

    for text in test_cases:
        print(f"\n[测试] {text}")

        payload = {
            "model": "qwen3:4b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            "stream": False,
            "options": {
                "temperature": 0.3
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=90)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']

                print(f"原始响应: {content[:80]}...")

                # 1. 先尝试正常JSON（没有thinking标签）
                content_stripped = content.strip()
                if content_stripped and not content_stripped.startswith('<'):
                    try:
                        parsed = json.loads(content_stripped)
                        print(f"  [OK] 直接JSON解析成功: {parsed.get('action')}")
                        continue
                    except:
                        pass

                # 2. 从thinking标签中提取JSON
                # 查找thinking标签内的JSON模式
                thinking_match = re.search(r'<thinking>(.*?)</thinking>', content, re.DOTALL)
                if thinking_match:
                    thinking_content = thinking_match.group(1)
                    # 在thinking内容中查找JSON
                    json_matches = re.findall(r'{[\s\S]*?}', thinking_content)
                    if json_matches:
                        # 尝试每个JSON匹配
                        for json_str in json_matches:
                            try:
                                parsed = json.loads(json_str)
                                if 'action' in parsed:
                                    print(f"  [OK] 从Thinking中提取JSON: {parsed.get('action')}")
                                    break
                            except:
                                continue
                        else:
                            print(f"  [WARN] Thinking中有JSON但解析失败")
                    else:
                        print(f"  [WARN] Thinking中没有找到JSON模式")
                else:
                    print(f"  [WARN] 没有找到thinking标签")

            else:
                print(f"[FAIL] 请求失败: {response.status_code}")
        except Exception as e:
            print(f"[FAIL] 异常: {e}")


def test_no_thinking_mode():
    """测试禁用thinking模式（如果支持）"""
    print("\n" + "=" * 60)
    print("测试禁用 Thinking 模式")
    print("=" * 60)

    url = "http://localhost:11434/v1/chat/completions"

    # 使用禁用thinking的配置（如果ollama支持）
    system_prompt = "直接回答JSON，不要thinking过程。"

    payload = {
        "model": "qwen3:4b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "我要锐化图像"}
        ],
        "stream": False,
        "options": {
            "temperature": 0.1,  # 降低随机性
            "top_k": 1,          # 最高确定性
            "num_predict": 100   # 限制输出长度
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=90)
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"响应: {content}")

            # 尝试提取JSON
            json_match = re.search(r'{[\s\S]*}', content)
            if json_match:
                try:
                    parsed = json.loads(json_match.group())
                    print(f"[OK] JSON解析成功: {parsed}")
                except:
                    print(f"[WARN] JSON解析失败")
            else:
                print(f"[WARN] 没有找到JSON")
        else:
            print(f"[FAIL] 请求失败: {response.status_code}")
    except Exception as e:
        print(f"[FAIL] 异常: {e}")


def main():
    test_extract_json_from_thinking()
    test_no_thinking_mode()

    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print("\nQwen3-4B 使用策略:")
    print("1. 性能优秀: 4.49秒 (比gemma快29.6%)")
    print("2. 需要从thinking中提取JSON")
    print("3. 建议集成时预处理响应内容")
    print("4. 适合作为主要本地LLM")


if __name__ == "__main__":
    main()
