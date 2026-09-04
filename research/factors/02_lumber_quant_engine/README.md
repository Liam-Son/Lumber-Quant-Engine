# Lumber Quant Engine v0.1

Six-factor lumber pressure/regime model.

## Factors
1. **Burning Timber Index** — wildfire acres × mill-capacity exposure + drought.
2. **Permit-to-Plank** — lagged building permits + housing starts impulses.
3. **Mortgage Choke** — mortgage-rate shock, mortgage applications, affordability.
4. **Wood on Wheels** — rail lumber carloads + trucking + Canadian exports.
5. **Rebuild Index** — storm damage × residential exposure, lagged.
6. **Weekend Warrior Index** — Home Depot/Lowe's traffic proxies + Google DIY trends + home-improvement sales.

Positive factor/aggregate values indicate bullish lumber pressure; negative values indicate bearish pressure.

## Run immediately (no internet)
```bash
pip install -r requirements.txt
python run.py --mode demo
```

## Live mode
```bash
python run.py --mode live --start 2020-01-01
python run.py --mode live --start 2015-01-01 --backtest-start 2020-01-01
```
Live mode pulls Lumber Futures (`LBR=F`) via Yahoo Finance and public FRED CSV series where available. FRED series are resampled monthly. Optional/alternative-data series can be supplied in `data/optional_factors.csv`.

### Optional CSV columns
`wildfire_acres,drought_index,mill_capacity_exposed,mortgage_apps,rail_lumber_carloads,canada_lumber_exports,storm_damage_usd,storm_residential_exposure,home_depot_traffic,lowes_traffic,google_diy_trends`

This separation is deliberate: wildfire-to-mill geospatial exposure and retailer foot traffic usually require specialized public datasets, scraping, geospatial processing, or paid vendors. Do not silently fake them. Missing factor inputs remain missing and the composite score reweights across available factors.

## Outputs
- `outputs/lumber_engine_results.csv`: raw data, six factor scores, pressure score, regime, positions, returns, equity.
- `outputs/summary.csv`: total return, Sharpe, max drawdown, trades, bootstrap return CI.

## Research next steps
- Replace equal weights with expanding-window IC weights.
- Add release-date / vintage handling to eliminate macro look-ahead bias.
- Add walk-forward logistic/XGBoost only after univariate factor validation.
- Use geospatial wildfire polygons + sawmill coordinates/capacity for true Burning Timber exposure.
- Use AAR rail commodity carloads and Statistics Canada lumber export/production feeds for Wood on Wheels.
- Use NOAA/FEMA event-level property exposure for Rebuild.
- Use Google Trends + Placer.ai/SafeGraph-style traffic if licensed for Weekend Warrior.

**Research software, not investment advice.**
