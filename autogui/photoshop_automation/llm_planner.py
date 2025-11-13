"""LLM planner that recommends Photoshop actions based on current state."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from openai import OpenAI

from ..config import APIConfig  # type: ignore
from ..get_photoshop_status import gather_status
from . import get_doc_info, get_layer_info
from .tool_loader import load_tool_tables
from .tool_mapper import match_intent


PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "base_tool_prompt.txt"


def format_tool_summary(tools: Dict[str, Any]) -> str:
    return "\n".join(
        f"- {tid}: {entry.description} (hotkey {entry.hotkey}, variants: {', '.join(entry.variants)})"
        for tid, entry in tools.items()
    )


def format_command_summary(commands: Dict[str, Any]) -> str:
    return "\n".join(
        f"- {cid}: {entry.description} -> {' '.join(entry.flags) or '(default)'} (shortcut {entry.shortcut})"
        for cid, entry in commands.items()
    )


def format_state(status: Dict[str, Any]) -> str:
    doc = get_doc_info.get_document_status(status)
    layer = get_layer_info.get_layer_status(status)
    tool = status.get("tool")
    return json.dumps(
        {
            "tool": tool,
            "document": doc,
            "layer": layer,
            "selection": status.get("selection"),
        },
        ensure_ascii=False,
        indent=2,
    )


class PhotoshopLLMPlanner:
    """High-level planner that mixes heuristic mapping with LLM reasoning."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "qwen-plus",
        base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    ):
        self.tools, self.commands = load_tool_tables()
        prompt = PROMPT_PATH.read_text(encoding="utf-8")
        self.prompt_template = prompt
        key = api_key or os.environ.get("QWEN_API_KEY") or getattr(APIConfig, "QWEN_API_KEY", None)
        if not key:
            raise ValueError("缺少 QWEN_API_KEY，请在环境变量或 config.APIConfig 中配置")
        self.client = OpenAI(api_key=key, base_url=base_url)
        self.model = model

    def build_prompt(self, instruction: str, status: Dict[str, Any]) -> str:
        return self.prompt_template.format(
            TOOL_SUMMARY=format_tool_summary(self.tools),
            COMMAND_SUMMARY=format_command_summary(self.commands),
            STATE_SUMMARY=format_state(status),
            USER_INSTRUCTION=instruction,
        )

    def plan(self, instruction: str) -> Dict[str, Any]:
        status = gather_status()
        prompt = self.build_prompt(instruction, status)

        heuristic = match_intent(instruction, self.tools, self.commands)

        messages = [
            {"role": "system", "content": "你是 Photoshop 自动化助手，请严格返回 JSON。"},
            {"role": "user", "content": prompt},
        ]

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
        llm_decision = json.loads(content.strip())
        if heuristic and llm_decision.get("status") in {"unsupported", "clarify"}:
            llm_decision.setdefault("notes", {})["heuristic_fallback"] = heuristic
        llm_decision["state"] = status
        return llm_decision
