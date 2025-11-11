#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置验证脚本
用于验证API密钥配置是否正确
"""

import sys
import os
from pathlib import Path

def test_python_config():
    """测试Python配置文件"""
    print("测试Python配置文件...")

    try:
        # 尝试导入配置
        sys.path.insert(0, str(Path(__file__).parent))
        from config import api_config

        # 验证配置
        missing_keys = api_config.validate_required_keys()

        if not missing_keys:
            print("[OK] Python配置文件正常")
            return True
        else:
            print(f"[WARN] 缺少必需的API密钥: {missing_keys}")
            return False

    except ImportError as e:
        print(f"[ERROR] 无法导入Python配置: {e}")
        print("请复制 config.example.py 为 config.py 并配置API密钥")
        return False

def test_yaml_config():
    """测试YAML配置文件"""
    print("测试YAML配置文件...")

    try:
        from voice_photoshop.config_manager import config_manager

        # 打印配置状态
        config_manager.print_status()

        # 验证至少有一个配置
        status = config_manager.validate_config()
        has_config = any(info['configured'] for info in status.values())

        if has_config:
            print("[OK] YAML配置文件正常")
            return True
        else:
            print("[WARN] 没有找到有效的API配置")
            return False

    except ImportError as e:
        print(f"[ERROR] 无法导入YAML配置: {e}")
        print("请复制 voice_photoshop/config.example.yaml 为 voice_photoshop/config.yaml")
        return False

def test_environment_variables():
    """测试环境变量配置"""
    print("测试环境变量...")

    env_vars = ['QWEN_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY']
    found_vars = []

    for var in env_vars:
        value = os.environ.get(var)
        if value:
            found_vars.append(var)
            print(f"[OK] {var}: 已配置 (长度: {len(value)})")
        else:
            print(f"[WARN] {var}: 未配置")

    if found_vars:
        print(f"[OK] 找到 {len(found_vars)} 个环境变量配置")
        return True
    else:
        print("[WARN] 没有找到环境变量配置")
        return False

def main():
    """主函数"""
    print("开始验证API密钥配置...")
    print("=" * 60)

    results = []

    # 测试各种配置方法
    results.append(test_environment_variables())
    results.append(test_python_config())
    results.append(test_yaml_config())

    print("=" * 60)

    # 总结结果
    success_count = sum(results)
    if success_count > 0:
        print(f"[OK] 配置验证完成！({success_count}/{len(results)} 种方法可用)")
        print("\n配置使用说明:")
        print("1. 环境变量 - 最高优先级")
        print("2. config.py - Python配置文件")
        print("3. config.yaml - YAML配置文件")
        print("\n如需帮助，请查看: API_KEYS_SETUP.md")
        return True
    else:
        print("[ERROR] 没有找到有效的API配置")
        print("\n请按以下步骤配置:")
        print("1. 复制配置模板: cp config.example.py config.py")
        print("2. 编辑配置文件: nano config.py")
        print("3. 填入你的API密钥")
        print("4. 或设置环境变量: export QWEN_API_KEY='your-key'")
        print("\n详细说明请查看: API_KEYS_SETUP.md")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)