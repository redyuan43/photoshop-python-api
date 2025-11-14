"""Load structured action definitions for autogui.

This loader reads YAML registry files to provide a unified set of actions
that LLMs can discover and invoke. Each action describes:
  - id, display_name, category, executor type
  - flags/script/template for execution
  - synonyms and optional params schema
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


REGISTRY_PATH = Path(__file__).resolve().with_name("actions.yaml")


@dataclass(frozen=True)
class ActionDef:
    action_id: str
    display_name: str
    category: str
    executor: str
    description: str = ""
    flags: List[str] = field(default_factory=list)
    script: Optional[str] = None
    template: Optional[str] = None
    callable_path: Optional[str] = None
    args_template: List[str] = field(default_factory=list)
    synonyms: List[str] = field(default_factory=list)
    default_params: Dict[str, Any] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)


def _normalize_action_id(key: str) -> str:
    return key.strip()


def _coerce_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


@lru_cache(maxsize=2)
def load_actions(registry_path: Optional[Path] = None) -> Dict[str, ActionDef]:
    path = registry_path or REGISTRY_PATH
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    source_actions = (data.get("actions") or {}) if isinstance(data, dict) else {}

    result: Dict[str, ActionDef] = {}
    for key, spec in source_actions.items():
        action_id = _normalize_action_id(str(key))
        display_name = str(spec.get("display_name") or action_id)
        category = str(spec.get("category") or "misc")
        executor = str(spec.get("executor") or "hotkey")
        description = str(spec.get("description") or "")
        flags = _coerce_list(spec.get("flags"))
        script = spec.get("script")
        template = spec.get("template")
        callable_path = spec.get("callable")
        args_template = _coerce_list(spec.get("args_template"))
        synonyms = _coerce_list(spec.get("synonyms"))
        default_params = dict(spec.get("default_params") or {})
        params = dict(spec.get("params") or {})
        result[action_id] = ActionDef(
            action_id=action_id,
            display_name=display_name,
            category=category,
            executor=executor,
            description=description,
            flags=flags,
            script=script,
            template=template,
            callable_path=callable_path,
            args_template=args_template,
            synonyms=synonyms,
            default_params=default_params,
            params=params,
        )
    return result


def format_actions_summary(actions: Dict[str, ActionDef]) -> str:
    """Return a human-readable summary grouped by category for prompts."""
    if not actions:
        return "(无可用命令)"
    # Order by category then id
    items = sorted(actions.values(), key=lambda a: (a.category, a.action_id))
    lines: List[str] = []
    current_cat: Optional[str] = None
    for act in items:
        if act.category != current_cat:
            current_cat = act.category
            lines.append(f"\n[{current_cat}]")
        runner = act.executor
        hint = ""
        if runner == "hotkey" and act.flags:
            hint = f" flags={' '.join(act.flags)}"
        elif runner == "python_script" and act.script:
            hint = f" script={act.script}"
        elif runner == "do_javascript" and act.template:
            hint = " jsx=app.doAction(...)"
        elif runner == "dom_api" and act.callable_path:
            hint = f" dom={act.callable_path}"
        lines.append(f"- {act.action_id}: {act.display_name} - {act.description}{hint}")
    return "\n".join(lines).strip()
