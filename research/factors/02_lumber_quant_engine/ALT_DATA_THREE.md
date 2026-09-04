# Three free alt-data series (implemented)

## 1. StatCan Canada softwood shipments → `canada_lumber_exports`

- Source: Statistics Canada table 16-10-0017 (Total softwood, shipments)
- Units: thousands of cubic metres
- Cache: `data/canada_softwood_shipments.csv`
- Loader: `load_canada_softwood_shipments(refresh=False)`
- Auto-injected by `load_live()`
- Note: shipments = mill outflow (domestic + export); strong physical-flow proxy for Wood on Wheels

## 2. NOAA Storm Events property damage → `storm_damage_usd`

- Source: NCEI Storm Events details bulk CSV (DAMAGE_PROPERTY)
- Aggregation: monthly sum of property damage (K/M/B parsed)
- Cache: `data/noaa_storm_damage_monthly.csv` (2022–2025 pulled)
- Loader: `load_noaa_storm_damage(years=..., refresh=False)`
- Auto-injected by `load_live()`
- Engine applies 2-month publication lag via PUBLICATION_LAGS_MONTHS

## 3. Google Trends DIY / lumber basket → `google_diy_trends`

- Keywords: lumber, 2x4, home improvement, DIY, plywood
- Loader: `load_google_diy_trends()` (requires `pytrends`)
- If rate-limited / missing: uses `data/google_diy_trends.csv` or seasonal placeholder
- Auto-injected by `load_live()`

## How to refresh

```python
from lumber_quant_engine.alt_data import (
    load_canada_softwood_shipments,
    load_noaa_storm_damage,
    load_google_diy_trends,
)

load_canada_softwood_shipments(refresh=True)
load_noaa_storm_damage(years=list(range(2018, 2027)), refresh=True)
load_google_diy_trends(refresh=True)  # needs pytrends + no 429
```

Then re-run:

```bash
python run.py --mode live --start 2018-01-01 --backtest-start 2022-01-01
```
