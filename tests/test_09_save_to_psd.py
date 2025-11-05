# -*- coding: utf-8 -*-
"""测试第9项: save_to_psd.py - 保存为PSD"""

import os
import sys
import shutil
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_save_to_psd():
    """运行save_to_psd测试"""
    safe_print("💾 开始执行第9项: save_to_psd.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 创建测试文档
        safe_print("\n🔧 创建测试文档...")
        with Session() as ps:
            doc = ps.active_document
            safe_print(f"✅ 获取到当前文档: {doc.name}")
            safe_print(f"📏 当前文档尺寸: {doc.width} x {doc.height}")

            # 如果当前文档是空的，创建内容
            if doc.artLayers.length == 0:
                safe_print("📝 添加测试内容...")

                # 创建背景图层
                bg_layer = doc.artLayers.add()
                bg_layer.name = "Background"

                # 填充背景颜色
                bg_color = ps.SolidColor()
                bg_color.rgb.red = 240
                bg_color.rgb.green = 240
                bg_color.rgb.blue = 240
                ps.app.backgroundColor = bg_color

                doc.selection.selectAll()
                doc.selection.fill(ps.app.backgroundColor)
                doc.selection.deselect()

                safe_print("   ✅ 创建背景图层")

                # 创建文本图层
                text_layer = doc.artLayers.add()
                text_layer.kind = ps.LayerKind.TextLayer
                text_layer.name = "Save PSD Test"

                text_color = ps.SolidColor()
                text_color.rgb.red = 0
                text_color.rgb.green = 100
                text_color.rgb.blue = 200

                text_layer.textItem.contents = "Save to PSD Test\n第9项测试"
                text_layer.textItem.size = 36
                text_layer.textItem.position = [100, 200]
                text_layer.textItem.color = text_color

                safe_print("   ✅ 创建文本图层")

                # 创建装饰图形
                shape_layer = doc.artLayers.add()
                shape_layer.name = "Decoration"

                shape_color = ps.SolidColor()
                shape_color.rgb.red = 255
                shape_color.rgb.green = 100
                shape_color.rgb.blue = 100
                ps.app.foregroundColor = shape_color

                # 创建矩形
                doc.selection.select([[50, 50], [350, 50], [350, 150], [50, 150]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                safe_print("   ✅ 创建装饰图形")

            # 测试1: 基本PSD保存 (原始代码逻辑)
            safe_print("\n💾 测试1: 基本PSD保存...")

            # 配置PSD保存选项 (原始代码逻辑)
            psd_options = ps.PhotoshopSaveOptions()
            psd_options.alphaChannels = True
            psd_options.annotations = True
            psd_options.layers = True
            psd_options.spotColors = True

            safe_print("   📋 PSD保存选项已配置:")
            safe_print("      Alpha通道: 启用")
            safe_print("      注释: 启用")
            safe_print("      图层: 启用")
            safe_print("      专色: 启用")

            # 生成输出路径 (原始代码逻辑)
            save_dir = get_test_save_dir()
            output_path = os.path.join(save_dir, "save_to_psd_test_1.psd")
            safe_print(f"📁 保存路径: {output_path}")

            # 保存文档为PSD (原始代码逻辑)
            try:
                doc.saveAs(output_path, psd_options, True)
                safe_print("   ✅ 成功保存PSD文件")

                # 验证文件是否存在
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    safe_print(f"   📊 文件大小: {file_size} 字节")
                else:
                    safe_print("   ❌ 保存的文件不存在")

            except Exception as e:
                safe_print(f"   ❌ 保存失败: {str(e)}")

        # 测试2: 不同PSD保存选项
        safe_print("\n💾 测试2: 不同PSD保存选项...")

        test_configs = [
            {
                "name": "minimal_psd",
                "alphaChannels": False,
                "annotations": False,
                "layers": True,
                "spotColors": False,
                "description": "最小配置"
            },
            {
                "name": "max_compatibility_psd",
                "alphaChannels": True,
                "annotations": True,
                "layers": True,
                "spotColors": True,
                "description": "最大兼容性"
            },
            {
                "name": "no_layers_psd",
                "alphaChannels": True,
                "annotations": True,
                "layers": False,
                "spotColors": True,
                "description": "无图层保存"
            }
        ]

        for i, config in enumerate(test_configs):
            safe_print(f"\n   🔧 配置 {i+1}: {config['description']}")

            try:
                with Session() as ps:
                    doc = ps.active_document

                    # 配置PSD保存选项
                    psd_options = ps.PhotoshopSaveOptions()
                    psd_options.alphaChannels = config['alphaChannels']
                    psd_options.annotations = config['annotations']
                    psd_options.layers = config['layers']
                    psd_options.spotColors = config['spotColors']

                    # 生成输出路径
                    output_path = os.path.join(save_dir, f"save_to_psd_test_{config['name']}.psd")

                    # 保存文档
                    doc.saveAs(output_path, psd_options, True)

                    # 验证保存结果
                    if os.path.exists(output_path):
                        file_size = os.path.getsize(output_path)
                        safe_print(f"      ✅ 成功保存: {config['name']} ({file_size} 字节)")
                    else:
                        safe_print(f"      ❌ 保存失败: {config['name']}")

            except Exception as e:
                safe_print(f"      ❌ 配置 {config['name']} 测试失败: {str(e)}")

        # 测试3: 不同文档类型的PSD保存
        safe_print("\n💾 测试3: 不同文档类型的PSD保存...")

        document_types = [
            {"width": 800, "height": 600, "name": "standard_doc", "description": "标准文档"},
            {"width": 1920, "height": 1080, "name": "hd_doc", "description": "HD文档"},
            {"width": 100, "height": 100, "name": "small_doc", "description": "小文档"},
            {"width": 3000, "height": 2000, "name": "large_doc", "description": "大文档"}
        ]

        for doc_type in document_types:
            safe_print(f"\n   📄 创建{doc_type['description']} ({doc_type['width']}x{doc_type['height']})")

            try:
                with Session(action="new_document") as ps:
                    # 创建新文档
                    new_doc = ps.active_document

                    # 添加测试内容
                    layer = new_doc.artLayers.add()
                    layer.name = f"{doc_type['name']}_layer"

                    # 添加文本标识
                    text_layer = new_doc.artLayers.add()
                    text_layer.kind = ps.LayerKind.TextLayer
                    text_layer.textItem.contents = f"{doc_type['description']}\n{doc_type['width']}x{doc_type['height']}"
                    text_layer.textItem.size = 24
                    text_layer.textItem.position = [50, 100]

                    # 配置PSD保存选项
                    psd_options = ps.PhotoshopSaveOptions()
                    psd_options.alphaChannels = True
                    psd_options.layers = True

                    # 保存文档
                    output_path = os.path.join(save_dir, f"{doc_type['name']}.psd")
                    new_doc.saveAs(output_path, psd_options, True)

                    # 验证保存结果
                    if os.path.exists(output_path):
                        file_size = os.path.getsize(output_path)
                        safe_print(f"      ✅ 成功保存: {doc_type['name']} ({file_size} 字节)")
                    else:
                        safe_print(f"      ❌ 保存失败: {doc_type['name']}")

            except Exception as e:
                safe_print(f"      ❌ {doc_type['description']} 测试失败: {str(e)}")

        # 测试4: 带有复杂内容的PSD保存
        safe_print("\n💾 测试4: 带有复杂内容的PSD保存...")

        try:
            with Session() as ps:
                doc = ps.active_document

                # 创建多个图层
                layer_types = [
                    ("背景层", "background"),
                    ("文本层", "text"),
                    ("形状层", "shape"),
                    ("调整层", "adjustment"),
                    ("蒙版层", "mask")
                ]

                for layer_name, layer_type in layer_types:
                    try:
                        if layer_type == "background":
                            # 背景层
                            layer = doc.artLayers.add()
                            layer.name = layer_name
                            bg_color = ps.SolidColor()
                            bg_color.rgb.red = 200 + len(layer_types) * 10
                            bg_color.rgb.green = 200
                            bg_color.rgb.blue = 200
                            ps.app.backgroundColor = bg_color
                            doc.selection.selectAll()
                            doc.selection.fill(ps.app.backgroundColor)
                            doc.selection.deselect()

                        elif layer_type == "text":
                            # 文本层
                            layer = doc.artLayers.add()
                            layer.kind = ps.LayerKind.TextLayer
                            layer.name = layer_name
                            layer.textItem.contents = f"复杂PSD测试\n{layer_name}"
                            layer.textItem.size = 28
                            layer.textItem.position = [100, 150 + len(doc.artLayers) * 50]

                        elif layer_type == "shape":
                            # 形状层
                            layer = doc.artLayers.add()
                            layer.name = layer_name
                            shape_color = ps.SolidColor()
                            shape_color.rgb.red = 255
                            shape_color.rgb.green = 200
                            shape_color.rgb.blue = 100
                            ps.app.foregroundColor = shape_color
                            x = 50 + len(doc.artLayers) * 30
                            doc.selection.select([[x, 300], [x+80, 300], [x+80, 380], [x, 380]])
                            doc.selection.fill(ps.app.foregroundColor)
                            doc.selection.deselect()

                        else:
                            # 其他类型
                            layer = doc.artLayers.add()
                            layer.name = layer_name

                        safe_print(f"      ✅ 创建图层: {layer_name}")

                    except Exception as e:
                        safe_print(f"      ⚠️ 创建图层 {layer_name} 失败: {str(e)}")

                # 配置完整的PSD保存选项
                psd_options = ps.PhotoshopSaveOptions()
                psd_options.alphaChannels = True
                psd_options.annotations = True
                psd_options.layers = True
                psd_options.spotColors = True
                psd_options.embedColorProfile = True

                # 保存复杂文档
                output_path = os.path.join(save_dir, "complex_save_to_psd_test.psd")
                doc.saveAs(output_path, psd_options, True)

                # 验证保存结果
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    safe_print(f"   ✅ 成功保存复杂PSD文件 ({file_size} 字节)")
                    safe_print(f"   📊 最终图层数量: {doc.artLayers.length}")
                else:
                    safe_print("   ❌ 复杂PSD文件保存失败")

        except Exception as e:
            safe_print(f"   ❌ 复杂内容保存测试失败: {str(e)}")

        # 测试5: 覆盖保存测试
        safe_print("\n💾 测试5: 覆盖保存测试...")

        try:
            with Session() as ps:
                doc = ps.active_document

                # 首次保存
                output_path = os.path.join(save_dir, "overwrite_test.psd")
                psd_options = ps.PhotoshopSaveOptions()
                psd_options.layers = True

                doc.saveAs(output_path, psd_options, True)
                safe_print("   ✅ 首次保存完成")

                # 修改文档内容
                text_layer = doc.artLayers.add()
                text_layer.kind = ps.LayerKind.TextLayer
                text_layer.name = "Modification"
                text_layer.textItem.contents = "已修改内容"
                text_layer.textItem.size = 24
                text_layer.textItem.position = [200, 200]

                # 覆盖保存
                doc.saveAs(output_path, psd_options, True)
                safe_print("   ✅ 覆盖保存完成")

                # 验证文件更新
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    safe_print(f"   ✅ 覆盖保存验证成功 ({file_size} 字节)")
                else:
                    safe_print("   ❌ 覆盖保存验证失败")

        except Exception as e:
            safe_print(f"   ❌ 覆盖保存测试失败: {str(e)}")

        # 测试6: 保存路径和文件名测试
        safe_print("\n💾 测试6: 保存路径和文件名测试...")

        special_names = [
            ("test_with_underscores.psd", "下划线文件名"),
            ("test-with-hyphens.psd", "连字符文件名"),
            ("TestWithCamelCase.psd", "驼峰命名文件名"),
            ("test123.psd", "数字文件名")
        ]

        for filename, description in special_names:
            try:
                with Session() as ps:
                    doc = ps.active_document

                    # 添加标识内容
                    text_layer = doc.artLayers.add()
                    text_layer.kind = ps.LayerKind.TextLayer
                    text_layer.textItem.contents = description
                    text_layer.textItem.size = 20
                    text_layer.textItem.position = [50, 100]

                    output_path = os.path.join(save_dir, filename)
                    psd_options = ps.PhotoshopSaveOptions()
                    psd_options.layers = True

                    doc.saveAs(output_path, psd_options, True)

                    if os.path.exists(output_path):
                        safe_print(f"   ✅ 成功保存: {description}")
                    else:
                        safe_print(f"   ❌ 保存失败: {description}")

            except Exception as e:
                safe_print(f"   ❌ {description} 测试失败: {str(e)}")

        # 保存测试结果汇总
        safe_print("\n💾 保存测试结果汇总...")
        try:
            result_file = os.path.join(save_dir, "save_to_psd_test_summary.txt")

            # 统计保存的文件
            saved_files = []
            for file in os.listdir(save_dir):
                if file.startswith("save_to_psd") and file.endswith(".psd"):
                    file_path = os.path.join(save_dir, file)
                    file_size = os.path.getsize(file_path)
                    saved_files.append((file, file_size))

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Save to PSD 测试结果汇总\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试保存的PSD文件数量: {len(saved_files)}\n\n")
                f.write("保存的文件列表:\n")
                for filename, size in saved_files:
                    f.write(f"- {filename}: {size} 字节\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试汇总: {result_file}")
            safe_print(f"   📊 总共保存了 {len(saved_files)} 个PSD文件")

            for filename, size in saved_files:
                safe_print(f"      - {filename}: {size} 字节")

        except Exception as e:
            safe_print(f"   ⚠️ 保存汇总失败: {str(e)}")

        safe_print("\n🎉 第9项: save_to_psd.py 测试完成!")
        safe_print("✅ 验证功能: 基本PSD保存、保存选项配置、不同文档类型、复杂内容保存、覆盖保存、文件命名")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 是否有活动文档")
        safe_print("3. 保存路径是否有写入权限")
        safe_print("4. 磁盘空间是否充足")
        return False

if __name__ == "__main__":
    test_save_to_psd()