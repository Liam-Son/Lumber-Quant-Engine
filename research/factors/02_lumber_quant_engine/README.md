# Lumber Quant Engine v3

Research-grade six-factor pressure / regime model for softwood lumber futures.

> Not investment advice. **No alpha has been demonstrated** on live LBR=F data yet.
> See [PROOF_STATUS.md](PROOF_STATUS.md), [PROGRESS.md](PROGRESS.md), [PRICE_ENGINE_LINK.md](PRICE_ENGINE_LINK.md).

## Factors

| # | Name | Idea | Free data in v3 |
|---|------|------|-----------------|
| 1 | Burning Timber | Fire / drought supply stress | NIFC annual to monthly |
| 2 | Permit-to-Plank | Housing demand pipeline | FRED PERMIT, HOUST |
| 3 | Mortgage Choke | Rate / affordability headwind | FRED mortgage rate |
| 4 | Wood on Wheels | Physical flow | FRED rail + StatCan shipments |
| 5 | Rebuild | Disaster rebuild demand | NOAA damage (v2 logic) |
| 6 | Weekend Warrior | DIY / home improvement | Trends cache + retail sales |

## Design

1. Publication lags (no look-ahead)
2. Expanding-window IC weights (fallback: equal weight)
3. Missing data causes automatic reweight
4. Rebuild v2 = short-window level + spike (not lag-1 impulse bet)

## Price check (Sep 2026)

LBR ~$566 (−14% from peak). Engine stayed **NORMAL** through summer peak and August selloff. Details: [PRICE_ENGINE_LINK.md](PRICE_ENGINE_LINK.md).

## Quick start

```bash
pip install -r requirements.txt
python run.py --mode demo
python run.py --mode live --start 2018-01-01 --backtest-start 2022-08-01
pytest tests/ -q
```

## License

MIT
