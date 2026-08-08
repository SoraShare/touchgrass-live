import unittest
import tempfile
import sys
from pathlib import Path

TOUCHGRASS_ROOT = Path(__file__).resolve().parents[1]
if str(TOUCHGRASS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOUCHGRASS_ROOT))

try:
    from touchgrass.src.scanner import AutoStockScanner
    from touchgrass.src.analyzer import StockAnalyzer
    from touchgrass.src.engine import TouchgrassEngine
except ImportError:
    from src.scanner import AutoStockScanner
    from src.analyzer import StockAnalyzer
    from src.engine import TouchgrassEngine


class TestTouchgrassEngine(unittest.TestCase):

    def test_auto_stock_scanner(self):
        scanner = AutoStockScanner()
        results = scanner.discover_stocks(max_candidates=3)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertIn("symbol", results[0])
        self.assertIn("score", results[0])

    def test_stock_analyzer(self):
        analyzer = StockAnalyzer()
        res = analyzer.analyze_stock("NVDA")
        self.assertEqual(res["symbol"], "NVDA")
        self.assertIn("touchgrass_score", res)
        self.assertIn(res["recommended_action"], ["BUY", "HOLD", "SELL / AVOID"])

    def test_touchgrass_engine_run(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_wl = Path(tmp_dir) / "wl.json"
            engine = TouchgrassEngine(portfolio_file=str(test_wl))
            res = engine.run_market_round(run_type="test", auto_add_scanned=True)
            self.assertEqual(res["run_type"], "test")
            self.assertIn("report_markdown", res)


if __name__ == "__main__":
    unittest.main()
