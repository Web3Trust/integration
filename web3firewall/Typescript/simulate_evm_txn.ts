// Web3Firewall Pre-Broadcast Simulation (TypeScript)
// =====================================================
//
// This script simulates a transaction before broadcast by sending it to the
// Web3Firewall API for pre-execution risk evaluation.
//
// Requires:
// - Node.js with axios installed
// - A valid Web3Firewall Bearer Token
//
// To run:
// $ ts-node simulatePrebroadcast.ts

import axios from 'axios';

const WEB3FIREWALL_API_URL = 'https://api.web3firewall.io/api/v1/policy/event';
const WEB3FIREWALL_TOKEN = 'YOUR_WEB3FIREWALL_BEARER_TOKEN_HERE';

// Sample payload (adjust fields as needed)
const prebroadcastPayload = {
  kind: 'transaction:prebroadcast',
  data: {
    network: 'ETH',
    from: '0x72a5843cc08275C8171E582972Aa42Da8C397B2A',
    to: '0xA160cdAB225685dA1d56aa342Ad8841c3b53f291',
    gasLimit: '1',
    maxFeePerGas: '1',
    value: '1',
    maxPriorityFeePerGas: '1',
    nonce: 1,
    input: '0x'
  }
};

async function simulatePrebroadcast() {
  try {
    const response = await axios.post(WEB3FIREWALL_API_URL, prebroadcastPayload, {
      headers: {
        Authorization: `Bearer ${WEB3FIREWALL_TOKEN}`,
        'Content-Type': 'application/json'
      }
    });

    const { actionToTake, eventId } = response.data;

    console.log(`[Web3Firewall] Action: ${actionToTake.toUpperCase()}`);
    console.log(`[Web3Firewall] Event ID: ${eventId}`);

    if (actionToTake === 'needsApproval') {
      console.log('[Web3Firewall] This transaction requires manual review.');
    } else if (actionToTake === 'allow' || actionToTake === 'deny') {
      console.log('[Web3Firewall] Automated decision returned.');
    } else {
      console.log(`[Web3Firewall] Unrecognized action: ${actionToTake}`);
    }
  } catch (error: any) {
    if (error.response) {
      console.error('[Web3Firewall] API Error:', error.response.data);
    } else {
      console.error('[Web3Firewall] Request failed:', error.message);
    }
  }
}

simulatePrebroadcast();
