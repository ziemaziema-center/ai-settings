"""Dry-run ALERT component."""

from __future__ import annotations


def build_alert(event_name: str, critical: bool) -> dict:
    return {
        "event": event_name,
        "severity": "CRITICAL" if critical else "HIGH",
        "state": "ALERT_REQUIRED",
        "alert_required": True,
    }
