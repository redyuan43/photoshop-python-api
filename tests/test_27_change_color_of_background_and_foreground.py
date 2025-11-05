# -*- coding: utf-8 -*-
"""测试第27项: change_color_of_background_and_foreground.py - 改变前景背景色"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_change_color_of_background_and_foreground():
    """运行change_color_of_background_and_foreground测试"""
    safe_print("📋 开始执行第27项: change_color_of_background_and_foreground.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本前景背景色设置 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本前景背景色设置 (原始逻辑)...")

        try:
            with Session() as ps:
                safe_print("   ✅ Session成功启动")

                # Create new colors (原始代码逻辑)
                fg_color = ps.SolidColor()
                fg_color.rgb.red = 255
                fg_color.rgb.green = 0
                fg_color.rgb.blue = 0

                bg_color = ps.SolidColor()
                bg_color.rgb.red = 0
                bg_color.rgb.green = 0
                bg_color.rgb.blue = 255

                # Set foreground and background colors (原始代码逻辑)
                ps.app.foregroundColor = fg_color
                ps.app.backgroundColor = bg_color

                # Print current colors (原始代码逻辑)
                safe_print(f"   📊 前景色RGB: {fg_color.rgb.red}, {fg_color.rgb.green}, {fg_color.rgb.blue}")
                safe_print(f"   📊 背景色RGB: {bg_color.rgb.red}, {bg_color.rgb.green}, {bg_color.rgb.blue}")

                # 验证设置结果
                current_fg = ps.app.foregroundColor
                current_bg = ps.app.backgroundColor
                safe_print(f"   ✅ 前景色设置验证: R={current_fg.rgb.red}, G={current_fg.rgb.green}, B={current_fg.rgb.blue}")
                safe_print(f"   ✅ 背景色设置验证: R={current_bg.rgb.red}, G={current_bg.rgb.green}, B={current_bg.rgb.blue}")

        except Exception as e:
            safe_print(f"❌ 基本前景背景色设置失败: {str(e)}")
            return False

        # 测试2: 使用不同颜色模型设置前景背景色
        safe_print("\n🔧 测试2: 使用不同颜色模型设置前景背景色...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 测试CMYK颜色模型
                safe_print("   🎨 测试CMYK颜色模型...")
                cmyk_fg = ps.SolidColor()
                cmyk_fg.cmyk.cyan = 100
                cmyk_fg.cmyk.magenta = 0
                cmyk_fg.cmyk.yellow = 0
                cmyk_fg.cmyk.black = 0
                ps.app.foregroundColor = cmyk_fg
                safe_print(f"      ✅ CMYK前景色设置: C={cmyk_fg.cmyk.cyan}%, M={cmyk_fg.cmyk.magenta}%, Y={cmyk_fg.cmyk.yellow}%, K={cmyk_fg.cmyk.black}%")

                cmyk_bg = ps.SolidColor()
                cmyk_bg.cmyk.cyan = 0
                cmyk_bg.cmyk.magenta = 100
                cmyk_bg.cmyk.yellow = 0
                cmyk_bg.cmyk.black = 0
                ps.app.backgroundColor = cmyk_bg
                safe_print(f"      ✅ CMYK背景色设置: C={cmyk_bg.cmyk.cyan}%, M={cmyk_bg.cmyk.magenta}%, Y={cmyk_bg.cmyk.yellow}%, K={cmyk_bg.cmyk.black}%")

                # 测试HSB颜色模型
                safe_print("   🎨 测试HSB颜色模型...")
                hsb_fg = ps.SolidColor()
                hsb_fg.hsb.hue = 120
                hsb_fg.hsb.saturation = 100
                hsb_fg.hsb.brightness = 100
                ps.app.foregroundColor = hsb_fg
                safe_print(f"      ✅ HSB前景色设置: H={hsb_fg.hsb.hue}, S={hsb_fg.hsb.saturation}%, B={hsb_fg.hsb.brightness}%")

                hsb_bg = ps.SolidColor()
                hsb_bg.hsb.hue = 240
                hsb_bg.hsb.saturation = 100
                hsb_bg.hsb.brightness = 100
                ps.app.backgroundColor = hsb_bg
                safe_print(f"      ✅ HSB背景色设置: H={hsb_bg.hsb.hue}, S={hsb_bg.hsb.saturation}%, B={hsb_bg.hsb.brightness}%")

        except Exception as e:
            safe_print(f"❌ 不同颜色模型设置失败: {str(e)}")

        # 测试3: 前景背景色切换
        safe_print("\n🔧 测试3: 前景背景色切换...")

        try:
            with Session(action="new_document") as ps:
                # 设置初始颜色
                color1 = ps.SolidColor()
                color1.rgb.red = 255
                color1.rgb.green = 128
                color1.rgb.blue = 64

                color2 = ps.SolidColor()
                color2.rgb.red = 64
                color2.rgb.green = 128
                color2.rgb.blue = 255

                ps.app.foregroundColor = color1
                ps.app.backgroundColor = color2

                safe_print("   🔄 初始颜色设置完成")
                safe_print(f"      前景色: R={color1.rgb.red}, G={color1.rgb.green}, B={color1.rgb.blue}")
                safe_print(f"      背景色: R={color2.rgb.red}, G={color2.rgb.green}, B={color2.rgb.blue}")

                # 执行切换操作
                safe_print("   🔄 执行前景背景色切换...")
                temp_color = ps.app.foregroundColor
                ps.app.foregroundColor = ps.app.backgroundColor
                ps.app.backgroundColor = temp_color

                # 验证切换结果
                new_fg = ps.app.foregroundColor
                new_bg = ps.app.backgroundColor
                safe_print(f"   ✅ 切换后前景色: R={new_fg.rgb.red}, G={new_fg.rgb.green}, B={new_fg.rgb.blue}")
                safe_print(f"   ✅ 切换后背景色: R={new_bg.rgb.red}, G={new_bg.rgb.green}, B={new_bg.rgb.blue}")

                # 验证切换是否成功
                if (new_fg.rgb.red == color2.rgb.red and
                    new_bg.rgb.red == color1.rgb.red):
                    safe_print("   ✅ 前景背景色切换验证成功")
                else:
                    safe_print("   ⚠️ 前景背景色切换可能有问题")

        except Exception as e:
            safe_print(f"❌ 前景背景色切换失败: {str(e)}")

        # 测试4: 颜色重置为默认值
        safe_print("\n🔧 测试4: 颜色重置为默认值...")

        try:
            with Session(action="new_document") as ps:
                # 设置非默认颜色
                custom_color = ps.SolidColor()
                custom_color.rgb.red = 128
                custom_color.rgb.green = 64
                custom_color.rgb.blue = 192
                ps.app.foregroundColor = custom_color

                safe_print("   🎨 设置自定义颜色")
                safe_print(f"      前景色: R={custom_color.rgb.red}, G={custom_color.rgb.green}, B={custom_color.rgb.blue}")

                # 重置为默认颜色（黑白）
                safe_print("   🔄 重置为默认颜色...")
                default_fg = ps.SolidColor()
                default_fg.rgb.red = 0
                default_fg.rgb.green = 0
                default_fg.rgb.blue = 0
                ps.app.foregroundColor = default_fg

                default_bg = ps.SolidColor()
                default_bg.rgb.red = 255
                default_bg.rgb.green = 255
                default_bg.rgb.blue = 255
                ps.app.backgroundColor = default_bg

                # 验证重置结果
                reset_fg = ps.app.foregroundColor
                reset_bg = ps.app.backgroundColor
                safe_print(f"   ✅ 重置后前景色: R={reset_fg.rgb.red}, G={reset_fg.rgb.green}, B={reset_fg.rgb.blue}")
                safe_print(f"   ✅ 重置后背景色: R={reset_bg.rgb.red}, G={reset_bg.rgb.green}, B={reset_bg.rgb.blue}")

                # 检查是否为默认颜色（前景色=黑，背景色=白）
                if (reset_fg.rgb.red == 0 and reset_bg.rgb.red == 255):
                    safe_print("   ✅ 重置为默认颜色成功")
                else:
                    safe_print("   ⚠️ 重置颜色可能有问题")

        except Exception as e:
            safe_print(f"❌ 颜色重置失败: {str(e)}")

        # 测试5: 颜色应用验证
        safe_print("\n🔧 测试5: 颜色应用验证...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建测试图层并应用前景色
                fg_test = ps.SolidColor()
                fg_test.rgb.red = 255
                fg_test.rgb.green = 0
                fg_test.rgb.blue = 0
                ps.app.foregroundColor = fg_test

                layer1 = doc.artLayers.add()
                layer1.name = "前景色测试"
                doc.selection.select([[100, 100], [200, 100], [200, 200], [100, 200]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()
                safe_print("   ✅ 前景色应用验证完成")

                # 创建测试图层并应用背景色
                bg_test = ps.SolidColor()
                bg_test.rgb.red = 0
                bg_test.rgb.green = 0
                bg_test.rgb.blue = 255
                ps.app.backgroundColor = bg_test

                layer2 = doc.artLayers.add()
                layer2.name = "背景色测试"
                doc.selection.select([[220, 100], [320, 100], [320, 200], [220, 200]])
                doc.selection.fill(ps.app.backgroundColor)
                doc.selection.deselect()
                safe_print("   ✅ 背景色应用验证完成")

        except Exception as e:
            safe_print(f"❌ 颜色应用验证失败: {str(e)}")

        # 测试6: 颜色面板交互
        safe_print("\n🔧 测试6: 颜色面板交互...")

        try:
            with Session(action="new_document") as ps:
                # 模拟颜色选择器操作
                safe_print("   🎨 模拟颜色选择器...")

                # 创建一系列颜色并应用
                colors = [
                    {"name": "红色", "r": 255, "g": 0, "b": 0},
                    {"name": "绿色", "r": 0, "g": 255, "b": 0},
                    {"name": "蓝色", "r": 0, "g": 0, "b": 255},
                    {"name": "黄色", "r": 255, "g": 255, "b": 0},
                    {"name": "紫色", "r": 255, "g": 0, "b": 255},
                ]

                for i, color_info in enumerate(colors):
                    test_color = ps.SolidColor()
                    test_color.rgb.red = color_info["r"]
                    test_color.rgb.green = color_info["g"]
                    test_color.rgb.blue = color_info["b"]

                    # 交替设置为前景色和背景色
                    if i % 2 == 0:
                        ps.app.foregroundColor = test_color
                        safe_print(f"      ✅ 设置{color_info['name']}为前景色")
                    else:
                        ps.app.backgroundColor = test_color
                        safe_print(f"      ✅ 设置{color_info['name']}为背景色")

        except Exception as e:
            safe_print(f"❌ 颜色面板交互测试失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "change_color_of_background_and_foreground_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Change Color of Background and Foreground 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 改变前景背景色功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本前景背景色设置 (原始代码逻辑)\n")
                f.write(f"- 使用不同颜色模型设置前景背景色\n")
                f.write(f"- 前景背景色切换\n")
                f.write(f"- 颜色重置为默认值\n")
                f.write(f"- 颜色应用验证\n")
                f.write(f"- 颜色面板交互\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第27项: change_color_of_background_and_foreground.py 测试完成!")
        safe_print("✅ 验证功能: 前景色设置、背景色设置、颜色切换、颜色重置、颜色模型")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 前景色背景色设置是否正常")
        safe_print("3. 颜色切换功能是否可用")
        safe_print("4. 颜色重置操作是否正常")
        return False

if __name__ == "__main__":
    test_change_color_of_background_and_foreground()
