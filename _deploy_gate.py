import json, os, time
from genlayer_py import create_client, create_account, studionet

acct = create_account()
print("account", acct.address)
client = create_client(chain=studionet, account=acct)
code = open("contracts/incident_disclosure_gate.py", "rb").read()
tx = client.deploy_contract(code=code, args=[])
r = client.wait_for_transaction_receipt(tx)
addr = (r.get("data") or {}).get("contract_address")
print("contract", addr, "tx", tx)
json.dump({"account": acct.address, "contract": addr, "deploy_tx": tx}, open("evidence/deploy.json", "w"), indent=2)
