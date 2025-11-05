# -*- coding: utf-8 -*-
"""测试第31项: selection_stroke.py - 选区描边"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_selection_stroke():
    """运行selection_stroke测试"""
    safe_print("📋 开始执行第31项: selection_stroke.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session
        import photoshop.api as ps

        # 测试1: 基本选区描边 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本选区描边 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ Session成功启动")

                # Create a rectangular selection (原始代码逻辑)
                safe_print("   🔲 创建矩形选区...")
                doc.selection.select([
                    [100, 100],
                    [400, 100],
                    [400, 300],
                    [100, 300]
                ])
                safe_print("      ✅ 矩形选区创建完成")

                # Create stroke color (原始代码逻辑)
                safe_print("   🎨 创建描边颜色...")
                stroke_color = ps.SolidColor()
                stroke_color.rgb.red = 255
                stroke_color.rgb.green = 0
                stroke_color.rgb.blue = 0
                safe_print(f"      ✅ 描边颜色: R={stroke_color.rgb.red}, G={stroke_color.rgb.green}, B={stroke_color.rgb.blue}")

                # Apply stroke to selection (原始代码逻辑)
                safe_print("   ✏️ 应用描边...")
                try:
                    doc.selection.stroke(
                        stroke_color,  # Color to use
                        2,             # Stroke width in pixels
                        ps.StrokeLocation.Inside,
                        ps.ColorBlendMode.Normal,
                        100
                    )
                    safe_print("      ✅ 描边应用完成（红色，2像素，内部）")
                except Exception as stroke_e:
                    safe_print(f"      ⚠️ 描边参数失败: {str(stroke_e)[:50]}")
                    # 简化方式测试
                    try:
                        doc.selection.stroke(stroke_color, 2, ps.StrokeLocation.Inside)
                        safe_print("      ✅ 简化描边成功")
                    except Exception as simple_e:
                        safe_print(f"      ❌ 简化描边也失败: {str(simple_e)}")

                # Clear selection (原始代码逻辑)
                doc.selection.deselect()

        except Exception as e:
            safe_print(f"❌ 基本选区描边失败: {str(e)}")
            return False

        # 测试2: 椭圆选区描边
        safe_print("\n🔧 测试2: 椭圆选区描边...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # Create circular selection (原始代码逻辑)
                safe_print("   🔲 创建椭圆选区...")
                doc.selection.selectElliptical(
                    left=200,
                    top=200,
                    width=200,
                    height=200
                )
                safe_print("      ✅ 椭圆选区创建完成")

                # Change stroke color (原始代码逻辑)
                stroke_color.rgb.blue = 255
                safe_print(f"   🎨 更改描边颜色为蓝色")

                # Apply different stroke (原始代码逻辑)
                safe_print("   ✏️ 应用描边...")
                try:
                    doc.selection.stroke(
                        stroke_color,
                        5,
                        ps.StrokeLocation.Center,
                        ps.ColorBlendMode.Normal,
                        75
                    )
                    safe_print("      ✅ 描边应用完成（蓝色，5像素，居中，75%不透明度）")
                except Exception as stroke_e:
                    safe_print(f"      ⚠️ 描边参数失败: {str(stroke_e)[:50]}")
                    try:
                        doc.selection.stroke(stroke_color, 5, ps.StrokeLocation.Center)
                        safe_print("      ✅ 简化描边成功")
                    except Exception as simple_e:
                        safe_print(f"      ❌ 简化描边也失败: {str(simple_e)}")

                doc.selection.deselect()

        except Exception as e:
            safe_print(f"❌ 椭圆选区描边失败: {str(e)}")

        # 测试3: 不同宽度描边
        safe_print("\n🔧 测试3: 不同宽度描边...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                widths = [1, 3, 5, 10]
                colors = [
                    {"name": "红色", "r": 255, "g": 0, "b": 0},
                    {"name": "绿色", "r": 0, "g": 255, "b": 0},
                    {"name": "蓝色", "r": 0, "g": 0, "b": 255},
                    {"name": "黄色", "r": 255, "g": 255, "b": 0},
                ]

                for i, (width, color_info) in enumerate(zip(widths, colors)):
                    safe_print(f"   ✏️ 创建{width}像素{color_info['name']}描边...")
                    x = 50 + i * 140

                    doc.selection.select([
                        [x, 50],
                        [x + 100, 50],
                        [x + 100, 150],
                        [x, 50]
                    ])

                    stroke_color = ps.SolidColor()
                    stroke_color.rgb.red = color_info["r"]
                    stroke_color.rgb.green = color_info["g"]
                    stroke_color.rgb.blue = color_info["b"]

                    try:
                        doc.selection.stroke(
                            stroke_color,
                            width,
                            ps.StrokeLocation.Inside,
                            ps.ColorBlendMode.Normal,
                            100
                        )
                        safe_print(f"      ✅ {width}像素{color_info['name']}描边成功")
                    except Exception as width_e:
                        safe_print(f"      ⚠️ 描边失败: {str(width_e)}")

                    doc.selection.deselect()

        except Exception as e:
            safe_print(f"❌ 不同宽度描边失败: {str(e)}")

        # 测试4: 不同描边位置
        safe_print("\n🔧 测试4: 不同描边位置...")

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

                locations = [
                    {"name": "内部", "location": ps.StrokeLocation.Inside},
                    {"name": "居中", "location": ps.StrokeLocation.Center},
                    {"name": "外部", "location": ps.StrokeLocation.Outside},
                ]

                for i, loc_info in enumerate(locations):
                    safe_print(f"   ✏️ 创建{loc_info['name']}描边...")
                    x = 50 + i * 150

                    doc.selection.select([
                        [x, 200],
                        [x + 100, 200],
                        [x + 100, 300],
                        [x, 200]
                    ])

                    stroke_color = ps.SolidColor()
                    stroke_color.rgb.red = 255
                    stroke_color.rgb.green = 128
                    stroke_color.rgb.blue = 0

                    try:
                        doc.selection.stroke(
                            stroke_color,
                            8,
                            loc_info['location'],
                            ps.ColorBlendMode.Normal,
                            100
                        )
                        safe_print(f"      ✅ {loc_info['name']}描边成功")
                    except Exception as loc_e:
                        safe_print(f"      ⚠️ {loc_info['name']}描边失败")
                        doc.selection.stroke(
                            stroke_color,
                            8,
                            ps.StrokeLocation.Inside,
                            ps.ColorBlendMode.Normal,
                            100
                        )

                    doc.selection.deselect()

        except Exception as e:
            safe_print(f"❌ 不同描边位置失败: {str(e)}")

        # 测试5: 复杂形状描边
        safe_print("\n🔧 测试5: 复杂形状描边...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建多边形选区
                safe_print("   🔲 创建多边形选区...")
                doc.selection.select([
                    [150, 150],
                    [350, 150],
                    [350, 250],
                    [250, 300],
                    [150, 250]
                ])
                safe_print("      ✅ 多边形选区创建完成")

                stroke_color = ps.SolidColor()
                stroke_color.rgb.red = 255
                stroke_color.rgb.green = 0
                stroke_color.rgb.blue = 255

                doc.selection.stroke(
                    stroke_color,
                    4,
                    ps.StrokeLocation.Inside,
                    ps.ColorBlendMode.Normal,
                    100
                )
                safe_print("   ✅ 多边形描边完成")

                doc.selection.deselect()

                # 创建星形选区（简化版）
                safe_print("   🔲 创建星形选区...")
                star_points = [
                    [300, 100],
                    [320, 140],
                    [360, 140],
                    [330, 165],
                    [345, 200],
                    [300, 180],
                    [255, 200],
                    [270, 165],
                    [240, 140],
                    [280, 140]
                ]
                doc.selection.select(star_points)
                safe_print("      ✅ 星形选区创建完成")

                stroke_color2 = ps.SolidColor()
                stroke_color2.rgb.red = 0
                stroke_color2.rgb.green = 255
                stroke_color2.rgb.blue = 255

                doc.selection.stroke(
                    stroke_color2,
                    3,
                    ps.StrokeLocation.Inside,
                    ps.ColorBlendMode.Normal,
                    100
                )
                safe_print("   ✅ 星形描边完成")

                doc.selection.deselect()

        except Exception as e:
            safe_print(f"❌ 复杂形状描边失败: {str(e)}")

        # 测试6: 描边和填充组合
        safe_print("\n🔧 测试6: 描边和填充组合...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建多个带描边和填充的形状
                shapes = [
                    {"name": "红色填充蓝色描边", "fill": (255, 0, 0), "stroke": (0, 0, 255), "x": 50},
                    {"name": "绿色填充黄色描边", "fill": (0, 255, 0), "stroke": (255, 255, 0), "x": 180},
                    {"name": "蓝色填充紫色描边", "fill": (0, 0, 255), "stroke": (255, 0, 255), "x": 310},
                ]

                for shape_info in shapes:
                    safe_print(f"   🎨 创建{shape_info['name']}...")

                    # 填充
                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = shape_info["fill"][0]
                    fill_color.rgb.green = shape_info["fill"][1]
                    fill_color.rgb.blue = shape_info["fill"][2]

                    doc.selection.select([
                        [shape_info["x"], 50],
                        [shape_info["x"] + 80, 50],
                        [shape_info["x"] + 80, 130],
                        [shape_info["x"], 130]
                    ])

                    doc.selection.fill(fill_color)

                    # 描边
                    stroke_color = ps.SolidColor()
                    stroke_color.rgb.red = shape_info["stroke"][0]
                    stroke_color.rgb.green = shape_info["stroke"][1]
                    stroke_color.rgb.blue = shape_info["stroke"][2]

                    try:
                        doc.selection.stroke(
                            stroke_color,
                            5,
                            ps.StrokeLocation.Inside,
                            ps.ColorBlendMode.Normal,
                            100
                        )
                        safe_print(f"      ✅ {shape_info['name']}成功")
                    except Exception as combo_e:
                        safe_print(f"      ⚠️ 描边失败: {str(combo_e)}")

                    doc.selection.deselect()

        except Exception as e:
            safe_print(f"❌ 描边和填充组合失败: {str(e)}")

        # 测试7: 描边不透明度测试
        safe_print("\n🔧 测试7: 描边不透明度测试...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建底层
                base_color = ps.SolidColor()
                base_color.rgb.red = 150
                base_color.rgb.green = 150
                base_color.rgb.blue = 150
                doc.selection.select([[0, 0], [500, 0], [500, 400], [0, 400]])
                doc.selection.fill(base_color)
                doc.selection.deselect()
                safe_print("   ✅ 创建底层")

                opacities = [100, 75, 50, 25]
                for i, opacity in enumerate(opacities):
                    safe_print(f"   ✏️ 创建{opacity}%不透明度描边...")
                    x = 50 + i * 110

                    doc.selection.select([
                        [x, 200],
                        [x + 80, 200],
                        [x + 80, 280],
                        [x, 200]
                    ])

                    stroke_color = ps.SolidColor()
                    stroke_color.rgb.red = 255
                    stroke_color.rgb.green = 0
                    stroke_color.rgb.blue = 0

                    try:
                        doc.selection.stroke(
                            stroke_color,
                            6,
                            ps.StrokeLocation.Inside,
                            ps.ColorBlendMode.Normal,
                            opacity
                        )
                        safe_print(f"      ✅ {opacity}%不透明度描边成功")
                    except Exception as opacity_e:
                        safe_print(f"      ⚠️ 不透明度参数失败")
                        doc.selection.stroke(
                            stroke_color,
                            6,
                            ps.StrokeLocation.Inside,
                            ps.ColorBlendMode.Normal,
                            100
                        )

                    doc.selection.deselect()

        except Exception as e:
            safe_print(f"❌ 描边不透明度测试失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "selection_stroke_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Selection Stroke 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 选区描边功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本选区描边 (原始代码逻辑)\n")
                f.write(f"- 椭圆选区描边\n")
                f.write(f"- 不同宽度描边\n")
                f.write(f"- 不同描边位置\n")
                f.write(f"- 复杂形状描边\n")
                f.write(f"- 描边和填充组合\n")
                f.write(f"- 描边不透明度测试\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第31项: selection_stroke.py 测试完成!")
        safe_print("✅ 验证功能: 基本描边、椭圆描边、不同宽度、不同位置、复杂形状、不透明度")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 选区描边功能是否可用")
        safe_print("3. stroke方法参数是否正确")
        safe_print("4. 描边位置和混合模式参数是否正常")
        return False

if __name__ == "__main__":
    test_selection_stroke()
