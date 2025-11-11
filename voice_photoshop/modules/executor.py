"""
真实执行引擎
集成photoshop-python-api执行真实的Photoshop操作
"""

import asyncio
import yaml
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Template
from core.utils import logger


class ActionDefinition:
    """动作定义类"""
    
    def __init__(self, data: Dict[str, Any]):
        self.name = data['name']
        self.category = data.get('category', '')
        self.description = data.get('description', '')
        self.aliases = data.get('aliases', [])
        self.params = data.get('params', {})
        self.code = data.get('code', '')
        self.code_template = Template(self.code)
    
    def render_code(self, params: Dict[str, Any]) -> str:
        """渲染动作代码"""
        return self.code_template.render(**params)


class ActionRegistry:
    """动作注册表"""
    
    def __init__(self, actions_dir: str = "actions"):
        self.actions_dir = Path(actions_dir)
        self.actions: Dict[str, ActionDefinition] = {}
        self.load_all_actions()
    
    def load_all_actions(self):
        """加载所有动作定义"""
        yaml_files = list(self.actions_dir.glob("*.yaml"))
        
        for file_path in yaml_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                actions = yaml.safe_load(f)
                
                for action_data in actions:
                    action = ActionDefinition(action_data)
                    self.actions[action.name] = action
        
        logger.info(f"Loaded {len(self.actions)} actions from {len(yaml_files)} files")
    
    def get_action(self, name: str) -> ActionDefinition:
        """获取动作定义"""
        if name not in self.actions:
            raise ValueError(f"Action not found: {name}")
        return self.actions[name]
    
    def list_actions(self, category: str = None) -> List[ActionDefinition]:
        """列出动作"""
        actions = self.actions.values()
        if category:
            actions = [a for a in actions if a.category == category]
        return list(actions)
    
    def find_by_alias(self, alias: str) -> List[ActionDefinition]:
        """通过别名查找动作"""
        result = []
        for action in self.actions.values():
            if alias in action.aliases:
                result.append(action)
        return result


class PhotoshopExecutor:
    """Photoshop执行器"""
    
    def __init__(self):
        self.action_registry = ActionRegistry()
        self.ps = None
        self.session = None
        self.initialized = False
    
    async def initialize(self):
        """初始化执行器"""
        if self.initialized:
            return
        
        try:
            # 尝试导入photoshop-python-api
            import photoshop
            self.ps = photoshop
            
            # 初始化Session
            from photoshop import Session
            self.session = Session()
            
            self.initialized = True
            logger.info("Photoshop executor initialized successfully")
            
        except ImportError as e:
            logger.warning(f"photoshop-python-api not available: {e}")
            logger.warning("Running in mock mode")
            self.initialized = False
        except Exception as e:
            logger.error(f"Failed to initialize Photoshop executor: {e}")
            self.initialized = False
    
    async def execute_action(
        self,
        action_name: str,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """执行单个动作"""
        if not self.initialized:
            # Mock模式
            await asyncio.sleep(0.1)  # 模拟处理时间
            return {
                "success": True,
                "message": f"Mock executed: {action_name}",
                "data": {"params": params or {}}
            }
        
        try:
            # 获取动作定义
            action = self.action_registry.get_action(action_name)
            
            # 渲染代码
            params = params or {}
            code = action.render_code(params)
            
            # 设置执行环境
            execution_globals = {"ps": self.ps}
            execution_locals = {}
            
            # 执行代码
            exec(code, execution_globals, execution_locals)
            
            logger.info(f"Successfully executed action: {action_name}", params=params)
            
            return {
                "success": True,
                "message": f"Action {action_name} completed",
                "data": {"action": action_name, "params": params}
            }
            
        except Exception as e:
            error_msg = f"Failed to execute action {action_name}: {str(e)}"
            logger.error(error_msg, error=e)
            
            return {
                "success": False,
                "message": error_msg,
                "error": str(e)
            }
    
    async def execute_sequence(
        self,
        actions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """执行动作序列"""
        results = []
        success_count = 0
        fail_count = 0
        
        for action_data in actions:
            action_name = action_data.get("action")
            params = action_data.get("params", {})
            
            result = await self.execute_action(action_name, params)
            results.append(result)
            
            if result["success"]:
                success_count += 1
            else:
                fail_count += 1
                # 可以选择是否继续执行后续动作
        
        return {
            "total": len(actions),
            "success": success_count,
            "fail": fail_count,
            "results": results
        }
    
    async def cleanup(self):
        """清理资源"""
        if self.session:
            self.session.close()
        logger.info("Photoshop executor cleaned up")


# 全局执行器实例
executor = PhotoshopExecutor()
