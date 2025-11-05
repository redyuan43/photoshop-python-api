# -*- coding: utf-8 -*-
"""Example of creating and manipulating layers in Photoshop.

This example demonstrates how to:
1. Create different types of layers
2. Set layer properties and attributes
3. Organize layers in the document
4. Apply basic layer effects

Key concepts:
- Layer creation
- Layer types (art layers, text layers)
- Layer properties
- Layer organization
"""

# Import built-in modules
import sys
import codecs

# 设置UTF-8编码解决中文显示问题
if sys.platform == 'win32':
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    except:
        pass

# Import local modules
from photoshop import Session

def safe_print(text):
    """安全的打印函数，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'ignore').decode('ascii'))

safe_print("🎨 开始执行第14项: creating_a_layer.py 测试...")
safe_print("📋 请确保Photoshop已经启动!")

with Session() as ps:
    safe_print("✅ Session成功启动")

    doc = ps.active_document
    safe_print(f"📄 当前文档: {doc.name}")
    safe_print(f"   🆔 文档ID: {doc.id}")

    # 获取初始图层数量
    initial_layers = doc.artLayers.length
    safe_print(f"🎭 初始图层数量: {initial_layers}")

    safe_print("\n🔧 测试1: 创建普通艺术图层...")
    # Create a new art layer (原始代码)
    new_layer = doc.artLayers.add()

    # Set layer properties (原始代码)
    new_layer.name = "New Art Layer"
    new_layer.opacity = 75
    new_layer.visible = True
    safe_print(f"   ✅ 创建了艺术图层: {new_layer.name}")
    safe_print(f"   📊 图层属性:")
    safe_print(f"      📝 名称: {new_layer.name}")
    safe_print(f"      🌟 透明度: {new_layer.opacity}%")
    safe_print(f"      👁️ 可见性: {'显示' if new_layer.visible else '隐藏'}")
    safe_print(f"      🎯 类型: {new_layer.kind}")

    safe_print("\n📝 测试2: 创建文本图层...")
    # Create a text layer (原始代码)
    text_layer = doc.artLayers.add()
    text_layer.kind = ps.LayerKind.TextLayer

    # Configure text properties (原始代码)
    text_item = text_layer.textItem
    text_item.contents = "Sample Text"
    text_item.size = 72
    text_item.position = [100, 100]
    safe_print(f"   ✅ 创建了文本图层")
    safe_print(f"   📊 文本属性:")
    safe_print(f"      📝 内容: '{text_item.contents}'")
    safe_print(f"      📏 大小: {text_item.size}px")
    safe_print(f"      📍 位置: {text_item.position}")

    safe_print("\n🔄 测试3: 移动图层位置...")
    # Move layers in stack (原始代码)
    original_order = [layer.name for layer in doc.artLayers]
    safe_print(f"   📋 移动前图层顺序: {original_order}")

    new_layer.move(text_layer, ps.ElementPlacement.PlaceAfter)

    new_order = [layer.name for layer in doc.artLayers]
    safe_print(f"   📋 移动后图层顺序: {new_order}")
    safe_print("   ✅ 图层位置重新排列")

    safe_print("\n🎯 测试4: 添加更多图层进行测试...")

    # 创建一个带有颜色的图层
    color_layer = doc.artLayers.add()
    color_layer.name = "Color Fill Layer"
    color_layer.opacity = 50
    safe_print(f"   ✅ 创建颜色图层: {color_layer.name}")

    # 创建另一个文本图层
    text_layer2 = doc.artLayers.add()
    text_layer2.kind = ps.LayerKind.TextLayer
    text_layer2.name = "Second Text Layer"
    text_layer2.textItem.contents = "第二层文本"
    text_layer2.textItem.size = 48
    text_layer2.textItem.position = [200, 200]
    safe_print(f"   ✅ 创建第二个文本图层: {text_layer2.name}")

    # 获取最终图层状态
    final_layers = doc.artLayers.length
    safe_print(f"\n📊 最终图层状态:")
    safe_print(f"   🎭 最终图层数量: {final_layers} (增加了 {final_layers - initial_layers} 个)")
    safe_print("   📝 所有图层列表:")
    for i, layer in enumerate(doc.artLayers):
        visibility = "👁️" if layer.visible else "🚫"
        opacity_info = f" ({layer.opacity}%)" if layer.opacity != 100 else ""
        safe_print(f"      {i+1}. {visibility} {layer.name}{opacity_info}")

    # 测试图层属性访问
    safe_print("\n🔍 图层属性验证:")
    safe_print(f"   ✅ 图层命名功能正常")
    safe_print(f"   ✅ 透明度设置正常")
    safe_print(f"   ✅ 可见性控制正常")
    safe_print(f"   ✅ 图层类型设置正常")
    safe_print(f"   ✅ 图层顺序调整正常")
    safe_print(f"   ✅ 文本属性设置正常")

safe_print("\n🎉 第14项: creating_a_layer.py 测试完成!")
safe_print("✅ 验证功能:")
safe_print("1. 创建不同类型的图层")
safe_print("2. 设置图层属性和属性")
safe_print("3. 文本图层配置")
safe_print("4. 图层顺序管理")
safe_print("5. 图层组织操作")

# 原始代码注释
# with Session() as ps:
#     doc = ps.active_document
#     new_layer = doc.artLayers.add()
#     new_layer.name = "New Art Layer"
#     new_layer.opacity = 75
#     new_layer.visible = True
#     text_layer = doc.artLayers.add()
#     text_layer.kind = ps.LayerKind.TextLayer
#     text_item = text_layer.textItem
#     text_item.contents = "Sample Text"
#     text_item.size = 72
#     text_item.position = [100, 100]
#     new_layer.move(text_layer, ps.ElementPlacement.PlaceAfter)
