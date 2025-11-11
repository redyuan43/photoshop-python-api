# -*- coding: utf-8 -*-
"""
测试创建文字的真实API实现
不依赖扩展脚本，直接测试
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import photoshop.api as ps
from color_manager import color_manager


def create_text_real(params: dict) -> dict:
    """创建文字 - 真实API实现"""
    try:
        app = ps.Application()
        print("[INFO] 连接到Photoshop成功")

        # 检查是否有活动文档
        if app.documents.length == 0:
            print("[INFO] 没有活动文档，创建新文档...")
            doc = app.documents.add(1920, 1080, 72, "Text Test")
        else:
            doc = app.activeDocument
        print(f"[INFO] 当前文档: {doc.name}")

        # 提取参数
        text = params.get('text', '新文字')
        x = params.get('x', 100)
        y = params.get('y', 100)
        font = params.get('font', 'Arial')
        font_size = params.get('font_size', 72)
        color_input = params.get('color', {'red': 0, 'green': 0, 'blue': 0})
        bold = params.get('bold', False)
        italic = params.get('italic', False)
        alignment = params.get('alignment', 'left')

        print(f"[参数] 文字内容: {text}")
        print(f"[参数] 位置: ({x}, {y})")
        print(f"[参数] 字体: {font}, 大小: {font_size}")
        print(f"[参数] 颜色: {color_input}")
        print(f"[参数] 粗体: {bold}, 斜体: {italic}, 对齐: {alignment}")

        # 获取RGB颜色
        color_rgb = color_manager.get_color(color_input)
        print(f"[颜色] 解析后的RGB: {color_rgb}")

        # 创建文字图层
        text_layer = doc.artLayers.add()
        text_layer.kind = ps.LayerKind.TextLayer
        print(f"[创建] 文字图层已创建")

        # 设置文字内容
        text_item = text_layer.textItem
        text_item.contents = text
        print(f"[设置] 文字内容: {text}")

        # 设置位置
        text_item.position = (x, y)
        print(f"[设置] 位置: ({x}, {y})")

        # 设置字体和大小
        text_item.font = font
        text_item.size = font_size
        print(f"[设置] 字体和大小完成")

        # 设置颜色
        color = ps.SolidColor()
        color.rgb.red = color_rgb['red']
        color.rgb.green = color_rgb['green']
        color.rgb.blue = color_rgb['blue']
        text_item.color = color
        print(f"[设置] 颜色完成")

        # 设置样式
        if bold:
            text_item.fauxBold = True
            print(f"[样式] 设置粗体")
        if italic:
            text_item.fauxItalic = True
            print(f"[样式] 设置斜体")

        # 设置对齐
        if alignment == 'center':
            text_item.justification = ps.Justification.Center
            print(f"[样式] 设置居中对齐")
        elif alignment == 'right':
            text_item.justification = ps.Justification.Right
            print(f"[样式] 设置右对齐")
        elif alignment == 'justify':
            text_item.justification = ps.Justification.FullJustify
            print(f"[样式] 设置两端对齐")
        else:
            text_item.justification = ps.Justification.Left
            print(f"[样式] 设置左对齐")

        return {
            'success': True,
            'message': f'文字已创建: {text} at ({x}, {y}) - {font} {font_size}pt',
            'layer_name': text_layer.name
        }

    except ImportError as e:
        return {
            'success': False,
            'message': f'Photoshop模块未找到，请安装photoshop-api: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'创建文字失败: {str(e)}',
            'error_type': type(e).__name__
        }


def main():
    """主函数 - 测试创建文字"""
    print("=" * 70)
    print("测试创建文字 - 真实API")
    print("=" * 70)

    # 测试参数
    test_params = {
        'text': '2025年春季之行',
        'x': 100,
        'y': 200,
        'font': 'Arial',
        'font_size': 72,
        'color': {'red': 255, 'green': 0, 'blue': 0},
        'bold': True,
        'italic': False,
        'alignment': 'center'
    }

    print("\n[开始] 执行创建文字测试...")
    result = create_text_real(test_params)

    print("\n" + "=" * 70)
    print("测试结果:")
    print("=" * 70)
    print(f"状态: {'✅ 成功' if result['success'] else '❌ 失败'}")
    print(f"消息: {result['message']}")
    if 'layer_name' in result:
        print(f"图层名: {result['layer_name']}")
    if 'error_type' in result:
        print(f"错误类型: {result['error_type']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
