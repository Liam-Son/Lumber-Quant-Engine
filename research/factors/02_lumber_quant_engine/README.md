# Lumber Quant Engine

**v0.3** — Research-grade six-factor pressure / regime model for softwood lumber futures.

> Research software. Not investment advice. No alpha has been demonstrated on live data yet.

## Factors

| # | Name | Economic idea | Live free data |
|---|------|---------------|----------------|
| 1 | **Burning Timber** | Fire + drought stress on timber supply | NIFC annual → monthly proxy + drought |
| 2 | **Permit-to-Plank** | Housing demand pipeline | FRED PERMIT + HOUST |
| 3 | **Mortgage Choke** | Rate / affordability headwind | FRED mortgage rate (+ apps if supplied) |
| 4 | **Wood on Wheels** | Physical flow (rail / truck / CA exports) | FRED total rail (coarse) + truck tonnage |
| 5 | **Rebuild** | Disaster-driven replacement demand | Optional (NOAA path documented) |
| 6 | **Weekend Warrior** | DIY / home-improvement demand | Home-improvement sales (+ traffic if supplied) |

Positive composite score → bullish pressure. Negative → bearish.

## Design principles

1. **Publication lags** on every macro series (no look-ahead).
2. **Expanding-window IC weights** (negative IC floored at 0; falls back to equal weight).
3. **Missing data is allowed** — the composite re-weights across available factors.
4. **Honest status** — see `PROOF_STATUS.md`. Coarse proxies ≠ research-grade alpha.

## Quick start

```bash
pip install -r requirements.txt

# Offline (synthetic, all six factors populated)
python run.py --mode demo

# Live free data + proxies
python run.py --mode live --start 2015-01-01 --backtest-start 2020-01-01

# Classic equal weights, no lags
python run.py --mode live --equal-weight --no-lags
```

Outputs:
- `outputs/lumber_engine_results.csv` — factors, score, regime, positions, equity
- `outputs/summary.csv` — total return, Sharpe, max DD, trades, bootstrap CI

## Project layout

```
lumber_quant_engine/
├── README.md
├── PROOF_STATUS.md
├── requirements.txt
├── run.py
├── data/
│   ├── nifc_wildfire_annual.csv
│   └── optional_factors.csv
├── src/lumber_quant_engine/
│   ├── __init__.py
│   ├── core.py
│   ├── data.py
│   └── alt_data.py
└── tests/
    └── test_engine.py
```

## Tests

```bash
pytest tests/ -q
```

## License

MIT
