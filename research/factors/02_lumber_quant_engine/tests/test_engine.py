import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from lumber_quant_engine.data import make_demo
from lumber_quant_engine.core import LumberFactorEngine, backtest

def test_demo_pipeline():
    df = make_demo(periods=120)
    sig = LumberFactorEngine().build(df)
    assert "lumber_pressure_score" in sig.columns
    assert "regime" in sig.columns
    bt, stats = backtest(sig)
    assert "total_return" in stats
    assert "sharpe" in stats
    print("test_demo_pipeline passed")

if __name__ == "__main__":
    test_demo_pipeline()
