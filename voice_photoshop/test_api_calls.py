# -*- coding: utf-8 -*-
"""
测试API调用解析
只显示将要执行的API，不实际执行
"""

import re
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def parse_command(text):
    """解析自然语言命令，返回API调用信息"""
    text = text.lower().strip()

    # 1. 智能锐化 - 基于 session_smart_sharpen.py
    if re.search(r'sharpen|锐化|清晰', text):
        return {
            'action': 'smart_sharpen',
            'description': '智能锐化',
            'params': {
                'amount': 100.0,
                'radius': 3.0,
                'noiseReduction': 20,
                'removeMotionBlur': False,
                'angle': 0,
                'moreAccurate': True
            },
            'api_code': """
# Apply Smart Sharpen - based on session_smart_sharpen.py (Action Manager)
from photoshop import Session

with Session() as ps:
    doc = ps.active_document
    layer = doc.activeLayer

    # Use Action Manager to call SmartSharpen
    idsmart_sharpen_id = ps.app.stringIDToTypeID(ps.EventID.SmartSharpen)
    desc = ps.ActionDescriptor()

    # Set PresetKind to Custom
    idpresetKind = ps.app.stringIDToTypeID(ps.EventID.PresetKind)
    idpresetKindType = ps.app.stringIDToTypeID(ps.EventID.PresetKindType)
    idpresetKindCustom = ps.app.stringIDToTypeID(ps.EventID.PresetKindCustom)
    desc.putEnumerated(idpresetKind, idpresetKindType, idpresetKindCustom)

    # Set parameters
    desc.putUnitDouble(ps.app.charIDToTypeID("Amnt"), ps.app.charIDToTypeID("Rds "), 100.0)
    desc.putUnitDouble(ps.app.charIDToTypeID("Rds "), ps.app.charIDToTypeID("#Pxl"), 3.0)
    desc.putUnitDouble(ps.app.stringIDToTypeID("noiseReduction"), ps.app.charIDToTypeID("#Prc"), 20)

    # Execute Action
    ps.app.ExecuteAction(idsmart_sharpen_id, desc)
""",
            'reference': 'session_smart_sharpen.py'
        }

    # 2. 新建文档
    if re.search(r'新建.*文档|创建.*文档', text):
        return {
            'action': 'new_document',
            'description': '创建新文档',
            'params': {'width': 800, 'height': 600},
            'api_code': """
# Create new document
from photoshop import Session

with Session() as ps:
    doc = ps.app.documents.add(width=800, height=600)
""",
            'reference': 'Photoshop API documents.add()'
        }

    # 3. 旋转图层
    if re.search(r'旋转|rotate', text):
        return {
            'action': 'rotate_layer',
            'description': '旋转图层',
            'params': {'angle': 45},
            'api_code': """
# Rotate layer
from photoshop import Session

with Session() as ps:
    layer = ps.active_document.activeLayer
    layer.rotate(45, ps.AnchorPosition.MiddleCenter)
""",
            'reference': 'test_20_rotate_layer.py'
        }

    # 4. 创建矩形框
    if re.search(r'矩形|rectangle|框', text):
        # 提取尺寸参数（如果用户指定了）
        width_match = re.search(r'(\d+)x(\d+)|宽[度]?[为]?(\d+).*高[度]?[为]?(\d+)', text)
        if width_match:
            if width_match.group(1):  # 格式如 200x300
                width, height = int(width_match.group(1)), int(width_match.group(2))
            else:  # 格式如 宽度200 高度300
                width, height = int(width_match.group(3)), int(width_match.group(4))
        else:
            width, height = 100, 100  # 默认尺寸

        # 提取位置参数
        pos_match = re.search(r'位置[为]?(\d+)[,，](\d+)|x[为]?(\d+).*y[为]?(\d+)', text)
        if pos_match:
            if pos_match.group(1):
                x, y = int(pos_match.group(1)), int(pos_match.group(2))
            else:
                x, y = int(pos_match.group(3)), int(pos_match.group(4))
        else:
            x, y = 100, 100  # 默认位置

        return {
            'action': 'create_rectangle',
            'description': '创建矩形框',
            'params': {
                'x': x, 'y': y,
                'width': width, 'height': height,
                'color': {'red': 255, 'green': 100, 'blue': 100}
            },
            'api_code': f"""
# Create Rectangle - based on test_02_create_new_document.py
from photoshop import Session

with Session() as ps:
    doc = ps.active_document

    # Set color
    color = ps.SolidColor()
    color.rgb.red = 255
    color.rgb.green = 100
    color.rgb.blue = 100
    ps.app.foregroundColor = color

    # Create rectangle selection
    x1, y1 = {x}, {y}
    x2, y2 = {x + width}, {y + height}
    doc.selection.select([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])

    # Fill with color
    doc.selection.fill(ps.app.foregroundColor)

    # Deselect
    doc.selection.deselect()
""",
            'reference': 'test_02_create_new_document.py'
        }

    return None


def show_api_call(text):
    """显示API调用信息"""
    result = parse_command(text)
    if not result:
        print(f"[解析] 未知命令: {text}")
        return

    print(f"=" * 60)
    print(f"[动作] {result['description']} ({result['action']})")
    print(f"[参数] {result['params']}")
    print(f"[参考] {result['reference']}")
    print(f"=" * 60)
    print("[将要执行的API调用代码]")
    print(result['api_code'])
    print("=" * 60)


def main():
    test_commands = [
        "我想锐化图像",
        "新建一个800x600的文档",
        "旋转图层45度",
        "创建一个矩形框",
        "创建一个200x150的矩形",
        "在位置100,200创建一个矩形框"
    ]

    print("=" * 60)
    print("测试API调用解析")
    print("=" * 60)

    for cmd in test_commands:
        print(f"\n输入: {cmd}")
        show_api_call(cmd)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        show_api_call(text)
    else:
        main()
