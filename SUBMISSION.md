# Portal submission draft

## Category

Builder -> Intelligent Contract

## Description (English, under 1,000 characters)

Incident Disclosure Gate is a reusable GenLayer primitive for vendor risk review. A publisher registers an incident with the vendor's public disclosure URL, the section mask the buyer's policy requires, and the maximum acceptable disclosure window. Anyone can trigger an assessment. Validators independently fetch the disclosure and extract only the constrained facts - dated timeline, technical root cause, affected scope, remediation performed, contact - plus the days between detection and disclosure. Deterministic contract code sends unreadable or self-contradictory disclosures to human review, blocks disclosures missing a root cause or a remediation, marks late or incomplete disclosures conditional, and approves fully compliant ones. Other contracts consume `is_compliant(incident_id)`. The repository ships source, 10 direct-mode tests, a policy example and a compliant report example.

## Live evidence

- Repository: https://github.com/Fan-Yu0/genlayer-incident-disclosure-gate
- Disclosure judged: examples/incident-report.md
- Policy: examples/disclosure-policy.md

## Reviewer checklist

- Persistent state with a clear lifecycle (draft / assessed / withdrawn).
- Publisher-only withdrawal; permissionless re-assessment.
- Validator independently re-fetches the disclosure.
- The LLM extracts only constrained facts; the decision stays deterministic.
- Missing or contradictory evidence fails closed (review / block).
- Source, tests and documentation are public.
