"""
Auto Stock Discovery Engine for Touchgrass Trader.
Scans the market using BreakoutAnalysis (technical patterns & volume surges)
and Serenity (supply chain bottlenecks & KOL conviction).
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

TOUCHGRASS_ROOT = Path(__file__).resolve().parents[1]
PARENT_ROOT = TOUCHGRASS_ROOT.parent
for p in [str(PARENT_ROOT), str(TOUCHGRASS_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from touchgrass.subprojects.breakout.bridge import BreakoutBridge
    from touchgrass.subprojects.serenity.bridge import SerenityBridge
except ImportError:
    from subprojects.breakout.bridge import BreakoutBridge
    from subprojects.serenity.bridge import SerenityBridge


class AutoStockScanner:
    """Combines Breakout Screener and Serenity Bottleneck Discovery."""

    def __init__(self):
        self.breakout_screener = BreakoutBridge()
        self.serenity_screener = SerenityBridge()

    def discover_stocks(self, max_candidates: int = 5) -> List[Dict[str, Any]]:
        """
        Runs comprehensive stock discovery:
        1. US Market Technical Breakouts
        2. Supply Chain Bottleneck Leaders
        3. Filters duplicates and scores top candidates
        """
        candidates = []

        # 1. Breakout Candidates
        breakouts = self.breakout_screener.scan_us_market(max_results=max_candidates)
        for item in breakouts:
            candidates.append({
                "symbol": item["symbol"],
                "name": item["name"],
                "source": "Breakout Scanner (VCP/Volume Surge)",
                "pattern": item["pattern"],
                "target_price": item["current_price"],
                "score": item["score"],
                "notes": f"RS Rating: {item['rs_rating']}, Rel Vol: {item['rel_volume']}x"
            })

        # 2. Serenity Bottleneck Candidates
        bottlenecks = self.serenity_screener.get_supply_chain_candidates()
        for item in bottlenecks:
            # Check if already added
            if not any(c["symbol"] == item["symbol"] for c in candidates):
                candidates.append({
                    "symbol": item["symbol"],
                    "name": item["name"],
                    "source": "Serenity Supply Chain",
                    "pattern": item["bottleneck_type"],
                    "target_price": 0.0,
                    "score": item["conviction_score"],
                    "notes": item["reason"]
                })

        # Sort by conviction score
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates[:max_candidates]
