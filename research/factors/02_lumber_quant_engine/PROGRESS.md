# Progress log — Lumber Quant Engine

Last updated: 2026-09-07 (fiber residual complex)

## Status snapshot

| Area | Status |
|------|--------|
| Core engine | **v3.0** |
| Rebuild | v2 (65% level + 35% spike) |
| StatCan shipments / NOAA damage / Trends | Live / cached |
| **Residual fiber complex** | **WPU085 + WPU0911 + CAPUTLG321S in Wood on Wheels** |
| Price–engine link | PRICE_ENGINE_LINK.md |
| Alpha on LBR=F | **No** |

## Fiber residual (new)

Free FRED injectors:
- `pulpwood_chips_ppi` (WPU085)
- `wood_pulp_ppi` (WPU0911)
- `wood_product_caputil` (CAPUTLG321S)

See **FIBER_RESIDUAL.md**. National proxies only — not regional chip quotes or true NBSK util.

## Price action ↔ engine

LBR ~$566 (Sep 2026). Engine stayed NORMAL through summer peak and August selloff. See PRICE_ENGINE_LINK.md.

## Next priorities

1. Longer NOAA history pre-2022
2. Live Google Trends
3. Regional residual chip series if/when free
4. Cash lumber proxy for pre-2022 history
