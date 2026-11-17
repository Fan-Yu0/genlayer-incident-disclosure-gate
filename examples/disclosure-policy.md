# Disclosure policy — vendor risk review

This policy is applied to every incident before a vendor may be re-admitted to
the approved supplier list.

## Required sections

| Bit | Section | Required |
| --- | --- | --- |
| 1 | Timeline with dated events | yes |
| 2 | Root cause (technical) | yes |
| 4 | Affected scope (products / versions / data) | yes |
| 8 | Remediation performed | yes |
| 16 | Security contact or advisory reference | yes |

Required mask: `31`

## Timing

Disclosure must be published within **7 days** of the incident being detected.
Late but complete disclosures are admissible on a conditional basis and require
a documented exception.

## Blocking rules

- A disclosure that does not state a technical root cause is rejected.
- A disclosure that does not state a remediation that was actually performed is
  rejected.
- A disclosure whose dates contradict each other, or that cannot be read, is
  escalated to human review instead of being scored.
