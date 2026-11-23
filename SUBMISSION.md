# Portal submission draft

## Category

Builder -> Intelligent Contract

## Description (English, under 1,000 characters)

Incident Disclosure Gate is a reusable GenLayer primitive for vendor risk review. A publisher registers an incident with the vendor's public disclosure URL, the section mask the buyer's policy requires, and the maximum acceptable disclosure window. Anyone can trigger an assessment. Validators independently fetch the disclosure and extract only the constrained facts - dated timeline, technical root cause, affected scope, remediation performed, contact - plus the days between detection and disclosure. Deterministic contract code sends unreadable or self-contradictory disclosures to human review, blocks disclosures missing a critical section the policy actually requires, marks late or incomplete disclosures conditional, and approves fully compliant ones. Other contracts consume `is_compliant(incident_id)`. The repository ships source, 16 direct-mode tests, a policy example and a compliant report example.

## Live evidence

- Repository: https://github.com/Fan-Yu0/genlayer-incident-disclosure-gate
- Disclosure judged: examples/incident-report.md
- Policy: examples/disclosure-policy.md
- Contract: `0x3751A413e21B9D0B6f54950244B1DF297de091Dd`
- Deploy transaction: `0x023e363113a4923f444c3cb44cd165b3d7a7b43158b64dbf0625bba30aa9e433`
- Assessment transaction: `0x64abf7466ec25c2591b3525aae3e6908e93a620666c5628f3b72c76a48e607d9`
- Live result: decision `APPROVED`, sections `31`, disclosed in `2` days against a 7-day SLA

## Reviewer checklist

- Persistent state with a clear lifecycle (draft / assessed / withdrawn).
- Publisher-only withdrawal; permissionless re-assessment.
- Validator independently re-fetches the disclosure.
- The LLM extracts only constrained facts; the decision stays deterministic.
- Missing or contradictory evidence fails closed (review / block).
- Source, tests and documentation are public.

## Response to Steward review (2026-11-23)

Both points from the review request are fixed, covered by focused tests, and live on a freshly deployed instance.

1. **Critical-section blocking is now requirement-scoped.**
   `assess` computes `missing_critical = required & CRITICAL_SECTIONS & ~present` and blocks only when that is non-zero.
   A policy that requires root cause alone is no longer blocked because remediation is absent; a policy that requires
   remediation still blocks when remediation is absent.

2. **Unreadable sources require the complete fail-closed result.**
   The validator now normalizes the leader payload and accepts an unreadable source only when the whole fail-closed
   triple is present: `sections == 0`, `consistency == "insufficient"`, and `disclosure_days == 36500` (the SLA
   sentinel). A bare zero section mask, a `consistent` claim, a missing sentinel, or a malformed payload is rejected.
   `_leader_matches` also returns false for malformed leader payloads on the readable path.

### Tests added

- `test_policy_requiring_only_root_cause_ignores_missing_remediation` - one-critical-section policy approves.
- `test_policy_requiring_only_remediation_blocks_when_that_section_is_missing` - that same section missing blocks.
- `test_missing_required_critical_blocks_while_optional_critical_is_ignored` - required critical absent still blocks.
- `test_fail_closed_leader_requires_the_complete_payload` - zero mask alone, wrong consistency and missing sentinel all fail.
- `test_unreadable_source_rejects_non_fail_closed_and_malformed_leaders` - mirrors the validator path for unreadable sources.
- `test_leader_comparison_rejects_malformed_payloads` - malformed leader payloads never match.

`python -m pytest tests -q` -> **16 passed**.
