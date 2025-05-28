# integration

# Web3Firewall Risk Monitor Integrations

This repository contains official scripts, tools, and integration examples for clients of [Web3Firewall](https://web3firewall.xyz) — the real-time risk intelligence platform for blockchain transactions.

## 🛡️ Overview

Web3Firewall empowers financial institutions, VASPs, custodians, protocols, and wallet infrastructure providers to screen and respond to risky blockchain activity before it settles. This repository provides vetted tools to integrate your systems with our API-driven intelligence.

## 📂 Included Scripts

- `monitor.ts`: A TypeScript CLI script that fetches Ethereum transactions to a given address and sends them to Web3Firewall for broadcast-time risk evaluation.
  - Currently uses **Etherscan** as a data source.
  - More data connectors (e.g. Alchemy, Infura, node watchers) will be supported in future scripts.

## 🔐 Access Requirements

To use these tools, you must have:
- An active Web3Firewall account
- Your Web3Firewall bearer token for the `/api/v1/policy/event` endpoint

To request access, contact [sales@web3firewall.xyz](mailto:sales@web3firewall.xyz) or visit [https://web3firewall.xyz](https://web3firewall.xyz).

## 🚀 Usage Example: Ethereum Risk Monitor

```bash
ts-node monitor.ts <ethereum_address> <lookback_hours>
