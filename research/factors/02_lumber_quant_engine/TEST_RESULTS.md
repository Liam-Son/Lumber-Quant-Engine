# Test and validation log

**Date:** 2026-09-10  
**Engine:** v3.1.0

## Automated tests

```
python -m pytest tests/ -q
...........                                                              [100%]
11 passed
```

Includes publication-lag shift, NIFC annual reconstruction, fiber columns, Wood on Wheels build, SHFE cache conversion, Newey–West helper sign check, demo + IC-weight pipelines.

## Demo-mode run

```
LUMBER QUANT ENGINE v3.1.0
Latest regime    : NORMAL
Latest score     : -0.423
Stats            : total_return -0.039, sharpe -0.125, max_drawdown -0.063, trades 64
Bootstrap 95%    : [-0.160, 0.098]
```

Demo prices are synthetic. Pipeline health check only.

## Live LBR=F (2022-08+)

- Backtest threshold 0.5: total return ≈ −26%, Sharpe ≈ −0.7.
- 2026-06→09 regime: NORMAL through peak and August selloff.
- **No alpha demonstrated.**
