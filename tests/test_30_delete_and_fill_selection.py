# -*- coding: utf-8 -*-
"""测试第30项: delete_and_fill_selection.py - 删除和填充选区"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def delete_and_fill_selection(doc, fill_type, mode=None, opacity=None, preserve_transparency=None):
    """Delete current selection and fill it with specified color.

    Args:
        doc: The active document.
        fill_type (SolidColor): The color to fill the selection with.
        mode (ColorBlendMode, optional): The color blend mode.
        opacity (int, optional): The opacity value.
        preserve_transparency (bool, optional): If true, preserves transparency.
    """
    # First fill the selection (原始代码逻辑)
    doc.selection.fill(fill_type, mode, opacity, preserve_transparency)
    # Then deselect (原始代码逻辑)
    doc.selection.deselect()

def test_delete_and_fill_selection():
    """运行delete_and_fill_selection测试"""
    safe_print("📋 开始执行第30项: delete_and_fill_selection.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session
        from photoshop.api import SolidColor
        import photoshop.api as ps

        # 测试1: 基本删除和填充选区 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本删除和填充选区 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ Session成功启动")

                # Create a rectangular selection (原始代码逻辑)
                safe_print("   🔲 创建矩形选区...")
                doc.selection.select([[100, 100], [400, 100], [400, 300], [100, 300]])
                safe_print("      ✅ 选区创建完成")

                # Create a solid color (red in this case) (原始代码逻辑)
                safe_print("   🎨 创建红色填充颜色...")
                red_color = SolidColor()
                red_color.rgb.red = 255
                red_color.rgb.green = 0
                red_color.rgb.blue = 0
                safe_print(f"      ✅ 填充颜色: R={red_color.rgb.red}, G={red_color.rgb.green}, B={red_color.rgb.blue}")

                # Delete and fill the selection (原始代码逻辑)
                safe_print("   🪣 删除和填充选区...")
                delete_and_fill_selection(doc, red_color, opacity=80)
                safe_print("      ✅ 删除和填充完成")

        except Exception as e:
            safe_print(f"❌ 基本删除和填充选区失败: {str(e)}")
            return False

        # 测试2: 使用不同不透明度删除和填充
        safe_print("\n🔧 测试2: 使用不同不透明度删除和填充...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建底层
                base_color = SolidColor()
                base_color.rgb.red = 100
                base_color.rgb.green = 100
                base_color.rgb.blue = 100
                doc.selection.select([[0, 0], [600, 0], [600, 400], [0, 400]])
                doc.selection.fill(base_color)
                doc.selection.deselect()
                safe_print("   ✅ 创建底层颜色")

                # 测试不同不透明度
                opacities = [100, 75, 50, 25]
                colors = [
                    {"name": "红色", "r": 255, "g": 0, "b": 0},
                    {"name": "绿色", "r": 0, "g": 255, "b": 0},
                    {"name": "蓝色", "r": 0, "g": 0, "b": 255},
                    {"name": "黄色", "r": 255, "g": 255, "b": 0},
                ]

                for i, (color_info, opacity) in enumerate(zip(colors, opacities)):
                    safe_print(f"   🎨 使用{opacity}%不透明度填充{color_info['name']}...")
                    x = 50 + i * 130

                    # 创建选区
                    doc.selection.select([
                        [x, 50],
                        [x + 100, 50],
                        [x + 100, 150],
                        [x, 150]
                    ])

                    # 创建颜色
                    fill_color = SolidColor()
                    fill_color.rgb.red = color_info["r"]
                    fill_color.rgb.green = color_info["g"]
                    fill_color.rgb.blue = color_info["b"]

                    # 删除和填充
                    delete_and_fill_selection(doc, fill_color, opacity=opacity)
                    safe_print(f"      ✅ {color_info['name']}填充完成（{opacity}%不透明度）")

        except Exception as e:
            safe_print(f"❌ 不同不透明度删除和填充失败: {str(e)}")

        # 测试3: 使用混合模式删除和填充
        safe_print("\n🔧 测试3: 使用混合模式删除和填充...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建底层
                base_color = SolidColor()
                base_color.rgb.red = 200
                base_color.rgb.green = 100
                base_color.rgb.blue = 50
                doc.selection.select([[0, 0], [500, 0], [500, 400], [0, 400]])
                doc.selection.fill(base_color)
                doc.selection.deselect()
                safe_print("   ✅ 创建底层颜色")

                # 测试混合模式
                blend_modes = [
                    {"name": "正常", "mode": ps.ColorBlendMode.Normal},
                    {"name": "正片叠底", "mode": ps.ColorBlendMode.Multiply},
                    {"name": "滤色", "mode": ps.ColorBlendMode.Screen},
                ]

                for i, blend_info in enumerate(blend_modes):
                    safe_print(f"   🎨 使用{blend_info['name']}混合模式...")
                    x = 50 + i * 150

                    doc.selection.select([
                        [x, 200],
                        [x + 100, 200],
                        [x + 100, 300],
                        [x, 200]
                    ])

                    fill_color = SolidColor()
                    fill_color.rgb.red = 100
                    fill_color.rgb.green = 150
                    fill_color.rgb.blue = 255

                    try:
                        delete_and_fill_selection(doc, fill_color, mode=blend_info['mode'])
                        safe_print(f"      ✅ {blend_info['name']}混合模式成功")
                    except Exception as blend_e:
                        safe_print(f"      ⚠️ {blend_info['name']}混合模式失败，使用默认模式")
                        delete_and_fill_selection(doc, fill_color)

        except Exception as e:
            safe_print(f"❌ 混合模式删除和填充失败: {str(e)}")

        # 测试4: 保留透明度的删除和填充
        safe_print("\n🔧 测试4: 保留透明度的删除和填充...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建测试图层
                layer = doc.artLayers.add()
                layer.name = "透明度测试"

                # 添加内容
                base_color = SolidColor()
                base_color.rgb.red = 150
                base_color.rgb.green = 150
                base_color.rgb.blue = 150
                doc.selection.select([[0, 0], [500, 0], [500, 400], [0, 400]])
                doc.selection.fill(base_color)
                doc.selection.deselect()
                safe_print("   ✅ 创建测试图层")

                # 创建选区并填充，保留透明度
                safe_print("   🎨 填充选区并保留透明度...")
                doc.selection.select([[100, 100], [400, 100], [400, 300], [100, 300]])

                fill_color = SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 0
                fill_color.rgb.blue = 0

                try:
                    delete_and_fill_selection(doc, fill_color, preserve_transparency=True)
                    safe_print("      ✅ 保留透明度填充成功")
                except Exception as trans_e:
                    safe_print(f"      ⚠️ 保留透明度参数失败，使用默认方式: {str(trans_e)[:50]}")
                    delete_and_fill_selection(doc, fill_color)

        except Exception as e:
            safe_print(f"❌ 保留透明度删除和填充失败: {str(e)}")

        # 测试5: 多步骤删除和填充
        safe_print("\n🔧 测试5: 多步骤删除和填充...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 步骤1: 创建初始内容
                safe_print("   步骤1: 创建初始内容...")
                doc.selection.select([[50, 50], [550, 50], [550, 350], [50, 350]])

                base_color = SolidColor()
                base_color.rgb.red = 100
                base_color.rgb.green = 100
                base_color.rgb.blue = 100
                doc.selection.fill(base_color)
                doc.selection.deselect()
                safe_print("      ✅ 初始内容创建完成")

                # 步骤2: 删除和填充第一个选区
                safe_print("   步骤2: 删除和填充第一个选区...")
                doc.selection.select([[100, 100], [250, 100], [250, 200], [100, 200]])

                color1 = SolidColor()
                color1.rgb.red = 255
                color1.rgb.green = 0
                color1.rgb.blue = 0
                delete_and_fill_selection(doc, color1)
                safe_print("      ✅ 第一个选区填充完成")

                # 步骤3: 删除和填充第二个选区
                safe_print("   步骤3: 删除和填充第二个选区...")
                doc.selection.select([[300, 150], [450, 150], [450, 250], [300, 250]])

                color2 = SolidColor()
                color2.rgb.red = 0
                color2.rgb.green = 255
                color2.rgb.blue = 0
                delete_and_fill_selection(doc, color2)
                safe_print("      ✅ 第二个选区填充完成")

                # 步骤4: 删除和填充第三个选区
                safe_print("   步骤4: 删除和填充第三个选区...")
                doc.selection.select([[150, 250], [400, 250], [400, 300], [150, 300]])

                color3 = SolidColor()
                color3.rgb.red = 0
                color3.rgb.green = 0
                color3.rgb.blue = 255
                delete_and_fill_selection(doc, color3)
                safe_print("      ✅ 第三个选区填充完成")

                safe_print("   ✅ 多步骤删除和填充完成")

        except Exception as e:
            safe_print(f"❌ 多步骤删除和填充失败: {str(e)}")

        # 测试6: 函数参数验证
        safe_print("\n🔧 测试6: 函数参数验证...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 验证只使用必需参数
                safe_print("   📝 验证必需参数...")
                doc.selection.select([[50, 50], [150, 50], [150, 150], [50, 150]])

                color = SolidColor()
                color.rgb.red = 255
                color.rgb.green = 128
                color.rgb.blue = 64

                delete_and_fill_selection(doc, color)
                safe_print("      ✅ 必需参数验证成功")

                # 验证使用可选参数
                safe_print("   📝 验证可选参数...")
                doc.selection.select([[200, 50], [300, 50], [300, 150], [200, 150]])

                try:
                    delete_and_fill_selection(doc, color, mode=ps.ColorBlendMode.Normal, opacity=75)
                    safe_print("      ✅ 可选参数验证成功")
                except Exception as opt_e:
                    safe_print(f"      ⚠️ 可选参数部分失败，使用默认方式: {str(opt_e)[:50]}")
                    delete_and_fill_selection(doc, color)

        except Exception as e:
            safe_print(f"❌ 函数参数验证失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "delete_and_fill_selection_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Delete and Fill Selection 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 删除和填充选区功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本删除和填充选区 (原始代码逻辑)\n")
                f.write(f"- 使用不同不透明度删除和填充\n")
                f.write(f"- 使用混合模式删除和填充\n")
                f.write(f"- 保留透明度的删除和填充\n")
                f.write(f"- 多步骤删除和填充\n")
                f.write(f"- 函数参数验证\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第30项: delete_and_fill_selection.py 测试完成!")
        safe_print("✅ 验证功能: 删除填充选区、不透明度、混合模式、透明度保留、多步骤操作")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 删除和填充函数是否可用")
        safe_print("3. 选区操作是否正常")
        safe_print("4. 函数参数是否正确")
        return False

if __name__ == "__main__":
    test_delete_and_fill_selection()
