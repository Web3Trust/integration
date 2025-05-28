#!/usr/bin/env python3
"""
Web3Firewall Client Script
==========================

This script is part of the official integration suite for Web3Firewall clients.
It allows you to submit Ethereum transactions to the Web3Firewall API for
broadcast-time risk evaluation.

You must have:
- An active Web3Firewall account
- A valid Web3Firewall bearer token

Visit https://web3firewall.xyz or contact sales@web3firewall.xyz for access.

Author: Web3Firewall Engineering
License: Apache 2.0
"""

import requests
import json

# === CONFIGURATION (EDIT BEFORE USE) ===
WEB3FIREWALL_API_URL = "https://api.web3firewall.io/api/v1/policy/event"
WEB3FIREWALL_TOKEN = "YOUR_WEB3FIREWALL_BEARER_TOKEN_HERE"

# === SAMPLE TX PAYLOAD (REPLACE OR INTEGRATE INTO YOUR PIPELINE) ===
transaction_payload = {
    "kind": "transaction:broadcasted",
    "datetime": "2025-02-20T11:38:19.718Z",
    "data": {
        "network": "eth",
        "from": "0x61ed4B62E03798305818607C7160B2AbFF15cFeD",
        "to": "0xd756bF764ad08E0B67E7466FFA7A52D788935344",
        "nonce": 16469,
        "value": "1000000000",
        "data": "0x",
        "gasLimit": "0x76c0",
        "gasPrice": "0x9184e72a000",
        "r": "0x...",
        "s": "0x...",
        "yParityOrV": "0x1"
    }
}

# === WEB3FIREWALL API INTERACTION ===
def evaluate_transaction(tx: dict):
    headers = {
        "Authorization": f"Bearer {WEB3FIREWALL_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(WEB3FIREWALL_API_URL, headers=headers, json=tx)
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        print(f"[Web3Firewall] Request failed: {e}")
        return
    except ValueError:
        print("[Web3Firewall] Failed to parse JSON response:", response.text)
        return

    action = result.get("actionToTake", "").lower()
    event_id = result.get("eventId", "N/A")

    print(f"[Web3Firewall] Action: {action.upper()}")
    print(f"[Web3Firewall] Event ID: {event_id}")

    if action == "needsapproval":
        print("[Web3Firewall] Manual review required. Check dashboard or use this Event ID to poll later.")
    elif action in ("allow", "deny"):
        print("[Web3Firewall] Automated decision returned.")
    else:
        print(f"[Web3Firewall] Unrecognized action: {action}")

# === MAIN ENTRYPOINT ===
if __name__ == "__main__":
    evaluate_transaction(transaction_payload)
