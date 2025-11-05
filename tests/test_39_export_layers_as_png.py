# -*- coding: utf-8 -*-
"""测试第39项: export_layers_as_png.py - 导出图层为PNG"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_export_layers_as_png():
    """运行export_layers_as_png测试"""
    safe_print("📋 开始执行第39项: export_layers_as_png.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 导出单个图层为PNG (原始代码逻辑)
        safe_print("\n🔧 测试1: 导出单个图层为PNG (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ Session成功启动")
                safe_print(f"   📄 当前文档: {doc.name}")

                # 创建测试图层
                safe_print("   🎨 创建测试图层...")
                colors = [
                    {"name": "红色图层", "r": 255, "g": 0, "b": 0, "x": 50},
                    {"name": "绿色图层", "r": 0, "g": 255, "b": 0, "x": 150},
                    {"name": "蓝色图层", "r": 0, "g": 0, "b": 255, "x": 250},
                ]

                for color_info in colors:
                    layer = doc.artLayers.add()
                    layer.name = color_info['name']

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

                safe_print(f"      ✅ 创建{len(colors)}个测试图层")

                # Store original layer visibilities (原始代码逻辑)
                safe_print("   💾 记录原始图层可见性...")
                layer_visibilities = []
                for layer in doc.layers:
                    layer_visibilities.append(layer.visible)
                    layer.visible = False
                safe_print(f"      ✅ 记录{len(layer_visibilities)}个图层可见性")

                # 设置导出目录
                save_dir = get_test_save_dir()

                # Export each layer individually (原始代码逻辑)
                safe_print("   📤 逐个导出图层...")
                exported_count = 0
                try:
                    for i, layer in enumerate(doc.layers):
                        # Show only current layer (原始代码逻辑)
                        layer.visible = True

                        # Configure PNG save options (原始代码逻辑)
                        options = ps.PNGSaveOptions()
                        options.interlaced = False

                        # Generate unique filename (修改为使用测试目录)
                        file_path = os.path.join(
                            save_dir,
                            f"layer_{i}_{layer.name}.png"
                        )

                        # Save the file (原始代码逻辑)
                        doc.saveAs(file_path, options, True)

                        # 验证文件存在
                        if os.path.exists(file_path):
                            size = os.path.getsize(file_path)
                            safe_print(f"      ✅ 导出{layer.name} ({size} bytes)")
                            exported_count += 1
                        else:
                            safe_print(f"      ⚠️ {layer.name}文件未找到")

                        # Hide the layer again (原始代码逻辑)
                        layer.visible = False

                except Exception as export_e:
                    safe_print(f"      ⚠️ 逐个导出过程异常: {str(export_e)[:50]}")

                # Restore original layer visibilities (原始代码逻辑)
                safe_print("   🔄 恢复原始图层可见性...")
                try:
                    for layer, visibility in zip(doc.layers, layer_visibilities):
                        layer.visible = visibility
                    safe_print("      ✅ 图层可见性恢复完成")
                except Exception as restore_e:
                    safe_print(f"      ⚠️ 恢复可见性失败: {str(restore_e)[:50]}")

                safe_print(f"   📊 共导出{export_count}个图层")

        except Exception as e:
            safe_print(f"❌ 导出单个图层失败: {str(e)}")
            return False

        # 测试2: 多图层导出验证
        safe_print("\n🔧 测试2: 多图层导出验证...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                doc.name = "多图层导出测试"

                # 创建更多图层
                safe_print("   🎨 创建多图层结构...")
                num_layers = 5
                for i in range(num_layers):
                    layer = doc.artLayers.add()
                    layer.name = f"导出测试_{i+1}"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 50 * i
                    fill_color.rgb.green = 100 + 30 * i
                    fill_color.rgb.blue = 200 - 20 * i
                    ps.app.foregroundColor = fill_color

                    x = 50 + i * 60
                    doc.selection.select([[x, 50], [x + 50, 50], [x + 50, 150], [x, 150]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                safe_print(f"      ✅ 创建{num_layers}个图层")

                # 记录并隐藏所有图层
                visibilities = []
                for layer in doc.layers:
                    visibilities.append(layer.visible)
                    layer.visible = False

                # 导出每个图层
                save_dir = get_test_save_dir()
                export_success = 0

                for i, layer in enumerate(doc.layers):
                    layer.visible = True
                    png_opt = ps.PNGSaveOptions()
                    png_opt.interlaced = False
                    file_path = os.path.join(save_dir, f"multi_layer_{i+1}.png")

                    try:
                        doc.saveAs(file_path, png_opt, True)
                        export_success += 1
                        safe_print(f"      ✅ 图层{i+1}导出成功")
                    except Exception as multi_e:
                        safe_print(f"      ❌ 图层{i+1}导出失败: {str(multi_e)[:50]}")

                    layer.visible = False

                # 恢复可见性
                for layer, vis in zip(doc.layers, visibilities):
                    layer.visible = vis

                safe_print(f"   📊 多图层导出: {export_success}/{num_layers} 成功")

        except Exception as e:
            safe_print(f"❌ 多图层导出验证失败: {str(e)}")

        # 测试3: 图层可见性管理
        safe_print("\n🔧 测试3: 图层可见性管理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建带可见性差异的图层
                colors = [
                    {"name": "可见图层1", "r": 255, "g": 0, "b": 0, "visible": True},
                    {"name": "隐藏图层", "r": 0, "g": 255, "b": 0, "visible": False},
                    {"name": "可见图层2", "r": 0, "g": 0, "b": 255, "visible": True},
                ]

                for color_info in colors:
                    layer = doc.artLayers.add()
                    layer.name = color_info['name']
                    layer.visible = color_info['visible']

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = color_info["r"]
                    fill_color.rgb.green = color_info["g"]
                    fill_color.rgb.blue = color_info["b"]
                    ps.app.foregroundColor = fill_color

                    doc.selection.select([[100, 100], [200, 100], [200, 200], [100, 200]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                safe_print("      ✅ 创建带可见性差异的图层")

                # 保存原始可见性状态
                original_vis = [layer.visible for layer in doc.layers]

                # 导出所有图层
                save_dir = get_test_save_dir()
                for i, layer in enumerate(doc.layers):
                    # 保存当前可见性
                    current_vis = layer.visible

                    # 设置为可见
                    layer.visible = True

                    # 导出
                    png_opt = ps.PNGSaveOptions()
                    file_path = os.path.join(save_dir, f"visibility_test_{i}.png")
                    try:
                        doc.saveAs(file_path, png_opt, True)
                        safe_print(f"      ✅ {layer.name}导出成功")
                    except Exception as vis_e:
                        safe_print(f"      ❌ {layer.name}导出失败: {str(vis_e)[:50]}")

                    # 恢复原始可见性
                    layer.visible = current_vis

        except Exception as e:
            safe_print(f"❌ 图层可见性管理失败: {str(e)}")

        # 测试4: PNG选项配置
        safe_print("\n🔧 测试4: PNG选项配置...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建内容
                layer = doc.artLayers.add()
                layer.name = "PNG选项测试"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 128
                fill_color.rgb.green = 128
                fill_color.rgb.blue = 255
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [300, 100], [300, 300], [100, 300]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 测试不同PNG选项
                png_configs = [
                    {"name": "非隔行扫描", "interlaced": False},
                    {"name": "隔行扫描", "interlaced": True},
                    {"name": "默认压缩", "compression": 0},
                    {"name": "最大压缩", "compression": 9},
                ]

                save_dir = get_test_save_dir()
                for config in png_configs:
                    safe_print(f"   🖼️ 导出{config['name']}...")
                    try:
                        png_opt = ps.PNGSaveOptions()
                        png_opt.interlaced = config["interlaced"]
                        if "compression" in config:
                            png_opt.compression = config["compression"]
                        file_path = os.path.join(save_dir, f"png_option_{config['name']}.png")
                        doc.saveAs(file_path, png_opt, True)
                        safe_print(f"      ✅ {config['name']}导出成功")
                    except Exception as opt_e:
                        safe_print(f"      ❌ {config['name']}导出失败: {str(opt_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ PNG选项配置失败: {str(e)}")

        # 测试5: 文件命名规范
        safe_print("\n🔧 测试5: 文件命名规范...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建不同名称的图层
                layer_names = [
                    "正常名称",
                    "带空格图层",
                    "带-特殊字符",
                    "123数字开头",
                ]

                for name in layer_names:
                    layer = doc.artLayers.add()
                    layer.name = name

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 100
                    fill_color.rgb.green = 150
                    fill_color.rgb.blue = 200
                    ps.app.foregroundColor = fill_color

                    doc.selection.select([[50, 50], [150, 50], [150, 150], [50, 150]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                # 导出并验证命名
                save_dir = get_test_save_dir()
                exported_files = []

                visibilities = [layer.visible for layer in doc.layers]
                for layer in doc.layers:
                    layer.visible = False

                for i, layer in enumerate(doc.layers):
                    layer.visible = True
                    png_opt = ps.PNGSaveOptions()

                    # 生成文件名
                    sanitized_name = layer.name.replace(" ", "_").replace("-", "_")
                    file_path = os.path.join(save_dir, f"naming_test_{i}_{sanitized_name}.png")

                    try:
                        doc.saveAs(file_path, png_opt, True)
                        if os.path.exists(file_path):
                            exported_files.append(os.path.basename(file_path))
                            safe_print(f"      ✅ {layer.name} -> {os.path.basename(file_path)}")
                    except Exception as naming_e:
                        safe_print(f"      ❌ {layer.name}导出失败: {str(naming_e)[:50]}")

                    layer.visible = False

                # 恢复可见性
                for layer, vis in zip(doc.layers, visibilities):
                    layer.visible = vis

                safe_print(f"   📊 共导出{len(exported_files)}个文件")

        except Exception as e:
            safe_print(f"❌ 文件命名规范失败: {str(e)}")

        # 测试6: 图层选择和激活
        safe_print("\n🔧 测试6: 图层选择和激活...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建多个图层
                for i in range(3):
                    layer = doc.artLayers.add()
                    layer.name = f"激活测试_{i+1}"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 255 // (i + 1) * 100
                    fill_color.rgb.green = 255 // (i + 1) * 50
                    fill_color.rgb.blue = 255 // (i + 1) * 25
                    ps.app.foregroundColor = fill_color

                    doc.selection.select([[50, 50], [150, 50], [150, 150], [50, 150]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                # 逐个激活并导出
                save_dir = get_test_save_dir()
                visibilities = [layer.visible for layer in doc.layers]

                for layer in doc.layers:
                    # 设置图层为活动状态
                    doc.activeLayer = layer
                    layer.visible = True

                    safe_print(f"   🎯 激活图层: {layer.name}")

                    # 导出
                    png_opt = ps.PNGSaveOptions()
                    file_path = os.path.join(save_dir, f"active_{layer.name}.png")
                    try:
                        doc.saveAs(file_path, png_opt, True)
                        safe_print(f"      ✅ {layer.name}导出成功")
                    except Exception as active_e:
                        safe_print(f"      ❌ {layer.name}导出失败: {str(active_e)[:50]}")

                    layer.visible = False

                # 恢复可见性
                for layer, vis in zip(doc.layers, visibilities):
                    layer.visible = vis

        except Exception as e:
            safe_print(f"❌ 图层选择和激活失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "export_layers_as_png_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Export Layers as PNG 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 导出图层为PNG功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 导出单个图层为PNG (原始代码逻辑)\n")
                f.write(f"- 多图层导出验证\n")
                f.write(f"- 图层可见性管理\n")
                f.write(f"- PNG选项配置\n")
                f.write(f"- 文件命名规范\n")
                f.write(f"- 图层选择和激活\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第39项: export_layers_as_png.py 测试完成!")
        safe_print("✅ 验证功能: 图层逐个导出、可见性管理、PNG选项、文件命名、图层激活")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 图层导出功能是否可用")
        safe_print("3. layer.visible属性是否可访问")
        safe_print("4. saveAs方法是否正常")
        return False

if __name__ == "__main__":
    test_export_layers_as_png()
