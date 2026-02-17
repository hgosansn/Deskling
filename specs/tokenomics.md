# Tokenomics Spec (DSL)

Related roadmap tasks: `P9-T1`, `P9-T2`, `P9-T3`, `P9-T4`, `P9-T5`

## Purpose
Define Deskling Token (`DSL`) as a utility-first economic layer for:
- AI compute consumption
- creator marketplace settlement
- optional staking-based usage perks

This spec is a product/economics document, not investment marketing.

## Product Principles
- Utility first: token value must come from product usage, not speculation mechanics.
- Web2 + Web3 compatibility: fiat paths remain available for non-crypto users.
- Safety and compliance: jurisdiction, AML/KYC, tax, and consumer-protection checks are required before launch.
- Progressive rollout: off-chain operational model first; on-chain expansion only after fit and controls.

## Token Basics (Draft)
| Property | Value |
| --- | --- |
| Token Name | Deskling Token |
| Symbol | DSL |
| Type | Utility Token |
| Standard | TBD (`ERC-20` / `SPL` / other) |
| Primary Use | AI credits + marketplace currency |
| Decimals | 18 (if EVM path selected) |
| Governance | Optional post-MVP |

## Utility Model
### 1) AI Service Fees (Primary)
DSL can be consumed for:
- model inference requests
- vision/screenshot analysis
- workflow automation runs
- premium latency tiers
- extended context/memory processing

Pricing abstraction:
- each action has a compute-unit cost
- compute units map to DSL at a configurable rate
- rate updates are versioned and auditable

### 2) Marketplace Currency
Marketplace settlement uses DSL for:
- skins, animation packs, voice packs
- personalities, workflows, plugins

Creator payouts:
- credited in DSL
- fee deductions and payout rules are transparent in transaction receipts

### 3) Fiat Coexistence
Users can still pay with fiat rails (card, wallet, etc.).
Fiat usage can convert to internal compute credits; DSL path may include fee discounts.

## Demand and Retention Mechanics
### Staking Perks (Draft)
| Tier | Stake | Benefit |
| --- | --- | --- |
| Bronze | 1,000 DSL | 5% AI fee discount |
| Silver | 5,000 DSL | 10% AI fee discount |
| Gold | 20,000 DSL | 20% AI fee discount |
| Creator Pro | 50,000 DSL | 50% marketplace fee discount |

Staking controls:
- unbonding period to reduce rapid churn
- anti-sybil constraints for perk abuse
- caps for promotional multipliers

### Premium Feature Gating (Optional)
Holding/staking DSL may unlock:
- advanced automation modes
- higher throughput quotas
- experimental/labs feature channels

## Revenue and Fee Flows
### Marketplace Fee (Draft)
- default fee example: `2.5%`

Illustrative split:
- `50%` treasury/operations
- `30%` compute reserve pool
- `20%` community incentives

### Compute Reserve Pool
Reserve funded by:
- DSL AI usage payments
- marketplace fee allocation
- fiat-to-credit conversion margin (if applicable)

Objective: maintain predictable infra budget for model and service operations.

## Supply and Distribution (Draft Policy)
### Total Supply
- Fixed supply target: `1,000,000,000 DSL`

### Initial Allocation (Draft)
| Category | Allocation | Share |
| --- | --- | --- |
| Community and Rewards | 300,000,000 | 30% |
| Ecosystem Growth | 200,000,000 | 20% |
| Treasury / Ops / Compute Reserve | 200,000,000 | 20% |
| Team | 150,000,000 | 15% |
| Liquidity and Listings | 100,000,000 | 10% |
| Advisors / Early Contributors | 50,000,000 | 5% |

## Vesting and Lockups
### Team
- 12-month cliff
- 36-month linear vesting after cliff

### Advisors / Early Contributors
- 6-month cliff
- 18-month linear vesting after cliff

## Optional Deflation Mechanisms
These are optional and must be A/B evaluated against retention and pricing stability.

### AI Usage Burn (Example)
- `5%` burn
- `95%` routed to reserve pool

### Marketplace Fee Burn (Example)
- up to `20%` of fees burned
- remainder for ops, reserve, and incentives

## Rewards Programs
### Creator Programs
- featured creator rotations
- seasonal contests and grants
- quality-based boosts for trusted creators

### Community Programs
- bug bounties
- docs/translations
- plugin contributions
- verified growth/community campaigns

## Collectible Asset Strategy
### Phase A (recommended start): Off-chain ownership
- account-bound ownership records in Deskling backend
- lower onboarding friction

### Phase B (optional): On-chain collectibles
- selective NFT-style asset minting
- external transfer/trade support
- only after legal and user-experience gates

## Compliance and Risk Controls
Mandatory before launch:
- jurisdiction matrix (where DSL utility launch is allowed)
- legal review checklist (token classification, consumer disclosures)
- AML/KYC rules for applicable flows
- tax and accounting handling for creator payouts and treasury
- fraud, abuse, and sanctions screening requirements

## Rollout Plan
1. Internal economics simulation and stress testing.
2. Closed beta with off-chain credits mirroring DSL logic.
3. Public utility launch with capped limits and monitoring.
4. Expansion to staking/perks after abuse-review pass.
5. Optional on-chain and governance extensions.

## Disclaimer Baseline
DSL is intended as a utility token for Deskling services and marketplace transactions.
DSL does not represent equity, ownership, or guaranteed financial return.

