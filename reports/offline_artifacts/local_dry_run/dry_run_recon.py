"""Dry-run RECON component."""

from __future__ import annotations

from typing import Dict


def detect_recon_drift(context: Dict[str, object]) -> bool:
    return bool(context.get("recon_drift", False))
