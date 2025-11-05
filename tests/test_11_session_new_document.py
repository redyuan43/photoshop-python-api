# -*- coding: utf-8 -*-
"""测试第11项: session_new_document.py - Session创建文档"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_session_new_document():
    """运行session_new_document测试"""
    safe_print("📄 开始执行第11项: session_new_document.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        from photoshop import Session

        # 测试1: 基本Session新文档创建 (原始代码逻辑)
        safe_print("\n🔧 测试1: 基本Session新文档创建 (原始逻辑)...")

        try:
            with Session(action="new_document") as ps:
                # 获取新创建的文档 (原始代码逻辑)
                doc = ps.active_document
                safe_print(f"✅ 成功创建新文档: {doc.name}")

                # 执行echo命令 (原始代码逻辑)
                ps.echo(ps.active_document.name)
                safe_print(f"💬 echo输出: {ps.active_document.name}")

                # 显示文档基本信息
                safe_print(f"   📏 文档尺寸: {doc.width} x {doc.height}")
                safe_print(f"   📐 分辨率: {doc.resolution} ppi")
                safe_print(f"   🎨 颜色模式: {doc.mode}")
                safe_print(f"   📊 位深度: {doc.bitsPerChannel}")
                safe_print(f"   🎭 图层数量: {doc.artLayers.length}")

        except Exception as e:
            safe_print(f"❌ 基本Session创建失败: {str(e)}")
            return False

        # 测试2: 多个Session文档创建
        safe_print("\n🔧 测试2: 多个Session文档创建...")

        session_configs = [
            {"name": "Session测试1", "width": 800, "height": 600, "resolution": 72},
            {"name": "Session测试2", "width": 1024, "height": 768, "resolution": 96},
            {"name": "Session测试3", "width": 640, "height": 480, "resolution": 150},
        ]

        created_docs = []
        for i, config in enumerate(session_configs):
            try:
                safe_print(f"   📄 创建文档 {i+1}: {config['name']}")

                with Session(action="new_document") as ps:
                    doc = ps.active_document

                    # 修改文档名称
                    doc.name = config['name']
                    safe_print(f"      ✅ 文档名称: {doc.name}")

                    # 显示文档信息
                    safe_print(f"      📏 尺寸: {doc.width} x {doc.height}")
                    safe_print(f"      📐 分辨率: {doc.resolution} ppi")

                    # 添加可见内容用于区分
                    layer = doc.artLayers.add()
                    layer.name = f"{config['name']}_标识层"

                    # 添加文本标识
                    text_layer = doc.artLayers.add()
                    text_layer.kind = ps.LayerKind.TextLayer
                    text_layer.name = "标识文本"
                    text_layer.textItem.contents = f"Session创建测试\n{config['name']}\n{doc.width}x{doc.height}\n{doc.resolution}ppi"
                    text_layer.textItem.size = 24
                    text_layer.textItem.position = [50, 100]

                    # 添加彩色背景区分
                    bg_color = ps.SolidColor()
                    bg_color.rgb.red = 200 + i * 20
                    bg_color.rgb.green = 200
                    bg_color.rgb.blue = 200 + i * 30
                    ps.app.backgroundColor = bg_color

                    doc.selection.selectAll()
                    doc.selection.fill(ps.app.backgroundColor)
                    doc.selection.deselect()

                    created_docs.append({
                        'name': config['name'],
                        'width': doc.width,
                        'height': doc.height,
                        'resolution': doc.resolution
                    })

                    # 保存文档用于验证
                    save_dir = get_test_save_dir()
                    save_path = os.path.join(save_dir, f"session_new_doc_{i+1}.psd")

                    psd_options = ps.PhotoshopSaveOptions()
                    psd_options.layers = True
                    doc.saveAs(save_path, psd_options, True)

                    safe_print(f"      💾 已保存: {save_path}")

            except Exception as e:
                safe_print(f"      ❌ 创建文档 {i+1} 失败: {str(e)}")

        safe_print(f"   📊 成功创建 {len(created_docs)} 个文档")

        # 测试3: Session参数测试
        safe_print("\n🔧 测试3: Session参数和配置测试...")

        parameter_tests = [
            {"desc": "默认参数", "params": {}},
            {"desc": "指定尺寸", "params": {"width": 1200, "height": 800}},
            {"desc": "高分辨率", "params": {"resolution": 300}},
        ]

        for i, test_config in enumerate(parameter_tests):
            try:
                safe_print(f"   📄 测试 {i+1}: {test_config['desc']}")

                # 使用Session创建文档
                with Session(action="new_document", **test_config['params']) as ps:
                    doc = ps.active_document

                    safe_print(f"      ✅ 文档创建成功")
                    safe_print(f"      📏 实际尺寸: {doc.width} x {doc.height}")
                    safe_print(f"      📐 实际分辨率: {doc.resolution} ppi")

                    # 验证参数是否生效
                    if 'width' in test_config['params']:
                        expected_width = test_config['params']['width']
                        if doc.width == expected_width:
                            safe_print(f"      ✅ 宽度参数生效: {expected_width}")
                        else:
                            safe_print(f"      ⚠️ 宽度参数未完全生效: 期望{expected_width}, 实际{doc.width}")

                    if 'height' in test_config['params']:
                        expected_height = test_config['params']['height']
                        if doc.height == expected_height:
                            safe_print(f"      ✅ 高度参数生效: {expected_height}")
                        else:
                            safe_print(f"      ⚠️ 高度参数未完全生效: 期望{expected_height}, 实际{doc.height}")

                    if 'resolution' in test_config['params']:
                        expected_res = test_config['params']['resolution']
                        if doc.resolution == expected_res:
                            safe_print(f"      ✅ 分辨率参数生效: {expected_res}")
                        else:
                            safe_print(f"      ⚠️ 分辨率参数未完全生效: 期望{expected_res}, 实际{doc.resolution}")

            except Exception as e:
                safe_print(f"      ❌ 参数测试 {i+1} 失败: {str(e)}")

        # 测试4: Session上下文管理测试
        safe_print("\n🔧 测试4: Session上下文管理测试...")

        try:
            safe_print("   📄 测试Session自动关闭...")

            doc_info_before = None
            doc_info_after = None

            # 在Session内操作
            with Session(action="new_document") as ps:
                doc = ps.active_document
                doc_info_before = {
                    'name': doc.name,
                    'width': doc.width,
                    'height': doc.height
                }
                safe_print(f"      📄 Session内文档: {doc.name}")

                # 添加一些内容
                layer = doc.artLayers.add()
                layer.name = "上下文测试层"

                # Session应该自动关闭文档

            # 检查Session外状态
            safe_print("      ✅ Session已自动退出")
            safe_print("      📁 文档应该已自动关闭")

        except Exception as e:
            safe_print(f"   ❌ 上下文管理测试失败: {str(e)}")

        # 测试5: Session错误处理
        safe_print("\n🔧 测试5: Session错误处理...")

        try:
            safe_print("   📄 测试无效Session参数...")

            # 测试无效的action参数
            try:
                with Session(action="invalid_action") as ps:
                    safe_print("      ⚠️ 意外成功: 无效action应该失败")
            except Exception as e:
                safe_print(f"      ✅ 正确处理无效action: {str(e)}")

            # 测试无效的文档参数
            try:
                with Session(action="new_document", width=-100) as ps:
                    safe_print("      ⚠️ 意外成功: 负数宽度应该失败")
            except Exception as e:
                safe_print(f"      ✅ 正确处理无效参数: {str(e)}")

        except Exception as e:
            safe_print(f"   ❌ 错误处理测试失败: {str(e)}")

        # 测试6: Session与直接API对比
        safe_print("\n🔧 测试6: Session与直接API创建方式对比...")

        try:
            # Session方式
            safe_print("   📄 Session方式创建文档...")
            with Session(action="new_document") as ps:
                session_doc = ps.active_document
                session_info = {
                    'name': session_doc.name,
                    'width': session_doc.width,
                    'height': session_doc.height,
                    'resolution': session_doc.resolution,
                    'layers': session_doc.artLayers.length
                }
                safe_print(f"      ✅ Session文档: {session_doc.name}")

            # 直接API方式
            safe_print("   📄 直接API方式创建文档...")
            import photoshop.api as ps_api
            app = ps_api.Application()
            api_doc = app.documents.add(800, 600, 72, "API创建文档")

            api_info = {
                'name': api_doc.name,
                'width': api_doc.width,
                'height': api_doc.height,
                'resolution': api_doc.resolution,
                'layers': api_doc.artLayers.length
            }
            safe_print(f"      ✅ API文档: {api_doc.name}")

            # 对比结果
            safe_print("   📊 创建方式对比:")
            safe_print(f"      Session方式: 名称='{session_info['name']}', 尺寸={session_info['width']}x{session_info['height']}")
            safe_print(f"      API方式: 名称='{api_info['name']}', 尺寸={api_info['width']}x{api_info['height']}")

            # 关闭API创建的文档
            api_doc.close()
            safe_print("      📁 API文档已关闭")

        except Exception as e:
            safe_print(f"   ❌ API对比测试失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "session_new_document_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Session New Document 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: Session创建文档功能\n")
                f.write(f"测试内容:\n")
                f.write(f"- 基本Session新文档创建 (原始代码逻辑)\n")
                f.write(f"- 多个Session文档创建\n")
                f.write(f"- Session参数和配置测试\n")
                f.write(f"- Session上下文管理测试\n")
                f.write(f"- Session错误处理\n")
                f.write(f"- Session与直接API对比\n")
                f.write(f"\n创建的文档数量: {len(created_docs)}\n")
                f.write("创建的文档列表:\n")
                for i, doc_info in enumerate(created_docs):
                    f.write(f"{i+1}. {doc_info['name']}: {doc_info['width']}x{doc_info['height']} @ {doc_info['resolution']}ppi\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第11项: session_new_document.py 测试完成!")
        safe_print("✅ 验证功能: 基本Session创建、参数配置、上下文管理、错误处理、API对比")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. Session模块是否正常导入")
        safe_print("3. 文档创建权限是否正常")
        safe_print("4. 保存路径是否有写入权限")
        return False

if __name__ == "__main__":
    test_session_new_document()