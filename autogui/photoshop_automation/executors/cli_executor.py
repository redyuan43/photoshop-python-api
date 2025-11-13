"""CLI executor that shells out to photoshop_hotkey_best.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class CLIExecutor:
    """Execute photoshop_hotkey_best.py with given arguments."""

    def __init__(self, script_path: Optional[Path] = None):
        default = Path(__file__).resolve().parents[2] / "photoshop_hotkey_best.py"
        self.script_path = script_path or default

    def run(self, args: List[str]) -> subprocess.CompletedProcess:
        if not self.script_path.exists():
            raise FileNotFoundError(f"找不到脚本 {self.script_path}")
        command = [sys.executable, str(self.script_path)] + args
        return subprocess.run(command, capture_output=True, text=True)
