# Progress log — Lumber Quant Engine

Last updated: 2026-09-07 (v3.0.0 + price–engine link)

## Status snapshot

| Area | Status |
|------|--------|
| Core engine (6 factors, IC weights, lags) | **v3.0** live |
| Rebuild factor redesign | **v2** (65% 12m level + 35% spike; lag=1) |
| StatCan Canada softwood shipments | Cached + auto-injected |
| NOAA storm property damage | Cached 2022–2025 + auto-injected |
| Google Trends DIY basket | Placeholder (live pull needs pytrends) |
| NIFC wildfire annual → monthly | Live |
| FRED total rail carloads | Live (coarse Wood-on-Wheels) |
| Price action linked to engine | **PRICE_ENGINE_LINK.md** |
| Alpha proven on LBR=F | **No** |

## Price action ↔ engine (2026-09-07)

LBR futures ~**$566.5**, −14% from 2026 peak (~659), under MA50.

| Month | Price | Score | Regime |
|-------|-------|-------|--------|
| 2026-06 | 617 | −0.46 | NORMAL |
| 2026-07 | 614 | −0.17 | NORMAL |
| 2026-08 | 569 | −0.05 | NORMAL |
| 2026-09 | 566.5 | +0.03 | NORMAL |

Engine stayed **NORMAL** through the summer peak and August selloff — no shortage signal into the high, no glut signal into the drop. Fits a supply-supported, demand-soft range market. See **PRICE_ENGINE_LINK.md**.

Live backtest (2022-08+, thresh 0.5): still negative; **no alpha**.

## Research findings (2026-09-04)

### Lag-1 storm damage impulse

- Earlier exploratory IC ~ +0.41 on lag-1 damage **did not replicate** under clean alignment.
- Tradable lag-1 ICs ~0 to slightly negative (n ~ 31).
- Rolling 18m IC of lag-1 log damage: mean −0.08 (unstable).
- **Conclusion:** lag-1 damage impulse is not a robust standalone signal.

### Rebuild redesign

| Version | Spec | Notes |
|---------|------|-------|
| v0 | 24m z of log(damage) | Wrong-sign buckets |
| v1 | impulse-heavy | Weak |
| **v2** | 65% z12(level) + 35% z12(delta) | Correct-sign buckets; lag=1 |

## Next research priorities

1. Longer NOAA history (pre-2022) for stable Rebuild baselines.
2. Live Google Trends pull when API access is available.
3. Optional: lag-2/lag-3 *level* damage as slow Rebuild channel.
4. Cash lumber proxy (Random Lengths) for pre-2022 LBR=F gap.
5. Richer mortgage / DIY coverage so fewer NaNs in live composite.
