# Residual fiber & sawmill operating rates (v3+)

Added to **Wood on Wheels** as the residual-fiber complex.

## Free series (auto-loaded via FRED in `load_live`)

| Column | FRED id | Meaning |
|--------|---------|--------|
| `pulpwood_chips_ppi` | **WPU085** | PPI: logs, bolts, timber, **pulpwood and wood chips** |
| `wood_pulp_ppi` | **WPU0911** | PPI: **wood pulp** (national cost proxy; not NBSK spot) |
| `wood_product_caputil` | **CAPUTLG321S** | Capacity utilization, wood products **NAICS 321** (sawmill operating-rate proxy) |

Publication lag: **1 month** each.

## Factor mapping

```
wood_on_wheels =
    0.30 * z(rail %chg)
  + 0.15 * z(truck %chg)
  + 0.20 * z(Canada shipments %chg)
  + 0.15 * z(pulpwood/chips PPI %chg)
  + 0.10 * z(wood pulp PPI %chg)
  + 0.10 * z(Δ capacity utilization)
```

## Economic read

- **Higher chips/pulpwood prices** → tighter residual fiber (can coincide with stronger sawlog/lumber balances).
- **Higher wood-product capacity utilization** → mills running harder → more residual supply into pulp/tissue.
- **Wood pulp PPI** → softwood pulp cost pressure (NBSK list/spot still paid/commercial).

## Limits

- National PPIs, not regional chip quotes (Forisk, etc.).
- NAICS 321 is broader than softwood sawmills alone.
- True NBSK production/capacity utilization is not a free monthly FRED series.

True regional residual prices remain the research upgrade path.
