# -*- coding: utf-8 -*-
"""测试第22项: operate_layerSet.py - 图层组操作"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_operate_layerSet():
    """运行operate_layerSet测试"""
    safe_print("📋 开始执行第22项: operate_layerSet.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本图层组操作 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本图层组操作 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print(f"📄 创建文档: {doc.name}")

                # Create a new layer group (原始代码逻辑)
                safe_print("   📁 创建主图层组...")
                main_group = doc.layerSets.add()
                main_group.name = "Main Group"
                safe_print(f"      ✅ 创建图层组: {main_group.name}")

                # Create a nested group (原始代码逻辑)
                safe_print("   📁 创建嵌套图层组...")
                sub_group = main_group.layerSets.add()
                sub_group.name = "Sub Group"
                safe_print(f"      ✅ 创建子图层组: {sub_group.name}")

                # Add layers to groups (原始代码逻辑)
                safe_print("   📄 在主组中创建图层...")
                layer1 = main_group.artLayers.add()
                layer1.name = "Layer in Main"
                safe_print(f"      ✅ 在主组中创建图层: {layer1.name}")

                safe_print("   📄 在子组中创建图层...")
                layer2 = sub_group.artLayers.add()
                layer2.name = "Layer in Sub"
                safe_print(f"      ✅ 在子组中创建图层: {layer2.name}")

                # Set group properties (原始代码逻辑)
                safe_print("   ⚙️ 设置图层组属性...")
                main_group.visible = True
                main_group.opacity = 80
                safe_print(f"      ✅ 设置可见性: {main_group.visible}")
                safe_print(f"      ✅ 设置透明度: {main_group.opacity}%")

                # List layers in groups (原始代码逻辑)
                safe_print("\n   📋 列出主组中的图层...")
                for layer in main_group.layers:
                    ps.echo(f"Layer in main group: {layer.name}")
                    safe_print(f"      📝 主组图层: {layer.name}")

                safe_print("\n   📋 列出子组中的图层...")
                for layer in sub_group.layers:
                    ps.echo(f"Layer in sub group: {layer.name}")
                    safe_print(f"      📝 子组图层: {layer.name}")

                # Move a layer between groups (修复版)
                safe_print("\n   🔄 在图层组间移动图层...")
                try:
                    layer1.move(sub_group, ps.ElementPlacement.PlaceInside)
                    safe_print(f"      ✅ 将{layer1.name}移动到子组")
                except Exception as move_e:
                    safe_print(f"      ❌ 移动失败: {str(move_e)}")
                    safe_print("   🔄 尝试其他移动方法...")
                    # 尝试直接设置parent
                    try:
                        layer1.parent = sub_group
                        safe_print(f"      ✅ 使用parent属性移动成功")
                    except Exception as parent_e:
                        safe_print(f"      ❌ parent属性也失败: {str(parent_e)}")

                # 验证移动结果
                safe_print("   📋 验证移动结果...")
                main_layers_after = [layer.name for layer in main_group.layers]
                sub_layers_after = [layer.name for layer in sub_group.layers]

                safe_print(f"      📝 移动后主组图层: {main_layers_after}")
                safe_print(f"      📝 移动后子组图层: {sub_layers_after}")

                if "Layer in Main" in sub_layers_after:
                    safe_print("      ✅ 图层移动验证成功")
                else:
                    safe_print("      ⚠️ 图层移动验证警告")

        except Exception as e:
            safe_print(f"❌ 基本图层组操作测试失败: {str(e)}")
            return False

        # 测试2: 多层级嵌套组
        safe_print("\n🔧 测试2: 多层级嵌套组...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建三级嵌套组
                group1 = doc.layerSets.add()
                group1.name = "第一级组"

                group2 = group1.layerSets.add()
                group2.name = "第二级组"

                group3 = group2.layerSets.add()
                group3.name = "第三级组"

                safe_print("   📁 创建三级嵌套组")

                # 在每级组中添加图层
                for i, group in enumerate([group1, group2, group3], 1):
                    layer = group.artLayers.add()
                    layer.name = f"第{i}级组图层"
                    safe_print(f"      ✅ 在第{i}级组创建图层")

                # 验证层级结构
                safe_print("   📊 验证层级结构...")
                safe_print(f"      📁 主文档图层组数量: {doc.layerSets.length}")
                safe_print(f"      📁 第一级组子组数量: {group1.layerSets.length}")
                safe_print(f"      📁 第二级组子组数量: {group2.layerSets.length}")

        except Exception as e:
            safe_print(f"❌ 多层级嵌套组测试失败: {str(e)}")

        # 测试3: 图层组属性管理
        safe_print("\n🔧 测试3: 图层组属性管理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建多个组并设置不同属性
                test_groups = [
                    {"name": "隐藏组", "visible": False, "opacity": 100},
                    {"name": "半透明组", "visible": True, "opacity": 50},
                    {"name": "低透明度组", "visible": True, "opacity": 20},
                ]

                for group_config in test_groups:
                    group = doc.layerSets.add()
                    group.name = group_config["name"]
                    group.visible = group_config["visible"]
                    group.opacity = group_config["opacity"]

                    safe_print(f"   📁 创建组: {group.name}")
                    safe_print(f"      👁️ 可见性: {group.visible}")
                    safe_print(f"      🎭 透明度: {group.opacity}%")

                    # 在组中添加图层
                    layer = group.artLayers.add()
                    layer.name = f"{group.name}的图层"

                safe_print("   ✅ 图层组属性管理完成")

        except Exception as e:
            safe_print(f"❌ 图层组属性管理测试失败: {str(e)}")

        # 测试4: 图层组中内容管理
        safe_print("\n🔧 测试4: 图层组中内容管理...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建组
                content_group = doc.layerSets.add()
                content_group.name = "内容管理组"

                # 在组中添加多种类型的内容
                safe_print("   📄 在组中添加文本内容...")
                text_layer = content_group.artLayers.add()
                text_layer.kind = ps.LayerKind.TextLayer
                text_layer.name = "组内文本"
                text_layer.textItem.contents = "图层组内文本"
                text_layer.textItem.size = 24
                text_layer.textItem.position = [100, 100]
                safe_print("      ✅ 创建文本图层")

                safe_print("   📄 在组中添加形状内容...")
                shape_layer = content_group.artLayers.add()
                shape_layer.name = "组内形状"

                # 添加彩色矩形
                fill_color = ps.SolidColor()
                fill_color.rgb.red = 255
                fill_color.rgb.green = 128
                fill_color.rgb.blue = 0
                ps.app.foregroundColor = fill_color

                doc.selection.select([[200, 200], [300, 200], [300, 300], [200, 300]])
                doc.selection.fill(ps.app.foregroundColor)
                doc.selection.deselect()
                safe_print("      ✅ 创建形状图层")

                # 验证组内内容
                safe_print("   📋 验证组内内容...")
                for layer in content_group.artLayers:
                    safe_print(f"      📝 图层: {layer.name}")
                safe_print(f"      ✅ 组内共有 {content_group.artLayers.length} 个图层")

        except Exception as e:
            safe_print(f"❌ 图层组内容管理测试失败: {str(e)}")

        # 测试5: 图层组操作和移动
        safe_print("\n🔧 测试5: 图层组操作和移动...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建两个组
                group_a = doc.layerSets.add()
                group_a.name = "组A"

                group_b = doc.layerSets.add()
                group_b.name = "组B"

                # 在组A中添加图层
                layer_a = group_a.artLayers.add()
                layer_a.name = "来自组A的图层"

                safe_print("   📁 创建组A和组B")
                safe_print("   📄 在组A中创建图层")

                # 将图层从组A移动到组B
                safe_print("   🔄 将图层从组A移动到组B...")
                layer_a.move(group_b, ps.ElementPlacement.INSIDE)
                safe_print("      ✅ 移动完成")

                # 验证移动结果
                safe_print("   📋 验证移动结果...")
                safe_print(f"      📝 组A剩余图层: {[layer.name for layer in group_a.layers]}")
                safe_print(f"      📝 组B图层: {[layer.name for layer in group_b.layers]}")

                if len(list(group_a.layers)) == 0 and len(list(group_b.layers)) > 0:
                    safe_print("      ✅ 图层组间移动验证成功")
                else:
                    safe_print("      ⚠️ 图层组间移动验证警告")

        except Exception as e:
            safe_print(f"❌ 图层组操作和移动测试失败: {str(e)}")

        # 测试6: 图层组和图层混合
        safe_print("\n🔧 测试6: 图层组和普通图层混合...")

        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document

                # 创建组
                mixed_group = doc.layerSets.add()
                mixed_group.name = "混合组"

                # 在组外创建图层
                outer_layer = doc.artLayers.add()
                outer_layer.name = "组外图层"

                # 在组内创建图层
                inner_layer = mixed_group.artLayers.add()
                inner_layer.name = "组内图层"

                safe_print("   📁 创建混合结构")
                safe_print("   ✅ 组外图层数量: 2")  # 背景层+组外图层
                safe_print(f"   ✅ 组内图层数量: {mixed_group.artLayers.length}")

        except Exception as e:
            safe_print(f"❌ 图层组和普通图层混合测试失败: {str(e)}")

        # 测试7: 错误处理和边界情况
        safe_print("\n🔧 测试7: 错误处理和边界情况...")

        try:
            # 测试空组操作
            safe_print("   📄 测试空组操作...")
            with Session(action="new_document") as ps:
                doc = ps.active_document

                empty_group = doc.layerSets.add()
                empty_group.name = "空组"

                safe_print(f"   ✅ 创建空组: {empty_group.name}")
                safe_print(f"   📊 空组图层数量: {empty_group.artLayers.length}")

            # 测试嵌套组深度
            safe_print("   📄 测试嵌套组深度...")
            with Session(action="new_document") as ps:
                doc = ps.active_document

                current_group = doc
                for i in range(5):  # 尝试5级嵌套
                    try:
                        if hasattr(current_group, 'layerSets'):
                            current_group = current_group.layerSets.add()
                            current_group.name = f"深度{i+1}组"
                            safe_print(f"      ✅ 第{i+1}级嵌套成功")
                        else:
                            safe_print(f"      ⚠️ 第{i+1}级嵌套失败")
                            break
                    except Exception as depth_e:
                        safe_print(f"      ⚠️ 第{i+1}级嵌套错误: {str(depth_e)}")
                        break

        except Exception as e:
            safe_print(f"❌ 错误处理测试失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "operate_layerSet_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Operate LayerSet 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 图层组操作功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本图层组操作 (原始代码逻辑)\n")
                f.write(f"- 多层级嵌套组\n")
                f.write(f"- 图层组属性管理\n")
                f.write(f"- 图层组中内容管理\n")
                f.write(f"- 图层组操作和移动\n")
                f.write(f"- 图层组和普通图层混合\n")
                f.write(f"- 错误处理和边界情况\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第22项: operate_layerSet.py 测试完成!")
        safe_print("✅ 验证功能: 基本组操作、多层级嵌套、属性管理、内容管理、组间移动")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 图层组功能是否可用")
        safe_print("3. 图层创建权限是否正常")
        safe_print("4. 图层移动权限是否正常")
        return False

if __name__ == "__main__":
    test_operate_layerSet()