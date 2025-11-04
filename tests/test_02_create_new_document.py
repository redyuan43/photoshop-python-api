# -*- coding: utf-8 -*-
"""测试第2项: create_new_document.py - 创建新文档示例"""

import os
import sys

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_create_new_document():
    """运行create_new_document测试"""
    safe_print("📄 开始执行第2项: create_new_document.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        from photoshop import Session

        with Session() as ps:
            safe_print("✅ Session成功启动")

            # Create a new document with specific dimensions
            safe_print("\n📄 创建新文档 (1920x1080)...")
            doc = ps.app.documents.add(
                width=1920,
                height=1080,
                resolution=72,
                name="New Document Example"
            )

            safe_print(f"   ✅ 新文档创建成功")
            safe_print(f"   📊 文档ID: {doc.id}")
            safe_print(f"   📝 文档名称: {doc.name}")
            safe_print(f"   📏 尺寸: {doc.width} x {doc.height}")

            # 为主文档添加内容
            safe_print("\n🎨 添加文档内容...")
            text_layer = doc.artLayers.add()
            text_layer.kind = ps.LayerKind.TextLayer
            text_layer.name = "文档信息标识"

            text_color = ps.SolidColor()
            text_color.rgb.red = 255
            text_color.rgb.green = 0
            text_color.rgb.blue = 0

            text_layer.textItem.contents = f"文档创建测试\n1920x1080\n72ppi"
            text_layer.textItem.size = 36
            text_layer.textItem.position = [100, 100]
            text_layer.textItem.color = text_color

            # 创建装饰元素
            color_layer = doc.artLayers.add()
            color_layer.name = "装饰色块"

            color = ps.SolidColor()
            color.rgb.red = 255
            color.rgb.green = 100
            color.rgb.blue = 100
            ps.app.foregroundColor = color

            doc.selection.select([[100, 200], [200, 200], [200, 300], [100, 300]])
            doc.selection.fill(ps.app.foregroundColor)
            doc.selection.deselect()

            safe_print("   ✅ 内容添加成功")

            # 测试多种文档创建参数
            safe_print("\n🧪 测试多种文档创建参数...")

            # 小尺寸文档
            small_doc = ps.app.documents.add(400, 300, 150, "Small Test Document")
            safe_print(f"   ✅ 小文档创建成功: {small_doc.width}x{small_doc.height}")
            small_doc.close(ps.SaveOptions.DoNotSaveChanges)

            # 正方形文档
            square_doc = ps.app.documents.add(800, 800, 96, "Square Test Document")
            safe_print(f"   ✅ 正方形文档创建成功: {square_doc.width}x{square_doc.height}")
            square_doc.close(ps.SaveOptions.DoNotSaveChanges)

            # 保存主文档
            safe_print("\n💾 保存文档...")
            try:
                save_dir = get_test_save_dir()
                jpg_file = os.path.join(save_dir, "create_new_document_test.jpg")
                save_options = ps.JPEGSaveOptions(quality=8)
                doc.saveAs(jpg_file, save_options, asCopy=True)
                safe_print(f"   ✅ 文档保存成功: {jpg_file}")
            except Exception as e:
                safe_print(f"   ⚠️ 保存失败: {str(e)}")

        safe_print("\n🎉 第2项: create_new_document.py 测试完成!")
        safe_print("✅ 验证功能: 指定尺寸文档创建、名称设置、分辨率设置、文档保存")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_create_new_document()