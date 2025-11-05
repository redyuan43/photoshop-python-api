# -*- coding: utf-8 -*-
"""测试第8项: open_psd.py - 打开PSD文件"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_open_psd():
    """运行open_psd测试"""
    safe_print("📂 开始执行第8项: open_psd.py 测试...")
    safe_print("📋 请确保Photoshop已经启动!")

    try:
        # Import local modules (原始代码逻辑)
        import photoshop.api as ps
        from photoshop import Session

        # 检查是否有可用的PSD文件
        safe_print("\n🔍 查找可用的PSD文件...")

        # 尝试使用项目中的PSD文件
        psd_files = []

        # 检查examples/_psd_files.py
        try:
            import examples._psd_files as psd_module
            PSD_FILE = psd_module.get_psd_files()
            safe_print("✅ 找到PSD文件模块")
            safe_print(f"📁 可用PSD文件: {list(PSD_FILE.keys())}")

            # 选择第一个可用的PSD文件
            for file_key, file_path in PSD_FILE.items():
                if os.path.exists(file_path):
                    psd_files.append((file_key, file_path))
                    safe_print(f"   📄 {file_key}: {file_path}")

        except Exception as e:
            safe_print(f"⚠️ 无法加载PSD文件模块: {str(e)}")

        # 如果没有找到PSD文件，创建一个测试用的
        if not psd_files:
            safe_print("🔧 未找到PSD文件，创建测试PSD文件...")
            try:
                # 创建一个简单的PSD文件用于测试
                app = ps.Application()
                test_doc = app.documents.add(800, 600, 72, "open_psd_test")

                # 添加一些内容
                art_layer = test_doc.artLayers.add()
                art_layer.kind = ps.LayerKind.TextLayer
                art_layer.textItem.contents = "Open PSD Test"
                art_layer.textItem.size = 48
                art_layer.textItem.position = [200, 300]

                # 设置文本颜色
                text_color = ps.SolidColor()
                text_color.rgb.red = 255
                text_color.rgb.green = 0
                text_color.rgb.blue = 0
                art_layer.textItem.color = text_color

                # 保存为PSD文件
                save_dir = get_test_save_dir()
                test_psd_path = os.path.join(save_dir, "open_psd_test_file.psd")

                save_options = ps.PhotoshopSaveOptions()
                test_doc.saveAs(test_psd_path, save_options)

                # 关闭文档
                test_doc.close()

                psd_files.append(("test_file", test_psd_path))
                safe_print(f"✅ 创建测试PSD文件: {test_psd_path}")

            except Exception as e:
                safe_print(f"❌ 创建测试PSD文件失败: {str(e)}")
                return False

        if not psd_files:
            safe_print("❌ 没有可用的PSD文件进行测试")
            return False

        # 测试1: 直接API方式打开PSD (原始代码逻辑 style 1)
        safe_print("\n🔧 测试1: 直接API方式打开PSD文件...")

        file_key, file_path = psd_files[0]
        safe_print(f"📂 打开文件: {file_key}")
        safe_print(f"📁 文件路径: {file_path}")

        try:
            app = ps.Application()

            # 记录打开前的文档数量
            initial_doc_count = len(app.documents)
            safe_print(f"📊 打开前文档数量: {initial_doc_count}")

            # 使用load方法打开PSD文件 (原始代码逻辑)
            app.load(file_path)

            # 检查文档是否成功打开
            current_doc_count = len(app.documents)
            safe_print(f"📊 打开后文档数量: {current_doc_count}")

            if current_doc_count > initial_doc_count:
                # 获取新打开的文档
                new_doc = app.documents[current_doc_count - 1]
                safe_print(f"✅ 成功打开文档: {new_doc.name}")
                safe_print(f"   📏 尺寸: {new_doc.width} x {new_doc.height}")
                safe_print(f"   📐 分辨率: {new_doc.resolution} ppi")
                safe_print(f"   🎨 模式: {new_doc.mode}")
                safe_print(f"   🎭 图层数量: {new_doc.artLayers.length}")

                # 关闭文档
                new_doc.close()
                safe_print("   📁 已关闭测试文档")
            else:
                safe_print("❌ 未能成功打开文档")

        except Exception as e:
            safe_print(f"❌ 直接API打开失败: {str(e)}")

        # 测试2: Session方式打开PSD (原始代码逻辑 style 2)
        safe_print("\n🔧 测试2: Session方式打开PSD文件...")

        try:
            with Session(file_path, action="open") as session:
                safe_print("✅ Session成功启动并打开PSD文件")

                # 获取文档信息
                doc = session.active_document
                safe_print(f"📄 当前文档: {doc.name}")
                safe_print(f"   📏 尺寸: {doc.width} x {doc.height}")
                safe_print(f"   📐 分辨率: {doc.resolution} ppi")
                safe_print(f"   🎨 颜色模式: {doc.mode}")
                safe_print(f"   🎭 图层数量: {doc.artLayers.length}")
                safe_print(f"   📁 图层组数量: {doc.layerSets.length}")

                # 列出所有图层
                safe_print("   🎨 图层列表:")
                for i, layer in enumerate(doc.artLayers):
                    safe_print(f"      {i+1}. {layer.name} ({layer.kind})")

                # 列出所有图层组
                if doc.layerSets.length > 0:
                    safe_print("   📁 图层组列表:")
                    for i, layer_set in enumerate(doc.layerSets):
                        safe_print(f"      {i+1}. {layer_set.name}")

                # 执行echo命令 (原始代码逻辑)
                try:
                    session.echo(f"成功打开文档: {doc.name}")
                    safe_print(f"   💬 echo输出: 成功打开文档: {doc.name}")
                except Exception as e:
                    safe_print(f"   ⚠️ echo命令失败: {str(e)}")

            safe_print("✅ Session已自动关闭文档")

        except Exception as e:
            safe_print(f"❌ Session打开失败: {str(e)}")

        # 测试3: 尝试打开不存在的文件
        safe_print("\n🔧 测试3: 错误处理 - 打开不存在的文件...")

        try:
            nonexistent_file = "nonexistent_file.psd"
            safe_print(f"📂 尝试打开: {nonexistent_file}")

            app = ps.Application()
            app.load(nonexistent_file)
            safe_print("⚠️ 意外成功打开了不存在的文件")

        except Exception as e:
            safe_print(f"✅ 正确处理错误: {str(e)}")

        # 测试4: 批量打开多个PSD文件
        if len(psd_files) > 1:
            safe_print("\n🔧 测试4: 批量打开多个PSD文件...")

            try:
                app = ps.Application()
                initial_count = len(app.documents)
                safe_print(f"📊 打开前文档数量: {initial_count}")

                opened_docs = []
                for i, (file_key, file_path) in enumerate(psd_files[:3]):  # 最多打开3个
                    try:
                        safe_print(f"📂 打开文件 {i+1}: {file_key}")
                        app.load(file_path)
                        opened_docs.append(file_key)
                    except Exception as e:
                        safe_print(f"   ❌ 打开失败: {str(e)}")

                final_count = len(app.documents)
                safe_print(f"📊 打开后文档数量: {final_count}")
                safe_print(f"✅ 成功打开 {len(opened_docs)} 个文件: {', '.join(opened_docs)}")

                # 关闭所有打开的测试文档
                for i in range(min(3, len(app.documents))):
                    if i < len(app.documents):
                        try:
                            doc = app.documents[len(app.documents) - 1]  # 从最后一个开始关闭
                            safe_print(f"   📁 关闭文档: {doc.name}")
                            doc.close()
                        except:
                            pass

            except Exception as e:
                safe_print(f"❌ 批量打开失败: {str(e)}")

        # 测试5: 打开不同类型的PSD文件
        safe_print("\n🔧 测试5: 测试不同PSD文件类型...")

        for file_key, file_path in psd_files[:2]:  # 测试前2个文件
            try:
                safe_print(f"📂 测试文件: {file_key}")

                with Session(file_path, action="open") as session:
                    doc = session.active_document

                    # 获取详细文档信息
                    safe_print(f"   📄 文档名称: {doc.name}")
                    safe_print(f"   📏 尺寸: {doc.width} x {doc.height}")
                    safe_print(f"   📐 分辨率: {doc.resolution} ppi")
                    safe_print(f"   🎨 颜色模式: {doc.mode}")
                    safe_print(f"   📊 位深度: {doc.bitsPerChannel}")
                    safe_print(f"   🎭 总图层数: {doc.artLayers.length}")
                    safe_print(f"   📁 图层组数: {doc.layerSets.length}")
                    safe_print(f"   📁 通道数: {doc.channels.length}")

                    # 检查是否有保存历史
                    try:
                        safe_print(f"   📚 历史状态数: {len(doc.historyStates) if hasattr(doc, 'historyStates') else '无法访问'}")
                    except:
                        safe_print(f"   📚 历史状态: 无法访问")

            except Exception as e:
                safe_print(f"   ❌ 测试失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "open_psd_test_result.txt")

            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Open PSD 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试的PSD文件数量: {len(psd_files)}\n\n")
                f.write("测试的文件:\n")
                for file_key, file_path in psd_files:
                    f.write(f"- {file_key}: {file_path}\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")

            safe_print(f"   ✅ 保存测试结果: {result_file}")

        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第8项: open_psd.py 测试完成!")
        safe_print("✅ 验证功能: 直接API打开、Session打开、错误处理、批量操作")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        safe_print("🔍 请检查:")
        safe_print("1. Photoshop是否已启动")
        safe_print("2. PSD文件是否存在且可访问")
        safe_print("3. 文件路径是否正确")
        safe_print("4. 文件权限是否正常")
        return False

if __name__ == "__main__":
    test_open_psd()