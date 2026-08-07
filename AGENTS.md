# AGENTS.md — Touchgrass Trader Guidance for AI Assistants

Welcome, AI Agent! You are helping a human manage their stock investments using **Touchgrass Trader**.

## Core Philosophy
1. **Minimum Effort, Maximum Discipline**: Touchgrass Trader protects non-expert investors from emotional trading, FOMO, and pump-and-dump traps.
2. **Double-Engine Security**: Every trade decision is cross-checked against Kronos AI predictions, Serenity supply chain bottlenecks, Uzi 65-Investor Panel, and Uzi Trap Detector.
3. **Local & GitHub Automation**: The user can ask you to run rounds locally or rely on GitHub Actions running twice daily.

## Common Agent Operations

### 1. Run Market Digest & Portfolio Analysis
Execute command:
```bash
python3 -m touchgrass.cli run
```

### 2. Auto-Discover Market Candidates
Execute command:
```bash
python3 -m touchgrass.cli scan --max 5
```

### 3. Analyze a Ticker for the User
Execute command:
```bash
python3 -m touchgrass.cli analyze NVDA
```

### 4. Add/Remove Stock from Watchlist
Execute command:
```bash
python3 -m touchgrass.cli add TICKER --target PRICE --notes "Reasoning"
python3 -m touchgrass.cli remove TICKER
```
