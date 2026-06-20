# 📊 Forex Market Analyzer - Backtesting Engine

A comprehensive Python-based forex market analysis and backtesting system with real-time signal generation using multiple technical indicators.

## 🚀 Features

- **Multiple Technical Indicators**: RSI, MACD, EMA, Bollinger Bands, Stochastic Oscillator, ATR
- **Smart Signal Generation**: Combines indicators for high-confidence trading signals
- **Backtesting Engine**: Simulates trading with realistic P&L calculations
- **Performance Analytics**: Win rate, Sharpe ratio, max drawdown, profit factor
- **Multi-pair Support**: Analyze multiple forex pairs simultaneously
- **Flexible Timeframes**: Works with 1-minute to daily candles
- **Risk Management**: Built-in stop-loss and take-profit mechanisms

## 📋 Requirements

```bash
pip install -r requirements.txt
```

## 🏃 Quick Start

```python
from analyzer import ForexAnalyzer

analyzer = ForexAnalyzer(pair='EURUSD=X', interval='1d')
results = analyzer.analyze(lookback_days=60)
analyzer.print_results()
analyzer.export_results()
```

## ⚠️ Important Disclaimers

1. **Educational Purpose Only**: For learning, not live trading
2. **Past Performance**: Does not guarantee future results
3. **Risk Management**: Always use proper risk management
4. **No Guarantee**: Use at your own risk

---

Happy trading! 📈💹
