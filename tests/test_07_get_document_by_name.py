# -*- coding: utf-8 -*-
"""测试第7项: get_document_by_name.py - 按名称获取文档"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_get_document_by_name():
    """运行get_document_by_name测试"""
    safe_print("🔍 开始执行第7项: get_document_by_name.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        with Session() as ps:
            safe_print("✅ Session成功启动")

            # 获取初始文档列表
            safe_print("\n📋 获取当前打开的文档...")
            initial_docs = []
            for doc in ps.app.documents:
                initial_docs.append({
                    'name': doc.name,
                    'id': doc.id,
                    'width': doc.width,
                    'height': doc.height
                })
                safe_print(f"   📄 {doc.name} (ID: {doc.id})")

            safe_print(f"   📊 初始文档数量: {len(initial_docs)}")

            # 创建测试文档以便按名称查找
            safe_print("\n🔧 创建测试文档...")
            test_docs_info = [
                ("test.psd", 400, 300, 72, "测试PSD文档"),
                ("search_target.jpg", 500, 400, 96, "搜索目标JPG文档"),
                ("find_this_file.png", 300, 200, 150, "查找目标PNG文档"),
                ("duplicate_name.psd", 600, 450, 72, "重复名称文档"),
                ("find_this_file.png", 800, 600, 96, "重复查找PNG文档"),  # 重复名称测试
            ]

            created_docs = []
            for name, width, height, resolution, desc in test_docs_info:
                try:
                    doc = ps.app.documents.add(width, height, resolution, name)
                    created_docs.append(doc)

                    # 添加可见内容以便区分
                    color = ps.SolidColor()
                    if "psd" in name.lower():
                        color.rgb.red = 255
                        color.rgb.green = 100
                        color.rgb.blue = 100
                    elif "jpg" in name.lower():
                        color.rgb.red = 100
                        color.rgb.green = 255
                        color.rgb.blue = 100
                    else:  # PNG
                        color.rgb.red = 100
                        color.rgb.green = 100
                        color.rgb.blue = 255

                    ps.app.foregroundColor = color
                    doc.selection.select([[50, 50], [width-50, 50], [width-50, height-50], [50, height-50]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                    safe_print(f"   ✅ 创建文档: {name} - {desc}")
                    safe_print(f"      📏 尺寸: {width}x{height}, 分辨率: {resolution}ppi")

                except Exception as e:
                    safe_print(f"   ❌ 创建文档失败: {name} - {str(e)}")

            safe_print(f"   📊 新增测试文档数量: {len(created_docs)}")

            # 测试1: 查找存在的文档 (原始代码逻辑)
            safe_print("\n🔍 测试1: 查找 'test.psd' 文档 (原始逻辑)...")
            found = False
            for doc in ps.app.documents:
                if doc.name == "test.psd":
                    safe_print(f"   ✅ 找到文档: {doc.name}")
                    safe_print(f"      🆔 ID: {doc.id}")
                    safe_print(f"      📏 尺寸: {doc.width} x {doc.height}")
                    found = True
                    break

            if not found:
                safe_print("   ❌ 未找到文档 'test.psd'!")

            # 测试2: 查找多个特定名称的文档
            safe_print("\n🔍 测试2: 查找多个特定名称的文档...")
            search_names = ["search_target.jpg", "find_this_file.png", "duplicate_name.psd"]

            for search_name in search_names:
                safe_print(f"   🔍 查找文档: {search_name}")
                found_docs = []

                for doc in ps.app.documents:
                    if doc.name == search_name:
                        found_docs.append(doc)

                if found_docs:
                    safe_print(f"      ✅ 找到 {len(found_docs)} 个同名文档:")
                    for i, doc in enumerate(found_docs):
                        safe_print(f"         {i+1}. {doc.name} (ID: {doc.id})")
                else:
                    safe_print(f"      ❌ 未找到文档: {search_name}")

            # 测试3: 查找不存在的文档
            safe_print("\n🔍 测试3: 查找不存在的文档...")
            non_existent_names = ["nonexistent.psd", "missing_file.jpg", "not_found.png"]

            for search_name in non_existent_names:
                safe_print(f"   🔍 查找不存在的文档: {search_name}")
                found = False

                for doc in ps.app.documents:
                    if doc.name == search_name:
                        found = True
                        break

                if not found:
                    safe_print(f"      ✅ 正确: 文档 '{search_name}' 不存在")
                else:
                    safe_print(f"      ⚠️ 意外: 找到了文档 '{search_name}'")

            # 测试4: 模糊查找和部分匹配
            safe_print("\n🔍 测试4: 模糊查找和部分匹配...")
            search_terms = ["test", "find", "target", ".psd", ".jpg", ".png"]

            for term in search_terms:
                safe_print(f"   🔍 查找包含 '{term}' 的文档:")
                matching_docs = []

                for doc in ps.app.documents:
                    if term.lower() in doc.name.lower():
                        matching_docs.append(doc)

                if matching_docs:
                    safe_print(f"      ✅ 找到 {len(matching_docs)} 个匹配文档:")
                    for i, doc in enumerate(matching_docs):
                        safe_print(f"         {i+1}. {doc.name}")
                else:
                    safe_print(f"      ℹ️ 没有包含 '{term}' 的文档")

            # 测试5: 大小写敏感性测试
            safe_print("\n🔍 测试5: 大小写敏感性测试...")
            case_test_names = ["Test.psd", "TEST.PSD", "test.PSD"]

            for test_name in case_test_names:
                safe_print(f"   🔍 查找 '{test_name}' (大小写测试):")
                found = False

                for doc in ps.app.documents:
                    if doc.name == test_name:  # 精确匹配
                        found = True
                        safe_print(f"      ✅ 精确匹配找到: {doc.name}")
                        break

                if not found:
                    safe_print(f"      ❌ 精确匹配未找到 (大小写敏感)")

            # 测试6: 获取文档引用并操作
            safe_print("\n🔍 测试6: 获取文档引用并进行操作...")
            target_name = "search_target.jpg"
            target_doc = None

            # 查找目标文档
            for doc in ps.app.documents:
                if doc.name == target_name:
                    target_doc = doc
                    break

            if target_doc:
                safe_print(f"   ✅ 获取到文档引用: {target_doc.name}")

                # 对文档进行一些操作
                try:
                    safe_print(f"      📊 文档信息:")
                    safe_print(f"         ID: {target_doc.id}")
                    safe_print(f"         尺寸: {target_doc.width} x {target_doc.height}")
                    safe_print(f"         分辨率: {target_doc.resolution} ppi")
                    safe_print(f"         图层数量: {target_doc.artLayers.length}")

                    # 修改文档属性
                    original_name = target_doc.name
                    target_doc.name = f"{original_name}_modified"
                    safe_print(f"      ✅ 修改名称为: {target_doc.name}")

                    # 恢复原始名称
                    target_doc.name = original_name
                    safe_print(f"      ✅ 恢复原始名称: {target_doc.name}")

                except Exception as e:
                    safe_print(f"      ❌ 操作文档失败: {str(e)}")
            else:
                safe_print(f"   ❌ 未找到文档: {target_name}")

            # 测试7: 文档集合操作
            safe_print("\n🔍 测试7: 文档集合操作...")
            all_doc_names = [doc.name for doc in ps.app.documents]
            safe_print(f"   📊 所有文档名称列表:")
            for i, name in enumerate(all_doc_names):
                safe_print(f"      {i+1:2d}. {name}")

            # 统计不同类型文档
            psd_count = sum(1 for name in all_doc_names if name.lower().endswith('.psd'))
            jpg_count = sum(1 for name in all_doc_names if name.lower().endswith('.jpg'))
            png_count = sum(1 for name in all_doc_names if name.lower().endswith('.png'))

            safe_print(f"   📊 文档类型统计:")
            safe_print(f"      PSD文档: {psd_count} 个")
            safe_print(f"      JPG文档: {jpg_count} 个")
            safe_print(f"      PNG文档: {png_count} 个")

            # 保存测试结果
            safe_print("\n💾 保存测试结果...")
            try:
                save_dir = get_test_save_dir()

                # 保存文档名称列表
                doc_list_file = os.path.join(save_dir, "document_names_list.txt")
                with open(doc_list_file, 'w', encoding='utf-8') as f:
                    f.write(f"文档名称查找测试结果\n")
                    f.write(f"测试时间: {datetime.now()}\n")
                    f.write(f"总文档数量: {len(all_doc_names)}\n\n")
                    f.write("文档列表:\n")
                    for i, name in enumerate(all_doc_names):
                        f.write(f"{i+1}. {name}\n")

                safe_print(f"   ✅ 保存文档列表: {doc_list_file}")

                # 保存一个测试文档的状态
                if created_docs:
                    test_doc = created_docs[0]
                    save_path = os.path.join(save_dir, "get_document_by_name_test.jpg")
                    save_options = ps.JPEGSaveOptions(quality=8)
                    test_doc.saveAs(save_path, save_options, asCopy=True)
                    safe_print(f"   ✅ 保存测试文档: {save_path}")

            except Exception as e:
                safe_print(f"   ⚠️ 保存失败: {str(e)}")

            # 最终状态
            final_docs = [doc.name for doc in ps.app.documents]
            safe_print(f"\n📊 最终状态:")
            safe_print(f"   📄 当前文档数量: {len(final_docs)}")
            safe_print(f"   📊 测试创建文档: {len(created_docs)} 个")

        safe_print("\n🎉 第7项: get_document_by_name.py 测试完成!")
        safe_print("✅ 验证功能: 按名称查找文档、精确匹配、模糊匹配、大小写敏感性")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 文档创建和访问权限是否正常")
        safe_print("3. 字符串比较和查找功能是否正常")
        safe_print("4. Session上下文管理是否稳定")
        return False

if __name__ == "__main__":
    test_get_document_by_name()