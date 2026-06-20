"""Data Fetching Module"""

import pandas as pd
import yfinance as yf
from config import DATA
from typing import Optional


class DataFetcher:
    def __init__(self, source: str = None):
        self.source = source or DATA['source']
    
    def fetch_historical_data(self, pair: str, lookback_days: int = None, interval: str = '1d') -> Optional[pd.DataFrame]:
        if lookback_days is None:
            lookback_days = DATA['lookback_days']
        
        if self.source == 'yfinance':
            return self._fetch_yfinance(pair, lookback_days, interval)
        else:
            raise ValueError(f"Unsupported data source: {self.source}")
    
    def _fetch_yfinance(self, pair: str, lookback_days: int, interval: str) -> Optional[pd.DataFrame]:
        try:
            df = yf.download(pair, period=f'{lookback_days}d', interval=interval, progress=False, prepost=False)
            if df.empty:
                print(f"No data found for {pair}")
                return None
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            df = df.dropna()
            print(f"Fetched {len(df)} candles for {pair} ({interval})")
            return df
        except Exception as e:
            print(f"Error fetching data for {pair}: {e}")
            return None
