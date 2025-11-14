#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Natural-language Photoshop tool selector powered by Qwen.

The workflow:
  1. Parse docs/autogui/TOOLS_MAPPING.md for toolbar metadata
  2. Ask an LLM (Qwen compatible) to choose the best action/tool
  3. Execute the action via hotkey/python/DOM/JS runner
  4. Confirm the resulting state (current tool, etc.)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from autogui.actions.loader import load_actions, format_actions_summary
from autogui.executors import (
    run_hotkey as exec_run_hotkey,
    run_python_script as exec_run_python_script,
    run_do_javascript as exec_run_do_javascript,
    run_dom_api as exec_run_dom_api,
)

try:
    from config import APIConfig  # type: ignore
except Exception:  # pylint: disable=broad-except
    APIConfig = None  # type: ignore

AUTOGUI_DIR = Path(__file__).resolve().parent
DOC_PATH = ROOT / "docs" / "autogui" / "TOOLS_MAPPING.md"
HOTKEY_SCRIPT = AUTOGUI_DIR / "photoshop_hotkey_best.py"
GET_TOOL_SCRIPT = AUTOGUI_DIR / "get_current_tool.py"
REGISTRY_FILE = AUTOGUI_DIR / "actions" / "actions.yaml"
LOG_DIR = AUTOGUI_DIR / "logs"
DEFAULT_SCREENSHOT_DIR = AUTOGUI_DIR / "shots"

VARIANT_HINTS = {
    "type": {
        "typeCreateOrEditTool": "Horizontal type",
        "typeVerticalCreateOrEditTool": "Vertical type",
        "typeCreateMaskTool": "Horizontal type mask",
        "typeVerticalCreateMaskTool": "Vertical type mask",
    }
}

OTHER_ACTIONS: Dict[str, Dict[str, Any]] = {
    "reset": {"args": [], "description": "Reset toolbar (Alt+W, K, R)"},
    "layer_move": {"args": ["--layer-move"], "description": "Nudge layer up/down (Ctrl+{ / Ctrl+})"},
    "layer_up": {"args": ["--layer-up"], "description": "Move layer up (Ctrl+})"},
    "layer_down": {"args": ["--layer-down"], "description": "Move layer down (Ctrl+{)"},
    "selection_up": {"args": ["--selection-up"], "description": "Move selection up"},
    "selection_down": {"args": ["--selection-down"], "description": "Move selection down"},
    "selection_left": {"args": ["--selection-left"], "description": "Move selection left"},
    "selection_right": {"args": ["--selection-right"], "description": "Move selection right"},
    "select_all": {"args": ["--select-all"], "description": "Select all (Ctrl+A)"},
    "deselect": {"args": ["--deselect"], "description": "Deselect (Ctrl+D)"},
    "invert": {"args": ["--invert"], "description": "Invert selection (Ctrl+Shift+I)"},
    "duplicate": {"args": ["--duplicate"], "description": "Duplicate layer (Ctrl+J)"},
    "file_new": {"args": ["--file-new"], "description": "New document (Ctrl+N)"},
    "file_open": {"args": ["--file-open"], "description": "Open document (Ctrl+O)"},
    "file_save": {"args": ["--file-save"], "description": "Save (Ctrl+S)"},
    "file_save_as": {"args": ["--file-save-as"], "description": "Save as (Ctrl+Shift+S)"},
    "export_as": {"args": ["--export-as"], "description": "Export As (Ctrl+Alt+Shift+W)"},
    "file_close": {"args": ["--file-close"], "description": "Close document (Ctrl+W)"},
    "file_close_all": {"args": ["--file-close-all"], "description": "Close all documents"},
    "undo": {"args": ["--undo"], "description": "Undo (Ctrl+Z)"},
    "screenshot": {
        "runner": "script",
        "script": AUTOGUI_DIR / "screenshot_photoshop.py",
        "description": "Capture the current Photoshop window",
        "output_dir": DEFAULT_SCREENSHOT_DIR,
        "filename_template": "photoshop_{timestamp}.png",
    },
}


def parse_tool_table() -> Dict[str, Dict[str, List[str]]]:
    text = DOC_PATH.read_text(encoding="utf-8")
    rows: List[str] = []
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

    mapping: Dict[str, Dict[str, List[str]]] = {}
    for line in rows:
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        tool_id = cells[0].strip("` ")
        hotkey = cells[1]
        description = cells[2]
        variants = [name.strip().strip("`") for name in cells[3].split(",") if name.strip()]
        mapping[tool_id] = {
            "hotkey": hotkey,
            "description": description,
            "variants": variants or [tool_id],
        }
    if not mapping:
        raise RuntimeError(f"Unable to parse tool mapping from {DOC_PATH}")
    return mapping


def build_tool_summary(mapping: Dict[str, Dict[str, List[str]]]) -> str:
    lines: List[str] = []
    for key, data in mapping.items():
        desc = data["description"]
        variant_names: List[str] = []
        for variant in data["variants"]:
            hint = VARIANT_HINTS.get(key, {}).get(variant)
            variant_names.append(f"{variant} ({hint})" if hint else variant)
        variant_text = ", ".join(variant_names)
        lines.append(
            f"- {key} (hotkey {data['hotkey']}): {desc}. "
            f"Photoshop internal names: {variant_text}"
        )
    return "\n".join(lines)


def build_legacy_action_summary(mapping: Dict[str, Dict[str, Any]]) -> str:
    lines = []
    for key, data in mapping.items():
        runner = data.get("runner", "hotkey")
        if runner == "script":
            script_path = Path(str(data.get("script", ""))).name
            template = data.get("filename_template", "output.png")
            cli = f"python {script_path} --out {template}"
        else:
            args_list = data.get("args", [])
            cli = " ".join(args_list) if args_list else "(default mode)"
        lines.append(f"- {key}: {data['description']} | CLI: {cli}")
    return "\n".join(lines)


def save_dialog_history(history: List[Dict[str, str]], decision: Dict[str, Any], reason: str, extra: Optional[Dict[str, Any]] = None) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dialog_{timestamp}_{uuid4().hex[:6]}.json"
    payload = {
        "timestamp": datetime.now().isoformat(),
        "reason": reason,
        "decision": decision,
        "history": history,
        "extra": extra or {},
    }
    out_path = LOG_DIR / filename
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


class QwenToolPlanner:
    """LLM client that keeps dialog context and summaries."""

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str,
        tool_summary: str,
        tool_ids: List[str],
        structured_summary: str,
        legacy_summary: str,
        action_ids: List[str],
        registry_actions: Dict[str, Any],
    ):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.tool_summary = tool_summary
        self.tool_ids = tool_ids
        self.structured_summary = structured_summary
        self.legacy_summary = legacy_summary
        self.action_ids = action_ids
        self.registry_actions = registry_actions
        self.system_prompt = f"""
你是 Photoshop 快捷键规划助手。可用工具如下：
{self.tool_summary}

结构化命令（支持 hotkey / python_script / dom_api / JSX）：
{self.structured_summary or '(无)'}

兼容命令（legacy CLI）：
{self.legacy_summary}

提示：历史对话中可能包含“上一操作”摘要，如果用户没有重新说明，可参考这些参数决定默认值。

请仅输出 JSON：
{{
  "status": "ok" | "clarify" | "unsupported",
  "action_type": "tool" | "command",
  "action_id": "<tool_id_or_command_id>",
  "target_variant": "<currentTool name if tool else null>",
  "params": {{}}
}}

规则：
- 当 action_type="tool" 时，action_id 必须来自 {self.tool_ids}
- 当 action_type="command" 时，action_id 可以来自结构化注册表或兼容表
- target_variant 只有在切工具时需要；如果用户说“竖排文字”，请选择 vertical variant
- 需要补充信息时返回 status="clarify" 并给出问题
- 若需求不适用工具栏，返回 status="unsupported"
- 颜色类参数请输出 #RRGGBB 或 [R,G,B] 数值，不要只写“蓝色”“red”
- 不透明度/百分比请转换为 0-100 的数值
- 只输出 JSON，不要附加解释
""".strip()
        self.history: List[Dict[str, str]] = []

    def reset_dialog(self) -> None:
        self.history = []

    def add_user_message(self, text: str) -> None:
        self.history.append({"role": "user", "content": text})

    def choose_tool(self) -> Dict[str, Any]:
        if not self.history:
            raise RuntimeError("No user input provided")
        messages = [{"role": "system", "content": self.system_prompt}] + self.history
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        self.history.append({"role": "assistant", "content": content})
        return json.loads(content)


def bring_photoshop_to_front() -> None:
    """Use Photoshop COM bridge to bring the app to the foreground before sending hotkeys."""
    try:
        from photoshop import Session  # type: ignore
    except Exception:  # pylint: disable=broad-except
        return
    try:
        with Session() as ps:  # type: ignore
            ps.app.bringToFront()
    except Exception:  # pylint: disable=broad-except
        pass


def run_photoshop_command(args: List[str]) -> subprocess.CompletedProcess[Any]:
    bring_photoshop_to_front()
    return subprocess.run([sys.executable, str(HOTKEY_SCRIPT)] + args, capture_output=True, text=True)


def run_python_helper(script_path: Path, args: Optional[List[str]] = None) -> subprocess.CompletedProcess[Any]:
    return subprocess.run([sys.executable, str(script_path)] + (args or []), capture_output=True, text=True)


def confirm_current_tool() -> str:
    proc = subprocess.run([sys.executable, str(GET_TOOL_SCRIPT)], capture_output=True, text=True)
    for line in proc.stdout.splitlines():
        if ":" in line and ("当前激活工具" in line or "Current tool" in line):
            return line.split(":" )[-1].strip()
    return "未知"


def main() -> None:
    parser = argparse.ArgumentParser(description="自然语言调用 Photoshop 工具（Qwen 驱动）")
    parser.add_argument("--text", help="直接提供一次性需求文本；未提供则进入交互输入")
    parser.add_argument("--api-key", help="Qwen API key（默认取 QWEN_API_KEY 或 config.APIConfig）")
    parser.add_argument("--model", default="qwen-plus", help="模型名称，默认 qwen-plus")
    parser.add_argument("--base-url", default="https://dashscope.aliyuncs.com/compatible-mode/v1", help="API Base URL")
    parser.add_argument("--dry-run", action="store_true", help="只打印 LLM 结果，不执行命令")
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

    registry_actions = load_actions(REGISTRY_FILE if REGISTRY_FILE.exists() else None)
    structured_summary = format_actions_summary(registry_actions) if registry_actions else ""
    legacy_summary = build_legacy_action_summary(OTHER_ACTIONS)
    action_ids = list(OTHER_ACTIONS.keys()) + list(registry_actions.keys())

    planner = QwenToolPlanner(
        api_key=api_key,
        model=args.model,
        base_url=args.base_url,
        tool_summary=tool_summary,
        tool_ids=list(mapping.keys()),
        structured_summary=structured_summary,
        legacy_summary=legacy_summary,
        action_ids=action_ids,
        registry_actions=registry_actions,
    )

    context_messages: List[Dict[str, str]] = []

    def remember_context(text: str) -> None:
        if not text:
            return
        context_messages.append({"role": "assistant", "content": text})
        if len(context_messages) > 6:
            context_messages.pop(0)

    def handle_request(text: str) -> None:
        try:
            planner.history = list(context_messages)
            planner.add_user_message(text)
            decision = planner.choose_tool()
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[FAIL] LLM 调用失败: {exc}")
            planner.reset_dialog()
            return

        print("[LLM 输出]")
        print(json.dumps(decision, ensure_ascii=False, indent=2))

        status = decision.get("status")
        action_id = decision.get("action_id") or decision.get("tool_id")

        def describe_missing(action: Any, provided: Dict[str, Any]) -> List[str]:
            missing: List[str] = []
            for key, spec in (action.params or {}).items():
                if not isinstance(spec, dict):
                    continue
                if spec.get("required"):
                    value = provided.get(key)
                    if value in (None, "", []):
                        missing.append(spec.get("description") or key)
            return missing

        def finalize_dialog(reason: str, extra: Optional[Dict[str, Any]] = None) -> None:
            try:
                save_dialog_history(planner.history, decision, reason, extra)
            except Exception as log_exc:  # pylint: disable=broad-except
                print(f"[WARN] 无法写入对话日志: {log_exc}")
            planner.reset_dialog()

        if status == "unsupported":
            print("[INFO] 请求不在工具栏范围内")
            finalize_dialog("unsupported", {"status": status})
            return
        if status == "clarify":
            auto_continue = False
            msg = decision.get("clarification")
            if action_id and action_id in planner.registry_actions:
                action = planner.registry_actions[action_id]
                missing = describe_missing(action, decision.get("params") or {})
                if not missing and decision.get("params"):
                    print("[INFO] LLM 请求澄清但参数已足够，自动继续执行。")
                    status = "ok"
                    decision["status"] = "ok"
                    auto_continue = True
                elif missing:
                    msg = msg or f"请补充参数: {', '.join(missing)}"
            if status != "ok":
                if not msg:
                    msg = "需要更多信息，请补充参数。"
                print(f"[INFO] 需要继续追问: {msg}")
                return
        if status != "ok":
            print("[FAIL] 未知状态，停止执行")
            finalize_dialog("invalid_status", {"status": status})
            return

        action_type = decision.get("action_type") or ("tool" if (decision.get("action_id") in mapping) else "command")

        if action_type == "tool":
            if not action_id or action_id not in mapping:
                print("[FAIL] LLM 返回的 tool_id 无效")
                finalize_dialog("tool_invalid_id", {"action_id": action_id})
                return
            target_variant = decision.get("target_variant")
            variants = mapping[action_id]["variants"]
            try:
                variant_index = variants.index(target_variant) if target_variant else 0
            except ValueError:
                print(f"[WARN] 变体 {target_variant} 不存在，将使用默认工具")
                variant_index = 0

            if args.dry_run:
                print(f"[DRY-RUN] 将执行 --tool {action_id} 并循环 {variant_index} 次")
                finalize_dialog("tool_dry_run", {"action_id": action_id, "variant_index": variant_index})
                return

            result = run_photoshop_command(["--tool", action_id])
            if result.returncode != 0:
                print("[FAIL] 主切换失败：")
                print(result.stdout)
                print(result.stderr)
                finalize_dialog("tool_switch_failed", {"action_id": action_id, "returncode": result.returncode})
                return

            if variant_index > 0:
                for idx in range(variant_index):
                    cycle_proc = run_photoshop_command(["--tool-cycle", action_id])
                    if cycle_proc.returncode != 0:
                        print(f"[FAIL] 第 {idx + 1} 次循环失败：")
                        print(cycle_proc.stdout)
                        print(cycle_proc.stderr)
                        finalize_dialog("tool_cycle_failed", {"action_id": action_id, "cycle_index": idx + 1})
                        return

            final_tool = confirm_current_tool()
            print(f"[OK] 已切换到 {action_id} (变体: {target_variant or '默认'})")
            print(f"[INFO] Photoshop 当前工具: {final_tool}")
            remember_context(f"上一操作：切换工具 {action_id}（变体 {target_variant or '默认'}），当前工具 {final_tool}")
            finalize_dialog("tool_success", {"action_id": action_id, "final_tool": final_tool})
            return

        if action_type == "command":
            registry = planner.registry_actions
            params = decision.get("params") or {}
            if registry and action_id in registry:
                action = registry[action_id]
                if args.dry_run:
                    print(f"[DRY-RUN] 将执行结构化命令 {action_id} (executor={action.executor}) params={params}")
                    finalize_dialog("command_dry_run", {"action_id": action_id, "executor": action.executor, "params": params})
                    return
                if action.executor == "hotkey":
                    res = exec_run_hotkey(action.flags)
                    if not res.ok:
                        print("[FAIL] 热键命令执行失败")
                        print(res.stdout)
                        print(res.stderr)
                        finalize_dialog("command_hotkey_failed", {"action_id": action_id, "returncode": res.return_code})
                        return
                    print(f"[OK] 已执行命令 {action_id}")
                    remember_context(f"上一命令：{action_id} (hotkey) 已执行")
                    finalize_dialog("command_hotkey_success", {"action_id": action_id})
                    return
                if action.executor == "python_script":
                    script_rel = action.script or ""
                    script_path = AUTOGUI_DIR / script_rel
                    context = dict(action.default_params)
                    context.update(params)
                    context.setdefault("timestamp", datetime.now().strftime("%Y%m%d_%H%M%S"))
                    needs_output = any("{output_path" in token for token in action.args_template) or "output_path" in context or "out" in params
                    if needs_output:
                        if params.get("out"):
                            output_path = Path(str(params["out"]))
                            if not output_path.is_absolute():
                                output_path = AUTOGUI_DIR / output_path
                        else:
                            output_dir = context.get("output_dir") or DEFAULT_SCREENSHOT_DIR
                            output_dir = Path(output_dir)
                            if not output_dir.is_absolute():
                                output_dir = AUTOGUI_DIR / output_dir
                            output_dir.mkdir(parents=True, exist_ok=True)
                            filename_template = context.get("filename_template") or f"{action_id}_{context['timestamp']}.png"
                            filename = filename_template.format(timestamp=context["timestamp"], action=action_id)
                            output_path = output_dir / filename
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        context["output_path"] = str(output_path)
                    arg_list = [segment.format(**context) for segment in action.args_template]
                    res = exec_run_python_script(script_path, arg_list)
                    if not res.ok:
                        print("[FAIL] 脚本执行失败")
                        print(res.stdout)
                        print(res.stderr)
                        finalize_dialog("command_script_failed", {"action_id": action_id, "returncode": res.return_code, "args": arg_list})
                        return
                    if res.stdout.strip():
                        print(res.stdout.strip())
                    remember_context(
                        f"上一命令：{action_id} (python_script) 参数 {json.dumps(context, ensure_ascii=False, default=str)}"
                    )
                    finalize_dialog("command_script_success", {"action_id": action_id, "args": arg_list, "context": context})
                    return
                if action.executor == "do_javascript":
                    merged = dict(action.default_params)
                    merged.update(params)
                    res = exec_run_do_javascript(action.template or "", merged)
                    if not res.ok:
                        print("[FAIL] JSX 执行失败")
                        print(res.stderr)
                        finalize_dialog("command_jsx_failed", {"action_id": action_id, "error": res.stderr})
                        return
                    print(f"[OK] 已执行 JSX 动作 {action_id}")
                    remember_context(
                        f"上一命令：{action_id} (JSX) 参数 {json.dumps(merged, ensure_ascii=False, default=str)}"
                    )
                    finalize_dialog("command_jsx_success", {"action_id": action_id})
                    return
                if action.executor == "dom_api":
                    if not action.callable_path:
                        print("[FAIL] 未配置 DOM callable")
                        finalize_dialog("command_dom_missing_callable", {"action_id": action_id})
                        return
                    res = exec_run_dom_api(action.callable_path, params)
                    if not res.ok:
                        print("[FAIL] DOM 操作执行失败")
                        if res.stderr:
                            print(res.stderr)
                        finalize_dialog("command_dom_failed", {"action_id": action_id, "error": res.stderr})
                        return
                    result_data = res.extra.get("result") if res.extra else None
                    if result_data:
                        print(json.dumps(result_data, ensure_ascii=False, indent=2))
                    remember_context(
                        f"上一命令：{action_id} 执行成功，参数 {json.dumps(params, ensure_ascii=False, default=str)}"
                    )
                    finalize_dialog("command_dom_success", {"action_id": action_id, "result": result_data})
                    return
                print(f"[FAIL] 未知执行器: {action.executor}")
                finalize_dialog("command_unknown_executor", {"action_id": action_id})
                return

            if not action_id or action_id not in OTHER_ACTIONS:
                print("[FAIL] 未找到命令 (结构化或兼容)")
                finalize_dialog("command_not_found", {"action_id": action_id})
                return

            entry = OTHER_ACTIONS[action_id]
            runner = entry.get("runner", "hotkey")
            if runner == "script":
                script_path = entry.get("script")
                if not script_path:
                    print("[FAIL] 未配置脚本路径")
                    finalize_dialog("legacy_script_missing", {"action_id": action_id})
                    return
                timestamp = datetime.now().strftime(entry.get("timestamp_format", "%Y%m%d_%H%M%S"))
                filename_template = entry.get("filename_template", f"{action_id}_{timestamp}.png")
                try:
                    filename = filename_template.format(timestamp=timestamp, action=action_id)
                except KeyError:
                    filename = filename_template
                out_dir = Path(entry.get("output_dir") or DEFAULT_SCREENSHOT_DIR)
                out_dir.mkdir(parents=True, exist_ok=True)
                out_path = out_dir / filename
                cmd_args = ["--out", str(out_path)]
                if args.dry_run:
                    print(f"[DRY-RUN] 将执行脚本 {Path(script_path).name} --out {out_path}")
                    finalize_dialog("legacy_script_dry_run", {"action_id": action_id})
                    return
                res = exec_run_python_script(Path(script_path), cmd_args)
                if not res.ok:
                    print("[FAIL] 脚本执行失败")
                    print(res.stdout)
                    print(res.stderr)
                    finalize_dialog("legacy_script_failed", {"action_id": action_id, "returncode": res.return_code})
                    return
                print(f"[OK] 已保存输出 {out_path}")
                remember_context(f"上一命令：{action_id} (脚本) 输出 {out_path}")
                finalize_dialog("legacy_script_success", {"action_id": action_id, "output": str(out_path)})
                return

            args_list = entry.get("args", [])
            if args.dry_run:
                print(f"[DRY-RUN] 将执行命令 {action_id}: {' '.join(args_list) or '(default)'}")
                finalize_dialog("legacy_command_dry_run", {"action_id": action_id, "args": args_list})
                return
            result = run_photoshop_command(args_list)
            if result.returncode != 0:
                print("[FAIL] 命令执行失败")
                print(result.stdout)
                print(result.stderr)
                finalize_dialog("legacy_command_failed", {"action_id": action_id, "returncode": result.returncode})
                return
                print(f"[OK] 已执行命令 {action_id}")
                remember_context(f"上一命令：{action_id} 已执行（legacy 模式）")
                finalize_dialog("legacy_command_success", {"action_id": action_id})
                return

        print("[FAIL] action_type 未知")
        finalize_dialog("unknown_action_type", {"action_type": action_type, "action_id": action_id})

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
