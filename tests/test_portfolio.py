import unittest
import os
import json
import tempfile
import sys
from pathlib import Path

TOUCHGRASS_ROOT = Path(__file__).resolve().parents[1]
if str(TOUCHGRASS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOUCHGRASS_ROOT))

try:
    from touchgrass.src.portfolio import PortfolioManager
except ImportError:
    from src.portfolio import PortfolioManager


class TestPortfolioManager(unittest.TestCase):

    def test_portfolio_add_and_remove(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "test_watchlist.json"
            pm = PortfolioManager(str(test_file))

            # Add item
            self.assertTrue(pm.add_to_watchlist("NVDA", target_entry=115.0, notes="Testing NVDA"))
            wl = pm.get_watchlist()
            self.assertEqual(len(wl), 1)
            self.assertEqual(wl[0]["symbol"], "NVDA")
            self.assertEqual(wl[0]["target_entry"], 115.0)

            # Update item
            pm.update_holding("NVDA", shares=10, avg_price=110.0)
            pf = pm.get_portfolio()
            self.assertEqual(len(pf), 1)
            self.assertEqual(pf[0]["symbol"], "NVDA")
            self.assertEqual(pf[0]["shares"], 10)

            # Remove item
            self.assertTrue(pm.remove_from_watchlist("NVDA"))
            self.assertEqual(len(pm.get_watchlist()), 0)


if __name__ == "__main__":
    unittest.main()
