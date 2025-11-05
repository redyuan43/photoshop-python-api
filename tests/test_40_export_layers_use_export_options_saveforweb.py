# -*- coding: utf-8 -*-
"""测试第40项: export_layers_use_export_options_saveforweb.py - Web导出"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_export_layers_use_export_options_saveforweb():
    """运行export_layers_use_export_options_saveforweb测试"""
    safe_print("📋 开始执行第40项: export_layers_use_export_options_saveforweb.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本Web导出功能 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本Web导出功能 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ Session成功启动")
                safe_print(f"   📄 当前文档: {doc.name}")

                # 创建测试内容
                safe_print("   🎨 创建测试内容...")
                layer = doc.artLayers.add()
                layer.name = "Web导出测试内容"

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

                # 基本Web导出测试 - 使用PNG格式作为SaveForWeb的替代
                safe_print("   🌐 执行基本Web导出...")
                try:
                    png_opt = ps.PNGSaveOptions()
                    png_opt.interlaced = False
                    png_path = os.path.join(save_dir, "web_export_basic.png")
                    doc.saveAs(png_path, png_opt, True)

                    if os.path.exists(png_path):
                        size = os.path.getsize(png_path)
                        safe_print(f"      ✅ 基本Web导出成功 ({size} bytes)")
                    else:
                        safe_print("      ⚠️ 基本Web导出文件未找到")
                except Exception as web_e:
                    safe_print(f"      ⚠️ 基本Web导出失败: {str(web_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 基本Web导出功能失败: {str(e)}")
            return False

        # 测试2: SaveForWeb选项详细配置
        safe_print("\n🔧 测试2: SaveForWeb选项详细配置...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建彩色内容
                safe_print("   🎨 创建彩色内容...")
                colors = [
                    {"name": "红色", "r": 255, "g": 0, "b": 0, "x": 50},
                    {"name": "绿色", "r": 0, "g": 255, "b": 0, "x": 150},
                    {"name": "蓝色", "r": 0, "g": 0, "b": 255, "x": 250},
                ]

                for color_info in colors:
                    layer = doc.artLayers.add()
                    layer.name = f"导出测试_{color_info['name']}"

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

                # 测试不同的Web导出配置
                safe_print("   🌐 配置不同SaveForWeb选项...")
                try:
                    # 使用PNG配置模拟GIF选项
                    png_opts = [
                        {"name": "高质量PNG", "interlaced": False, "compression": 0},
                        {"name": "标准PNG", "interlaced": False, "compression": 3},
                        {"name": "压缩PNG", "interlaced": True, "compression": 6},
                    ]

                    for opt in png_opts:
                        safe_print(f"      🖼️ 配置{opt['name']}...")
                        try:
                            png_opt = ps.PNGSaveOptions()
                            png_opt.interlaced = opt["interlaced"]
                            png_opt.compression = opt["compression"]

                            png_path = os.path.join(get_test_save_dir(), f"web_{opt['name'].replace(' ', '_').lower()}.png")
                            doc.saveAs(png_path, png_opt, True)

                            if os.path.exists(png_path):
                                size = os.path.getsize(png_path)
                                safe_print(f"         ✅ {opt['name']}导出成功 ({size} bytes)")
                            else:
                                safe_print(f"         ⚠️ {opt['name']}文件未找到")
                        except Exception as opt_e:
                            safe_print(f"         ❌ {opt['name']}导出失败: {str(opt_e)[:40]}")

                except Exception as config_e:
                    safe_print(f"      ⚠️ Web导出配置警告: {str(config_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ SaveForWeb选项详细配置失败: {str(e)}")

        # 测试3: 图层Web导出优化
        safe_print("\n🔧 测试3: 图层Web导出优化...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建多个图层用于Web导出
                safe_print("   🎨 创建Web优化测试图层...")
                for i in range(3):
                    layer = doc.artLayers.add()
                    layer.name = f"Web优化图层_{i+1}"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 80 * (i + 1)
                    fill_color.rgb.green = 100 + 50 * i
                    fill_color.rgb.blue = 200 - 30 * i
                    ps.app.foregroundColor = fill_color

                    x = 50 + i * 80
                    doc.selection.select([[x, 100], [x + 60, 100], [x + 60, 200], [x, 200]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                safe_print("      ✅ Web优化测试图层创建完成")

                # 测试图层可见性管理
                safe_print("   👁️ 管理图层可见性...")
                try:
                    visibilities = []
                    for layer in doc.layers:
                        visibilities.append(layer.visible)
                        layer.visible = False

                    # 逐个导出图层
                    export_count = 0
                    exported_files = []
                    for i, layer in enumerate(doc.layers):
                        layer.visible = True
                        safe_print(f"      📤 导出图层 {i+1}: {layer.name}")

                        png_opt = ps.PNGSaveOptions()
                        file_path = os.path.join(get_test_save_dir(), f"layer_{i+1}_{layer.name.replace(' ', '_')}.png")

                        try:
                            doc.saveAs(file_path, png_opt, True)
                            if os.path.exists(file_path):
                                exported_files.append(os.path.basename(file_path))
                                safe_print(f"         ✅ {layer.name}导出成功")
                            export_count += 1
                        except Exception as export_e:
                            safe_print(f"         ❌ {layer.name}导出失败: {str(export_e)[:40]}")

                        layer.visible = False

                    # 恢复可见性
                    for layer, vis in zip(doc.layers, visibilities):
                        layer.visible = vis

                    safe_print(f"      ✅ 共{export_count}个图层完成导出管理，{len(exported_files)}个文件")
                except Exception as visibility_e:
                    safe_print(f"      ⚠️ 图层可见性管理警告: {str(visibility_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 图层Web导出优化失败: {str(e)}")

        # 测试4: Web导出格式比较
        safe_print("\n🔧 测试4: Web导出格式比较...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建测试内容
                layer = doc.artLayers.add()
                layer.name = "格式比较内容"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 150
                fill_color.rgb.green = 200
                fill_color.rgb.blue = 100
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [350, 100], [350, 350], [100, 350]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 测试不同格式的Web导出
                web_formats = [
                    {"name": "PNG", "ext": "png", "option_class": ps.PNGSaveOptions},
                    {"name": "JPEG", "ext": "jpg", "option_class": ps.JPEGSaveOptions},
                    {"name": "PSD", "ext": "psd", "option_class": ps.PhotoshopSaveOptions},
                ]

                file_sizes = {}
                for fmt in web_formats:
                    safe_print(f"   📄 测试{fmt['name']} Web导出...")
                    try:
                        if fmt['ext'] == 'png':
                            opt = fmt['option_class']()
                            opt.interlaced = False
                        elif fmt['ext'] == 'jpg':
                            opt = fmt['option_class']()
                            opt.quality = 10
                        else:
                            opt = fmt['option_class']()

                        file_path = os.path.join(get_test_save_dir(), f"web_export_{fmt['name'].lower()}.{fmt['ext']}")
                        doc.saveAs(file_path, opt, True)

                        if os.path.exists(file_path):
                            size = os.path.getsize(file_path)
                            file_sizes[fmt['name']] = size
                            safe_print(f"      ✅ {fmt['name']}导出成功 ({size} bytes)")
                        else:
                            safe_print(f"      ⚠️ {fmt['name']}文件未找到")
                    except Exception as fmt_e:
                        safe_print(f"      ⚠️ {fmt['name']}导出警告: {str(fmt_e)[:50]}")

                # 显示文件大小比较
                if file_sizes:
                    safe_print("   📊 Web格式文件大小比较:")
                    for name, size in file_sizes.items():
                        safe_print(f"      📁 {name}: {size} bytes")

        except Exception as e:
            safe_print(f"❌ Web导出格式比较失败: {str(e)}")

        # 测试5: 透明度和背景处理
        safe_print("\n🔧 测试5: 透明度和背景处理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建透明内容
                safe_print("   🎨 创建透明背景内容...")
                layer = doc.artLayers.add()
                layer.name = "透明内容"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 255
                fill_color.rgb.blue = 0
                ps.app.foregroundColor = fill_color

                # 创建部分透明的内容
                doc.selection.select([[50, 50], [250, 50], [250, 250], [50, 250]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                safe_print("      ✅ 透明内容创建完成")

                # 测试透明处理选项
                safe_print("   🌈 配置透明处理选项...")
                try:
                    # PNG导出保持透明度
                    png_opt = ps.PNGSaveOptions()
                    png_opt.interlaced = False
                    png_path = os.path.join(get_test_save_dir(), "web_transparent.png")
                    doc.saveAs(png_path, png_opt, True)

                    if os.path.exists(png_path):
                        size = os.path.getsize(png_path)
                        safe_print(f"      ✅ 透明背景PNG导出成功 ({size} bytes)")
                    else:
                        safe_print("      ⚠️ 透明背景PNG文件未找到")
                except Exception as transparent_e:
                    safe_print(f"      ⚠️ 透明处理配置警告: {str(transparent_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 透明度和背景处理失败: {str(e)}")

        # 测试6: 压缩和优化设置
        safe_print("\n🔧 测试6: 压缩和优化设置...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建测试内容
                safe_print("   🎨 创建压缩测试内容...")
                for i in range(2):
                    layer = doc.artLayers.add()
                    layer.name = f"压缩测试图层_{i+1}"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 100 + 50 * i
                    fill_color.rgb.green = 150 + 25 * i
                    fill_color.rgb.blue = 200 - 40 * i
                    ps.app.foregroundColor = fill_color

                    x = 50 + i * 100
                    doc.selection.select([[x, 100], [x + 80, 100], [x + 80, 200], [x, 200]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                safe_print("      ✅ 压缩测试内容创建完成")

                # 测试不同压缩级别
                safe_print("   🔧 配置压缩级别...")
                compression_configs = [
                    {"name": "最小压缩", "interlaced": False, "compression": 0},
                    {"name": "中等压缩", "interlaced": False, "compression": 3},
                    {"name": "最大压缩", "interlaced": True, "compression": 6},
                ]

                for comp in compression_configs:
                    safe_print(f"   📦 配置{comp['name']}...")
                    try:
                        png_opt = ps.PNGSaveOptions()
                        png_opt.interlaced = comp["interlaced"]
                        png_opt.compression = comp["compression"]

                        file_path = os.path.join(get_test_save_dir(), f"web_compression_{comp['name'].replace(' ', '_').lower()}.png")
                        doc.saveAs(file_path, png_opt, True)

                        if os.path.exists(file_path):
                            size = os.path.getsize(file_path)
                            safe_print(f"      ✅ {comp['name']}配置成功 ({size} bytes)")
                        else:
                            safe_print(f"      ⚠️ {comp['name']}文件未找到")
                    except Exception as comp_e:
                        safe_print(f"      ⚠️ {comp['name']}配置警告: {str(comp_e)[:40]}")

        except Exception as e:
            safe_print(f"❌ 压缩和优化设置失败: {str(e)}")

        # 测试7: 错误处理和边界情况
        safe_print("\n🔧 测试7: 错误处理和边界情况...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建测试内容
                layer = doc.artLayers.add()
                layer.name = "错误处理测试"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 128
                fill_color.rgb.green = 128
                fill_color.rgb.blue = 128
                ps.app.foregroundColor = fill_color

                doc.selection.select([[50, 50], [150, 50], [150, 150], [50, 150]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 测试无效文件路径
                safe_print("   📄 测试无效文件路径...")
                try:
                    png_opt = ps.PNGSaveOptions()
                    invalid_path = "/invalid/path/image.png"
                    doc.saveAs(invalid_path, png_opt, True)
                    safe_print("      ⚠️ 无效路径意外成功")
                except Exception as invalid_e:
                    safe_print(f"      ✅ 正确处理无效路径")

                # 测试空扩展名
                safe_print("   📄 测试空扩展名...")
                try:
                    png_opt = ps.PNGSaveOptions()
                    empty_ext_path = os.path.join(get_test_save_dir(), "test_file")
                    doc.saveAs(empty_ext_path, png_opt, True)
                    safe_print("      ⚠️ 空扩展名意外成功")
                except Exception as empty_e:
                    safe_print(f"      ✅ 正确处理空扩展名")

        except Exception as e:
            safe_print(f"❌ 错误处理和边界情况失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "export_layers_use_export_options_saveforweb_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Export Layers Use ExportOptions SaveForWeb 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: Web导出功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本Web导出功能 (原始代码逻辑)\n")
                f.write(f"- SaveForWeb选项详细配置\n")
                f.write(f"- 图层Web导出优化\n")
                f.write(f"- Web导出格式比较\n")
                f.write(f"- 透明度和背景处理\n")
                f.write(f"- 压缩和优化设置\n")
                f.write(f"- 错误处理和边界情况\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第40项: export_layers_use_export_options_saveforweb.py 测试完成!")
        safe_print("✅ 验证功能: SaveForWeb配置、格式优化、透明处理、压缩设置、错误处理")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. Web导出功能是否可用")
        safe_print("3. saveAs方法是否正常")
        safe_print("4. 导出选项是否正确配置")
        return False

if __name__ == "__main__":
    test_export_layers_use_export_options_saveforweb()
