#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Natural-language Photoshop tool selector powered by Qwen.

Workflow:
  1. Load tool metadata from docs/autogui/TOOLS_MAPPING.md
  2. Ask Qwen LLM to pick the best --tool / variant for the user request
  3. Execute photoshop_hotkey_best.py (and optional --tool-cycle) to switch tools
  4. Run get_current_tool.py to confirm the final tool
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

from openai import OpenAI


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from config import APIConfig  # type: ignore
except Exception:  # pylint: disable=broad-except
    APIConfig = None  # type: ignore


OTHER_ACTIONS = {
    "reset": {"args": [], "description": "复位工具 (Alt+W, K, R)"},
    "layer_move": {"args": ["--layer-move"], "description": "上下移动当前图层 (Ctrl+{, Ctrl+})"},
    "layer_up": {"args": ["--layer-up"], "description": "图层向上移动 (Ctrl+})"},
    "layer_down": {"args": ["--layer-down"], "description": "图层向下移动 (Ctrl+{)"},
    "selection_up": {"args": ["--selection-up"], "description": "选区向上移动 (Ctrl+方向键)"},
    "selection_down": {"args": ["--selection-down"], "description": "选区向下移动"},
    "selection_left": {"args": ["--selection-left"], "description": "选区向左移动"},
    "selection_right": {"args": ["--selection-right"], "description": "选区向右移动"},
    "select_all": {"args": ["--select-all"], "description": "全选 (Ctrl+A)"},
    "deselect": {"args": ["--deselect"], "description": "取消选区 (Ctrl+D)"},
    "invert": {"args": ["--invert"], "description": "反选 (Ctrl+Shift+I)"},
    "duplicate": {"args": ["--duplicate"], "description": "复制图层 (Ctrl+J)"},
    "file_new": {"args": ["--file-new"], "description": "新建文档 (Ctrl+N)"},
    "file_open": {"args": ["--file-open"], "description": "打开文档 (Ctrl+O)"},
    "file_save": {"args": ["--file-save"], "description": "保存当前文档 (Ctrl+S)"},
    "file_save_as": {"args": ["--file-save-as"], "description": "另存为 (Ctrl+Shift+S)"},
    "export_as": {"args": ["--export-as"], "description": "导出为... (Ctrl+Alt+Shift+W)"},
    "file_close": {"args": ["--file-close"], "description": "关闭当前文档 (Ctrl+W)"},
    "file_close_all": {"args": ["--file-close-all"], "description": "关闭所有文档 (Ctrl+Alt+W)"},
    "undo": {"args": ["--undo"], "description": "撤销 (Ctrl+Z)"},
}


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "autogui" / "TOOLS_MAPPING.md"
HOTKEY_SCRIPT = Path(__file__).resolve().parent / "photoshop_hotkey_best.py"
GET_TOOL_SCRIPT = Path(__file__).resolve().parent / "get_current_tool.py"


def parse_tool_table() -> Dict[str, Dict[str, List[str]]]:
    """Parse docs/autogui/TOOLS_MAPPING.md table into a structured dict."""
    text = DOC_PATH.read_text(encoding="utf-8")
    rows = []
    capture = False
    for line in text.splitlines():
        if line.strip().startswith("| `move`"):
            capture = True
        if not capture:
            continue
        if not line.strip():
            break
        if line.startswith("| ---"):
            continue
        if line.startswith("| `"):
            rows.append(line)

    mapping = {}
    for line in rows:
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        tool_id = cells[0].strip("` ")
        hotkey = cells[1]
        description = cells[2]
        variants = [
            name.strip().strip("`")
            for name in cells[3].split(",")
            if name.strip()
        ]
        mapping[tool_id] = {
            "hotkey": hotkey,
            "description": description,
            "variants": variants or [tool_id],
        }
    if not mapping:
        raise RuntimeError(f"无法从 {DOC_PATH} 解析工具表")
    return mapping


def build_tool_summary(mapping: Dict[str, Dict[str, List[str]]]) -> str:
    lines = []
    for key, data in mapping.items():
        desc = data["description"]
        variants = ", ".join(data["variants"])
        lines.append(
            f"- {key} (hotkey {data['hotkey']}): {desc}. "
            f"Photoshop internal names: {variants}"
        )
    return "\n".join(lines)


def build_action_summary(mapping: Dict[str, Dict[str, List[str]]]) -> str:
    lines = []
    for key, data in mapping.items():
        args = " ".join(data["args"]) if data["args"] else "(默认模式)"
        lines.append(f"- {key}: {data['description']}；CLI: {args}")
    return "\n".join(lines)


class QwenToolPlanner:
    """LLM client that picks Photoshop actions/tools and maintains dialog history."""

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str,
        tool_summary: str,
        tool_ids: List[str],
        action_summary: str,
        action_ids: List[str],
    ):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.tool_summary = tool_summary
        self.tool_ids = tool_ids
        self.action_summary = action_summary
        self.action_ids = action_ids
        self.system_prompt = f"""
你是 Photoshop 快捷键规划助手。可用工具如下：
{self.tool_summary}

除工具外，还可调用以下快捷命令：
{self.action_summary}

请在以下 JSON 模板内回应：
{{
  "status": "ok" | "clarify" | "unsupported",
  "action_type": "tool" | "command",
  "action_id": "<tool_id_or_command_id_or_null>",
  "target_variant": "<currentTool_name_if_tool_else_null>",
  "reason": "解释为什么选择该工具或命令",
  "clarification": "若 status=clarify 时要补充的问题"
}}

规则：
- 当 action_type="tool" 时，action_id 必须来自 {self.tool_ids}。
- 当 action_type="command" 时，action_id 必须来自 {self.action_ids}。
- target_variant 仅在 action_type="tool" 时需要；若用户明确指定某个 Photoshop 内部工具名（如 quickSelectTool）请填写，否则设为 null。
- 如果需求不适用工具栏，请返回 status="unsupported"。
- 如果需要用户补充信息，返回 status="clarify" 并填写 clarification。
- 只输出 JSON，不要附加说明。
""".strip()
        self.history: List[Dict[str, str]] = []

    def reset_dialog(self):
        self.history = []

    def add_user_message(self, text: str):
        self.history.append({"role": "user", "content": text})

    def choose_tool(self) -> Dict[str, str]:
        if not self.history:
            raise RuntimeError("未提供任何用户输入")

        messages = [{"role": "system", "content": self.system_prompt}] + self.history
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
        )

        content = response.choices[0].message.content.strip()
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        self.history.append({"role": "assistant", "content": content})
        return json.loads(content)


def run_photoshop_command(args: List[str]) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        [sys.executable, str(HOTKEY_SCRIPT)] + args,
        capture_output=True,
        text=True,
    )
    return proc


def confirm_current_tool() -> str:
    proc = subprocess.run(
        [sys.executable, str(GET_TOOL_SCRIPT)],
        capture_output=True,
        text=True,
    )
    tool_name = None
    for line in proc.stdout.splitlines():

        if ":" in line and ("当前激活工具" in line or "Current tool" in line):
            tool_name = line.split(":")[-1].strip()
            break
    return tool_name or "未知"


def main():
    parser = argparse.ArgumentParser(description="自然语言调用 Photoshop 工具（Qwen 驱动）")
    parser.add_argument("--text", help="直接提供一次性需求文本；未提供则交互式输入")
    parser.add_argument("--api-key", help="Qwen API key（默认取 QWEN_API_KEY 环境变量或 config.APIConfig）")
    parser.add_argument("--model", default="qwen-plus", help="模型名称，默认 qwen-plus")
    parser.add_argument("--base-url", default="https://dashscope.aliyuncs.com/compatible-mode/v1", help="API Base URL")
    parser.add_argument("--dry-run", action="store_true", help="只打印 LLM 结果，不真正执行 Photoshop 命令")
    args = parser.parse_args()

    mapping = parse_tool_table()
    tool_summary = build_tool_summary(mapping)
    api_key = args.api_key or os.environ.get("QWEN_API_KEY")
    if not api_key and APIConfig:
        try:
            api_key = APIConfig.QWEN_API_KEY
        except Exception:  # pylint: disable=broad-except
            api_key = None
    if not api_key:
        print("[FAIL] 请通过 --api-key 或环境变量 QWEN_API_KEY 提供通义千问密钥")
        sys.exit(1)

    planner = QwenToolPlanner(
        api_key=api_key,
        model=args.model,
        base_url=args.base_url,
        tool_summary=tool_summary,
        tool_ids=list(mapping.keys()),
        action_summary=build_action_summary(OTHER_ACTIONS),
        action_ids=list(OTHER_ACTIONS.keys()),
    )

    def handle_request(text: str):
        try:
            planner.add_user_message(text)
            decision = planner.choose_tool()
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[FAIL] LLM 调用失败: {exc}")
            return

        print("[LLM 输出]")
        print(json.dumps(decision, ensure_ascii=False, indent=2))

        status = decision.get("status")
        if status == "unsupported":
            print("[INFO] 请求不在工具栏范围内。")
            planner.reset_dialog()
            return
        if status == "clarify":
            print(f"[INFO] 需要继续追问: {decision.get('clarification')}")
            return
        if status != "ok":
            print("[FAIL] 未知状态，停止执行。")
            planner.reset_dialog()
            return

        action_type = decision.get("action_type") or ("tool" if decision.get("action_id") in mapping else "command")
        action_id = decision.get("action_id") or decision.get("tool_id")

        if action_type == "tool":
            if not action_id or action_id not in mapping:
                print("[FAIL] LLM 返回的 tool_id 无效")
                planner.reset_dialog()
                return
            target_variant = decision.get("target_variant")
            variants = mapping[action_id]["variants"]
            try:
                variant_index = variants.index(target_variant) if target_variant else 0
            except ValueError:
                print(f"[WARN] 变体 {target_variant} 不在列表中，将使用默认工具。")
                variant_index = 0

            if args.dry_run:
                print(f"[DRY-RUN] 将执行 --tool {action_id} + {variant_index} 次 --tool-cycle")
                return

            result = run_photoshop_command(["--tool", action_id])
            if result.returncode != 0:
                print("[FAIL] 执行主切换失败：")
                print(result.stdout)
                print(result.stderr)
                planner.reset_dialog()
                return

            if variant_index > 0:
                for idx in range(variant_index):
                    cycle_proc = run_photoshop_command(["--tool-cycle", action_id])
                    if cycle_proc.returncode != 0:
                        print(f"[FAIL] 第 {idx+1} 次循环失败：")
                        print(cycle_proc.stdout)
                        print(cycle_proc.stderr)
                        planner.reset_dialog()
                        return

            final_tool = confirm_current_tool()
            print(f"[OK] 已切换到 {action_id} (目标变体: {target_variant or '默认'})")
            print(f"[INFO] Photoshop 报告当前工具：{final_tool}")
            planner.reset_dialog()
            return

        if action_type == "command":
            if not action_id or action_id not in OTHER_ACTIONS:
                print("[FAIL] LLM 返回的 command 无效")
                planner.reset_dialog()
                return

            args_list = OTHER_ACTIONS[action_id]["args"]
            if args.dry_run:
                print(f"[DRY-RUN] 将执行命令 {action_id}: {' '.join(args_list) or '(默认)'}")
                return

            result = run_photoshop_command(args_list)
            if result.returncode != 0:
                print("[FAIL] 命令执行失败：")
                print(result.stdout)
                print(result.stderr)
                planner.reset_dialog()
                return

            print(f"[OK] 已执行命令 {action_id}")
            planner.reset_dialog()
            return

        print("[FAIL] action_type 未知")
        planner.reset_dialog()

    planner.reset_dialog()
    if args.text:
        handle_request(args.text)
    else:
        print("=== Photoshop 工具 LLM 调度 ===")
        print("输入自然语言描述（输入 quit 退出）\n")
        while True:
            try:
                user_text = input("> ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n[退出]")
                break
            if not user_text:
                continue
            if user_text.lower() in {"quit", "exit", "q"}:
                print("[退出]")
                break
            handle_request(user_text)


if __name__ == "__main__":
    main()
