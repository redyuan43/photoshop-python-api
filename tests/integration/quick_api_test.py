# -*- coding: utf-8 -*-
"""
单个API功能快速测试工具
逐个测试Photoshop API功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from photoshop_api_extended import api

def test_single_function():
    """单个功能测试"""

    print("=" * 70)
    print(" Photoshop API 单个功能测试工具")
    print("=" * 70)
    print("\n支持的功能类别：")
    print("  1. 文档操作: new_document, open_document, save_document, close_document")
    print("  2. 图层操作: duplicate_layer, delete_layer, merge_layers, rename_layer")
    print("  3. 选择操作: select_all, deselect, create_rectangular_selection")
    print("  4. 变换操作: rotate_layer, flip_horizontal, scale_layer")
    print("  5. 图像调整: brightness_contrast, hue_saturation, auto_tone")
    print("  6. 滤镜效果: smart_sharpen, gaussian_blur, emboss")
    print("  7. 形状绘制: create_rectangle, create_ellipse, create_circle")
    print("  8. 文本操作: create_text, set_text_font, set_text_color")
    print("\n" + "=" * 70)
    print("\n输入格式:")
    print("  功能名 [参数...]")
    print("  例如: create_text text='Hello' x=100 y=100")
    print("  例如: new_document width=1920 height=1080")
    print("\n输入 'quit' 退出")
    print("=" * 70)

    while True:
        try:
            user_input = input("\n> ").strip()

            if user_input.lower() in ['quit', 'exit', 'q', '退出']:
                print("\n[退出] 感谢使用!")
                break

            if not user_input:
                continue

            # 解析输入
            if '=' in user_input:
                # 有参数的输入: create_text text='Hello' x=100 y=100
                parts = user_input.split()
                function_name = parts[0]
                params = {}

                for part in parts[1:]:
                    if '=' in part:
                        key, value = part.split('=', 1)
                        # 简单处理引号
                        if value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        elif value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        else:
                            # 尝试转换为数字
                            try:
                                if '.' in value:
                                    value = float(value)
                                else:
                                    value = int(value)
                            except:
                                pass
                        params[key] = value
            else:
                # 无参数的输入: smart_sharpen
                function_name = user_input
                params = {}

            # 执行测试
            print(f"\n[执行] 测试功能: {function_name}")
            print(f"[参数] {params}")

            result = api.execute(function_name, params)

            # 显示结果
            if result['success']:
                print(f"✅ 成功: {result['message']}")
            else:
                print(f"❌ 失败: {result['message']}")

        except KeyboardInterrupt:
            print("\n\n[退出] 感谢使用!")
            break
        except Exception as e:
            print(f"\n[错误] {str(e)}")


if __name__ == "__main__":
    test_single_function()
