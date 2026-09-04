"""
Core factor engine, IC weighting, publication lags, and backtest.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd


def zscore(s: pd.Series, window: int = 24) -> pd.Series:
    """Rolling z-score with defensive min_periods."""
    m = s.rolling(window, min_periods=max(6, window // 3)).mean()
    sd = s.rolling(window, min_periods=max(6, window // 3)).std()
    return (s - m) / sd.replace(0, np.nan)


def pct_mom(s: pd.Series, periods: int = 1) -> pd.Series:
    return s.pct_change(periods)


PUBLICATION_LAGS_MONTHS: dict[str, int] = {
    "building_permits": 1,
    "housing_starts": 1,
    "mortgage_rate_30y": 0,
    "mortgage_apps": 0,
    "housing_affordability": 1,
    "truck_tonnage": 1,
    "home_improvement_sales": 1,
    "wildfire_acres": 1,
    "drought_index": 1,
    "rail_lumber_carloads": 1,
    "canada_lumber_exports": 2,
    "storm_damage_usd": 1,
    "storm_residential_exposure": 1,
    "home_depot_traffic": 1,
    "lowes_traffic": 1,
    "google_diy_trends": 0,
    "mill_capacity_exposed": 0,
}


def apply_publication_lags(
    df: pd.DataFrame, lags: Optional[dict[str, int]] = None
) -> pd.DataFrame:
    lags = lags or PUBLICATION_LAGS_MONTHS
    out = df.copy()
    for col, lag in lags.items():
        if col in out.columns and lag > 0:
            out[col] = out[col].shift(int(lag))
    return out


@dataclass
class FactorWeights:
    burning_timber: float = 1 / 6
    permit_to_plank: float = 1 / 6
    mortgage_choke: float = 1 / 6
    wood_on_wheels: float = 1 / 6
    rebuild: float = 1 / 6
    weekend_warrior: float = 1 / 6

    def as_dict(self) -> dict[str, float]:
        return {
            "burning_timber": self.burning_timber,
            "permit_to_plank": self.permit_to_plank,
            "mortgage_choke": self.mortgage_choke,
            "wood_on_wheels": self.wood_on_wheels,
            "rebuild": self.rebuild,
            "weekend_warrior": self.weekend_warrior,
        }


FACTOR_NAMES = list(FactorWeights().as_dict().keys())


class LumberFactorEngine:
    """Six-factor lumber pressure model."""

    def __init__(
        self,
        weights: Optional[FactorWeights] = None,
        z_window: int = 24,
        use_ic_weights: bool = True,
        ic_min_periods: int = 24,
        apply_lags: bool = True,
    ):
        self.weights = weights or FactorWeights()
        self.z_window = z_window
        self.use_ic_weights = use_ic_weights
        self.ic_min_periods = ic_min_periods
        self.apply_lags = apply_lags

    def _build_raw_factors(self, x: pd.DataFrame) -> pd.DataFrame:
        idx = x.index

        def col(name: str, default: float | None = None) -> pd.Series:
            if name in x.columns:
                return x[name]
            if default is None:
                return pd.Series(np.nan, index=idx, dtype=float)
            return pd.Series(default, index=idx, dtype=float)

        fire = col("wildfire_acres")
        drought = col("drought_index", 0.0)
        mill = col("mill_capacity_exposed", 1.0)
        x["burning_timber"] = (
            zscore(np.log1p(fire.clip(lower=0)) * mill.clip(lower=0), self.z_window)
            + 0.35 * zscore(drought, self.z_window)
        )

        permits = col("building_permits")
        starts = col("housing_starts")
        impulse = (
            0.50 * pct_mom(permits, 1)
            + 0.30 * pct_mom(permits, 3)
            + 0.20 * pct_mom(starts, 1)
        )
        x["permit_to_plank"] = zscore(impulse, self.z_window)

        mort = col("mortgage_rate_30y")
        apps = col("mortgage_apps")
        afford = col("housing_affordability")
        choke = zscore(mort.diff(), self.z_window) - zscore(apps.pct_change(), self.z_window)
        if afford.notna().any():
            choke = choke - 0.5 * zscore(afford.pct_change(), self.z_window)
        x["mortgage_choke"] = -choke

        rail = col("rail_lumber_carloads")
        truck = col("truck_tonnage")
        exports = col("canada_lumber_exports")
        x["wood_on_wheels"] = (
            0.45 * zscore(rail.pct_change(), self.z_window)
            + 0.25 * zscore(truck.pct_change(), self.z_window)
            + 0.30 * zscore(exports.pct_change(), self.z_window)
        )

        # Rebuild v2: 65% 12m level + 35% spike; lag=1 on storm series
        storm = col("storm_damage_usd")
        exposure = col("storm_residential_exposure", 1.0)
        log_dmg = np.log1p(storm.clip(lower=0)) * np.sqrt(exposure.clip(lower=0.1))
        w = min(12, max(6, self.z_window // 2))
        level = zscore(log_dmg, window=w)
        spike = zscore(log_dmg.diff(1), window=w)
        x["rebuild"] = (0.65 * level + 0.35 * spike).clip(-4.0, 4.0)

        hd = col("home_depot_traffic")
        low = col("lowes_traffic")
        diy = col("google_diy_trends")
        retail = col("home_improvement_sales")
        x["weekend_warrior"] = (
            0.30 * zscore(hd.pct_change(), self.z_window)
            + 0.25 * zscore(low.pct_change(), self.z_window)
            + 0.25 * zscore(diy, self.z_window)
            + 0.20 * zscore(retail.pct_change(), self.z_window)
        )

        for c in FACTOR_NAMES:
            x[c] = x[c].replace([np.inf, -np.inf], np.nan).clip(-4.0, 4.0)
        return x

    def _expanding_ic_weights(
        self, factors: pd.DataFrame, fwd_ret: pd.Series, min_periods: int
    ) -> pd.DataFrame:
        ics = pd.DataFrame(index=factors.index, columns=FACTOR_NAMES, dtype=float)
        for c in FACTOR_NAMES:
            pair = pd.concat([factors[c], fwd_ret], axis=1).dropna()
            if len(pair) < min_periods:
                continue
            roll = pair.iloc[:, 0].expanding(min_periods=min_periods).corr(pair.iloc[:, 1])
            ics[c] = roll.reindex(factors.index)
        w = ics.clip(lower=0.0)
        row_sum = w.sum(axis=1).replace(0, np.nan)
        return w.div(row_sum, axis=0)

    def build(self, df: pd.DataFrame) -> pd.DataFrame:
        x = df.copy().sort_index()
        if self.apply_lags:
            x = apply_publication_lags(x)
        x = self._build_raw_factors(x)
        if "lumber_price" in x.columns:
            fwd = x["lumber_price"].pct_change().shift(-1)
        else:
            fwd = pd.Series(np.nan, index=x.index)
        if self.use_ic_weights:
            w_df = self._expanding_ic_weights(x[FACTOR_NAMES], fwd, self.ic_min_periods)
            equal = {c: 1.0 / len(FACTOR_NAMES) for c in FACTOR_NAMES}
            num = pd.Series(0.0, index=x.index)
            den = pd.Series(0.0, index=x.index)
            for c in FACTOR_NAMES:
                w = w_df[c].fillna(equal[c])
                num = num + x[c].fillna(0.0) * w
                den = den + x[c].notna().astype(float) * w
            x["lumber_pressure_score"] = (num / den.replace(0, np.nan)).clip(-4.0, 4.0)
            x["ic_weight_coverage"] = den
        else:
            w = self.weights.as_dict()
            num = sum(x[c].fillna(0.0) * w[c] for c in FACTOR_NAMES)
            den = sum(x[c].notna().astype(float) * w[c] for c in FACTOR_NAMES)
            den = den.replace(0, np.nan)
            x["lumber_pressure_score"] = (num / den).clip(-4.0, 4.0)
        x["regime"] = pd.cut(
            x["lumber_pressure_score"],
            bins=[-np.inf, -0.75, 0.75, np.inf],
            labels=["GLUT/BEAR", "NORMAL", "SHORTAGE/BULL"],
        )
        return x


def backtest(
    signals: pd.DataFrame,
    price_col: str = "lumber_price",
    score_col: str = "lumber_pressure_score",
    threshold: float = 0.75,
    cost_bps: float = 5.0,
) -> tuple[pd.DataFrame, dict]:
    if price_col not in signals.columns:
        raise KeyError(f"Missing price column '{price_col}'")
    x = signals.copy()
    x["ret"] = x[price_col].pct_change()
    pos = np.where(
        x[score_col] > threshold, 1.0, np.where(x[score_col] < -threshold, -1.0, 0.0)
    )
    x["position"] = pd.Series(pos, index=x.index).shift(1).fillna(0.0)
    turnover = x["position"].diff().abs().fillna(0.0)
    x["strategy_ret"] = x["position"] * x["ret"] - turnover * (cost_bps / 10_000.0)
    x["equity"] = (1.0 + x["strategy_ret"].fillna(0.0)).cumprod()
    med_days = 30
    if len(x.index) > 1:
        med_days = x.index.to_series().diff().median().days or 30
    ann = 12 if med_days > 7 else 252
    r = x["strategy_ret"].dropna()
    total = float(x["equity"].iloc[-1] - 1.0) if len(x) else np.nan
    sharpe = float(r.mean() / r.std() * math.sqrt(ann)) if len(r) and r.std() > 0 else np.nan
    dd = x["equity"] / x["equity"].cummax() - 1.0
    stats = {
        "total_return": total,
        "sharpe": sharpe,
        "max_drawdown": float(dd.min()) if len(dd) else np.nan,
        "trades": int((turnover > 0).sum()),
        "ann_factor": ann,
    }
    return x, stats


def bootstrap_total_return(
    r: pd.Series, n: int = 2000, seed: int = 42
) -> dict[str, float]:
    arr = r.dropna().to_numpy()
    if len(arr) == 0:
        return {}
    rng = np.random.default_rng(seed)
    sims = [
        float(np.prod(1.0 + rng.choice(arr, size=len(arr), replace=True)) - 1.0)
        for _ in range(n)
    ]
    q = np.quantile(sims, [0.025, 0.50, 0.975])
    return {"p2_5": float(q[0]), "median": float(q[1]), "p97_5": float(q[2])}
