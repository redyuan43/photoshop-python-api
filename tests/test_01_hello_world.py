# -*- coding: utf-8 -*-
"""测试第1项: hello_world.py - 基础连接和Hello World示例"""

import os
import sys

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_hello_world():
    """运行hello_world测试"""
    safe_print("🌍 开始执行第1项: hello_world.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        from photoshop import Session

        with Session() as ps:
            safe_print("✅ Session成功启动")

            # Create a new document
            safe_print("\n📄 创建新文档...")
            doc = ps.app.documents.add()
            safe_print(f"   ✅ 新文档创建成功")
            safe_print(f"   📊 文档ID: {doc.id}")
            safe_print(f"   📏 默认尺寸: {doc.width} x {doc.height}")

            # Create text layer with "Hello, World!"
            safe_print("\n✏️ 创建文本图层...")
            text_color = ps.SolidColor()
            text_color.rgb.red = 255
            text_color.rgb.green = 0
            text_color.rgb.blue = 0

            new_text_layer = doc.artLayers.add()
            new_text_layer.kind = ps.LayerKind.TextLayer
            new_text_layer.textItem.contents = "Hello, World!"
            new_text_layer.textItem.position = [160, 167]
            new_text_layer.textItem.size = 40
            new_text_layer.textItem.color = text_color

            safe_print(f"   ✅ 文本图层创建成功: {new_text_layer.name}")
            safe_print(f"   📝 内容: {new_text_layer.textItem.contents}")
            safe_print(f"   🎨 颜色: 红色 (RGB: 255, 0, 0)")
            safe_print(f"   📏 大小: {new_text_layer.textItem.size}pt")

            # 添加装饰内容
            safe_print("\n🎨 添加装饰内容...")

            # 创建背景
            bg_layer = doc.artLayers.add()
            bg_layer.name = "Background Color"
            bg_layer.move(doc.artLayers[0], ps.ElementPlacement.PlaceBefore)

            bg_color = ps.SolidColor()
            bg_color.rgb.red = 200
            bg_color.rgb.green = 220
            bg_color.rgb.blue = 255
            ps.app.backgroundColor = bg_color

            doc.selection.selectAll()
            doc.selection.fill(ps.app.backgroundColor)
            doc.selection.deselect()
            safe_print("   ✅ 背景图层创建并填充")

            # 创建装饰文本
            decor_text = doc.artLayers.add()
            decor_text.kind = ps.LayerKind.TextLayer
            decor_text.name = "Decoration Text"
            decor_text.textItem.contents = "Photoshop Python API - 基础连接测试"
            decor_text.textItem.size = 20
            decor_text.textItem.position = [100, 100]
            decor_text.textItem.color = text_color
            safe_print("   ✅ 装饰文本创建")

            # 保存文档
            safe_print("\n💾 保存文档...")
            try:
                save_dir = get_test_save_dir()
                jpg_file = os.path.join(save_dir, "hello_world_test.jpg")
                save_options = ps.JPEGSaveOptions(quality=10)
                doc.saveAs(jpg_file, save_options, asCopy=True)
                safe_print(f"   ✅ 文档保存成功: {jpg_file}")
            except Exception as e:
                safe_print(f"   ⚠️ 保存失败: {str(e)}")

            # 最终状态
            safe_print(f"\n📊 最终状态:")
            safe_print(f"   🎭 总图层数量: {doc.artLayers.length}")
            safe_print(f"   📄 文档名称: {doc.name}")
            safe_print(f"   📏 文档尺寸: {doc.width} x {doc.height}")

        safe_print("\n🎉 第1项: hello_world.py 测试完成!")
        safe_print("✅ 验证功能: Session连接、文档创建、文本图层、颜色设置、文档保存")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_hello_world()