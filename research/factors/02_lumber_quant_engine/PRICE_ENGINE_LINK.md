# Price action linked to Lumber Quant Engine v3

**As of 2026-09-07** · LBR≈$566.5 · Engine regime: **NORMAL** (score ≈ +0.03)

## What the market did (2025–2026)

| Phase | Price action | Approx. levels |
|-------|--------------|----------------|
| Late 2025 soft | Oct–Dec drift lower | ~539–544 |
| Early 2026 chop | Jan spike, Feb dip, Mar rebound | 558–668 range |
| Summer 2026 peak | Jun–Jul strength | **617 / 614** monthly; high ~**659** |
| August selloff | **−7.3%** month | 617 → **569** |
| Early Sep | Range stabilize | **560–580**, last ~**566.5** |

Fundamentals: supply tighter (curtailments, CA duties) vs **flat housing demand** and seasonal soft patch. Curve: flat front, contango into 2027.

## What the engine said

| Month | LBR close | Pressure score | Regime | Notes |
|-------|-----------|----------------|--------|-------|
| 2026-06 | 617 | −0.46 | NORMAL | Peak price; score **not** SHORTAGE — demand factors soft |
| 2026-07 | 614 | −0.17 | NORMAL | Still elevated price, neutral pressure |
| 2026-08 | 569 | −0.05 | NORMAL | Selloff month; score near zero (no panic GLUT signal) |
| 2026-09 | 566.5 | +0.03 | NORMAL | Stabilization; composite neutral |

### Factor colors during the correction

- **Permit-to-Plank**: Mixed; weak in Jun (−1.76), better in Jul (+0.82) — housing impulse not driving a sustained bull signal into the peak.
- **Wood on Wheels**: Mildly negative through summer (shipments/rail not signaling tight physical flow).
- **Rebuild**: Slightly negative (no fresh damage impulse in lag window).
- **Mortgage / Burning / Weekend**: Sparse coverage on this window (NaNs) → composite leans on available factors only.

### Interpretation

1. **Engine did not flash SHORTAGE/BULL into the summer high.** Price ran on supply narrative and positioning; the free-data composite stayed **NORMAL**.
2. **Engine did not flash GLUT/BEAR into the August drop.** The selloff looks more seasonal/technical than a full factor-driven glut regime.
3. That matches a **range / mean-reversion market**: supply floor + soft demand → hard for threshold long/short rules.
4. Live backtest from 2022-08 (threshold 0.5) remains **negative** (total return ~−26%, Sharpe ~−0.7) — consistent with no proven edge.

## Design implication

v3 stays research-grade:

- Publication lags + IC weights + Rebuild v2 remain appropriate.
- Lag-1 damage impulse still **not** treated as alpha.
- Price–factor linkage for 2026 is **neutral regime through a supply-led peak and seasonal selloff** — useful as a **regime check**, not a trade signal.

## Reproduce

```bash
python run.py --mode live --start 2018-01-01 --backtest-start 2022-08-01
```
