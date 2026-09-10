# Methodology (research protocol)

Version 3.1.0 · last validated 2026-09-10

This document states the identification strategy, estimation choices, and **explicit non-claims**.

## 1. Research question

Do publicly available, lagged physical and macro series contain tradable information about subsequent monthly CME lumber futures (LBR=F) returns?

## 2. Identification / no look-ahead

Every predictor is shifted by a publication lag before it enters a factor (`PUBLICATION_LAGS_MONTHS` in `core.py`). Returns used for IC and backtest are forward one month. Positions are lag-1 of the thresholded score.

Lags are conservative calendar months, not official ALFRED vintages — a known limitation.

## 3. Six factors

Burning Timber; Permit-to-Plank; Mortgage Choke; Wood on Wheels (nan-aware flow + residual fiber + SHFE pulp USD); Rebuild v2 (65% 12m level + 35% spike); Weekend Warrior.

## 4. Weights

Expanding-window IC vs next-month return; negative IC floored at 0; fallback equal weight.

## 5. Inference

Pearson IC; Newey–West HAC t on the slope of forward return on the factor (lag 3); i.i.d. bootstrap of strategy returns. Demo ICs are synthetic and must not be cited as evidence. Live LBR sample is too short for FDR to be meaningful.

## 6. Binding constraints

LBR=F usable monthly history ~ Aug 2022+; NOAA cache 2022–2025; SHFE USD seed short; Trends often placeholder.

## 7. Pre-registered negative results

1. Lag-1 storm-damage impulse IC ≈ +0.41 did not replicate (rolling mean ≈ −0.08).
2. Live LBR backtest from 2022-08 remains negative.
3. Engine stayed NORMAL through the 2026 summer peak and August selloff.

## 8. Replication

```bash
pip install -r requirements.txt
pytest tests/ -q
python run.py --mode demo
python run.py --mode live --start 2018-01-01 --backtest-start 2022-08-01
```
