"""Signal Generation Module"""

import pandas as pd
import numpy as np
from config import INDICATORS, SIGNAL_THRESHOLDS
from typing import Tuple


class SignalGenerator:
    """Generate trading signals based on technical indicators"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.signals = pd.DataFrame(index=df.index)
        self.signals['Buy_Signal'] = 0
        self.signals['Sell_Signal'] = 0
        self.signals['Strength'] = 0.0
    
    def generate_signals(self) -> pd.DataFrame:
        buy_votes = pd.Series(0, index=self.df.index)
        sell_votes = pd.Series(0, index=self.df.index)
        
        if INDICATORS['RSI']['enabled'] and 'RSI' in self.df.columns:
            rsi_buy, rsi_sell = self._rsi_signals()
            buy_votes += rsi_buy
            sell_votes += rsi_sell
        
        if INDICATORS['MACD']['enabled'] and 'MACD' in self.df.columns:
            macd_buy, macd_sell = self._macd_signals()
            buy_votes += macd_buy
            sell_votes += macd_sell
        
        if INDICATORS['EMA']['enabled'] and 'EMA_Short' in self.df.columns:
            ema_buy, ema_sell = self._ema_signals()
            buy_votes += ema_buy
            sell_votes += ema_sell
        
        if INDICATORS['BOLLINGER_BANDS']['enabled'] and 'BB_Upper' in self.df.columns:
            bb_buy, bb_sell = self._bollinger_signals()
            buy_votes += bb_buy
            sell_votes += bb_sell
        
        if INDICATORS['STOCHASTIC']['enabled'] and 'Stochastic_K' in self.df.columns:
            stoch_buy, stoch_sell = self._stochastic_signals()
            buy_votes += stoch_buy
            sell_votes += stoch_sell
        
        self.signals['Buy_Signal'] = (buy_votes >= SIGNAL_THRESHOLDS['buy_signals_required']).astype(int)
        self.signals['Sell_Signal'] = (sell_votes >= SIGNAL_THRESHOLDS['sell_signals_required']).astype(int)
        
        total_indicators = sum([
            INDICATORS['RSI']['enabled'],
            INDICATORS['MACD']['enabled'],
            INDICATORS['EMA']['enabled'],
            INDICATORS['BOLLINGER_BANDS']['enabled'],
            INDICATORS['STOCHASTIC']['enabled']
        ])
        
        self.signals['Strength'] = (buy_votes + sell_votes) / (total_indicators * 2)
        self.signals['Strength'] = self.signals['Strength'].clip(0, 1)
        return self.signals
    
    def _rsi_signals(self) -> Tuple[pd.Series, pd.Series]:
        buy = pd.Series(0, index=self.df.index)
        sell = pd.Series(0, index=self.df.index)
        buy = (self.df['RSI'] < INDICATORS['RSI']['oversold']).astype(int)
        sell = (self.df['RSI'] > INDICATORS['RSI']['overbought']).astype(int)
        return buy, sell
    
    def _macd_signals(self) -> Tuple[pd.Series, pd.Series]:
        buy = (self.df['MACD'] > self.df['MACD_Signal']) & (self.df['MACD'].shift(1) <= self.df['MACD_Signal'].shift(1))
        sell = (self.df['MACD'] < self.df['MACD_Signal']) & (self.df['MACD'].shift(1) >= self.df['MACD_Signal'].shift(1))
        return buy.astype(int), sell.astype(int)
    
    def _ema_signals(self) -> Tuple[pd.Series, pd.Series]:
        buy = (self.df['Close'] > self.df['EMA_Short']) & (self.df['EMA_Short'] > self.df['EMA_Long'])
        sell = (self.df['Close'] < self.df['EMA_Short']) & (self.df['EMA_Short'] < self.df['EMA_Long'])
        return buy.astype(int), sell.astype(int)
    
    def _bollinger_signals(self) -> Tuple[pd.Series, pd.Series]:
        buy = (self.df['Close'] <= self.df['BB_Lower']).astype(int)
        sell = (self.df['Close'] >= self.df['BB_Upper']).astype(int)
        return buy, sell
    
    def _stochastic_signals(self) -> Tuple[pd.Series, pd.Series]:
        oversold = INDICATORS['STOCHASTIC']['oversold']
        overbought = INDICATORS['STOCHASTIC']['overbought']
        buy = (self.df['Stochastic_K'] > self.df['Stochastic_D']) & (self.df['Stochastic_K'] < oversold)
        sell = (self.df['Stochastic_K'] < self.df['Stochastic_D']) & (self.df['Stochastic_K'] > overbought)
        return buy.astype(int), sell.astype(int)
