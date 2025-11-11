# -*- coding: utf-8 -*-
"""
Photoshop API 完整功能测试套件
测试所有106个核心功能
支持批量测试和单独测试
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from photoshop_api_extended import PhotoshopAPIExtended


class ComprehensiveTestSuite:
    """完整功能测试套件"""

    def __init__(self):
        self.api = PhotoshopAPIExtended()
        self.test_results = []
        self.test_categories = {
            'document': '文档操作',
            'layer': '图层操作',
            'selection': '选择操作',
            'transform': '变换操作',
            'adjustment': '图像调整',
            'filter': '滤镜效果',
            'shape': '形状绘制',
            'text': '文本操作'
        }

    def get_all_test_cases(self) -> List[Dict[str, Any]]:
        """获取所有测试用例"""
        test_cases = []

        # ========== 文档操作 (9个) ==========
        test_cases.extend([
            {'name': 'new_document_default', 'category': 'document', 'action': 'new_document', 'params': {}},
            {'name': 'new_document_custom', 'category': 'document', 'action': 'new_document', 'params': {
                'width': 1920, 'height': 1080, 'resolution': 300, 'name': 'TestDoc'
            }},
            {'name': 'open_document', 'category': 'document', 'action': 'open_document', 'params': {
                'path': 'D:/test.jpg'
            }},
            {'name': 'save_document', 'category': 'document', 'action': 'save_document', 'params': {}},
            {'name': 'save_as_psd', 'category': 'document', 'action': 'save_as_psd', 'params': {
                'path': 'D:/test.psd'
            }},
            {'name': 'save_as_pdf', 'category': 'document', 'action': 'save_as_pdf', 'params': {
                'path': 'D:/test.pdf', 'quality': 3
            }},
            {'name': 'save_as_png', 'category': 'document', 'action': 'save_as_png', 'params': {
                'path': 'D:/test.png'
            }},
            {'name': 'save_as_jpeg', 'category': 'document', 'action': 'save_as_jpeg', 'params': {
                'path': 'D:/test.jpg', 'quality': 8
            }},
            {'name': 'close_document', 'category': 'document', 'action': 'close_document', 'params': {}},
            {'name': 'close_all_documents', 'category': 'document', 'action': 'close_all_documents', 'params': {}},
        ])

        # ========== 图层操作 (17个) ==========
        test_cases.extend([
            {'name': 'duplicate_layer', 'category': 'layer', 'action': 'duplicate_layer', 'params': {}},
            {'name': 'delete_layer', 'category': 'layer', 'action': 'delete_layer', 'params': {}},
            {'name': 'merge_layers', 'category': 'layer', 'action': 'merge_layers', 'params': {}},
            {'name': 'create_layer_set', 'category': 'layer', 'action': 'create_layer_set', 'params': {
                'name': 'Layer Group'
            }},
            {'name': 'move_layer_up', 'category': 'layer', 'action': 'move_layer', 'params': {
                'direction': 'up'
            }},
            {'name': 'move_layer_down', 'category': 'layer', 'action': 'move_layer', 'params': {
                'direction': 'down'
            }},
            {'name': 'rename_layer', 'category': 'layer', 'action': 'rename_layer', 'params': {
                'name': 'New Layer Name'
            }},
            {'name': 'toggle_layer_visibility', 'category': 'layer', 'action': 'toggle_layer_visibility', 'params': {}},
            {'name': 'lock_layer_all', 'category': 'layer', 'action': 'lock_layer', 'params': {
                'lock_type': 'all'
            }},
            {'name': 'unlock_layer', 'category': 'layer', 'action': 'unlock_layer', 'params': {}},
            {'name': 'convert_to_smart_object', 'category': 'layer', 'action': 'convert_to_smart_object', 'params': {}},
            {'name': 'rasterize_layer', 'category': 'layer', 'action': 'rasterize_layer', 'params': {}},
            {'name': 'link_layers', 'category': 'layer', 'action': 'link_layers', 'params': {}},
            {'name': 'unlink_layers', 'category': 'layer', 'action': 'unlink_layers', 'params': {}},
            {'name': 'set_blend_mode_multiply', 'category': 'layer', 'action': 'set_layer_blend_mode', 'params': {
                'mode': 'multiply'
            }},
            {'name': 'set_blend_mode_overlay', 'category': 'layer', 'action': 'set_layer_blend_mode', 'params': {
                'mode': 'overlay'
            }},
            {'name': 'set_layer_opacity', 'category': 'layer', 'action': 'set_layer_opacity', 'params': {
                'opacity': 75
            }},
        ])

        # ========== 选择操作 (11个) ==========
        test_cases.extend([
            {'name': 'select_all', 'category': 'selection', 'action': 'select_all', 'params': {}},
            {'name': 'deselect', 'category': 'selection', 'action': 'deselect', 'params': {}},
            {'name': 'select_inverse', 'category': 'selection', 'action': 'select_inverse', 'params': {}},
            {'name': 'create_rectangular_selection', 'category': 'selection', 'action': 'create_rectangular_selection', 'params': {
                'x': 50, 'y': 50, 'width': 300, 'height': 200
            }},
            {'name': 'create_elliptical_selection', 'category': 'selection', 'action': 'create_elliptical_selection', 'params': {
                'x': 200, 'y': 200, 'width': 150, 'height': 100
            }},
            {'name': 'fill_selection', 'category': 'selection', 'action': 'fill_selection', 'params': {
                'color': {'red': 255, 'green': 0, 'blue': 0}
            }},
            {'name': 'stroke_selection', 'category': 'selection', 'action': 'stroke_selection', 'params': {
                'color': {'red': 0, 'green': 0, 'blue': 0}, 'width': 5
            }},
            {'name': 'feather_selection', 'category': 'selection', 'action': 'feather_selection', 'params': {
                'radius': 10
            }},
            {'name': 'expand_selection', 'category': 'selection', 'action': 'expand_selection', 'params': {
                'pixels': 5
            }},
            {'name': 'contract_selection', 'category': 'selection', 'action': 'contract_selection', 'params': {
                'pixels': 5
            }},
        ])

        # ========== 变换操作 (8个) ==========
        test_cases.extend([
            {'name': 'rotate_layer_45', 'category': 'transform', 'action': 'rotate_layer', 'params': {
                'angle': 45
            }},
            {'name': 'rotate_layer_90', 'category': 'transform', 'action': 'rotate_layer', 'params': {
                'angle': 90
            }},
            {'name': 'flip_horizontal', 'category': 'transform', 'action': 'flip_horizontal', 'params': {}},
            {'name': 'flip_vertical', 'category': 'transform', 'action': 'flip_vertical', 'params': {}},
            {'name': 'scale_layer', 'category': 'transform', 'action': 'scale_layer', 'params': {
                'scale_x': 150, 'scale_y': 150
            }},
            {'name': 'free_transform', 'category': 'transform', 'action': 'free_transform', 'params': {}},
            {'name': 'crop', 'category': 'transform', 'action': 'crop', 'params': {}},
            {'name': 'trim', 'category': 'transform', 'action': 'trim', 'params': {}},
        ])

        # ========== 图像调整 (12个) ==========
        test_cases.extend([
            {'name': 'brightness_contrast', 'category': 'adjustment', 'action': 'brightness_contrast', 'params': {
                'brightness': 20, 'contrast': 30
            }},
            {'name': 'hue_saturation', 'category': 'adjustment', 'action': 'hue_saturation', 'params': {
                'hue': 30, 'saturation': 20, 'lightness': 10
            }},
            {'name': 'color_balance', 'category': 'adjustment', 'action': 'color_balance', 'params': {
                'shadows_red': 10, 'midtones_green': -10, 'highlights_blue': 5
            }},
            {'name': 'levels', 'category': 'adjustment', 'action': 'levels', 'params': {
                'input_shadow': 10, 'input_highlight': 240
            }},
            {'name': 'curves', 'category': 'adjustment', 'action': 'curves', 'params': {}},
            {'name': 'vibrance', 'category': 'adjustment', 'action': 'vibrance', 'params': {
                'vibrance': 30, 'saturation': 20
            }},
            {'name': 'auto_tone', 'category': 'adjustment', 'action': 'auto_tone', 'params': {}},
            {'name': 'auto_contrast', 'category': 'adjustment', 'action': 'auto_contrast', 'params': {}},
            {'name': 'auto_color', 'category': 'adjustment', 'action': 'auto_color', 'params': {}},
            {'name': 'invert_colors', 'category': 'adjustment', 'action': 'invert_colors', 'params': {}},
            {'name': 'desaturate', 'category': 'adjustment', 'action': 'desaturate', 'params': {}},
        ])

        # ========== 滤镜效果 (30个) ==========
        test_cases.extend([
            {'name': 'smart_sharpen', 'category': 'filter', 'action': 'smart_sharpen', 'params': {
                'amount': 150, 'radius': 5, 'noiseReduction': 20
            }},
            {'name': 'gaussian_blur', 'category': 'filter', 'action': 'gaussian_blur', 'params': {
                'radius': 10
            }},
            {'name': 'blur', 'category': 'filter', 'action': 'blur', 'params': {}},
            {'name': 'sharpen', 'category': 'filter', 'action': 'sharpen', 'params': {}},
            {'name': 'blur_more', 'category': 'filter', 'action': 'blur_more', 'params': {}},
            {'name': 'motion_blur', 'category': 'filter', 'action': 'motion_blur', 'params': {
                'angle': 45, 'distance': 10
            }},
            {'name': 'radial_blur', 'category': 'filter', 'action': 'radial_blur', 'params': {
                'amount': 10, 'blur_method': 'spin'
            }},
            {'name': 'surface_blur', 'category': 'filter', 'action': 'surface_blur', 'params': {
                'radius': 15, 'threshold': 15
            }},
            {'name': 'lens_blur', 'category': 'filter', 'action': 'lens_blur', 'params': {}},
            {'name': 'median_blur', 'category': 'filter', 'action': 'median_blur', 'params': {}},
            {'name': 'emboss', 'category': 'filter', 'action': 'emboss', 'params': {
                'angle': 45, 'height': 10, 'amount': 100
            }},
            {'name': 'find_edges', 'category': 'filter', 'action': 'find_edges', 'params': {}},
            {'name': 'trace_contour', 'category': 'filter', 'action': 'trace_contour', 'params': {}},
            {'name': 'stylize_diffuse', 'category': 'filter', 'action': 'stylize_diffuse', 'params': {}},
            {'name': 'pixelate_mosaic', 'category': 'filter', 'action': 'pixelate_mosaic', 'params': {
                'cell_size': 10
            }},
            {'name': 'pixelate_crystallize', 'category': 'filter', 'action': 'pixelate_crystallize', 'params': {}},
            {'name': 'pixelate_coloring', 'category': 'filter', 'action': 'pixelate_coloring', 'params': {}},
            {'name': 'noise_add', 'category': 'filter', 'action': 'noise_add', 'params': {
                'amount': 25, 'distribution': 'uniform', 'mono': False
            }},
            {'name': 'noise_dust_scratches', 'category': 'filter', 'action': 'noise_dust_scratches', 'params': {}},
            {'name': 'noise_despeckle', 'category': 'filter', 'action': 'noise_despeckle', 'params': {}},
            {'name': 'noise_median', 'category': 'filter', 'action': 'noise_median', 'params': {}},
            {'name': 'render_clouds', 'category': 'filter', 'action': 'render_clouds', 'params': {}},
            {'name': 'render_difference_clouds', 'category': 'filter', 'action': 'render_difference_clouds', 'params': {}},
            {'name': 'render_fibers', 'category': 'filter', 'action': 'render_fibers', 'params': {}},
            {'name': 'render_lens_flare', 'category': 'filter', 'action': 'render_lens_flare', 'params': {}},
        ])

        # ========== 形状绘制 (8个) ==========
        test_cases.extend([
            {'name': 'create_rectangle', 'category': 'shape', 'action': 'create_rectangle', 'params': {
                'x': 100, 'y': 100, 'width': 200, 'height': 150,
                'color': {'red': 255, 'green': 0, 'blue': 0}
            }},
            {'name': 'create_ellipse', 'category': 'shape', 'action': 'create_ellipse', 'params': {
                'x': 200, 'y': 200, 'width': 150, 'height': 100,
                'color': {'red': 0, 'green': 255, 'blue': 0}
            }},
            {'name': 'create_circle', 'category': 'shape', 'action': 'create_circle', 'params': {
                'x': 300, 'y': 300, 'diameter': 100,
                'color': {'red': 0, 'green': 0, 'blue': 255}
            }},
            {'name': 'create_line', 'category': 'shape', 'action': 'create_line', 'params': {
                'x1': 0, 'y1': 0, 'x2': 200, 'y2': 200,
                'color': {'red': 0, 'green': 0, 'blue': 0}, 'stroke_width': 5
            }},
            {'name': 'create_triangle', 'category': 'shape', 'action': 'create_triangle', 'params': {
                'x': 200, 'y': 300, 'width': 100, 'height': 100,
                'color': {'red': 255, 'green': 255, 'blue': 0}
            }},
            {'name': 'create_star', 'category': 'shape', 'action': 'create_star', 'params': {
                'x': 200, 'y': 200, 'points': 5,
                'outer_radius': 50, 'inner_radius': 25,
                'color': {'red': 255, 'green': 255, 'blue': 0}
            }},
            {'name': 'create_polygon', 'category': 'shape', 'action': 'create_polygon', 'params': {
                'x': 200, 'y': 200, 'sides': 6, 'radius': 50,
                'color': {'red': 255, 'green': 150, 'blue': 0}
            }},
        ])

        # ========== 文本操作 (11个) ==========
        test_cases.extend([
            {'name': 'create_text', 'category': 'text', 'action': 'create_text', 'params': {
                'text': 'Hello Photoshop', 'x': 100, 'y': 100,
                'font': 'Arial', 'font_size': 72,
                'color': {'red': 0, 'green': 0, 'blue': 255}
            }},
            {'name': 'edit_text', 'category': 'text', 'action': 'edit_text', 'params': {
                'text': 'New Text Content'
            }},
            {'name': 'set_text_font', 'category': 'text', 'action': 'set_text_font', 'params': {
                'font': 'Arial'
            }},
            {'name': 'set_text_size', 'category': 'text', 'action': 'set_text_size', 'params': {
                'size': 48
            }},
            {'name': 'set_text_color', 'category': 'text', 'action': 'set_text_color', 'params': {
                'color': {'red': 255, 'green': 0, 'blue': 0}
            }},
            {'name': 'set_text_bold', 'category': 'text', 'action': 'set_text_bold', 'params': {
                'bold': True
            }},
            {'name': 'set_text_italic', 'category': 'text', 'action': 'set_text_italic', 'params': {
                'italic': True
            }},
            {'name': 'set_text_alignment_center', 'category': 'text', 'action': 'set_text_alignment', 'params': {
                'alignment': 'center'
            }},
            {'name': 'set_text_alignment_left', 'category': 'text', 'action': 'set_text_alignment', 'params': {
                'alignment': 'left'
            }},
            {'name': 'warp_text', 'category': 'text', 'action': 'warp_text', 'params': {
                'warp_style': 'arc', 'bend': 50
            }},
            {'name': 'convert_text_to_shape', 'category': 'text', 'action': 'convert_text_to_shape', 'params': {}},
        ])

        return test_cases

    def run_single_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """运行单个测试"""
        start_time = time.time()
        result = {
            'name': test_case['name'],
            'category': test_case['category'],
            'action': test_case['action'],
            'params': test_case['params'],
            'success': False,
            'message': '',
            'execution_time': 0,
            'timestamp': datetime.now().isoformat()
        }

        try:
            api_result = self.api.execute(test_case['action'], test_case['params'])
            result['execution_time'] = time.time() - start_time
            result['success'] = api_result.get('success', False)
            result['message'] = api_result.get('message', '')
            result['api_result'] = api_result
        except Exception as e:
            result['execution_time'] = time.time() - start_time
            result['success'] = False
            result['error'] = str(e)
            result['message'] = f'测试执行异常: {str(e)}'

        return result

    def run_batch_test(self, category: str = None, limit: int = None) -> List[Dict[str, Any]]:
        """批量测试"""
        all_tests = self.get_all_test_cases()

        if category:
            all_tests = [t for t in all_tests if t['category'] == category]

        if limit:
            all_tests = all_tests[:limit]

        print(f"\n{'=' * 80}")
        print(f"开始批量测试: {len(all_tests)} 个功能")
        if category:
            print(f"测试类别: {self.test_categories.get(category, category)}")
        print(f"{'=' * 80}\n")

        results = []
        for i, test in enumerate(all_tests, 1):
            print(f"[{i}/{len(all_tests)}] 测试: {test['name']}")
            print(f"  动作: {test['action']}")
            print(f"  参数: {json.dumps(test['params'], ensure_ascii=False, indent=2)}")

            result = self.run_single_test(test)
            results.append(result)
            self.test_results.append(result)

            if result['success']:
                print(f"  [OK] 成功 ({result['execution_time']:.3f}s)")
            else:
                print(f"  [X] 失败: {result['message']}")
            print()

        return results

    def generate_report(self, results: List[Dict[str, Any]] = None) -> str:
        """生成测试报告"""
        if results is None:
            results = self.test_results

        total = len(results)
        success = sum(1 for r in results if r['success'])
        failed = total - success

        # 按类别统计
        category_stats = {}
        for test in results:
            cat = test['category']
            if cat not in category_stats:
                category_stats[cat] = {'total': 0, 'success': 0, 'failed': 0}
            category_stats[cat]['total'] += 1
            if test['success']:
                category_stats[cat]['success'] += 1
            else:
                category_stats[cat]['failed'] += 1

        report = f"""
{'=' * 80}
Photoshop API 完整功能测试报告
{'=' * 80}

测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

总体统计:
---------
总测试数: {total}
成功: {success} ({success/total*100:.1f}%)
失败: {failed} ({failed/total*100:.1f}%)

{'=' * 80}
按类别统计:
{'=' * 80}
"""

        for cat, stats in category_stats.items():
            cat_name = self.test_categories.get(cat, cat)
            report += f"""
{cat_name} ({cat}):
  总计: {stats['total']}
  成功: {stats['success']} ({stats['success']/stats['total']*100:.1f}%)
  失败: {stats['failed']} ({stats['failed']/stats['total']*100:.1f}%)
"""

        # 失败详情
        failed_tests = [r for r in results if not r['success']]
        if failed_tests:
            report += f"\n{'=' * 80}\n失败详情:\n{'=' * 80}\n"
            for test in failed_tests:
                report += f"""
测试: {test['name']} ({test['action']})
类别: {test['category']}
错误: {test['message']}
参数: {json.dumps(test['params'], ensure_ascii=False, indent=2)}
"""

        report += f"\n{'=' * 80}\n"
        report += f"报告生成完毕 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"{'=' * 80}\n"

        return report

    def interactive_mode(self):
        """交互式测试模式"""
        print("\n" + "=" * 80)
        print("Photoshop API 完整功能测试 - 交互模式")
        print("=" * 80)

        all_tests = self.get_all_test_cases()
        categories = list(set(t['category'] for t in all_tests))

        print("\n可用测试类别:")
        for i, cat in enumerate(categories, 1):
            count = sum(1 for t in all_tests if t['category'] == cat)
            print(f"  {i}. {cat} ({self.test_categories.get(cat, cat)}) - {count}个功能")

        print("\n命令:")
        print("  test all           - 测试所有功能")
        print("  test <category>    - 测试指定类别 (如: test document)")
        print("  test <name>        - 测试单个功能 (如: test new_document_default)")
        print("  list <category>    - 列出类别中的所有功能")
        print("  report             - 显示测试报告")
        print("  quit               - 退出")

        while True:
            try:
                cmd = input("\n> ").strip().split()

                if not cmd:
                    continue

                if cmd[0] == 'quit':
                    break
                elif cmd[0] == 'test':
                    if len(cmd) == 1:
                        # 测试所有
                        results = self.run_batch_test()
                        print(self.generate_report(results))
                    elif len(cmd) == 2:
                        arg = cmd[1]
                        if arg in ['all', '所有', 'everything']:
                            # 测试所有功能
                            print("\n[执行] 测试所有功能...")
                            results = self.run_batch_test()
                            print(self.generate_report(results))
                        elif arg in categories:
                            # 测试类别
                            results = self.run_batch_test(category=arg)
                            print(self.generate_report(results))
                        else:
                            # 测试单个
                            test = next((t for t in all_tests if t['name'] == arg), None)
                            if test:
                                result = self.run_single_test(test)
                                self.test_results.append(result)
                                print(f"\n测试结果:")
                                print(f"  名称: {result['name']}")
                                print(f"  状态: {'[OK] 成功' if result['success'] else '[X] 失败'}")
                                print(f"  消息: {result['message']}")
                                print(f"  时间: {result['execution_time']:.3f}s")
                            else:
                                print(f"未找到测试: {arg}")
                    else:
                        print("命令格式错误: test [all|<category>|<name>]")
                elif cmd[0] == 'list':
                    if len(cmd) == 2:
                        arg = cmd[1]
                        if arg in categories:
                            tests = [t for t in all_tests if t['category'] == arg]
                            print(f"\n{self.test_categories.get(arg, arg)} 功能列表:")
                            for t in tests:
                                print(f"  - {t['name']} ({t['action']})")
                        else:
                            print(f"未找到类别: {arg}")
                    else:
                        print("命令格式错误: list <category>")
                elif cmd[0] == 'report':
                    print(self.generate_report())
                else:
                    print(f"未知命令: {cmd[0]}")

            except KeyboardInterrupt:
                print("\n\n退出测试")
                break
            except Exception as e:
                print(f"\n错误: {str(e)}")

        print("\n" + "=" * 80)
        print("测试结束!")
        print("=" * 80)


def main():
    """主函数"""
    print("=" * 80)
    print("Photoshop API 完整功能测试套件")
    print("=" * 80)
    print("\n支持测试 99+ 个 Photoshop 功能")
    print("包括: 文档、图层、选择、变换、调整、滤镜、形状、文本")
    print("\n选择模式:")
    print("  1. 交互模式 (推荐)")
    print("  2. 批量测试所有功能")
    print("  3. 测试指定类别")
    print("  4. 查看帮助")
    print("  5. 直接开始 (进入交互模式)")

    while True:
        choice = input("\n请选择 (1-5): ").strip()

        suite = ComprehensiveTestSuite()

        if choice in ['1', '5']:
            suite.interactive_mode()
            break
        elif choice == '2':
            results = suite.run_batch_test()
            print(suite.generate_report(results))
            break
        elif choice == '3':
            print("\n可用类别:")
            for cat in suite.test_categories.keys():
                print(f"  - {cat}")
            cat = input("\n输入类别名: ").strip()
            results = suite.run_batch_test(category=cat)
            print(suite.generate_report(results))
            break
        elif choice == '4':
            print("""
使用说明:
---------
1. 交互模式: 提供完整交互式测试界面
2. 批量测试: 自动测试所有99个功能
3. 类别测试: 选择特定类别进行测试

交互模式命令:
  test all           - 测试所有功能
  test <category>    - 测试指定类别 (如: test document)
  test <name>        - 测试单个功能 (如: test new_document_default)
  list <category>    - 列出类别中的所有功能
  report             - 显示测试报告
  quit               - 退出

测试模式:
- 模拟模式: 当Photoshop未运行时，返回模拟结果
- 真实模式: 当Photoshop运行时，执行真实API调用

测试报告:
- 总体统计: 成功/失败数量和百分比
- 类别统计: 按8个类别分别统计
- 失败详情: 显示失败的功能和原因
            """)
        else:
            print("无效选择，请输入 1-5")


if __name__ == "__main__":
    main()
