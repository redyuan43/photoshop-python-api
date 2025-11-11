# API密钥配置指南

本项目支持多种AI模型和API服务，需要配置相应的API密钥才能使用。为了保护敏感信息，所有API密钥都通过配置文件或环境变量管理，不会被提交到版本控制系统。

## 🚨 重要安全提示

- **切勿**将包含真实API密钥的配置文件提交到Git
- 所有敏感配置文件已添加到`.gitignore`
- 仅将`*.example.*`文件提交到版本控制

## 配置方法

### 方法1: 使用配置文件（推荐）

#### 1. Python配置文件

```bash
# 复制模板文件
cp config.example.py config.py

# 编辑配置文件，填入你的API密钥
nano config.py
```

在`config.py`中填入你的API密钥：

```python
class APIConfig:
    # 通义千问API密钥
    QWEN_API_KEY: str = "your-qwen-api-key-here"

    # OpenAI API密钥
    OPENAI_API_KEY: str = "your-openai-api-key-here"

    # Anthropic Claude API密钥
    ANTHROPIC_API_KEY: str = "your-anthropic-api-key-here"

    # Google AI API密钥
    GOOGLE_API_KEY: str = "your-google-api-key-here"
```

#### 2. YAML配置文件

```bash
# 复制模板文件
cp voice_photoshop/config.example.yaml voice_photoshop/config.yaml

# 编辑配置文件
nano voice_photoshop/config.yaml
```

在`config.yaml`中配置：

```yaml
api_keys:
  qwen_api_key: "your-qwen-api-key-here"
  openai_api_key: "your-openai-api-key-here"
  anthropic_api_key: "your-anthropic-api-key-here"
  google_api_key: "your-google-api-key-here"

api_endpoints:
  qwen_base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  openai_base_url: "https://api.openai.com/v1"
  anthropic_base_url: "https://api.anthropic.com"
```

### 方法2: 使用环境变量

```bash
# Linux/macOS
export QWEN_API_KEY="your-qwen-api-key"
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export GOOGLE_API_KEY="your-google-api-key"

# Windows (PowerShell)
$env:QWEN_API_KEY="your-qwen-api-key"
$env:OPENAI_API_KEY="your-openai-api-key"
$env:ANTHROPIC_API_KEY="your-anthropic-api-key"
$env:GOOGLE_API_KEY="your-google-api-key"

# Windows (CMD)
set QWEN_API_KEY=your-qwen-api-key
set OPENAI_API_KEY=your-openai-api-key
set ANTHROPIC_API_KEY=your-anthropic-api-key
set GOOGLE_API_KEY=your-google-api-key
```

### 方法3: 使用.env文件（开发环境）

创建`.env`文件（已添加到.gitignore）：

```bash
# .env文件（不会被提交到Git）
QWEN_API_KEY=your-qwen-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
GOOGLE_API_KEY=your-google-api-key-here
```

## 支持的API服务

### 1. 通义千问 (Qwen)

- **获取API密钥**: https://dashscope.console.aliyun.com/
- **配置名称**: `QWEN_API_KEY`
- **Base URL**: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- **支持模型**: qwen-turbo, qwen-plus, qwen-max, qwen3-4b等

### 2. OpenAI

- **获取API密钥**: https://platform.openai.com/api-keys
- **配置名称**: `OPENAI_API_KEY`
- **Base URL**: `https://api.openai.com/v1`
- **支持模型**: gpt-4, gpt-3.5-turbo等

### 3. Anthropic Claude

- **获取API密钥**: https://console.anthropic.com/
- **配置名称**: `ANTHROPIC_API_KEY`
- **Base URL**: `https://api.anthropic.com`
- **支持模型**: claude-3-sonnet, claude-3-haiku等

### 4. Google AI (Gemma等)

- **获取API密钥**: https://makersuite.google.com/app/apikey
- **配置名称**: `GOOGLE_API_KEY`
- **Base URL**: `https://generativelanguage.googleapis.com/v1beta`
- **支持模型**: gemma-pro, gemma-7b等

## 本地模型配置

### Ollama

对于本地模型（如Gemma），需要先安装Ollama：

```bash
# 安装Ollama (Linux/macOS)
curl -fsSL https://ollama.ai/install.sh | sh

# 下载模型
ollama pull gemma:7b
ollama run qwen3:4b

# 启动Ollama服务
ollama serve
```

配置本地模型：

```yaml
llm:
  models:
    gemma3n:
      provider: "custom"
      model_name: "gemma:7b"
      base_url: "http://localhost:11434/v1"
      api_key: "ollama"  # Ollama通常不需要真实API密钥
```

## 配置验证

使用以下命令验证配置是否正确：

```python
# 验证Python配置
python -c "from config import api_config; api_config.validate_required_keys()"

# 验证YAML配置
python -c "from voice_photoshop.config_manager import config_manager; config_manager.print_status()"
```

## 优先级说明

配置加载优先级（从高到低）：

1. **环境变量** - 最高优先级，适合生产环境
2. **配置文件** (`config.py` 或 `config.yaml`) - 适合开发环境
3. **默认值** - 最低优先级，用于演示

## 故障排除

### 常见错误

1. **ImportError: No module named 'config'**
   - 确保已创建`config.py`文件
   - 检查文件路径是否正确

2. **API Key未配置错误**
   - 检查环境变量是否设置正确
   - 确认配置文件中的API密钥格式正确

3. **连接失败**
   - 检查网络连接
   - 确认API端点URL正确
   - 验证API密钥是否有效

### 调试模式

启用调试模式查看详细配置信息：

```python
# 在代码中启用调试
import logging
logging.basicConfig(level=logging.DEBUG)

# 或者修改配置文件
system:
  debug: true
```

## 安全最佳实践

1. **定期轮换API密钥**
2. **使用最小权限原则**
3. **监控API使用量和费用**
4. **不要在日志中打印API密钥**
5. **使用不同的密钥用于开发和生产环境**

## 成本优化建议

1. **优先使用本地模型** - 零API调用成本
2. **设置合理的限制** - max_tokens, temperature等
3. **使用缓存** - 避免重复API调用
4. **监控使用量** - 定期检查API费用

---

如有问题，请参考项目的其他文档或提交Issue。