"""Unit tests for Lumber Quant Engine."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lumber_quant_engine import (
    LumberFactorEngine,
    backtest,
    bootstrap_total_return,
    make_demo,
    apply_publication_lags,
)
from lumber_quant_engine.alt_data import load_nifc_annual_proxy


def test_demo_pipeline_runs():
    df = make_demo(periods=120)
    sig = LumberFactorEngine(use_ic_weights=False).build(df)
    assert "lumber_pressure_score" in sig.columns
    assert "regime" in sig.columns
    assert sig["lumber_pressure_score"].notna().sum() > 50
    bt, stats = backtest(sig)
    assert "total_return" in stats
    assert "sharpe" in stats
    assert np.isfinite(stats["total_return"])


def test_ic_weights_pipeline():
    df = make_demo(periods=180)
    sig = LumberFactorEngine(use_ic_weights=True, ic_min_periods=24).build(df)
    assert "lumber_pressure_score" in sig.columns
    bt, stats = backtest(sig)
    assert stats["trades"] >= 0


def test_publication_lags_shift():
    idx = pd.date_range("2020-01-01", periods=6, freq="MS")
    df = pd.DataFrame({"building_permits": range(6)}, index=idx)
    lagged = apply_publication_lags(df, {"building_permits": 1})
    assert pd.isna(lagged["building_permits"].iloc[0])
    assert lagged["building_permits"].iloc[1] == 0


def test_nifc_proxy_preserves_annual_total():
    s = load_nifc_annual_proxy()
    assert abs(s.loc["2024"].sum() - 8_924_884) < 1.0


def test_bootstrap_empty():
    assert bootstrap_total_return(pd.Series(dtype=float)) == {}


def test_bootstrap_runs():
    r = pd.Series(np.random.default_rng(0).normal(0.001, 0.02, 60))
    out = bootstrap_total_return(r, n=200)
    assert "median" in out
    assert out["p2_5"] <= out["median"] <= out["p97_5"]
