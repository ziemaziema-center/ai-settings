"""Dry-run PTRC evaluator."""

from __future__ import annotations

from typing import Dict


def evaluate_ptrc(candidate: Dict[str, object], *, kill_active: bool, recon_drift: bool, clock_skew: bool) -> Dict[str, object]:
    if kill_active:
        return {"status": "PTRC_REJECTED", "reason": "kill_active"}
    if recon_drift:
        return {"status": "PTRC_REJECTED", "reason": "recon_drift"}
    if clock_skew:
        return {"status": "PTRC_REJECTED", "reason": "clock_skew"}
    return {"status": "PTRC_ELIGIBLE", "reason": "all_local_checks_passed"}
