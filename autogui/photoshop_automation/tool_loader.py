"""Utilities for loading tool/command mappings from TOOLS_MAPPING.md."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAPPING_PATH = PROJECT_ROOT / "docs" / "autogui" / "TOOLS_MAPPING.md"


@dataclass(frozen=True)
class ToolEntry:
    tool_id: str
    hotkey: str
    description: str
    variants: List[str]


@dataclass(frozen=True)
class CommandEntry:
    command_id: str
    flags: List[str]
    description: str
    shortcut: str


def _split_table_line(line: str) -> List[str]:
    """Split a Markdown table line into clean cells."""
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return [cell for cell in cells if cell]


def _parse_tool_table(lines: List[str]) -> Dict[str, ToolEntry]:
    entries: Dict[str, ToolEntry] = {}
    for raw in lines:
        if not raw.startswith("| `"):
            continue
        cells = _split_table_line(raw)
        if len(cells) < 4:
            continue
        tool_id = cells[0].strip("`")
        hotkey = cells[1]
        description = cells[2]
        variants = [variant.strip().strip("`") for variant in cells[3].split(",")]
        entries[tool_id] = ToolEntry(tool_id, hotkey, description, [v for v in variants if v])
    return entries


def _parse_command_table(lines: List[str]) -> Dict[str, CommandEntry]:
    entries: Dict[str, CommandEntry] = {}
    for raw in lines:
        if not raw.startswith("|"):
            continue
        cells = _split_table_line(raw)
        if len(cells) < 4 or cells[0].startswith("---"):
            continue
        command_id = cells[0]
        flags = [flag for flag in cells[1].split() if flag]
        description = cells[2]
        shortcut = cells[3]
        entries[command_id] = CommandEntry(command_id, flags, description, shortcut)
    return entries


def _read_sections(text: str) -> Tuple[List[str], List[str]]:
    tool_lines: List[str] = []
    command_lines: List[str] = []
    current = None
    for line in text.splitlines():
        if line.startswith("| CLI flag"):
            current = "tools"
        elif line.startswith("| Action ID"):
            current = "commands"
        elif not line.strip():
            current = None
        if current == "tools":
            tool_lines.append(line)
        elif current == "commands":
            command_lines.append(line)
    return tool_lines, command_lines


@lru_cache(maxsize=4)
def load_tool_tables(mapping_path: Optional[Path] = None) -> Tuple[Dict[str, ToolEntry], Dict[str, CommandEntry]]:
    """Load tools/commands from TOOLS_MAPPING.md."""
    path = mapping_path or DEFAULT_MAPPING_PATH
    if not path.exists():
        raise FileNotFoundError(f"无法找到映射文件: {path}")

    text = path.read_text(encoding="utf-8")
    tool_lines, command_lines = _read_sections(text)
    tools = _parse_tool_table(tool_lines)
    commands = _parse_command_table(command_lines)
    if not tools:
        raise ValueError("工具映射表为空，请检查 TOOLS_MAPPING.md")
    return tools, commands
