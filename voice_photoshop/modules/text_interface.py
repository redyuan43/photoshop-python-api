"""
文本输入接口
替代ASR和LLM模块，用户直接输入中文命令
"""

import re
from typing import List, Dict, Any, Tuple
from modules.executor import ActionRegistry
from core.utils import logger


class TextParser:
    """文本命令解析器"""
    
    def __init__(self):
        self.action_registry = ActionRegistry()
        
        # 动作映射表 - 中文命令到动作名称
        self.command_map = {
            # 基本文档操作
            "新建文档": "new_document",
            "新建": "new_document",
            "打开文档": "open_document",
            "打开": "open_document",
            "保存": "save_document",
            "保存为": "save_document",
            
            # 文本操作
            "创建文本": "hello_world",
            "文本图层": "hello_world",
            "文本": "hello_world",
            
            # 图层操作
            "新建图层": "add_layer",
            "添加图层": "add_layer",
            "复制图层": "duplicate_layer",
            "合并图层": "merge_layers",
            "删除图层": "delete_layer",
            "设置混合模式": "layer_blend_mode",
            "设置透明度": "layer_opacity",
            "锁定图层": "layer_lock",
            "选择图层": "set_active_layer",
            "链接图层": "link_layer",
            "移动到底部": "move_to_end",
            "旋转图层": "rotate_layer",
            "栅格化": "convert_smartobject_to_layer",
            "智能对象": "convert_smartobject_to_layer",
            "导入图像": "import_image_as_layer",
            "图片导入": "import_image_as_layer",
            "替换图像": "replace_images",
            
            # 选区操作
            "全选": "select_all",
            "取消选择": "deselect",
            "反选": "invert_selection",
            "扩展选区": "expand_selection",
            "收缩选区": "contract_selection",
            "羽化": "feather_selection",
            "裁剪": "crop",
            "描边": "stroke_selection",
            "填充": "fill_color",
            "删除填充": "delete_and_fill_selection",
            
            # 滤镜效果
            "锐化": "smart_sharpen",
            "智能锐化": "smart_sharpen",
            "模糊": "gaussian_blur",
            "高斯模糊": "gaussian_blur",
            "边缘检测": "edge_detect",
            "浮雕": "emboss",
            "结晶": "crystallize",
            "石板效果": "add_slate",
            
            # 图像调整
            "亮度对比": "brightness_contrast",
            "调整色相": "hue_saturation",
            "色相饱和": "hue_saturation",
            "色阶": "levels",
            "曲线": "curves",
            "反相": "invert",
            "去色": "desaturate",
            "色调分离": "posterize",
            
            # 导出操作
            "导出": "export_document_simple",
            "导出为": "export_document_with_options",
            "图层导出": "export_layers_as_png",
            "Web导出": "export_layers_web",
            "画板导出": "export_artboards",
            "缩略图": "create_thumbnail",
            "保存为PDF": "save_as_pdf",
            "保存为TGA": "save_as_tga",
        }
    
    def parse_command(self, text: str) -> List[Dict[str, Any]]:
        """解析文本命令为动作序列"""
        text = text.strip()
        
        # 检查是否是数字参数格式
        result = self._parse_with_params(text)
        if result:
            return result
        
        # 查找匹配的命令
        for command, action_name in self.command_map.items():
            if command in text:
                return self._create_action_sequence(action_name, text)
        
        # 如果没有匹配的命令，返回空列表
        logger.warning(f"No matching action found for: {text}")
        return []
    
    def _parse_with_params(self, text: str) -> List[Dict[str, Any]]:
        """解析带有参数的命令"""
        # 锐化 100
        if text.startswith("锐化"):
            match = re.search(r'锐化\s+(\d+)', text)
            if match:
                amount = int(match.group(1))
                return [{
                    "action": "smart_sharpen",
                    "params": {"amount": amount, "radius": 2.0}
                }]
        
        # 模糊 5
        if text.startswith("模糊"):
            match = re.search(r'模糊\s+(\d+)', text)
            if match:
                radius = float(match.group(1))
                return [{
                    "action": "gaussian_blur",
                    "params": {"radius": radius}
                }]
        
        return None
    
    def _create_action_sequence(self, action_name: str, text: str) -> List[Dict[str, Any]]:
        """创建动作序列"""
        try:
            action = self.action_registry.get_action(action_name)
            params = self._extract_params_from_text(text, action)
            
            return [{
                "action": action_name,
                "params": params
            }]
        except Exception as e:
            logger.error(f"Failed to create action: {e}")
            return []
    
    def _extract_params_from_text(self, text: str, action) -> Dict[str, Any]:
        """从文本中提取参数"""
        params = {}
        
        # 根据动作类型提取参数
        if action.name == "smart_sharpen" or action.name == "gaussian_blur":
            match = re.search(r'(\d+)', text)
            if match:
                value = int(match.group(1))
                if action.name == "smart_sharpen":
                    params["amount"] = value
                    params["radius"] = 2.0
                else:
                    params["radius"] = value
        
        elif action.name == "new_document":
            match = re.search(r'(\d+)x(\d+)', text)
            if match:
                params["width"] = int(match.group(1))
                params["height"] = int(match.group(2))
        
        # 使用默认参数
        for param_name, param_config in action.params.items():
            if param_name not in params:
                if "default" in param_config:
                    params[param_name] = param_config["default"]
        
        return params
    
    def list_available_commands(self, category: str = None) -> List[Tuple[str, str]]:
        """列出可用的命令"""
        actions = self.action_registry.list_actions(category)
        
        result = []
        for action in actions:
            aliases = action.aliases if hasattr(action, 'aliases') else []
            if aliases:
                for alias in aliases:
                    result.append((alias, action.name))
            else:
                result.append((action.description or action.name, action.name))
        
        return sorted(result)


class TextInterface:
    """文本输入接口"""
    
    def __init__(self):
        self.parser = TextParser()
    
    def process_text_command(self, text: str) -> Dict[str, Any]:
        """处理文本命令"""
        logger.info(f"Processing text command: {text}")
        
        # 解析命令
        actions = self.parser.parse_command(text)
        
        if not actions:
            return {
                "success": False,
                "message": f"未找到匹配的动作: {text}",
                "actions": []
            }
        
        logger.info(f"Parsed {len(actions)} actions")
        for action in actions:
            logger.info(f"  - {action['action']} {action.get('params', {})}")
        
        return {
            "success": True,
            "message": f"成功解析命令: {text}",
            "actions": actions
        }


# 创建全局接口实例
text_interface = TextInterface()
