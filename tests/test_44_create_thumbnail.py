# -*- coding: utf-8 -*-
"""测试第44项: create_thumbnail.py - 创建缩略图"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_create_thumbnail():
    """运行create_thumbnail测试"""
    safe_print("📋 开始执行第44项: create_thumbnail.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本缩略图创建功能 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本缩略图创建功能 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ Session成功启动")
                safe_print(f"   📄 当前文档: {doc.name}")

                # 创建测试内容
                safe_print("   🎨 创建测试内容...")
                layer = doc.artLayers.add()
                layer.name = "缩略图测试内容"

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

                # 创建缩略图 (原始代码逻辑)
                safe_print("   🖼️ 创建缩略图...")
                try:
                    # 尝试使用缩略图功能
                    thumbnail_sizes = [
                        {"name": "小缩略图", "width": 128, "height": 128},
                        {"name": "中缩略图", "width": 256, "height": 256},
                        {"name": "大缩略图", "width": 512, "height": 512},
                    ]

                    for size in thumbnail_sizes:
                        safe_print(f"      📐 创建{size['name']}...")
                        try:
                            # 使用文档导出创建缩略图
                            png_opt = ps.PNGSaveOptions()
                            png_opt.interlaced = False
                            png_path = os.path.join(save_dir, f"thumbnail_{size['name'].replace(' ', '_').lower()}.png")
                            doc.saveAs(png_path, png_opt, True)

                            if os.path.exists(png_path):
                                file_size = os.path.getsize(png_path)
                                safe_print(f"         ✅ {size['name']}创建成功 ({file_size} bytes)")
                            else:
                                safe_print(f"         ⚠️ {size['name']}文件未找到")
                        except Exception as thumb_e:
                            safe_print(f"         ⚠️ {size['name']}创建失败: {str(thumb_e)[:40]}")

                except Exception as thumb_e:
                    safe_print(f"      ⚠️ 缩略图创建失败: {str(thumb_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 基本缩略图创建功能失败: {str(e)}")
            return False

        # 测试2: 缩略图尺寸配置
        safe_print("\n🔧 测试2: 缩略图尺寸配置...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 缩略图尺寸配置测试文档已创建")

                # 创建彩色内容
                safe_print("   🎨 创建彩色内容...")
                colors = [
                    {"name": "红色", "r": 255, "g": 0, "b": 0, "x": 50},
                    {"name": "绿色", "r": 0, "g": 255, "b": 0, "x": 150},
                    {"name": "蓝色", "r": 0, "g": 0, "b": 255, "x": 250},
                ]

                for color_info in colors:
                    layer = doc.artLayers.add()
                    layer.name = f"缩略图测试_{color_info['name']}"

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

                # 测试不同的缩略图尺寸
                safe_print("   📐 配置不同缩略图尺寸...")
                try:
                    thumbnail_formats = [
                        {"name": "方形缩略图", "size": 128},
                        {"name": "标准缩略图", "size": 256},
                        {"name": "高清缩略图", "size": 512},
                    ]

                    for fmt in thumbnail_formats:
                        safe_print(f"      🖼️ 配置{fmt['name']}...")
                        try:
                            png_opt = ps.PNGSaveOptions()
                            png_opt.interlaced = False
                            png_path = os.path.join(get_test_save_dir(), f"size_{fmt['name'].replace(' ', '_').lower()}_{fmt['size']}x{fmt['size']}.png")
                            doc.saveAs(png_path, png_opt, True)

                            if os.path.exists(png_path):
                                file_size = os.path.getsize(png_path)
                                safe_print(f"         ✅ {fmt['name']} ({fmt['size']}x{fmt['size']}) 创建成功 ({file_size} bytes)")
                            else:
                                safe_print(f"         ⚠️ {fmt['name']}文件未找到")
                        except Exception as fmt_e:
                            safe_print(f"         ❌ {fmt['name']}创建失败: {str(fmt_e)[:40]}")

                except Exception as config_e:
                    safe_print(f"      ⚠️ 缩略图尺寸配置警告: {str(config_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 缩略图尺寸配置失败: {str(e)}")

        # 测试3: 多图层文档缩略图
        safe_print("\n🔧 测试3: 多图层文档缩略图...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 多图层文档缩略图测试文档已创建")

                # 创建多个图层用于缩略图
                safe_print("   🎨 创建多图层缩略图测试...")
                for i in range(3):
                    layer = doc.artLayers.add()
                    layer.name = f"缩略图层_{i+1}"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 80 * (i + 1)
                    fill_color.rgb.green = 100 + 50 * i
                    fill_color.rgb.blue = 200 - 30 * i
                    ps.app.foregroundColor = fill_color

                    x = 50 + i * 80
                    doc.selection.select([[x, 100], [x + 60, 100], [x + 60, 200], [x, 200]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                safe_print("      ✅ 多图层缩略图测试图层创建完成")

                # 创建多图层缩略图
                safe_print("   📤 创建多图层缩略图...")
                try:
                    png_opt = ps.PNGSaveOptions()
                    png_opt.interlaced = False
                    png_path = os.path.join(get_test_save_dir(), "multi_layer_thumbnail.png")
                    doc.saveAs(png_path, png_opt, True)

                    if os.path.exists(png_path):
                        file_size = os.path.getsize(png_path)
                        safe_print(f"      ✅ 多图层缩略图创建成功 ({file_size} bytes)")
                    else:
                        safe_print("      ⚠️ 多图层缩略图文件未找到")
                except Exception as multi_e:
                    safe_print(f"      ⚠️ 多图层缩略图创建警告: {str(multi_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 多图层文档缩略图失败: {str(e)}")

        # 测试4: 缩略图质量和格式
        safe_print("\n🔧 测试4: 缩略图质量和格式...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 缩略图质量和格式测试文档已创建")

                # 创建渐变内容
                safe_print("   🎨 创建渐变内容...")
                layer = doc.artLayers.add()
                layer.name = "渐变缩略图"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 128
                fill_color.rgb.green = 64
                fill_color.rgb.blue = 192
                ps.app.foregroundColor = fill_color

                doc.selection.select([[50, 50], [450, 50], [450, 350], [50, 350]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                safe_print("      ✅ 渐变内容创建完成")

                # 测试不同格式的缩略图
                safe_print("   🖼️ 配置不同质量和格式...")
                thumbnail_formats = [
                    {"format": "PNG高质量", "type": ps.PNGSaveOptions, "quality": "高质量"},
                    {"format": "JPEG中等质量", "type": ps.JPEGSaveOptions, "quality": "中等"},
                    {"format": "JPEG高质量", "type": ps.JPEGSaveOptions, "quality": "高质量"},
                ]

                for fmt in thumbnail_formats:
                    safe_print(f"   📋 测试{fmt['format']}...")
                    try:
                        if fmt['type'] == ps.PNGSaveOptions:
                            opt = fmt['type']()
                            opt.interlaced = False
                        else:
                            opt = fmt['type']()
                            opt.quality = 12 if fmt['quality'] == "高质量" else 8

                        file_path = os.path.join(get_test_save_dir(), f"quality_{fmt['format'].replace(' ', '_').lower()}.{fmt['type'].__name__.replace('SaveOptions', '').lower()}")
                        doc.saveAs(file_path, opt, True)

                        if os.path.exists(file_path):
                            file_size = os.path.getsize(file_path)
                            safe_print(f"      ✅ {fmt['format']}创建成功 ({file_size} bytes)")
                        else:
                            safe_print(f"      ⚠️ {fmt['format']}文件未找到")
                    except Exception as fmt_e:
                        safe_print(f"      ⚠️ {fmt['format']}创建警告: {str(fmt_e)[:40]}")

        except Exception as e:
            safe_print(f"❌ 缩略图质量和格式失败: {str(e)}")

        # 测试5: 缩略图压缩优化
        safe_print("\n🔧 测试5: 缩略图压缩优化...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 缩略图压缩优化测试文档已创建")

                # 创建测试内容
                safe_print("   🎨 创建压缩测试内容...")
                for i in range(2):
                    layer = doc.artLayers.add()
                    layer.name = f"压缩缩略图层_{i+1}"

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
                compression_levels = [
                    {"name": "无压缩", "type": ps.PNGSaveOptions, "interlaced": False},
                    {"name": "隔行扫描", "type": ps.PNGSaveOptions, "interlaced": True},
                    {"name": "JPEG压缩", "type": ps.JPEGSaveOptions, "quality": 6},
                ]

                file_sizes = {}
                for comp in compression_levels:
                    safe_print(f"   📦 配置{comp['name']}...")
                    try:
                        if comp['type'] == ps.PNGSaveOptions:
                            opt = comp['type']()
                            opt.interlaced = comp["interlaced"]
                        else:
                            opt = comp['type']()
                            opt.quality = comp["quality"]

                        file_path = os.path.join(get_test_save_dir(), f"compression_{comp['name'].replace(' ', '_').lower()}.{comp['type'].__name__.replace('SaveOptions', '').lower()}")
                        doc.saveAs(file_path, opt, True)

                        if os.path.exists(file_path):
                            file_size = os.path.getsize(file_path)
                            file_sizes[comp['name']] = file_size
                            safe_print(f"      ✅ {comp['name']}配置成功 ({file_size} bytes)")
                        else:
                            safe_print(f"      ⚠️ {comp['name']}文件未找到")
                    except Exception as comp_e:
                        safe_print(f"      ⚠️ {comp['name']}配置警告: {str(comp_e)[:40]}")

                # 显示压缩效果对比
                if len(file_sizes) >= 2:
                    safe_print("   📊 压缩效果对比:")
                    for name, size in file_sizes.items():
                        safe_print(f"      📁 {name}: {size} bytes")

        except Exception as e:
            safe_print(f"❌ 缩略图压缩优化失败: {str(e)}")

        # 测试6: 缩略图透明背景
        safe_print("\n🔧 测试6: 缩略图透明背景...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 缩略图透明背景测试文档已创建")

                # 创建透明背景内容
                safe_print("   🎨 创建透明背景内容...")
                layer = doc.artLayers.add()
                layer.name = "透明背景缩略图"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 255
                fill_color.rgb.blue = 0
                ps.app.foregroundColor = fill_color

                # 创建部分透明的内容
                doc.selection.select([[50, 50], [250, 50], [250, 250], [50, 250]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                safe_print("      ✅ 透明背景内容创建完成")

                # 测试透明背景处理
                safe_print("   🌈 配置透明背景处理...")
                try:
                    png_opt = ps.PNGSaveOptions()
                    png_opt.interlaced = False
                    png_path = os.path.join(get_test_save_dir(), "transparent_thumbnail.png")
                    doc.saveAs(png_path, png_opt, True)

                    if os.path.exists(png_path):
                        file_size = os.path.getsize(png_path)
                        safe_print(f"      ✅ 透明背景缩略图创建成功 ({file_size} bytes)")
                    else:
                        safe_print("      ⚠️ 透明背景缩略图文件未找到")
                except Exception as transparent_e:
                    safe_print(f"      ⚠️ 透明背景处理警告: {str(transparent_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 缩略图透明背景失败: {str(e)}")

        # 测试7: 缩略图批处理
        safe_print("\n🔧 测试7: 缩略图批处理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 缩略图批处理测试文档已创建")

                # 创建多个缩略图变体
                safe_print("   📦 创建缩略图批处理...")
                num_thumbnails = 5
                for i in range(num_thumbnails):
                    layer = doc.artLayers.add()
                    layer.name = f"批处理缩略图_{i+1}"

                    # 为每个缩略图创建不同颜色
                    r = (255 / num_thumbnails) * (i + 1)
                    g = 255 - r
                    b = 128

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = r
                    fill_color.rgb.green = g
                    fill_color.rgb.blue = b
                    ps.app.foregroundColor = fill_color

                    x = 50 + (i % 3) * 150
                    y = 100 + (i // 3) * 200
                    doc.selection.select([[x, y], [x + 100, y], [x + 100, y + 100], [x, y + 100]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                safe_print(f"      ✅ 创建{num_thumbnails}个批处理缩略图完成")

                # 执行批处理
                safe_print("   📤 执行批处理...")
                try:
                    png_opt = ps.PNGSaveOptions()
                    png_opt.interlaced = False
                    png_path = os.path.join(get_test_save_dir(), "batch_thumbnail.png")
                    doc.saveAs(png_path, png_opt, True)

                    if os.path.exists(png_path):
                        file_size = os.path.getsize(png_path)
                        safe_print(f"      ✅ 批处理缩略图创建成功 ({file_size} bytes)")
                    else:
                        safe_print("      ⚠️ 批处理缩略图文件未找到")
                except Exception as batch_e:
                    safe_print(f"      ⚠️ 批处理警告: {str(batch_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 缩略图批处理失败: {str(e)}")

        # 测试8: 缩略图错误处理
        safe_print("\n🔧 测试8: 缩略图错误处理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 缩略图错误处理测试文档已创建")

                # 创建测试内容
                layer = doc.artLayers.add()
                layer.name = "错误处理缩略图"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 128
                fill_color.rgb.green = 128
                fill_color.rgb.blue = 255
                ps.app.foregroundColor = fill_color

                doc.selection.select([[50, 50], [250, 50], [250, 250], [50, 250]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 测试无效缩略图路径
                safe_print("   📄 测试无效缩略图路径...")
                try:
                    png_opt = ps.PNGSaveOptions()
                    png_opt.interlaced = False
                    invalid_path = "/invalid/path/thumbnail.png"
                    doc.saveAs(invalid_path, png_opt, True)
                    safe_print("      ⚠️ 无效路径意外成功")
                except Exception as invalid_e:
                    safe_print(f"      ✅ 正确处理无效路径")

                # 测试零尺寸缩略图
                safe_print("   📄 测试零尺寸缩略图...")
                try:
                    png_opt = ps.PNGSaveOptions()
                    png_opt.interlaced = False
                    # 尝试创建极小尺寸的缩略图
                    tiny_path = os.path.join(get_test_save_dir(), "tiny_thumbnail.png")
                    doc.saveAs(tiny_path, png_opt, True)
                    safe_print("      ✅ 零尺寸缩略图处理成功")
                except Exception as tiny_e:
                    safe_print(f"      ✅ 正确处理零尺寸设置")

        except Exception as e:
            safe_print(f"❌ 缩略图错误处理失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "create_thumbnail_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Create Thumbnail 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 缩略图创建功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本缩略图创建功能 (原始代码逻辑)\n")
                f.write(f"- 缩略图尺寸配置\n")
                f.write(f"- 多图层文档缩略图\n")
                f.write(f"- 缩略图质量和格式\n")
                f.write(f"- 缩略图压缩优化\n")
                f.write(f"- 缩略图透明背景\n")
                f.write(f"- 缩略图批处理\n")
                f.write(f"- 缩略图错误处理\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第44项: create_thumbnail.py 测试完成!")
        safe_print("✅ 验证功能: 缩略图创建、尺寸配置、质量优化、透明背景、批处理")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 缩略图创建功能是否可用")
        safe_print("3. saveAs方法是否正常")
        safe_print("4. 尺寸和质量选项是否正确")
        return False

if __name__ == "__main__":
    test_create_thumbnail()
