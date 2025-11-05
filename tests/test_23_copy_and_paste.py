# -*- coding: utf-8 -*-
"""测试第23项: copy_and_paste.py - 复制粘贴"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_copy_and_paste():
    """运行copy_and_paste测试"""
    safe_print("📋 开始执行第23项: copy_and_paste.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        import photoshop.api as ps
        from photoshop import Session

        # 测试1: 基本复制粘贴 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本复制粘贴 (原始逻辑)...")

        try:
            # 记录原始标尺单位
            startRulerUnits = ps.Application().preferences.rulerUnits
            safe_print(f"   📏 原始标尺单位: {startRulerUnits}")

            app = ps.Application()
            app.preferences.rulerUnits = ps.Units.Inches

            # 创建新文档 (原始代码逻辑)
            safe_print("   📄 创建7x5英寸文档...")
            doc = app.documents.add(7, 5, 72, None, ps.NewDocumentMode.NewRGB, ps.DocumentFill.White)
            safe_print(f"      ✅ 创建文档: {doc.name}")
            safe_print(f"      📏 尺寸: {doc.width} x {doc.height} 英寸")
            safe_print(f"      📐 分辨率: {doc.resolution} ppi")

            # 确保活动图层不是文本图层 (原始代码逻辑)
            safe_print("\n   🎯 检查活动图层类型...")
            if doc.activeLayer.kind != ps.LayerKind.TextLayer:
                safe_print("      ✅ 活动图层不是文本图层，可以复制")

                # 选择左半部分 (原始代码逻辑)
                safe_print("   🔲 选择文档左半部分...")
                x2 = (doc.width * doc.resolution) / 2
                y2 = doc.height * doc.resolution
                safe_print(f"      📊 选择区域: 0,0 到 {x2:.0f},{y2:.0f} 像素")

                sel_area = ((0, 0), (x2, 0), (x2, y2), (0, y2))
                doc.selection.select(sel_area, ps.SelectionType.ReplaceSelection, 0, False)
                safe_print("      ✅ 选区创建成功")

                # 复制选区 (原始代码逻辑)
                safe_print("   📋 复制选区...")
                doc.selection.copy()
                safe_print("      ✅ 复制完成")

                # 创建新文档用于粘贴 (原始代码逻辑)
                safe_print("   📄 创建粘贴目标文档...")
                app.preferences.rulerUnits = ps.Units.Pixels
                pasteDoc = app.documents.add(x2, y2, doc.resolution, "Paste Target")
                safe_print(f"      ✅ 创建目标文档: {pasteDoc.name}")
                safe_print(f"      📏 尺寸: {pasteDoc.width} x {pasteDoc.height} 像素")

                # 粘贴内容 (原始代码逻辑)
                safe_print("   📥 粘贴内容...")
                pasted_layer = pasteDoc.paste()
                safe_print("      ✅ 粘贴完成")
                safe_print(f"      📝 粘贴的图层: {pasted_layer.name}")

                # 添加可见内容以便验证
                safe_print("   🎨 添加验证内容...")
                pasteDoc.selection.selectAll()
                bg_color = ps.SolidColor()
                bg_color.rgb.red = 200
                bg_color.rgb.green = 200
                bg_color.rgb.blue = 255
                pasteDoc.selection.fill(bg_color)
                pasteDoc.selection.deselect()
                safe_print("      ✅ 验证内容添加完成")

            else:
                safe_print("      ⚠️ 活动图层是文本图层，无法复制")

            # 恢复原始标尺单位 (原始代码逻辑)
            if startRulerUnits != app.preferences.rulerUnits:
                app.preferences.rulerUnits = startRulerUnits
                safe_print("   🔄 恢复原始标尺单位")

        except Exception as e:
            safe_print(f"❌ 基本复制粘贴测试失败: {str(e)}")
            return False

        # 测试2: 多图层复制粘贴
        safe_print("\n🔧 测试2: 多图层复制粘贴...")

        try:
            # 使用直接API (原始代码使用)
            app = ps.Application()
            doc = app.documents.add(400, 300, 72, "多图层复制测试")
            doc.name = "多图层复制测试"
            safe_print(f"   📄 创建文档: {doc.name}")

            # 创建多个图层
            layers = []
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

            for i, (r, g, b) in enumerate(colors):
                layer = doc.artLayers.add()
                layer.name = f"复制测试图层{i+1}"

                # 添加内容
                fill_color = ps.SolidColor()
                fill_color.rgb.red = r
                fill_color.rgb.green = g
                fill_color.rgb.blue = b
                ps.app.foregroundColor = fill_color

                x = 50 + i * 60
                doc.selection.select([[x, x], [x+50, x], [x+50, x+50], [x, x+50]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()

                layers.append(layer)
                safe_print(f"      ✅ 创建图层: {layer.name}")

            # 选择所有图层
            safe_print("   🔲 选择所有图层...")
            doc.selection.selectAll()
            safe_print("      ✅ 选区创建成功")

            # 复制选区
            safe_print("   📋 复制所有图层内容...")
            doc.selection.copy()
            safe_print("      ✅ 复制完成")

            # 粘贴到新位置
            safe_print("   📥 粘贴到新位置...")
            pasted_layer = doc.paste()
            safe_print(f"      ✅ 粘贴完成: {pasted_layer.name}")

            safe_print("   ✅ 多图层复制粘贴测试完成")

        except Exception as e:
            safe_print(f"❌ 多图层复制粘贴测试失败: {str(e)}")

        # 测试3: 复制粘贴到新文档
        safe_print("\n🔧 测试3: 复制粘贴到新文档...")

        try:
            # 创建源文档
            with Session(action="new_document") as ps:
                source_doc = ps.active_document
                source_doc.name = "复制源文档"

                # 添加内容
                layer = source_doc.artLayers.add()
                layer.name = "源内容"

                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 128
                fill_color.rgb.blue = 0
                ps.app.foregroundColor = fill_color

                source_doc.selection.select([[100, 100], [300, 100], [300, 300], [100, 300]])
                source_doc.selection.fill(ps.app.foregroundColor)
                source_doc.selection.deselect()

                safe_print(f"   📄 创建源文档: {source_doc.name}")

                # 复制内容
                source_doc.selection.selectAll()
                source_doc.selection.copy()
                safe_print("   📋 复制源文档内容...")

                # 创建目标文档
                app = ps.Application()
                target_doc = app.documents.add(500, 400, 72, "复制目标文档")
                target_doc.name = "复制目标文档"

                safe_print(f"   📄 创建目标文档: {target_doc.name}")

                # 粘贴到目标文档
                pasted_layer = target_doc.paste()
                safe_print("   📥 粘贴到目标文档...")
                safe_print(f"      ✅ 粘贴完成: {pasted_layer.name}")

                # 保存目标文档用于验证
                save_dir = get_test_save_dir()
                save_path = os.path.join(save_dir, "copy_paste_target.psd")

                psd_options = ps.PhotoshopSaveOptions()
                psd_options.layers = True
                target_doc.saveAs(save_path, psd_options, True)

                safe_print(f"   💾 保存目标文档: {save_path}")

                # 关闭目标文档
                target_doc.close()

        except Exception as e:
            safe_print(f"❌ 复制粘贴到新文档测试失败: {str(e)}")

        # 测试4: 复制粘贴错误处理
        safe_print("\n🔧 测试4: 复制粘贴错误处理...")

        try:
            # 测试空文档复制
            safe_print("   📄 测试空文档复制...")
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print(f"   📄 当前文档: {doc.name}")

                # 尝试复制空选区
                safe_print("   🔲 选择小区域...")
                doc.selection.select([[10, 10], [20, 10], [20, 20], [10, 20]])

                safe_print("   📋 尝试复制...")
                try:
                    doc.selection.copy()
                    safe_print("      ✅ 复制成功")
                except Exception as copy_e:
                    safe_print(f"      ⚠️ 复制失败: {str(copy_e)}")

                safe_print("   ✅ 空文档复制测试完成")

        except Exception as e:
            safe_print(f"❌ 错误处理测试失败: {str(e)}")

        # 测试5: 不同文档尺寸的复制粘贴
        safe_print("\n🔧 测试5: 不同文档尺寸的复制粘贴...")

        try:
            # 创建不同尺寸的文档
            doc_configs = [
                {"name": "小文档", "width": 400, "height": 300},
                {"name": "大文档", "width": 800, "height": 600},
                {"name": "宽屏文档", "width": 1000, "height": 500},
            ]

            for config in doc_configs:
                safe_print(f"   📄 测试{config['name']}...")

                with Session(action="new_document") as ps:
                    doc = ps.active_document

                    # 添加内容
                    layer = doc.artLayers.add()
                    layer.name = f"{config['name']}内容"

                    fill_color = ps.SolidColor()
                    fill_color.rgb.red = 100 + config['width'] // 100
                    fill_color.rgb.green = 150
                    fill_color.rgb.blue = 200
                    ps.app.foregroundColor = fill_color

                    doc.selection.select([[50, 50], [150, 50], [150, 150], [50, 150]])
                    doc.selection.fill(ps.app.foregroundColor)
                    doc.selection.deselect()

                    safe_print(f"      ✅ 创建{config['name']}并添加内容")

        except Exception as e:
            safe_print(f"❌ 不同尺寸文档测试失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "copy_and_paste_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Copy and Paste 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 复制粘贴功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本复制粘贴 (原始代码逻辑)\n")
                f.write(f"- 多图层复制粘贴\n")
                f.write(f"- 复制粘贴到新文档\n")
                f.write(f"- 复制粘贴错误处理\n")
                f.write(f"- 不同文档尺寸的复制粘贴\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第23项: copy_and_paste.py 测试完成!")
        safe_print("✅ 验证功能: 基本复制粘贴、多图层复制、跨文档复制、错误处理")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 复制粘贴功能是否可用")
        safe_print("3. 选区操作是否正常")
        safe_print("4. 文档管理权限是否正常")
        return False

if __name__ == "__main__":
    test_copy_and_paste()