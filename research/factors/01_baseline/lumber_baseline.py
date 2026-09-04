"""
===============================================================================
LUMBER PRICE BASELINE ANALYSIS
===============================================================================
Simple, clean starting point for softwood lumber futures research.

Ticker: LBR=F (CME Lumber continuous contract via Yahoo Finance)
===============================================================================
"""

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
TICKER = "LBR=F"
START  = "2015-01-01"

# -----------------------------------------------------------------------------
# Data
# -----------------------------------------------------------------------------
def load_lumber(start: str = START) -> pd.DataFrame:
    """Download CME Lumber futures and return a clean OHLCV DataFrame."""
    print(f"Downloading {TICKER} from {start}...")
    raw = yf.download(TICKER, start=start, progress=False, auto_adjust=True)

    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    df = raw[["Open", "High", "Low", "Close", "Volume"]].copy()
    df = df.dropna()
    df.index = pd.to_datetime(df.index)
    return df


def add_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add returns, realized vol, and simple moving averages."""
    out = df.copy()
    out["Return"] = np.log(out["Close"] / out["Close"].shift(1))
    out["RV_20D"] = out["Return"].rolling(20).std() * np.sqrt(252)
    out["MA_20"]  = out["Close"].rolling(20).mean()
    out["MA_60"]  = out["Close"].rolling(60).mean()
    out["MA_120"] = out["Close"].rolling(120).mean()
    return out


# -----------------------------------------------------------------------------
# Analysis helpers
# -----------------------------------------------------------------------------
def print_summary(df: pd.DataFrame):
    print("\n=== Basic Statistics ===")
    print(f"Period          : {df.index.min().date()} → {df.index.max().date()}")
    print(f"Observations    : {len(df)}")
    print(f"Mean Close      : ${df['Close'].mean():.2f}")
    print(f"Max Close       : ${df['Close'].max():.2f}")
    print(f"Min Close       : ${df['Close'].min():.2f}")
    print(f"Annualized Vol  : {df['Return'].std() * np.sqrt(252):.1%}")
    print(f"Skewness        : {df['Return'].skew():.2f}")
    print(f"Kurtosis        : {df['Return'].kurtosis():.2f}")


def plot_price_and_vol(df: pd.DataFrame):
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

    axes[0].plot(df.index, df["Close"], label="Close", color="#2c5f2d", linewidth=1.3)
    axes[0].plot(df.index, df["MA_20"], label="MA20", alpha=0.7)
    axes[0].plot(df.index, df["MA_60"], label="MA60", alpha=0.7)
    axes[0].set_title("CME Lumber Futures (LBR=F) — Price")
    axes[0].set_ylabel("USD / 1000 board feet")
    axes[0].legend(loc="upper left")
    axes[0].grid(True, alpha=0.3)

    axes[1].bar(df.index, df["Volume"], color="gray", alpha=0.6, width=1.5)
    axes[1].set_title("Volume")
    axes[1].set_ylabel("Contracts")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(df.index, df["RV_20D"], color="#d62828", linewidth=1.2)
    axes[2].set_title("20-Day Realized Volatility (Annualized)")
    axes[2].set_ylabel("Volatility")
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def seasonality_heatmap(df: pd.DataFrame):
    """Average monthly return heatmap."""
    tmp = df.copy()
    tmp["Year"]  = tmp.index.year
    tmp["Month"] = tmp.index.month
    monthly = tmp.groupby(["Year", "Month"])["Return"].sum().unstack()

    plt.figure(figsize=(12, 6))
    sns.heatmap(monthly, cmap="RdYlGn", center=0, annot=False)
    plt.title("Lumber Monthly Log-Return Seasonality")
    plt.xlabel("Month")
    plt.ylabel("Year")
    plt.tight_layout()
    plt.show()


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    lumber = load_lumber()
    lumber = add_basic_features(lumber)

    print_summary(lumber)
    plot_price_and_vol(lumber)
    seasonality_heatmap(lumber)

    # Optional: save clean series
    # lumber.to_csv("../../data/lumber_lbrf_daily.csv")
