import json, time, urllib.request
from genlayer_py import create_client, create_account, studionet

URL = "https://raw.githubusercontent.com/Fan-Yu0/genlayer-incident-disclosure-gate/master/examples/incident-report.md"
print("raw status", urllib.request.urlopen(URL, timeout=30).status)

meta = json.load(open("evidence/deploy.json"))
addr = meta["contract"]
acct = create_account()
client = create_client(chain=studionet, account=acct)

def wait(tx):
    r = client.wait_for_transaction_receipt(tx)
    for e in (r.get("consensus_data") or {}).get("leader_receipt") or []:
        if str(e.get("execution_result", "")).upper() == "ERROR":
            raise RuntimeError(json.dumps(e.get("genvm_result", {}), default=str)[:600])
    return r

tx1 = client.write_contract(address=addr, function_name="register_incident",
                            args=["inc-2026-014", "Northwind Analytics", URL, 31, 7])
wait(tx1)
print("registered", tx1)
started = time.time()
tx2 = client.write_contract(address=addr, function_name="assess", args=["inc-2026-014"])
wait(tx2)
print("assessed", tx2, "in", int(time.time()-started), "s")
res = client.read_contract(address=addr, function_name="get_assessment", args=["inc-2026-014"])
print(json.dumps(res, indent=2)[:900])
out = {"network": "GenLayer Studio Network", "chain_id": 61999, "contract": addr,
       "deploy_tx": meta["deploy_tx"], "publisher": acct.address,
       "register_tx": tx1, "assess_tx": tx2, "disclosure_url": URL,
       "assessment": res, "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
json.dump(out, open("evidence/live.json", "w"), indent=2)
