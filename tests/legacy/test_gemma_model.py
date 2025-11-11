# -*- coding: utf-8 -*-
"""
Gemma3nPhotoshop
"""

import requests
import json
from typing import Dict, Any


def test_gemma_connection(model_name: str = "gemma3n:latest", base_url: str = "http://localhost:11434/v1"):
    """Gemma"""
    print("=" * 60)
    print(f" Gemma3n ")
    print("=" * 60)

    try:
        # API
        url = f"{base_url}/api/tags"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            models = response.json()
            print("\n[OK] Ollama")

            # 
            model_exists = False
            for model in models.get('models', []):
                if model_name in model['name']:
                    model_exists = True
                    print(f"[OK]  {model_name} ")
                    break

            if not model_exists:
                print(f"[WARN]  {model_name} ")
                print(":")
                for model in models.get('models', []):
                    print(f"  - {model['name']}")
                return False

            return True
        else:
            print(f"[FAIL] Ollama: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("[FAIL] Ollama")
        print("Ollamaollama serve")
        return False
    except Exception as e:
        print(f"[FAIL] : {e}")
        return False


def test_gemma_simple_chat(model_name: str = "gemma3n:latest"):
    """Gemma"""
    print("\n" + "=" * 60)
    print(" Gemma ")
    print("=" * 60)

    url = "http://localhost:11434/v1/chat/completions"

    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": ""}
        ],
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            print("\n[OK] ")
            print(f"\n: ")
            print(f"Gemma: {result['message']['content']}")
            return True
        else:
            print(f"[FAIL] : {response.status_code}")
            print(response.text)
            return False

    except Exception as e:
        print(f"[FAIL] : {e}")
        return False


def test_gemma_photoshop_intent(model_name: str = "gemma3n:latest"):
    """GemmaPhotoshop"""
    print("\n" + "=" * 60)
    print(" Gemma Photoshop")
    print("=" * 60)

    url = "http://localhost:11434/v1/chat/completions"

    # 
    test_cases = [
        {
            "user": "",
            "expected": ""
        },
        {
            "user": "200x150",
            "expected": ""
        },
        {
            "user": "800x600",
            "expected": ""
        }
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"\n[ {i}]")
        print(f": {case['user']}")
        print(f": {case['expected']}")

        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "PhotoshopJSON"
                },
                {
                    "role": "user",
                    "content": f"{case['user']}\n\nJSON{{\"action\": \"\", \"params\": {{}}, \"complete\": true/false}}"
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.8
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=30)

            if response.status_code == 200:
                result = response.json()
                content = result['message']['content']

                print(f"\nGemma:")
                print(content)

                # JSON
                try:
                    parsed = json.loads(content)
                    print(f"\n[OK] JSON")
                    print(f"   : {parsed.get('action')}")
                    print(f"   : {parsed.get('complete')}")
                    print(f"   : {parsed.get('params')}")
                except json.JSONDecodeError:
                    print(f"\n[WARN] JSONJSON")

            else:
                print(f"[FAIL] : {response.status_code}")

        except Exception as e:
            print(f"[FAIL] : {e}")


def test_performance(model_name: str = "gemma3n:latest"):
    """"""
    print("\n" + "=" * 60)
    print(" Gemma ")
    print("=" * 60)

    url = "http://localhost:11434/v1/chat/completions"

    import time

    # 10
    times = []
    for i in range(3):  # 3
        payload = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": ""}
            ]
        }

        start_time = time.time()
        try:
            response = requests.post(url, json=payload, timeout=60)
            end_time = time.time()

            if response.status_code == 200:
                elapsed = end_time - start_time
                times.append(elapsed)
                print(f"{i+1}: {elapsed:.2f}")
            else:
                print(f"{i+1}: ")

        except Exception as e:
            print(f"{i+1}:  - {e}")

    if times:
        avg_time = sum(times) / len(times)
        print(f"\n: {avg_time:.2f}")

        # 
        if avg_time < 2:
            print("[OK]  (<2)")
        elif avg_time < 5:
            print("[OK]  (2-5)")
        else:
            print("[WARN]  (>5)")


def main():
    """"""
    model_name = "gemma3n:latest"

    print("\n Gemma3n Model Test")
    print("=" * 60)

    # 1. 
    if not test_gemma_connection(model_name):
        print("\n[FAIL] GemmaOllama")
        return

    # 2. 
    test_gemma_simple_chat(model_name)

    # 3. Photoshop
    test_gemma_photoshop_intent(model_name)

    # 4. 
    test_performance(model_name)

    print("\n" + "=" * 60)
    print("")
    print("=" * 60)

    # 
    print("\n :")
    print("1.  < 2")
    print("2. JSON")
    print("3. LLM")
    print("4. LLM")


if __name__ == "__main__":
    main()
