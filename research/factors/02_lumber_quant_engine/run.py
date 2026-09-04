#!/usr/bin/env python3
"""
Lumber Quant Engine v0.3
========================
Demo / live runner with publication lags, IC weights, and free proxies.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from lumber_quant_engine import (
    LumberFactorEngine,
    backtest,
    bootstrap_total_return,
    load_live,
    make_demo,
    __version__,
)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=f"Lumber Quant Engine v{__version__}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    ap.add_argument("--mode", choices=["demo", "live"], default="demo")
    ap.add_argument("--start", default="2005-01-01", help="Data start date")
    ap.add_argument(
        "--backtest-start",
        default=None,
        help="Evaluate performance only from this date forward",
    )
    ap.add_argument("--threshold", type=float, default=0.75)
    ap.add_argument(
        "--equal-weight",
        action="store_true",
        help="Disable IC weighting; use static 1/6 weights",
    )
    ap.add_argument("--no-lags", action="store_true", help="Disable publication lags")
    args = ap.parse_args()

    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)

    if args.mode == "demo":
        df = make_demo(start=args.start)
    else:
        df = load_live(args.start)

    engine = LumberFactorEngine(
        use_ic_weights=not args.equal_weight,
        apply_lags=not args.no_lags,
    )
    sig = engine.build(df)

    if args.backtest_start:
        sig = sig.loc[args.backtest_start:].copy()
        print(f"[Info] Backtest window starts {args.backtest_start}")

    bt, stats = backtest(sig, threshold=args.threshold)
    boot = bootstrap_total_return(bt["strategy_ret"])

    bt.to_csv(out_dir / "lumber_engine_results.csv")
    pd.DataFrame([{**stats, **{f"bootstrap_{k}": v for k, v in boot.items()}}]).to_csv(
        out_dir / "summary.csv", index=False
    )

    latest_regime = (
        bt["regime"].dropna().iloc[-1] if bt["regime"].notna().any() else "N/A"
    )
    latest_score = (
        round(float(bt["lumber_pressure_score"].dropna().iloc[-1]), 3)
        if bt["lumber_pressure_score"].notna().any()
        else float("nan")
    )

    print()
    print(f"LUMBER QUANT ENGINE v{__version__}")
    print(f"Mode             : {args.mode}")
    print(f"IC weights       : {not args.equal_weight}")
    print(f"Publication lags : {not args.no_lags}")
    print(f"Data start       : {args.start}")
    print(f"Backtest start   : {args.backtest_start or '(full series)'}")
    print(f"Latest regime    : {latest_regime}")
    print(f"Latest score     : {latest_score}")
    print(f"Stats            : {stats}")
    print(f"Bootstrap        : {boot}")
    print(f"Wrote {out_dir / 'lumber_engine_results.csv'}")
    print(f"Wrote {out_dir / 'summary.csv'}")


if __name__ == "__main__":
    main()
