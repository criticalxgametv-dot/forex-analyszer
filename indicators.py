"""Technical Indicators Module"""

import pandas as pd
import numpy as np
from config import INDICATORS


class TechnicalIndicators:
    """Calculate technical indicators for price data"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.indicators = {}
    
    def calculate_all(self) -> pd.DataFrame:
        """Calculate all enabled indicators"""
        if INDICATORS['RSI']['enabled']:
            self.calculate_rsi()
        if INDICATORS['MACD']['enabled']:
            self.calculate_macd()
        if INDICATORS['EMA']['enabled']:
            self.calculate_ema()
        if INDICATORS['BOLLINGER_BANDS']['enabled']:
            self.calculate_bollinger_bands()
        if INDICATORS['STOCHASTIC']['enabled']:
            self.calculate_stochastic()
        if INDICATORS['ATR']['enabled']:
            self.calculate_atr()
        return self.df
    
    def calculate_rsi(self, period: int = None):
        if period is None:
            period = INDICATORS['RSI']['period']
        delta = self.df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        self.df['RSI'] = rsi
        self.indicators['RSI'] = rsi
        return rsi
    
    def calculate_macd(self, fast: int = None, slow: int = None, signal: int = None):
        if fast is None:
            fast = INDICATORS['MACD']['fast']
        if slow is None:
            slow = INDICATORS['MACD']['slow']
        if signal is None:
            signal = INDICATORS['MACD']['signal']
        ema_fast = self.df['Close'].ewm(span=fast).mean()
        ema_slow = self.df['Close'].ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        self.df['MACD'] = macd_line
        self.df['MACD_Signal'] = signal_line
        self.df['MACD_Histogram'] = histogram
        self.indicators['MACD'] = macd_line
        self.indicators['MACD_Signal'] = signal_line
        return macd_line, signal_line, histogram
    
    def calculate_ema(self, short: int = None, long: int = None):
        if short is None:
            short = INDICATORS['EMA']['short']
        if long is None:
            long = INDICATORS['EMA']['long']
        ema_short = self.df['Close'].ewm(span=short).mean()
        ema_long = self.df['Close'].ewm(span=long).mean()
        self.df['EMA_Short'] = ema_short
        self.df['EMA_Long'] = ema_long
        self.indicators['EMA_Short'] = ema_short
        self.indicators['EMA_Long'] = ema_long
        return ema_short, ema_long
    
    def calculate_bollinger_bands(self, period: int = None, std_dev: float = None):
        if period is None:
            period = INDICATORS['BOLLINGER_BANDS']['period']
        if std_dev is None:
            std_dev = INDICATORS['BOLLINGER_BANDS']['std_dev']
        sma = self.df['Close'].rolling(window=period).mean()
        std = self.df['Close'].rolling(window=period).std()
        upper_band = sma + (std_dev * std)
        lower_band = sma - (std_dev * std)
        self.df['BB_Upper'] = upper_band
        self.df['BB_Middle'] = sma
        self.df['BB_Lower'] = lower_band
        self.indicators['BB_Upper'] = upper_band
        self.indicators['BB_Middle'] = sma
        self.indicators['BB_Lower'] = lower_band
        return upper_band, sma, lower_band
    
    def calculate_stochastic(self, period: int = None, smooth_k: int = None, smooth_d: int = None):
        if period is None:
            period = INDICATORS['STOCHASTIC']['period']
        if smooth_k is None:
            smooth_k = INDICATORS['STOCHASTIC']['smooth_k']
        if smooth_d is None:
            smooth_d = INDICATORS['STOCHASTIC']['smooth_d']
        low_min = self.df['Low'].rolling(window=period).min()
        high_max = self.df['High'].rolling(window=period).max()
        k_percent = 100 * ((self.df['Close'] - low_min) / (high_max - low_min))
        k_percent = k_percent.rolling(window=smooth_k).mean()
        d_percent = k_percent.rolling(window=smooth_d).mean()
        self.df['Stochastic_K'] = k_percent
        self.df['Stochastic_D'] = d_percent
        self.indicators['Stochastic_K'] = k_percent
        self.indicators['Stochastic_D'] = d_percent
        return k_percent, d_percent
    
    def calculate_atr(self, period: int = None):
        if period is None:
            period = INDICATORS['ATR']['period']
        high_low = self.df['High'] - self.df['Low']
        high_close = abs(self.df['High'] - self.df['Close'].shift())
        low_close = abs(self.df['Low'] - self.df['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        atr = true_range.rolling(period).mean()
        self.df['ATR'] = atr
        self.indicators['ATR'] = atr
        return atr
