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
