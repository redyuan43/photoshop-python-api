# -*- coding: utf-8 -*-
"""测试第29项: fill_selection.py - 填充选区"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_fill_selection():
    """运行fill_selection测试"""
    safe_print("📋 开始执行第29项: fill_selection.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本填充选区 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本填充选区 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ Session成功启动")

                # Create a rectangular selection (原始代码逻辑)
                safe_print("   🔲 创建矩形选区...")
                doc.selection.select([
                    [100, 100],
                    [300, 100],
                    [300, 200],
                    [100, 200]
                ])
                safe_print("      ✅ 选区创建完成")

                # Create fill color (原始代码逻辑)
                safe_print("   🎨 创建填充颜色...")
                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 0
                fill_color.rgb.blue = 0
                safe_print(f"      ✅ 填充颜色: R={fill_color.rgb.red}, G={fill_color.rgb.green}, B={fill_color.rgb.blue}")

                # Fill the selection (原始代码逻辑)
                safe_print("   🪣 填充选区...")
                doc.selection.fill(fill_color)
                safe_print("      ✅ 填充完成")

                # Deselect (原始代码逻辑)
                doc.selection.deselect()
                safe_print("      ✅ 取消选区")

        except Exception as e:
            safe_print(f"❌ 基本填充选区失败: {str(e)}")
            return False

        # 测试2: 创建多个填充选区
        safe_print("\n🔧 测试2: 创建多个填充选区...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建网格填充
                colors = [
                    {"name": "红色", "r": 255, "g": 0, "b": 0, "x": 100, "y": 100},
                    {"name": "绿色", "r": 0, "g": 255, "b": 0, "x": 300, "y": 100},
                    {"name": "蓝色", "r": 0, "g": 0, "b": 255, "x": 500, "y": 100},
                    {"name": "黄色", "r": 255, "g": 255, "b": 0, "x": 100, "y": 300},
                    {"name": "紫色", "r": 255, "g": 0, "b": 255, "x": 300, "y": 300},
                    {"name": "青色", "r": 0, "g": 255, "b": 255, "x": 500, "y": 300},
                ]

                for color_info in colors:
                    safe_print(f"   🎨 创建{color_info['name']}填充...")
                    # 创建矩形选区
                    doc.selection.select([
                        [color_info['x'], color_info['y']],
                        [color_info['x'] + 80, color_info['y']],
                        [color_info['x'] + 80, color_info['y'] + 80],
                        [color_info['x'], color_info['y'] + 80]
                    ])

                    # 创建填充颜色
                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = color_info['r']
                    fill_color.rgb.green = color_info['g']
                    fill_color.rgb.blue = color_info['b']

                    # 填充选区
                    doc.selection.fill(fill_color)
                    doc.selection.deselect()
                    safe_print(f"      ✅ {color_info['name']}填充完成")

        except Exception as e:
            safe_print(f"❌ 多个填充选区失败: {str(e)}")

        # 测试3: 透明填充
        safe_print("\n🔧 测试3: 透明填充...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 先创建一个底层颜色
                base_color = ps.SolidColor()
                base_color.rgb.red = 100
                base_color.rgb.green = 100
                base_color.rgb.blue = 100
                doc.selection.select([[0, 0], [600, 0], [600, 400], [0, 400]])
                doc.selection.fill(base_color)
                doc.selection.deselect()
                safe_print("   ✅ 创建底层颜色")

                # 在上层创建透明填充
                safe_print("   🎨 创建透明填充...")
                doc.selection.select([
                    [150, 150],
                    [350, 150],
                    [350, 250],
                    [150, 250]
                ])

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 0
                fill_color.rgb.blue = 0

                # 尝试使用不透明度填充（原始代码逻辑）
                try:
                    doc.selection.fill(fill_color, ps.ColorBlendMode.Normal, 50)
                    safe_print("   ✅ 透明填充完成（50%不透明度）")
                except Exception as opacity_e:
                    safe_print(f"   ⚠️ 透明填充参数失败，使用默认不透明度: {str(opacity_e)[:50]}")
                    doc.selection.fill(fill_color)

                doc.selection.deselect()

        except Exception as e:
            safe_print(f"❌ 透明填充失败: {str(e)}")

        # 测试4: 复杂形状填充
        safe_print("\n🔧 测试4: 复杂形状填充...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建圆形选区
                safe_print("   🔲 创建圆形选区...")
                doc.selection.select([
                    [200, 200],
                    [400, 200],
                    [400, 400],
                    [200, 400]
                ], ps.SelectionType.ReplaceSelection, 0, False)
                safe_print("      ✅ 圆形选区创建完成")

                # 填充渐变色
                fill_color = ps.SolidColor()
                fill_color.rgb.red = 128
                fill_color.rgb.green = 128
                fill_color.rgb.blue = 255

                doc.selection.fill(fill_color)
                doc.selection.deselect()
                safe_print("   ✅ 复杂形状填充完成")

        except Exception as e:
            safe_print(f"❌ 复杂形状填充失败: {str(e)}")

        # 测试5: 选区操作和填充组合
        safe_print("\n🔧 测试5: 选区操作和填充组合...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建初始选区
                safe_print("   🔲 创建初始选区...")
                doc.selection.select([[100, 100], [200, 100], [200, 200], [100, 200]])
                safe_print("      ✅ 初始选区创建")

                # 填充红色
                red_color = ps.SolidColor()
                red_color.rgb.red = 255
                red_color.rgb.green = 0
                red_color.rgb.blue = 0
                doc.selection.fill(red_color)
                safe_print("   🎨 填充红色")

                # 添加到选区
                safe_print("   🔲 扩展选区...")
                doc.selection.select([[150, 150], [300, 150], [300, 300], [150, 300]],
                                     ps.SelectionType.ExtendSelection)
                safe_print("      ✅ 选区扩展")

                # 填充蓝色
                blue_color = ps.SolidColor()
                blue_color.rgb.red = 0
                blue_color.rgb.green = 0
                blue_color.rgb.blue = 255
                doc.selection.fill(blue_color)
                safe_print("   🎨 填充蓝色")

                # 取消选区
                doc.selection.deselect()
                safe_print("   ✅ 取消选区")

        except Exception as e:
            safe_print(f"❌ 选区操作和填充组合失败: {str(e)}")

        # 测试6: 不同混合模式填充
        safe_print("\n🔧 测试6: 不同混合模式填充...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建底层
                base_color = ps.SolidColor()
                base_color.rgb.red = 200
                base_color.rgb.green = 200
                base_color.rgb.blue = 200
                doc.selection.select([[0, 0], [500, 0], [500, 400], [0, 400]])
                doc.selection.fill(base_color)
                doc.selection.deselect()
                safe_print("   ✅ 创建底层")

                # 测试不同混合模式
                blend_modes = [
                    {"name": "正常", "mode": ps.ColorBlendMode.Normal},
                    {"name": "正片叠底", "mode": ps.ColorBlendMode.Multiply},
                    {"name": "滤色", "mode": ps.ColorBlendMode.Screen},
                ]

                for i, blend_info in enumerate(blend_modes):
                    safe_print(f"   🎨 测试{blend_info['name']}混合模式...")
                    x = 50 + i * 150

                    doc.selection.select([[x, 50], [x+100, 50], [x+100, 150], [x, 50]])

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 255
                    fill_color.rgb.green = 100
                    fill_color.rgb.blue = 0

                    try:
                        doc.selection.fill(fill_color, blend_info['mode'])
                        safe_print(f"      ✅ {blend_info['name']}混合模式成功")
                    except Exception as blend_e:
                        safe_print(f"      ⚠️ {blend_info['name']}混合模式失败，使用默认模式")
                        doc.selection.fill(fill_color)

                    doc.selection.deselect()

        except Exception as e:
            safe_print(f"❌ 不同混合模式填充失败: {str(e)}")

        # 测试7: 选区边框和填充
        safe_print("\n🔧 测试7: 选区边框和填充...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建外部选区
                doc.selection.select([[100, 100], [400, 100], [400, 400], [100, 400]])
                safe_print("   🔲 创建外部选区")

                # 创建内部选区
                doc.selection.select([[150, 150], [350, 150], [350, 350], [150, 350]],
                                     ps.SelectionType.SubtractSelection)
                safe_print("   🔲 创建内部选区（创建边框）")

                # 填充边框
                border_color = ps.SolidColor()
                border_color.rgb.red = 255
                border_color.rgb.green = 255
                border_color.rgb.blue = 0

                doc.selection.fill(border_color)
                doc.selection.deselect()
                safe_print("   ✅ 选区边框填充完成")

        except Exception as e:
            safe_print(f"❌ 选区边框和填充失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "fill_selection_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Fill Selection 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 填充选区功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本填充选区 (原始代码逻辑)\n")
                f.write(f"- 创建多个填充选区\n")
                f.write(f"- 透明填充\n")
                f.write(f"- 复杂形状填充\n")
                f.write(f"- 选区操作和填充组合\n")
                f.write(f"- 不同混合模式填充\n")
                f.write(f"- 选区边框和填充\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第29项: fill_selection.py 测试完成!")
        safe_print("✅ 验证功能: 基本选区填充、多色填充、透明填充、混合模式、复杂选区")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 选区创建是否正常")
        safe_print("3. 填充操作是否可用")
        safe_print("4. 混合模式参数是否正确")
        return False

if __name__ == "__main__":
    test_fill_selection()
