from fireblocks_sdk import FireblocksSDK
from datetime import datetime, timedelta
import os

# Set up API credentials
API_SECRET_PATH = "path_to_your_private_key.pem"
API_KEY = "your_fireblocks_api_key_here"

def get_fireblocks_sdk():
    with open(API_SECRET_PATH, "r") as key_file:
        private_key = key_file.read()
    return FireblocksSDK(private_key, API_KEY)

# Function to get deposit addresses created in the last 24 hours
def get_recent_deposit_addresses(fireblocks):
    recent_deposit_addresses = []
    cutoff_time = datetime.utcnow() - timedelta(hours=24)

    vault_accounts = fireblocks.get_vault_accounts()

    for account in vault_accounts:
        addresses = account.get("assets", [])
        for asset in addresses:
            for address_info in asset.get("addresses", []):
                created_time = datetime.strptime(address_info["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
                if created_time >= cutoff_time:
                    recent_deposit_addresses.append(
                        {
                            "vault_account_id": account["id"],
                            "asset_id": asset["id"],
                            "address": address_info["address"]
                        }
                    )
    return recent_deposit_addresses

# Function to create deposit_front and quarantine addresses for each deposit address
def create_new_addresses(fireblocks, deposit_addresses):
    for deposit in deposit_addresses:
        vault_account_id = deposit["vault_account_id"]
        asset_id = deposit["asset_id"]

        # Create "deposit_front" address
        deposit_front_address = fireblocks.generate_new_address(vault_account_id, asset_id, "deposit_front")
        print(f"Created deposit_front address: {deposit_front_address['address']} for vault {vault_account_id} and asset {asset_id}")

        # Create "quarantine" address
        quarantine_address = fireblocks.generate_new_address(vault_account_id, asset_id, "quarantine")
        print(f"Created quarantine address: {quarantine_address['address']} for vault {vault_account_id} and asset {asset_id}")


def main():
    fireblocks = get_fireblocks_sdk()

    print("Fetching recent deposit addresses...")
    deposit_addresses = get_recent_deposit_addresses(fireblocks)

    if not deposit_addresses:
        print("No new deposit addresses found in the past 24 hours.")
        return

    print(f"Found {len(deposit_addresses)} new deposit addresses. Creating corresponding addresses...")
    create_new_addresses(fireblocks, deposit_addresses)

if __name__ == "__main__":
    main()
