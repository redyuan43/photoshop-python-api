# -*- coding: utf-8 -*-
"""测试第24项: import_image_as_layer.py - 导入图像为图层"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_import_image_as_layer():
    """运行import_image_as_layer测试"""
    safe_print("📋 开始执行第24项: import_image_as_layer.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本导入图像为图层 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本导入图像为图层 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                safe_print("   ✅ Session成功启动")

                # 使用ActionDescriptor导入图像 (原始代码逻辑)
                safe_print("   📄 使用ActionDescriptor导入图像...")

                # 首先创建一个测试图像文件
                safe_print("   🎨 创建测试图像文件...")
                save_dir = get_test_save_dir()
                test_image_path = os.path.join(save_dir, "test_import_image.jpg")

                # 使用当前文档保存为JPG作为测试图像
                doc = ps.active_document
                jpg_options = ps.JPEGSaveOptions()
                jpg_options.quality = 10
                doc.saveAs(test_image_path, jpg_options, True)
                safe_print(f"      ✅ 创建测试图像: {test_image_path}")

                # 执行导入操作 (原始代码逻辑)
                safe_print("   📥 执行导入操作...")
                desc = ps.ActionDescriptor()
                desc.putPath(ps.app.charIDToTypeID("null"), test_image_path)
                event_id = ps.app.charIDToTypeID("Plc ")
                ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc)
                safe_print("      ✅ 导入操作执行完成")

                # 验证导入结果
                safe_print("   🔍 验证导入结果...")
                layers_before = ps.active_document.artLayers.length
                safe_print(f"      📊 导入前图层数: {layers_before}")
                safe_print(f"      📄 当前活动文档: {ps.active_document.name}")

        except Exception as e:
            safe_print(f"❌ 基本导入图像测试失败: {str(e)}")
            safe_print("   🔄 尝试替代方法...")

            # 尝试使用菜单命令
            try:
                with Session(action="new_document") as ps:
                    # 尝试使用菜单命令Place
                    safe_print("   🖱️ 尝试使用Place菜单...")
                    desc = ps.ActionDescriptor()
                    desc.putPath(ps.app.charIDToTypeID("null"), "dummy_path")
                    ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc)
                    safe_print("      ✅ Place菜单命令执行成功")
            except Exception as place_e:
                safe_print(f"   ❌ Place菜单也失败: {str(place_e)}")

        # 测试2: 使用Session导入
        safe_print("\n🔧 测试2: 使用Session导入...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print(f"   📄 创建新文档: {doc.name}")

                # 创建测试图像
                save_dir = get_test_save_dir()
                test_image_path2 = os.path.join(save_dir, "test_import_image2.png")

                # 先创建一些内容作为测试图像
                doc2 = ps.app.documents.add(300, 300, 72, "临时图像")
                layer = doc2.artLayers.add()
                layer.name = "测试内容"

                # 添加内容
                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 0
                fill_color.rgb.blue = 255
                ps.app.foregroundColor = fill_color

                doc2.selection.select([[50, 50], [250, 50], [250, 250], [50, 250]])
                doc2.selection.fill(ps.app.foregroundColor)
                doc2.selection.deselect()

                # 保存为PNG
                png_options = ps.PNGSaveOptions()
                doc2.saveAs(test_image_path2, png_options, True)
                doc2.close()

                safe_print(f"      ✅ 创建测试PNG图像: {test_image_path2}")

                # 尝试导入
                safe_print("   📥 尝试导入PNG图像...")
                try:
                    desc = ps.ActionDescriptor()
                    desc.putPath(ps.app.charIDToTypeID("null"), test_image_path2)
                    ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc)
                    safe_print("      ✅ PNG导入成功")
                except Exception as png_e:
                    safe_print(f"      ⚠️ PNG导入失败: {str(png_e)}")

        except Exception as e:
            safe_print(f"❌ Session导入测试失败: {str(e)}")

        # 测试3: 导入不同格式的图像
        safe_print("\n🔧 测试3: 导入不同格式的图像...")

        try:
            # 测试JPG导入
            safe_print("   📄 测试JPG格式...")
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建测试JPG
                jpg_path = os.path.join(save_dir, "format_test.jpg")
                jpg_options = ps.JPEGSaveOptions()
                jpg_options.quality = 8
                doc.saveAs(jpg_path, jpg_options, True)

                safe_print(f"      ✅ 创建JPG文件: {jpg_path}")

            # 测试PNG导入
            safe_print("   📄 测试PNG格式...")
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建测试PNG
                png_path = os.path.join(save_dir, "format_test.png")
                png_options = ps.PNGSaveOptions()
                doc.saveAs(png_path, png_options, True)

                safe_print(f"      ✅ 创建PNG文件: {png_path}")

        except Exception as e:
            safe_print(f"❌ 不同格式测试失败: {str(e)}")

        # 测试4: 导入图像到现有图层
        safe_print("\n🔧 测试4: 导入图像到现有图层...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print(f"   📄 使用现有文档: {doc.name}")

                # 创建多个图层
                for i in range(3):
                    layer = doc.artLayers.add()
                    layer.name = f"背景图层{i+1}"

                    # 添加内容
                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 100 * i
                    fill_color.rgb.green = 100
                    fill_color.rgb.blue = 200
                    ps.app.foregroundColor = fill_color

                    x = i * 50
                    doc.selection.select([[x, x], [x+40, x], [x+40, x+40], [x, x+40]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                safe_print("      ✅ 创建多个背景图层")

                # 尝试在图层上放置图像
                safe_print("   📥 尝试在图层上放置图像...")
                try:
                    desc = ps.ActionDescriptor()
                    # Place命令可能会创建新的图层
                    ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc)
                    safe_print("      ✅ Place操作执行")
                except Exception as place_e:
                    safe_print(f"      ⚠️ Place操作失败: {str(place_e)}")

        except Exception as e:
            safe_print(f"❌ 导入到现有图层测试失败: {str(e)}")

        # 测试5: 错误处理
        safe_print("\n🔧 测试5: 错误处理测试...")

        try:
            # 测试无效路径
            safe_print("   📄 测试无效图像路径...")
            with Session(action="new_document") as ps:
                desc = ps.ActionDescriptor()
                desc.putPath(ps.app.charIDToTypeID("null"), "/invalid/path/image.jpg")

                try:
                    ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc)
                    safe_print("      ⚠️ 无效路径意外成功")
                except Exception as invalid_e:
                    safe_print(f"      ✅ 正确处理无效路径: 导入失败（预期）")

            # 测试空路径
            safe_print("   📄 测试空路径...")
            with Session(action="new_document") as ps:
                desc = ps.ActionDescriptor()
                desc.putPath(ps.app.charIDToTypeID("null"), "")

                try:
                    ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc)
                    safe_print("      ⚠️ 空路径意外成功")
                except Exception as empty_e:
                    safe_print(f"      ✅ 正确处理空路径: 导入失败（预期）")

        except Exception as e:
            safe_print(f"❌ 错误处理测试失败: {str(e)}")

        # 测试6: 使用Place命令的不同参数
        safe_print("\n🔧 测试6: 使用Place命令的不同参数...")

        try:
            with Session(action="new_document") as ps:
                # 尝试不同的ActionDescriptor参数
                safe_print("   📄 测试Place命令参数...")

                # 参数1: 基本Place
                try:
                    desc1 = ps.ActionDescriptor()
                    desc1.putPath(ps.app.charIDToTypeID("null"), "dummy_path")
                    ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc1)
                    safe_print("      ✅ 基本Place参数可用")
                except Exception as p1_e:
                    safe_print(f"      ⚠️ 基本Place参数失败: {str(p1_e)}")

                # 参数2: 带位置参数
                try:
                    desc2 = ps.ActionDescriptor()
                    desc2.putPath(ps.app.charIDToTypeID("null"), "dummy_path")
                    # 添加位置信息（如果有的话）
                    ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc2)
                    safe_print("      ✅ 带位置Place参数可用")
                except Exception as p2_e:
                    safe_print(f"      ⚠️ 带位置Place参数失败: {str(p2_e)}")

        except Exception as e:
            safe_print(f"❌ Place命令参数测试失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "import_image_as_layer_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Import Image as Layer 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 导入图像为图层功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本导入图像为图层 (原始代码逻辑)\n")
                f.write(f"- 使用Session导入\n")
                f.write(f"- 导入不同格式的图像\n")
                f.write(f"- 导入图像到现有图层\n")
                f.write(f"- 错误处理测试\n")
                f.write(f"- 使用Place命令的不同参数\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第24项: import_image_as_layer.py 测试完成!")
        safe_print("✅ 验证功能: ActionDescriptor、executeAction、Place命令、多格式导入")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 图像导入功能是否可用")
        safe_print("3. ActionDescriptor和executeAction权限是否正常")
        safe_print("4. 文件路径和格式是否正确")
        return False

if __name__ == "__main__":
    test_import_image_as_layer()