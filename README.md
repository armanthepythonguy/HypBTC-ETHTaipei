# HypBTC 🔥🔥🔥
### A privacy-preserving cross-chain token transfer protocol powered by MPC
![6310009675059412305](https://github.com/user-attachments/assets/79a55b03-6dab-494d-a93a-253a3e724274)

## Motivation
HypBTC introduces a novel privacy layer for token transfers across blockchains—starting with Bitcoin on the Citrea zkL2 and extending to other chains via Hyperlane. The key innovation lies in concealing the transaction amounts using Multi-Party Computation (MPC), ensuring that sensitive financial data remains private even on public chains like Ethereum.

Here’s how it works: when users deposit cBTC (Citrea's bridged Bitcoin) into our smart contract on the Citrea chain, they opt into a privacy layer. From that moment, all subsequent transactions—whether they’re within Citrea or bridged to another chain—are amount-obfuscated, meaning no one on-chain can deduce the actual value being transferred. Behind the scenes, a committee of MPC nodes manage the balance ledger in secret-shared form, so no single party ever learns the actual balances.

To facilitate cross-chain transfers, we leverage Hyperlane, a modular interoperability layer, allowing private transfers to propagate securely to destination chains. All this happens without revealing the transaction amount at any step.

To enforce regulatory compliance, particularly concerning sanctioned entities, we integrate with the Self Protocol to perform private OFAC checks. Users who are found to be on the US OFAC list are prevented from initiating any transactions within the protocol.

This project represents a new primitive for privacy in a cross-chain, multi-asset world—one that balances both privacy and compliance, making it viable for real-world adoption.
![hypbtc](https://github.com/user-attachments/assets/b8e23caa-ef6c-4741-beae-7d52e2849941)



## How it works
🔒 MPC (Multi-Party Computation) Layer
We implemented an MPC protocol based on Shamir’s Secret Sharing (SSS) and additive secret sharing.
Every user balance is split into secret shares and distributed across an MPC committee.
When a user initiates a transfer, the amount is never revealed; instead, MPC parties update the ledger via additive operations on shares.
We designed secure protocols for add and subtract to maintain balance correctness without leakage.


🔁 Cross-Chain Transfer with Hyperlane
We integrated Hyperlane as our cross-chain messaging protocol to support bridging to EVM chains.
When a user initiates a bridge, the MPC committee confirms share availability and sends an obfuscated payload to the destination chain via Hyperlane.
Destination smart contracts validate the message, and users can claim their tokens without any amount disclosure on-chain.


🚨 OFAC Compliance with Self Protocol
Before any user can transact, their identity is checked using Self Protocol’s privacy-preserving KYC framework.
If they are found on the US OFAC sanctions list, their transaction is blocked at the MPC coordination layer.
This ensures that we remain compliant with global regulations while maintaining privacy for legitimate users.
