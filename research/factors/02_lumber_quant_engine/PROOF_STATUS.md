# Can we prove alpha in the four candidate directions?

**Short answer (Sep 2026): Not yet.**  
Below is the rigorous status of each claim.

---

## 1. True geospatial Burning Timber (fire polygons × mill capacity)

| Requirement | Status |
|-------------|--------|
| Fire polygons with dates | Free (MTBS, FPA-FOD, NIFC Open Data) — multi-GB |
| Sawmill points + capacity | Mostly paid (Forisk). Partial open: AXE USA JSON (21 states, 2,931 records) |
| Spatial join + capacity weighting | Not implemented (needs geopandas + compute) |
| Monthly national/regional index | **Not built** |

**What we have instead**  
- Annual NIFC acres → seasonally distributed monthly proxy  
- Drought series (FRED)  
- These feed the existing `burning_timber` slot  

**Verdict**  
Coarse national proxy exists. Research-grade geospatial factor does **not**. No alpha can be claimed.

---

## 2. Proper monthly rail lumber carloads + Canadian exports

| Series | Free source? | In engine? |
|--------|--------------|------------|
| Total US rail carloads | Yes — FRED `RAILFRTCARLOADS` | Yes (auto-injected as coarse proxy) |
| Lumber-specific rail carloads | AAR / STB (mostly paid or weekly PDF) | No |
| Canadian softwood exports / shipments | Yes — StatCan 16-10-0017, BC Open Data | Scaffold only (download links provided) |

**Verdict**  
A coarse rail-flow proxy is live. Lumber-specific + Canadian export series are **not yet ingested**. No lumber-specific Wood-on-Wheels alpha is proven.

---

## 3. Storm / rebuild intensity with residential exposure

| Piece | Status |
|-------|--------|
| NOAA Storm Events bulk CSV / parquet | Free and documented |
| Monthly property-damage aggregation | Scaffold + exact method written |
| Residential exposure weighting | Needs Census housing units by county — not wired |
| Live series in engine | **No** |

**Verdict**  
Path is clear and free. Implementation of the monthly damage series is the remaining engineering step. No Rebuild alpha is proven yet.

---

## 4. Combination under IC weights + publication lags

| Component | Status |
|-----------|--------|
| Expanding-window IC weights | Implemented (v0.2) |
| Publication lags on FRED / proxies | Implemented |
| Live factors with real coverage | Permit-to-Plank + coarse fire + coarse rail + partial mortgage/truck/sales |
| Out-of-sample alpha test on LBR=F | **Failed / inconclusive** (short sample, mostly one-factor) |

**Verdict**  
The statistical machinery is ready. The data diet is still too thin to claim alpha.

---

## Bottom line

| Candidate | Implemented? | Alpha proven? |
|-----------|--------------|---------------|
| Geospatial Burning Timber | Proxy only | No |
| Rail + Canadian exports | Coarse rail only | No |
| Storm / Rebuild | Scaffold only | No |
| IC weights + lags on full set | Machinery yes, data no | No |

**No alpha has been demonstrated.**  
The honest next work is to ingest StatCan shipments, aggregate NOAA storm damage, and (if resources allow) run a true spatial fire×mill join. Until those series exist and survive walk-forward tests on a longer LBR=F sample, any performance claim would be overstated.
