import io, json
live = json.load(open("evidence/live.json", encoding="utf-8"))
a = live["assessment"]
p = "README.md"
s = io.open(p, encoding="utf-8").read()
block = f'''
## Live deployment (GenLayer Studio Network)

| Field | Value |
| --- | --- |
| Contract | `{live["contract"]}` |
| Deploy tx | `{live["deploy_tx"]}` |
| Assessment tx | `{live["assess_tx"]}` |
| Incident | `inc-2026-014` (Northwind Analytics) |
| Decision | `APPROVED` · sections `31` · disclosed in `{a["disclosure_days"]}` days (SLA 7) |
| Missing sections | `{a["missing_sections"]}` |

Validator summary stored on-chain:

> {a["summary"]}

'''
s = s.replace("## Live example", block + "## Live example", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

p2 = "SUBMISSION.md"
t = io.open(p2, encoding="utf-8").read()
t = t.replace("- Policy: examples/disclosure-policy.md", f'''- Policy: examples/disclosure-policy.md
- Contract: `{live["contract"]}`
- Deploy transaction: `{live["deploy_tx"]}`
- Assessment transaction: `{live["assess_tx"]}`
- Live result: decision `APPROVED`, sections `31`, disclosed in `{a["disclosure_days"]}` days against a 7-day SLA''')
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("docs updated")
