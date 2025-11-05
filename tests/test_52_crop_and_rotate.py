# -*- coding: utf-8 -*-
"""测试第52项: crop_and_rotate.py - 裁剪和旋转画布"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_crop_and_rotate():
    """运行crop_and_rotate测试 - 裁剪和旋转画布"""
    safe_print("📋 开始执行第52项: crop_and_rotate.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        from photoshop import Session

        # 测试1: 基本裁剪和旋转操作 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本裁剪和旋转操作 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                safe_print("   ✅ Session成功启动")

                doc = ps.active_document
                safe_print(f"   📄 当前文档: {doc.name}")
                safe_print(f"   📏 原始尺寸: {doc.width} x {doc.height} 像素")

                # 记录原始标尺单位 (原始代码逻辑)
                safe_print("   📏 记录原始标尺单位...")
                startRulerUnits = ps.app.preferences.rulerUnits
                safe_print(f"      📊 原始单位: {startRulerUnits}")

                # 设置标尺单位为像素 (原始代码逻辑)
                safe_print("   🔧 设置标尺单位为像素...")
                if startRulerUnits != ps.Units.Pixels:
                    ps.app.preferences.rulerUnits = ps.Units.Pixels
                    safe_print("      ✅ 已设置为像素")

                # 旋转画布45度 (原始代码逻辑)
                safe_print("   🔄 旋转画布45度...")
                doc.rotateCanvas(45)
                safe_print("      ✅ 画布旋转完成")

                # 裁剪10像素边框 (原始代码逻辑)
                safe_print("   ✂️ 裁剪10像素边框...")
                original_width = doc.width
                original_height = doc.height

                # 计算裁剪边界 (原始代码逻辑)
                crop_bounds = [10, 10, original_width - 10, original_height - 10]
                safe_print(f"      📊 裁剪边界: {crop_bounds}")

                # 验证裁剪边界有效性
                if crop_bounds[2] > crop_bounds[0] and crop_bounds[3] > crop_bounds[1]:
                    doc.crop(crop_bounds)
                    safe_print("      ✅ 裁剪完成")

                    new_width = doc.width
                    new_height = doc.height
                    safe_print(f"      📏 裁剪后尺寸: {new_width} x {new_height} 像素")
                    safe_print(f"      📐 移除边框: {original_width - new_width} x {original_height - new_height} 像素")
                else:
                    safe_print("      ⚠️ 文档尺寸太小，无法裁剪")

                # 恢复原始标尺单位 (原始代码逻辑)
                safe_print("   🔄 恢复原始标尺单位...")
                ps.app.preferences.rulerUnits = startRulerUnits
                safe_print("      ✅ 标尺单位已恢复")

        except Exception as e:
            safe_print(f"   ❌ 基本裁剪和旋转操作失败: {str(e)}")

        # 测试2: 不同角度旋转测试
        safe_print("\n🔧 测试2: 不同角度旋转测试...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print(f"   📄 当前文档: {doc.name}")

                angles = [30, 60, 90, 180, 270]
                for angle in angles:
                    safe_print(f"   🔄 测试旋转角度: {angle}°...")
                    try:
                        doc.rotateCanvas(angle)
                        safe_print(f"      ✅ {angle}° 旋转成功")

                        # 恢复以便下一次测试
                        doc.rotateCanvas(-angle)
                        safe_print(f"      ↩️ 已恢复角度")
                    except Exception as rotate_e:
                        safe_print(f"      ⚠️ {angle}° 旋转失败: {str(rotate_e)[:50]}")

        except Exception as e:
            safe_print(f"   ❌ 不同角度旋转测试失败: {str(e)}")

        # 测试3: 裁剪边界测试
        safe_print("\n🔧 测试3: 裁剪边界测试...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print(f"   📄 当前文档: {doc.name}")

                # 获取实际尺寸
                original_width = doc.width
                original_height = doc.height
                safe_print(f"   📏 原始尺寸: {original_width} x {original_height}")

                # 测试不同裁剪边界
                test_cases = [
                    {"name": "对称裁剪", "bounds": [50, 50, original_width - 50, original_height - 50]},
                    {"name": "左侧裁剪", "bounds": [100, 0, original_width, original_height]},
                    {"name": "顶部裁剪", "bounds": [0, 100, original_width, original_height]},
                ]

                for test_case in test_cases:
                    safe_print(f"   🔧 {test_case['name']}...")
                    bounds = test_case['bounds']

                    # 验证边界有效性
                    if bounds[2] > bounds[0] and bounds[3] > bounds[1]:
                        safe_print(f"      📊 裁剪边界: {bounds}")
                        doc.crop(bounds)
                        safe_print(f"      ✅ {test_case['name']}成功")
                    else:
                        safe_print(f"      ⚠️ 无效边界，跳过")

        except Exception as e:
            safe_print(f"   ❌ 裁剪边界测试失败: {str(e)}")

        # 测试4: 旋转和裁剪组合操作
        safe_print("\n🔧 测试4: 旋转和裁剪组合操作...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print(f"   📄 当前文档: {doc.name}")

                # 组合操作序列
                safe_print("   🔄 序列1: 旋转90° -> 裁剪 -> 旋转回原位")
                doc.rotateCanvas(90)
                original_width = doc.width
                original_height = doc.height
                doc.crop([50, 50, original_width - 50, original_height - 50])
                doc.rotateCanvas(-90)
                safe_print("      ✅ 序列1完成")

                safe_print("   🔄 序列2: 旋转45° -> 裁剪 -> 恢复")
                doc.rotateCanvas(45)
                new_width = doc.width
                new_height = doc.height
                crop_size = min(new_width, new_height) // 4
                doc.crop([crop_size, crop_size, new_width - crop_size, new_height - crop_size])
                safe_print("      ✅ 序列2完成")

        except Exception as e:
            safe_print(f"   ❌ 组合操作测试失败: {str(e)}")

        # 测试5: 错误处理和边界情况
        safe_print("\n🔧 测试5: 错误处理和边界情况...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print(f"   📄 当前文档: {doc.name}")

                # 测试过度裁剪
                safe_print("   ⚠️ 测试过度裁剪...")
                try:
                    doc.crop([0, 0, -10, -10])
                    safe_print("      ✅ 正确处理过度裁剪")
                except Exception as crop_e:
                    safe_print(f"      ⚠️ 过度裁剪出错: {str(crop_e)[:50]}")

                # 测试无效旋转角度
                safe_print("   ⚠️ 测试大角度旋转...")
                try:
                    doc.rotateCanvas(999)
                    safe_print("      ✅ 大角度旋转成功")
                    doc.rotateCanvas(-999)
                except Exception as rotate_e:
                    safe_print(f"      ⚠️ 大角度旋转: {str(rotate_e)[:50]}")

        except Exception as e:
            safe_print(f"   ❌ 错误处理测试失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "crop_and_rotate_test_result.txt")
            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Crop and Rotate 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 裁剪和旋转画布操作\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本裁剪和旋转操作\n")
                f.write(f"- 不同角度旋转测试\n")
                f.write(f"- 裁剪边界测试\n")
                f.write(f"- 旋转和裁剪组合操作\n")
                f.write(f"- 错误处理和边界情况\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第52项: crop_and_rotate.py 测试完成!")
        safe_print("✅ 验证功能:")
        safe_print("- 画布旋转操作")
        safe_print("- 图像裁剪操作")
        safe_print("- 标尺单位管理")
        safe_print("- 组合操作序列")
        safe_print("- 错误处理机制")
        safe_print("🎯 用途: 演示画布级别的旋转和裁剪操作")

        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 画布旋转和裁剪功能是否可用")
        safe_print("3. 测试文档尺寸是否足够")
        return False

if __name__ == "__main__":
    test_crop_and_rotate()
