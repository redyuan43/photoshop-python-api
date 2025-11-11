# -*- coding: utf-8 -*-
"""
测试YAML架构系统
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from action_registry import ActionRegistry


def test_registry():
    """测试注册表系统"""
    print("=" * 60)
    print("测试 ActionRegistry")
    print("=" * 60)

    registry = ActionRegistry()

    # 列出所有动作
    print("\n所有动作:")
    for name in sorted(registry.list_actions()):
        info = registry.get_action_info(name)
        print(f"  {name}: {info['description']}")

    # 测试别名查找
    print("\n测试别名查找:")
    test_cases = [
        "我想锐化图像",
        "新建一个文档",
        "旋转图层45度",
        "创建一个矩形框"
    ]

    for text in test_cases:
        action = registry.find_by_alias(text)
        print(f"  '{text}' -> {action}")

    # 显示metadata示例
    print("\n示例: smart_sharpen 的metadata:")
    metadata = registry.get_metadata('smart_sharpen')
    import json
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    test_registry()
