# Changelog

## v3.0.0 — 2026-09-07

### Research
- Rebuild factor v2: 65% 12-month z-score of log(damage) + 35% spike; publication lag 1 month
- Lag-1 storm-damage impulse explored end-to-end — not robust (rolling IC mean ~ -0.08)
- Honest proof status: no alpha demonstrated on LBR=F short sample

### Data
- StatCan Canada softwood shipments auto-inject
- NOAA Storm Events monthly property damage auto-inject
- Google Trends DIY/lumber basket (cache / pytrends)
- NIFC annual wildfire seasonal monthly proxy
- FRED total rail carloads coarse Wood-on-Wheels proxy

### Engine
- Expanding-window IC weights (negative IC floored at 0)
- Publication lags on all macro series
- Missing-factor reweighting
- Demo + live CLI

### Docs
- PROGRESS.md, PROOF_STATUS.md, ALT_DATA_THREE.md

## v0.3.x — 2026-09-04
- Production package layout, tests, free proxies

## v0.2 — earlier
- IC weights, publication lags, optional factors CSV
