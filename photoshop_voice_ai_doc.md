# 📘 Photoshop 智能语音控制系统开发文档

## 一、项目概述

### 📖 项目名称
**AI Voice-Controlled Photoshop Assistant**

### 💡 项目目标
通过语音命令自动操作 Photoshop，实现从自然语言（或语音）到自动执行 Photoshop 功能的完整链路。  
系统核心目标是：
- 高精度语义识别；
- 低延迟执行；
- 可扩展 100+ Photoshop 功能；
- 安全、可商业化。

---

## 二、系统总体架构

```
🎤 用户语音
  ↓
[1] ASR 模块（Whisper / FunASR）
  ↓ 文本命令
[2] LLM 模块（Claude / GPT / Qwen）
  ↓ JSON 调用序列
[3] 执行器 (Executor)
  ↓
[4] Photoshop API 调用 (photoshop-python-api)
  ↓
[5] TTS 反馈 / 控制台输出
```

---

## 三、模块划分与职责

| 模块名 | 主要功能 | 部署位置 |
|--------|-----------|-----------|
| **ASR (语音识别)** | 将语音转文字 | Jetson Orin / 本地 GPU |
| **LLM (意图理解)** | 将自然语言 → JSON 动作序列 | 云端或本地大模型 |
| **Action Registry (动作注册库)** | 定义所有可执行 Photoshop 功能 | YAML 文件 |
| **Metadata 生成器** | 自动提取 YAML 元数据供 LLM 提示 | Python 脚本 |
| **Function Schema 生成器** | 将 YAML 转换为 OpenAI Function Schema | Python 脚本 |
| **Executor (执行器)** | 加载模板并安全执行 API 调用 | Windows x86 主机 |
| **MCP Manifest 生成器（可选）** | 生成 Claude MCP 插件配置文件 | Python 脚本 |

---

## 四、数据结构说明

### 1️⃣ 动作定义文件（YAML）

```yaml
# actions/filters.yaml

- name: smart_sharpen
  category: filter
  description: "应用智能锐化滤镜（锐化、清晰化、增强边缘细节）)"
  aliases: ["锐化", "清晰化", "细节增强"]
  params:
    amount: float  # 锐化强度 0–500
    radius: float  # 半径像素
    noise: int     # 降噪百分比
  code: |
    layer = ps.active_document.activeLayer
    layer.applySmartSharpen(
      amount={amount},
      radius={radius},
      noiseReduction={noise},
      removeMotionBlur=False,
      angle=0,
      moreAccurate=True
    )
```

---

### 2️⃣ metadata.json

```json
{
  "smart_sharpen": {
    "category": "filter",
    "description": "应用智能锐化滤镜（锐化、清晰化、增强边缘细节）)",
    "params": ["amount", "radius", "noise"]
  },
  "trim_image": {
    "category": "edit",
    "description": "去除图片空白边缘",
    "params": []
  }
}
```

---

### 3️⃣ openai_functions.json

```json
[
  {
    "name": "smart_sharpen",
    "description": "应用智能锐化滤镜",
    "parameters": {
      "type": "object",
      "properties": {
        "amount": {"type": "number", "description": "锐化强度"},
        "radius": {"type": "number", "description": "半径像素"},
        "noise": {"type": "integer", "description": "降噪比例"}
      },
      "required": ["amount", "radius"]
    }
  }
]
```

---

### 4️⃣ claude_mcp.yaml

```yaml
name: photoshop
description: 控制 Photoshop 功能的接口
version: 1.0.0
tools:
  - name: smart_sharpen
    description: 应用智能锐化滤镜
    input_schema:
      type: object
      properties:
        amount: { type: number, description: 锐化强度 }
        radius: { type: number, description: 半径像素 }
        noise:  { type: integer, description: 降噪百分比 }
      required: [amount, radius]
```

---

## 五、 generate_artifacts.py

```python
import yaml, json, glob, os

metadata, functions, mcp = {}, [], {"name": "photoshop", "version": "1.0.0", "tools": []}

for file in glob.glob("actions/*.yaml"):
    with open(file, encoding="utf-8") as f:
        actions = yaml.safe_load(f)
        for a in actions:
            name, desc, params = a["name"], a.get("description", ""), a.get("params", {})
            metadata[name] = {
                "category": a.get("category", ""),
                "description": desc,
                "params": list(params.keys())
            }

            fn = {
                "name": name,
                "description": desc,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": list(params.keys())
                }
            }
            for p, typ in params.items():
                fn["parameters"]["properties"][p] = {"type": "number" if typ in ["float", "int"] else "string"}
            functions.append(fn)

            mcp["tools"].append({
                "name": name,
                "description": desc,
                "input_schema": fn["parameters"]
            })

os.makedirs("artifacts", exist_ok=True)
json.dump(metadata, open("artifacts/metadata.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(functions, open("artifacts/openai_functions.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
yaml.safe_dump(mcp, open("artifacts/claude_mcp.yaml", "w", encoding="utf-8"), allow_unicode=True)

print("✅ 已生成 artifacts：metadata.json, openai_functions.json, claude_mcp.yaml")
```

---

## 六、 executor.py

```python
import yaml, json
from photoshop import Session

def load_actions():
    import glob
    actions = {}
    for file in glob.glob("actions/*.yaml"):
        with open(file, encoding="utf-8") as f:
            for a in yaml.safe_load(f):
                actions[a["name"]] = a
    return actions

ACTIONS = load_actions()

def execute_action(ps, name, params):
    if name not in ACTIONS:
        raise ValueError(f"未知动作: {name}")
    template = ACTIONS[name]["code"]
    code = template.format(**params)
    exec(code, {"ps": ps})

def execute_sequence(actions_json):
    actions = json.loads(actions_json)
    with Session() as ps:
        for a in actions:
            execute_action(ps, a["action"], a)
        print("✅ 所有动作执行完成")
```

---

## 七、 LLM Prompt 规范

```
你是 Photoshop 智能控制助手。
你可以从下列动作中选择合适的操作：
{metadata_summary}

用户会输入自然语言命令，请输出严格的 JSON 数组格式。
不要输出解释性文字。
```

**示例输入：**
> “帮我锐化图片并导出成 jpg”

**示例输出：**
```json
[
  {"action": "smart_sharpen", "amount": 120, "radius": 3.0, "noise": 10},
  {"action": "export_as_jpg", "path": "C:/output/result.jpg"}
]
```

---

## 八、 ASR 模块接口

```python
import whisper
model = whisper.load_model("large-v3")
def transcribe_audio(path):
    result = model.transcribe(path, language="zh")
    return result["text"]
```

---

## 九、 执行链路示例

```
[语音输入] → “请帮我锐化一下图片”
   ↓
[ASR] → “请帮我锐化一下图片”
   ↓
[LLM] → JSON 输出 [{"action":"smart_sharpen","amount":100,"radius":2.5,"noise":10}]
   ↓
[Executor] → 调用 photoshop-python-api
   ↓
[完成提示] → “已完成锐化操作”
```

---

## 🔒 十、安全与健壮性

| 风险点 | 措施 |
|--------|------|
| LLM 幻觉输出无效动作 | 限制只能调用 metadata.json 中的动作 |
| 参数缺失或类型错误 | Schema 校验 / MCP 参数验证 |
| 代码注入风险 | 禁止直接执行 LLM 原始代码，只允许模板渲染 |
| 任务中断 | 使用 try/except 包裹每个动作执行 |

---

## 🧭 十一、开发任务清单

| 任务 | 文件 | 说明 |
|------|------|------|
| 1️⃣ 构建 actions/ 目录结构 | `actions/` | 每个 YAML 模块化定义 |
| 2️⃣ 编写 generate_artifacts.py | `generate_artifacts.py` | 自动生成 metadata / schema / MCP |
| 3️⃣ 实现 executor.py | `executor.py` | 执行器核心 |
| 4️⃣ 构建 ASR 模块 | `asr.py` | Jetson 上本地语音识别 |
| 5️⃣ 设计 LLM prompt 模板 | `prompt_template.txt` | 用于 few-shot 提示 |
| 6️⃣ 集成测试 | `run_demo.py` | 语音 → JSON → Photoshop 流程验证 |

---

## ✅ 十二、最终交付成果结构

```
project_root/
 ├─ actions/
 │   ├─ filters.yaml
 │   ├─ layers.yaml
 │   ├─ export.yaml
 │   └─ adjustments.yaml
 ├─ artifacts/
 │   ├─ metadata.json
 │   ├─ openai_functions.json
 │   └─ claude_mcp.yaml
 ├─ generate_artifacts.py
 ├─ executor.py
 ├─ asr.py
 ├─ prompt_template.txt
 ├─ run_demo.py
 └─ README.md
```

---

## ✳️ 十三、后续扩展方向

| 模块 | 方向 |
|------|------|
| LLM 语义增强 | 微调指令理解模型（few-shot 或 SFT） |
| 多语言支持 | 增加 EN / JP / KR 语言包 |
| 多模态交互 | 加入视觉反馈、实时缩略图 |
| Plugin生态 | 发布为 Photoshop 插件或 Claude MCP 插件 |
| 商业接口 | 封装 HTTP API（接入语音设备 / 移动端） |

---

> **说明：**
> - Claude Code 或 GPT 可直接根据本文档结构自动生成代码；
> - 所有输出模块需严格遵守 JSON / YAML / Schema 约束；
> - actions.yaml 为唯一数据源，其他文件均自动生成。

