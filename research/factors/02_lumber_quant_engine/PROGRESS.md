# Progress log — Lumber Quant Engine

Last updated: 2026-09-04

## Status snapshot

| Area | Status |
|------|--------|
| Core engine (6 factors, IC weights, lags) | **v0.3** live |
| Rebuild factor redesign | **v2** (65% 12m level + 35% spike; lag=1) |
| StatCan Canada softwood shipments | Cached + auto-injected |
| NOAA storm property damage | Cached 2022–2025 + auto-injected |
| Google Trends DIY basket | Placeholder (live pull needs pytrends) |
| NIFC wildfire annual → monthly | Live |
| FRED total rail carloads | Live (coarse Wood-on-Wheels) |
| Alpha proven on LBR=F | **No** |

## Research findings (2026-09-04)

### Lag-1 storm damage impulse

- Earlier exploratory IC ≈ +0.41 on lag-1 damage **did not replicate** under clean alignment.
- Tradable lag-1 ICs for level/impulse are ~0 to slightly negative (n ≈ 31).
- Concurrent (lag-0) raw damage still correlates with same-window returns (not tradable).
- Rolling 18m IC of lag-1 log damage: mean −0.08, range −0.49 to +0.19 (unstable).
- **Conclusion:** lag-1 damage impulse is not a robust standalone signal on this sample.

### Rebuild redesign

| Version | Spec | IC1 | High−Low spread |
|---------|------|-----|-----------------|
| v0 | 24m z of log(damage) | −0.13 | wrong sign |
| v1 | impulse-heavy | −0.04 | weak |
| **v2** | 65% z12(level) + 35% z12(Δ) | ~0 | **+2.2%** (correct sign) |

Publication lag for storm series set to **1 month**.

### Factor ICs (LBR=F window ~2022-08 → 2026-09, exploratory)

- Composite 3m IC mildly positive (~0.2–0.3) in some cuts; 1m IC weak/negative.
- Backtests on this window remain **negative** overall.
- Sample too short for claims.

## Data inventory (`data/`)

| File | Contents |
|------|----------|
| `canada_softwood_shipments.csv` | StatCan total softwood shipments (000 m³) |
| `noaa_storm_damage_monthly.csv` | NOAA monthly property damage USD |
| `google_diy_trends.csv` | Trends basket (placeholder if rate-limited) |
| `nifc_wildfire_annual.csv` | NIFC annual acres 1983–2025 |
| `lbr_f_monthly.csv` | LBR=F monthly closes (Yahoo chart) |
| `optional_factors.csv` | User overlay template |

## How to run

```bash
pip install -r requirements.txt
python run.py --mode demo
python run.py --mode live --start 2018-01-01 --backtest-start 2022-08-01
pytest tests/ -q
```

## Next research priorities

1. Longer NOAA history (pre-2022) for stable Rebuild baselines.
2. Live Google Trends pull when API access is available.
3. Optional: lag-2/lag-3 *level* damage as slow Rebuild channel (not lag-1 impulse).
4. Cash lumber proxy (e.g. Random Lengths) for pre-2022 LBR=F gap.
