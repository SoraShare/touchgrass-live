---
name: touchgrass
description: Automated chill stock management skill for Antigravity, Claude, Codex, and Cursor. Runs stock analysis, market breakout scanner, 65 investor panel evaluation, trap detection, and updates local watchlist/portfolio with minimal user effort.
---

# Touchgrass Skill (`touchgrass`)

**Touchgrass Trader** allows AI agents (Antigravity, Claude, Codex, Cursor) to manage user stock portfolios with zero stress.

## Quick Trigger Commands

When the user asks to analyze stocks, check market trends, or update watchlists:

- **Run Full Market Digest & Portfolio Update**:
  ```bash
  python3 -m touchgrass.cli run
  ```

- **Scan US Market for Breakout & Bottleneck Stocks**:
  ```bash
  python3 -m touchgrass.cli scan --max 5
  ```

- **Analyze Specific Stock Ticker**:
  ```bash
  python3 -m touchgrass.cli analyze NVDA
  ```

- **View Current Watchlist & Positions**:
  ```bash
  python3 -m touchgrass.cli watchlist
  ```

- **Add / Remove Stock Symbol**:
  ```bash
  python3 -m touchgrass.cli add AAPL --target 210.0 --notes "AI iPhone cycle"
  python3 -m touchgrass.cli remove TSLA
  ```

## Workflows & Capabilities

1. **Auto Stock Discovery**: Combines `BreakoutAnalysis` (momentum setups, VCP contraction) and `Serenity` (supply chain bottleneck leaders like NVDA, TSM, AVGO).
2. **360 Evaluation**: Synthesizes `Kronos` AI time-series predictions, `Uzi` 65-investor panel consensus, and `Trap Detector` (scam & pump-and-dump filter).
3. **Automated Notification**: Sends twice-daily digests to Telegram, Email, Discord, or Webhooks.
