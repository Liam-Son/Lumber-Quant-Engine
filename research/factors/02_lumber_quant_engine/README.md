# Lumber Quant Engine v3.1

Research software for a six-factor pressure / regime model of softwood lumber futures.

> **Not investment advice. No alpha has been demonstrated on live CME LBR=F.**
>
> Start here: [METHODOLOGY.md](METHODOLOGY.md) · [PROOF_STATUS.md](PROOF_STATUS.md) · [TEST_RESULTS.md](TEST_RESULTS.md)

Cite: `CITATION.cff` · License: MIT

## Quick start

```bash
pip install -r requirements.txt
pytest tests/ -q
python run.py --mode demo
python run.py --mode live --start 2018-01-01 --backtest-start 2022-08-01
```

## Factors

| # | Name | Idea |
|---|------|------|
| 1 | Burning Timber | Fire / drought supply stress |
| 2 | Permit-to-Plank | Housing demand pipeline |
| 3 | Mortgage Choke | Rate / affordability |
| 4 | Wood on Wheels | Physical flow + residual fiber + SHFE pulp USD |
| 5 | Rebuild | Disaster rebuild (v2: level + spike) |
| 6 | Weekend Warrior | DIY / home improvement |

Design: publication lags, expanding-window IC weights, missing-data reweight.
