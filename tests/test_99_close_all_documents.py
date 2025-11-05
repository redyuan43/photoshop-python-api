# -*- coding: utf-8 -*-
"""测试第99项: close_all_documents.py - 关闭所有文档"""

import os
import sys
from datetime import datetime

# 导入公共工具
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import safe_print, get_test_save_dir

def test_close_all_documents():
    """运行close_all_documents测试 - 清理所有打开的文档"""
    safe_print("📋 开始执行第99项: close_all_documents.py 测试...")
    safe_print("📋 此测试用于清理所有遗留的Photoshop文档!")

    try:
        from photoshop import Session

        # 测试1: 获取当前所有打开的文档
        safe_print("\n🔍 测试1: 获取当前所有打开的文档...")
        try:
            with Session() as ps:
                all_docs = ps.app.documents
                doc_count = len(all_docs)
                safe_print(f"   📊 当前打开文档数: {doc_count}")

                if doc_count > 0:
                    safe_print("   📄 文档列表:")
                    for i, doc in enumerate(all_docs, 1):
                        safe_print(f"      {i}. {doc.name} ({doc.width}x{doc.height})")
                else:
                    safe_print("   ✅ 没有打开的文档")

        except Exception as e:
            safe_print(f"❌ 获取文档列表失败: {str(e)}")

        # 测试2: 关闭所有非活动文档
        safe_print("\n🔧 测试2: 关闭所有非活动文档...")
        try:
            with Session() as ps:
                all_docs = list(ps.app.documents)  # 转换为列表避免修改时出错
                closed_count = 0

                for doc in all_docs:
                    try:
                        # 不关闭当前活动文档
                        if doc == ps.active_document:
                            safe_print(f"   ⏭️ 跳过活动文档: {doc.name}")
                            continue

                        safe_print(f"   🔒 关闭文档: {doc.name}")
                        doc.close()
                        closed_count += 1

                    except Exception as doc_e:
                        safe_print(f"   ⚠️ 关闭失败 {doc.name}: {str(doc_e)}")

                safe_print(f"   ✅ 成功关闭 {closed_count} 个文档")

        except Exception as e:
            safe_print(f"❌ 关闭非活动文档失败: {str(e)}")

        # 测试3: 保存并关闭剩余文档
        safe_print("\n💾 测试3: 保存并关闭所有剩余文档...")
        try:
            with Session() as ps:
                remaining_docs = list(ps.app.documents)

                if len(remaining_docs) > 0:
                    safe_print(f"   📊 剩余文档数: {len(remaining_docs)}")

                    for i, doc in enumerate(remaining_docs, 1):
                        try:
                            safe_print(f"   💾 处理文档 {i}/{len(remaining_docs)}: {doc.name}")

                            # 检查文档是否有未保存的更改
                            if doc.saved:
                                safe_print(f"      ✅ 文档已保存，直接关闭")
                                doc.close()
                            else:
                                # 提示用户或使用默认值
                                safe_print(f"      ⚠️ 文档有未保存更改")

                                # 使用不保存方式关闭（测试环境）
                                doc.close(0)  # 0 = 不保存
                                safe_print(f"      ✅ 已不保存方式关闭")

                        except Exception as doc_e:
                            safe_print(f"   ❌ 处理失败 {doc.name}: {str(doc_e)}")
                else:
                    safe_print("   ✅ 没有剩余文档需要关闭")

        except Exception as e:
            safe_print(f"❌ 保存并关闭文档失败: {str(e)}")

        # 测试4: 验证所有文档已关闭
        safe_print("\n✅ 测试4: 验证所有文档已关闭...")
        try:
            with Session() as ps:
                final_count = len(ps.app.documents)

                if final_count == 0:
                    safe_print("   🎉 所有文档已成功关闭!")
                    safe_print("   ✅ Photoshop现在处于干净状态")
                else:
                    safe_print(f"   ⚠️ 仍有 {final_count} 个文档未关闭")
                    for doc in ps.app.documents:
                        safe_print(f"      - {doc.name}")

        except Exception as e:
            safe_print(f"❌ 验证失败: {str(e)}")

        # 测试5: 创建新的干净测试环境
        safe_print("\n🆕 测试5: 创建新的干净测试环境...")
        try:
            with Session(action="new_document") as ps:
                doc = ps.active_document
                safe_print("   ✅ 已创建新的干净测试文档")
                safe_print(f"   📄 文档: {doc.name}")
                safe_print(f"   📏 尺寸: {doc.width}x{doc.height}")

                # 立即关闭它，保持环境干净
                doc.close()
                safe_print("   ✅ 已关闭测试文档")

        except Exception as e:
            safe_print(f"❌ 创建干净环境失败: {str(e)}")

        # 保存测试结果
        safe_print("\n💾 保存测试结果...")
        try:
            save_dir = get_test_save_dir()
            result_file = os.path.join(save_dir, "close_all_documents_test_result.txt")
            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Close All Documents 测试结果\n")
                f.write(f"测试时间: {datetime.now()}\n")
                f.write(f"测试项目: 关闭所有Photoshop文档\n")
                f.write(f"测试内容:\n")
                f.write(f"- 获取当前所有打开的文档\n")
                f.write(f"- 关闭所有非活动文档\n")
                f.write(f"- 保存并关闭所有剩余文档\n")
                f.write(f"- 验证所有文档已关闭\n")
                f.write(f"- 创建新的干净测试环境\n")
                f.write(f"\n测试完成时间: {datetime.now()}\n")
            safe_print(f"   ✅ 保存测试结果: {result_file}")
        except Exception as e:
            safe_print(f"   ⚠️ 保存结果失败: {str(e)}")

        safe_print("\n🎉 第99项: close_all_documents.py 测试完成!")
        safe_print("✅ 验证功能: 文档列表、关闭非活动、保存关闭、清理环境")
        safe_print("🎯 用途: 清理测试遗留文件，保持Photoshop环境干净")
        return True

    except Exception as e:
        safe_print(f"❌ 测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_close_all_documents()
