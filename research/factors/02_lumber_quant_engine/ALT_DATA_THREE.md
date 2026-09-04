# Three free alt-data series (implemented)

## 1. StatCan Canada softwood shipments → `canada_lumber_exports`
- Source: Statistics Canada 16-10-0017 (Total softwood, shipments)
- Cache: `data/canada_softwood_shipments.csv`
- Loader: `load_canada_softwood_shipments(refresh=False)`
- Auto-injected by `load_live()`

## 2. NOAA Storm Events → `storm_damage_usd`
- Source: NCEI Storm Events details bulk CSV
- Cache: `data/noaa_storm_damage_monthly.csv` (2022–2025)
- Loader: `load_noaa_storm_damage(refresh=False)`
- Publication lag: 1 month (Rebuild v2)

## 3. Google Trends DIY / lumber → `google_diy_trends`
- Keywords: lumber, 2x4, home improvement, DIY, plywood
- Requires `pytrends`; falls back to cache/placeholder
- Loader: `load_google_diy_trends(refresh=False)`

## Research note (2026-09-04)
Lag-1 damage impulse was explored in depth and **did not** replicate as a robust signal.
See PROGRESS.md and PROOF_STATUS.md.
