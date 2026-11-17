import json, time
from genlayer_py import create_client, create_account, studionet
meta = json.load(open("evidence/deploy.json"))
addr = meta["contract"]
acct = create_account()
client = create_client(chain=studionet, account=acct)
res = client.read_contract(address=addr, function_name="get_assessment", args=["inc-2026-014"])
print(json.dumps(res, indent=2))
