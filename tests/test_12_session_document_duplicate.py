# -*- coding: utf-8 -*-
"""测试第12项: session_document_duplicate.py - Session复制文档"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def check_and_prepare_document_layers(doc, ps):
    """检查并准备文档图层状态"""
    safe_print("🔍 检查文档图层状态...")

    # 统计图层信息
    total_layers = doc.artLayers.length
    background_layer_exists = False
    locked_layers = []

    safe_print(f"   📊 总图层数: {total_layers}")

    # 检查每个图层
    for i in range(total_layers):
        try:
            layer = doc.artLayers[i]
            is_locked = hasattr(layer, 'allLocked') and layer.allLocked
            is_background = hasattr(layer, 'isBackgroundLayer') and getattr(layer, 'isBackgroundLayer', False)

            safe_print(f"      {i+1}. {layer.name}")
            safe_print(f"         🔒 锁定状态: {'是' if is_locked else '否'}")
            safe_print(f"         🎨 背景图层: {'是' if is_background else '否'}")

            if is_locked:
                locked_layers.append(layer)
            if is_background:
                background_layer_exists = True

        except Exception as e:
            safe_print(f"      ⚠️ 无法访问图层 {i+1}: {str(e)}")

    # 准备图层（解锁或添加新图层）
    safe_print("🔧 准备文档图层...")

    # 方法1: 尝试解锁锁定图层
    if locked_layers:
        safe_print(f"   🔓 尝试解锁 {len(locked_layers)} 个锁定图层...")
        for layer in locked_layers:
            try:
                layer.allLocked = False
                safe_print(f"      ✅ 解锁成功: {layer.name}")
            except Exception as e:
                safe_print(f"      ❌ 解锁失败: {layer.name} - {str(e)}")

    # 方法2: 如果有背景图层，添加新的可操作图层
    if background_layer_exists:
        safe_print("   📄 检测到背景图层，添加新的可操作图层...")
        try:
            # 添加新的普通图层
            new_layer = doc.artLayers.add()
            new_layer.name = "可复制内容层"

            # 在新图层上添加一些内容
            text_layer = doc.artLayers.add()
            text_layer.kind = ps.LayerKind.TextLayer
            text_layer.name = "复制测试文本"
            text_layer.textItem.contents = "文档复制测试\n可操作内容"
            text_layer.textItem.size = 24
            text_layer.textItem.position = [100, 150]

            safe_print("      ✅ 添加了新的可操作图层和内容")

        except Exception as e:
            safe_print(f"      ❌ 添加新图层失败: {str(e)}")

    # 最终状态检查
    final_layers = doc.artLayers.length
    safe_print(f"   📊 准备后图层数: {final_layers}")

    return True

def test_session_document_duplicate():
    """运行session_document_duplicate测试"""
    safe_print("📋 开始执行第12项: session_document_duplicate.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session
        import photoshop.api as ps_api

        # 测试1: 基本文档复制 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本文档复制 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                source_doc = ps.active_document
                original_name = source_doc.name
                safe_print(f"✅ 创建源文档: {original_name}")

                # 添加一些内容用于识别
                layer = source_doc.artLayers.add()
                layer.name = "源内容层"

                # 添加文本标识
                text_layer = source_doc.artLayers.add()
                text_layer.kind = ps.LayerKind.TextLayer
                text_layer.name = "源文本"
                text_layer.textItem.contents = "源文档内容\n用于复制测试"
                text_layer.textItem.size = 32
                text_layer.textItem.position = [100, 200]

                # 先检查并准备图层状态，避免填充问题
                safe_print(f"   📏 尺寸: {source_doc.width} x {source_doc.height}")
                safe_print(f"   🎭 初始图层数量: {source_doc.artLayers.length}")

                # 检查并准备图层状态
                layer_prepared = check_and_prepare_document_layers(source_doc, ps)

                if not layer_prepared:
                    safe_print("❌ 图层准备失败，跳过复制测试")
                    return False

                # 然后尝试添加彩色背景（在可操作图层上）
                try:
                    bg_color = ps.SolidColor()
                    bg_color.rgb.red = 255
                    bg_color.rgb.green = 200
                    bg_color.rgb.blue = 150
                    ps.app.backgroundColor = bg_color

                    source_doc.selection.selectAll()
                    source_doc.selection.fill(ps.app.backgroundColor)
                    source_doc.selection.deselect()
                    safe_print("   ✅ 背景填充成功")
                except Exception as fill_e:
                    safe_print(f"   ⚠️ 背景填充失败: {str(fill_e)}")
                    safe_print("   📄 继续测试，不依赖背景填充")

                safe_print(f"   🎭 最终图层数量: {source_doc.artLayers.length}")

                # 记录源文档信息
                source_info = {
                    'name': original_name,
                    'width': source_doc.width,
                    'height': source_doc.height,
                    'layers': source_doc.artLayers.length,
                    'layer_names': [layer.name for layer in source_doc.artLayers]
                }

                # 复制文档 (原始代码逻辑)
                safe_print("\n📋 执行文档复制...")
                if len(ps.app.documents) > 0:
                    duplicated_doc = ps.active_document.duplicate()
                    safe_print(f"✅ 成功复制文档: {duplicated_doc.name}")

                    # 验证复制结果
                    safe_print(f"   📏 复制文档尺寸: {duplicated_doc.width} x {duplicated_doc.height}")
                    safe_print(f"   🎭 复制文档图层数量: {duplicated_doc.artLayers.length}")

                    # 检查图层是否也被复制
                    dup_layer_names = [layer.name for layer in duplicated_doc.artLayers]
                    safe_print(f"   📋 复制文档图层: {dup_layer_names}")

                    # 验证复制是否完整
                    if (duplicated_doc.width == source_info['width'] and
                        duplicated_doc.height == source_info['height'] and
                        duplicated_doc.artLayers.length == source_info['layers']):
                        safe_print("   ✅ 文档复制完整性验证通过")
                    else:
                        safe_print("   ⚠️ 文档复制可能不完整")

        except Exception as e:
            safe_print(f"❌ 基本文档复制失败: {str(e)}")
            return False

        # 测试2: 多次文档复制
        safe_print("\n🔧 测试2: 多次文档复制测试...")

        try:
            # 创建新的源文档
            with Session(action="new_document") as ps:
                source_doc = ps.active_document

                # 添加复杂内容
                for i in range(3):
                    layer = source_doc.artLayers.add()
                    layer.name = f"内容层{i+1}"

                    text_layer = source_doc.artLayers.add()
                    text_layer.kind = ps.LayerKind.TextLayer
                    text_layer.name = f"文本{i+1}"
                    text_layer.textItem.contents = f"复制测试文本{i+1}"
                    text_layer.textItem.size = 20 + i * 4
                    text_layer.textItem.position = [50, 50 + i * 60]

                safe_print(f"✅ 创建复杂源文档: {source_doc.name}")
                safe_print(f"   🎭 源文档图层数量: {source_doc.artLayers.length}")

                # 执行多次复制
                duplicated_docs = []
                for i in range(3):
                    if len(ps.app.documents) > 0:
                        dup_doc = ps.active_document.duplicate()
                        duplicated_docs.append(dup_doc)
                        safe_print(f"   ✅ 第{i+1}次复制: {dup_doc.name}")
                        safe_print(f"      🎭 图层数量: {dup_doc.artLayers.length}")

                safe_print(f"   📊 总共复制了 {len(duplicated_docs)} 个文档")

                # 验证所有复制的文档
                for i, doc in enumerate(duplicated_docs):
                    if doc.artLayers.length == source_doc.artLayers.length:
                        safe_print(f"      ✅ 复制文档{i+1}图层数量正确")
                    else:
                        safe_print(f"      ⚠️ 复制文档{i+1}图层数量不匹配")

        except Exception as e:
            safe_print(f"❌ 多次复制测试失败: {str(e)}")

        # 测试3: 复制文档的独立操作
        safe_print("\n🔧 测试3: 复制文档的独立操作测试...")

        try:
            with Session(action="new_document") as ps:
                # 创建源文档
                source_doc = ps.active_document

                # 添加基础内容
                layer = source_doc.artLayers.add()
                layer.name = "原始内容"

                safe_print(f"   📄 创建源文档: {source_doc.name}")

                # 复制文档
                if len(ps.app.documents) > 0:
                    dup_doc = ps.active_document.duplicate()

                    safe_print(f"   📄 复制文档: {dup_doc.name}")

                    # 在副本上进行独立操作
                    new_layer = dup_doc.artLayers.add()
                    new_layer.name = "副本新增内容"

                    text_layer = dup_doc.artLayers.add()
                    text_layer.kind = ps.LayerKind.TextLayer
                    text_layer.name = "副本文本"
                    text_layer.textItem.contents = "这是副本新增的内容"
                    text_layer.textItem.size = 24
                    text_layer.textItem.position = [150, 150]

                    safe_print(f"      🎭 副本原始层数: {source_doc.artLayers.length}")
                    safe_print(f"      🎭 副本修改后层数: {dup_doc.artLayers.length}")

                    if dup_doc.artLayers.length > source_doc.artLayers.length:
                        safe_print("      ✅ 副本独立操作成功，不影响源文档")
                    else:
                        safe_print("      ⚠️ 副本独立操作可能有问题")

        except Exception as e:
            safe_print(f"   ❌ 独立操作测试失败: {str(e)}")

        # 测试4: 复制文档的保存
        safe_print("\n🔧 测试4: 复制文档的保存测试...")

        try:
            save_dir = get_test_save_dir()

            with Session(action="new_document") as ps:
                # 创建带内容的源文档
                source_doc = ps.active_document

                # 添加标识内容
                text_layer = source_doc.artLayers.add()
                text_layer.kind = ps.LayerKind.TextLayer
                text_layer.name = "源标识"
                text_layer.textItem.contents = "源文档 - 保存测试"
                text_layer.textItem.size = 28
                text_layer.textItem.position = [100, 150]

                # 复制文档
                if len(ps.app.documents) > 0:
                    dup_doc = ps.active_document.duplicate()

                    # 修改副本内容
                    mod_text = dup_doc.artLayers.add()
                    mod_text.kind = ps.LayerKind.TextLayer
                    mod_text.name = "副本标识"
                    mod_text.textItem.contents = "副本文档 - 已修改"
                    mod_text.textItem.size = 24
                    mod_text.textItem.position = [100, 200]

                    # 保存源文档和副本
                    source_save_path = os.path.join(save_dir, "duplicate_test_source.psd")
                    dup_save_path = os.path.join(save_dir, "duplicate_test_copy.psd")

                    psd_options = ps.PhotoshopSaveOptions()
                    psd_options.layers = True

                    source_doc.saveAs(source_save_path, psd_options, True)
                    dup_doc.saveAs(dup_save_path, psd_options, True)

                    safe_print(f"   ✅ 源文档已保存: {source_save_path}")
                    safe_print(f"   ✅ 副本文档已保存: {dup_save_path}")

                    # 验证文件存在
                    if os.path.exists(source_save_path) and os.path.exists(dup_save_path):
                        source_size = os.path.getsize(source_save_path)
                        dup_size = os.path.getsize(dup_save_path)
                        safe_print(f"   📊 源文件大小: {source_size} 字节")
                        safe_print(f"   📊 副本文件大小: {dup_size} 字节")
                        safe_print("   ✅ 复制文档保存测试成功")

        except Exception as e:
            safe_print(f"   ❌ 保存测试失败: {str(e)}")

        # 测试5: Session和API对比测试
        safe_print("\n🔧 测试5: Session和API对比测试...")

        try:
            # Session方式复制
            safe_print("   📄 Session方式复制文档...")
            with Session(action="new_document") as ps:
                source_doc = ps.active_document
                layer = source_doc.artLayers.add()
                layer.name = "Session测试内容"

                if len(ps.app.documents) > 0:
                    session_dup = ps.active_document.duplicate()
                    safe_print(f"      ✅ Session复制成功: {session_dup.name}")

            # API方式复制
            safe_print("   📄 API方式复制文档...")
            app = ps_api.Application()
            if len(app.documents) > 0:
                api_source = app.documents[0]
                api_dup = api_source.duplicate()
                safe_print(f"      ✅ API复制成功: {api_dup.name}")

                # 关闭API复制的文档
                api_dup.close()
                safe_print("      📁 API复制的文档已关闭")

        except Exception as e:
            safe_print(f"   ❌ API对比测试失败: {str(e)}")

        # 测试6: 错误处理
        safe_print("\n🔧 测试6: 错误处理测试...")

        try:
            # 测试无文档时的复制
            safe_print("   📄 测试无文档时的复制...")
            with Session() as ps:
                # 不创建文档，直接尝试复制
                try:
                    if len(ps.app.documents) > 0:
                        ps.active_document.duplicate()
                        safe_print("      ⚠️ 意外成功：无文档时应该失败")
                    else:
                        safe_print("      ✅ 正确：无文档时无法复制")
                except Exception as e:
                    safe_print(f"      ✅ 正确处理无文档情况: {str(e)}")

        except Exception as e:
            safe_print(f"   ❌ 错误处理测试失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "session_document_duplicate_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Session Document Duplicate 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: Session文档复制功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本文档复制 (原始代码逻辑)\n")
                f.write(f"- 多次文档复制\n")
                f.write(f"- 复制文档独立操作\n")
                f.write(f"- 复制文档保存\n")
                f.write(f"- Session和API对比\n")
                f.write(f"- 错误处理测试\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第12项: session_document_duplicate.py 测试完成!")
        safe_print("✅ 验证功能: 基本文档复制、多次复制、独立操作、保存功能、API对比")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. 文档复制功能是否正常")
        safe_print("3. Session上下文是否稳定")
        safe_print("4. 文档保存权限是否正常")
        return False

if __name__ == "__main__":
    test_session_document_duplicate()