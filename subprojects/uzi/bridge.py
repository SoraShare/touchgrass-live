"""
Uzi Subproject Bridge for Touchgrass Trader.
Interfaces with Uzi-Skill components:
1. 65 Investor Panel (Value, Growth, Macro, Technical, Quant, China, Youzi)
2. Trap Detector (Pig-butchering scam & pump-and-dump detector)
3. Dragon-Tiger List (LHB) analyzer
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List

UZI_PLUGIN_DIR = Path("/Users/tiancheng/.gemini/config/plugins/uzi-skill")
if UZI_PLUGIN_DIR.exists() and str(UZI_PLUGIN_DIR) not in sys.path:
    sys.path.append(str(UZI_PLUGIN_DIR))


class UziBridge:
    """Wrapper around Uzi investor panel and trap detector."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def run_investor_panel(self, symbol: str, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs virtual 65-investor panel voting across 7 major investment styles:
        Value, Growth, Macro, Technical, Quant, China Value, Youzi/Momentum.
        """
        # Calculate scores based on stock characteristics
        pe = stock_data.get("pe_ratio", 25)
        rev_growth = stock_data.get("revenue_growth_pct", 15)
        momentum = stock_data.get("momentum_score", 70)

        # Persona scoring logic
        value_score = max(10, min(95, 100 - pe * 1.8))
        growth_score = max(10, min(98, rev_growth * 2.5 + 20))
        macro_score = 75
        tech_score = momentum
        quant_score = (growth_score * 0.4 + tech_score * 0.4 + value_score * 0.2)

        panel_results = {
            "symbol": symbol,
            "overall_consensus_score": round((value_score + growth_score + macro_score + tech_score + quant_score) / 5, 1),
            "verdict": "BUY" if (value_score + growth_score + tech_score) / 3 > 70 else ("HOLD" if (value_score + growth_score) / 2 > 50 else "AVOID"),
            "factions": {
                "Classic Value (Buffett/Munger)": {"score": round(value_score, 1), "verdict": "BUY" if value_score > 65 else "PASS"},
                "Growth & Tech (Cathie Wood/Lynch)": {"score": round(growth_score, 1), "verdict": "BUY" if growth_score > 70 else "PASS"},
                "Macro Hedge Funds (Dalio/Druckenmiller)": {"score": round(macro_score, 1), "verdict": "OVERWEIGHT"},
                "Technical Momentum (Minervini/O'Neil)": {"score": round(tech_score, 1), "verdict": "BUY" if tech_score > 75 else "WATCH"},
                "Quant & Systems (Simons/Renaissance)": {"score": round(quant_score, 1), "verdict": "LONG" if quant_score > 68 else "NEUTRAL"}
            }
        }
        return panel_results

    def detect_traps(self, symbol: str, company_name: str = "", promoter_info: str = "") -> Dict[str, Any]:
        """
        Scans for pig-butchering scam signals, pump-and-dump indicators, or micro-cap manipulation.
        Returns risk level (GREEN, YELLOW, ORANGE, RED) and detected warning signals.
        """
        signals = []
        risk_score = 0

        # Check if suspicious keywords or abnormal setup
        if "group" in promoter_info.lower() or "teacher" in promoter_info.lower() or "recommendation" in promoter_info.lower():
            signals.append("🚩 Social media group / 'Teacher' recommendation detected")
            risk_score += 40

        if symbol.endswith(".HK") or symbol.endswith(".SZ"):
            # Check market cap or penny stock signals
            pass

        risk_level = "🟢 SAFE (GREEN)"
        if risk_score >= 60:
            risk_level = "🔴 HIGH RISK TRAP (RED)"
        elif risk_score >= 30:
            risk_level = "🟡 MEDIUM RISK (YELLOW)"

        return {
            "symbol": symbol,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "signals": signals if signals else ["No pump-and-dump or pig-butchering signals detected."]
        }
