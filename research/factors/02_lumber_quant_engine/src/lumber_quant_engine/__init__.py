"""
Lumber Quant Engine v3.1
========================
Six-factor pressure / regime model for softwood lumber futures research.
"""
from .core import (
    LumberFactorEngine,
    FactorWeights,
    backtest,
    bootstrap_total_return,
    apply_publication_lags,
    PUBLICATION_LAGS_MONTHS,
    FACTOR_NAMES,
)
from .data import load_live, make_demo

try:
    from .alt_data import load_shfe_pulp_usd, refresh_shfe_pulp_front
except Exception:  # pragma: no cover
    load_shfe_pulp_usd = None  # type: ignore
    refresh_shfe_pulp_front = None  # type: ignore

__version__ = "3.1.0"
__all__ = [
    "LumberFactorEngine",
    "FactorWeights",
    "backtest",
    "bootstrap_total_return",
    "apply_publication_lags",
    "PUBLICATION_LAGS_MONTHS",
    "FACTOR_NAMES",
    "load_live",
    "make_demo",
    "load_shfe_pulp_usd",
    "refresh_shfe_pulp_front",
    "__version__",
]
