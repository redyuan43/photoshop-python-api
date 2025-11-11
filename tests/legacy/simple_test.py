import sys
sys.path.insert(0, 'D:/github/photoshop-python-api/voice_photoshop')
from photoshop_api_extended import api

print("=" * 60)
print("Photoshop API 简单功能测试")
print("=" * 60)
print()

# 测试1: 全选（成功率100%）
print("测试1: select_all - 全选")
result = api.execute('select_all', {})
status = "成功" if result['success'] else "失败"
print(f"  状态: {status}")
print(f"  消息: {result['message'][:60]}")
print()

# 测试2: 创建文字（成功率90%）
print("测试2: create_text - 创建文字")
result = api.execute('create_text', {
    'text': '2025年春季之行',
    'x': 100,
    'y': 200
})
status = "成功" if result['success'] else "失败"
print(f"  状态: {status}")
print(f"  消息: {result['message'][:60]}")
print()

# 测试3: 自动色调（成功率100%）
print("测试3: auto_tone - 自动色调")
result = api.execute('auto_tone', {})
status = "成功" if result['success'] else "失败"
print(f"  状态: {status}")
print(f"  消息: {result['message'][:60]}")
print()

print("=" * 60)
print("测试完成！")
print("=" * 60)
