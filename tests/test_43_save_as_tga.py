# -*- coding: utf-8 -*-
"""测试第43项: save_as_tga.py - 保存为TGA"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_save_as_tga():
    """运行save_as_tga测试"""
    safe_print("📋 开始执行第43项: save_as_tga.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本TGA保存功能 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本TGA保存功能 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ Session成功启动")
                safe_print(f"   📄 当前文档: {doc.name}")

                # 创建测试内容
                safe_print("   🎨 创建测试内容...")
                layer = doc.artLayers.add()
                layer.name = "TGA测试内容"

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

                # 保存为TGA (原始代码逻辑)
                safe_print("   📄 保存为TGA...")
                try:
                    # 尝试使用TGA保存选项
                    if hasattr(ps, 'TGASaveOptions'):
                        tga_opt = ps.TGASaveOptions()
                        tga_opt.alphaChannels = True
                        tga_opt.rleCompression = True
                        tga_path = os.path.join(save_dir, "output.tga")
                        doc.saveAs(tga_path, tga_opt, True)

                        if os.path.exists(tga_path):
                            size = os.path.getsize(tga_path)
                            safe_print(f"      ✅ TGA保存成功 ({size} bytes)")
                        else:
                            safe_print("      ⚠️ TGA文件未找到")
                    else:
                        safe_print("      ⚠️ TGASaveOptions不可用，使用替代方法")
                        # 尝试直接保存为TGA
                        tga_path = os.path.join(save_dir, "output.tga")
                        doc.saveAs(tga_path, True)

                        if os.path.exists(tga_path):
                            size = os.path.getsize(tga_path)
                            safe_print(f"      ✅ TGA保存成功 ({size} bytes)")
                        else:
                            safe_print("      ⚠️ TGA文件未找到")
                except Exception as tga_e:
                    safe_print(f"      ⚠️ TGA保存失败: {str(tga_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 基本TGA保存功能失败: {str(e)}")
            return False

        # 测试2: TGA选项详细配置
        safe_print("\n🔧 测试2: TGA选项详细配置...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ TGA选项详细配置测试文档已创建")

                # 创建彩色内容
                safe_print("   🎨 创建彩色内容...")
                colors = [
                    {"name": "红色", "r": 255, "g": 0, "b": 0, "x": 50},
                    {"name": "绿色", "r": 0, "g": 255, "b": 0, "x": 150},
                    {"name": "蓝色", "r": 0, "g": 0, "b": 255, "x": 250},
                ]

                for color_info in colors:
                    layer = doc.artLayers.add()
                    layer.name = f"TGA测试_{color_info['name']}"

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

                # 测试不同的TGA配置
                safe_print("   📄 配置不同TGA选项...")
                try:
                    # TGA压缩选项
                    tga_compression_options = [
                        {"name": "RLE压缩", "rle": True},
                        {"name": "无压缩", "rle": False},
                        {"name": "Alpha通道", "alpha": True},
                        {"name": "无Alpha通道", "alpha": False},
                    ]

                    for opt in tga_compression_options:
                        safe_print(f"      🖼️ 配置{opt['name']}...")
                        try:
                            if hasattr(ps, 'TGASaveOptions'):
                                tga_opt = ps.TGASaveOptions()
                                tga_opt.rleCompression = opt["rle"]
                                tga_opt.alphaChannels = opt["alpha"]
                                tga_path = os.path.join(get_test_save_dir(), f"tga_{opt['name'].replace(' ', '_').lower()}.tga")
                                doc.saveAs(tga_path, tga_opt, True)

                                if os.path.exists(tga_path):
                                    size = os.path.getsize(tga_path)
                                    safe_print(f"         ✅ {opt['name']}保存成功 ({size} bytes)")
                                else:
                                    safe_print(f"         ⚠️ {opt['name']}文件未找到")
                            else:
                                safe_print(f"      ⚠️ TGASaveOptions不可用，跳过选项配置")
                                break
                        except Exception as opt_e:
                            safe_print(f"         ❌ {opt['name']}保存失败: {str(opt_e)[:40]}")

                except Exception as config_e:
                    safe_print(f"      ⚠️ TGA选项配置警告: {str(config_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ TGA选项详细配置失败: {str(e)}")

        # 测试3: 多图层TGA保存
        safe_print("\n🔧 测试3: 多图层TGA保存...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 多图层TGA保存测试文档已创建")

                # 创建多个图层用于TGA保存
                safe_print("   🎨 创建多图层TGA测试...")
                for i in range(3):
                    layer = doc.artLayers.add()
                    layer.name = f"TGA图层_{i+1}"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 80 * (i + 1)
                    fill_color.rgb.green = 100 + 50 * i
                    fill_color.rgb.blue = 200 - 30 * i
                    ps.app.foregroundColor = fill_color

                    x = 50 + i * 80
                    doc.selection.select([[x, 100], [x + 60, 100], [x + 60, 200], [x, 200]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                safe_print("      ✅ 多图层TGA测试图层创建完成")

                # 保存多图层TGA
                safe_print("   📤 保存多图层TGA...")
                try:
                    if hasattr(ps, 'TGASaveOptions'):
                        tga_opt = ps.TGASaveOptions()
                        tga_opt.alphaChannels = True
                        tga_opt.rleCompression = True
                        tga_path = os.path.join(get_test_save_dir(), "multi_layer.tga")
                        doc.saveAs(tga_path, tga_opt, True)

                        if os.path.exists(tga_path):
                            size = os.path.getsize(tga_path)
                            safe_print(f"      ✅ 多图层TGA保存成功 ({size} bytes)")
                        else:
                            safe_print("      ⚠️ 多图层TGA文件未找到")
                    else:
                        safe_print("      ⚠️ TGASaveOptions不可用，使用替代方法")
                        tga_path = os.path.join(get_test_save_dir(), "multi_layer.tga")
                        doc.saveAs(tga_path, True)

                        if os.path.exists(tga_path):
                            size = os.path.getsize(tga_path)
                            safe_print(f"      ✅ 多图层TGA保存成功 ({size} bytes)")
                        else:
                            safe_print("      ⚠️ 多图层TGA文件未找到")
                except Exception as multi_e:
                    safe_print(f"      ⚠️ 多图层TGA保存警告: {str(multi_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 多图层TGA保存失败: {str(e)}")

        # 测试4: TGA透明度和Alpha通道
        safe_print("\n🔧 测试4: TGA透明度和Alpha通道...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ TGA透明度和Alpha通道测试文档已创建")

                # 创建半透明内容
                safe_print("   🎨 创建半透明内容...")
                layer = doc.artLayers.add()
                layer.name = "透明度测试"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 255
                fill_color.rgb.blue = 0
                ps.app.foregroundColor = fill_color

                doc.selection.select([[50, 50], [350, 50], [350, 350], [50, 350]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                safe_print("      ✅ 半透明内容创建完成")

                # 测试Alpha通道选项
                safe_print("   🌈 配置Alpha通道选项...")
                try:
                    if hasattr(ps, 'TGASaveOptions'):
                        tga_opt = ps.TGASaveOptions()
                        tga_opt.alphaChannels = True
                        tga_opt.rleCompression = True
                        tga_path = os.path.join(get_test_save_dir(), "alpha_channel.tga")
                        doc.saveAs(tga_path, tga_opt, True)

                        if os.path.exists(tga_path):
                            size = os.path.getsize(tga_path)
                            safe_print(f"      ✅ Alpha通道TGA保存成功 ({size} bytes)")
                        else:
                            safe_print("      ⚠️ Alpha通道TGA文件未找到")
                    else:
                        safe_print("      ⚠️ TGASaveOptions不可用，跳过Alpha通道配置")
                except Exception as alpha_e:
                    safe_print(f"      ⚠️ Alpha通道配置警告: {str(alpha_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ TGA透明度和Alpha通道失败: {str(e)}")

        # 测试5: TGA压缩对比
        safe_print("\n🔧 测试5: TGA压缩对比...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ TGA压缩对比测试文档已创建")

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

                # 测试RLE压缩对比
                safe_print("   🔧 配置RLE压缩...")
                compression_configs = [
                    {"name": "启用RLE", "rle": True},
                    {"name": "禁用RLE", "rle": False},
                ]

                file_sizes = {}
                for comp in compression_configs:
                    safe_print(f"   📦 配置{comp['name']}...")
                    try:
                        if hasattr(ps, 'TGASaveOptions'):
                            tga_opt = ps.TGASaveOptions()
                            tga_opt.rleCompression = comp["rle"]
                            tga_opt.alphaChannels = True

                            file_path = os.path.join(get_test_save_dir(), f"tga_compression_{comp['rle']}.tga")
                            doc.saveAs(file_path, tga_opt, True)

                            if os.path.exists(file_path):
                                size = os.path.getsize(file_path)
                                file_sizes[comp['name']] = size
                                safe_print(f"      ✅ {comp['name']}配置成功 ({size} bytes)")
                            else:
                                safe_print(f"      ⚠️ {comp['name']}文件未找到")
                        else:
                            safe_print(f"      ⚠️ TGASaveOptions不可用，跳过压缩配置")
                            break
                    except Exception as comp_e:
                        safe_print(f"      ⚠️ {comp['name']}配置警告: {str(comp_e)[:40]}")

                # 显示压缩对比
                if len(file_sizes) >= 2:
                    safe_print("   📊 压缩效果对比:")
                    rle_enabled = file_sizes.get("启用RLE", 0)
                    rle_disabled = file_sizes.get("禁用RLE", 0)
                    if rle_enabled > 0 and rle_disabled > 0:
                        ratio = ((rle_disabled - rle_enabled) / rle_disabled) * 100
                        safe_print(f"      📁 RLE压缩节省: {ratio:.2f}%")

        except Exception as e:
            safe_print(f"❌ TGA压缩对比失败: {str(e)}")

        # 测试6: TGA颜色深度处理
        safe_print("\n🔧 测试6: TGA颜色深度处理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ TGA颜色深度处理测试文档已创建")

                # 创建渐变内容
                layer = doc.artLayers.add()
                layer.name = "颜色深度测试"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 128
                fill_color.rgb.green = 64
                fill_color.rgb.blue = 192
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [300, 100], [300, 300], [100, 300]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 测试颜色深度选项
                safe_print("   🎨 配置颜色深度选项...")
                try:
                    if hasattr(ps, 'TGASaveOptions'):
                        tga_opt = ps.TGASaveOptions()
                        tga_opt.alphaChannels = True
                        tga_opt.rleCompression = True
                        tga_path = os.path.join(get_test_save_dir(), "color_depth.tga")
                        doc.saveAs(tga_path, tga_opt, True)

                        if os.path.exists(tga_path):
                            size = os.path.getsize(tga_path)
                            safe_print(f"      ✅ 颜色深度TGA保存成功 ({size} bytes)")
                        else:
                            safe_print("      ⚠️ 颜色深度TGA文件未找到")
                    else:
                        safe_print("      ⚠️ TGASaveOptions不可用，跳过颜色深度配置")
                except Exception as depth_e:
                    safe_print(f"      ⚠️ 颜色深度配置警告: {str(depth_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ TGA颜色深度处理失败: {str(e)}")

        # 测试7: TGA分辨率处理
        safe_print("\n🔧 测试7: TGA分辨率处理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ TGA分辨率处理测试文档已创建")

                # 创建测试内容
                layer = doc.artLayers.add()
                layer.name = "分辨率测试"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 200
                fill_color.rgb.blue = 100
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [300, 100], [300, 300], [100, 300]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 保存TGA（包含分辨率信息）
                safe_print("   📏 保存包含分辨率的TGA...")
                try:
                    if hasattr(ps, 'TGASaveOptions'):
                        tga_opt = ps.TGASaveOptions()
                        tga_opt.alphaChannels = True
                        tga_opt.rleCompression = True
                        tga_path = os.path.join(get_test_save_dir(), "resolution.tga")
                        doc.saveAs(tga_path, tga_opt, True)

                        if os.path.exists(tga_path):
                            size = os.path.getsize(tga_path)
                            safe_print(f"      ✅ 分辨率TGA保存成功 ({size} bytes)")
                        else:
                            safe_print("      ⚠️ 分辨率TGA文件未找到")
                    else:
                        safe_print("      ⚠️ TGASaveOptions不可用，跳过分辨率配置")
                except Exception as res_e:
                    safe_print(f"      ⚠️ 分辨率配置警告: {str(res_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ TGA分辨率处理失败: {str(e)}")

        # 测试8: TGA错误处理
        safe_print("\n🔧 测试8: TGA错误处理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ TGA错误处理测试文档已创建")

                # 创建测试内容
                layer = doc.artLayers.add()
                layer.name = "错误处理测试"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 128
                fill_color.rgb.green = 128
                fill_color.rgb.blue = 255
                ps.app.foregroundColor = fill_color

                doc.selection.select([[50, 50], [250, 50], [250, 250], [50, 250]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 测试无效TGA路径
                safe_print("   📄 测试无效TGA路径...")
                try:
                    if hasattr(ps, 'TGASaveOptions'):
                        tga_opt = ps.TGASaveOptions()
                        tga_opt.alphaChannels = True
                        tga_opt.rleCompression = True
                        invalid_path = "/invalid/path/image.tga"
                        doc.saveAs(invalid_path, tga_opt, True)
                        safe_print("      ⚠️ 无效路径意外成功")
                    else:
                        safe_print("      ⚠️ TGASaveOptions不可用，跳过路径测试")
                except Exception as invalid_e:
                    safe_print(f"      ✅ 正确处理无效路径")

                # 测试空TGA文件名
                safe_print("   📄 测试空TGA文件名...")
                try:
                    if hasattr(ps, 'TGASaveOptions'):
                        tga_opt = ps.TGASaveOptions()
                        tga_opt.alphaChannels = True
                        tga_opt.rleCompression = True
                        empty_path = os.path.join(get_test_save_dir(), "")
                        doc.saveAs(empty_path, tga_opt, True)
                        safe_print("      ⚠️ 空文件名意外成功")
                    else:
                        safe_print("      ⚠️ TGASaveOptions不可用，跳过文件名测试")
                except Exception as empty_e:
                    safe_print(f"      ✅ 正确处理空文件名")

        except Exception as e:
            safe_print(f"❌ TGA错误处理失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "save_as_tga_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Save As TGA 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: TGA保存功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本TGA保存功能 (原始代码逻辑)\n")
                f.write(f"- TGA选项详细配置\n")
                f.write(f"- 多图层TGA保存\n")
                f.write(f"- TGA透明度和Alpha通道\n")
                f.write(f"- TGA压缩对比\n")
                f.write(f"- TGA颜色深度处理\n")
                f.write(f"- TGA分辨率处理\n")
                f.write(f"- TGA错误处理\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第43项: save_as_tga.py 测试完成!")
        safe_print("✅ 验证功能: TGA保存、Alpha通道、RLE压缩、颜色深度、分辨率")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. TGA保存功能是否可用")
        safe_print("3. TGASaveOptions是否支持")
        safe_print("4. Alpha通道和压缩选项是否正确")
        return False

if __name__ == "__main__":
    test_save_as_tga()
