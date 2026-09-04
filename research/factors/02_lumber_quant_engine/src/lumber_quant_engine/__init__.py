"""
Lumber Quant Engine
===================
Six-factor pressure / regime model for softwood lumber futures research.

Public API
----------
- LumberFactorEngine
- backtest, bootstrap_total_return
- load_live, make_demo
- load_nifc_annual_proxy, load_fred_rail_total
"""

from .core import (
    LumberFactorEngine,
    FactorWeights,
    backtest,
    bootstrap_total_return,
    apply_publication_lags,
    PUBLICATION_LAGS_MONTHS,
)
from .data import load_live, make_demo

__version__ = "0.3.0"
__all__ = [
    "LumberFactorEngine",
    "FactorWeights",
    "backtest",
    "bootstrap_total_return",
    "apply_publication_lags",
    "PUBLICATION_LAGS_MONTHS",
    "load_live",
    "make_demo",
    "__version__",
]
