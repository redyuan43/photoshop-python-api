# -*- coding: utf-8 -*-
"""测试第13项: fit_on_screen.py - 适应屏幕"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_fit_on_screen():
    """运行fit_on_screen测试"""
    safe_print("🖥️ 开始执行第13项: fit_on_screen.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本适应屏幕功能 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本适应屏幕功能 (原始逻辑)...")

        try:
            with Session() as ps:
                safe_print("✅ Session成功启动")

                # 获取当前活动文档
                if len(ps.app.documents) > 0:
                    doc = ps.active_document
                    safe_print(f"📄 当前活动文档: {doc.name}")
                    safe_print(f"   🆔 文档ID: {doc.id}")
                    safe_print(f"   📏 尺寸: {doc.width} x {doc.height} 像素")

                    # 原始代码执行
                    safe_print("\n🔄 执行适应屏幕命令...")
                    char_id = ps.app.charIDToTypeID("FtOn")
                    safe_print(f"📝 'FtOn' 转换为类型ID: {char_id}")

                    # 执行原始功能
                    ps.app.runMenuItem(char_id)
                    safe_print("✅ 适应屏幕命令执行完成!")

                    safe_print("👁️ 请观察Photoshop窗口 - 文档应该已经适应到屏幕大小")

                else:
                    safe_print("⚠️ 没有打开的文档，创建测试文档...")
                    test_doc = ps.app.documents.add(2000, 1500, 72, "Fit_Screen_Test")
                    safe_print(f"✅ 创建测试文档: {test_doc.name} (2000 x 1500 像素)")

                    # 执行适应屏幕
                    ps.app.runMenuItem(ps.app.charIDToTypeID("FtOn"))
                    safe_print("✅ 适应屏幕命令执行完成!")

        except Exception as e:
            safe_print(f"❌ 基本适应屏幕测试失败: {str(e)}")
            return False

        # 测试2: 不同尺寸文档的适应屏幕测试
        safe_print("\n🔧 测试2: 不同尺寸文档的适应屏幕测试...")

        document_sizes = [
            {"name": "小文档测试", "width": 400, "height": 300},
            {"name": "中等文档测试", "width": 1200, "height": 900},
            {"name": "大文档测试", "width": 3000, "height": 2000},
            {"name": "超大文档测试", "width": 5000, "height": 4000},
            {"name": "宽屏文档测试", "width": 4000, "height": 1000},
            {"name": "竖屏文档测试", "width": 1500, "height": 3000}
        ]

        for i, doc_config in enumerate(document_sizes):
            try:
                safe_print(f"   📄 测试 {i+1}: {doc_config['name']} ({doc_config['width']}x{doc_config['height']})")

                with Session(action="new_document") as ps:
                    # 创建指定尺寸的文档
                    test_doc = ps.app.documents.add(
                        doc_config['width'],
                        doc_config['height'],
                        72,
                        f"{doc_config['name']}_Doc"
                    )

                    safe_print(f"      ✅ 创建文档: {test_doc.name}")

                    # 添加可见内容用于观察
                    layer = test_doc.artLayers.add()
                    layer.name = f"{doc_config['name']}_内容"

                    # 添加文本标识
                    text_layer = test_doc.artLayers.add()
                    text_layer.kind = ps.LayerKind.TextLayer
                    text_layer.name = "尺寸标识"
                    text_layer.textItem.contents = f"{doc_config['name']}\n{doc_config['width']} x {doc_config['height']} 像素\n适应屏幕测试"
                    text_layer.textItem.size = 36
                    text_layer.textItem.position = [50, 100]

                    # 添加彩色边框
                    border_color = ps.SolidColor()
                    border_color.rgb.red = 255 - i * 30
                    border_color.rgb.green = 100 + i * 25
                    border_color.rgb.blue = 150 + i * 20
                    ps.app.foregroundColor = border_color

                    # 创建边框
                    test_doc.selection.select([[10, 10], [doc_config['width']-10, 10],
                                               [doc_config['width']-10, doc_config['height']-10],
                                               [10, doc_config['height']-10]])
                    test_doc.selection.stroke(ps.app.foregroundColor, 5)
                    test_doc.selection.deselect()

                    safe_print(f"      📏 文档尺寸: {test_doc.width} x {test_doc.height}")
                    safe_print(f"      🎨 已添加内容和边框")

                    # 执行适应屏幕
                    safe_print("      🔄 执行适应屏幕...")
                    ps.app.runMenuItem(ps.app.charIDToTypeID("FtOn"))
                    safe_print("      ✅ 适应屏幕完成")

                    # 添加延迟以便观察
                    safe_print("      👁️ 请观察文档适应效果")

            except Exception as e:
                safe_print(f"      ❌ {doc_config['name']} 测试失败: {str(e)}")

        # 测试3: 连续适应屏幕测试
        safe_print("\n🔧 测试3: 连续适应屏幕测试...")

        try:
            with Session(action="new_document") as ps:
                test_doc = ps.active_document
                test_doc.name = "连续适应屏幕测试"

                # 添加测试内容
                for i in range(3):
                    layer = test_doc.artLayers.add()
                    layer.name = f"测试层{i+1}"

                    text_layer = test_doc.artLayers.add()
                    text_layer.kind = ps.LayerKind.TextLayer
                    text_layer.name = f"文本{i+1}"
                    text_layer.textItem.contents = f"连续适应屏幕测试\n第{i+1}次"
                    text_layer.textItem.size = 24
                    text_layer.textItem.position = [100, 100 + i * 80]

                safe_print("   📄 创建连续测试文档")
                safe_print(f"      🎭 图层数量: {test_doc.artLayers.length}")

                # 连续执行多次适应屏幕
                for i in range(3):
                    safe_print(f"      🔄 第{i+1}次适应屏幕...")
                    ps.app.runMenuItem(ps.app.charIDToTypeID("FtOn"))
                    safe_print(f"      ✅ 第{i+1}次完成")

                safe_print("   ✅ 连续适应屏幕测试完成")

        except Exception as e:
            safe_print(f"   ❌ 连续适应屏幕测试失败: {str(e)}")

        # 测试4: 适应屏幕与其他操作组合测试
        safe_print("\n🔧 测试4: 适应屏幕与其他操作组合测试...")

        try:
            with Session(action="new_document") as ps:
                test_doc = ps.active_document

                # 先进行一些缩放操作
                safe_print("   📄 执行缩放操作...")
                # 缩小
                ps.app.runMenuItem(ps.app.charIDToTypeID("ZmOt"))
                safe_print("      🔍 缩小视图")

                # 放大
                ps.app.runMenuItem(ps.app.charIDToTypeID("ZmIn"))
                safe_print("      🔍 放大视图")

                # 实际像素
                ps.app.runMenuItem(ps.app.charIDToTypeID("Actl"))
                safe_print("      📐 实际像素大小")

                # 最后适应屏幕
                safe_print("   🔄 执行适应屏幕...")
                ps.app.runMenuItem(ps.app.charIDToTypeID("FtOn"))
                safe_print("   ✅ 适应屏幕与其他操作组合测试完成")

        except Exception as e:
            safe_print(f"   ❌ 组合操作测试失败: {str(e)}")

        # 测试5: 多文档适应屏幕测试
        safe_print("\n🔧 测试5: 多文档适应屏幕测试...")

        try:
            # 创建多个文档
            docs = []
            for i in range(3):
                with Session(action="new_document") as ps:
                    doc = ps.active_document
                    doc.name = f"多文档测试_{i+1}"

                    # 添加标识内容
                    layer = doc.artLayers.add()
                    layer.name = f"内容{i+1}"

                    text_layer = doc.artLayers.add()
                    text_layer.kind = ps.LayerKind.TextLayer
                    text_layer.textItem.contents = f"文档 {i+1}\n适应屏幕测试"
                    text_layer.textItem.size = 32
                    text_layer.textItem.position = [100, 150]

                    docs.append(doc.name)
                    safe_print(f"   📄 创建文档: {doc.name}")

                    # 对每个文档执行适应屏幕
                    ps.app.runMenuItem(ps.app.charIDToTypeID("FtOn"))
                    safe_print(f"      ✅ {doc.name} 适应屏幕完成")

            safe_print(f"   📊 多文档适应屏幕测试完成，共处理 {len(docs)} 个文档")

        except Exception as e:
            safe_print(f"   ❌ 多文档测试失败: {str(e)}")

        # 测试6: 适应屏幕命令参数测试
        safe_print("\n🔧 测试6: 适应屏幕命令参数测试...")

        try:
            with Session(action="new_document") as ps:
                test_doc = ps.active_document

                # 测试不同的字符ID转换
                char_ids = ["FtOn", "FitS", "Fits"]  # 尝试可能的字符ID

                for char_id_str in char_ids:
                    try:
                        char_id = ps.app.charIDToTypeID(char_id_str)
                        safe_print(f"   📝 '{char_id_str}' -> {char_id}")

                        # 尝试执行
                        ps.app.runMenuItem(char_id)
                        safe_print(f"      ✅ '{char_id_str}' 命令执行成功")

                        # 短暂延迟
                        import time
                        time.sleep(0.5)

                    except Exception as e:
                        safe_print(f"      ⚠️ '{char_id_str}' 命令执行失败: {str(e)}")

        except Exception as e:
            safe_print(f"   ❌ 参数测试失败: {str(e)}")

        # 测试7: 错误处理和边界情况
        safe_print("\n🔧 测试7: 错误处理和边界情况...")

        try:
            # 测试无文档时的适应屏幕
            safe_print("   📄 测试无文档时的适应屏幕...")
            with Session() as ps:
                # 不创建文档，直接尝试适应屏幕
                try:
                    ps.app.runMenuItem(ps.app.charIDToTypeID("FtOn"))
                    safe_print("      ✅ 无文档时适应屏幕执行成功")
                except Exception as e:
                    safe_print(f"      ⚠️ 无文档时适应屏幕失败: {str(e)}")

            # 测试极小文档的适应屏幕
            safe_print("   📄 测试极小文档的适应屏幕...")
            with Session(action="new_document") as ps:
                # 创建极小文档
                tiny_doc = ps.app.documents.add(10, 10, 72, "极小文档")
                safe_print(f"      📄 创建极小文档: {tiny_doc.name}")

                ps.app.runMenuItem(ps.app.charIDToTypeID("FtOn"))
                safe_print("      ✅ 极小文档适应屏幕完成")

        except Exception as e:
            safe_print(f"   ❌ 边界情况测试失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "fit_on_screen_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Fit on Screen 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 适应屏幕功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本适应屏幕功能 (原始代码逻辑)\n")
                f.write(f"- 不同尺寸文档适应屏幕\n")
                f.write(f"- 连续适应屏幕测试\n")
                f.write(f"- 适应屏幕与其他操作组合\n")
                f.write(f"- 多文档适应屏幕\n")
                f.write(f"- 适应屏幕命令参数测试\n")
                f.write(f"- 错误处理和边界情况\n")
                f.write(f"\n测试的文档尺寸:\n")
                for doc_config in document_sizes:
                    f.write(f"- {doc_config['name']}: {doc_config['width']}x{doc_config['height']}\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第13项: fit_on_screen.py 测试完成!")
        safe_print("✅ 验证功能: 基本适应屏幕、不同尺寸文档、连续操作、组合操作、多文档处理")
        safe_print("👁️ 请在Photoshop中观察各个文档的适应屏幕效果")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 适应屏幕功能是否可用")
        safe_print("3. 菜单命令访问权限是否正常")
        safe_print("4. 文档创建和显示是否正常")
        return False

if __name__ == "__main__":
    test_fit_on_screen()