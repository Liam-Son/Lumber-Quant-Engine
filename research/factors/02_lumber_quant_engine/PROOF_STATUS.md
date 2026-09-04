# Proof status — is there alpha?

**As of 2026-09-04: No alpha has been demonstrated.**

| Candidate | What exists | Alpha proven? |
|-----------|-------------|---------------|
| Geospatial Burning Timber (fire × mill) | Annual NIFC seasonal proxy only | **No** |
| Lumber-specific rail + Canadian exports | FRED total rail + StatCan shipments | **No** |
| Storm / Rebuild intensity | NOAA monthly damage + redesigned factor | **No** |
| Lag-1 damage impulse (standalone) | Explored; IC unstable / not robust | **No** |
| Full set under IC weights + lags | Machinery ready; LBR=F sample short | **No** |

### Rebuild note

Lag-1 raw damage once appeared strong (IC ≈ +0.41) under a single alignment.  
Clean re-test: lag-1 ICs ≈ 0 to negative; rolling IC mean ≈ −0.08.  
Rebuild v2 preserves short-window level + spike with correct-sign buckets, but is **not** a proven edge.

### Binding constraints

1. LBR=F usable monthly history ≈ 2022+ only.
2. Alternative series coverage still incomplete (Trends placeholder, no mill×fire spatial).
3. n ≈ 30–50 months is insufficient for stable IC / backtest claims.

The framework (lags, IC weights, free alt-data injectors) is in place.  
The constraint is **data length and quality**, not code.
