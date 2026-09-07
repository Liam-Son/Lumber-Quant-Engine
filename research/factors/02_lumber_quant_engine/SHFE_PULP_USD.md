# SHFE pulp → USD (NBSK-adjacent public proxy)

## Formula

```
shfe_pulp_usd = (shfe_cny / 1.13 - logistics_cny) / usdcny
```

| Piece | Source |
|-------|--------|
| `shfe_cny` | SHFE SP (纸浆) highest-volume contract close |
| `1.13` | China VAT 13% on pulp |
| `logistics_cny` | Optional pad (0, **120** default, 150) toward CIF-comparable |
| `usdcny` | FRED `DEXCHUS` (Yuan per USD) |

Aligned with Fastmarkets/Norexeco-style **ex-VAT → USD** conversion.

## API

```python
from lumber_quant_engine.alt_data import load_shfe_pulp_usd, refresh_shfe_pulp_front

# extend daily CNY cache from SHFE public JSON
refresh_shfe_pulp_front(days=60)

# monthly USD series
s = load_shfe_pulp_usd(logistics_cny=120.0)
```

Caches:
- `data/shfe_pulp_front_cny.csv`
- `data/shfe_pulp_usd_monthly.csv`

## Engine

- Auto-injected in `load_live` as `shfe_pulp_usd`
- Publication lag **0** (futures)
- Mapped into **Wood on Wheels** residual-fiber leg

## Sample (seed cache, Sep 2026)

| Month | USD/t (L=120) | USD/t (L=0) |
|-------|---------------|-------------|
| 2026-08 | ~607 | ~625 |
| 2026-09 | ~621 | ~639 |

Front contract in seed: **SP2611** ~4,680–4,892 CNY.

## Limits

- Short history until you run `refresh_shfe_pulp_front` over more days
- Domestic BSK warehouse ≠ pure NBSK CIF China
- Brand list changes move basis
