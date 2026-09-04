"""
Lumber Quant Engine v0.2
- Demo / Live modes
- Publication lags (no look-ahead on FRED)
- Expanding-window IC weights (falls back to equal weight)
- Configurable data start + backtest evaluation window
"""
import argparse
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent / "src"))
from lumber_quant_engine.data import load_live, make_demo
from lumber_quant_engine.core import LumberFactorEngine, backtest, bootstrap_total_return


def main():
    ap = argparse.ArgumentParser(description="Lumber Quant Engine v0.2")
    ap.add_argument("--mode", choices=["demo", "live"], default="demo")
    ap.add_argument("--start", default="2005-01-01",
                    help="Data download / generation start date")
    ap.add_argument("--backtest-start", default=None,
                    help="Only evaluate performance from this date (e.g. 2020-01-01)")
    ap.add_argument("--threshold", type=float, default=0.75)
    ap.add_argument("--equal-weight", action="store_true",
                    help="Disable IC weighting and use static equal weights")
    args = ap.parse_args()

    Path("outputs").mkdir(exist_ok=True)

    if args.mode == "demo":
        df = make_demo(start=args.start)
    else:
        df = load_live(args.start)

    engine = LumberFactorEngine(
        use_ic_weights=not args.equal_weight,
        apply_lags=True,
    )
    sig = engine.build(df)

    if args.backtest_start:
        sig = sig.loc[args.backtest_start:].copy()
        print(f"[Info] Backtest evaluation window starts at {args.backtest_start}")

    bt, stats = backtest(sig, threshold=args.threshold)
    boot = bootstrap_total_return(bt["strategy_ret"])

    bt.to_csv("outputs/lumber_engine_results.csv")
    pd.DataFrame([{**stats, **{f"bootstrap_{k}": v for k, v in boot.items()}}]).to_csv(
        "outputs/summary.csv", index=False
    )

    print("\nLUMBER QUANT ENGINE v0.2")
    print("Mode            :", args.mode)
    print("IC weights      :", not args.equal_weight)
    print("Publication lags:", True)
    print("Data start      :", args.start)
    print("Backtest start  :", args.backtest_start or "(full series)")
    print("Latest regime   :", bt["regime"].dropna().iloc[-1] if bt["regime"].notna().any() else "N/A")
    print("Latest score    :", round(float(bt["lumber_pressure_score"].dropna().iloc[-1]), 3))
    print("Stats           :", stats)
    print("Bootstrap       :", boot)
    print("Saved outputs/lumber_engine_results.csv and outputs/summary.csv")


if __name__ == "__main__":
    main()
