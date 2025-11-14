"""Simple heuristic mapper from natural language to Photoshop tools/commands."""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

from .tool_loader import CommandEntry, ToolEntry


EXTRA_SYNONYMS = {
    "crop": ["裁剪", "剪裁", "裁切"],
    "move": ["移动", "拖拽", "挪动", "对齐"],
    "lasso": ["套索", "抠图", "自由选择"],
    "magic_wand": ["魔棒", "快速选择", "对象选择"],
    "marquee": ["选框", "矩形选框", "椭圆选框"],
    "spot_heal": ["修复", "污点", "补丁", "内容识别"],
    "clone_stamp": ["仿制", "克隆图章"],
    "pen": ["钢笔", "路径绘制"],
    "type": ["文字", "横排文字", "竖排文字", "vertical type", "文字工具"],
    "shape": ["矩形工具", "椭圆工具", "绘制形状"],
    "paint_bucket": ["油漆桶", "填充", "渐变"],
    "eyedropper": ["吸管", "取色", "颜色取样"],
    "hand": ["抓手", "平移画布"],
    "zoom": ["缩放", "放大", "缩小"],
    "selection_up": ["上移选区", "选区上移"],
    "selection_down": ["下移选区"],
    "selection_left": ["左移选区"],
    "selection_right": ["右移选区"],
    "selection_layer_up": ["上一图层", "上一层", "Alt+]", "切换上一层"],
    "selection_layer_down": ["下一图层", "下一层", "Alt+[", "切换下一层"],
    "select_all": ["全选"],
    "deselect": ["取消选区", "取消选择"],
    "invert": ["反选"],
    "duplicate": ["复制图层", "拷贝图层"],
    "file_save": ["保存文件", "保存文档"],
    "file_save_as": ["另存为"],
    "file_open": ["打开文件"],
    "file_new": ["新建文档"],
    "undo": ["撤销"],
    "screenshot": ["截图", "截屏", "屏幕截图", "screenshot", "screen shot", "capture screen", "保存屏幕", "拍一下屏幕"]
}




def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text.lower())


def build_keywords(entry: ToolEntry) -> List[str]:
    base = [entry.tool_id.lower(), entry.description.lower()]
    base.extend(variant.lower() for variant in entry.variants)
    base.extend(EXTRA_SYNONYMS.get(entry.tool_id, []))
    return [kw for kw in base if kw]


def build_command_keywords(entry: CommandEntry) -> List[str]:
    base = [entry.command_id.lower(), entry.description.lower(), entry.shortcut.lower()]
    base.extend(EXTRA_SYNONYMS.get(entry.command_id, []))
    return [kw for kw in base if kw]


def score_entry(text: str, keywords: List[str]) -> int:
    score = 0
    for kw in keywords:
        if kw and kw in text:
            score += len(kw)
    return score


def match_intent(user_text: str, tools: Dict[str, ToolEntry], commands: Dict[str, CommandEntry]) -> Optional[Dict[str, str]]:
    """Return the best guess for the user's intent."""
    norm = normalize(user_text)
    best: Tuple[int, Optional[str], str] = (0, None, "tool")

    for tool_id, entry in tools.items():
        score = score_entry(norm, build_keywords(entry))
        if score > best[0]:
            best = (score, tool_id, "tool")

    for cmd_id, entry in commands.items():
        score = score_entry(norm, build_command_keywords(entry))
        if score > best[0]:
            best = (score, cmd_id, "command")

    if best[0] == 0 or best[1] is None:
        return None
    return {"action_type": best[2], "action_id": best[1], "score": best[0]}
