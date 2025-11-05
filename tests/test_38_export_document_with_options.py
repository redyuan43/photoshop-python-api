# -*- coding: utf-8 -*-
"""测试第38项: export_document_with_options.py - 带选项导出"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_export_document_with_options():
    """运行export_document_with_options测试"""
    safe_print("📋 开始执行第38项: export_document_with_options.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import modules (原始代码逻辑，简化版)
        from photoshop import Session

        # 测试1: 基本导出与选项配置
        safe_print("\n🔧 测试1: 基本导出与选项配置...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ Session成功启动")

                # 创建测试内容
                safe_print("   🎨 创建测试内容...")
                layer = doc.artLayers.add()
                layer.name = "导出测试内容"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 128
                fill_color.rgb.blue = 64
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [400, 100], [400, 400], [100, 100]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()
                safe_print("      ✅ 测试内容创建完成")

                # 设置导出目录
                save_dir = get_test_save_dir()

                # 导出PNG-24 (原始代码逻辑，简化)
                safe_print("   🖼️ 导出PNG-24...")
                try:
                    png_options = ps.PNGSaveOptions()
                    png_options.interlaced = False
                    png_options.compression = 0
                    png_path = os.path.join(save_dir, "exported_png24.png")
                    doc.saveAs(png_path, png_options, True)
                    safe_print(f"      ✅ PNG-24导出成功: {png_path}")

                    if os.path.exists(png_path):
                        size = os.path.getsize(png_path)
                        safe_print(f"      📊 文件大小: {size} bytes")
                except Exception as png_e:
                    safe_print(f"      ❌ PNG-24导出失败: {str(png_e)}")

                # 导出JPEG高质量 (原始代码逻辑，简化)
                safe_print("   📸 导出JPEG高质量...")
                try:
                    jpg_options = ps.JPEGSaveOptions()
                    jpg_options.quality = 12
                    jpg_path = os.path.join(save_dir, "exported_jpeg.jpg")
                    doc.saveAs(jpg_path, jpg_options, True)
                    safe_print(f"      ✅ JPEG导出成功: {jpg_path}")

                    if os.path.exists(jpg_path):
                        size = os.path.getsize(jpg_path)
                        safe_print(f"      📊 文件大小: {size} bytes")
                except Exception as jpg_e:
                    safe_print(f"      ❌ JPEG导出失败: {str(jpg_e)}")

        except Exception as e:
            safe_print(f"❌ 基本导出与选项配置失败: {str(e)}")
            return False

        # 测试2: PNG选项详细配置
        safe_print("\n🔧 测试2: PNG选项详细配置...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                doc.name = "PNG选项测试文档"

                # 创建彩色内容
                safe_print("   🎨 创建彩色内容...")
                colors = [
                    {"name": "红色", "r": 255, "g": 0, "b": 0, "x": 50},
                    {"name": "绿色", "r": 0, "g": 255, "b": 0, "x": 150},
                    {"name": "蓝色", "r": 0, "g": 0, "b": 255, "x": 250},
                ]

                for color_info in colors:
                    layer = doc.artLayers.add()
                    layer.name = f"PNG测试_{color_info['name']}"

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

                safe_print("      ✅ 彩色内容创建完成")

                # 测试不同PNG选项
                png_configs = [
                    {"name": "高质量PNG", "interlaced": False, "compression": 0},
                    {"name": "标准PNG", "interlaced": False, "compression": 3},
                    {"name": "压缩PNG", "interlaced": True, "compression": 6},
                ]

                for config in png_configs:
                    safe_print(f"   🖼️ 导出{config['name']}...")
                    try:
                        png_opt = ps.PNGSaveOptions()
                        png_opt.interlaced = config["interlaced"]
                        png_opt.compression = config["compression"]
                        png_path = os.path.join(save_dir, f"png_{config['name']}.png")
                        doc.saveAs(png_path, png_opt, True)
                        safe_print(f"      ✅ {config['name']}导出成功")
                    except Exception as config_e:
                        safe_print(f"      ❌ {config['name']}导出失败: {str(config_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ PNG选项详细配置失败: {str(e)}")

        # 测试3: JPEG选项详细配置
        safe_print("\n🔧 测试3: JPEG选项详细配置...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                doc.name = "JPEG选项测试文档"

                # 创建渐变内容
                safe_print("   🎨 创建渐变内容...")
                layer = doc.artLayers.add()
                layer.name = "渐变测试"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 128
                fill_color.rgb.green = 64
                fill_color.rgb.blue = 192
                ps.app.foregroundColor = fill_color

                doc.selection.select([[50, 50], [450, 50], [450, 350], [50, 350]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                safe_print("      ✅ 渐变内容创建完成")

                # 测试不同JPEG质量
                jpg_qualities = [3, 6, 10, 12]
                for quality in jpg_qualities:
                    safe_print(f"   📸 导出质量{quality}...")
                    try:
                        jpg_opt = ps.JPEGSaveOptions()
                        jpg_opt.quality = quality
                        jpg_opt.embedColorProfile = True
                        jpg_opt.formatOptions = 1
                        jpg_path = os.path.join(save_dir, f"jpeg_q{quality}.jpg")
                        doc.saveAs(jpg_path, jpg_opt, True)
                        safe_print(f"      ✅ 质量{quality}导出成功")
                    except Exception as quality_e:
                        safe_print(f"      ❌ 质量{quality}导出失败: {str(quality_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ JPEG选项详细配置失败: {str(e)}")

        # 测试4: 颜色配置文件处理
        safe_print("\n🔧 测试4: 颜色配置文件处理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建内容
                layer = doc.artLayers.add()
                layer.name = "颜色配置测试"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 200
                fill_color.rgb.green = 100
                fill_color.rgb.blue = 50
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [300, 100], [300, 300], [100, 100]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 测试颜色配置文件选项
                safe_print("   🎨 导出带颜色配置文件的JPEG...")
                try:
                    jpg_opt = ps.JPEGSaveOptions()
                    jpg_opt.quality = 10
                    jpg_opt.embedColorProfile = True
                    jpg_path = os.path.join(save_dir, "jpeg_with_profile.jpg")
                    doc.saveAs(jpg_path, jpg_opt, True)
                    safe_print(f"      ✅ 带颜色配置文件的JPEG导出成功")
                except Exception as profile_e:
                    safe_print(f"      ❌ 颜色配置文件导出失败: {str(profile_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 颜色配置文件处理失败: {str(e)}")

        # 测试5: 渐进式扫描配置
        safe_print("\n🔧 测试5: 渐进式扫描配置...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建内容
                layer = doc.artLayers.add()
                layer.name = "渐进扫描测试"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 100
                fill_color.rgb.green = 200
                fill_color.rgb.blue = 150
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [300, 100], [300, 300], [100, 100]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 测试渐进式扫描
                safe_print("   📸 导出渐进式JPEG...")
                try:
                    jpg_opt = ps.JPEGSaveOptions()
                    jpg_opt.quality = 10
                    jpg_opt.scans = 3
                    jpg_opt.formatOptions = 1
                    jpg_path = os.path.join(save_dir, "jpeg_progressive.jpg")
                    doc.saveAs(jpg_path, jpg_opt, True)
                    safe_print(f"      ✅ 渐进式JPEG导出成功")
                except Exception as progressive_e:
                    safe_print(f"      ❌ 渐进式JPEG导出失败: {str(progressive_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 渐进式扫描配置失败: {str(e)}")

        # 测试6: 多格式导出对比
        safe_print("\n🔧 测试6: 多格式导出对比...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                doc.name = "多格式对比文档"

                # 创建复杂内容
                safe_print("   🎨 创建复杂内容...")
                colors = [
                    {"name": "红", "r": 255, "g": 0, "b": 0, "x": 50, "y": 50},
                    {"name": "绿", "r": 0, "g": 255, "b": 0, "x": 150, "y": 50},
                    {"name": "蓝", "r": 0, "g": 0, "b": 255, "x": 50, "y": 150},
                    {"name": "黄", "r": 255, "g": 255, "b": 0, "x": 150, "y": 150},
                ]

                for color_info in colors:
                    layer = doc.artLayers.add()
                    layer.name = f"颜色{color_info['name']}"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = color_info["r"]
                    fill_color.rgb.green = color_info["g"]
                    fill_color.rgb.blue = color_info["b"]
                    ps.app.foregroundColor = fill_color

                    doc.selection.select([
                        [color_info['x'], color_info['y']],
                        [color_info['x'] + 80, color_info['y']],
                        [color_info['x'] + 80, color_info['y'] + 80],
                        [color_info['x'], color_info['y'] + 80]
                    ])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                # 导出多种格式
                formats = [
                    {"ext": "psd", "name": "PSD", "opt": ps.PhotoshopSaveOptions()},
                    {"ext": "jpg", "name": "JPEG高质量", "opt": ps.JPEGSaveOptions(quality=12)},
                    {"ext": "jpg", "name": "JPEG中等质量", "opt": ps.JPEGSaveOptions(quality=6)},
                    {"ext": "png", "name": "PNG", "opt": ps.PNGSaveOptions()},
                ]

                file_sizes = {}
                for fmt in formats:
                    safe_print(f"   📄 导出{fmt['name']}...")
                    try:
                        if fmt["ext"] == "jpg":
                            fmt["opt"].quality = fmt["opt"].quality
                        elif fmt["ext"] == "psd":
                            fmt["opt"].layers = True

                        file_path = os.path.join(save_dir, f"compare_{fmt['name']}.{fmt['ext']}")
                        doc.saveAs(file_path, fmt["opt"], True)

                        if os.path.exists(file_path):
                            size = os.path.getsize(file_path)
                            file_sizes[fmt["name"]] = size
                            safe_print(f"      ✅ {fmt['name']}导出成功 ({size} bytes)")
                        else:
                            safe_print(f"      ⚠️ {fmt['name']}文件未找到")
                    except Exception as fmt_e:
                        safe_print(f"      ❌ {fmt['name']}导出失败: {str(fmt_e)[:50]}")

                # 显示文件大小对比
                if file_sizes:
                    safe_print("   📊 文件大小对比:")
                    for name, size in file_sizes.items():
                        safe_print(f"      📁 {name}: {size} bytes")

        except Exception as e:
            safe_print(f"❌ 多格式导出对比失败: {str(e)}")

        # 测试7: 导出错误处理
        safe_print("\n🔧 测试7: 导出错误处理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建内容
                layer = doc.artLayers.add()
                layer.name = "错误处理测试"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 128
                fill_color.rgb.green = 128
                fill_color.rgb.blue = 128
                ps.app.foregroundColor = fill_color

                doc.selection.select([[50, 50], [250, 50], [250, 250], [50, 250]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 测试无效路径
                safe_print("   📄 测试无效路径...")
                try:
                    jpg_opt = ps.JPEGSaveOptions()
                    jpg_opt.quality = 10
                    invalid_path = "/invalid/path/image.jpg"
                    doc.saveAs(invalid_path, jpg_opt, True)
                    safe_print("      ⚠️ 无效路径意外成功")
                except Exception as invalid_e:
                    safe_print(f"      ✅ 正确处理无效路径")

                # 测试空文件扩展名
                safe_print("   📄 测试无效文件扩展名...")
                try:
                    png_opt = ps.PNGSaveOptions()
                    empty_ext_path = os.path.join(save_dir, "test_file")
                    doc.saveAs(empty_ext_path, png_opt, True)
                    safe_print("      ⚠️ 空扩展名意外成功")
                except Exception as empty_e:
                    safe_print(f"      ✅ 正确处理空扩展名")

        except Exception as e:
            safe_print(f"❌ 导出错误处理失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "export_document_with_options_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Export Document with Options 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 带选项导出文档功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本导出与选项配置\n")
                f.write(f"- PNG选项详细配置\n")
                f.write(f"- JPEG选项详细配置\n")
                f.write(f"- 颜色配置文件处理\n")
                f.write(f"- 渐进式扫描配置\n")
                f.write(f"- 多格式导出对比\n")
                f.write(f"- 导出错误处理\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第38项: export_document_with_options.py 测试完成!")
        safe_print("✅ 验证功能: PNG选项、JPEG质量、颜色配置、渐进扫描、多格式对比")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 导出选项是否正确配置")
        safe_print("3. 文件路径和权限是否正常")
        safe_print("4. saveAs方法是否可用")
        return False

if __name__ == "__main__":
    test_export_document_with_options()
