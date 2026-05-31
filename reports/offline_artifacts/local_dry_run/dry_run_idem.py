"""Dry-run IDEM component."""

from __future__ import annotations


class DryRunIdemStore:
    def __init__(self) -> None:
        self._seen = set()

    def prepare(self, client_order_id: str) -> dict:
        if client_order_id in self._seen:
            return {"status": "IDEM_RETRY_BLOCKED", "reason": "duplicate_client_order_id"}
        self._seen.add(client_order_id)
        return {"status": "IDEM_PREPARED", "reason": "client_order_id_reserved"}
