"""
系统编排器
协调各模块工作，处理完整流程
"""

import asyncio
from typing import Any, Dict, List, Optional
from .config import config
from .utils import logger, AsyncTimer


class FeedbackManager:
    """反馈管理器"""
    
    def __init__(self):
        self.callbacks = []
    
    def add_callback(self, callback):
        """添加反馈回调"""
        self.callbacks.append(callback)
    
    def info(self, message: str):
        """信息反馈"""
        logger.info(f"INFO: {message}")
        for callback in self.callbacks:
            callback("info", message)
    
    def success(self, message: str):
        """成功反馈"""
        logger.info(f"SUCCESS: {message}")
        for callback in self.callbacks:
            callback("success", message)
    
    def warning(self, message: str):
        """警告反馈"""
        logger.warning(f"WARNING: {message}")
        for callback in self.callbacks:
            callback("warning", message)
    
    def error(self, message: str):
        """错误反馈"""
        logger.error(f"ERROR: {message}")
        for callback in self.callbacks:
            callback("error", message)


class Action:
    """动作类"""
    
    def __init__(
        self,
        name: str,
        category: str,
        params: Dict[str, Any] = None
    ):
        self.name = name
        self.category = category
        self.params = params or {}
        self.timestamp = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category,
            "params": self.params
        }


class ExecutionResult:
    """执行结果类"""
    
    def __init__(self, success: bool, message: str, data: Any = None):
        self.success = success
        self.message = message
        self.data = data


class ActionSequence:
    """动作序列类"""
    
    def __init__(self, actions: List[Action]):
        self.actions = actions
    
    def __len__(self):
        return len(self.actions)
    
    def __iter__(self):
        return iter(self.actions)


class ModuleInterface:
    """模块接口基类"""
    
    async def initialize(self):
        """初始化模块"""
        pass
    
    async def process(self, input_data: Any) -> Any:
        """处理输入数据"""
        raise NotImplementedError
    
    async def cleanup(self):
        """清理资源"""
        pass


class MockASRModule(ModuleInterface):
    """模拟ASR模块 (待实现Whisper集成)"""
    
    async def process(self, audio_chunk: bytes) -> str:
        """语音识别"""
        async with AsyncTimer(logger) as timer:
            # TODO: 集成Whisper
            # return await whisper.transcribe(audio_chunk)
            
            # 模拟处理
            await asyncio.sleep(0.05)  # 50ms
            return "帮我锐化图片"
    
    async def initialize(self):
        logger.info("ASR module initialized (mock)")


class MockLLMModule(ModuleInterface):
    """模拟LLM模块 (待实现本地模型集成)"""
    
    def __init__(self):
        self.actions_registry = {}
    
    async def process(self, text: str) -> ActionSequence:
        """语义理解"""
        async with AsyncTimer(logger) as timer:
            # TODO: 集成LLM
            # 解析自然语言为动作序列
            
            # 模拟处理
            await asyncio.sleep(0.1)  # 100ms
            
            # 模拟解析结果
            if "锐化" in text:
                actions = [
                    Action("smart_sharpen", "filter", {
                        "amount": 100,
                        "radius": 2.0,
                        "noise": 10
                    })
                ]
            else:
                actions = []
            
            return ActionSequence(actions)
    
    async def initialize(self):
        logger.info("LLM module initialized (mock)")


class MockExecutorModule(ModuleInterface):
    """模拟执行引擎 (待实现Photoshop API调用)"""
    
    def __init__(self):
        self.action_registry = {}
    
    async def execute(self, action: Action) -> ExecutionResult:
        """执行动作"""
        async with AsyncTimer(logger) as timer:
            # TODO: 集成photoshop-python-api
            # 执行真实的Photoshop操作
            
            # 模拟处理
            await asyncio.sleep(0.1)  # 100ms
            
            logger.info(f"Executing action: {action.name}", params=action.params)
            return ExecutionResult(True, f"Action {action.name} completed")
    
    async def initialize(self):
        logger.info("Executor module initialized (mock)")


class Orchestrator:
    """系统编排器"""
    
    def __init__(self):
        self.feedback = FeedbackManager()
        self.asr = MockASRModule()
        self.llm = MockLLMModule()
        self.executor = MockExecutorModule()
        self.initialized = False
    
    async def initialize(self):
        """初始化所有模块"""
        if self.initialized:
            return
        
        logger.info("Initializing Orchestrator...")
        
        await self.asr.initialize()
        await self.llm.initialize()
        await self.executor.initialize()
        
        self.initialized = True
        logger.info("Orchestrator initialized successfully")
    
    async def process_voice_command(self, audio_chunk: bytes) -> None:
        """处理语音命令的完整流程"""
        await self.initialize()
        
        try:
            # 1. 语音识别
            self.feedback.info("正在识别语音...")
            text = await self.asr.process(audio_chunk)
            self.feedback.success(f"识别结果: {text}")
            
            # 2. 语义理解
            self.feedback.info("正在理解命令...")
            actions = await self.llm.process(text)
            self.feedback.info(f"将执行 {len(actions)} 个动作")
            
            if len(actions) == 0:
                self.feedback.warning("未识别到可执行的动作")
                return
            
            # 3. 执行动作
            for i, action in enumerate(actions, 1):
                self.feedback.info(f"执行动作 {i}/{len(actions)}: {action.name}")
                result = await self.executor.execute(action)
                
                if result.success:
                    self.feedback.success(result.message)
                else:
                    self.feedback.error(f"动作失败: {result.message}")
                    break
            
            self.feedback.success("所有操作已完成")
            
        except Exception as e:
            self.feedback.error(f"操作失败: {str(e)}")
            logger.error("Command processing failed", error=e)
    
    async def cleanup(self):
        """清理所有资源"""
        logger.info("Cleaning up Orchestrator...")
        
        await self.asr.cleanup()
        await self.llm.cleanup()
        await self.executor.cleanup()
        
        logger.info("Orchestrator cleaned up")


# 创建全局编排器实例
orchestrator = Orchestrator()
