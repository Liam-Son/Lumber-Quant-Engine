"""
Alternative-data helpers for Lumber Quant Engine
------------------------------------------------
1. load_nifc_annual_proxy()  – turns annual NIFC acres into a monthly series
2. scaffold downloaders for NIFC / NOAA (documented, ready to extend)
"""
from __future__ import annotations
from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd

DEFAULT_NIFC_CSV = Path(__file__).resolve().parents[2] / "data" / "nifc_wildfire_annual.csv"


def load_nifc_annual_proxy(
    csv_path: Optional[Path | str] = None,
    method: str = "seasonal",
) -> pd.Series:
    """
    Load annual NIFC wildfire acres and expand to a monthly series.

    method: 'seasonal' | 'flat' | 'front'
    """
    path = Path(csv_path) if csv_path else DEFAULT_NIFC_CSV
    if not path.exists():
        raise FileNotFoundError(
            f"NIFC annual file not found: {path}\n"
            "Place a CSV with columns [year, acres] in data/nifc_wildfire_annual.csv"
        )

    ann = pd.read_csv(path)
    if "acres" not in ann.columns or "year" not in ann.columns:
        raise ValueError("CSV must contain 'year' and 'acres' columns")

    ann["year"] = ann["year"].astype(int)
    ann = ann.set_index("year")["acres"].sort_index()

    seasonal_w = np.array([
        0.02, 0.02, 0.03, 0.04, 0.06,
        0.12, 0.18, 0.20, 0.15, 0.10,
        0.05, 0.03,
    ])
    seasonal_w = seasonal_w / seasonal_w.sum()

    rows = []
    for year, acres in ann.items():
        if method == "flat":
            weights = np.full(12, 1 / 12)
        elif method == "front":
            weights = np.zeros(12)
            weights[7] = 1.0
        else:
            weights = seasonal_w

        for m, w in enumerate(weights, start=1):
            rows.append({
                "date": pd.Timestamp(year=year, month=m, day=1),
                "wildfire_acres": acres * w,
            })

    s = pd.DataFrame(rows).set_index("date")["wildfire_acres"]
    s.name = "wildfire_acres"
    return s


def scaffold_nifc_notes() -> str:
    return """
NIFC / Wildfire data sources
----------------------------
1. Annual totals (shipped as data/nifc_wildfire_annual.csv)
   https://www.nifc.gov/fire-information/statistics/wildfires

2. Monthly / YTD situation reports (PDF / HTML – needs scraping)
   https://www.nifc.gov/fire-information/nfn

3. Spatial fire-occurrence (best for true mill-exposure work)
   - FPA-FOD (USFS)
   - MTBS: https://www.mtbs.gov/
   - NIFC Open Data: https://data-nifc.opendata.arcgis.com/

4. Research-grade Burning Timber:
   Intersect fire polygons with sawmill / timberland capacity layers.
"""


def scaffold_noaa_disaster_notes() -> str:
    return """
NOAA / Storm & Disaster data sources
------------------------------------
1. Billion-Dollar Weather and Climate Disasters (event-level)
   https://www.ncei.noaa.gov/access/billions/

2. Storm Events Database (1950–present)
   https://www.ncei.noaa.gov/stormevents/

3. Practical monthly reconstruction:
   Filter high-damage events → aggregate by month → lag 1–2 months.
"""


def try_download_nifc_annual_placeholder() -> pd.DataFrame:
    path = DEFAULT_NIFC_CSV
    if path.exists():
        return pd.read_csv(path)
    raise FileNotFoundError("No local NIFC annual CSV and live download not yet implemented")


if __name__ == "__main__":
    s = load_nifc_annual_proxy()
    print(s.tail(12))
    print("\nAnnual total check (2024):", s.loc["2024"].sum())
    print(scaffold_nifc_notes())
