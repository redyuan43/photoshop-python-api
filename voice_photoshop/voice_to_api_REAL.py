# -*- coding: utf-8 -*-
"""
语音转真实Photoshop API调用
基于真实API调用（不是测试文件）
"""

import re
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入颜色管理器
from voice_photoshop.color_manager import color_manager

# 自然语言解析到API调用
def parse_command(text):
    """解析自然语言命令，返回API调用信息"""
    text = text.lower().strip()

    # 1. 智能锐化 - 基于 session_smart_sharpen.py
    if re.search(r'sharpen|锐化|清晰', text):
        return {
            'action': 'smart_sharpen',
            'params': {
                'amount': 100.0,
                'radius': 3.0,
                'noiseReduction': 20,
                'removeMotionBlur': False,
                'angle': 0,
                'moreAccurate': True
            },
            'api_code': """
# 应用智能锐化 - 基于 session_smart_sharpen.py (Action Manager)
# 使用Action Manager调用SmartSharpen
idsmart_sharpen_id = ps.app.stringIDToTypeID(ps.EventID.SmartSharpen)
desc = ps.ActionDescriptor()

# 设置PresetKind为Custom
idpresetKind = ps.app.stringIDToTypeID(ps.EventID.PresetKind)
idpresetKindType = ps.app.stringIDToTypeID(ps.EventID.PresetKindType)
idpresetKindCustom = ps.app.stringIDToTypeID(ps.EventID.PresetKindCustom)
desc.putEnumerated(idpresetKind, idpresetKindType, idpresetKindCustom)

# 设置参数
desc.putUnitDouble(ps.app.charIDToTypeID("Amnt"), ps.app.charIDToTypeID("Rds "), 100.0)
desc.putUnitDouble(ps.app.charIDToTypeID("Rds "), ps.app.charIDToTypeID("#Pxl"), 3.0)
desc.putUnitDouble(ps.app.stringIDToTypeID("noiseReduction"), ps.app.charIDToTypeID("#Prc"), 20)

# 执行Action
ps.app.ExecuteAction(idsmart_sharpen_id, desc)
"""
        }

    # 2. 新建文档 - 基于真实API
    if re.search(r'新建.*文档|创建.*文档', text):
        return {
            'action': 'new_document',
            'params': {'width': 800, 'height': 600},
            'api_code': """
# 创建新文档
doc = ps.app.documents.add(width=800, height=600)
"""
        }

    # 3. 旋转图层 - 基于 test_20_rotate_layer.py
    if re.search(r'旋转|rotate', text):
        return {
            'action': 'rotate_layer',
            'params': {'angle': 45},
            'api_code': """
# 旋转图层
layer = ps.active_document.activeLayer
layer.rotate(45, ps.AnchorPosition.MiddleCenter)
"""
        }

    # 4. 创建矩形框 - 基于 test_02_create_new_document.py
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
            'params': {
                'x': x, 'y': y,
                'width': width, 'height': height,
                'color': {'red': 255, 'green': 100, 'blue': 100}
            },
            'api_code': f"""
# 创建矩形框 - 基于 test_02_create_new_document.py
doc = ps.active_document

# 设置颜色
color = ps.SolidColor()
color.rgb.red = {255}
color.rgb.green = {100}
color.rgb.blue = {100}
ps.app.foregroundColor = color

# 创建矩形选择区域
x1, y1 = {x}, {y}
x2, y2 = {x + width}, {y + height}
doc.selection.select([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])

# 填充颜色
doc.selection.fill(ps.app.foregroundColor)

# 取消选择
doc.selection.deselect()
"""
        }

    return None


def execute_api(action_name, params):
    """执行真实的Photoshop API调用"""
    try:
        # 导入Photoshop模块
        from photoshop import Session

        with Session() as ps:
            if action_name == 'smart_sharpen':
                # === 智能锐化 - 基于 session_smart_sharpen.py (Action Manager) ===
                doc = ps.active_document
                layer = doc.activeLayer

                # 获取参数
                amount = params.get('amount', 100.0)
                radius = params.get('radius', 3.0)
                noise = params.get('noiseReduction', 20)

                # 使用Action Manager调用SmartSharpen
                idsmart_sharpen_id = ps.app.stringIDToTypeID(ps.EventID.SmartSharpen)
                desc = ps.ActionDescriptor()

                # 设置PresetKind为Custom
                idpresetKind = ps.app.stringIDToTypeID(ps.EventID.PresetKind)
                idpresetKindType = ps.app.stringIDToTypeID(ps.EventID.PresetKindType)
                idpresetKindCustom = ps.app.stringIDToTypeID(ps.EventID.PresetKindCustom)
                desc.putEnumerated(idpresetKind, idpresetKindType, idpresetKindCustom)

                # 设置Amount (percentage)
                idAmnt = ps.app.charIDToTypeID("Amnt")
                idPrc = ps.app.charIDToTypeID("Rds ")
                desc.putUnitDouble(idAmnt, idPrc, amount)

                # 设置Radius (pixels)
                idRds = ps.app.charIDToTypeID("Rds ")
                idPxl = ps.app.charIDToTypeID("#Pxl")
                desc.putUnitDouble(idRds, idPxl, radius)

                # 设置noiseReduction (percentage)
                idnoiseReduction = ps.app.stringIDToTypeID("noiseReduction")
                idPrcNoise = ps.app.charIDToTypeID("#Prc")
                desc.putUnitDouble(idnoiseReduction, idPrcNoise, noise)

                # 设置blur type为Gaussian
                idblur = ps.app.charIDToTypeID("blur")
                idblurType = ps.app.stringIDToTypeID("blurType")
                idGsnB = ps.app.charIDToTypeID("GsnB")
                desc.putEnumerated(idblur, idblurType, idGsnB)

                # 执行Action
                ps.app.ExecuteAction(idsmart_sharpen_id, desc)

                print(f"[SUCCESS] Smart Sharpen applied successfully!")
                print(f"  Amount: {amount}")
                print(f"  Radius: {radius}")
                print(f"  Noise Reduction: {noise}%")

                return {
                    'success': True,
                    'message': f"Smart Sharpen completed (amount:{amount}, radius:{radius})"
                }

            elif action_name == 'new_document':
                # === 新建文档 ===
                width = params.get('width', 800)
                height = params.get('height', 600)
                doc = ps.app.documents.add(width=width, height=height)

                print(f"[SUCCESS] Document created!")
                print(f"  Size: {width}x{height}")

                return {
                    'success': True,
                    'message': f"Document created {width}x{height}"
                }

            elif action_name == 'rotate_layer':
                # === 旋转图层 - 基于 test_20_rotate_layer.py ===
                doc = ps.active_document
                angle = params.get('angle', 45)

                # 获取当前图层
                layer = doc.activeLayer

                # 检查是否是背景图层（背景图层不能直接旋转）
                if layer.isBackgroundLayer:
                    # 如果是背景图层，先复制一份
                    layer = layer.duplicate()
                    layer.isBackgroundLayer = False
                    doc.activeLayer = layer

                # 旋转图层
                layer.rotate(angle, ps.AnchorPosition.MiddleCenter)

                print(f"[SUCCESS] Layer rotated!")
                print(f"  Angle: {angle} degrees")

                return {
                    'success': True,
                    'message': f"Layer rotated {angle} degrees"
                }

            elif action_name == 'create_rectangle':
                # === 创建矩形框 - 基于 test_02_create_new_document.py ===
                doc = ps.active_document

                x = params.get('x', 100)
                y = params.get('y', 100)
                width = params.get('width', 100)
                height = params.get('height', 100)

                # 处理颜色参数 - 兼容字符串和字典格式
                color_input = params.get('color', {'red': 255, 'green': 100, 'blue': 100})

                # 处理颜色参数 - 使用动态颜色管理器
                color_input = params.get('color', {'red': 255, 'green': 100, 'blue': 100})
                color_rgb = color_manager.get_color(color_input)

                # 设置颜色
                color = ps.SolidColor()
                color.rgb.red = color_rgb['red']
                color.rgb.green = color_rgb['green']
                color.rgb.blue = color_rgb['blue']
                ps.app.foregroundColor = color

                # 创建矩形选择区域
                x1, y1 = x, y
                x2, y2 = x + width, y + height
                doc.selection.select([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])

                # 填充颜色
                doc.selection.fill(ps.app.foregroundColor)

                # 取消选择
                doc.selection.deselect()

                print(f"[SUCCESS] Rectangle created!")
                print(f"  Position: ({x}, {y})")
                print(f"  Size: {width} x {height}")
                print(f"  Color: RGB({color_rgb['red']}, {color_rgb['green']}, {color_rgb['blue']})")

                return {
                    'success': True,
                    'message': f"Rectangle created at ({x}, {y}) size {width}x{height}"
                }

            else:
                print(f"[ERROR] Unknown action: {action_name}")
                return {
                    'success': False,
                    'message': f"Unknown action: {action_name}"
                }

    except ImportError as e:
        print(f"[ERROR] Import error: {str(e)}")
        print(f"  Make sure 'photoshop' module is installed")
        return {
            'success': False,
            'message': f"Import error: {str(e)}"
        }
    except Exception as e:
        print(f"[ERROR] API call failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'message': f"API call failed: {str(e)}"
        }


def main():
    """主函数：语音 -> 解析 -> API调用"""
    print("=" * 70)
    print(" Photoshop Voice Control - Real API Implementation")
    print("=" * 70)

    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = input("\n请输入语音命令（或文本）: ").strip()

    # 1. 解析命令
    print("\n[1] Parsing command...")
    result = parse_command(text)
    if not result:
        print(f"[ERROR] Unknown command: {text}")
        return

    action = result['action']
    params = result['params']

    print(f"[OK] Action: {action}")
    print(f"[OK] Params: {params}")
    print(f"\n[2] API Code to execute:")
    print("-" * 70)
    print(result['api_code'].strip())
    print("-" * 70)

    # 2. 执行API调用
    print(f"\n[3] Executing API call...")
    exec_result = execute_api(action, params)

    print("\n" + "=" * 70)
    if exec_result['success']:
        print(f"[OK] SUCCESS: {exec_result['message']}")
    else:
        print(f"[ERROR] FAILED: {exec_result['message']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
