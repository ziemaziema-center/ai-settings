from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


FORBIDDEN_CAPABILITIES = {
    "profit_guarantee": "수익 보장은 불가능하므로 자동 차단",
    "unlimited_auto_buy": "무제한 자동매수는 계좌 리스크가 무한대라 차단",
    "simultaneous_live_orders": "동시 실주문은 중복 노출과 미체결 꼬임 때문에 차단",
    "loss_recovery_guarantee": "손실 복구 확정은 시장 구조상 보장 불가",
    "bypass_live_gates": "게이트 우회는 주문 안전장치를 무력화하므로 차단",
    "market_order": "시장가는 슬리피지 통제가 불가능해 현재 단계에서 차단",
    "auto_cancel": "자동 취소는 재주문 루프 위험 때문에 현재 단계에서 차단",
}


SECTION_WEIGHTS = {
    "safety_failsafe": 12,
    "execution_gates": 12,
    "portfolio_rotation": 10,
    "market_data_quality": 10,
    "strategy_brain": 10,
    "news_reference": 8,
    "learning_loop": 8,
    "observability": 10,
    "finality_recovery": 10,
    "deployment_ops": 10,
}


@dataclass(frozen=True)
class AutonomySection:
    name: str
    weight: int
    score: int
    reason: str


@dataclass(frozen=True)
class AutonomyScorecard:
    total_score: int
    target_score: int
    target_hit: bool
    sections: tuple[AutonomySection, ...]
    blockers: tuple[str, ...] = field(default_factory=tuple)
    allowed_capabilities: tuple[str, ...] = field(default_factory=tuple)
    forbidden_capabilities: tuple[str, ...] = field(default_factory=tuple)
    operating_contract: str = "parallel_scan_single_live_order_until_finality"


def _as_bool(state: dict, key: str) -> bool:
    return bool(state.get(key))


def _score(weight: int, passed: Iterable[bool]) -> int:
    checks = list(passed)
    if not checks:
        return 0
    return int(round(weight * (sum(1 for item in checks if item) / len(checks))))


def build_autonomy_scorecard(state: dict, target_score: int = 95) -> AutonomyScorecard:
    requested_forbidden = tuple(sorted(set(state.get("requested_capabilities") or ()) & FORBIDDEN_CAPABILITIES.keys()))
    blockers = [FORBIDDEN_CAPABILITIES[key] for key in requested_forbidden]

    sections = (
        AutonomySection(
            "safety_failsafe",
            SECTION_WEIGHTS["safety_failsafe"],
            _score(
                SECTION_WEIGHTS["safety_failsafe"],
                [
                    _as_bool(state, "no_market_orders"),
                    _as_bool(state, "no_auto_cancel"),
                    _as_bool(state, "secret_safe"),
                    _as_bool(state, "system_stop_supported"),
                ],
            ),
            "시장가/자동취소/비밀노출/시스템스톱 안전장치",
        ),
        AutonomySection(
            "execution_gates",
            SECTION_WEIGHTS["execution_gates"],
            _score(
                SECTION_WEIGHTS["execution_gates"],
                [
                    _as_bool(state, "helper_live_sell_gate"),
                    _as_bool(state, "helper_live_buy_gate"),
                    _as_bool(state, "execution_lock"),
                    _as_bool(state, "one_order_at_a_time"),
                ],
            ),
            "helper live gate, execution lock, 단일 실주문 원칙",
        ),
        AutonomySection(
            "portfolio_rotation",
            SECTION_WEIGHTS["portfolio_rotation"],
            _score(
                SECTION_WEIGHTS["portfolio_rotation"],
                [
                    _as_bool(state, "portfolio_cleanup_plan"),
                    _as_bool(state, "parallel_candidate_scan"),
                    _as_bool(state, "staged_slice_size"),
                    _as_bool(state, "core_asset_floor"),
                ],
            ),
            "묶인 알트 정리와 핵심 자산 보호",
        ),
        AutonomySection(
            "market_data_quality",
            SECTION_WEIGHTS["market_data_quality"],
            _score(
                SECTION_WEIGHTS["market_data_quality"],
                [
                    _as_bool(state, "fresh_orderbook_required"),
                    _as_bool(state, "spread_cap_required"),
                    _as_bool(state, "maker_limit_required"),
                    _as_bool(state, "open_order_clear_required"),
                ],
            ),
            "호가 신선도, 스프레드, 메이커 지정가, 미체결 확인",
        ),
        AutonomySection(
            "strategy_brain",
            SECTION_WEIGHTS["strategy_brain"],
            _score(
                SECTION_WEIGHTS["strategy_brain"],
                [
                    _as_bool(state, "brain_v4_1"),
                    _as_bool(state, "scalping_shadow_layer"),
                    _as_bool(state, "buy_candidate_gate"),
                    _as_bool(state, "sell_candidate_gate"),
                ],
            ),
            "Brain v4.1, 단타 후보, 매수/매도 후보 게이트",
        ),
        AutonomySection(
            "news_reference",
            SECTION_WEIGHTS["news_reference"],
            _score(
                SECTION_WEIGHTS["news_reference"],
                [
                    _as_bool(state, "daily_news_digest"),
                    _as_bool(state, "credible_sources"),
                    _as_bool(state, "news_reference_only"),
                    _as_bool(state, "defensive_news_blocks_buy"),
                ],
            ),
            "뉴스는 참고층이며 직접 주문 트리거가 아님",
        ),
        AutonomySection(
            "learning_loop",
            SECTION_WEIGHTS["learning_loop"],
            _score(
                SECTION_WEIGHTS["learning_loop"],
                [
                    _as_bool(state, "winning_trade_learning"),
                    _as_bool(state, "loss_case_review"),
                    _as_bool(state, "fee_slippage_review"),
                    _as_bool(state, "no_profit_based_gate_bypass"),
                ],
            ),
            "승리 패턴 학습은 검증된 가중치로만 반영",
        ),
        AutonomySection(
            "observability",
            SECTION_WEIGHTS["observability"],
            _score(
                SECTION_WEIGHTS["observability"],
                [
                    _as_bool(state, "state_json"),
                    _as_bool(state, "events_jsonl"),
                    _as_bool(state, "reports_written"),
                    _as_bool(state, "sanitized_telemetry"),
                ],
            ),
            "상태, 이벤트, 보고서, 민감정보 제거 텔레메트리",
        ),
        AutonomySection(
            "finality_recovery",
            SECTION_WEIGHTS["finality_recovery"],
            _score(
                SECTION_WEIGHTS["finality_recovery"],
                [
                    _as_bool(state, "finality_check"),
                    _as_bool(state, "lock_release_on_done_cancel"),
                    _as_bool(state, "stop_on_wait_watch_unknown"),
                    _as_bool(state, "open_order_count_verified"),
                ],
            ),
            "체결 완료/취소만 다음 단계 허용",
        ),
        AutonomySection(
            "deployment_ops",
            SECTION_WEIGHTS["deployment_ops"],
            _score(
                SECTION_WEIGHTS["deployment_ops"],
                [
                    _as_bool(state, "remote_bounded_workspace"),
                    _as_bool(state, "tmux_runner"),
                    _as_bool(state, "tests_passed"),
                    _as_bool(state, "secret_scan_passed"),
                ],
            ),
            "EC2 bounded workspace, tmux runner, 테스트, 시크릿 스캔",
        ),
    )

    total = sum(section.score for section in sections)
    if blockers:
        total = min(total, target_score - 1)

    allowed = (
        "parallel_read_only_scan",
        "single_live_limit_order_after_helper_gate",
        "staged_capital_rotation",
        "daily_news_reference",
        "bounded_self_improvement",
        "finality_based_lock_release",
    )
    return AutonomyScorecard(
        total_score=total,
        target_score=target_score,
        target_hit=total >= target_score and not blockers,
        sections=sections,
        blockers=tuple(blockers),
        allowed_capabilities=allowed,
        forbidden_capabilities=tuple(f"{key}: {FORBIDDEN_CAPABILITIES[key]}" for key in sorted(FORBIDDEN_CAPABILITIES)),
    )


def scorecard_to_dict(card: AutonomyScorecard) -> dict:
    return {
        "total_score": card.total_score,
        "target_score": card.target_score,
        "target_hit": card.target_hit,
        "operating_contract": card.operating_contract,
        "sections": [
            {"name": section.name, "weight": section.weight, "score": section.score, "reason": section.reason}
            for section in card.sections
        ],
        "blockers": list(card.blockers),
        "allowed_capabilities": list(card.allowed_capabilities),
        "forbidden_capabilities": list(card.forbidden_capabilities),
    }


def default_live_autonomy_state() -> dict:
    return {
        "no_market_orders": True,
        "no_auto_cancel": True,
        "secret_safe": True,
        "system_stop_supported": True,
        "helper_live_sell_gate": True,
        "helper_live_buy_gate": True,
        "execution_lock": True,
        "one_order_at_a_time": True,
        "portfolio_cleanup_plan": True,
        "parallel_candidate_scan": True,
        "staged_slice_size": True,
        "core_asset_floor": True,
        "fresh_orderbook_required": True,
        "spread_cap_required": True,
        "maker_limit_required": True,
        "open_order_clear_required": True,
        "brain_v4_1": True,
        "scalping_shadow_layer": True,
        "buy_candidate_gate": True,
        "sell_candidate_gate": True,
        "daily_news_digest": True,
        "credible_sources": True,
        "news_reference_only": True,
        "defensive_news_blocks_buy": True,
        "winning_trade_learning": True,
        "loss_case_review": True,
        "fee_slippage_review": True,
        "no_profit_based_gate_bypass": True,
        "state_json": True,
        "events_jsonl": True,
        "reports_written": True,
        "sanitized_telemetry": True,
        "finality_check": True,
        "lock_release_on_done_cancel": True,
        "stop_on_wait_watch_unknown": True,
        "open_order_count_verified": True,
        "remote_bounded_workspace": True,
        "tmux_runner": True,
        "tests_passed": True,
        "secret_scan_passed": True,
    }
