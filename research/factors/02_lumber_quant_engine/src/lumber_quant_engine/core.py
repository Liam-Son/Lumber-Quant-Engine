from __future__ import annotations
import math, warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Dict
import numpy as np
import pandas as pd


def zscore(s: pd.Series, window: int = 24) -> pd.Series:
    m = s.rolling(window, min_periods=max(6, window//3)).mean()
    sd = s.rolling(window, min_periods=max(6, window//3)).std()
    return (s-m)/sd.replace(0, np.nan)


def pct_mom(s: pd.Series, periods: int = 1) -> pd.Series:
    return s.pct_change(periods)

@dataclass
class FactorWeights:
    burning_timber: float = 1/6
    permit_to_plank: float = 1/6
    mortgage_choke: float = 1/6
    wood_on_wheels: float = 1/6
    rebuild: float = 1/6
    weekend_warrior: float = 1/6

class LumberFactorEngine:
    """Six-factor lumber pressure engine. Positive score = bullish lumber pressure."""
    def __init__(self, weights: FactorWeights | None = None, z_window: int = 24):
        self.weights = weights or FactorWeights()
        self.z_window = z_window

    def build(self, df: pd.DataFrame) -> pd.DataFrame:
        x = df.copy().sort_index()
        # 1) Burning Timber: fire exposure / mill capacity proxy / drought
        fire = x.get('wildfire_acres', pd.Series(index=x.index, dtype=float))
        drought = x.get('drought_index', pd.Series(0.0, index=x.index))
        mill = x.get('mill_capacity_exposed', pd.Series(1.0, index=x.index))
        x['burning_timber'] = zscore(np.log1p(fire.clip(lower=0))*mill.clip(lower=0), self.z_window) + 0.35*zscore(drought, self.z_window)

        # 2) Permit-to-Plank: permits/starts with lag structure
        permits = x.get('building_permits', pd.Series(index=x.index, dtype=float))
        starts = x.get('housing_starts', pd.Series(index=x.index, dtype=float))
        permit_impulse = 0.5*pct_mom(permits, 1).shift(1) + 0.3*pct_mom(permits, 3).shift(1) + 0.2*pct_mom(starts, 1).shift(1)
        x['permit_to_plank'] = zscore(permit_impulse, self.z_window)

        # 3) Mortgage Choke: higher rates + weaker applications = bearish, so invert
        mort = x.get('mortgage_rate_30y', pd.Series(index=x.index, dtype=float))
        apps = x.get('mortgage_apps', pd.Series(index=x.index, dtype=float))
        affordability = x.get('housing_affordability', pd.Series(index=x.index, dtype=float))
        choke = zscore(mort.diff(), self.z_window) - zscore(apps.pct_change(), self.z_window)
        if affordability.notna().any():
            choke += -0.5*zscore(affordability.pct_change(), self.z_window)
        x['mortgage_choke'] = -choke

        # 4) Wood on Wheels: rail/truck/export physical flow
        rail = x.get('rail_lumber_carloads', pd.Series(index=x.index, dtype=float))
        truck = x.get('truck_tonnage', pd.Series(index=x.index, dtype=float))
        exports = x.get('canada_lumber_exports', pd.Series(index=x.index, dtype=float))
        physical = 0.45*zscore(rail.pct_change(), self.z_window) + 0.25*zscore(truck.pct_change(), self.z_window) + 0.30*zscore(exports.pct_change(), self.z_window)
        x['wood_on_wheels'] = physical

        # 5) Rebuild: disaster intensity x exposed population/property
        storm = x.get('storm_damage_usd', pd.Series(index=x.index, dtype=float))
        exposure = x.get('storm_residential_exposure', pd.Series(1.0, index=x.index))
        x['rebuild'] = zscore(np.log1p(storm.clip(lower=0))*np.sqrt(exposure.clip(lower=0)), self.z_window).shift(1)

        # 6) Weekend Warrior: home improvement/DIY attention + retailer traffic proxies
        hd = x.get('home_depot_traffic', pd.Series(index=x.index, dtype=float))
        low = x.get('lowes_traffic', pd.Series(index=x.index, dtype=float))
        diy = x.get('google_diy_trends', pd.Series(index=x.index, dtype=float))
        retail = x.get('home_improvement_sales', pd.Series(index=x.index, dtype=float))
        x['weekend_warrior'] = 0.30*zscore(hd.pct_change(), self.z_window) + 0.25*zscore(low.pct_change(), self.z_window) + 0.25*zscore(diy, self.z_window) + 0.20*zscore(retail.pct_change(), self.z_window)

        cols = list(self.weights.__dict__.keys())
        for c in cols:
            x[c] = x[c].replace([np.inf,-np.inf], np.nan).clip(-4,4)
        w = self.weights.__dict__
        num = sum(x[c].fillna(0)*w[c] for c in cols)
        den = sum((x[c].notna().astype(float))*w[c] for c in cols).replace(0,np.nan)
        x['lumber_pressure_score'] = (num/den).clip(-4,4)
        x['regime'] = pd.cut(x['lumber_pressure_score'], [-np.inf,-0.75,0.75,np.inf], labels=['GLUT/BEAR','NORMAL','SHORTAGE/BULL'])
        return x


def backtest(signals: pd.DataFrame, price_col='lumber_price', score_col='lumber_pressure_score', threshold=0.75, cost_bps=5):
    x = signals.copy()
    x['ret'] = x[price_col].pct_change()
    x['position'] = np.where(x[score_col] > threshold, 1, np.where(x[score_col] < -threshold, -1, 0))
    x['position'] = pd.Series(x['position'], index=x.index).shift(1).fillna(0)
    turnover = pd.Series(x['position'], index=x.index).diff().abs().fillna(0)
    x['strategy_ret'] = x['position']*x['ret'] - turnover*(cost_bps/10000)
    x['equity'] = (1+x['strategy_ret'].fillna(0)).cumprod()
    ann = 12 if len(x.index)>1 and (x.index.to_series().diff().median().days or 30) > 7 else 252
    r=x['strategy_ret'].dropna(); total=x['equity'].iloc[-1]-1
    sharpe=(r.mean()/r.std()*math.sqrt(ann)) if r.std()>0 else np.nan
    dd=x['equity']/x['equity'].cummax()-1
    stats={'total_return':float(total),'sharpe':float(sharpe) if pd.notna(sharpe) else np.nan,'max_drawdown':float(dd.min()),'trades':int((turnover>0).sum())}
    return x, stats


def bootstrap_total_return(r: pd.Series, n=2000, seed=42):
    r=r.dropna().to_numpy(); rng=np.random.default_rng(seed)
    if len(r)==0: return {}
    sims=[]
    for _ in range(n):
        s=rng.choice(r,size=len(r),replace=True); sims.append(np.prod(1+s)-1)
    q=np.quantile(sims,[.025,.5,.975])
    return {'p2_5':float(q[0]),'median':float(q[1]),'p97_5':float(q[2])}
