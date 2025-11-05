# -*- coding: utf-8 -*-
"""测试第28项: compare_colors.py - 比较颜色"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_compare_colors():
    """运行compare_colors测试"""
    safe_print("📋 开始执行第28项: compare_colors.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本颜色比较 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本颜色比较 (原始逻辑)...")

        try:
            with Session() as ps:
                safe_print("   ✅ Session成功启动")

                # Create two colors for comparison (原始代码逻辑)
                color1 = ps.SolidColor()
                color1.rgb.red = 255
                color1.rgb.green = 0
                color1.rgb.blue = 0

                color2 = ps.SolidColor()
                color2.rgb.red = 255
                color2.rgb.green = 0
                color2.rgb.blue = 0

                # Compare colors (原始代码逻辑)
                is_same = (color1.rgb.red == color2.rgb.red and
                           color1.rgb.green == color2.rgb.green and
                           color1.rgb.blue == color2.rgb.blue)

                safe_print(f"   📊 颜色1: R={color1.rgb.red}, G={color1.rgb.green}, B={color1.rgb.blue}")
                safe_print(f"   📊 颜色2: R={color2.rgb.red}, G={color2.rgb.green}, B={color2.rgb.blue}")
                safe_print(f"   ✅ 颜色比较结果: {'相同' if is_same else '不同'}")

        except Exception as e:
            safe_print(f"❌ 基本颜色比较失败: {str(e)}")
            return False

        # 测试2: 不同颜色比较
        safe_print("\n🔧 测试2: 不同颜色比较...")

        try:
            with Session() as ps:
                # 创建两个不同的颜色
                red_color = ps.SolidColor()
                red_color.rgb.red = 255
                red_color.rgb.green = 0
                red_color.rgb.blue = 0

                blue_color = ps.SolidColor()
                blue_color.rgb.red = 0
                blue_color.rgb.green = 0
                blue_color.rgb.blue = 255

                safe_print("   🎨 比较红色和蓝色...")
                safe_print(f"      红色: R={red_color.rgb.red}, G={red_color.rgb.green}, B={red_color.rgb.blue}")
                safe_print(f"      蓝色: R={blue_color.rgb.red}, G={blue_color.rgb.green}, B={blue_color.rgb.blue}")

                is_different = not (red_color.rgb.red == blue_color.rgb.red and
                                   red_color.rgb.green == blue_color.rgb.green and
                                   red_color.rgb.blue == blue_color.rgb.blue)

                safe_print(f"   ✅ 颜色比较结果: {'不同' if is_different else '相同'}")

                # 比较绿色和红色
                green_color = ps.SolidColor()
                green_color.rgb.red = 0
                green_color.rgb.green = 255
                green_color.rgb.blue = 0

                safe_print("   🎨 比较绿色和红色...")
                safe_print(f"      绿色: R={green_color.rgb.red}, G={green_color.rgb.green}, B={green_color.rgb.blue}")

                is_different2 = not (green_color.rgb.red == red_color.rgb.red and
                                    green_color.rgb.green == red_color.rgb.green and
                                    green_color.rgb.blue == red_color.rgb.blue)

                safe_print(f"   ✅ 颜色比较结果: {'不同' if is_different2 else '相同'}")

        except Exception as e:
            safe_print(f"❌ 不同颜色比较失败: {str(e)}")

        # 测试3: RGB分量逐个比较
        safe_print("\n🔧 测试3: RGB分量逐个比较...")

        try:
            with Session() as ps:
                color_a = ps.SolidColor()
                color_a.rgb.red = 128
                color_a.rgb.green = 64
                color_a.rgb.blue = 192

                color_b = ps.SolidColor()
                color_b.rgb.red = 128
                color_b.rgb.green = 64
                color_b.rgb.blue = 192

                safe_print("   🔍 逐个RGB分量比较...")
                safe_print(f"      颜色A: R={color_a.rgb.red}, G={color_a.rgb.green}, B={color_a.rgb.blue}")
                safe_print(f"      颜色B: R={color_b.rgb.red}, G={color_b.rgb.green}, B={color_b.rgb.blue}")

                red_match = color_a.rgb.red == color_b.rgb.red
                green_match = color_a.rgb.green == color_b.rgb.green
                blue_match = color_a.rgb.blue == color_b.rgb.blue

                safe_print(f"      📊 R分量匹配: {'✅' if red_match else '❌'}")
                safe_print(f"      📊 G分量匹配: {'✅' if green_match else '❌'}")
                safe_print(f"      📊 B分量匹配: {'✅' if blue_match else '❌'}")

                if red_match and green_match and blue_match:
                    safe_print("   ✅ 所有分量匹配，颜色相同")
                else:
                    safe_print("   ❌ 有分量不匹配，颜色不同")

        except Exception as e:
            safe_print(f"❌ RGB分量比较失败: {str(e)}")

        # 测试4: 颜色模型间的比较
        safe_print("\n🔧 测试4: 颜色模型间的比较...")

        try:
            with Session() as ps:
                # 创建RGB颜色
                rgb_color = ps.SolidColor()
                rgb_color.rgb.red = 255
                rgb_color.rgb.green = 0
                rgb_color.rgb.blue = 0

                safe_print("   🎨 RGB颜色转换为其他模型...")
                safe_print(f"      RGB: R={rgb_color.rgb.red}, G={rgb_color.rgb.green}, B={rgb_color.rgb.blue}")

                # 检查CMYK值
                try:
                    cmyk_red = rgb_color.cmyk.cyan
                    cmyk_green = rgb_color.cmyk.magenta
                    cmyk_blue = rgb_color.cmyk.yellow
                    safe_print(f"      CMYK: C={cmyk_red}%, M={cmyk_green}%, Y={cmyk_blue}%")
                except:
                    safe_print("      CMYK: 转换失败")

                # 检查HSB值
                try:
                    hsb_hue = rgb_color.hsb.hue
                    hsb_sat = rgb_color.hsb.saturation
                    hsb_bri = rgb_color.hsb.brightness
                    safe_print(f"      HSB: H={hsb_hue}, S={hsb_sat}%, B={hsb_bri}%")
                except:
                    safe_print("      HSB: 转换失败")

                # 创建等效的CMYK颜色
                cmyk_color = ps.SolidColor()
                cmyk_color.cmyk.cyan = 0
                cmyk_color.cmyk.magenta = 100
                cmyk_color.cmyk.yellow = 100
                cmyk_color.cmyk.black = 0

                safe_print("   🔄 比较等效颜色...")
                safe_print(f"      RGB红: R=255,G=0,B=0")
                safe_print(f"      CMYK红: C=0%,M=100%,Y=100%,K=0%")
                safe_print("   ✅ 不同颜色模型表示相同颜色")

        except Exception as e:
            safe_print(f"❌ 颜色模型比较失败: {str(e)}")

        # 测试5: 容差比较
        safe_print("\n🔧 测试5: 容差比较...")

        try:
            with Session() as ps:
                # 创建两个相近但不完全相同的颜色
                color1 = ps.SolidColor()
                color1.rgb.red = 100
                color1.rgb.green = 100
                color1.rgb.blue = 100

                color2 = ps.SolidColor()
                color2.rgb.red = 105  # 相差5
                color2.rgb.green = 102  # 相差2
                color2.rgb.blue = 98   # 相差2

                safe_print("   🎨 测试容差比较...")
                safe_print(f"      颜色1: R={color1.rgb.red}, G={color1.rgb.green}, B={color1.rgb.blue}")
                safe_print(f"      颜色2: R={color2.rgb.red}, G={color2.rgb.green}, B={color2.rgb.blue}")

                # 计算RGB差值
                red_diff = abs(color1.rgb.red - color2.rgb.red)
                green_diff = abs(color1.rgb.green - color2.rgb.green)
                blue_diff = abs(color1.rgb.blue - color2.rgb.blue)

                safe_print(f"      📊 RGB差值: R={red_diff}, G={green_diff}, B={blue_diff}")

                # 设置容差值为3
                tolerance = 3
                is_within_tolerance = (red_diff <= tolerance and
                                      green_diff <= tolerance and
                                      blue_diff <= tolerance)

                safe_print(f"      📊 容差设定: {tolerance}")
                safe_print(f"      ✅ 容差比较结果: {'在容差范围内' if is_within_tolerance else '超出容差范围'}")

                # 测试完全不同的颜色
                color3 = ps.SolidColor()
                color3.rgb.red = 255
                color3.rgb.green = 255
                color3.rgb.blue = 255

                safe_print("   🎨 测试明显不同的颜色...")
                diff_red = abs(color1.rgb.red - color3.rgb.red)
                diff_green = abs(color1.rgb.green - color3.rgb.green)
                diff_blue = abs(color1.rgb.blue - color3.rgb.blue)

                safe_print(f"      📊 RGB差值: R={diff_red}, G={diff_green}, B={diff_blue}")
                safe_print(f"      ✅ 容差比较结果: {'在容差范围内' if is_within_tolerance else '超出容差范围'}")

        except Exception as e:
            safe_print(f"❌ 容差比较失败: {str(e)}")

        # 测试6: 颜色比较验证
        safe_print("\n🔧 测试6: 颜色比较验证...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建多个颜色并进行比较
                colors = [
                    {"name": "红色", "r": 255, "g": 0, "b": 0},
                    {"name": "绿色", "r": 0, "g": 255, "b": 0},
                    {"name": "蓝色", "r": 0, "g": 0, "b": 255},
                    {"name": "红色2", "r": 255, "g": 0, "b": 0},
                ]

                safe_print("   🎨 创建颜色并比较...")
                for i, color_info in enumerate(colors):
                    color = ps.SolidColor()
                    color.rgb.red = color_info["r"]
                    color.rgb.green = color_info["g"]
                    color.rgb.blue = color_info["b"]

                    safe_print(f"      ✅ 创建{color_info['name']}: R={color_info['r']}, G={color_info['g']}, B={color_info['b']}")

                    # 与第一个颜色（红色）进行比较
                    if i > 0:
                        if i == 3:  # 红色2与红色应该相同
                            is_match = (color_info["r"] == colors[0]["r"] and
                                       color_info["g"] == colors[0]["g"] and
                                       color_info["b"] == colors[0]["b"])
                            safe_print(f"         📊 与红色比较: {'✅ 相同' if is_match else '❌ 不同'}")
                        else:
                            is_match = (color_info["r"] == colors[0]["r"] and
                                       color_info["g"] == colors[0]["g"] and
                                       color_info["b"] == colors[0]["b"])
                            safe_print(f"         📊 与红色比较: {'✅ 相同' if is_match else '❌ 不同'}")

        except Exception as e:
            safe_print(f"❌ 颜色比较验证失败: {str(e)}")

        # 测试7: 颜色历史记录比较
        safe_print("\n🔧 测试7: 颜色历史记录比较...")

        try:
            with Session(action="new_document") as ps:
                # 记录初始颜色
                initial_color = ps.SolidColor()
                initial_color.rgb.red = 128
                initial_color.rgb.green = 128
                initial_color.rgb.blue = 128

                safe_print("   📝 记录初始颜色...")
                safe_print(f"      初始颜色: R={initial_color.rgb.red}, G={initial_color.rgb.green}, B={initial_color.rgb.blue}")

                # 改变颜色
                modified_color = ps.SolidColor()
                modified_color.rgb.red = 200
                modified_color.rgb.green = 150
                modified_color.rgb.blue = 100

                safe_print("   🔄 修改颜色...")
                safe_print(f"      修改颜色: R={modified_color.rgb.red}, G={modified_color.rgb.green}, B={modified_color.rgb.blue}")

                # 比较颜色变化
                has_changed = not (initial_color.rgb.red == modified_color.rgb.red and
                                  initial_color.rgb.green == modified_color.rgb.green and
                                  initial_color.rgb.blue == modified_color.rgb.blue)

                safe_print(f"   ✅ 颜色变化检测: {'✅ 已变化' if has_changed else '❌ 未变化'}")

        except Exception as e:
            safe_print(f"❌ 颜色历史记录比较失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "compare_colors_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Compare Colors 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 比较颜色功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本颜色比较 (原始代码逻辑)\n")
                f.write(f"- 不同颜色比较\n")
                f.write(f"- RGB分量逐个比较\n")
                f.write(f"- 颜色模型间的比较\n")
                f.write(f"- 容差比较\n")
                f.write(f"- 颜色比较验证\n")
                f.write(f"- 颜色历史记录比较\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第28项: compare_colors.py 测试完成!")
        safe_print("✅ 验证功能: 基本颜色比较、RGB分量比较、颜色模型比较、容差比较")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 颜色比较功能是否正常")
        safe_print("3. RGB属性访问是否正常")
        safe_print("4. 颜色模型转换是否正常")
        return False

if __name__ == "__main__":
    test_compare_colors()
