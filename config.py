"""Configuration file for Forex Analyzer"""

# Technical Indicators Configuration
INDICATORS = {
    'RSI': {
        'enabled': True,
        'period': 14,
        'overbought': 70,
        'oversold': 30
    },
    'MACD': {
        'enabled': True,
        'fast': 12,
        'slow': 26,
        'signal': 9
    },
    'EMA': {
        'enabled': True,
        'short': 12,
        'long': 26
    },
    'BOLLINGER_BANDS': {
        'enabled': True,
        'period': 20,
        'std_dev': 2
    },
    'STOCHASTIC': {
        'enabled': True,
        'period': 14,
        'smooth_k': 3,
        'smooth_d': 3,
        'overbought': 80,
        'oversold': 20
    },
    'ATR': {
        'enabled': True,
        'period': 14
    }
}

# Trading Configuration
TRADING = {
    'timeframe': '1m',
    'initial_balance': 1000,
    'position_size': 0.1,
    'stop_loss_pips': 20,
    'take_profit_pips': 40,
    'max_positions': 3
}

# Data Configuration
DATA = {
    'source': 'yfinance',
    'pairs': ['EURUSD=X', 'GBPUSD=X', 'JPYUSD=X'],
    'lookback_days': 30,
    'update_interval': 60
}

# Signal Thresholds
SIGNAL_THRESHOLDS = {
    'buy_signals_required': 3,
    'sell_signals_required': 2,
    'confidence_threshold': 0.6
}
