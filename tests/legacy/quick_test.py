# -*- coding: utf-8 -*-
"""
快速测试脚本 - 直接测试所有功能
无需交互，直接运行并显示结果
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_all_functions import ComprehensiveTestSuite


def main():
    """快速测试所有功能"""
    print("=" * 80)
    print("Photoshop API 快速功能测试")
    print("=" * 80)
    print("\n正在测试所有99个功能...")

    suite = ComprehensiveTestSuite()
    results = suite.run_batch_test()

    print("\n" + "=" * 80)
    print("测试完成!")
    print("=" * 80)
    print(suite.generate_report(results))


if __name__ == "__main__":
    main()
