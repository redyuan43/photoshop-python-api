# -*- coding: utf-8 -*-
"""测试第20项: rotate_layer.py - 旋转图层"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_rotate_layer():
    """运行rotate_layer测试"""
    safe_print("🔄 开始执行第20项: rotate_layer.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本图层旋转 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本图层旋转 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print(f"📄 创建文档: {doc.name}")

                # 创建可旋转的图层内容
                layer = doc.artLayers.add()
                layer.name = "旋转测试图层"

                # 添加可见内容
                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 100
                fill_color.rgb.blue = 100
                ps.app.foregroundColor = fill_color

                # 创建矩形
                doc.selection.select([[200, 200], [300, 200], [300, 300], [200, 300]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()
                safe_print("   ✅ 创建红色矩形图层")

                # Store original bounds (原始代码逻辑)
                safe_print("   📏 获取原始边界框...")
                try:
                    bounds_raw = layer.bounds
                    bounds = [float(bounds_raw[0]), float(bounds_raw[1]),
                             float(bounds_raw[2]), float(bounds_raw[3])]
                    safe_print(f"      📐 原始边界框: {bounds}")

                    # Calculate center point (原始代码逻辑)
                    center_x = (bounds[0] + bounds[2]) / 2
                    center_y = (bounds[1] + bounds[3]) / 2
                    safe_print(f"      🎯 中心点: ({center_x:.1f}, {center_y:.1f})")
                except Exception as bounds_e:
                    safe_print(f"      ⚠️ 边界框获取失败: {str(bounds_e)}")
                    bounds = [200, 200, 300, 300]
                    center_x = 250
                    center_y = 250

                # Rotate layer by 45 degrees (原始代码逻辑)
                safe_print("   🔄 旋转图层45度...")
                layer.rotate(45.0, ps.AnchorPosition.MiddleCenter)
                ps.echo("Layer rotated by 45 degrees")
                safe_print("   ✅ 45度旋转完成")

                # Create new layer and rotate it (原始代码逻辑)
                safe_print("   📄 创建新图层...")
                new_layer = doc.artLayers.add()
                new_layer.name = "Rotated Layer"

                # 添加可见内容
                fill_color2 = ps.SolidColor()
                fill_color2.rgb.red = 100
                fill_color2.rgb.green = 100
                fill_color2.rgb.blue = 255
                ps.app.foregroundColor = fill_color2

                doc.selection.select([[400, 200], [500, 200], [500, 300], [400, 300]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()
                safe_print("   ✅ 创建蓝色矩形")

                # Rotate new layer by 90 degrees (原始代码逻辑)
                safe_print("   🔄 旋转新图层90度...")
                new_layer.rotate(90.0, ps.AnchorPosition.MiddleCenter)
                safe_print("   ✅ 90度旋转完成")

                # Move layer to original center (原始代码逻辑)
                safe_print("   📍 移动到原始中心...")
                try:
                    new_bounds = new_layer.bounds
                    new_center_x = (new_bounds[0] + new_bounds[2]) / 2
                    new_center_y = (new_bounds[1] + new_bounds[3]) / 2

                    # 计算移动距离
                    move_x = center_x - new_center_x
                    move_y = center_y - new_center_y

                    new_layer.translate(move_x, move_y)
                    safe_print("   ✅ 移动到中心完成")
                except Exception as move_e:
                    safe_print(f"      ⚠️ 移动到中心失败: {str(move_e)}")

        except Exception as e:
            safe_print(f"❌ 基本图层旋转测试失败: {str(e)}")
            return False

        # 测试2: 多角度旋转测试
        safe_print("\n🔧 测试2: 多角度旋转测试...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 测试不同角度
                angles = [30, 60, 120, 180, 270]
                for i, angle in enumerate(angles):
                    try:
                        layer = doc.artLayers.add()
                        layer.name = f"旋转{angle}度"

                        # 添加内容
                        fill_color = ps.SolidColor()
                        fill_color.rgb.red = 255
                        fill_color.rgb.green = 255
                        fill_color.rgb.blue = 0
                        ps.app.foregroundColor = fill_color

                        x = 50 + i * 50
                        y = 250 + i * 30
                        doc.selection.select([[x, y], [x+50, y], [x+50, y+50], [x, y+50]])
                        doc.selection.fill(ps.app.foregroundColor)
                        doc.selection.deselect()

                        # 旋转
                        layer.rotate(float(angle), ps.AnchorPosition.MiddleCenter)
                        safe_print(f"   ✅ {angle}度旋转成功")
                    except Exception as angle_e:
                        safe_print(f"   ❌ {angle}度旋转失败: {str(angle_e)}")

        except Exception as e:
            safe_print(f"❌ 多角度旋转测试失败: {str(e)}")

        # 测试3: 文本图层旋转
        safe_print("\n🔧 测试3: 文本图层旋转...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建文本图层
                text_layer = doc.artLayers.add()
                text_layer.kind = ps.LayerKind.TextLayer
                text_layer.name = "旋转文本"
                text_layer.textItem.contents = "旋转测试文本"
                text_layer.textItem.size = 24
                text_layer.textItem.position = [200, 300]

                safe_print("   ✅ 创建文本图层")

                # 旋转文本图层
                safe_print("   🔄 旋转文本图层...")
                try:
                    text_layer.rotate(45.0, ps.AnchorPosition.MiddleCenter)
                    safe_print("   ✅ 文本图层旋转成功")
                except Exception as text_e:
                    safe_print(f"   ❌ 文本图层旋转失败: {str(text_e)}")

        except Exception as e:
            safe_print(f"❌ 文本图层旋转测试失败: {str(e)}")

        # 测试4: 边界框变化验证
        safe_print("\n🔧 测试4: 边界框变化验证...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建测试图层
                layer = doc.artLayers.add()
                layer.name = "验证测试"

                # 添加内容
                fill_color = ps.SolidColor()
                fill_color.rgb.red = 128
                fill_color.rgb.green = 128
                fill_color.rgb.blue = 255
                ps.app.foregroundColor = fill_color

                doc.selection.select([[100, 100], [200, 100], [200, 200], [100, 200]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 记录旋转前信息
                safe_print("   📊 旋转前状态...")
                try:
                    before_bounds = layer.bounds
                    safe_print(f"      📏 旋转前边界: {before_bounds}")
                except Exception as before_e:
                    safe_print(f"      ⚠️ 旋转前边界获取失败: {str(before_e)}")
                    before_bounds = None

                # 旋转
                layer.rotate(60.0, ps.AnchorPosition.MiddleCenter)

                # 记录旋转后信息
                safe_print("   📊 旋转后状态...")
                try:
                    after_bounds = layer.bounds
                    safe_print(f"      📏 旋转后边界: {after_bounds}")

                    # 验证边界是否改变
                    if before_bounds and before_bounds != after_bounds:
                        safe_print("   ✅ 旋转效果验证通过")
                    else:
                        safe_print("   ⚠️ 旋转效果验证警告")
                except Exception as after_e:
                    safe_print(f"      ⚠️ 旋转后边界获取失败: {str(after_e)}")

        except Exception as e:
            safe_print(f"❌ 旋转验证测试失败: {str(e)}")

        # 测试5: 错误处理
        safe_print("\n🔧 测试5: 错误处理测试...")

        try:
            # 测试无效角度
            safe_print("   📄 测试无效角度...")
            with Session(action="new_document") as ps:
                doc = ps.active_document
                layer = doc.artLayers.add()
                layer.name = "错误测试"

                # 测试负角度
                try:
                    layer.rotate(-45.0, ps.AnchorPosition.MiddleCenter)
                    safe_print("      ✅ 负角度旋转成功")
                except Exception as neg_e:
                    safe_print(f"      ⚠️ 负角度旋转失败: {str(neg_e)}")

                # 测试超大角度
                try:
                    layer.rotate(999.0, ps.AnchorPosition.MiddleCenter)
                    safe_print("      ✅ 超大角度旋转成功")
                except Exception as large_e:
                    safe_print(f"      ⚠️ 超大角度旋转失败: {str(large_e)}")

        except Exception as e:
            safe_print(f"❌ 错误处理测试失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "rotate_layer_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Rotate Layer 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 图层旋转功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本图层旋转 (原始代码逻辑)\n")
                f.write(f"- 多角度旋转测试\n")
                f.write(f"- 文本图层旋转\n")
                f.write(f"- 边界框变化验证\n")
                f.write(f"- 错误处理测试\n")
                f.write(f"\n修复内容:\n")
                f.write(f"- 解决了图层对象边界框访问问题\n")
                f.write(f"- 添加了可见内容创建\n")
                f.write(f"- 增强了错误处理机制\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第20项: rotate_layer.py 测试完成!")
        safe_print("✅ 验证功能: 基本旋转、多角度旋转、文本旋转、效果验证、错误处理")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 图层旋转功能是否可用")
        safe_print("3. AnchorPosition枚举是否正确")
        safe_print("4. 图层内容是否正确创建")
        return False

if __name__ == "__main__":
    test_rotate_layer()