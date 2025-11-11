# -*- coding: utf-8 -*-
"""
颜色管理器 - 从YAML动态加载颜色映射
"""

import yaml
import os
from typing import Dict, List, Optional, Union

class ColorManager:
    """动态颜色映射管理器"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._color_map = {}
        self._alias_map = {}
        self._load_colors()

    def _load_colors(self):
        """从YAML文件加载颜色配置"""
        colors_file = os.path.join(os.path.dirname(__file__), 'actions', 'colors.yaml')

        if not os.path.exists(colors_file):
            # 如果文件不存在，使用默认颜色
            self._color_map = self._get_default_colors()
            return

        try:
            with open(colors_file, 'r', encoding='utf-8') as f:
                colors = yaml.safe_load(f)

            self._color_map = {}
            self._alias_map = {}

            for color_info in colors:
                name = color_info['name']
                rgb = color_info['rgb']
                aliases = color_info.get('aliases', [])

                # 主颜色
                self._color_map[name] = {
                    'red': rgb[0],
                    'green': rgb[1],
                    'blue': rgb[2]
                }

                # 别名映射
                for alias in aliases:
                    self._alias_map[alias.lower()] = name

                # 自己也作为别名
                self._alias_map[name.lower()] = name

        except Exception as e:
            print(f"[WARNING] 颜色配置文件加载失败，使用默认颜色: {e}")
            self._color_map = self._get_default_colors()

    def _get_default_colors(self) -> Dict:
        """默认颜色映射"""
        return {
            '红色': {'red': 255, 'green': 0, 'blue': 0},
            '绿色': {'red': 0, 'green': 255, 'blue': 0},
            '蓝色': {'red': 0, 'green': 0, 'blue': 255},
            '黄色': {'red': 255, 'green': 255, 'blue': 0},
            '白色': {'red': 255, 'green': 255, 'blue': 255},
            '黑色': {'red': 0, 'green': 0, 'blue': 0},
            '橙色': {'red': 255, 'green': 165, 'blue': 0},
            '紫色': {'red': 128, 'green': 0, 'blue': 128},
            '粉色': {'red': 255, 'green': 192, 'blue': 203},
            '棕色': {'red': 165, 'green': 42, 'blue': 42},
        }

    def get_color(self, color_input: Union[str, dict]) -> Dict[str, int]:
        """
        根据输入获取颜色RGB值
        支持字符串（颜色名）和字典格式
        """
        # 如果已经是字典格式，直接返回
        if isinstance(color_input, dict):
            return color_input

        # 如果不是字符串，尝试转换
        if not isinstance(color_input, str):
            color_input = str(color_input)

        # 查找颜色（忽略大小写）
        color_name = color_input.lower()

        # 先在别名映射中查找
        if color_name in self._alias_map:
            actual_name = self._alias_map[color_name]
            return self._color_map[actual_name]

        # 再直接在主映射中查找
        for name, rgb in self._color_map.items():
            if name.lower() == color_name:
                return rgb

        # 没找到，返回默认值
        print(f"[WARNING] 未找到颜色: {color_input}，使用默认红色")
        return {'red': 255, 'green': 0, 'blue': 0}

    def list_colors(self) -> List[str]:
        """列出所有可用颜色"""
        return list(self._color_map.keys())

    def add_color(self, name: str, rgb: List[int], aliases: List[str] = None):
        """添加新颜色"""
        aliases = aliases or []

        # 添加主颜色
        self._color_map[name] = {
            'red': rgb[0],
            'green': rgb[1],
            'blue': rgb[2]
        }

        # 添加别名
        self._alias_map[name.lower()] = name
        for alias in aliases:
            self._alias_map[alias.lower()] = name

    def get_stats(self) -> Dict:
        """获取颜色统计信息"""
        return {
            'total_colors': len(self._color_map),
            'total_aliases': len(self._alias_map),
            'colors': list(self._color_map.keys())
        }


# 全局实例
color_manager = ColorManager()
