"""Dry-run KILL component."""

from __future__ import annotations

from typing import Dict


def is_kill_active(context: Dict[str, object]) -> bool:
    return bool(context.get("kill_active", False))
