#!/usr/bin/env python3
"""
Web3Firewall Pre-Broadcast Simulation
=====================================

This script allows clients to simulate an Ethereum transaction before it is broadcast.
It submits a `transaction:prebroadcast` payload to the Web3Firewall risk engine.

Requires:
- A valid Web3Firewall bearer token
- A structured transaction input

For access, visit: https://web3firewall.xyz or contact: sales@web3firewall.xyz

License: Apache 2.0
"""

import requests
import json

# === CONFIGURATION (EDIT BEFORE USE) ===
WEB3FIREWALL_API_URL = "https://api.web3firewall.io/api/v1/policy/event"
WEB3FIREWALL_TOKEN = "YOUR_WEB3FIREWALL_BEARER_TOKEN_HERE"

# === TRANSACTION SIMULATION PAYLOAD ===
prebroadcast_payload = {
    "kind": "transaction:prebroadcast",
    "data": {
        "network": "ETH",
        "from": "0x72a5843cc08275C8171E582972Aa42Da8C397B2A",
        "to": "0xA160cdAB225685dA1d56aa342Ad8841c3b53f291",
        "gasLimit": "1",
        "maxFeePerGas": "1",
        "value": "1",
        "maxPriorityFeePerGas": "1",
        "nonce": 1,
        "input": "0x"
    }
}

# === SEND TO WEB3FIREWALL ===
def simulate_prebroadcast(tx: dict):
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
        print("[Web3Firewall] Invalid JSON response:", response.text)
        return

    action = result.get("actionToTake", "").lower()
    event_id = result.get("eventId", "N/A")

    print(f"[Web3Firewall] Action: {action.upper()}")
    print(f"[Web3Firewall] Event ID: {event_id}")

    if action == "needsapproval":
        print("[Web3Firewall] This transaction requires manual review.")
    elif action in ("allow", "deny"):
        print("[Web3Firewall] Automated decision returned.")
    else:
        print(f"[Web3Firewall] Unrecognized action: {action}")

# === MAIN ===
if __name__ == "__main__":
    simulate_prebroadcast(prebroadcast_payload)
