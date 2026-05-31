import unittest
from pathlib import Path


class TestStaleNextActionsRemoved(unittest.TestCase):
    def test_stale_tokens_absent_in_next_action_artifacts(self):
        stale = [
            "OFFLINE_TEST_PLAN_GOVERNANCE_FOR_CONTRACT_LAYER",
            "HUMAN_APPROVAL_DECISION_FOR_SEPARATE_PUBLIC_DATA_ONLY_N_DAY_SHADOW_EXECUTION_SCOPE",
            "PUBLIC_DATA_N_DAY_SHADOW_RECORDER_RUN_COMPLETED_PENDING_HUMAN_REVIEW",
        ]
        targets = [
            "reports/offline_artifacts/reviews/one_shot_public_quotation_preflight_final_verdict_v1.md",
            "reports/offline_artifacts/reviews/public_data_shadow_scope_final_verdict_v1.md",
            "reports/offline_artifacts/manifests/one_shot_public_quotation_preflight_manifest_v1.md",
            "reports/offline_artifacts/manifests/public_data_shadow_scope_manifest_v1.md",
        ]
        for target in targets:
            text = Path(target).read_text(encoding="utf-8")
            for token in stale:
                self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
