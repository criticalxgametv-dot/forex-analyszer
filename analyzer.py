"""Main Analyzer Module"""

import pandas as pd
from data_fetcher import DataFetcher
from indicators import TechnicalIndicators
from signal_generator import SignalGenerator
from backtester import Backtester
from config import DATA
from typing import Dict
import json


class ForexAnalyzer:
    def __init__(self, pair: str = 'EURUSD=X', interval: str = '1d'):
        self.pair = pair
        self.interval = interval
        self.df = None
        self.signals = None
        self.backtest_results = None
        self.trades = None
    
    def analyze(self, lookback_days: int = None) -> Dict:
        if lookback_days is None:
            lookback_days = DATA['lookback_days']
        print(f"\n{'='*60}\nAnalyzing {self.pair} on {self.interval} timeframe\n{'='*60}\n")
        print("[1/4] Fetching historical data...")
        self._fetch_data(lookback_days)
        if self.df is None or len(self.df) == 0:
            print("Failed to fetch data")
            return {}
        print("[2/4] Calculating technical indicators...")
        self._calculate_indicators()
        print("[3/4] Generating trading signals...")
        self._generate_signals()
        print("[4/4] Running backtest...")
        self._backtest()
        print(f"\n{'='*60}\nAnalysis Complete!\n{'='*60}\n")
        return self._get_results()
    
    def _fetch_data(self, lookback_days: int):
        fetcher = DataFetcher()
        self.df = fetcher.fetch_historical_data(self.pair, lookback_days, self.interval)
    
    def _calculate_indicators(self):
        if self.df is None:
            return
        indicator = TechnicalIndicators(self.df)
        self.df = indicator.calculate_all()
    
    def _generate_signals(self):
        if self.df is None:
            return
        signal_gen = SignalGenerator(self.df)
        self.signals = signal_gen.generate_signals()
    
    def _backtest(self):
        if self.df is None or self.signals is None:
            return
        backtester = Backtester(self.df, self.signals)
        self.backtest_results = backtester.run()
        self.trades = backtester.get_trades_df()
    
    def _get_results(self) -> Dict:
        return {
            'Pair': self.pair,
            'Interval': self.interval,
            'Data Points': len(self.df) if self.df is not None else 0,
            'Backtest Results': self.backtest_results or {},
            'Trades': self.trades.to_dict('records') if self.trades is not None and len(self.trades) > 0 else []
        }
    
    def print_results(self):
        results = self._get_results()
        print(f"\n📊 ANALYSIS RESULTS - {self.pair}\n{'='*60}\n")
        print(f"Data Points: {results['Data Points']}")
        print(f"Interval: {results['Interval']}\n")
        if results['Backtest Results']:
            print("📈 BACKTEST PERFORMANCE")
            print(f"{'-'*60}")
            for key, value in results['Backtest Results'].items():
                if isinstance(value, float):
                    print(f"{key:.<40} {value:>15.2f}")
                else:
                    print(f"{key:.<40} {value:>15}")
    
    def export_results(self, filename: str = None):
        if filename is None:
            filename = f"{self.pair.replace('=X', '')}_{self.interval}_analysis.json"
        results = self._get_results()
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n✅ Results exported to {filename}")
