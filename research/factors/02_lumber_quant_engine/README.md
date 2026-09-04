# Lumber Quant Engine

**v0.3.1** (Rebuild redesign + alt-data) — Research-grade six-factor pressure / regime model for softwood lumber futures.

> Research software. Not investment advice. No alpha has been demonstrated on live data yet.

See **PROGRESS.md** and **PROOF_STATUS.md** for the latest research findings.

## Factors

| # | Name | Economic idea | Live free data |
|---|------|---------------|----------------|
| 1 | **Burning Timber** | Fire + drought stress on timber supply | NIFC annual → monthly proxy |
| 2 | **Permit-to-Plank** | Housing demand pipeline | FRED PERMIT + HOUST |
| 3 | **Mortgage Choke** | Rate / affordability headwind | FRED mortgage rate |
| 4 | **Wood on Wheels** | Physical flow (rail / truck / CA shipments) | FRED rail + StatCan shipments |
| 5 | **Rebuild** | Disaster-driven demand (v2: 12m level + spike) | NOAA monthly property damage |
| 6 | **Weekend Warrior** | DIY / home-improvement demand | Trends placeholder + sales |

## Design principles

1. **Publication lags** on every macro series (no look-ahead).
2. **Expanding-window IC weights** (negative IC floored at 0; falls back to equal weight).
3. **Missing data is allowed** — the composite re-weights across available factors.
4. **Honest status** — lag-1 damage impulse explored and **not** robust; no alpha claimed.

## Quick start

```bash
pip install -r requirements.txt
python run.py --mode demo
python run.py --mode live --start 2018-01-01 --backtest-start 2022-08-01
pytest tests/ -q
```

## License

MIT
