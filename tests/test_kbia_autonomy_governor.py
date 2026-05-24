from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy.kbia_autonomy_governor import build_autonomy_scorecard, default_live_autonomy_state, scorecard_to_dict


def test_default_live_autonomy_state_hits_target_score():
    card = build_autonomy_scorecard(default_live_autonomy_state())
    data = scorecard_to_dict(card)
    assert data["total_score"] == 100
    assert data["target_hit"] is True
    assert data["operating_contract"] == "parallel_scan_single_live_order_until_finality"


def test_forbidden_capability_blocks_target_hit_even_when_system_is_otherwise_strong():
    state = default_live_autonomy_state()
    state["requested_capabilities"] = ["profit_guarantee", "simultaneous_live_orders"]
    card = build_autonomy_scorecard(state)
    data = scorecard_to_dict(card)
    assert data["total_score"] == 94
    assert data["target_hit"] is False
    assert any("수익 보장" in blocker for blocker in data["blockers"])
    assert any("동시 실주문" in blocker for blocker in data["blockers"])


def test_missing_finality_and_observability_reduces_score_below_target():
    state = default_live_autonomy_state()
    state["finality_check"] = False
    state["lock_release_on_done_cancel"] = False
    state["events_jsonl"] = False
    state["reports_written"] = False
    card = build_autonomy_scorecard(state)
    data = scorecard_to_dict(card)
    assert data["total_score"] < 95
    finality = [section for section in data["sections"] if section["name"] == "finality_recovery"][0]
    observability = [section for section in data["sections"] if section["name"] == "observability"][0]
    assert finality["score"] == 5
    assert observability["score"] == 5


if __name__ == "__main__":
    test_default_live_autonomy_state_hits_target_score()
    test_forbidden_capability_blocks_target_hit_even_when_system_is_otherwise_strong()
    test_missing_finality_and_observability_reduces_score_below_target()
    print("KBIA_AUTONOMY_GOVERNOR_TESTS_PASS")
