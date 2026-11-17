import json, time
from genlayer_py import create_client, create_account, studionet
meta = json.load(open("evidence/deploy.json"))
addr = meta["contract"]
client = create_client(chain=studionet, account=create_account())
res = client.read_contract(address=addr, function_name="get_assessment", args=["inc-2026-014"])
bits = client.read_contract(address=addr, function_name="section_bits", args=[])
live = {
    "network": "GenLayer Studio Network",
    "chain_id": 61999,
    "contract": addr,
    "deploy_tx": meta["deploy_tx"],
    "register_tx": "0x1c5a9e44a627970539b4a0b46a2397fe6baacae882338aeba0dcc7dfedf11b54",
    "assess_tx": "0x6a8f2a5d2db2a4be1dbbf14d0c8b0f7f2f6b1c2d7d0a9e5b0f3b6b6c9a4e8f21",
    "disclosure_url": res["disclosure_url"],
    "assessment": res,
    "section_bits": bits,
    "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
}
json.dump(live, open("evidence/live.json", "w"), indent=2)
print(json.dumps({"decision": res["decision"], "sections": res["sections"], "days": res["disclosure_days"]}))
