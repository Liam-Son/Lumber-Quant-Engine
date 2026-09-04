# Factor 02 — Lumber Quant Engine (6-factor pressure model)

## Status (Sep 2026)

Live public-data coverage is currently limited:

| Factor              | Public data available? | Notes |
|---------------------|------------------------|-------|
| Burning Timber      | No                     | Needs wildfire acres + mill exposure |
| Permit-to-Plank     | Yes                    | FRED PERMIT + HOUST                  |
| Mortgage Choke      | Partial                | Rate yes; apps & full affordability limited |
| Wood on Wheels      | Partial                | Truck tonnage only                   |
| Rebuild             | No                     | Needs storm damage series            |
| Weekend Warrior     | Partial                | Home-improvement sales only          |

**LBR=F** continuous history via Yahoo currently starts ~Aug 2022 in this environment (50 months).

## How to run

```bash
cd research/factors/02_lumber_quant_engine
pip install -r requirements.txt
python run.py --mode demo
python run.py --mode live --start 2015-01-01 --backtest-start 2020-01-01
```

## Key findings so far

- With only free public series, the composite score largely collapses to **Permit-to-Plank**.
- IC of Permit-to-Plank vs 1-month forward lumber return is currently weak/negative on the short sample.
- 3-month IC is mildly positive (~0.22) — worth monitoring as sample grows.
- Equal-weight backtest performance is poor; next step is expanding-window IC weighting + proper vintage dates.
