# -*- coding: utf-8 -*-
"""
语音控制器 - 基于YAML架构
"""

import re
import sys
from pathlib import Path

# 添加项目根目录
sys.path.insert(0, str(Path(__file__).parent.parent))

from action_registry import ActionRegistry


class VoiceController:
    """语音控制器"""
    
    def __init__(self):
        self.registry = ActionRegistry()
        self.api_implementations = {
            'smart_sharpen': self._api_smart_sharpen,
            'new_document': self._api_new_document,
            'rotate_layer': self._api_rotate_layer,
            'create_rectangle': self._api_create_rectangle,
        }
    
    def parse_command(self, text: str):
        """解析自然语言命令"""
        text = text.lower().strip()
        
        # 通过ActionRegistry查找动作
        action_name = self.registry.find_by_alias(text)
        
        if not action_name:
            # 尝试直接匹配
            for name in self.registry.list_actions():
                metadata = self.registry.get_metadata(name)
                if any(alias.lower() in text for alias in metadata.get('aliases', [])):
                    action_name = name
                    break
        
        if not action_name:
            return None
        
        # 提取参数
        params = self._extract_params(text, action_name)
        
        return {
            'action': action_name,
            'params': params,
            'info': self.registry.get_action_info(action_name)
        }
    
    def _extract_params(self, text: str, action_name: str) -> dict:
        """提取参数"""
        params = {}
        
        # 尺寸格式: "200x150"
        size_match = re.search(r'(\d+)x(\d+)', text)
        if size_match:
            params['width'] = int(size_match.group(1))
            params['height'] = int(size_match.group(2))
        
        # 位置格式: "位置100,200"
        pos_match = re.search(r'位置[为]?(\d+)[,，](\d+)', text)
        if pos_match:
            params['x'] = int(pos_match.group(1))
            params['y'] = int(pos_match.group(2))
        
        # 角度格式: "45度"
        angle_match = re.search(r'(\d+(?:\.\d+)?)度', text)
        if angle_match:
            params['angle'] = float(angle_match.group(1))
        
        # 使用注册表处理默认值
        return self.registry.extract_params(action_name, params)
    
    def execute_api(self, action_name: str, params: dict) -> dict:
        """执行API调用"""
        if action_name not in self.api_implementations:
            return {'success': False, 'message': f'未实现: {action_name}'}
        
        try:
            result = self.api_implementations[action_name](params)
            return {'success': True, 'message': result}
        except Exception as e:
            return {'success': False, 'message': f'错误: {str(e)}'}
    
    # ========== API实现 ==========
    
    def _api_smart_sharpen(self, params):
        """智能锐化"""
        from photoshop import Session
        with Session() as ps:
            doc = ps.active_document
            layer = doc.activeLayer
            
            amount = params.get('amount', 100.0)
            radius = params.get('radius', 3.0)
            noise = params.get('noiseReduction', 20)
            
            idsmart_sharpen_id = ps.app.stringIDToTypeID(ps.EventID.SmartSharpen)
            desc = ps.ActionDescriptor()
            
            idpresetKind = ps.app.stringIDToTypeID(ps.EventID.PresetKind)
            idpresetKindType = ps.app.stringIDToTypeID(ps.EventID.PresetKindType)
            idpresetKindCustom = ps.app.stringIDToTypeID(ps.EventID.PresetKindCustom)
            desc.putEnumerated(idpresetKind, idpresetKindType, idpresetKindCustom)
            
            desc.putUnitDouble(ps.app.charIDToTypeID("Amnt"), ps.app.charIDToTypeID("Rds "), amount)
            desc.putUnitDouble(ps.app.charIDToTypeID("Rds "), ps.app.charIDToTypeID("#Pxl"), radius)
            desc.putUnitDouble(ps.app.stringIDToTypeID("noiseReduction"), ps.app.charIDToTypeID("#Prc"), noise)
            
            idblur = ps.app.charIDToTypeID("blur")
            idblurType = ps.app.stringIDToTypeID("blurType")
            idGsnB = ps.app.charIDToTypeID("GsnB")
            desc.putEnumerated(idblur, idblurType, idGsnB)
            
            ps.app.ExecuteAction(idsmart_sharpen_id, desc)
            
            return f"Smart Sharpen completed (amount:{amount}, radius:{radius}, noise:{noise}%)"
    
    def _api_new_document(self, params):
        """新建文档"""
        from photoshop import Session
        with Session() as ps:
            width = params.get('width', 800)
            height = params.get('height', 600)
            resolution = params.get('resolution', 72)
            
            doc = ps.app.documents.add(width=width, height=height, resolution=resolution)
            return f"Document created {width}x{height}"
    
    def _api_rotate_layer(self, params):
        """旋转图层"""
        from photoshop import Session
        with Session() as ps:
            doc = ps.active_document
            angle = params.get('angle', 45.0)
            
            layer = doc.activeLayer
            if layer.isBackgroundLayer:
                layer = layer.duplicate()
                layer.isBackgroundLayer = False
                doc.activeLayer = layer
            
            layer.rotate(angle, ps.AnchorPosition.MiddleCenter)
            return f"Layer rotated {angle} degrees"
    
    def _api_create_rectangle(self, params):
        """创建矩形框"""
        from photoshop import Session
        with Session() as ps:
            doc = ps.active_document
            x, y = params.get('x', 100), params.get('y', 100)
            width, height = params.get('width', 100), params.get('height', 100)
            
            color = ps.SolidColor()
            color.rgb.red = 255
            color.rgb.green = 100
            color.rgb.blue = 100
            ps.app.foregroundColor = color
            
            x1, y1 = x, y
            x2, y2 = x + width, y + height
            doc.selection.select([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
            doc.selection.fill(ps.app.foregroundColor)
            doc.selection.deselect()
            
            return f"Rectangle created at ({x}, {y}) size {width}x{height}"
    
    def process_command(self, text: str):
        """处理命令"""
        print("
" + "=" * 70)
        print(" Photoshop Voice Control - YAML Architecture")
        print("=" * 70)
        
        print("
[1] Parsing...")
        result = self.parse_command(text)
        
        if not result:
            print(f"[ERROR] Unknown: {text}")
            return
        
        action = result['action']
        params = result['params']
        info = result['info']
        
        print(f"[OK] Action: {action}")
        print(f"[OK] Params: {params}")
        
        print("
[2] Executing...")
        exec_result = self.execute_api(action, params)
        
        print("
" + "=" * 70)
        if exec_result['success']:
            print(f"[OK] SUCCESS: {exec_result['message']}")
        else:
            print(f"[ERROR] FAILED: {exec_result['message']}")
        print("=" * 70)


def main():
    controller = VoiceController()
    
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = input("
请输入命令: ").strip()
    
    controller.process_command(text)


if __name__ == "__main__":
    main()
