# -*- coding: utf-8 -*-
"""Photoshop Python API 统一测试入口"""

import os
import sys
import codecs
import importlib
from pathlib import Path

# 设置UTF-8编码解决中文显示问题
if sys.platform == 'win32':
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    except:
        pass

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def safe_print(text):
    """安全的打印函数，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'ignore').decode('ascii'))

# 测试用例注册表
TEST_CASES = {
    # 基础入门类 (1-5项)
    "01_hello_world": "test_01_hello_world",
    "02_create_new_document": "test_02_create_new_document",
    "03_new_document": "test_03_new_document",
    "04_photoshop_session": "test_04_photoshop_session",
    "05_session_hello_world": "test_05_session_hello_world",

    # 文档操作类 (6-13项)
    # "06_list_documents": "test_06_list_documents",
    # ...

    # 图层操作类 (14-25项)
    # "14_creating_a_layer": "test_14_creating_a_layer",
    # ...
}

def run_test(test_name):
    """运行指定的测试用例"""
    if test_name not in TEST_CASES:
        safe_print(f"❌ 未找到测试用例: {test_name}")
        return False

    module_name = TEST_CASES[test_name]

    try:
        # 动态导入测试模块
        module = importlib.import_module(f"tests.{module_name}")

        # 获取测试函数
        if hasattr(module, 'test_hello_world') and test_name == "01_hello_world":
            test_function = module.test_hello_world
        elif hasattr(module, 'test_create_new_document') and test_name == "02_create_new_document":
            test_function = module.test_create_new_document
        elif hasattr(module, 'test_new_document') and test_name == "03_new_document":
            test_function = module.test_new_document
        elif hasattr(module, 'test_photoshop_session') and test_name == "04_photoshop_session":
            test_function = module.test_photoshop_session
        elif hasattr(module, 'test_session_hello_world') and test_name == "05_session_hello_world":
            test_function = module.test_session_hello_world
        else:
            # 通用方法：查找test_开头的函数
            test_functions = [func for func in dir(module) if func.startswith('test_')]
            if test_functions:
                test_function = getattr(module, test_functions[0])
            else:
                safe_print(f"❌ 在模块 {module_name} 中未找到测试函数")
                return False

        # 运行测试
        safe_print(f"🚀 开始运行测试: {test_name}")
        success = test_function()

        if success:
            safe_print(f"✅ 测试 {test_name} 通过!")
        else:
            safe_print(f"❌ 测试 {test_name} 失败!")

        return success

    except ImportError as e:
        safe_print(f"❌ 导入测试模块失败: {module_name} - {str(e)}")
        return False
    except Exception as e:
        safe_print(f"❌ 运行测试时出错: {str(e)}")
        return False

def run_all_tests():
    """运行所有测试用例"""
    safe_print("🚀 开始运行所有测试用例...")

    results = []
    for test_name in TEST_CASES:
        safe_print(f"\n{'='*60}")
        success = run_test(test_name)
        results.append((test_name, success))

    # 统计结果
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)

    safe_print(f"\n{'='*60}")
    safe_print(f"📊 测试完成: {success_count}/{total_count} 成功")

    if success_count == total_count:
        safe_print("🎉 所有测试都通过了!")
    else:
        failed_tests = [name for name, success in results if not success]
        safe_print(f"❌ 失败的测试: {', '.join(failed_tests)}")

    return success_count == total_count

def list_tests():
    """列出所有可用的测试用例"""
    safe_print("📋 可用的测试用例:")

    categories = {
        "基础入门类 (1-5项)": ["01_hello_world", "02_create_new_document", "03_new_document"],
        "文档操作类 (6-13项)": [],
        "图层操作类 (14-25项)": [],
        "颜色和绘制类 (26-31项)": [],
        "选区操作类 (32-36项)": [],
        "导出保存类 (37-44项)": [],
        "滤镜效果类 (45-50项)": [],
        "高级功能类": []
    }

    for category, tests in categories.items():
        if tests:
            safe_print(f"\n📂 {category}:")
            for test in tests:
                if test in TEST_CASES:
                    module_name = TEST_CASES[test]
                    safe_print(f"  ✅ {test} -> {module_name}.py")
                else:
                    safe_print(f"  ❌ {test} -> 未实现")
        else:
            safe_print(f"\n📂 {category}: (暂无测试)")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        safe_print("使用方法:")
        safe_print("  python test_main.py <test_name>     # 运行指定测试")
        safe_print("  python test_main.py --list         # 列出所有测试")
        safe_print("  python test_main.py --all          # 运行所有测试")
        safe_print("")
        safe_print("示例:")
        safe_print("  python test_main.py 01_hello_world")
        safe_print("  python test_main.py 02_create_new_document")
        safe_print("  python test_main.py --all")
        return

    command = sys.argv[1]

    if command == "--list":
        list_tests()
    elif command == "--all":
        success = run_all_tests()
        sys.exit(0 if success else 1)
    else:
        test_name = command
        success = run_test(test_name)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()