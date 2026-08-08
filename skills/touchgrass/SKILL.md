---
name: touchgrass
description: Automated chill swing trading stock management skill for Antigravity, Claude, Codex, and Cursor. Runs swing stock analysis, Kronos 5-day trend prediction, supply-chain discovery, 65 investor panel evaluation, trap detection, and updates local watchlist/portfolio with minimal user effort.
---

# Touchgrass Skill (`touchgrass`)

**Touchgrass Trader** allows AI agents (Antigravity, Claude, Codex, Cursor) to manage user stock portfolios with zero stress using a **disciplined Swing Trading strategy (5-20 days hold)**.

## Quick Trigger Commands

When the user asks to analyze stocks, check market trends, or update swing watchlists:

- **Run Full Swing Market Digest & Portfolio Update**:
  ```bash
  python main.py run
  ```

- **Discover Swing Trade Stock Candidates (Supply-Chain Monopolies)**:
  ```bash
  python main.py scan --max 5
  ```

- **Analyze Specific Stock Ticker (Kronos 5-Day Trend + 65 Investor Panel)**:
  ```bash
  python main.py analyze NVDA
  ```

- **View Current Swing Watchlist & Positions**:
  ```bash
  python main.py watchlist
  ```

- **Add / Remove Stock Symbol**:
  ```bash
  python main.py add AAPL --target 210.0 --notes "AI iPhone cycle swing"
  python main.py remove TSLA
  ```

## Workflows & Capabilities

1. **Auto Stock Discovery**: Discovers supply chain bottleneck leaders (e.g., NVDA, TSM, AVGO, ASML) via `serenity-skill`.
2. **Kronos 5-Day Trend Prediction**: Uses `Kronos` financial time-series model to infer projected 5-to-10 day directional K-line momentum.
3. **360 Evaluation**: Synthesizes Kronos predictions, `Uzi` 65-investor panel consensus, and `Uzi Trap Detector` (scam & pump-and-dump filter).
4. **Automated Report Persistence**: Saves daily reports to `reports/latest.md` and `reports/report_YYYYMMDD.md` and dispatches alerts via Telegram, Email, or Discord.
