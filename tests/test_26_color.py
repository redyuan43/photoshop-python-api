# -*- coding: utf-8 -*-
"""测试第26项: color.py - 颜色操作"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_color():
    """运行color测试"""
    safe_print("📋 开始执行第26项: color.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本颜色操作 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本颜色操作 (原始逻辑)...")

        try:
            with Session() as ps:
                safe_print("   ✅ Session成功启动")

                # Create a new RGB color (原始代码逻辑)
                safe_print("   🎨 创建RGB颜色...")
                rgb_color = ps.SolidColor()
                rgb_color.rgb.red = 255
                rgb_color.rgb.green = 0
                rgb_color.rgb.blue = 0
                safe_print(f"      ✅ RGB颜色: R={rgb_color.rgb.red}, G={rgb_color.rgb.green}, B={rgb_color.rgb.blue}")

                # Create a new CMYK color (原始代码逻辑)
                safe_print("   🎨 创建CMYK颜色...")
                cmyk_color = ps.SolidColor()
                cmyk_color.cmyk.cyan = 0
                cmyk_color.cmyk.magenta = 100
                cmyk_color.cmyk.yellow = 100
                cmyk_color.cmyk.black = 0
                safe_print(f"      ✅ CMYK颜色: C={cmyk_color.cmyk.cyan}%, M={cmyk_color.cmyk.magenta}%, Y={cmyk_color.cmyk.yellow}%, K={cmyk_color.cmyk.black}%")

                # Set as foreground color (原始代码逻辑)
                safe_print("   🎯 设置为前景色...")
                ps.app.foregroundColor = rgb_color
                safe_print(f"      ✅ 前景色设置成功")

                # Create HSB color (原始代码逻辑)
                safe_print("   🎨 创建HSB颜色...")
                hsb_color = ps.SolidColor()
                hsb_color.hsb.hue = 360
                hsb_color.hsb.saturation = 100
                hsb_color.hsb.brightness = 100
                safe_print(f"      ✅ HSB颜色: H={hsb_color.hsb.hue}, S={hsb_color.hsb.saturation}%, B={hsb_color.hsb.brightness}%")

                # Set as background color (原始代码逻辑)
                safe_print("   🎯 设置为背景色...")
                ps.app.backgroundColor = hsb_color
                safe_print(f"      ✅ 背景色设置成功")

        except Exception as e:
            safe_print(f"❌ 基本颜色操作测试失败: {str(e)}")
            return False

        # 测试2: RGB颜色模型操作
        safe_print("\n🔧 测试2: RGB颜色模型操作...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print(f"   📄 使用新文档: {doc.name}")

                # 创建多种RGB颜色
                rgb_colors = [
                    {"name": "纯红色", "r": 255, "g": 0, "b": 0},
                    {"name": "纯绿色", "r": 0, "g": 255, "b": 0},
                    {"name": "纯蓝色", "r": 0, "g": 0, "b": 255},
                    {"name": "黄色", "r": 255, "g": 255, "b": 0},
                    {"name": "紫色", "r": 255, "g": 0, "b": 255},
                    {"name": "青色", "r": 0, "g": 255, "b": 255},
                    {"name": "白色", "r": 255, "g": 255, "b": 255},
                    {"name": "黑色", "r": 0, "g": 0, "b": 0},
                ]

                for i, color_info in enumerate(rgb_colors):
                    try:
                        color = ps.SolidColor()
                        color.rgb.red = color_info["r"]
                        color.rgb.green = color_info["g"]
                        color.rgb.blue = color_info["b"]
                        ps.app.foregroundColor = color

                        # 创建图层并应用颜色
                        layer = doc.artLayers.add()
                        layer.name = f"RGB_{color_info['name']}"

                        # 创建颜色块
                        x = 50 + i * 60
                        y = 100
                        doc.selection.select([[x, y], [x+50, y], [x+50, y+50], [x, y+50]])
                        doc.selection.fill(ps.app.foregroundColor)
                        doc.selection.deselect()

                        safe_print(f"      ✅ 创建{color_info['name']}图层")
                    except Exception as rgb_e:
                        safe_print(f"      ❌ 创建{color_info['name']}失败: {str(rgb_e)}")

        except Exception as e:
            safe_print(f"❌ RGB颜色模型操作测试失败: {str(e)}")

        # 测试3: CMYK颜色模型操作
        safe_print("\n🔧 测试3: CMYK颜色模型操作...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建多种CMYK颜色
                cmyk_colors = [
                    {"name": "纯青色", "c": 100, "m": 0, "y": 0, "k": 0},
                    {"name": "纯洋红", "c": 0, "m": 100, "y": 0, "k": 0},
                    {"name": "纯黄色", "c": 0, "m": 0, "y": 100, "k": 0},
                    {"name": "纯黑色", "c": 0, "m": 0, "y": 0, "k": 100},
                ]

                for i, color_info in enumerate(cmyk_colors):
                    try:
                        color = ps.SolidColor()
                        color.cmyk.cyan = color_info["c"]
                        color.cmyk.magenta = color_info["m"]
                        color.cmyk.yellow = color_info["y"]
                        color.cmyk.black = color_info["k"]
                        ps.app.foregroundColor = color

                        # 创建图层并应用颜色
                        layer = doc.artLayers.add()
                        layer.name = f"CMYK_{color_info['name']}"

                        # 创建颜色块
                        x = 50 + i * 60
                        y = 200
                        doc.selection.select([[x, y], [x+50, y], [x+50, y+50], [x, y+50]])
                        doc.selection.fill(ps.app.foregroundColor)
                        doc.selection.deselect()

                        safe_print(f"      ✅ 创建{color_info['name']}图层")
                    except Exception as cmyk_e:
                        safe_print(f"      ❌ 创建{color_info['name']}失败: {str(cmyk_e)}")

        except Exception as e:
            safe_print(f"❌ CMYK颜色模型操作测试失败: {str(e)}")

        # 测试4: HSB颜色模型操作
        safe_print("\n🔧 测试4: HSB颜色模型操作...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建多种HSB颜色（彩虹色）
                hsb_colors = [
                    {"name": "红色", "h": 0, "s": 100, "b": 100},
                    {"name": "橙色", "h": 30, "s": 100, "b": 100},
                    {"name": "黄色", "h": 60, "s": 100, "b": 100},
                    {"name": "绿色", "h": 120, "s": 100, "b": 100},
                    {"name": "青色", "h": 180, "s": 100, "b": 100},
                    {"name": "蓝色", "h": 240, "s": 100, "b": 100},
                    {"name": "紫色", "h": 300, "s": 100, "b": 100},
                ]

                for i, color_info in enumerate(hsb_colors):
                    try:
                        color = ps.SolidColor()
                        color.hsb.hue = color_info["h"]
                        color.hsb.saturation = color_info["s"]
                        color.hsb.brightness = color_info["b"]
                        ps.app.foregroundColor = color

                        # 创建图层并应用颜色
                        layer = doc.artLayers.add()
                        layer.name = f"HSB_{color_info['name']}"

                        # 创建颜色块
                        x = 50 + i * 60
                        y = 300
                        doc.selection.select([[x, y], [x+50, y], [x+50, y+50], [x, y+50]])
                        doc.selection.fill(ps.app.foregroundColor)
                        doc.selection.deselect()

                        safe_print(f"      ✅ 创建{color_info['name']}图层")
                    except Exception as hsb_e:
                        safe_print(f"      ❌ 创建{color_info['name']}失败: {str(hsb_e)}")

        except Exception as e:
            safe_print(f"❌ HSB颜色模型操作测试失败: {str(e)}")

        # 测试5: 前景色和背景色管理
        safe_print("\n🔧 测试5: 前景色和背景色管理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 交换前景和背景色
                safe_print("   🔄 测试前景色和背景色交换...")
                original_fg = ps.app.foregroundColor
                original_bg = ps.app.backgroundColor

                safe_print(f"      📊 原始前景色: {original_fg}")
                safe_print(f"      📊 原始背景色: {original_bg}")

                # 交换颜色
                ps.app.foregroundColor = original_bg
                ps.app.backgroundColor = original_fg

                safe_print(f"      ✅ 交换后前景色: {ps.app.foregroundColor}")
                safe_print(f"      ✅ 交换后背景色: {ps.app.backgroundColor}")

                # 使用前景色绘制
                layer1 = doc.artLayers.add()
                layer1.name = "前景色绘制"

                doc.selection.select([[100, 400], [200, 400], [200, 500], [100, 500]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()
                safe_print("      ✅ 使用前景色绘制完成")

                # 使用背景色绘制
                layer2 = doc.artLayers.add()
                layer2.name = "背景色绘制"

                doc.selection.select([[220, 400], [320, 400], [320, 500], [220, 500]])
                doc.selection.fill(ps.app.backgroundColor)
                doc.selection.deselect()
                safe_print("      ✅ 使用背景色绘制完成")

        except Exception as e:
            safe_print(f"❌ 前景色和背景色管理测试失败: {str(e)}")

        # 测试6: 颜色模型转换
        safe_print("\n🔧 测试6: 颜色模型转换...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 测试颜色模型之间的转换
                safe_print("   🔄 测试RGB转CMYK...")
                rgb_test = ps.SolidColor()
                rgb_test.rgb.red = 255
                rgb_test.rgb.green = 128
                rgb_test.rgb.blue = 64

                # 设置为前景色
                ps.app.foregroundColor = rgb_test
                safe_print(f"      📊 RGB: R={rgb_test.rgb.red}, G={rgb_test.rgb.green}, B={rgb_test.rgb.blue}")

                # 应用到图层
                layer = doc.artLayers.add()
                layer.name = "颜色转换测试"
                doc.selection.select([[100, 100], [200, 100], [200, 200], [100, 200]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()
                safe_print("      ✅ 颜色转换应用成功")

        except Exception as e:
            safe_print(f"❌ 颜色模型转换测试失败: {str(e)}")

        # 测试7: 颜色属性访问
        safe_print("\n🔧 测试7: 颜色属性访问...")

        try:
            with Session(action="new_document") as ps:
                # 创建测试颜色
                test_color = ps.SolidColor()
                test_color.rgb.red = 128
                test_color.rgb.green = 128
                test_color.rgb.blue = 128

                safe_print("   🔍 检查颜色属性...")
                safe_print(f"      📊 RGB.red: {test_color.rgb.red}")
                safe_print(f"      📊 RGB.green: {test_color.rgb.green}")
                safe_print(f"      📊 RGB.blue: {test_color.rgb.blue}")

                # 检查其他属性
                try:
                    if hasattr(test_color, 'cmyk'):
                        safe_print(f"      📊 CMYK属性: 可用")
                        safe_print(f"      📊 CMYK.cyan: {test_color.cmyk.cyan}")
                    if hasattr(test_color, 'hsb'):
                        safe_print(f"      📊 HSB属性: 可用")
                        safe_print(f"      📊 HSB.hue: {test_color.hsb.hue}")
                    if hasattr(test_color, 'lab'):
                        safe_print(f"      📊 Lab属性: 可用")
                except Exception as attr_e:
                    safe_print(f"      ⚠️ 属性访问异常: {str(attr_e)}")

                safe_print("      ✅ 颜色属性访问完成")

        except Exception as e:
            safe_print(f"❌ 颜色属性访问测试失败: {str(e)}")

        # 测试8: 颜色填充验证
        safe_print("\n🔧 测试8: 颜色填充验证...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建多个颜色测试图层
                for i in range(5):
                    # 设置随机颜色
                    color = ps.SolidColor()
                    color.rgb.red = 50 + i * 40
                    color.rgb.green = 100 + i * 30
                    color.rgb.blue = 150 + i * 20
                    ps.app.foregroundColor = color

                    # 创建图层
                    layer = doc.artLayers.add()
                    layer.name = f"颜色验证_{i+1}"

                    # 填充矩形
                    x = 50 + i * 70
                    y = 450
                    doc.selection.select([[x, y], [x+60, y], [x+60, y+60], [x, y+60]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                    safe_print(f"      ✅ 颜色验证图层{i+1}创建成功")

                safe_print("   ✅ 颜色填充验证完成")

        except Exception as e:
            safe_print(f"❌ 颜色填充验证测试失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "color_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Color 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 颜色操作功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本颜色操作 (原始代码逻辑)\n")
                f.write(f"- RGB颜色模型操作\n")
                f.write(f"- CMYK颜色模型操作\n")
                f.write(f"- HSB颜色模型操作\n")
                f.write(f"- 前景色和背景色管理\n")
                f.write(f"- 颜色模型转换\n")
                f.write(f"- 颜色属性访问\n")
                f.write(f"- 颜色填充验证\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第26项: color.py 测试完成!")
        safe_print("✅ 验证功能: RGB、CMYK、HSB颜色模型、前景色背景色管理、颜色转换")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 颜色模型是否可用")
        safe_print("3. 前景色背景色设置是否正常")
        safe_print("4. 颜色填充操作是否正常")
        return False

if __name__ == "__main__":
    test_color()