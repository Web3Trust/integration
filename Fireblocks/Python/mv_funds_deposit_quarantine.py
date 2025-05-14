"""
----------------------------------------------------------------------------
 Web3Firewall™ - Blockchain Risk & Compliance Intelligence Platform
----------------------------------------------------------------------------

 Title     : Fireblocks Internal Fund Movement Script (Deposit ➔ Quarantine)
 Version   : 1.0
 Language  : Python 3.x
 Author    : Web3Firewall Engineering Team
 License   : Proprietary - Web3Firewall™ All Rights Reserved

 Description:
 This script connects to Fireblocks™ via its official SDK,
 moves the full available balance from a vault account's deposit
 address to a quarantine address using tagged address selection.

 Disclaimer:
 Usage of this script is provided "AS IS" without warranty of any kind.
 Web3Firewall™, its affiliates, and contributors accept no liability
 for any damages, data loss, financial exposure, or regulatory breaches
 arising from the use, misuse, or inability to use this code.

 You are solely responsible for reviewing, testing, and ensuring
 that this code meets your compliance, security, and operational needs.

----------------------------------------------------------------------------
 (C) 2025 Web3Firewall™. All Rights Reserved.
 https://web3firewall.ai
----------------------------------------------------------------------------
"""

from fireblocks_sdk import FireblocksSDK, TransferPeerPath, TransactionArguments
import os
from datetime import datetime

# CONFIG
API_SECRET_PATH = "path_to_your_private_key.pem"
API_KEY = "your_fireblocks_api_key_here"
VAULT_ACCOUNT_ID = "123456"  # Replace with your Fireblocks Vault account ID
ASSET_ID = "ETH"             # Replace with your desired asset, e.g., "ETH", "USDC"

def get_fireblocks_sdk():
    with open(API_SECRET_PATH, "r") as key_file:
        private_key = key_file.read()
    return FireblocksSDK(private_key, API_KEY)

def get_address_by_tag(fireblocks, vault_id, asset_id, tag):
    vault_accounts = fireblocks.get_vault_accounts(vault_id)
    for asset in vault_accounts.get("assets", []):
        if asset["id"] == asset_id:
            for address_info in asset.get("addressInfos", []):
                if address_info.get("tag") == tag:
                    return address_info.get("address")
    return None

def get_available_balance(fireblocks, vault_id, asset_id, address):
    balance = fireblocks.get_vault_account_asset(vault_id, asset_id)
    return balance.get("available"), balance.get("total")

def move_funds(fireblocks, vault_id, asset_id, source_tag, destination_tag):
    # Get addresses
    from_address = get_address_by_tag(fireblocks, vault_id, asset_id, source_tag)
    to_address = get_address_by_tag(fireblocks, vault_id, asset_id, destination_tag)

    if not from_address or not to_address:
        print(f"Missing address: deposit={from_address}, quarantine={to_address}")
        return

    available_balance, _ = get_available_balance(fireblocks, vault_id, asset_id, from_address)
    if float(available_balance) <= 0:
        print("No available funds to transfer.")
        return

    # Create transfer
    tx = fireblocks.create_transaction(
        asset_id=asset_id,
        source=TransferPeerPath(vault_account_id=vault_id),
        destination=TransferPeerPath(vault_account_id=vault_id),
        amount=str(available_balance),
        note=f"Auto-transfer to quarantine on {datetime.utcnow().isoformat()}",
        tx_type="INTERNAL",
        source_address=from_address,
        destination_address=to_address,
        extra_parameters=TransactionArguments()
    )

    print(f"Transfer initiated. TX ID: {tx['id']}, Status: {tx['status']}")

def main():
    fireblocks = get_fireblocks_sdk()
    move_funds(fireblocks, VAULT_ACCOUNT_ID, ASSET_ID, "deposit", "quarantine")

if __name__ == "__main__":
    main()
