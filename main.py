"""Main entry point for Forex Analyzer"""

from analyzer import ForexAnalyzer


def main():
    print("\n🚀 FOREX MARKET ANALYZER - Backtesting Engine\n")
    analyzer = ForexAnalyzer(pair='EURUSD=X', interval='1d')
    results = analyzer.analyze(lookback_days=60)
    analyzer.print_results()
    analyzer.export_results()


if __name__ == '__main__':
    main()
