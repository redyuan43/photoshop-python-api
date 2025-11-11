#!/usr/bin/env python3
"""
主测试运行器
用于运行不同类型的测试
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def run_command(cmd, description=""):
    """运行命令并输出结果"""
    print(f"\n{'='*50}")
    if description:
        print(f"运行: {description}")
    print(f"命令: {cmd}")
    print(f"{'='*50}")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.stdout:
        print("输出:")
        print(result.stdout)

    if result.stderr:
        print("错误:")
        print(result.stderr)

    return result.returncode == 0

def run_unit_tests():
    """运行单元测试"""
    return run_command("python -m pytest tests/unit/ -v", "单元测试")

def run_integration_tests():
    """运行集成测试"""
    return run_command("python -m pytest tests/integration/ -v", "集成测试")

def run_performance_tests():
    """运行性能测试"""
    success = True
    perf_files = list(Path("tests/performance/").glob("*.py"))

    for test_file in perf_files:
        if not run_command(f"python {test_file}", f"性能测试: {test_file.name}"):
            success = False

    return success

def run_demo():
    """运行演示"""
    demo_path = Path("voice_photoshop/demo_final.py")
    if demo_path.exists():
        return run_command(f"python {demo_path}", "完整演示")
    else:
        print(f"演示文件不存在: {demo_path}")
        return False

def run_quick_test():
    """运行快速测试"""
    test_file = Path("tests/integration/quick_api_test.py")
    if test_file.exists():
        return run_command(f"python {test_file}", "快速API测试")
    else:
        print(f"快速测试文件不存在: {test_file}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Photoshop Python API 测试运行器")
    parser.add_argument("--type", choices=["unit", "integration", "performance", "demo", "quick", "all"],
                       default="all", help="测试类型")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")

    args = parser.parse_args()

    print("Photoshop Python API 测试运行器")
    print("=" * 50)

    success = True

    if args.type in ["unit", "all"]:
        if not run_unit_tests():
            success = False

    if args.type in ["integration", "all"]:
        if not run_integration_tests():
            success = False

    if args.type in ["performance", "all"]:
        if not run_performance_tests():
            success = False

    if args.type in ["demo", "all"]:
        if not run_demo():
            success = False

    if args.type in ["quick", "all"] and args.type != "all":
        if not run_quick_test():
            success = False

    print("\n" + "=" * 50)
    if success:
        print("✅ 所有测试通过")
        sys.exit(0)
    else:
        print("❌ 部分测试失败")
        sys.exit(1)

if __name__ == "__main__":
    main()