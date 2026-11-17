# Incident INC-2026-014 — Public Disclosure

**Vendor:** Northwind Analytics
**Severity:** High
**Status:** Resolved

## Timeline

| Date | Event |
| --- | --- |
| 2026-10-01 09:12 UTC | Anomalous read volume detected on the staging API |
| 2026-10-01 11:40 UTC | Incident declared; staging credentials revoked |
| 2026-10-02 08:00 UTC | Root cause confirmed |
| 2026-10-03 17:30 UTC | Public disclosure published (2 days after detection) |

## Root cause

A staging API key had been committed to a public code mirror in 2025 and was
never rotated. An external party used the leaked key to replay read requests
against the staging dataset. Production credentials and production data were
not reachable from the staging environment.

## Affected scope

- Northwind Analytics staging API (`staging.api.northwind.example`)
- 1,240 synthetic test records; no customer production data
- No impact on the production API, billing or authentication services

## Remediation

- Staging key rotated and old key permanently disabled on 2026-10-01 11:40 UTC
- Public mirror purged and secret scanning enabled on all repositories
- Staging environment isolated behind a separate network boundary
- Post-incident review completed on 2026-10-05

## Contact

Security contact: security@northwind.example
Advisory reference: NWSA-2026-014
