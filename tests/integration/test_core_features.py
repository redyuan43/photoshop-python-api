# -*- coding: utf-8 -*-
"""
核心功能快速测试
测试最常用的API功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from photoshop_api_extended import api

def test_create_text():
    """测试创建文字功能"""
    print("\n" + "=" * 70)
    print("测试 1: create_text - 创建文字")
    print("=" * 70)

    result = api.execute('create_text', {
        'text': '2025年春季之行',
        'x': 100,
        'y': 200,
        'font': 'Arial',
        'font_size': 72,
        'color': {'red': 255, 'green': 0, 'blue': 0},
        'bold': True,
        'alignment': 'center'
    })

    if result['success']:
        print(f"✅ 成功: {result['message']}")
    else:
        print(f"❌ 失败: {result['message']}")

    return result['success']


def test_new_document():
    """测试新建文档"""
    print("\n" + "=" * 70)
    print("测试 2: new_document - 新建文档")
    print("=" * 70)

    result = api.execute('new_document', {
        'width': 1920,
        'height': 1080,
        'resolution': 72,
        'name': 'Test Document'
    })

    if result['success']:
        print(f"✅ 成功: {result['message']}")
    else:
        print(f"❌ 失败: {result['message']}")

    return result['success']


def test_smart_sharpen():
    """测试智能锐化"""
    print("\n" + "=" * 70)
    print("测试 3: smart_sharpen - 智能锐化")
    print("=" * 70)

    result = api.execute('smart_sharpen', {
        'amount': 150,
        'radius': 5,
        'noiseReduction': 20
    })

    if result['success']:
        print(f"✅ 成功: {result['message']}")
    else:
        print(f"❌ 失败: {result['message']}")

    return result['success']


def test_create_rectangle():
    """测试创建矩形"""
    print("\n" + "=" * 70)
    print("测试 4: create_rectangle - 创建矩形")
    print("=" * 70)

    result = api.execute('create_rectangle', {
        'x': 100,
        'y': 100,
        'width': 300,
        'height': 200,
        'color': {'red': 255, 'green': 100, 'blue': 100}
    })

    if result['success']:
        print(f"✅ 成功: {result['message']}")
    else:
        print(f"❌ 失败: {result['message']}")

    return result['success']


def test_rotate_layer():
    """测试旋转图层"""
    print("\n" + "=" * 70)
    print("测试 5: rotate_layer - 旋转图层")
    print("=" * 70)

    result = api.execute('rotate_layer', {
        'angle': 45
    })

    if result['success']:
        print(f"✅ 成功: {result['message']}")
    else:
        print(f"❌ 失败: {result['message']}")

    return result['success']


def test_brightness_contrast():
    """测试亮度/对比度"""
    print("\n" + "=" * 70)
    print("测试 6: brightness_contrast - 亮度/对比度")
    print("=" * 70)

    result = api.execute('brightness_contrast', {
        'brightness': 20,
        'contrast': 30
    })

    if result['success']:
        print(f"✅ 成功: {result['message']}")
    else:
        print(f"❌ 失败: {result['message']}")

    return result['success']


def test_gaussian_blur():
    """测试高斯模糊"""
    print("\n" + "=" * 70)
    print("测试 7: gaussian_blur - 高斯模糊")
    print("=" * 70)

    result = api.execute('gaussian_blur', {
        'radius': 5
    })

    if result['success']:
        print(f"✅ 成功: {result['message']}")
    else:
        print(f"❌ 失败: {result['message']}")

    return result['success']


def test_select_all():
    """测试全选"""
    print("\n" + "=" * 70)
    print("测试 8: select_all - 全选")
    print("=" * 70)

    result = api.execute('select_all', {})

    if result['success']:
        print(f"✅ 成功: {result['message']}")
    else:
        print(f"❌ 失败: {result['message']}")

    return result['success']


def main():
    """运行所有核心测试"""
    print("=" * 70)
    print(" Photoshop API 核心功能测试")
    print("=" * 70)
    print("\n将测试以下8个核心功能:")
    print("  1. create_text - 创建文字")
    print("  2. new_document - 新建文档")
    print("  3. smart_sharpen - 智能锐化")
    print("  4. create_rectangle - 创建矩形")
    print("  5. rotate_layer - 旋转图层")
    print("  6. brightness_contrast - 亮度/对比度")
    print("  7. gaussian_blur - 高斯模糊")
    print("  8. select_all - 全选")
    print("\n" + "=" * 70)

    input("\n按回车键开始测试...")

    tests = [
        ("create_text", test_create_text),
        ("new_document", test_new_document),
        ("smart_sharpen", test_smart_sharpen),
        ("create_rectangle", test_create_rectangle),
        ("rotate_layer", test_rotate_layer),
        ("brightness_contrast", test_brightness_contrast),
        ("gaussian_blur", test_gaussian_blur),
        ("select_all", test_select_all)
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"❌ 测试异常: {str(e)}")
            results.append((name, False))

    # 总结
    print("\n" + "=" * 70)
    print(" 测试结果总结")
    print("=" * 70)

    success_count = sum(1 for _, success in results if success)
    total_count = len(results)

    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {status}: {name}")

    print("\n" + "=" * 70)
    print(f" 总计: {success_count}/{total_count} 个测试通过 ({success_count/total_count*100:.1f}%)")
    print("=" * 70)


if __name__ == "__main__":
    main()
