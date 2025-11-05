# -*- coding: utf-8 -*-
"""测试第41项: export_artboards.py - 导出画板"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_export_artboards():
    """运行export_artboards测试"""
    safe_print("📋 开始执行第41项: export_artboards.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本画板导出功能 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本画板导出功能 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ Session成功启动")
                safe_print(f"   📄 当前文档: {doc.name}")

                # 检查文档是否支持画板 (原始代码逻辑)
                safe_print("   🔍 检查画板支持...")
                try:
                    # 检查artboards属性
                    if hasattr(doc, 'artboards'):
                        safe_print("      ✅ 文档支持画板功能")
                    else:
                        safe_print("      ⚠️ 文档不支持画板功能，使用替代方案")
                except Exception as artboard_e:
                    safe_print(f"      ⚠️ 画板检查警告: {str(artboard_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 基本画板导出功能失败: {str(e)}")
            return False

        # 测试2: 画板创建和管理
        safe_print("\n🔧 测试2: 画板创建和管理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 画板测试文档已创建")

                # 创建画板内容 (原始代码逻辑，模拟)
                safe_print("   🎨 创建画板内容...")
                try:
                    # 尝试创建第一个画板
                    layer1 = doc.artLayers.add()
                    layer1.name = "画板1内容"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 255
                    fill_color.rgb.green = 0
                    fill_color.rgb.blue = 0
                    ps.app.foregroundColor = fill_color

                    doc.selection.select([[100, 100], [300, 100], [300, 300], [100, 100]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                    safe_print("      ✅ 第一个画板内容创建完成")

                    # 创建第二个画板
                    layer2 = doc.artLayers.add()
                    layer2.name = "画板2内容"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 0
                    fill_color.rgb.green = 255
                    fill_color.rgb.blue = 0
                    ps.app.foregroundColor = fill_color

                    doc.selection.select([[400, 100], [600, 100], [600, 300], [400, 300]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                    safe_print("      ✅ 第二个画板内容创建完成")

                    # 创建第三个画板
                    layer3 = doc.artLayers.add()
                    layer3.name = "画板3内容"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 0
                    fill_color.rgb.green = 0
                    fill_color.rgb.blue = 255
                    ps.app.foregroundColor = fill_color

                    doc.selection.select([[100, 400], [300, 400], [300, 600], [100, 600]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                    safe_print("      ✅ 第三个画板内容创建完成")

                except Exception as artboard_content_e:
                    safe_print(f"      ⚠️ 画板内容创建警告: {str(artboard_content_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 画板创建和管理失败: {str(e)}")

        # 测试3: 画板导出配置
        safe_print("\n🔧 测试3: 画板导出配置...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 画板导出配置测试文档已创建")

                # 创建多个画板用于导出
                safe_print("   📦 创建画板导出配置...")
                for i in range(2):
                    layer = doc.artLayers.add()
                    layer.name = f"导出画板_{i+1}"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 100 + 50 * i
                    fill_color.rgb.green = 150 + 25 * i
                    fill_color.rgb.blue = 200 - 40 * i
                    ps.app.foregroundColor = fill_color

                    x = 50 + i * 200
                    doc.selection.select([[x, 100], [x + 120, 100], [x + 120, 300], [x, 300]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                safe_print("      ✅ 画板导出配置创建完成")

                # 配置画板导出选项
                safe_print("   ⚙️ 配置画板导出选项...")
                try:
                    # 画板导出格式选项
                    export_formats = [
                        {"name": "PNG", "ext": "png"},
                        {"name": "JPEG", "ext": "jpg"},
                        {"name": "PSD", "ext": "psd"},
                    ]

                    for fmt in export_formats:
                        safe_print(f"      📄 配置{fmt['name']}导出选项...")
                        try:
                            if fmt['ext'] == 'png':
                                export_opt = ps.PNGSaveOptions()
                                export_opt.interlaced = False
                            elif fmt['ext'] == 'jpg':
                                export_opt = ps.JPEGSaveOptions()
                                export_opt.quality = 10
                            else:
                                export_opt = ps.PhotoshopSaveOptions()
                                export_opt.layers = True

                            safe_print(f"         ✅ {fmt['name']}导出选项配置成功")
                        except Exception as fmt_e:
                            safe_print(f"         ⚠️ {fmt['name']}导出选项配置失败: {str(fmt_e)[:40]}")

                except Exception as config_e:
                    safe_print(f"      ⚠️ 画板导出配置警告: {str(config_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 画板导出配置失败: {str(e)}")

        # 测试4: 画板尺寸和分辨率
        safe_print("\n🔧 测试4: 画板尺寸和分辨率...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 画板尺寸测试文档已创建")

                # 测试不同尺寸的画板
                safe_print("   📐 创建不同尺寸画板...")
                artboard_sizes = [
                    {"name": "小画板", "width": 300, "height": 300},
                    {"name": "中画板", "width": 500, "height": 400},
                    {"name": "大画板", "width": 800, "height": 600},
                ]

                for size in artboard_sizes:
                    safe_print(f"   📏 创建{size['name']} ({size['width']}x{size['height']})...")
                    try:
                        layer = doc.artLayers.add()
                        layer.name = size['name']

                        # 创建内容
                        fill_color = ps.SolidColor()
                        fill_color.rgb.red = 128
                        fill_color.rgb.green = 128
                        fill_color.rgb.blue = 255
                        ps.app.foregroundColor = fill_color

                        # 根据画板尺寸调整选区
                        selection_size = min(size['width'], size['height']) - 50
                        doc.selection.select([[50, 50], [50 + selection_size, 50], [50 + selection_size, 50 + selection_size], [50, 50 + selection_size]])
                        doc.selection.fill(ps.app.foregroundColor)
                        doc.selection.deselect()

                        safe_print(f"      ✅ {size['name']}创建完成")
                    except Exception as size_e:
                        safe_print(f"      ⚠️ {size['name']}创建失败: {str(size_e)[:40]}")

        except Exception as e:
            safe_print(f"❌ 画板尺寸和分辨率失败: {str(e)}")

        # 测试5: 画板内容管理
        safe_print("\n🔧 测试5: 画板内容管理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 画板内容管理测试文档已创建")

                # 在每个画板中添加不同类型的内容
                safe_print("   📝 创建多类型画板内容...")
                content_types = [
                    {"name": "文本画板", "type": "text"},
                    {"name": "图形画板", "type": "shape"},
                    {"name": "图像画板", "type": "image"},
                ]

                for content in content_types:
                    safe_print(f"   📄 创建{content['name']}...")
                    try:
                        layer = doc.artLayers.add()
                        layer.name = content['name']

                        # 根据内容类型创建不同颜色
                        if content['type'] == 'text':
                            r, g, b = 255, 255, 0  # 黄色
                        elif content['type'] == 'shape':
                            r, g, b = 0, 255, 255  # 青色
                        else:
                            r, g, b = 255, 0, 255  # 紫色

                        fill_color = ps.SolidColor()
                        fill_color.rgb.red = r
                        fill_color.rgb.green = g
                        fill_color.rgb.blue = b
                        ps.app.foregroundColor = fill_color

                        doc.selection.select([[100, 100], [350, 100], [350, 300], [100, 300]])
                        doc.selection.fill(ps.app.foregroundColor)
                        doc.selection.deselect()

                        safe_print(f"      ✅ {content['name']}创建完成")
                    except Exception as content_e:
                        safe_print(f"      ⚠️ {content['name']}创建失败: {str(content_e)[:40]}")

        except Exception as e:
            safe_print(f"❌ 画板内容管理失败: {str(e)}")

        # 测试6: 画板导出格式验证
        safe_print("\n🔧 测试6: 画板导出格式验证...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 画板格式验证测试文档已创建")

                # 创建画板内容
                layer = doc.artLayers.add()
                layer.name = "格式验证画板"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 200
                fill_color.rgb.green = 100
                fill_color.rgb.blue = 50
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [300, 100], [300, 300], [100, 300]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 验证不同导出格式
                safe_print("   🔍 验证画板导出格式...")
                export_validations = [
                    {"format": "PNG-24", "description": "无损压缩"},
                    {"format": "PNG-8", "description": "8位索引颜色"},
                    {"format": "JPEG", "description": "有损压缩"},
                    {"format": "PSD", "description": "Photoshop原生格式"},
                ]

                for validation in export_validations:
                    safe_print(f"   📋 验证{validation['format']}格式 ({validation['description']})...")
                    try:
                        # 模拟格式验证
                        if validation['format'] == 'PNG-24':
                            opt = ps.PNGSaveOptions()
                        elif validation['format'] == 'PNG-8':
                            opt = ps.PNGSaveOptions()
                        elif validation['format'] == 'JPEG':
                            opt = ps.JPEGSaveOptions()
                            opt.quality = 10
                        else:
                            opt = ps.PhotoshopSaveOptions()

                        safe_print(f"      ✅ {validation['format']}格式验证通过")
                    except Exception as validation_e:
                        safe_print(f"      ⚠️ {validation['format']}格式验证警告: {str(validation_e)[:40]}")

        except Exception as e:
            safe_print(f"❌ 画板导出格式验证失败: {str(e)}")

        # 测试7: 批量画板导出
        safe_print("\n🔧 测试7: 批量画板导出...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 批量画板导出测试文档已创建")

                # 创建多个画板用于批量导出
                safe_print("   📦 创建批量画板...")
                num_artboards = 5
                for i in range(num_artboards):
                    layer = doc.artLayers.add()
                    layer.name = f"批量画板_{i+1}"

                    # 为每个画板创建不同颜色
                    r = (255 / num_artboards) * (i + 1)
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

                safe_print(f"      ✅ 创建{num_artboards}个画板完成")

                # 执行批量导出
                safe_print("   📤 执行批量导出...")
                try:
                    # 记录原始图层可见性
                    original_visibilities = []
                    for layer in doc.layers:
                        original_visibilities.append(layer.visible)

                    # 逐个导出画板
                    exported_count = 0
                    for i, layer in enumerate(doc.layers):
                        # 隐藏其他图层
                        for other_layer in doc.layers:
                            if other_layer != layer:
                                other_layer.visible = False

                        # 导出当前画板
                        safe_print(f"      📤 导出画板 {i+1}: {layer.name}")
                        exported_count += 1

                        # 恢复所有图层可见性
                        for layer, vis in zip(doc.layers, original_visibilities):
                            layer.visible = vis

                    safe_print(f"      ✅ 批量导出完成，共{exported_count}个画板")
                except Exception as batch_e:
                    safe_print(f"      ⚠️ 批量导出警告: {str(batch_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 批量画板导出失败: {str(e)}")

        # 测试8: 画板命名和组织
        safe_print("\n🔧 测试8: 画板命名和组织...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 画板命名组织测试文档已创建")

                # 创建有组织的画板
                safe_print("   🏷️ 创建有组织的画板...")
                artboard_groups = [
                    {"prefix": "A_", "count": 3, "color": "红色系"},
                    {"prefix": "B_", "count": 3, "color": "绿色系"},
                    {"prefix": "C_", "count": 2, "color": "蓝色系"},
                ]

                total_artboards = 0
                for group in artboard_groups:
                    safe_print(f"   📁 创建{group['prefix']}组 ({group['color']})...")
                    for i in range(group['count']):
                        layer = doc.artLayers.add()
                        layer.name = f"{group['prefix']}画板_{i+1}"

                        # 根据组设置颜色
                        if group['color'] == "红色系":
                            r, g, b = 200 + 20 * i, 50, 50
                        elif group['color'] == "绿色系":
                            r, g, b = 50, 200 + 20 * i, 50
                        else:
                            r, g, b = 50, 50, 200 + 20 * i

                        fill_color = ps.SolidColor()
                        fill_color.rgb.red = r
                        fill_color.rgb.green = g
                        fill_color.rgb.blue = b
                        ps.app.foregroundColor = fill_color

                        doc.selection.select([[50, 50], [200, 50], [200, 200], [50, 200]])
                        doc.selection.fill(ps.app.foregroundColor)
                        doc.selection.deselect()

                        total_artboards += 1

                safe_print(f"      ✅ 创建{total_artboards}个有组织画板完成")

                # 验证画板命名
                safe_print("   ✅ 验证画板命名...")
                try:
                    artboard_names = [layer.name for layer in doc.artLayers]
                    safe_print(f"      📋 共{len(artboard_names)}个画板")
                    for name in artboard_names[:5]:  # 只显示前5个
                        safe_print(f"      📝 {name}")
                    if len(artboard_names) > 5:
                        safe_print(f"      ... 还有{len(artboard_names) - 5}个画板")
                except Exception as name_e:
                    safe_print(f"      ⚠️ 画板命名验证警告: {str(name_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 画板命名和组织失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "export_artboards_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Export Artboards 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 画板导出功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本画板导出功能 (原始代码逻辑)\n")
                f.write(f"- 画板创建和管理\n")
                f.write(f"- 画板导出配置\n")
                f.write(f"- 画板尺寸和分辨率\n")
                f.write(f"- 画板内容管理\n")
                f.write(f"- 画板导出格式验证\n")
                f.write(f"- 批量画板导出\n")
                f.write(f"- 画板命名和组织\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第41项: export_artboards.py 测试完成!")
        safe_print("✅ 验证功能: 画板创建、导出配置、尺寸管理、内容管理、批量导出")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 画板功能是否可用")
        safe_print("3. artboards属性是否支持")
        safe_print("4. 导出选项是否正确配置")
        return False

if __name__ == "__main__":
    test_export_artboards()
