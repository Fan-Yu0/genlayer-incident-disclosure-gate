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
| A required critical section (root cause / remediation) is missing | `BLOCKED` |
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
