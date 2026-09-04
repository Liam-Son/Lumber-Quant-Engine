from __future__ import annotations
import io
from pathlib import Path
import numpy as np
import pandas as pd

FRED = {
 'building_permits':'PERMIT','housing_starts':'HOUST','mortgage_rate_30y':'MORTGAGE30US',
 'truck_tonnage':'TRUCKD11','home_improvement_sales':'MRTSSM444USS','housing_affordability':'FIXHAI'
}

def fred_csv(series_id: str) -> pd.Series:
    url=f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}'
    d=pd.read_csv(url); d.columns=['date',series_id]; d['date']=pd.to_datetime(d['date']); d[series_id]=pd.to_numeric(d[series_id],errors='coerce')
    return d.set_index('date')[series_id]

def yahoo_lumber(start='2000-01-01') -> pd.Series:
    import yfinance as yf
    d=yf.download('LBR=F',start=start,auto_adjust=True,progress=False)
    if d.empty: raise RuntimeError('No Yahoo lumber data returned')
    s=d['Close'];
    if isinstance(s,pd.DataFrame): s=s.iloc[:,0]
    return s.rename('lumber_price')

def load_live(start='2000-01-01') -> pd.DataFrame:
    frames=[]
    try: frames.append(yahoo_lumber(start))
    except Exception as e: print('WARN lumber:',e)
    for name,sid in FRED.items():
        try: frames.append(fred_csv(sid).rename(name))
        except Exception as e: print('WARN FRED',sid,e)
    if not frames: raise RuntimeError('No live sources available')
    x=pd.concat(frames,axis=1).sort_index().resample('MS').last().ffill()
    # optional CSV overrides/proxies
    p=Path('data/optional_factors.csv')
    if p.exists():
        o=pd.read_csv(p,parse_dates=['date'])
        if not o.empty and 'date' in o.columns:
            o=o.set_index('date')
            if not isinstance(o.index, pd.DatetimeIndex):
                o.index = pd.to_datetime(o.index)
            o=o.resample('MS').last()
            x=x.join(o,how='outer')
    return x.ffill()

def make_demo(start='2005-01-01', periods=250, seed=7):
    rng=np.random.default_rng(seed); idx=pd.date_range(start,periods=periods,freq='MS')
    cyc=np.sin(np.arange(periods)/11)+0.4*np.sin(np.arange(periods)/31)
    df=pd.DataFrame(index=idx)
    df['building_permits']=1400+180*cyc+rng.normal(0,50,periods)
    df['housing_starts']=1350+170*cyc+rng.normal(0,60,periods)
    df['mortgage_rate_30y']=4.5-0.4*cyc+rng.normal(0,.25,periods)
    df['mortgage_apps']=300+35*cyc+rng.normal(0,15,periods)
    df['housing_affordability']=120+12*cyc+rng.normal(0,4,periods)
    df['wildfire_acres']=np.maximum(0,rng.lognormal(11,1,periods)*(1+0.5*np.maximum(cyc,0)))
    df['drought_index']=rng.normal(0,1,periods)+.3*cyc
    df['mill_capacity_exposed']=rng.uniform(.8,1.2,periods)
    df['rail_lumber_carloads']=100+10*cyc+rng.normal(0,4,periods)
    df['truck_tonnage']=110+6*cyc+rng.normal(0,2,periods)
    df['canada_lumber_exports']=1000+120*cyc+rng.normal(0,45,periods)
    df['storm_damage_usd']=rng.lognormal(17,1.3,periods)*(rng.random(periods)<.18)
    df['storm_residential_exposure']=rng.uniform(.5,2,periods)
    df['home_depot_traffic']=100+9*cyc+rng.normal(0,3,periods)
    df['lowes_traffic']=100+8*cyc+rng.normal(0,3,periods)
    df['google_diy_trends']=50+8*cyc+rng.normal(0,4,periods)
    df['home_improvement_sales']=40000+3500*cyc+rng.normal(0,900,periods)
    # synthetic price loosely driven by housing cycle + shocks
    rr=.012*cyc + .006*rng.normal(size=periods)+.008*np.log1p(df['storm_damage_usd'])/20
    df['lumber_price']=450*np.exp(np.cumsum(rr))
    return df
