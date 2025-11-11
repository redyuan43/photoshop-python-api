#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试修复后的交互式系统
"""

import sys
sys.path.insert(0, "D:/github/photoshop-python-api")

from voice_photoshop.test_interactive_utf8 import InteractiveSession

def test_single_command():
    """测试单个命令"""
    session = InteractiveSession()

    # 测试用例1：锐化图像（complete=true）
    print("=" * 70)
    print(" 测试1: 锐化图像")
    print("=" * 70)

    result = session.process_message("我要锐化图像")
    print(f"返回结果: {result}\n")

    # 测试用例2：生成矩形框（complete=true）
    print("=" * 70)
    print(" 测试2: 生成矩形框")
    print("=" * 70)

    result = session.process_message("生成一个矩形框")
    print(f"返回结果: {result}\n")

    # 测试用例3：新建文档（complete=true）
    print("=" * 70)
    print(" 测试3: 新建文档")
    print("=" * 70)

    result = session.process_message("创建一个新文档")
    print(f"返回结果: {result}\n")

    print("=" * 70)
    print(" 测试完成!")
    print("=" * 70)

if __name__ == "__main__":
    test_single_command()
