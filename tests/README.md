# 测试目录结构说明

## 目录组织

```
tests/
├── unit/           # 单元测试（待补充）
├── integration/    # 集成测试
│   ├── batch_tester.py      # 批量测试
│   ├── quick_api_test.py    # API快速测试
│   └── test_core_features.py # 核心功能测试
├── performance/    # 性能测试
│   ├── test_gemma_improved.py # Gemma模型性能测试
│   └── test_qwen3_4b.py       # Qwen3-4B性能测试
├── legacy/         # 旧版测试文件（已迁移）
│   ├── test_*.py            # 各种测试文件
│   ├── quick_test.py
│   ├── simple_test.py
│   └── interactive_test.py
└── README.md       # 本文件
```

## 使用说明

### 运行集成测试
```bash
python -m pytest tests/integration/
```

### 运行性能测试
```bash
python tests/performance/test_gemma_improved.py
python tests/performance/test_qwen3_4b.py
```

### 运行快速API测试
```bash
python tests/integration/quick_api_test.py
```

### 运行完整演示
```bash
python voice_photoshop/demo_final.py
```

## 测试覆盖范围

- **LLM模型测试**: Gemma, Qwen3等本地模型
- **API功能测试**: Photoshop API调用
- **性能测试**: 响应时间和准确率
- **集成测试**: 完整工作流程
- **对话测试**: 自然语言处理

## 注意事项

- 需要Photoshop运行才能执行API测试
- 本地LLM测试需要相应模型已安装
- 某些测试可能需要特定配置