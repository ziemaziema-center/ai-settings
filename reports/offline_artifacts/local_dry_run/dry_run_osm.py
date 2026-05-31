"""Dry-run OSM component."""

from __future__ import annotations


def persist_intent(intent_id: str) -> dict:
    return {
        "intent_id": intent_id,
        "osm_state": "OSM_INTENT_PERSISTED",
        "persisted": True,
        "submitted": False,
        "persisted_before_submitted": True,
    }
