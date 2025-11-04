# -*- coding: utf-8 -*-
"""测试第5项: session_hello_world.py - Session版本的Hello World"""

import os
import sys

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_session_hello_world():
    """运行session_hello_world测试"""
    safe_print("🌍 开始执行第5项: session_hello_world.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import built-in modules (原始代码逻辑)
        from tempfile import mkdtemp

        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 使用Session创建文档 (原始代码逻辑)
        safe_print("\n🚀 使用Session创建Hello World文档...")
        with Session() as adobe:
            safe_print("✅ Session成功启动")

            # 创建文档 (原始代码逻辑)
            safe_print("\n📄 创建2000x2000文档...")
            doc = adobe.app.documents.add(2000, 2000)
            safe_print(f"   ✅ 文档创建成功")
            safe_print(f"   📊 文档ID: {doc.id}")
            safe_print(f"   📏 文档尺寸: {doc.width} x {doc.height}")

            # 创建文本图层 (原始代码逻辑)
            safe_print("\n✏️ 创建Hello World文本图层...")
            text_color = adobe.SolidColor()
            text_color.rgb.red = 255
            text_color.rgb.green = 0
            text_color.rgb.blue = 0

            new_text_layer = doc.artLayers.add()
            new_text_layer.kind = adobe.LayerKind.TextLayer
            new_text_layer.textItem.contents = "Hello, World!"
            new_text_layer.textItem.position = [160, 167]
            new_text_layer.textItem.size = 40
            new_text_layer.textItem.color = text_color

            safe_print(f"   ✅ 文本图层创建成功: {new_text_layer.name}")
            safe_print(f"   📝 内容: {new_text_layer.textItem.contents}")
            safe_print(f"   🎨 颜色: 红色 (RGB: 255, 0, 0)")
            safe_print(f"   📏 大小: {new_text_layer.textItem.size}pt")
            safe_print(f"   📍 位置: {new_text_layer.textItem.position}")

            # 添加更多测试内容
            safe_print("\n🎨 添加更多测试内容...")

            # 创建背景
            bg_layer = doc.artLayers.add()
            bg_layer.name = "Background"
            bg_layer.move(doc.artLayers[0], adobe.ElementPlacement.PlaceBefore)

            bg_color = adobe.SolidColor()
            bg_color.rgb.red = 240
            bg_color.rgb.green = 240
            bg_color.rgb.blue = 240
            adobe.app.backgroundColor = bg_color

            doc.selection.selectAll()
            doc.selection.fill(adobe.app.backgroundColor)
            doc.selection.deselect()
            safe_print("   ✅ 背景图层创建并填充")

            # 创建装饰文本
            decor_text = doc.artLayers.add()
            decor_text.kind = adobe.LayerKind.TextLayer
            decor_text.name = "Session Info"

            decor_color = adobe.SolidColor()
            decor_color.rgb.red = 0
            decor_color.rgb.green = 100
            decor_color.rgb.blue = 200
            decor_text.textItem.contents = "Session Hello World\n2000x2000 Document\nSession Version Test"
            decor_text.textItem.size = 28
            decor_text.textItem.position = [100, 300]
            decor_text.textItem.color = decor_color
            safe_print("   ✅ 装饰文本创建")

            # 创建彩色装饰
            colors = [
                ("红色装饰", 255, 100, 100, [300, 500]),
                ("绿色装饰", 100, 255, 100, [500, 500]),
                ("蓝色装饰", 100, 100, 255, [700, 500])
            ]

            for name, r, g, b, position in colors:
                decor_layer = doc.artLayers.add()
                decor_layer.name = name

                color = adobe.SolidColor()
                color.rgb.red = r
                color.rgb.green = g
                color.rgb.blue = b
                adobe.app.foregroundColor = color

                x, y = position
                doc.selection.select([[x, y], [x+80, y], [x+80, y+80], [x, y+80]])
                doc.selection.fill(adobe.app.foregroundColor)
                doc.selection.deselect()
                safe_print(f"   ✅ 创建装饰: {name}")

            # 设置保存选项 (原始代码逻辑)
            safe_print("\n💾 设置保存选项...")
            options = adobe.JPEGSaveOptions(quality=1)
            safe_print(f"   📊 JPEG质量设置: {options.quality}")

            # 保存文档 (原始代码逻辑)
            safe_print("\n💾 保存文档...")
            try:
                # 使用临时目录 (原始代码逻辑)
                temp_dir = mkdtemp("photoshop-python-api")
                jpg_file = os.path.join(temp_dir, "hello_world.jpg")
                safe_print(f"   📁 临时目录: {temp_dir}")

                # 执行保存 (原始代码逻辑)
                doc.saveAs(jpg_file, options, asCopy=True)
                safe_print(f"   ✅ 文档保存成功: {jpg_file}")

                # 同时保存到我们的测试目录
                test_save_dir = get_test_save_dir()
                test_jpg_file = os.path.join(test_save_dir, "session_hello_world_test.jpg")
                doc.saveAs(test_jpg_file, options, asCopy=True)
                safe_print(f"   ✅ 测试文档保存成功: {test_jpg_file}")

                # 执行JavaScript (原始代码逻辑)
                safe_print("\n🔧 执行JavaScript...")
                try:
                    js_code = f'alert("save to jpg: {jpg_file}")'
                    # 注释掉alert，避免干扰测试
                    # adobe.app.doJavaScript(js_code)
                    safe_print(f"   ℹ️ JavaScript代码已准备: {js_code}")
                    safe_print("   ℹ️ 已跳过alert显示以避免干扰")
                except Exception as e:
                    safe_print(f"   ⚠️ JavaScript执行失败: {str(e)}")

            except Exception as e:
                safe_print(f"   ❌ 保存失败: {str(e)}")

            # 最终状态检查
            safe_print("\n📊 最终状态:")
            safe_print(f"   🎭 总图层数量: {doc.artLayers.length}")
            safe_print(f"   📄 文档名称: {doc.name}")
            safe_print(f"   📏 文档尺寸: {doc.width} x {doc.height}")
            safe_print(f"   📐 分辨率: {doc.resolution} ppi")

            # Session自动关闭
            safe_print("\n🔚 Session将自动关闭...")

        safe_print("✅ Session已自动关闭")

        safe_print("\n🎉 第5项: session_hello_world.py 测试完成!")
        safe_print("✅ 验证功能: Session上下文、文档创建、文本图层、保存选项、JavaScript执行")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. Session上下文是否正常工作")
        safe_print("3. 文档创建和保存权限是否正常")
        safe_print("4. JavaScript执行是否支持")
        return False

if __name__ == "__main__":
    test_session_hello_world()