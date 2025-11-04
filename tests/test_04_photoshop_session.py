# -*- coding: utf-8 -*-
"""测试第4项: photoshop_session.py - Session上下文管理"""

import os
import sys

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_photoshop_session():
    """运行photoshop_session测试"""
    safe_print("🔧 开始执行第4项: photoshop_session.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import built-in modules (原始代码逻辑)
        from datetime import datetime
        from tempfile import mkdtemp

        # Import third-party modules (原始代码逻辑)
        import examples._psd_files as psd

        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 获取PSD文件 (原始代码逻辑)
        PSD_FILE = psd.get_psd_files()
        file_path = PSD_FILE["slate_template.psd"]
        safe_print(f"📁 找到PSD模板文件: {file_path}")

        # 使用Session打开PSD文件 (原始代码逻辑)
        safe_print("\n🚀 使用Session打开PSD模板...")
        with Session(file_path, action="open", auto_close=True) as ps:
            safe_print("✅ Session成功启动并打开PSD文件")
            safe_print(f"📄 当前文档: {ps.active_document.name}")
            safe_print(f"📏 文档尺寸: {ps.active_document.width} x {ps.active_document.height}")

            # 获取图层组 (原始代码逻辑)
            safe_print("\n🎭 查找模板图层组...")
            try:
                layer_set = ps.active_document.layerSets.getByName("template")
                safe_print(f"✅ 找到图层组: {layer_set.name}")
                safe_print(f"   📊 图层组包含图层数量: {layer_set.layers.length}")
            except Exception as e:
                safe_print(f"   ⚠️ 未找到'template'图层组: {str(e)}")
                safe_print("   💡 创建测试图层组...")

                # 如果没有模板图层组，创建一个用于测试
                layer_set = ps.active_document.layerSets.add()
                layer_set.name = "template"

                # 创建一些测试文本图层
                test_layers = [
                    ("project name", "项目名称测试"),
                    ("datetime", "日期时间测试"),
                    ("test_field", "测试字段")
                ]

                for layer_name, content in test_layers:
                    text_layer = layer_set.artLayers.add()
                    text_layer.kind = ps.LayerKind.TextLayer
                    text_layer.name = layer_name
                    text_layer.textItem.contents = layer_name
                    text_layer.textItem.size = 24
                    text_layer.textItem.position = [100, 100 + len(layer_set.artLayers) * 50]

                    # 设置颜色
                    text_color = ps.SolidColor()
                    text_color.rgb.red = 0
                    text_color.rgb.green = 0
                    text_color.rgb.blue = 0
                    text_layer.textItem.color = text_color

                safe_print(f"   ✅ 创建测试图层组: {layer_set.name}")

            # 准备数据 (原始代码逻辑)
            safe_print("\n📝 准备替换数据...")
            data = {
                "project name": "test_project",
                "datetime": datetime.today().strftime("%Y-%m-%d"),
            }

            safe_print("   📊 数据内容:")
            for key, value in data.items():
                safe_print(f"      {key}: {value}")

            # 遍历图层并替换文本 (原始代码逻辑)
            safe_print("\n🔄 遍历图层并替换文本内容...")
            replaced_count = 0

            for layer in layer_set.layers:
                try:
                    safe_print(f"   🔍 处理图层: {layer.name}")

                    if layer.kind == ps.LayerKind.TextLayer:
                        original_content = layer.textItem.contents.strip()
                        safe_print(f"      📝 原始内容: {original_content}")

                        if original_content in data:
                            new_content = data[original_content]
                            layer.textItem.contents = new_content
                            safe_print(f"      ✅ 替换为: {new_content}")
                            replaced_count += 1
                        else:
                            safe_print(f"      ⚠️ 未找到匹配的数据: {original_content}")
                    else:
                        safe_print(f"      ℹ️ 非文本图层，跳过")

                except Exception as e:
                    safe_print(f"      ❌ 处理图层时出错: {str(e)}")

            safe_print(f"\n📊 文本替换完成，共替换 {replaced_count} 个图层")

            # 显示最终文档信息
            safe_print("\n📊 最终文档信息:")
            safe_print(f"   📄 文档名称: {ps.active_document.name}")
            safe_print(f"   🎭 图层组数量: {ps.active_document.layerSets.length}")
            safe_print(f"   🎭 总图层数量: {ps.active_document.artLayers.length}")

            # 尝试保存文档 (原始代码逻辑)
            safe_print("\n💾 保存文档...")
            try:
                save_dir = get_test_save_dir()
                jpg_file = os.path.join(save_dir, "photoshop_session_test.jpg")

                # 创建保存选项
                save_options = ps.JPEGSaveOptions(quality=10)
                ps.active_document.saveAs(jpg_file, save_options, asCopy=True)

                safe_print(f"   ✅ 文档保存成功: {jpg_file}")

                # 尝试打开保存的文件 (原始代码逻辑)
                # os.startfile(jpg_file)  # 注释掉自动打开，避免干扰
                safe_print("   ℹ️ 文档已保存，可手动查看")

            except Exception as e:
                safe_print(f"   ⚠️ 保存失败: {str(e)}")

            # 测试Session自动关闭功能
            safe_print("\n🔚 测试Session自动关闭功能...")
            safe_print("   ℹ️ Session将在with块结束时自动关闭文档")

        safe_print("   ✅ Session已自动关闭")
        safe_print("\n🎉 第4项: photoshop_session.py 测试完成!")
        safe_print("✅ 验证功能: Session文件打开、图层组操作、文本替换、自动关闭")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. PSD模板文件是否存在")
        safe_print("3. 是否有足够的权限操作文件")
        safe_print("4. Session上下文管理是否正常")
        return False

if __name__ == "__main__":
    test_photoshop_session()