"""
Lumber Quant Engine v3
======================
Six-factor pressure / regime model for softwood lumber futures research.

Public API
----------
- LumberFactorEngine
- backtest, bootstrap_total_return
- load_live, make_demo
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

__version__ = "3.0.0"
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
