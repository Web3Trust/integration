// Web3Firewall Post-Broadcast Evaluation (TypeScript)
// =====================================================
//
// This script submits a broadcasted Ethereum transaction to the Web3Firewall API
// for post-signature risk evaluation.
//
// Requires:
// - Node.js with axios installed
// - A valid Web3Firewall Bearer Token
//
// To run:
// $ ts-node simulatePostbroadcast.ts

import axios from 'axios';

const WEB3FIREWALL_API_URL = 'https://api.web3firewall.io/api/v1/policy/event';
const WEB3FIREWALL_TOKEN = 'YOUR_WEB3FIREWALL_BEARER_TOKEN_HERE';

// Sample signed transaction payload
const postbroadcastPayload = {
  kind: 'transaction:broadcasted',
  datetime: '2025-02-20T11:38:19.718Z',
  data: {
    network: 'eth',
    from: '0x61ed4B62E03798305818607C7160B2AbFF15cFeD',
    to: '0xd756bF764ad08E0B67E7466FFA7A52D788935344',
    nonce: 16469,
    value: '1000000000',
    data: '0x',
    gasLimit: '0x76c0',
    gasPrice: '0x9184e72a000',
    r: '0xc7f985f8286d87c7db7c7eed96534caf461be358504a0fcd82a5861c6b343dba',
    s: '0x1dd708a092571cdf513f3658fd4fca7de119b0eb953abb3e1141e1fbc02d37e5',
    yParityOrV: '0x1'
  }
};

async function evaluatePostbroadcast() {
  try {
    const response = await axios.post(WEB3FIREWALL_API_URL, postbroadcastPayload, {
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

evaluatePostbroadcast();
