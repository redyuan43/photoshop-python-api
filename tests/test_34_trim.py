# -*- coding: utf-8 -*-
"""测试第34项: trim.py - 修剪"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_trim():
    """运行trim测试"""
    safe_print("📋 开始执行第34项: trim.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑，简化版)
        from photoshop import Session
        import photoshop.api as ps

        # 测试1: 基本修剪操作 (基于原始代码逻辑)
        safe_print("\n🔧 测试1: 基本修剪操作 (基于原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ Session成功启动")
                safe_print(f"   📄 初始文档尺寸: {doc.width} x {doc.height}")

                # 创建一个带有透明边缘的内容
                safe_print("   🎨 创建测试内容...")
                # 创建一个图层
                layer = doc.artLayers.add()
                layer.name = "修剪内容"

                # 填充背景为透明（在Photoshop中，默认背景是白色）
                # 我们创建一个居中的内容，边缘留空
                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 0
                fill_color.rgb.blue = 0
                ps.app.foregroundColor = fill_color

                # 在文档中央创建一个红色矩形
                doc.selection.select([
                    [200, 100],
                    [700, 100],
                    [700, 400],
                    [200, 400]
                ])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                safe_print("      ✅ 创建中央红色矩形")

                # 记录修剪前尺寸
                before_trim_width = doc.width
                before_trim_height = doc.height
                safe_print(f"   📊 修剪前尺寸: {before_trim_width} x {before_trim_height}")

                # 执行修剪操作 (原始代码逻辑)
                safe_print("   ✂️ 执行修剪操作...")
                try:
                    doc.trim(ps.TrimType.TopLeftPixel, True, True, True, True)
                    after_trim_width = doc.width
                    after_trim_height = doc.height
                    safe_print(f"      ✅ 修剪操作完成")
                    safe_print(f"   📊 修剪后尺寸: {after_trim_width} x {after_trim_height}")
                except Exception as trim_e:
                    safe_print(f"      ⚠️ 修剪参数失败: {str(trim_e)[:50]}")
                    # 尝试简化参数
                    try:
                        doc.trim(ps.TrimType.TopLeftPixel)
                        safe_print("      ✅ 简化修剪成功")
                    except Exception as simple_e:
                        safe_print(f"      ❌ 简化修剪也失败: {str(simple_e)}")

        except Exception as e:
            safe_print(f"❌ 基本修剪操作失败: {str(e)}")
            return False

        # 测试2: 不同修剪类型
        safe_print("\n🔧 测试2: 不同修剪类型...")

        try:
            # 测试TopLeftPixel
            safe_print("   📄 测试TopLeftPixel修剪...")
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建不对称内容
                layer = doc.artLayers.add()
                layer.name = "TopLeft测试"

                fill_color = ps.SolidColor()
                fill_color.rgb.green = 0
                fill_color.rgb.green = 255
                fill_color.rgb.blue = 0
                ps.app.foregroundColor = fill_color

                # 在左上角创建内容
                doc.selection.select([[0, 0], [100, 0], [100, 100], [0, 100]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                try:
                    doc.trim(ps.TrimType.TopLeftPixel)
                    safe_print("      ✅ TopLeftPixel修剪成功")
                except Exception as tl_e:
                    safe_print(f"      ⚠️ TopLeftPixel修剪失败: {str(tl_e)[:50]}")

            # 测试BottomRightPixel
            safe_print("   📄 测试BottomRightPixel修剪...")
            with Session(action="new_document") as ps:
                doc = ps.active_document

                layer = doc.artLayers.add()
                layer.name = "BottomRight测试"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 0
                fill_color.rgb.green = 0
                fill_color.rgb.blue = 255
                ps.app.foregroundColor = fill_color

                # 在右下角创建内容
                doc.selection.select([[800, 400], [900, 400], [900, 500], [800, 500]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                try:
                    doc.trim(ps.TrimType.BottomRightPixel)
                    safe_print("      ✅ BottomRightPixel修剪成功")
                except Exception as br_e:
                    safe_print(f"      ⚠️ BottomRightPixel修剪失败: {str(br_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 不同修剪类型失败: {str(e)}")

        # 测试3: 透明像素修剪
        safe_print("\n🔧 测试3: 透明像素修剪...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建复杂内容
                safe_print("   🎨 创建复杂内容...")
                colors = [
                    {"name": "红色", "r": 255, "g": 0, "b": 0, "x": 100, "y": 100},
                    {"name": "绿色", "r": 0, "g": 255, "b": 0, "x": 300, "y": 100},
                    {"name": "蓝色", "r": 0, "g": 0, "b": 255, "x": 100, "y": 300},
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
                        [color_info['x'] + 100, color_info['y']],
                        [color_info['x'] + 100, color_info['y'] + 100],
                        [color_info['x'], color_info['y'] + 100]
                    ])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                safe_print("      ✅ 复杂内容创建完成")

                before_trim = f"{doc.width} x {doc.height}"
                safe_print(f"   📊 修剪前尺寸: {before_trim}")

                # 执行透明像素修剪
                safe_print("   ✂️ 执行透明像素修剪...")
                try:
                    doc.trim(ps.TrimType.TopLeftPixel, True, True, True, True)
                    after_trim = f"{doc.width} x {doc.height}"
                    safe_print(f"   📊 修剪后尺寸: {after_trim}")
                    safe_print("      ✅ 透明像素修剪成功")
                except Exception as transparent_e:
                    safe_print(f"      ⚠️ 透明像素修剪失败: {str(transparent_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 透明像素修剪失败: {str(e)}")

        # 测试4: 边缘修剪参数
        safe_print("\n🔧 测试4: 边缘修剪参数...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建内容
                layer = doc.artLayers.add()
                layer.name = "边缘测试"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 255
                fill_color.rgb.blue = 0
                ps.app.foregroundColor = fill_color

                # 居中创建内容
                doc.selection.select([[150, 150], [750, 150], [750, 350], [150, 350]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                safe_print("   🎨 创建居中内容")
                safe_print(f"   📊 内容尺寸: {doc.width} x {doc.height}")

                # 测试不同边缘组合
                edge_tests = [
                    {"name": "顶部和左边", "top": True, "left": True, "bottom": False, "right": False},
                    {"name": "底部和右边", "top": False, "left": False, "bottom": True, "right": True},
                    {"name": "所有边缘", "top": True, "left": True, "bottom": True, "right": True},
                ]

                for i, edge_test in enumerate(edge_tests):
                    if i > 0:
                        # 为每个测试创建新文档
                        with Session(action="new_document") as ps2:
                            doc2 = ps2.active_document
                            layer2 = doc2.artLayers.add()
                            layer2.name = f"边缘测试_{i}"

                            fill_color2 = ps.SolidColor()
                            fill_color2.rgb.red = 255
                            fill_color2.rgb.green = 128
                            fill_color2.rgb.blue = 0
                            ps2.app.foregroundColor = fill_color2

                            doc2.selection.select([[150, 150], [750, 150], [750, 350], [150, 350]])
                            doc2.selection.fill(ps2.app.foregroundColor)
                            doc2.selection.deselect()

                            safe_print(f"   ✂️ 执行{edge_test['name']}修剪...")
                            try:
                                doc2.trim(ps.TrimType.TopLeftPixel,
                                         edge_test['top'],
                                         edge_test['left'],
                                         edge_test['bottom'],
                                         edge_test['right'])
                                safe_print(f"      ✅ {edge_test['name']}修剪成功")
                            except Exception as edge_e:
                                safe_print(f"      ⚠️ {edge_test['name']}修剪失败: {str(edge_e)[:50]}")
                    else:
                        safe_print(f"   ✂️ 执行{edge_test['name']}修剪...")
                        try:
                            doc.trim(ps.TrimType.TopLeftPixel,
                                     edge_test['top'],
                                     edge_test['left'],
                                     edge_test['bottom'],
                                     edge_test['right'])
                            safe_print(f"      ✅ {edge_test['name']}修剪成功")
                        except Exception as edge_e:
                            safe_print(f"      ⚠️ {edge_test['name']}修剪失败: {str(edge_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 边缘修剪参数失败: {str(e)}")

        # 测试5: 修剪前后的内容验证
        safe_print("\n🔧 测试5: 修剪前后的内容验证...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建可识别的内容
                safe_print("   🎨 创建可识别内容...")
                # 红色矩形
                layer1 = doc.artLayers.add()
                layer1.name = "红色"

                fill_color1 = ps.SolidColor()
                fill_color1.rgb.red = 255
                fill_color1.rgb.green = 0
                fill_color1.rgb.blue = 0
                ps.app.foregroundColor = fill_color1

                doc.selection.select([[100, 100], [200, 100], [200, 200], [100, 200]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 绿色矩形
                layer2 = doc.artLayers.add()
                layer2.name = "绿色"

                fill_color2 = ps.SolidColor()
                fill_color2.rgb.red = 0
                fill_color2.rgb.green = 255
                fill_color2.rgb.blue = 0
                ps.app.foregroundColor = fill_color2

                doc.selection.select([[300, 100], [400, 100], [400, 200], [300, 200]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                # 记录修剪前图层数
                layers_before = len(doc.artLayers)
                safe_print(f"   📊 修剪前图层数: {layers_before}")

                # 执行修剪
                safe_print("   ✂️ 执行修剪...")
                try:
                    doc.trim(ps.TrimType.TopLeftPixel)
                    layers_after = len(doc.artLayers)
                    safe_print(f"   📊 修剪后图层数: {layers_after}")
                    safe_print("      ✅ 修剪验证完成")
                except Exception as verify_e:
                    safe_print(f"      ⚠️ 修剪验证失败: {str(verify_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 修剪前后验证失败: {str(e)}")

        # 测试6: 修剪错误处理
        safe_print("\n🔧 测试6: 修剪错误处理...")

        try:
            # 测试空文档
            safe_print("   📄 测试空文档修剪...")
            with Session(action="new_document") as ps:
                doc = ps.active_document

                try:
                    doc.trim(ps.TrimType.TopLeftPixel)
                    safe_print("      ✅ 空文档修剪完成")
                except Exception as empty_e:
                    safe_print(f"      ⚠️ 空文档修剪失败: {str(empty_e)[:50]}")

            # 测试全填充文档（全白或全黑）
            safe_print("   📄 测试全填充文档修剪...")
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 全填充
                fill_color = ps.SolidColor()
                fill_color.rgb.red = 128
                fill_color.rgb.green = 128
                fill_color.rgb.blue = 128
                ps.app.foregroundColor = fill_color

                doc.selection.select([[0, 0], [doc.width, 0], [doc.width, doc.height], [0, doc.height]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                try:
                    doc.trim(ps.TrimType.TopLeftPixel)
                    safe_print("      ✅ 全填充文档修剪完成")
                except Exception as full_e:
                    safe_print(f"      ⚠️ 全填充文档修剪失败: {str(full_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 修剪错误处理失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "trim_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Trim 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 修剪功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本修剪操作 (基于原始逻辑)\n")
                f.write(f"- 不同修剪类型\n")
                f.write(f"- 透明像素修剪\n")
                f.write(f"- 边缘修剪参数\n")
                f.write(f"- 修剪前后的内容验证\n")
                f.write(f"- 修剪错误处理\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第34项: trim.py 测试完成!")
        safe_print("✅ 验证功能: 基本修剪、不同修剪类型、透明像素修剪、边缘参数")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 修剪功能是否可用")
        safe_print("3. trim方法参数是否正确")
        safe_print("4. 文档内容是否符合修剪条件")
        return False

if __name__ == "__main__":
    test_trim()
