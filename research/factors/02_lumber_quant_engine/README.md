# Lumber Quant Engine v3.1

Research-grade six-factor pressure / regime model for softwood lumber futures.

> Not investment advice. **No alpha has been demonstrated** on live LBR=F yet.
> See PROOF_STATUS.md, PROGRESS.md, PRICE_ENGINE_LINK.md, FIBER_RESIDUAL.md, SHFE_PULP_USD.md.

## Factors

| # | Name | Idea | Data in v3.1 |
|---|------|------|----------------|
| 1 | Burning Timber | Fire / drought supply stress | NIFC annual → monthly |
| 2 | Permit-to-Plank | Housing demand pipeline | FRED PERMIT, HOUST |
| 3 | Mortgage Choke | Rate / affordability | FRED mortgage rate |
| 4 | Wood on Wheels | Physical flow + residual fiber | Rail, StatCan, chips PPI, wood pulp PPI, capacity util, **SHFE pulp USD** |
| 5 | Rebuild | Disaster rebuild demand | NOAA damage (v2: 65% level + 35% spike) |
| 6 | Weekend Warrior | DIY / home improvement | Trends cache + retail sales |

## Design

1. Publication lags (no look-ahead)
2. Expanding-window IC weights
3. Missing data → automatic reweight (nan-aware factor legs)
4. Honest status: no proven alpha

## Quick start

```bash
pip install -r requirements.txt
python run.py --mode demo
python run.py --mode live --start 2018-01-01 --backtest-start 2022-08-01
pytest tests/ -q
```

```python
from lumber_quant_engine import refresh_shfe_pulp_front, load_shfe_pulp_usd
refresh_shfe_pulp_front(days=60)
s = load_shfe_pulp_usd(logistics_cny=120)
```

## License

MIT
