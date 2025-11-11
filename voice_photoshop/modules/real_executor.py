#!/usr/bin/env python3
"""
真实Photoshop API执行器
基于 tests/ 文件夹中经过验证的真实API调用
"""

import os
import sys
from typing import Dict, Any, Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from photoshop import Session
    PS_AVAILABLE = True
except ImportError:
    PS_AVAILABLE = False
    print("⚠️  photoshop-python-api 未安装")


class RealExecutor:
    """真实Photoshop API执行器"""
    
    def __init__(self, use_real_api: bool = True):
        self.use_real_api = use_real_api and PS_AVAILABLE
        self.session = None
        
        if not self.use_real_api:
            print("⚠️  运行在模拟模式")
    
    def execute_action(self, action_name: str, params: Dict[str, Any] = None) -> Dict:
        """执行真实Photoshop动作"""
        params = params or {}
        
        if not self.use_real_api:
            # 模拟模式
            return self._mock_execute(action_name, params)
        
        # 真实API调用
        try:
            with Session() as ps:
                return self._real_execute(ps, action_name, params)
        except Exception as e:
            return {
                'success': False,
                'message': f'API调用失败: {str(e)}',
                'error': str(e)
            }
    
    def _mock_execute(self, action_name: str, params: Dict) -> Dict:
        """模拟执行"""
        descriptions = {
            'new_document': '创建新文档',
            'smart_sharpen': '智能锐化',
            'rotate_layer': '旋转图层',
            'select_all': '全选',
            'hello_world': '添加文本',
        }
        return {
            'success': True,
            'message': f"{descriptions.get(action_name, action_name)}执行成功 (模拟)",
            'action': action_name,
            'params': params
        }
    
    def _real_execute(self, ps: Session, action_name: str, params: Dict) -> Dict:
        """真实API执行 - 基于tests/中的验证代码"""
        
        # === 文档操作 ===
        if action_name == 'new_document':
            width = params.get('width', 800)
            height = params.get('height', 600)
            resolution = params.get('resolution', 72)
            name = params.get('name', '语音AI文档')
            
            doc = ps.app.documents.add(
                width=width,
                height=height,
                resolution=resolution,
                name=name
            )
            return {
                'success': True,
                'message': f'创建文档成功: {width}x{height}',
                'document_id': doc.id,
                'document_name': doc.name
            }
        
        # === 智能锐化 - 基于 test_48_smart_sharpen.py ===
        elif action_name == 'smart_sharpen':
            amount = params.get('amount', 100)
            radius = params.get('radius', 2.0)
            noise = params.get('noise', 10)
            
            doc = ps.active_document
            layer = doc.activeLayer
            
            layer.applySmartSharpen(
                amount=amount,
                radius=radius,
                noiseReduction=noise,
                removeMotionBlur=False,
                angle=0,
                moreAccurate=True
            )
            
            return {
                'success': True,
                'message': f'智能锐化完成 (强度:{amount}, 半径:{radius})',
                'action': 'smart_sharpen'
            }
        
        # === 旋转图层 - 基于 test_20_rotate_layer.py ===
        elif action_name == 'rotate_layer':
            angle = params.get('angle', 45.0)
            
            doc = ps.active_document
            layer = doc.activeLayer
            
            # 旋转图层
            layer.rotate(float(angle), ps.AnchorPosition.MiddleCenter)
            
            return {
                'success': True,
                'message': f'图层旋转 {angle} 度',
                'angle': angle
            }
        
        # === 全选 ===
        elif action_name == 'select_all':
            doc = ps.active_document
            doc.selection.selectAll()
            
            return {
                'success': True,
                'message': '全选完成'
            }
        
        # === 添加文本图层 - 基于 test_01_hello_world.py ===
        elif action_name == 'hello_world':
            text_content = params.get('text', 'Hello, World!')
            font_size = params.get('size', 40)
            color_rgb = params.get('color', (255, 0, 0))
            
            doc = ps.active_document
            text_layer = doc.artLayers.add()
            text_layer.kind = ps.LayerKind.TextLayer
            text_layer.textItem.contents = text_content
            text_layer.textItem.size = font_size
            
            # 设置颜色
            text_color = ps.SolidColor()
            text_color.rgb.red = color_rgb[0]
            text_color.rgb.green = color_rgb[1]
            text_color.rgb.blue = color_rgb[2]
            text_layer.textItem.color = text_color
            
            return {
                'success': True,
                'message': f'文本图层创建: "{text_content}"',
                'layer_name': text_layer.name
            }
        
        else:
            return {
                'success': False,
                'message': f'未实现的动作: {action_name}',
                'hint': '请在 real_executor.py 中添加此动作的真实API调用'
            }


if __name__ == "__main__":
    executor = RealExecutor(use_real_api=False)
    
    result = executor.execute_action('new_document', {
        'width': 800,
        'height': 600
    })
    print(f"创建文档: {result}")
