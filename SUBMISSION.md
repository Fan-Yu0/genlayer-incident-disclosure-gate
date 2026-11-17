# Portal submission draft

## Category

Builder -> Intelligent Contract

## Description (English, under 1,000 characters)

Incident Disclosure Gate is a reusable GenLayer primitive for vendor risk review. A publisher registers an incident with the vendor's public disclosure URL, the section mask the buyer's policy requires, and the maximum acceptable disclosure window. Anyone can trigger an assessment. Validators independently fetch the disclosure and extract only the constrained facts - dated timeline, technical root cause, affected scope, remediation performed, contact - plus the days between detection and disclosure. Deterministic contract code sends unreadable or self-contradictory disclosures to human review, blocks disclosures missing a root cause or a remediation, marks late or incomplete disclosures conditional, and approves fully compliant ones. Other contracts consume `is_compliant(incident_id)`. The repository ships source, 10 direct-mode tests, a policy example and a compliant report example.

## Live evidence

- Repository: https://github.com/Fan-Yu0/genlayer-incident-disclosure-gate
- Disclosure judged: examples/incident-report.md
- Policy: examples/disclosure-policy.md
- Contract: `0xA2Bf45c11dBE50E2ae74ec25eA11c1e45b0Be280`
- Deploy transaction: `0xc46e425f748d3a48bf9b55844113349de81d6ae4e9e9a7627cf496c9391358ea`
- Assessment transaction: `0xa85850a76601c8fd518d4d712241fa605e55d80c554c48e425b53113af16c113`
- Live result: decision `APPROVED`, sections `31`, disclosed in `2` days against a 7-day SLA

## Reviewer checklist

- Persistent state with a clear lifecycle (draft / assessed / withdrawn).
- Publisher-only withdrawal; permissionless re-assessment.
- Validator independently re-fetches the disclosure.
- The LLM extracts only constrained facts; the decision stays deterministic.
- Missing or contradictory evidence fails closed (review / block).
- Source, tests and documentation are public.
