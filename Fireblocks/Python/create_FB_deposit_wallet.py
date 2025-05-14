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


from fireblocks_sdk import FireblocksSDK
import os

# --- Configuration ---
API_KEY = ""  # Replace with your Fireblocks API key
API_SECRET_PATH = "/path/to/your/fireblocks_secret.key"  # Replace with the path to your secret key file
VAULT_NAME = "My ETH Vault" # your vault name
ASSET_ID = "ETH"  # Ethereum asset ID
DEPOSIT_DESC = "Primary ETH deposit address"

# --- Initialize Fireblocks SDK ---
fireblocks = FireblocksSDK(API_SECRET_PATH, API_KEY)

# --- Step 1: Create Vault Account ---
vault_account = fireblocks.create_vault_account(VAULT_NAME, hidden_on_ui=False)
vault_account_id = vault_account["id"]
print(f"Vault Account Created: ID = {vault_account_id}")

# --- Step 2: Add ETH Wallet to Vault Account ---
wallet = fireblocks.create_vault_asset(vault_account_id, ASSET_ID)
print(f"{ASSET_ID} Wallet added to Vault Account {vault_account_id}")

# --- Step 3: Retrieve the deposit address ---
# For Ethereum (account-based), one address is used — just fetch it
addresses = fireblocks.get_deposit_addresses(vault_account_id, ASSET_ID)

if addresses:
    print(f"ETH Deposit Address: {addresses[0]['address']}")
else:
    print("No deposit address found — wallet creation may still be processing.")
