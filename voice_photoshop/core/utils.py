"""
通用工具模块
包含日志系统、消息格式、工具函数等
"""

import os
import sys
import structlog
from pathlib import Path
from typing import Any, Dict


def setup_logging(log_level: str = 'INFO', log_file: str = None) -> None:
    """设置日志系统"""
    log_level = os.getenv('LOG_LEVEL', log_level)
    log_file = log_file or os.getenv('LOG_FILE')
    
    # 创建日志目录
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 配置structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


class Logger:
    """日志记录器"""
    
    def __init__(self, name: str = 'voice_photoshop'):
        self.logger = structlog.get_logger(name)
    
    def info(self, message: str, **kwargs):
        self.logger.info(message, **kwargs)
    
    def error(self, message: str, error: Exception = None, **kwargs):
        if error:
            self.logger.error(message, error=str(error), **kwargs)
        else:
            self.logger.error(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self.logger.warning(message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        self.logger.debug(message, **kwargs)
    
    def performance(self, operation: str, duration: float, **kwargs):
        """记录性能指标"""
        self.logger.info(
            "performance_metric",
            operation=operation,
            duration_ms=duration * 1000,
            **kwargs
        )


# 全局日志实例
logger = Logger()


def create_message(
    action: str,
    params: Dict[str, Any] = None,
    context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """创建标准消息格式"""
    import time
    import uuid
    
    message = {
        "id": str(uuid.uuid4()),
        "action": action,
        "timestamp": time.time(),
        "params": params or {},
        "context": context or {}
    }
    
    return message


def validate_params(params: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """验证参数是否符合模式"""
    for key, rule in schema.items():
        if rule.get('required', False) and key not in params:
            return False
        
        if key in params and 'type' in rule:
            expected_type = rule['type']
            actual_value = params[key]
            
            if expected_type == 'int' and not isinstance(actual_value, int):
                return False
            elif expected_type == 'float' and not isinstance(actual_value, (int, float)):
                return False
            elif expected_type == 'str' and not isinstance(actual_value, str):
                return False
    
    return True


def safe_import(module_name: str):
    """安全导入模块"""
    try:
        import importlib
        return importlib.import_module(module_name)
    except ImportError as e:
        logger.error(f"Failed to import module: {module_name}", error=e)
        return None


class AsyncTimer:
    """异步计时器"""
    
    def __init__(self, logger_instance: Logger = None):
        self.logger = logger_instance or logger
    
    async def __aenter__(self):
        import time
        self.start = time.time()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        import time
        duration = time.time() - self.start
        self.logger.performance(
            operation="async_operation",
            duration=duration
        )
