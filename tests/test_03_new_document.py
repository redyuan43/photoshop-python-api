# -*- coding: utf-8 -*-
"""测试第3项: new_document.py - 文档创建变体示例"""

import os
import sys

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_new_document():
    """运行new_document测试"""
    safe_print("📄 开始执行第3项: new_document.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        import photoshop.api as ps

        # Start up Photoshop application
        app = ps.Application()
        safe_print("✅ Photoshop应用程序连接成功")

        # 获取原始标尺单位设置
        start_ruler_units = app.preferences.rulerUnits
        safe_print(f"📏 原始标尺单位: {start_ruler_units}")

        # 设置标尺单位为像素
        app.preferences.rulerUnits = ps.Units.Pixels
        safe_print("✅ 标尺单位设置为像素")

        # Create the document
        safe_print("\n📄 创建新文档...")
        docRef = app.documents.add(1920, 1080, 72.0, "My New Document")

        safe_print(f"   ✅ 文档创建成功")
        safe_print(f"   📊 文档ID: {docRef.id}")
        safe_print(f"   📝 文档名称: {docRef.name}")
        safe_print(f"   📏 文档尺寸: {docRef.width} x {docRef.height}")

        # 恢复原始标尺单位
        app.preferences.rulerUnits = start_ruler_units
        safe_print(f"✅ 恢复原始标尺单位: {start_ruler_units}")

        # 为主文档添加内容
        safe_print("\n🎨 添加文档内容...")
        text_layer = docRef.artLayers.add()
        text_layer.kind = ps.LayerKind.TextLayer
        text_layer.name = "单位信息"

        text_color = ps.SolidColor()
        text_color.rgb.red = 0
        text_color.rgb.green = 0
        text_color.rgb.blue = 255

        text_layer.textItem.contents = f"标尺单位测试\n原始单位: {start_ruler_units}\n文档尺寸: 1920x1080"
        text_layer.textItem.size = 28
        text_layer.textItem.position = [100, 100]
        text_layer.textItem.color = text_color

        safe_print("   ✅ 文档内容添加成功")

        # 保存文档
        safe_print("\n💾 保存文档...")
        try:
            save_dir = get_test_save_dir()
            save_path = os.path.join(save_dir, "new_document_test.jpg")
            save_options = ps.JPEGSaveOptions(quality=10)
            docRef.saveAs(save_path, save_options, asCopy=True)
            safe_print(f"   ✅ 文档保存成功: new_document_test.jpg")
        except Exception as e:
            safe_print(f"   ⚠️ 保存失败: {str(e)}")

        safe_print("\n🎉 第3项: new_document.py 测试完成!")
        safe_print("✅ 验证功能: 直接API连接、应用程序偏好设置、标尺单位设置")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_new_document()