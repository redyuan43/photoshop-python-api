import sys
import time
sys.path.insert(0, 'D:/github/photoshop-python-api/voice_photoshop')
from photoshop_api_extended import api

print("=" * 70)
print(" Photoshop API 交互式测试工具")
print("=" * 70)
print("\n预设测试功能:")
print("  1. select_all  - 全选")
print("  2. create_text - 创建文字")
print("  3. auto_tone   - 自动色调")
print("  4. auto_contrast - 自动对比度")
print("  5. smart_sharpen - 智能锐化")
print("  6. gaussian_blur - 高斯模糊")
print("  7. new_document - 新建文档")
print("  8. create_rectangle - 创建矩形")
print("\n输入数字选择功能 (1-8)，或输入 'quit' 退出")
print("=" * 70)

actions = {
    '1': ('select_all', {}),
    '2': ('create_text', {'text': '测试文字', 'x': 100, 'y': 100, 'font_size': 48}),
    '3': ('auto_tone', {}),
    '4': ('auto_contrast', {}),
    '5': ('smart_sharpen', {'amount': 150, 'radius': 5}),
    '6': ('gaussian_blur', {'radius': 3}),
    '7': ('new_document', {'width': 1920, 'height': 1080}),
    '8': ('create_rectangle', {'x': 100, 'y': 100, 'width': 200, 'height': 150}),
}

while True:
    choice = input("\n请选择 (1-8): ").strip()

    if choice.lower() in ['quit', 'q', 'exit', '退出']:
        print("\n感谢使用！")
        break

    if choice in actions:
        action_name, params = actions[choice]
        print(f"\n[执行] {action_name}")
        
        result = api.execute(action_name, params)
        
        if result['success']:
            print(f"✓ 成功: {result['message']}")
        else:
            print(f"✗ 失败: {result['message']}")
            if 'busy' in result['message'].lower():
                print("  提示: COM繁忙，可以重新选择此功能再试一次")
        
        time.sleep(1)  # 等待1秒
    else:
        print("无效选择，请输入 1-8")
