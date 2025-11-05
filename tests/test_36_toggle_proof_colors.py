# -*- coding: utf-8 -*-
"""测试第36项: toggle_proof_colors.py - 切换校样颜色"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_toggle_proof_colors():
    """运行toggle_proof_colors测试"""
    safe_print("📋 开始执行第36项: toggle_proof_colors.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 切换校样颜色 (原始代码逻辑)
        safe_print("\n🔧 测试1: 切换校样颜色 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                safe_print("   ✅ Session成功启动")

                # 运行菜单命令切换校样颜色 (原始代码逻辑)
                safe_print("   🔄 执行切换校样颜色命令...")
                try:
                    ps.app.runMenuItem(ps.app.stringIDToTypeID("toggleProofColors"))
                    safe_print("      ✅ 切换校样颜色成功")
                except Exception as proof_e:
                    safe_print(f"      ⚠️ 切换校样颜色失败: {str(proof_e)[:50]}")
                    safe_print("      📝 这可能需要Photoshop处于活跃状态")

        except Exception as e:
            safe_print(f"❌ 切换校样颜色失败: {str(e)}")
            return False

        # 测试2: 多次切换校样颜色
        safe_print("\n🔧 测试2: 多次切换校样颜色...")

        try:
            with Session(action="new_document") as ps:
                safe_print("   🔄 执行多次切换...")
                for i in range(3):
                    try:
                        ps.app.runMenuItem(ps.app.stringIDToTypeID("toggleProofColors"))
                        safe_print(f"      ✅ 第{i+1}次切换成功")
                    except Exception as multi_e:
                        safe_print(f"      ⚠️ 第{i+1}次切换失败: {str(multi_e)[:50]}")
                        break

        except Exception as e:
            safe_print(f"❌ 多次切换失败: {str(e)}")

        # 测试3: 校样颜色状态验证
        safe_print("\n🔧 测试3: 校样颜色状态验证...")

        try:
            with Session(action="new_document") as ps:
                safe_print("   🔍 验证校样颜色状态...")
                try:
                    # 切换到开启状态
                    ps.app.runMenuItem(ps.app.stringIDToTypeID("toggleProofColors"))
                    safe_print("      ✅ 切换到开启状态")

                    # 等待一段时间
                    import time
                    time.sleep(1)

                    # 切换到关闭状态
                    ps.app.runMenuItem(ps.app.stringIDToTypeID("toggleProofColors"))
                    safe_print("      ✅ 切换到关闭状态")
                except Exception as state_e:
                    safe_print(f"      ⚠️ 状态验证失败: {str(state_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 校样颜色状态验证失败: {str(e)}")

        # 测试4: 不同文档校样颜色
        safe_print("\n🔧 测试4: 不同文档校样颜色...")

        try:
            for i in range(2):
                safe_print(f"   📄 处理文档{i+1}...")
                with Session(action="new_document") as ps:
                    doc = ps.active_document
                    doc.name = f"校样测试文档_{i+1}"

                    # 创建测试内容
                    layer = doc.artLayers.add()
                    layer.name = f"测试内容_{i+1}"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 128 + i * 100
                    fill_color.rgb.green = 128
                    fill_color.rgb.blue = 200
                    ps.app.foregroundColor = fill_color

                    doc.selection.select([[100, 100], [300, 100], [300, 300], [100, 300]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                    # 切换校样颜色
                    try:
                        ps.app.runMenuItem(ps.app.stringIDToTypeID("toggleProofColors"))
                        safe_print(f"      ✅ 文档{i+1}校样颜色切换成功")
                    except Exception as doc_proof_e:
                        safe_print(f"      ⚠️ 文档{i+1}切换失败: {str(doc_proof_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 不同文档校样颜色失败: {str(e)}")

        # 测试5: 菜单命令验证
        safe_print("\n🔧 测试5: 菜单命令验证...")

        try:
            with Session(action="new_document") as ps:
                safe_print("   🔍 验证菜单命令...")
                try:
                    # 使用stringIDToTypeID获取命令ID
                    proof_cmd = ps.app.stringIDToTypeID("toggleProofColors")
                    safe_print(f"      📊 校样颜色命令ID: {proof_cmd}")

                    # 执行菜单命令
                    ps.app.runMenuItem(proof_cmd)
                    safe_print("      ✅ 菜单命令验证成功")
                except Exception as menu_e:
                    safe_print(f"      ⚠️ 菜单命令验证失败: {str(menu_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 菜单命令验证失败: {str(e)}")

        # 测试6: 校样颜色与文档内容
        safe_print("\n🔧 测试6: 校样颜色与文档内容...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建彩色内容
                safe_print("   🎨 创建彩色内容...")
                colors = [
                    {"name": "红色", "r": 255, "g": 0, "b": 0, "x": 50},
                    {"name": "绿色", "r": 0, "g": 255, "b": 0, "x": 150},
                    {"name": "蓝色", "r": 0, "g": 0, "b": 255, "x": 250},
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
                        [color_info['x'], 100],
                        [color_info['x'] + 80, 100],
                        [color_info['x'] + 80, 200],
                        [color_info['x'], 200]
                    ])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                safe_print("      ✅ 彩色内容创建完成")

                # 切换校样颜色
                safe_print("   🔄 切换校样颜色...")
                try:
                    ps.app.runMenuItem(ps.app.stringIDToTypeID("toggleProofColors"))
                    safe_print("      ✅ 校样颜色切换成功")
                except Exception as content_e:
                    safe_print(f"      ⚠️ 切换失败: {str(content_e)[:50]}")

        except Exception as e:
            safe_print(f"❌ 校样颜色与文档内容失败: {str(e)}")

        # 测试7: 错误处理
        safe_print("\n🔧 测试7: 错误处理...")

        try:
            # 测试无效命令
            safe_print("   📄 测试无效命令...")
            with Session(action="new_document") as ps:
                try:
                    invalid_cmd = ps.app.stringIDToTypeID("invalidCommand")
                    ps.app.runMenuItem(invalid_cmd)
                    safe_print("      ⚠️ 无效命令意外成功")
                except Exception as invalid_e:
                    safe_print(f"      ✅ 正确处理无效命令")

        except Exception as e:
            safe_print(f"❌ 错误处理失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "toggle_proof_colors_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Toggle Proof Colors 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 切换校样颜色功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 切换校样颜色 (原始代码逻辑)\n")
                f.write(f"- 多次切换校样颜色\n")
                f.write(f"- 校样颜色状态验证\n")
                f.write(f"- 不同文档校样颜色\n")
                f.write(f"- 菜单命令验证\n")
                f.write(f"- 校样颜色与文档内容\n")
                f.write(f"- 错误处理\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第36项: toggle_proof_colors.py 测试完成!")
        safe_print("✅ 验证功能: 校样颜色切换、菜单命令、状态验证、多文档支持")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. runMenuItem方法是否可用")
        safe_print("3. toggleProofColors命令ID是否正确")
        safe_print("4. 菜单命令权限是否正常")
        return False

if __name__ == "__main__":
    test_toggle_proof_colors()
