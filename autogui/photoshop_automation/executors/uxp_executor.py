"""Placeholder for Photoshop UXP plugin bridge."""

from __future__ import annotations


class UXPExecutor:
    """Bridge to UXP panel or remote plugin (to be implemented)."""

    def trigger(self, payload: dict) -> None:
        raise NotImplementedError("UXP executor 暂未实现")
