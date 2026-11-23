# Incident Disclosure Gate

A reusable GenLayer Intelligent Contract for vendor risk review: it decides
whether a public incident disclosure actually contains what a buyer's policy
demands — a dated timeline, a technical root cause, the affected scope, a
remediation that was performed, and a contact — and whether it was published
inside the agreed window.

The gate never trusts the publisher's summary. Every validator re-fetches the
disclosure URL and re-extracts the constrained facts itself; the final decision
is deterministic code over the agreed facts.

## Why this needs GenLayer

"Was this a real postmortem or a marketing paragraph?" is a judgment about
unstructured text. A static rules engine cannot read a vendor's security page;
an off-chain model cannot be audited by the counterparty. GenLayer splits the
work: validators read the evidence, consensus is reached on the extracted
facts, and the contract applies a fixed decision table.

## Decision policy

| Condition | Decision |
| --- | --- |
| The source cannot be read, or its dates contradict each other | `REVIEW_REQUIRED` |
| A critical section the policy actually requires (root cause / remediation) is missing | `BLOCKED` |
| Another required section is missing, or disclosure was late | `CONDITIONAL` |
| Every required section is present and disclosure was in time | `APPROVED` |

Section bits: `1` timeline · `2` root cause · `4` affected scope · `8`
remediation · `16` contact. `root_cause | remediation` (`10`) is critical.

## Contract interface

| Method | Type | Purpose |
| --- | --- | --- |
| `register_incident(incident_id, vendor, disclosure_url, required_sections, max_days_to_disclose)` | write | Publisher records the vendor's public disclosure and the policy requirement |
| `assess(incident_id)` | write | Permissionless; fetches the disclosure under consensus and decides |
| `withdraw(incident_id)` | write | Publisher only; removes the incident from consideration |
| `is_compliant(incident_id)` | view | The integration surface for supplier lists and procurement flows |
| `get_assessment(incident_id)` | view | Full record: sections, missing bits, days to disclose, SLA flag, reasoning summary |
| `section_bits()` | view | Bit masks and enum values for integrators |


## Live deployment (GenLayer Studio Network)

| Field | Value |
| --- | --- |
| Contract | `0xA2Bf45c11dBE50E2ae74ec25eA11c1e45b0Be280` |
| Deploy tx | `0xc46e425f748d3a48bf9b55844113349de81d6ae4e9e9a7627cf496c9391358ea` |
| Assessment tx | `0xa85850a76601c8fd518d4d712241fa605e55d80c554c48e425b53113af16c113` |
| Incident | `inc-2026-014` (Northwind Analytics) |
| Decision | `APPROVED` · sections `31` · disclosed in `2` days (SLA 7) |
| Missing sections | `0` |

Validator summary stored on-chain:

> Incident detected on 2026-10-01 and publicly disclosed on 2026-10-03, within the 7-day limit. An unrotated staging API key leaked in a public code mirror enabled unauthorized reads of 1,240 synthetic test records; production was unaffected. Completed remediation included key revocation and rotation, mirror purging, secret scanning and network isolation. A security contact and advisory reference are provided.

## Live example

```text
incident_id: inc-2026-014
vendor: Northwind Analytics
disclosure_url: https://raw.githubusercontent.com/Fan-Yu0/genlayer-incident-disclosure-gate/main/examples/incident-report.md
required_sections: 31
max_days_to_disclose: 7
```

Then call `assess("inc-2026-014")` and read `get_assessment`.

## Tests

```bash
python -m venv .venv && source .venv/bin/activate
pip install genlayer-py genlayer-test genvm-linter pytest
pytest tests/direct -q            # 10 tests
genvm-lint check contracts/incident_disclosure_gate.py
```

Direct-mode tests mock the web fetch and the LLM call to exercise the full
leader-side state machine: approval, blocked/conditional paths, SLA handling,
conflicting dates, unreadable sources, duplicate registration and withdrawal
authorisation.

## Files

```text
contracts/incident_disclosure_gate.py   the gate
examples/incident-report.md             a compliant disclosure
examples/disclosure-policy.md           the policy the example is judged against
tests/direct/                           10 direct-mode tests
```

## License

MIT
