# Proof status — is there alpha?

**As of 2026-09-10 (v3.1.0): No alpha has been demonstrated.**

Automated tests and demo pipeline are green (`TEST_RESULTS.md`). That is software validation, not an economic result.

| Candidate | What exists | Alpha proven? |
|-----------|-------------|---------------|
| Geospatial Burning Timber (fire × mill) | Annual NIFC seasonal proxy only | **No** |
| Lumber-specific rail + Canadian exports | FRED total rail + StatCan shipments | **No** |
| Storm / Rebuild intensity | NOAA monthly damage + Rebuild v2 | **No** |
| Lag-1 damage impulse (standalone) | Explored; IC unstable / not robust | **No** |
| SHFE pulp USD / residual fiber | Wired into Wood on Wheels | **No** |
| Full set under IC weights + lags | Machinery ready; LBR=F sample short | **No** |

### Binding constraints

1. LBR=F usable monthly history ~ 2022+ only.
2. Alternative series still incomplete (Trends placeholder; no mill×fire spatial).
3. n ~ 30–50 months is insufficient for stable IC / backtest claims.

The framework is in place. The constraint is data length and quality, not code.
