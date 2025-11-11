"""
编排器测试
"""

import pytest
import asyncio
from core.orchestrator import Orchestrator, Action


@pytest.mark.asyncio
async def test_orchestrator_initialize():
    """测试编排器初始化"""
    orchestrator = Orchestrator()
    await orchestrator.initialize()
    assert orchestrator.initialized == True


@pytest.mark.asyncio
async def test_voice_command_processing():
    """测试语音命令处理"""
    orchestrator = Orchestrator()
    await orchestrator.initialize()
    
    mock_audio = b"mock_audio_data"
    await orchestrator.process_voice_command(mock_audio)
    
    assert True  # 如果没有异常抛出则测试通过


@pytest.mark.asyncio
async def test_action_creation():
    """测试动作创建"""
    action = Action(
        name="smart_sharpen",
        category="filter",
        params={"amount": 100, "radius": 2.0}
    )
    
    assert action.name == "smart_sharpen"
    assert action.category == "filter"
    assert action.params["amount"] == 100


if __name__ == "__main__":
    pytest.main([__file__])
