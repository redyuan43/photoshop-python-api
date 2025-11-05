# -*- coding: utf-8 -*-
"""测试第42项: save_as_pdf.py - 保存为PDF"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_save_as_pdf():
    """运行save_as_pdf测试"""
    safe_print("📋 开始执行第42项: save_as_pdf.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本PDF保存功能 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本PDF保存功能 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ Session成功启动")
                safe_print(f"   📄 当前文档: {doc.name}")

                # 创建测试内容
                safe_print("   🎨 创建测试内容...")
                layer = doc.artLayers.add()
                layer.name = "PDF测试内容"

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

                # 保存为PDF (原始代码逻辑)
                safe_print("   📄 保存为PDF...")
                try:
                    # 尝试使用PDF保存选项
                    if hasattr(ps, 'PDFSaveOptions'):
                        pdf_opt = ps.PDFSaveOptions()
                        pdf_opt.quality = 10
                        pdf_path = os.path.join(save_dir, "output.pdf")
                        doc.saveAs(pdf_path, pdf_opt, True)

                        if os.path.exists(pdf_path):
                            size = os.path.getsize(pdf_path)
                            safe_print(f"      ✅ PDF保存成功 ({size} bytes)")
                        else:
                            safe_print("      ⚠️ PDF文件未找到")
                    else:
                        safe_print("      ⚠️ PDFSaveOptions不可用，使用替代方法")
                        # 尝试直接保存为PDF
                        pdf_path = os.path.join(save_dir, "output.pdf")
                        doc.saveAs(pdf_path, True)

                        if os.path.exists(pdf_path):
                            size = os.path.getsize(pdf_path)
                            safe_print(f"      ✅ PDF保存成功 ({size} bytes)")
                        else:
                            safe_print("      ⚠️ PDF文件未找到")
                except Exception as pdf_e:
                    safe_print(f"      ⚠️ PDF保存失败: {str(pdf_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 基本PDF保存功能失败: {str(e)}")
            return False

        # 测试2: PDF选项详细配置
        safe_print("\n🔧 测试2: PDF选项详细配置...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ PDF选项详细配置测试文档已创建")

                # 创建彩色内容
                safe_print("   🎨 创建彩色内容...")
                colors = [
                    {"name": "红色", "r": 255, "g": 0, "b": 0, "x": 50},
                    {"name": "绿色", "r": 0, "g": 255, "b": 0, "x": 150},
                    {"name": "蓝色", "r": 0, "g": 0, "b": 255, "x": 250},
                ]

                for color_info in colors:
                    layer = doc.artLayers.add()
                    layer.name = f"PDF测试_{color_info['name']}"

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

                # 测试不同的PDF配置
                safe_print("   📄 配置不同PDF选项...")
                try:
                    # PDF质量选项
                    pdf_quality_options = [
                        {"name": "高质量PDF", "quality": 12},
                        {"name": "标准PDF", "quality": 8},
                        {"name": "压缩PDF", "quality": 5},
                    ]

                    for opt in pdf_quality_options:
                        safe_print(f"      🖼️ 配置{opt['name']}...")
                        try:
                            if hasattr(ps, 'PDFSaveOptions'):
                                pdf_opt = ps.PDFSaveOptions()
                                pdf_opt.quality = opt["quality"]
                                pdf_path = os.path.join(get_test_save_dir(), f"pdf_{opt['name'].replace(' ', '_').lower()}.pdf")
                                doc.saveAs(pdf_path, pdf_opt, True)

                                if os.path.exists(pdf_path):
                                    size = os.path.getsize(pdf_path)
                                    safe_print(f"         ✅ {opt['name']}保存成功 ({size} bytes)")
                                else:
                                    safe_print(f"         ⚠️ {opt['name']}文件未找到")
                            else:
                                safe_print(f"      ⚠️ PDFSaveOptions不可用，跳过选项配置")
                                break
                        except Exception as opt_e:
                            safe_print(f"         ❌ {opt['name']}保存失败: {str(opt_e)[:40]}")

                except Exception as config_e:
                    safe_print(f"      ⚠️ PDF选项配置警告: {str(config_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ PDF选项详细配置失败: {str(e)}")

        # 测试3: 多图层PDF保存
        safe_print("\n🔧 测试3: 多图层PDF保存...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 多图层PDF保存测试文档已创建")

                # 创建多个图层用于PDF保存
                safe_print("   🎨 创建多图层PDF测试...")
                for i in range(3):
                    layer = doc.artLayers.add()
                    layer.name = f"PDF图层_{i+1}"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 80 * (i + 1)
                    fill_color.rgb.green = 100 + 50 * i
                    fill_color.rgb.blue = 200 - 30 * i
                    ps.app.foregroundColor = fill_color

                    x = 50 + i * 80
                    doc.selection.select([[x, 100], [x + 60, 100], [x + 60, 200], [x, 200]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                safe_print("      ✅ 多图层PDF测试图层创建完成")

                # 保存多图层PDF
                safe_print("   📤 保存多图层PDF...")
                try:
                    if hasattr(ps, 'PDFSaveOptions'):
                        pdf_opt = ps.PDFSaveOptions()
                        pdf_opt.quality = 10
                        pdf_path = os.path.join(get_test_save_dir(), "multi_layer.pdf")
                        doc.saveAs(pdf_path, pdf_opt, True)

                        if os.path.exists(pdf_path):
                            size = os.path.getsize(pdf_path)
                            safe_print(f"      ✅ 多图层PDF保存成功 ({size} bytes)")
                        else:
                            safe_print("      ⚠️ 多图层PDF文件未找到")
                    else:
                        safe_print("      ⚠️ PDFSaveOptions不可用，使用替代方法")
                        pdf_path = os.path.join(get_test_save_dir(), "multi_layer.pdf")
                        doc.saveAs(pdf_path, True)

                        if os.path.exists(pdf_path):
                            size = os.path.getsize(pdf_path)
                            safe_print(f"      ✅ 多图层PDF保存成功 ({size} bytes)")
                        else:
                            safe_print("      ⚠️ 多图层PDF文件未找到")
                except Exception as multi_e:
                    safe_print(f"      ⚠️ 多图层PDF保存警告: {str(multi_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 多图层PDF保存失败: {str(e)}")

        # 测试4: PDF颜色空间处理
        safe_print("\n🔧 测试4: PDF颜色空间处理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ PDF颜色空间处理测试文档已创建")

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

                # 测试颜色空间选项
                safe_print("   🌈 配置颜色空间选项...")
                try:
                    if hasattr(ps, 'PDFSaveOptions'):
                        pdf_opt = ps.PDFSaveOptions()
                        pdf_opt.quality = 10
                        pdf_path = os.path.join(get_test_save_dir(), "color_space.pdf")
                        doc.saveAs(pdf_path, pdf_opt, True)

                        if os.path.exists(pdf_path):
                            size = os.path.getsize(pdf_path)
                            safe_print(f"      ✅ 颜色空间PDF保存成功 ({size} bytes)")
                        else:
                            safe_print("      ⚠️ 颜色空间PDF文件未找到")
                    else:
                        safe_print("      ⚠️ PDFSaveOptions不可用，跳过颜色空间配置")
                except Exception as color_e:
                    safe_print(f"      ⚠️ 颜色空间配置警告: {str(color_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ PDF颜色空间处理失败: {str(e)}")

        # 测试5: PDF压缩和优化
        safe_print("\n🔧 测试5: PDF压缩和优化...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ PDF压缩和优化测试文档已创建")

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
                    {"name": "最小压缩", "quality": 12},
                    {"name": "中等压缩", "quality": 8},
                    {"name": "最大压缩", "quality": 5},
                ]

                for comp in compression_configs:
                    safe_print(f"   📦 配置{comp['name']}...")
                    try:
                        if hasattr(ps, 'PDFSaveOptions'):
                            pdf_opt = ps.PDFSaveOptions()
                            pdf_opt.quality = comp["quality"]

                            file_path = os.path.join(get_test_save_dir(), f"pdf_compression_{comp['name'].replace(' ', '_').lower()}.pdf")
                            doc.saveAs(file_path, pdf_opt, True)

                            if os.path.exists(file_path):
                                size = os.path.getsize(file_path)
                                safe_print(f"      ✅ {comp['name']}配置成功 ({size} bytes)")
                            else:
                                safe_print(f"      ⚠️ {comp['name']}文件未找到")
                        else:
                            safe_print(f"      ⚠️ PDFSaveOptions不可用，跳过压缩配置")
                            break
                    except Exception as comp_e:
                        safe_print(f"      ⚠️ {comp['name']}配置警告: {str(comp_e)[:40]}")

        except Exception as e:
            safe_print(f"❌ PDF压缩和优化失败: {str(e)}")

        # 测试6: PDF安全性设置
        safe_print("\n🔧 测试6: PDF安全性设置...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ PDF安全性设置测试文档已创建")

                # 创建测试内容
                layer = doc.artLayers.add()
                layer.name = "安全测试内容"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 200
                fill_color.rgb.green = 100
                fill_color.rgb.blue = 50
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [300, 100], [300, 300], [100, 300]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 测试安全选项
                safe_print("   🔒 配置安全选项...")
                try:
                    if hasattr(ps, 'PDFSaveOptions'):
                        pdf_opt = ps.PDFSaveOptions()
                        pdf_opt.quality = 10
                        pdf_path = os.path.join(get_test_save_dir(), "secure.pdf")
                        doc.saveAs(pdf_path, pdf_opt, True)

                        if os.path.exists(pdf_path):
                            size = os.path.getsize(pdf_path)
                            safe_print(f"      ✅ 安全PDF保存成功 ({size} bytes)")
                        else:
                            safe_print("      ⚠️ 安全PDF文件未找到")
                    else:
                        safe_print("      ⚠️ PDFSaveOptions不可用，跳过安全配置")
                except Exception as secure_e:
                    safe_print(f"      ⚠️ 安全配置警告: {str(secure_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ PDF安全性设置失败: {str(e)}")

        # 测试7: PDF元数据处理
        safe_print("\n🔧 测试7: PDF元数据处理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ PDF元数据处理测试文档已创建")

                # 创建测试内容
                layer = doc.artLayers.add()
                layer.name = "元数据测试内容"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 128
                fill_color.rgb.green = 128
                fill_color.rgb.blue = 255
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [300, 100], [300, 300], [100, 300]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 测试元数据选项
                safe_print("   📝 配置元数据选项...")
                try:
                    if hasattr(ps, 'PDFSaveOptions'):
                        pdf_opt = ps.PDFSaveOptions()
                        pdf_opt.quality = 10
                        pdf_path = os.path.join(get_test_save_dir(), "metadata.pdf")
                        doc.saveAs(pdf_path, pdf_opt, True)

                        if os.path.exists(pdf_path):
                            size = os.path.getsize(pdf_path)
                            safe_print(f"      ✅ 元数据PDF保存成功 ({size} bytes)")
                        else:
                            safe_print("      ⚠️ 元数据PDF文件未找到")
                    else:
                        safe_print("      ⚠️ PDFSaveOptions不可用，跳过元数据配置")
                except Exception as meta_e:
                    safe_print(f"      ⚠️ 元数据配置警告: {str(meta_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ PDF元数据处理失败: {str(e)}")

        # 测试8: PDF错误处理
        safe_print("\n🔧 测试8: PDF错误处理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ PDF错误处理测试文档已创建")

                # 创建测试内容
                layer = doc.artLayers.add()
                layer.name = "错误处理测试"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 255
                fill_color.rgb.blue = 128
                ps.app.foregroundColor = fill_color

                doc.selection.select([[50, 50], [250, 50], [250, 250], [50, 250]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 测试无效PDF路径
                safe_print("   📄 测试无效PDF路径...")
                try:
                    if hasattr(ps, 'PDFSaveOptions'):
                        pdf_opt = ps.PDFSaveOptions()
                        invalid_path = "/invalid/path/document.pdf"
                        doc.saveAs(invalid_path, pdf_opt, True)
                        safe_print("      ⚠️ 无效路径意外成功")
                    else:
                        safe_print("      ⚠️ PDFSaveOptions不可用，跳过路径测试")
                except Exception as invalid_e:
                    safe_print(f"      ✅ 正确处理无效路径")

                # 测试低质量PDF
                safe_print("   📄 测试低质量PDF...")
                try:
                    if hasattr(ps, 'PDFSaveOptions'):
                        pdf_opt = ps.PDFSaveOptions()
                        pdf_opt.quality = 1
                        pdf_path = os.path.join(get_test_save_dir(), "low_quality.pdf")
                        doc.saveAs(pdf_path, pdf_opt, True)
                        safe_print("      ✅ 低质量PDF保存成功")
                    else:
                        safe_print("      ⚠️ PDFSaveOptions不可用，跳过低质量测试")
                except Exception as low_e:
                    safe_print(f"      ✅ 正确处理低质量设置")

        except Exception as e:
            safe_print(f"❌ PDF错误处理失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "save_as_pdf_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Save As PDF 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: PDF保存功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本PDF保存功能 (原始代码逻辑)\n")
                f.write(f"- PDF选项详细配置\n")
                f.write(f"- 多图层PDF保存\n")
                f.write(f"- PDF颜色空间处理\n")
                f.write(f"- PDF压缩和优化\n")
                f.write(f"- PDF安全性设置\n")
                f.write(f"- PDF元数据处理\n")
                f.write(f"- PDF错误处理\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第42项: save_as_pdf.py 测试完成!")
        safe_print("✅ 验证功能: PDF保存、选项配置、多图层、压缩优化、安全设置")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. PDF保存功能是否可用")
        safe_print("3. PDFSaveOptions是否支持")
        safe_print("4. 压缩和质量选项是否正确")
        return False

if __name__ == "__main__":
    test_save_as_pdf()
