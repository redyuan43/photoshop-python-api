# -*- coding: utf-8 -*-
"""Let the current document Fit on screen."""

# Import built-in modules
import os
import sys
import codecs

# 设置UTF-8编码解决中文显示问题
if sys.platform == 'win32':
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    except:
        pass

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import local modules
from photoshop import Session

def safe_print(text):
    """安全的打印函数，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'ignore').decode('ascii'))

safe_print("🖥️ 开始执行 fit_on_screen.py 测试...")
safe_print("📋 请确保Photoshop已经启动!")

with Session() as ps:
    safe_print("✅ Session成功启动")

    # 获取当前活动文档
    if len(ps.app.documents) > 0:
        doc = ps.active_document
        safe_print(f"📄 当前活动文档: {doc.name}")
        safe_print(f"   🆔 文档ID: {doc.id}")
        safe_print(f"   📏 尺寸: {doc.width} x {doc.height} 像素")

        # 原始代码执行
        safe_print("\n🔄 执行适应屏幕命令...")
        char_id = ps.app.charIDToTypeID("FtOn")
        safe_print(f"📝 'FtOn' 转换为类型ID: {char_id}")

        # 执行原始功能
        ps.app.runMenuItem(char_id)
        safe_print("✅ 适应屏幕命令执行完成!")

        safe_print("👁️ 请观察Photoshop窗口 - 文档应该已经适应到屏幕大小")

    else:
        safe_print("⚠️ 没有打开的文档，创建测试文档...")
        test_doc = ps.app.documents.add(2000, 1500, 72, "Fit_Screen_Test")
        safe_print(f"✅ 创建测试文档: {test_doc.name} (2000 x 1500 像素)")

        # 执行适应屏幕
        ps.app.runMenuItem(ps.app.charIDToTypeID("FtOn"))
        safe_print("✅ 适应屏幕命令执行完成!")

safe_print("🎉 fit_on_screen.py 测试完成!")

# 原始功能代码
# with Session() as ps:
#     ps.app.runMenuItem(ps.app.charIDToTypeID("FtOn"))
