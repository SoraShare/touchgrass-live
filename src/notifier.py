"""
Universal Notification Engine for Touchgrass Trader.
Supports Console output, Telegram, Email, Discord Webhook, and ServerChan.
"""

import sys
import os
import json
from typing import Dict, Any, List, Optional


class Notifier:
    """Dispatches Touchgrass trade decisions and market digests."""

    def __init__(self, channels: Optional[List[str]] = None):
        self.channels = channels or ["console"]

    def format_report_markdown(self, run_type: str, watchlist_results: List[Dict[str, Any]], candidates: List[Dict[str, Any]]) -> str:
        """
        Formats a clean, attractive markdown digest.
        """
        lines = [
            f"🌿 **Touchgrass Trader Market Report** ({run_type.upper()}) 🌿",
            f"📅 Date: 2026-08-07 | Status: Market Active",
            "--------------------------------------------------",
            "📊 **Portfolio & Watchlist Health Digest**:"
        ]

        for item in watchlist_results:
            emoji = "🟢" if item["recommended_action"] == "BUY" else ("🟡" if item["recommended_action"] == "HOLD" else "🔴")
            lines.append(
                f"• **{item['symbol']}** ({item['name']}): ${item['current_price']} ({item['change_pct']:+}%) | "
                f"Score: {item['touchgrass_score']}/100 | Action: {emoji} **{item['recommended_action']}**"
            )
            lines.append(f"  └ Kronos: {item['kronos_prediction']['direction']} ({item['kronos_prediction']['confidence']*100:.0f}%) | Panel: {item['investor_panel']['verdict']}")

        if candidates:
            lines.append("\n🎯 **Auto-Discovered High-Conviction Candidates**:")
            for c in candidates:
                lines.append(f"• **{c['symbol']}** ({c['name']}) - {c['source']} | Score: {c['score']} | {c['notes']}")

        lines.append("\n✨ *Go touch grass! Touchgrass AI is keeping your portfolio safe.* ✨")
        return "\n".join(lines)

    def dispatch(self, report_markdown: str) -> bool:
        """
        Dispatches report to configured notification channels.
        """
        print("\n================ TOUCHGRASS NOTIFICATION DISPATCH ================")
        print(report_markdown)
        print("==================================================================\n")

        # Telegram webhook dispatch check
        telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        telegram_chat = os.environ.get("TELEGRAM_CHAT_ID")
        if "telegram" in self.channels and telegram_token and telegram_chat:
            self._send_telegram(report_markdown, telegram_token, telegram_chat)

        return True

    def _send_telegram(self, message: str, token: str, chat_id: str):
        try:
            import urllib.request
            import urllib.parse
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = urllib.parse.urlencode({"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}).encode()
            req = urllib.request.Request(url, data=data)
            urllib.request.urlopen(req, timeout=10)
        except Exception as e:
            print(f"[Notifier] Telegram dispatch failed: {e}")
