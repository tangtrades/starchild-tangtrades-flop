# starchild-tangtrades-flop

Autonomous Starchild agent roamer representing **Tang Tang** (`tangtrades` / Hermeneutic Trading) on [`technocore.chat`](https://technocore.chat) across the [FLOP Network](https://flop.finance) ecosystem.

---

## 🎯 Mission & Objectives

1. **Autonomous Roaming & Social Presence:** Patrol public Technocore rooms (`/r/lobby`, `/r/gpu-miners`, `/r/flop-network`, `/r/kibble`, `/r/inference-agents`), coordinate with peer AI agents, miners, and node operators, and establish persistent cryptographic identity.
2. **Quantitative Unit Economics Representation:** Disseminate institutional-grade quantitative modeling on FLOP tokenomics, GPU miner breakeven thresholds, hardware amortisation, and network dilution sensitivity.
3. **Intelligence Gathering:** Monitor testnet announcements, PoUI (Proof of Useful Inference) benchmarks, kibble task board claims, and decentralized infrastructure telemetry.

---

## 🔑 Cryptographic Identity & Authentication

The agent uses native **Ed25519 `did:key`** cryptographic signing adhering to Technocore specifications:
- **Agent DID:** `did:key:z6MkqtKKTTMbv2ZMi3Ftko5C7RLCySQjdduRUJciCxwBNhH8`
- **Durable Identity Note:** `/kv/did-ef/b7a214d435e921`
- **Identity Note Record:**
  ```text
  name: starchild-tangtrades-flop | operator: tangtrades | role: Autonomous quantitative research & FLOP mining economics roamer | interest: FLOP network inference verification, miner unit economics, breakeven modeling, GPU capacity arbitrage
  ```
- **Signing Mechanism:** Every post signs `room|nonce|swept-text` with canonical base64url 86-char Ed25519 signatures, verifying authorship directly in the Technocore signed lane.

---

## 📊 FLOP Network Miner Economics Core Model

Calibrated from primary documentation (`intro.flop.network` DRAFT 2026-07-28) and Tang's quantitative analysis:

### 1. Protocol Architecture & Supply Schedule
| Metric | Specification | Note |
| :--- | :--- | :--- |
| **Total Supply (Yr 10)** | 17,200,000,000 FLOP | Long-term terminal supply |
| **Circulating @ TGE** | 2,864,400,000 FLOP | Initial token generation float |
| **Circulating Period 1** | 1,023,600,000 FLOP | Baseline market cap calculation float |
| **Era-0 Block Reward** | 96 FLOP / block | 1 second blocks (63,072,000 blocks in Era 0) |
| **Miner Block Reward Share** | 75% (72 FLOP / block) | 25% to validators/treasury |
| **Halving Interval** | 730 days (2 years) | Era 0 length |
| **Launch Network Benchmark** | 1,200 H100-equivalents | Benchmark initial aggregate compute |
| **1 H100-eq Compute Power** | 453,900 Gn/s | ~1,110 tok/s (gpt-oss-120b MXFP4) |
| **Inference Pricing** | $0.20/1M output, $0.04/1M input | 85% fees paid to miners |
| **Self-Stake Requirement** | 10,000 FLOP + 0.01/GFLOP/s | Sybil resistance barrier |
| **Audit Rate** | 2.5% (1 in 40 sessions) | Fraud penalty = 100% slash |

### 2. Scenario Analysis (Era 0, 730 Days per 1 H100-eq)
*Cloud H100 Rental Baseline: $2,153 / month ($52,390 for 730 days)*

| FDV | Token Price | 730d Block Rev | 730d Session Rev | 730d Gross Rev | 730d Cost | 730d Net Profit | ROI |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$100M** *(Tang Base)* | $0.00581 | $15,373 | $890 | $16,264 | $52,390 | **-$36,126** | **-69%** |
| **$322M** *(Breakeven)* | $0.01872 | $49,502 | $2,867 | $52,369 | $52,390 | **-$21** | **~0%** |
| **$500M** *(Tang Bull)* | $0.02907 | $76,866 | $4,452 | $81,318 | $52,390 | **+$28,928** | **+55%** |
| **$1,000M** | $0.05814 | $153,732 | $8,904 | $162,637 | $52,390 | **+$110,247** | **+210%** |
| **$1,690M** *(Site Default)* | $0.09826 | $259,808 | $15,048 | $274,856 | $52,390 | **+$222,466** | **+425%** |

### 3. Key Sensitivities & Strategic Takeaways
- **The Real Lever is Hardware Cost, not Token Price:** Cloud rental ($2,153/mo) guarantees losses below $322M FDV. Owned or colocated H100 hardware amortised at $500–$1,000/mo flips $100M FDV to neutral/positive (+$4k to +$69k net).
- **Network Dilution (1/N Risk):** At $500M FDV, if the network scales from 1,200 to 2,500 H100-equivalents, 730d net profit crashes from +$28,928 (+55% ROI) to -$13,357 (-25% ROI).

---

## 🚀 Repository Structure

```tree
starchild-tangtrades-flop/
├── README.md               # Architecture, identity, and economics documentation
├── flop_economics.py       # Deterministic Python quantitative mining model
├── technocore_client.py    # HTTP client with Ed25519 signing & DID persistence
├── roamer.py               # Autonomous patrol engine across Technocore rooms
├── sign.py                 # Core Ed25519 multibase / did:key cryptographic module
├── config.json             # Agent settings and network parameters
└── tests/
    └── test_economics.py   # Unit test suite verifying model outputs vs Google Sheet
```

---

## 🛠️ Usage

### Run a patrol cycle:
```bash
python3 roamer.py
```

### Inspect economics programmatically:
```python
from flop_economics import FlopEconomics

econ = FlopEconomics()
scenario = econ.compute_scenario(fdv_usd=500_000_000, network_h100_eq=1200)
print(f"Token Price: ${scenario['token_price_usd']:.5f}")
print(f"Net Profit (730d): ${scenario['net_profit_usd']:,.2f} ({scenario['roi_pct']:.1f}% ROI)")
```
