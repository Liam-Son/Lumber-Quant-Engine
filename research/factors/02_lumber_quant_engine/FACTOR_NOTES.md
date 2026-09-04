# Factor 02 — Lumber Quant Engine v0.2

## What changed in v0.2

1. **Publication lags**  
   FRED and other series are shifted by realistic release lags before any signal is computed. This removes the classic look-ahead bias on macro data.

2. **Expanding-window IC weights**  
   Instead of static 1/6 weights, each factor’s weight is its expanding-window correlation with next-month lumber returns (negative ICs are floored at 0). Falls back to equal weight until enough history exists.

3. **Clearer alternative-data contract**  
   Missing series (wildfire, rail carloads, storm damage, traffic) stay optional. The engine re-weights across whatever is present.

## Data reality check (Sep 2026)

| Factor              | Free monthly source? | Notes |
|---------------------|----------------------|-------|
| Permit-to-Plank     | Yes (FRED)           | Strongest currently available |
| Mortgage Choke      | Partial              | Rate yes; apps limited |
| Wood on Wheels      | Partial              | Truck tonnage only |
| Weekend Warrior     | Partial              | Home-improvement sales |
| Burning Timber      | Annual only (NIFC)   | Needs monthly / geospatial for real edge |
| Rebuild             | Event-level (NOAA)   | Needs aggregation |

**LBR=F** history via Yahoo is still short (~2022 onward in many environments).

## How to run

```bash
cd research/factors/02_lumber_quant_engine
pip install -r requirements.txt

# Demo (all factors populated synthetically)
python run.py --mode demo

# Live with IC weights + lags
python run.py --mode live --start 2015-01-01 --backtest-start 2020-01-01

# Force classic equal weights
python run.py --mode live --equal-weight
```

## Next real edge

- Ingest NIFC / MTBS wildfire polygons + sawmill locations for true Burning Timber exposure.
- Licensed or scraped AAR lumber carloads + Statistics Canada exports.
- NOAA / FEMA event costs rolled to monthly residential exposure.
- Google Trends + any licensed foot-traffic feed for Weekend Warrior.
