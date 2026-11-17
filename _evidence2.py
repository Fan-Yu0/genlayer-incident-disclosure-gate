import json, time
from genlayer_py import create_client, create_account, studionet

meta = json.load(open("evidence/deploy.json"))
addr = meta["contract"]
acct = create_account()
client = create_client(chain=studionet, account=acct)

tx = client.write_contract(address=addr, function_name="assess", args=["inc-2026-014"])
r = client.wait_for_transaction_receipt(tx)
hard = []
for e in (r.get("consensus_data") or {}).get("leader_receipt") or []:
    g = e.get("genvm_result") or {}
    code = str(g.get("error_code") or "")
    if str(e.get("execution_result", "")).upper() == "ERROR" and "QUORUM" not in code:
        hard.append(code)
print("assess tx", tx, "hard_errors", hard)
res = client.read_contract(address=addr, function_name="get_assessment", args=["inc-2026-014"])
bits = client.read_contract(address=addr, function_name="section_bits", args=[])
live = {
    "network": "GenLayer Studio Network",
    "chain_id": 61999,
    "contract": addr,
    "deploy_tx": meta["deploy_tx"],
    "assess_tx": tx,
    "assessor": acct.address,
    "disclosure_url": res["disclosure_url"],
    "assessment": res,
    "section_bits": bits,
    "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
}
json.dump(live, open("evidence/live.json", "w"), indent=2)
print(json.dumps({k: res[k] for k in ("decision", "sections", "missing_sections", "disclosure_days", "within_sla", "consistency")}))
