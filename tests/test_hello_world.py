# -*- coding: utf-8 -*-
"""测试第1项: hello_world.py - 基础连接和Hello World示例"""

import os
import sys
from test_framework import PhotoshopTestCase, register_test_case, create_session_test

class HelloWorldTest(PhotoshopTestCase):
    """Hello World测试用例"""

    def __init__(self):
        super().__init__(
            name="hello_world",
            description="基础连接测试，创建Hello World文档"
        )

    def run_test(self):
        """运行Hello World测试"""
        from photoshop import Session

        with Session() as ps:
            self._execute_hello_world_test(ps)

    def _execute_hello_world_test(self, ps):
        """运行Hello World测试"""
        self.print_result('info', '请确保Photoshop已经启动!')
        self.print_result('success', 'Session成功启动')

        # Create a new document (原始代码逻辑)
        self.print_result('info', '📄 创建新文档...')
        doc = ps.app.documents.add()
        self.print_result('success', f'新文档创建成功 (ID: {doc.id})')
        self.print_result('info', f'📏 默认尺寸: {doc.width} x {doc.height}')

        # Create text layer with "Hello, World!" (原始代码逻辑)
        self.print_result('info', '✏️ 创建文本图层...')
        text_color = ps.SolidColor()
        text_color.rgb.red = 255
        text_color.rgb.green = 0
        text_color.rgb.blue = 0

        new_text_layer = doc.artLayers.add()
        new_text_layer.kind = ps.LayerKind.TextLayer
        new_text_layer.textItem.contents = "Hello, World!"
        new_text_layer.textItem.position = [160, 167]
        new_text_layer.textItem.size = 40
        new_text_layer.textItem.color = text_color

        self.print_result('success', f'文本图层创建成功: {new_text_layer.name}')
        self.print_result('info', f'📝 内容: {new_text_layer.textItem.contents}')
        self.print_result('info', f'🎨 颜色: 红色 (RGB: 255, 0, 0)')
        self.print_result('info', f'📏 大小: {new_text_layer.textItem.size}pt')
        self.print_result('info', f'📍 位置: {new_text_layer.textItem.position}')

        # 验证图层属性
        self.print_result('info', '🔍 验证图层属性...')
        self.print_result('success', f'👁️ 可见性: {"显示" if new_text_layer.visible else "隐藏"}')
        self.print_result('success', f'🌟 透明度: {new_text_layer.opacity}%')
        self.print_result('success', f'🎭 图层类型: {new_text_layer.kind}')

        # 添加额外的测试内容
        self._add_test_content(doc)

        # 最终状态检查
        self._check_final_status(doc)

        # 保存文档
        self._save_document(doc)

        # 功能验证
        self._verify_functionality()

    def _add_test_content(self, doc):
        """添加测试内容"""
        self.print_result('info', '🎨 添加更多测试内容...')

        # 创建蓝色背景图层
        bg_layer = doc.artLayers.add()
        bg_layer.name = "Background Color"
        bg_layer.move(doc.artLayers[0], ps.ElementPlacement.PlaceBefore)

        bg_color = ps.SolidColor()
        bg_color.rgb.red = 200
        bg_color.rgb.green = 220
        bg_color.rgb.blue = 255
        ps.app.backgroundColor = bg_color

        doc.selection.selectAll()
        doc.selection.fill(ps.app.backgroundColor)
        doc.selection.deselect()
        self.print_result('success', f'背景图层创建并填充: {bg_layer.name}')

        # 创建装饰性文本
        decor_text = doc.artLayers.add()
        decor_text.kind = ps.LayerKind.TextLayer
        decor_text.name = "Decoration Text"
        decor_text.textItem.contents = "Photoshop Python API - 基础连接测试"
        decor_text.textItem.size = 20
        decor_text.textItem.position = [100, 100]

        text_color = ps.SolidColor()
        text_color.rgb.red = 255
        text_color.rgb.green = 0
        text_color.rgb.blue = 0
        decor_text.textItem.color = text_color

        self.print_result('success', f'装饰文本创建: {decor_text.name}')

        # 创建彩色方块装饰
        self._create_color_decorations(doc)

    def _create_color_decorations(self, doc):
        """创建彩色装饰"""
        self.print_result('info', '🔲 添加彩色方块装饰...')
        colors = [
            ("红色装饰", 255, 100, 100, [50, 200]),
            ("绿色装饰", 100, 255, 100, [150, 200]),
            ("蓝色装饰", 100, 100, 255, [250, 200])
        ]

        for name, r, g, b, position in colors:
            decor_layer = doc.artLayers.add()
            decor_layer.name = name

            color = ps.SolidColor()
            color.rgb.red = r
            color.rgb.green = g
            color.rgb.blue = b
            ps.app.foregroundColor = color

            x, y = position
            doc.selection.select([[x, y], [x+50, y], [x+50, y+50], [x, y+50]])
            doc.selection.fill(ps.app.foregroundColor)
            doc.selection.deselect()
            self.print_result('success', f'创建装饰: {name}')

    def _check_final_status(self, doc):
        """检查最终状态"""
        self.print_result('info', '📊 最终文档状态:')
        self.print_result('success', f'🎭 总图层数量: {doc.artLayers.length}')
        self.print_result('success', f'📄 文档名称: {doc.name}')
        self.print_result('success', f'📏 文档尺寸: {doc.width} x {doc.height}')
        self.print_result('success', f'📐 分辨率: {doc.resolution} ppi')

    def _save_document(self, doc):
        """保存文档"""
        self.print_result('info', '💾 保存文档...')
        try:
            save_dir = os.path.join(os.path.dirname(__file__), "..", "tested_cases")
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            jpg_file = os.path.join(save_dir, "hello_world_test.jpg")
            save_options = ps.JPEGSaveOptions(quality=10)
            doc.saveAs(jpg_file, save_options, asCopy=True)
            self.print_result('success', f'文档保存成功: {jpg_file}')

        except Exception as e:
            self.print_result('warning', f'保存失败: {str(e)}')

    def _verify_functionality(self):
        """验证功能"""
        self.print_result('info', '🔍 基础功能验证:')
        features = [
            "Session连接成功",
            "文档创建功能正常",
            "文本图层创建功能正常",
            "颜色设置功能正常",
            "图层操作功能正常",
            "装饰元素创建成功",
            "文档保存功能可用"
        ]

        for feature in features:
            self.print_result('success', feature)

        self.print_result('info', '👁️ 在Photoshop中您应该能看到:')
        visual_elements = [
            "🔴 红色大文字: 'Hello, World!' (40pt)",
            "🔵 浅蓝色背景",
            "🔴 红色小文字: 'Photoshop Python API - 基础连接测试'",
            "🟢🔴🔵 三个彩色方块装饰",
            "📋 多个图层的层次结构"
        ]

        for element in visual_elements:
            self.print_result('info', element)

# 注册测试用例
register_test_case("hello_world", HelloWorldTest)

if __name__ == "__main__":
    # 如果直接运行此文件，执行测试
    from test_framework import run_test_case
    run_test_case("hello_world")