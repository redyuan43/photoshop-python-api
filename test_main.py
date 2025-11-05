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
    "06_list_documents": "test_06_list_documents",
    "07_get_document_by_name": "test_07_get_document_by_name",
    "08_open_psd": "test_08_open_psd",
    "09_save_to_psd": "test_09_save_to_psd",
    "10_revert_changes": "test_10_revert_changes",
    "11_session_new_document": "test_11_session_new_document",
  "12_session_document_duplicate": "test_12_session_document_duplicate",
  "13_fit_on_screen": "test_13_fit_on_screen",

    # 图层操作类 (14-25项)
    "20_rotate_layer": "test_20_rotate_layer",
    "21_convert_smartobject_to_layer": "test_21_convert_smartobject_to_layer",
    "22_operate_layerSet": "test_22_operate_layerSet",
    "23_copy_and_paste": "test_23_copy_and_paste",
    "24_import_image_as_layer": "test_24_import_image_as_layer",
    "25_replace_images": "test_25_replace_images",

    # 颜色和绘制类 (26-31项)
    "26_color": "test_26_color",
    "27_change_color_of_background_and_foreground": "test_27_change_color_of_background_and_foreground",
    "28_compare_colors": "test_28_compare_colors",
    "29_fill_selection": "test_29_fill_selection",
    "30_delete_and_fill_selection": "test_30_delete_and_fill_selection",
    "31_selection_stroke": "test_31_selection_stroke",

    # 选区操作类 (32-36项)
    "32_load_selection": "test_32_load_selection",
    "33_cropping": "test_33_cropping",
    "34_trim": "test_34_trim",
    "35_current_tool": "test_35_current_tool",
    "36_toggle_proof_colors": "test_36_toggle_proof_colors",

    # 导出保存类 (37-44项)
    "37_export_document": "test_37_export_document",
    "38_export_document_with_options": "test_38_export_document_with_options",
    "39_export_layers_as_png": "test_39_export_layers_as_png",
    "40_export_layers_use_export_options_saveforweb": "test_40_export_layers_use_export_options_saveforweb",
    "41_export_artboards": "test_41_export_artboards",
    "42_save_as_pdf": "test_42_save_as_pdf",
    "43_save_as_tga": "test_43_save_as_tga",
    "44_create_thumbnail": "test_44_create_thumbnail",

    # 滤镜效果类 (45-50项)
    "45_apply_filters": "test_45_apply_filters",
    "46_apply_crystallize_filter_action": "test_46_apply_crystallize_filter_action",
    "47_emboss_action": "test_47_emboss_action",
    "48_smart_sharpen": "test_48_smart_sharpen",
    "49_session_smart_sharpen": "test_49_session_smart_sharpen",
    "50_add_slate": "test_50_add_slate",
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
        elif hasattr(module, 'test_list_documents') and test_name == "06_list_documents":
            test_function = module.test_list_documents
        elif hasattr(module, 'test_get_document_by_name') and test_name == "07_get_document_by_name":
            test_function = module.test_get_document_by_name
        elif hasattr(module, 'test_open_psd') and test_name == "08_open_psd":
            test_function = module.test_open_psd
        elif hasattr(module, 'test_save_to_psd') and test_name == "09_save_to_psd":
            test_function = module.test_save_to_psd
        elif hasattr(module, 'test_revert_changes') and test_name == "10_revert_changes":
            test_function = module.test_revert_changes
        elif hasattr(module, 'test_session_new_document') and test_name == "11_session_new_document":
            test_function = module.test_session_new_document
        elif hasattr(module, 'test_session_document_duplicate') and test_name == "12_session_document_duplicate":
            test_function = module.test_session_document_duplicate
        elif hasattr(module, 'test_fit_on_screen') and test_name == "13_fit_on_screen":
            test_function = module.test_fit_on_screen
        elif hasattr(module, 'test_export_layers_use_export_options_saveforweb') and test_name == "40_export_layers_use_export_options_saveforweb":
            test_function = module.test_export_layers_use_export_options_saveforweb
        elif hasattr(module, 'test_export_artboards') and test_name == "41_export_artboards":
            test_function = module.test_export_artboards
        elif hasattr(module, 'test_save_as_pdf') and test_name == "42_save_as_pdf":
            test_function = module.test_save_as_pdf
        elif hasattr(module, 'test_save_as_tga') and test_name == "43_save_as_tga":
            test_function = module.test_save_as_tga
        elif hasattr(module, 'test_create_thumbnail') and test_name == "44_create_thumbnail":
            test_function = module.test_create_thumbnail
        elif hasattr(module, 'test_apply_filters') and test_name == "45_apply_filters":
            test_function = module.test_apply_filters
        elif hasattr(module, 'test_apply_crystallize_filter_action') and test_name == "46_apply_crystallize_filter_action":
            test_function = module.test_apply_crystallize_filter_action
        elif hasattr(module, 'test_emboss_action') and test_name == "47_emboss_action":
            test_function = module.test_emboss_action
        elif hasattr(module, 'test_smart_sharpen') and test_name == "48_smart_sharpen":
            test_function = module.test_smart_sharpen
        elif hasattr(module, 'test_session_smart_sharpen') and test_name == "49_session_smart_sharpen":
            test_function = module.test_session_smart_sharpen
        elif hasattr(module, 'test_add_slate') and test_name == "50_add_slate":
            test_function = module.test_add_slate
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