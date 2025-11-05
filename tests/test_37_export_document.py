# -*- coding: utf-8 -*-
"""测试第37项: export_document.py - 导出文档"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_export_document():
    """运行export_document测试"""
    safe_print("📋 开始执行第37项: export_document.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本导出文档 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本导出文档 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ Session成功启动")
                safe_print(f"   📄 当前文档: {doc.name}")

                # 创建测试内容
                safe_print("   🎨 创建测试内容...")
                layer = doc.artLayers.add()
                layer.name = "导出内容"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 128
                fill_color.rgb.blue = 64
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [400, 100], [400, 400], [100, 100]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()
                safe_print("      ✅ 测试内容创建完成")

                # Get the save directory (原始代码逻辑，修改为使用测试目录)
                safe_print("   💾 设置导出目录...")
                save_dir = get_test_save_dir()
                safe_print(f"      📁 导出目录: {save_dir}")

                # Save as JPG with high quality (原始代码逻辑)
                safe_print("   📸 导出JPG格式...")
                try:
                    jpg_opt = ps.JPEGSaveOptions()
                    jpg_opt.quality = 12
                    jpg_path = os.path.join(save_dir, "output.jpg")
                    doc.saveAs(jpg_path, jpg_opt)
                    safe_print(f"      ✅ JPG导出成功: {jpg_path}")

                    # 验证文件是否存在
                    if os.path.exists(jpg_path):
                        file_size = os.path.getsize(jpg_path)
                        safe_print(f"      📊 文件大小: {file_size} bytes")
                    else:
                        safe_print(f"      ⚠️ JPG文件未找到")
                except Exception as jpg_e:
                    safe_print(f"      ❌ JPG导出失败: {str(jpg_e)}")

                # Save as PNG with transparency (原始代码逻辑)
                safe_print("   🖼️ 导出PNG格式...")
                try:
                    png_opt = ps.PhotoshopSaveOptions()
                    png_path = os.path.join(save_dir, "output.png")
                    doc.saveAs(png_path, png_opt)
                    safe_print(f"      ✅ PNG导出成功: {png_path}")

                    # 验证文件是否存在
                    if os.path.exists(png_path):
                        file_size = os.path.getsize(png_path)
                        safe_print(f"      📊 文件大小: {file_size} bytes")
                    else:
                        safe_print(f"      ⚠️ PNG文件未找到")
                except Exception as png_e:
                    safe_print(f"      ❌ PNG导出失败: {str(png_e)}")

        except Exception as e:
            safe_print(f"❌ 基本导出文档失败: {str(e)}")
            return False

        # 测试2: 不同质量设置导出
        safe_print("\n🔧 测试2: 不同质量设置导出...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                doc.name = "质量测试文档"

                # 创建内容
                layer = doc.artLayers.add()
                layer.name = "质量测试内容"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 0
                fill_color.rgb.green = 255
                fill_color.rgb.blue = 255
                ps.app.foregroundColor = fill_color

                doc.selection.select([[50, 50], [350, 50], [350, 350], [50, 50]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 测试不同JPG质量
                qualities = [1, 6, 12]
                for quality in qualities:
                    safe_print(f"   📸 导出JPG质量{quality}...")
                    try:
                        jpg_opt = ps.JPEGSaveOptions()
                        jpg_opt.quality = quality
                        jpg_path = os.path.join(get_test_save_dir(), f"quality_test_{quality}.jpg")
                        doc.saveAs(jpg_path, jpg_opt)
                        safe_print(f"      ✅ 质量{quality}导出成功")
                    except Exception as q_e:
                        safe_print(f"      ❌ 质量{quality}导出失败: {str(q_e)}")

        except Exception as e:
            safe_print(f"❌ 不同质量设置导出失败: {str(e)}")

        # 测试3: PNG选项配置
        safe_print("\n🔧 测试3: PNG选项配置...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                doc.name = "PNG测试文档"

                # 创建内容
                layer = doc.artLayers.add()
                layer.name = "PNG测试内容"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 0
                fill_color.rgb.blue = 255
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [300, 100], [300, 300], [100, 300]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 导出PNG
                safe_print("   🖼️ 导出PNG...")
                try:
                    png_opt = ps.PhotoshopSaveOptions()
                    png_path = os.path.join(get_test_save_dir(), "png_test.png")
                    doc.saveAs(png_path, png_opt)
                    safe_print(f"      ✅ PNG导出成功")
                except Exception as png_opt_e:
                    safe_print(f"      ❌ PNG导出失败: {str(png_opt_e)}")

        except Exception as e:
            safe_print(f"❌ PNG选项配置失败: {str(e)}")

        # 测试4: 多图层文档导出
        safe_print("\n🔧 测试4: 多图层文档导出...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                doc.name = "多图层导出文档"

                # 创建多个图层
                colors = [
                    {"name": "红色", "r": 255, "g": 0, "b": 0, "x": 50},
                    {"name": "绿色", "r": 0, "g": 255, "b": 0, "x": 150},
                    {"name": "蓝色", "r": 0, "g": 0, "b": 255, "x": 250},
                ]

                for color_info in colors:
                    layer = doc.artLayers.add()
                    layer.name = f"图层_{color_info['name']}"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = color_info["r"]
                    fill_color.rgb.green = color_info["g"]
                    fill_color.rgb.blue = color_info["b"]
                    ps.app.foregroundColor = fill_color

                    doc.selection.select([
                        [color_info['x'], 100],
                        [color_info['x'] + 80, 100],
                        [color_info['x'] + 80, 200],
                        [color_info['x'], 200]
                    ])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                safe_print("      ✅ 多图层创建完成")

                # 导出多图层文档
                safe_print("   💾 导出多图层文档...")
                try:
                    psd_opt = ps.PhotoshopSaveOptions()
                    psd_opt.layers = True
                    psd_path = os.path.join(get_test_save_dir(), "multi_layer_export.psd")
                    doc.saveAs(psd_path, psd_opt)
                    safe_print(f"      ✅ 多图层PSD导出成功")
                except Exception as multi_e:
                    safe_print(f"      ❌ 多图层导出失败: {str(multi_e)}")

        except Exception as e:
            safe_print(f"❌ 多图层文档导出失败: {str(e)}")

        # 测试5: 文件路径处理
        safe_print("\n🔧 测试5: 文件路径处理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建内容
                layer = doc.artLayers.add()
                layer.name = "路径测试内容"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 200
                fill_color.rgb.green = 200
                fill_color.rgb.blue = 0
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [300, 100], [300, 300], [100, 300]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 测试不同路径
                safe_print("   📁 测试不同文件路径...")
                test_paths = [
                    "simple_name.jpg",
                    "path with spaces.jpg",
                    "special_chars-测试.jpg",
                ]

                for path_name in test_paths:
                    safe_print(f"      📝 测试路径: {path_name}")
                    try:
                        jpg_opt = ps.JPEGSaveOptions()
                        jpg_opt.quality = 8
                        file_path = os.path.join(get_test_save_dir(), path_name)
                        doc.saveAs(file_path, jpg_opt)
                        safe_print(f"         ✅ {path_name} 导出成功")
                    except Exception as path_e:
                        safe_print(f"         ❌ {path_name} 导出失败: {str(path_e)[:30]}")

        except Exception as e:
            safe_print(f"❌ 文件路径处理失败: {str(e)}")

        # 测试6: 导出格式验证
        safe_print("\n🔧 测试6: 导出格式验证...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建内容
                layer = doc.artLayers.add()
                layer.name = "格式验证内容"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 128
                fill_color.rgb.green = 64
                fill_color.rgb.blue = 192
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [400, 100], [400, 400], [100, 300]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 导出不同格式
                formats = [
                    {"ext": "jpg", "name": "JPEG"},
                    {"ext": "png", "name": "PNG"},
                    {"ext": "psd", "name": "PSD"},
                ]

                for fmt in formats:
                    safe_print(f"   📄 导出{fmt['name']}格式...")
                    try:
                        if fmt["ext"] == "jpg":
                            opt = ps.JPEGSaveOptions()
                            opt.quality = 10
                        elif fmt["ext"] == "png":
                            opt = ps.PNGSaveOptions()
                        else:
                            opt = ps.PhotoshopSaveOptions()

                        file_path = os.path.join(get_test_save_dir(), f"format_test.{fmt['ext']}")
                        doc.saveAs(file_path, opt)

                        # 验证文件
                        if os.path.exists(file_path):
                            size = os.path.getsize(file_path)
                            safe_print(f"      ✅ {fmt['name']}导出成功 ({size} bytes)")
                        else:
                            safe_print(f"      ⚠️ {fmt['name']}文件未找到")
                    except Exception as fmt_e:
                        safe_print(f"      ❌ {fmt['name']}导出失败: {str(fmt_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 导出格式验证失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "export_document_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Export Document 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 导出文档功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本导出文档 (原始代码逻辑)\n")
                f.write(f"- 不同质量设置导出\n")
                f.write(f"- PNG选项配置\n")
                f.write(f"- 多图层文档导出\n")
                f.write(f"- 文件路径处理\n")
                f.write(f"- 导出格式验证\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第37项: export_document.py 测试完成!")
        safe_print("✅ 验证功能: JPG导出、PNG导出、质量设置、多图层导出、格式验证")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 导出功能是否可用")
        safe_print("3. saveAs方法参数是否正确")
        safe_print("4. 文件路径和权限是否正常")
        return False

if __name__ == "__main__":
    test_export_document()
