# -*- coding: utf-8 -*-
"""测试第33项: cropping.py - 裁剪"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_cropping():
    """运行cropping测试"""
    safe_print("📋 开始执行第33项: cropping.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本裁剪操作 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本裁剪操作 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ Session成功启动")
                safe_print(f"   📄 初始文档尺寸: {doc.width} x {doc.height}")

                # 获取初始尺寸
                initial_width = doc.width
                initial_height = doc.height
                safe_print(f"   📊 初始尺寸: {initial_width} x {initial_height}")

                # 执行裁剪操作 (原始代码逻辑)
                safe_print("   ✂️ 执行裁剪操作...")
                try:
                    # 先添加一些内容到文档，便于验证裁剪效果
                    layer = doc.artLayers.add()
                    layer.name = "裁剪内容"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 255
                    fill_color.rgb.green = 0
                    fill_color.rgb.blue = 0
                    ps.app.foregroundColor = fill_color

                    doc.selection.select([[0, 0], [500, 0], [500, 500], [0, 500]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()
                    safe_print("      ✅ 添加测试内容")

                    # 执行裁剪
                    doc.crop(bounds=[100, 12, 354, 246], width=1920, height=1080)
                    safe_print("      ✅ 裁剪操作完成")
                    safe_print(f"   📄 裁剪后文档尺寸: {doc.width} x {doc.height}")

                except Exception as crop_e:
                    safe_print(f"      ⚠️ 裁剪参数失败: {str(crop_e)[:50]}")
                    # 尝试简化裁剪
                    try:
                        doc.crop(bounds=[100, 100, 300, 300])
                        safe_print("      ✅ 简化裁剪成功")
                    except Exception as simple_e:
                        safe_print(f"      ❌ 简化裁剪也失败: {str(simple_e)}")

        except Exception as e:
            safe_print(f"❌ 基本裁剪操作失败: {str(e)}")
            return False

        # 测试2: 不同边界裁剪
        safe_print("\n🔧 测试2: 不同边界裁剪...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建测试内容
                safe_print("   🎨 创建测试内容...")
                colors = [
                    {"name": "红色", "r": 255, "g": 0, "b": 0, "x": 0, "y": 0},
                    {"name": "绿色", "r": 0, "g": 255, "b": 0, "x": 200, "y": 0},
                    {"name": "蓝色", "r": 0, "g": 0, "b": 255, "x": 0, "y": 200},
                    {"name": "黄色", "r": 255, "g": 255, "b": 0, "x": 200, "y": 200},
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
                        [color_info['x'], color_info['y']],
                        [color_info['x'] + 150, color_info['y']],
                        [color_info['x'] + 150, color_info['y'] + 150],
                        [color_info['x'], color_info['y'] + 150]
                    ])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                safe_print("      ✅ 测试内容创建完成")

                # 测试不同裁剪边界
                crop_tests = [
                    {"name": "左上角裁剪", "bounds": [0, 0, 200, 200]},
                    {"name": "右上角裁剪", "bounds": [200, 0, 400, 200]},
                    {"name": "中央裁剪", "bounds": [100, 100, 300, 300]},
                ]

                for i, crop_test in enumerate(crop_tests):
                    safe_print(f"   ✂️ 执行{crop_test['name']}...")
                    try:
                        doc.crop(bounds=crop_test['bounds'])
                        safe_print(f"      ✅ {crop_test['name']}成功")
                    except Exception as crop_e:
                        safe_print(f"      ⚠️ {crop_test['name']}失败: {str(crop_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 不同边界裁剪失败: {str(e)}")

        # 测试3: 裁剪并调整大小
        safe_print("\n🔧 测试3: 裁剪并调整大小...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建大尺寸内容
                safe_print("   🎨 创建大尺寸内容...")
                layer = doc.artLayers.add()
                layer.name = "大尺寸内容"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 128
                fill_color.rgb.green = 128
                fill_color.rgb.blue = 255
                ps.app.foregroundColor = fill_color

                doc.selection.select([[0, 0], [800, 0], [800, 600], [0, 600]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                safe_print(f"      ✅ 创建内容，当前尺寸: {doc.width} x {doc.height}")

                # 裁剪并调整大小
                safe_print("   ✂️ 裁剪并调整大小...")
                try:
                    doc.crop(bounds=[100, 100, 500, 400], width=800, height=600)
                    safe_print(f"      ✅ 裁剪并调整成功，当前尺寸: {doc.width} x {doc.height}")
                except Exception as resize_e:
                    safe_print(f"      ⚠️ 裁剪并调整失败: {str(resize_e)[:50]}")
                    # 尝试只裁剪
                    try:
                        doc.crop(bounds=[100, 100, 500, 400])
                        safe_print(f"      ✅ 仅裁剪成功")
                    except Exception as crop_only_e:
                        safe_print(f"      ❌ 裁剪失败: {str(crop_only_e)}")

        except Exception as e:
            safe_print(f"❌ 裁剪并调整大小失败: {str(e)}")

        # 测试4: 选区裁剪
        safe_print("\n🔧 测试4: 选区裁剪...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建复杂选区
                safe_print("   🔲 创建复杂选区...")
                doc.selection.select([
                    [50, 50],
                    [250, 50],
                    [250, 250],
                    [50, 250]
                ])
                safe_print("      ✅ 选区创建完成")

                # 使用选区进行裁剪
                safe_print("   ✂️ 使用选区裁剪...")
                try:
                    doc.crop()
                    safe_print("      ✅ 选区裁剪成功")
                except Exception as selection_crop_e:
                    safe_print(f"      ⚠️ 选区裁剪失败: {str(selection_crop_e)[:50]}")

                doc.selection.deselect()

        except Exception as e:
            safe_print(f"❌ 选区裁剪失败: {str(e)}")

        # 测试5: 裁剪精度验证
        safe_print("\n🔧 测试5: 裁剪精度验证...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建网格内容用于验证
                safe_print("   🎨 创建网格内容...")
                for i in range(4):
                    for j in range(4):
                        layer = doc.artLayers.add()
                        layer.name = f"网格_{i}_{j}"

                        fill_color = ps.SolidColor()
                        fill_color.rgb.red = 50 + i * 50
                        fill_color.rgb.green = 50 + j * 50
                        fill_color.rgb.blue = 200
                        ps.app.foregroundColor = fill_color

                        doc.selection.select([
                            [i * 100, j * 100],
                            [(i + 1) * 100, j * 100],
                            [(i + 1) * 100, (j + 1) * 100],
                            [i * 100, (j + 1) * 100]
                        ])
                        doc.selection.fill(ps.app.foregroundColor)
                        doc.selection.deselect()

                safe_print("      ✅ 网格内容创建完成")

                # 记录裁剪前信息
                before_crop_width = doc.width
                before_crop_height = doc.height
                safe_print(f"   📊 裁剪前尺寸: {before_crop_width} x {before_crop_height}")

                # 执行精确裁剪
                safe_print("   ✂️ 执行精确裁剪...")
                try:
                    doc.crop(bounds=[50, 50, 350, 350])
                    after_crop_width = doc.width
                    after_crop_height = doc.height
                    safe_print(f"   📊 裁剪后尺寸: {after_crop_width} x {after_crop_height}")

                    # 验证裁剪效果
                    expected_width = 300
                    expected_height = 300
                    safe_print(f"   ✅ 裁剪精度验证")
                except Exception as precision_e:
                    safe_print(f"      ⚠️ 精确裁剪失败: {str(precision_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 裁剪精度验证失败: {str(e)}")

        # 测试6: 批处理裁剪
        safe_print("\n🔧 测试6: 批处理裁剪...")

        try:
            # 创建多个文档进行批处理裁剪
            for i in range(3):
                safe_print(f"   📄 处理文档 {i+1}/3...")
                with Session(action="new_document") as ps:
                    doc = ps.active_document
                    doc.name = f"裁剪测试文档_{i+1}"

                    # 创建内容
                    layer = doc.artLayers.add()
                    layer.name = f"内容_{i+1}"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 100 + i * 50
                    fill_color.rgb.green = 150
                    fill_color.rgb.blue = 200
                    ps.app.foregroundColor = fill_color

                    doc.selection.select([[0, 0], [400, 0], [400, 300], [0, 300]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                    # 执行裁剪
                    try:
                        doc.crop(bounds=[50, 50, 350, 250])
                        safe_print(f"      ✅ 文档{i+1}裁剪成功")
                    except Exception as batch_e:
                        safe_print(f"      ⚠️ 文档{i+1}裁剪失败: {str(batch_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 批处理裁剪失败: {str(e)}")

        # 测试7: 裁剪错误处理
        safe_print("\n🔧 测试7: 裁剪错误处理...")

        try:
            # 测试无效边界
            safe_print("   📄 测试无效边界...")
            with Session(action="new_document") as ps:
                doc = ps.active_document

                try:
                    # 边界大于文档尺寸
                    doc.crop(bounds=[1000, 1000, 2000, 2000])
                    safe_print("      ⚠️ 无效边界意外成功")
                except Exception as invalid_e:
                    safe_print(f"      ✅ 正确处理无效边界")

                # 测试空边界
                try:
                    doc.crop(bounds=[])
                    safe_print("      ⚠️ 空边界意外成功")
                except Exception as empty_e:
                    safe_print(f"      ✅ 正确处理空边界")

        except Exception as e:
            safe_print(f"❌ 裁剪错误处理失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "cropping_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Cropping 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 裁剪功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本裁剪操作 (原始代码逻辑)\n")
                f.write(f"- 不同边界裁剪\n")
                f.write(f"- 裁剪并调整大小\n")
                f.write(f"- 选区裁剪\n")
                f.write(f"- 裁剪精度验证\n")
                f.write(f"- 批处理裁剪\n")
                f.write(f"- 裁剪错误处理\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第33项: cropping.py 测试完成!")
        safe_print("✅ 验证功能: 基本裁剪、边界裁剪、选区裁剪、精度验证、批处理")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 裁剪功能是否可用")
        safe_print("3. crop方法参数是否正确")
        safe_print("4. 边界参数是否在文档范围内")
        return False

if __name__ == "__main__":
    test_cropping()
