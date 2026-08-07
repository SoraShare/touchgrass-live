"""
Touchgrass Orchestrator Engine.
Coordinates daily market runs (Morning run at 2h post-open, Afternoon run at 2h pre-close),
watchlist analysis, auto stock discovery, and report generation.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

TOUCHGRASS_ROOT = Path(__file__).resolve().parents[1]
PARENT_ROOT = TOUCHGRASS_ROOT.parent
for p in [str(PARENT_ROOT), str(TOUCHGRASS_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from touchgrass.src.portfolio import PortfolioManager
    from touchgrass.src.scanner import AutoStockScanner
    from touchgrass.src.analyzer import StockAnalyzer
    from touchgrass.src.notifier import Notifier
except ImportError:
    from src.portfolio import PortfolioManager
    from src.scanner import AutoStockScanner
    from src.analyzer import StockAnalyzer
    from src.notifier import Notifier


class TouchgrassEngine:
    """Core execution engine for Touchgrass Trader."""

    def __init__(self, portfolio_file: Optional[str] = None):
        self.portfolio_mgr = PortfolioManager(portfolio_file)
        self.scanner = AutoStockScanner()
        self.analyzer = StockAnalyzer()
        self.notifier = Notifier()

    def run_market_round(self, run_type: str = "scheduled", auto_add_scanned: bool = True) -> Dict[str, Any]:
        """
        Executes one full round of market analysis:
        1. Analyzes existing watchlist stocks
        2. Runs market-wide stock scanner (Breakout + Supply Chain)
        3. Optionally auto-adds top discovered candidate to watchlist
        4. Generates decision report and dispatches notification
        """
        print(f"🌿 Starting Touchgrass Market Round: {run_type.upper()}...")

        # 1. Analyze existing watchlist
        watchlist = self.portfolio_mgr.get_watchlist()
        watchlist_results = []
        for item in watchlist:
            symbol = item["symbol"]
            analysis = self.analyzer.analyze_stock(symbol)
            watchlist_results.append(analysis)

        # 2. Discover new candidates
        candidates = self.scanner.discover_stocks(max_candidates=3)

        # 3. Auto-add top candidate if enabled
        if auto_add_scanned and candidates:
            top_candidate = candidates[0]
            self.portfolio_mgr.add_to_watchlist(
                symbol=top_candidate["symbol"],
                name=top_candidate["name"],
                notes=f"Auto-discovered via {top_candidate['source']}"
            )

        # 4. Generate & dispatch report
        report = self.notifier.format_report_markdown(run_type, watchlist_results, candidates)
        self.notifier.dispatch(report)

        return {
            "run_type": run_type,
            "analyzed_count": len(watchlist_results),
            "discovered_candidates": candidates,
            "report_markdown": report
        }
