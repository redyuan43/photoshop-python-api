# -*- coding: utf-8 -*-
"""
批量测试工具 - 系统性测试所有106个API功能
按优先级分批测试，自动记录结果
"""

import sys
import os
import time
import json
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from photoshop_api_extended import api


class BatchTester:
    """批量测试工具"""

    def __init__(self):
        self.results = []
        self.test_file = f'test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

        # 按优先级分组的测试用例
        self.test_groups = {
            'P0_基础功能': {
                'description': '最重要功能，必须测试',
                'tests': [
                    ('select_all', {}),
                    ('deselect', {}),
                    ('create_text', {'text': '测试', 'x': 100, 'y': 100}),
                    ('set_text_font', {'font': 'Arial'}),
                    ('set_text_color', {'color': {'red': 255, 'green': 0, 'blue': 0}}),
                    ('auto_tone', {}),
                    ('auto_contrast', {}),
                    ('auto_color', {}),
                    ('brightness_contrast', {'brightness': 20, 'contrast': 30}),
                ]
            },
            'P1_常用功能': {
                'description': '常用功能，建议测试',
                'tests': [
                    ('smart_sharpen', {'amount': 150, 'radius': 5}),
                    ('gaussian_blur', {'radius': 3}),
                    ('sharpen', {}),
                    ('blur', {}),
                    ('emboss', {}),
                    ('hue_saturation', {'hue': 30, 'saturation': 20}),
                    ('vibrance', {'vibrance': 30}),
                    ('invert_colors', {}),
                    ('desaturate', {}),
                ]
            },
            'P2_形状功能': {
                'description': '形状绘制功能',
                'tests': [
                    ('create_rectangle', {'x': 100, 'y': 100, 'width': 200, 'height': 150}),
                    ('create_ellipse', {'x': 150, 'y': 150, 'width': 100, 'height': 100}),
                    ('create_circle', {'x': 200, 'y': 200, 'width': 100, 'height': 100}),
                    ('create_line', {'x1': 100, 'y1': 100, 'x2': 200, 'y2': 200}),
                    ('create_triangle', {'x': 150, 'y': 150, 'width': 100, 'height': 100}),
                    ('create_star', {'x': 150, 'y': 150, 'width': 100, 'height': 100}),
                    ('create_polygon', {'x': 150, 'y': 150, 'width': 100, 'height': 100, 'sides': 6}),
                ]
            },
            'P3_文档功能': {
                'description': '文档操作功能',
                'tests': [
                    ('new_document', {'width': 1920, 'height': 1080}),
                    ('save_document', {}),
                    ('save_as_psd', {'path': 'test.psd'}),
                    ('save_as_png', {'path': 'test.png'}),
                    ('save_as_jpeg', {'path': 'test.jpg', 'quality': 8}),
                    ('close_document', {}),
                ]
            },
            'P4_图层功能': {
                'description': '图层操作功能',
                'tests': [
                    ('duplicate_layer', {}),
                    ('delete_layer', {}),
                    ('merge_layers', {}),
                    ('create_layer_set', {'name': 'Layer Group'}),
                    ('move_layer', {'direction': 'up'}),
                    ('rename_layer', {'name': 'New Layer'}),
                    ('toggle_layer_visibility', {}),
                    ('lock_layer', {'lock_type': 'all'}),
                    ('unlock_layer', {}),
                    ('convert_to_smart_object', {}),
                    ('rasterize_layer', {}),
                    ('link_layers', {}),
                    ('unlink_layers', {}),
                    ('set_layer_blend_mode', {'mode': 'multiply'}),
                    ('set_layer_opacity', {'opacity': 75}),
                ]
            },
            'P5_变换功能': {
                'description': '变换操作功能',
                'tests': [
                    ('rotate_layer', {'angle': 45}),
                    ('flip_horizontal', {}),
                    ('flip_vertical', {}),
                    ('scale_layer', {'scale': 150}),
                    ('free_transform', {}),
                    ('crop', {}),
                ]
            },
            'P6_高级功能': {
                'description': '高级功能',
                'tests': [
                    ('select_inverse', {}),
                    ('create_rectangular_selection', {'x': 100, 'y': 100, 'width': 200, 'height': 150}),
                    ('create_elliptical_selection', {'x': 150, 'y': 150, 'width': 100, 'height': 100}),
                    ('fill_selection', {'color': {'red': 255, 'green': 0, 'blue': 0}}),
                    ('stroke_selection', {'width': 5, 'color': {'red': 0, 'green': 0, 'blue': 0}}),
                    ('feather_selection', {'radius': 5}),
                    ('expand_selection', {'pixels': 10}),
                    ('contract_selection', {'pixels': 5}),
                    ('levels', {}),
                    ('curves', {}),
                    ('color_balance', {}),
                    ('motion_blur', {'angle': 45, 'distance': 10}),
                    ('radial_blur', {'amount': 10}),
                    ('surface_blur', {'radius': 5, 'threshold': 3}),
                    ('lens_blur', {'radius': 5}),
                    ('median_blur', {'radius': 3}),
                    ('find_edges', {}),
                    ('trace_contour', {}),
                    ('stylize_diffuse', {}),
                    ('pixelate_mosaic', {'cell_size': 8}),
                    ('pixelate_crystallize', {'cell_size': 6}),
                    ('pixelate_coloring', {'max_radius': 8}),
                    ('noise_add', {'amount': 10}),
                    ('noise_dust_scratches', {'width': 1, 'threshold': 0}),
                    ('noise_despeckle', {}),
                    ('noise_median', {'radius': 3}),
                    ('render_clouds', {}),
                    ('render_difference_clouds', {}),
                    ('render_fibers', {}),
                    ('render_lens_flare', {}),
                    ('set_text_size', {'font_size': 48}),
                    ('set_text_bold', {'bold': True}),
                    ('set_text_italic', {'italic': True}),
                    ('set_text_alignment', {'alignment': 'center'}),
                    ('warp_text', {'type': 'arch'}),
                    ('convert_text_to_shape', {}),
                ]
            }
        }

    def run_group(self, group_name, group_info, delay=2):
        """运行一组测试"""
        print(f"\n{'=' * 70}")
        print(f" 测试组: {group_name}")
        print(f" 描述: {group_info['description']}")
        print(f" 测试数: {len(group_info['tests'])}")
        print(f" 建议延迟: {delay}秒")
        print('=' * 70)

        group_results = []
        for action, params in group_info['tests']:
            print(f"\n测试: {action}")
            result = api.execute(action, params)

            success = result['success']
            group_results.append({
                'action': action,
                'params': params,
                'success': success,
                'message': result['message']
            })

            if success:
                print(f"  ✓ 成功: {result['message'][:60]}...")
            else:
                print(f"  ✗ 失败: {result['message'][:60]}...")
                if 'busy' in result['message'].lower():
                    print(f"    提示: COM繁忙，重新测试...")
                    time.sleep(1)
                    retry_result = api.execute(action, params)
                    if retry_result['success']:
                        print(f"    重试成功!")
                        group_results[-1]['success'] = True
                        group_results[-1]['message'] = retry_result['message']

            time.sleep(delay)

        return group_results

    def run_all(self, selected_groups=None):
        """运行所有测试或指定测试组"""
        print("=" * 70)
        print(" Photoshop API 批量测试工具")
        print("=" * 70)
        print(f"\n开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"测试文件: {self.test_file}")
        print("\n可用测试组:")

        for i, (group_name, group_info) in enumerate(self.test_groups.items(), 1):
            print(f"  {i}. {group_name}")
            print(f"     {group_info['description']} ({len(group_info['tests'])}个测试)")

        if not selected_groups:
            print("\n" + "=" * 70)
            print(" 选择要运行的测试组:")
            print("  输入 'all' - 运行所有测试")
            print("  输入 '1,2,3' - 运行指定测试组")
            print("  输入单个数字 - 运行一个测试组")
            print("  输入 'quit' - 退出")
            print("=" * 70)

            choice = input("\n请选择: ").strip()

            if choice.lower() in ['quit', 'exit', 'q']:
                print("\n取消测试")
                return

            if choice.lower() == 'all':
                selected_groups = list(self.test_groups.keys())
            else:
                try:
                    indices = [int(x.strip()) for x in choice.split(',')]
                    selected_groups = [list(self.test_groups.keys())[i-1] for i in indices]
                except:
                    print("\n无效选择，运行第一组测试")
                    selected_groups = [list(self.test_groups.keys())[0]]

        print(f"\n将运行 {len(selected_groups)} 个测试组")
        input("按回车键开始测试...")

        total_tests = 0
        for group_name in selected_groups:
            if group_name in self.test_groups:
                total_tests += len(self.test_groups[group_name]['tests'])

        print(f"\n总计 {total_tests} 个测试，预计需要 {total_tests * 2 / 60:.1f} 分钟")
        input("按回车键继续...")

        # 运行测试
        all_results = {}
        for group_name in selected_groups:
            if group_name in self.test_groups:
                group_info = self.test_groups[group_name]
                results = self.run_group(group_name, group_info)
                all_results[group_name] = results
                self.results.extend(results)

        # 生成报告
        self.generate_report(all_results)

    def generate_report(self, all_results):
        """生成测试报告"""
        print(f"\n{'=' * 70}")
        print(" 测试结果报告")
        print('=' * 70)

        total = 0
        success = 0

        for group_name, results in all_results.items():
            group_total = len(results)
            group_success = sum(1 for r in results if r['success'])
            group_failed = group_total - group_success
            total += group_total
            success += group_success

            print(f"\n{group_name}:")
            print(f"  总计: {group_total}, 成功: {group_success}, 失败: {group_failed}")
            print(f"  成功率: {group_success/group_total*100:.1f}%")

            for result in results:
                if not result['success']:
                    print(f"    ✗ {result['action']}: {result['message'][:50]}")

        print(f"\n{'=' * 70}")
        print(f" 总计: {total} 个测试")
        print(f" 成功: {success} 个 ({success/total*100:.1f}%)")
        print(f" 失败: {total-success} 个")
        print('=' * 70)

        # 保存结果到文件
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': total,
                'success': success,
                'failed': total - success,
                'success_rate': success / total * 100
            },
            'results': all_results
        }

        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        print(f"\n详细结果已保存到: {self.test_file}")


def main():
    """主函数"""
    tester = BatchTester()
    tester.run_all()


if __name__ == "__main__":
    main()
