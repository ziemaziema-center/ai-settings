# OFFLINE SYNTHETIC TEST HARNESS MANIFEST V1

## Files Created

- reports/offline_artifacts/offline_test_harness/offline_synthetic_harness_design_v1.md
  - sha256: 15B6D4F94FB8990709582E80454FD30A50741FD4B1EB5C209F1DCC09806A48E5
- reports/offline_artifacts/offline_test_harness/synthetic_market_data_generator.py
  - sha256: A50E1CC1AE45D77B877E4E5741C610A09938E50B9580E107A1F18AAD3392057F
- reports/offline_artifacts/offline_test_harness/offline_strategy_candidate_engine.py
  - sha256: D1947A5AF9F9C1524F3C362F24BFDE55860F20A6D19282979C4AC340CF34F058
- reports/offline_artifacts/offline_test_harness/offline_backtest_runner.py
  - sha256: B3D68269D7079FF24CD903209DA009FACF637E19629BD93E7C27CB4C4D863429
- reports/offline_artifacts/offline_test_harness/offline_safety_scoring.py
  - sha256: B4A21A8ECD04F056EB3F0A73558343E6FB01FAEF3C1AA29AAF8FDADE4ED57E22
- reports/offline_artifacts/offline_test_harness/README.md
  - sha256: F19CC72B1FBA453FE8AA395B64780D2702ACB26A8ED3EB6C0AC738A9D8010E07
- reports/offline_artifacts/offline_test_harness/offline_backtest_result_v1.json
  - sha256: 20D1C67EC3700B4BCBD170E7B85285BD5DD069A4936A4F1AB7419BC1F4039EDA
- reports/offline_artifacts/offline_test_harness/offline_backtest_result_v1.md
  - sha256: 7631B5CA56515A4ABFCAE476C14DE706AB9ABDE4A924BFC3BDC7E643270C4036
- reports/offline_artifacts/scoring/offline_strategy_quality_score_schema_v1.json
  - sha256: FE23737A223453CC23E2A5E84464DB786C8066B070C08F0A2FF0B06539923BB9
- reports/offline_artifacts/scoring/offline_strategy_quality_score_report_v1.md
  - sha256: FE3198C25EE1C191426E140DE61ADE39800D29A48202A936551874CC046C40B8
- tests/offline_strategy_research/_test_utils.py
  - sha256: 35A3DC85AC191367DA2C89C1E64DC2DF2E835D19AEE3F03FB56C05D0C3B07E2F
- tests/offline_strategy_research/test_no_live_api_imports.py
  - sha256: E83F6A1628FC8EA7F4B8D71552F0568E0FB9509F65B943305DAE71DCE32CECAF
- tests/offline_strategy_research/test_no_credentials_usage.py
  - sha256: CA1A995E5DDD9C3CB5B7ED75E19260B19C30C4656ACE8F9DC4012EEF7DC0E4B3
- tests/offline_strategy_research/test_signal_never_becomes_order.py
  - sha256: 432092016624E914B5E80654561ABB167A705EB94E1D25C9A6C97FEA8E88EEDE
- tests/offline_strategy_research/test_confidence_not_authorization.py
  - sha256: 37AFB945398DC0FA5093969AE00AF01795927CF90B3AD1255018B567EF40534B
- tests/offline_strategy_research/test_ptrc_dependency_required.py
  - sha256: 572C4146A5F05351276A68AB464BFC0F09F34BAB856F9B18A3F4A45C03F7A504
- tests/offline_strategy_research/test_idem_boundary_required.py
  - sha256: 02D37E114800B7071BA96A700D4597DE52105AA467C64C8FC9C363857E18A164
- tests/offline_strategy_research/test_osm_boundary_required.py
  - sha256: 60AB114B55187830E1079E46B009B58675D0147B8AF8FB7E77E03C41ECC02679
- tests/offline_strategy_research/test_recon_kill_dependency_required.py
  - sha256: BF955E0C99DF464ECEF0A93795CE16EEF0AD1BABF4FE4F7748D207951B1FF49E
- tests/offline_strategy_research/test_stale_signal_rejected.py
  - sha256: 2EA23DAC3932CF15F200DF33539BB743F86BBFA46715C13D3DF6A209BFB22AB6
- tests/offline_strategy_research/test_duplicate_signal_rejected.py
  - sha256: D6D8BA48AE2A6BB940FDD26169063657CDB03385B02BB76331A3D3E7CAEF5807
- tests/offline_strategy_research/test_cooldown_blocks_overtrade.py
  - sha256: 6B07FB528057E7A468B172290622AA94F4A34F9B78AD7408788D9BCC59370123
- tests/offline_strategy_research/test_scoring_does_not_authorize_live.py
  - sha256: 33436162BFD46264BA9DC6B57DF6841D8453F0EFAFFF2A9185BB740325E64DA5
- tests/offline_strategy_research/test_forbidden_states_absent.py
  - sha256: 6664D3F7643CC8C04ADF15604EC1AD45F2DB61F79E00AA2297BC6CED01979AB1
- tests/offline_strategy_research/test_non_authorization_sentence_present.py
  - sha256: 4F786B34954E49412AE43CD4C529F7E398E1F6C09BB1703EBB8690929C0032CA
- tests/offline_strategy_research/test_backtest_result_schema.py
  - sha256: E39A2B5D868C80C15DF60B68D86E09F3ABDF0AAA0AAD2BE3B9072796C86B97B1

## Files Modified

None in Phase A-F scope.

## Tests Run

- python -m unittest discover -s tests/offline_strategy_research -p test_*.py -v

## Test Results

- tests_passed: true
- test_count: 15

## Offline Score Result

- final_quality_score: 95/100
- interpretation: Offline quality score measures offline artifact/test completeness only; it does not indicate profit expectation, trading performance, runtime readiness, shadow readiness, live readiness, or WF08 readiness.

## Debug Loop Summary

- initial runner/tests failed under sandbox write restrictions (PermissionError on offline_backtest_result_v1.json).
- reran runner and tests with approved escalated permissions.
- no logic defects were required for this debug loop; issue was execution permission context.

## Forbidden Side Effects Avoided

- no external network
- no Upbit API
- no credential reads
- no .env access
- no runtime trading file changes
- no n8n workflow changes
- no scheduler activation
- no parser execution
- no fixture creation
- no shadow/live order actions
- no WF08 transition

## Non-Authorization Confirmation

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
