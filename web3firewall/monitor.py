"""
------------------------------------------------------------
 Web3Firewall — Ethereum Address Risk Monitor (v1.1)
------------------------------------------------------------

This script checks all transactions sent to a given Ethereum address 
within the past X hours using the Etherscan API and evaluates the risk 
of each transaction using Web3Firewall's real-time threat intelligence API.

INSTRUCTIONS:

1. Set your credentials below.
2. Run from terminal:
    python monitor.py <ethereum_address> <lookback_hours>

3. All transactions are submitted to Web3Firewall for risk assessment.

Get a free Etherscan API key at:
    https://etherscan.io/myapikey

Learn more or upgrade your coverage:
    https://web3firewall.xyz
------------------------------------------------------------
"""

# === SET YOUR API KEYS HERE ===
ETHERSCAN_API_KEY = "YOUR_ETHERSCAN_API_KEY_HERE"
WEB3FIREWALL_TOKEN = "YOUR_WEB3FIREWALL_BEARER_TOKEN_HERE"

# === STATIC CONFIGURATION ===
WEB3FIREWALL_API_URL = "https://api.web3firewall.io/api/v1/policy/event"

# === DO NOT MODIFY BELOW THIS LINE ===

import sys
import requests
from datetime import datetime, timedelta, timezone

def get_recent_transactions(address, cutoff_timestamp):
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY
    }

    try:
        response = requests.get("https://api.etherscan.io/api", params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "1":
            print("No transactions found or API error:", data.get("message"))
            return []

        return [
            tx for tx in data["result"]
            if tx["to"] and tx["to"].lower() == address.lower() and int(tx["timeStamp"]) >= cutoff_timestamp
        ]

    except Exception as e:
        print("Error fetching transactions from Etherscan:", e)
        return []

def send_to_web3firewall(tx):
    tx_time = datetime.utcfromtimestamp(int(tx["timeStamp"])).replace(tzinfo=timezone.utc).isoformat()

    r = tx.get("r", "0x0")
    s = tx.get("s", "0x0")
    v = tx.get("v", "0x0")
    if not str(v).startswith("0x"):
        try:
            v = hex(int(v))
        except Exception:
            v = "0x0"

    body = {
        "kind": "transaction:broadcasted",
        "datetime": tx_time,
        "data": {
            "network": "eth",
            "from": tx["from"],
            "to": tx["to"],
            "nonce": int(tx["nonce"]),
            "value": tx["value"],
            "data": tx["input"],
            "gasLimit": hex(int(tx["gas"])),
            "gasPrice": hex(int(tx["gasPrice"])),
            "r": r,
            "s": s,
            "yParityOrV": v
        }
    }

    headers = {
        "Authorization": f"Bearer {WEB3FIREWALL_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(WEB3FIREWALL_API_URL, json=body, headers=headers)
        response.raise_for_status()
        print(f"{tx['hash']} → Risk Response: {response.json()}")
    except Exception as e:
        print(f"Failed to send {tx['hash']} to Web3Firewall: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python monitor.py <ethereum_address> <lookback_hours>")
        sys.exit(1)

    target_address = sys.argv[1].lower()
    try:
        lookback_hours = int(sys.argv[2])
    except ValueError:
        print("The second argument must be an integer (hours).")
        sys.exit(1)

    cutoff_ts = int((datetime.now(timezone.utc) - timedelta(hours=lookback_hours)).timestamp())

    print(f"Scanning {target_address} for the last {lookback_hours} hours...")

    txs = get_recent_transactions(target_address, cutoff_ts)

    print(f"\nFound {len(txs)} transactions to {target_address}.\n")

    for tx in txs:
        send_to_web3firewall(tx)
