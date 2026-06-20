"""Backtesting Engine"""

import pandas as pd
import numpy as np
from config import TRADING
from typing import Dict, List


class Trade:
    def __init__(self, entry_price: float, entry_time: pd.Timestamp, position_type: str, size: float):
        self.entry_price = entry_price
        self.entry_time = entry_time
        self.position_type = position_type
        self.size = size
        self.exit_price = None
        self.exit_time = None
        self.pnl = 0.0
        self.return_pct = 0.0
    
    def close(self, exit_price: float, exit_time: pd.Timestamp):
        self.exit_price = exit_price
        self.exit_time = exit_time
        if self.position_type == 'BUY':
            self.pnl = (exit_price - self.entry_price) * self.size
            self.return_pct = ((exit_price - self.entry_price) / self.entry_price) * 100
        else:
            self.pnl = (self.entry_price - exit_price) * self.size
            self.return_pct = ((self.entry_price - exit_price) / self.entry_price) * 100
    
    def to_dict(self) -> dict:
        return {
            'Entry Time': self.entry_time,
            'Entry Price': self.entry_price,
            'Position Type': self.position_type,
            'Size': self.size,
            'Exit Time': self.exit_time,
            'Exit Price': self.exit_price,
            'P&L': self.pnl,
            'Return %': self.return_pct
        }


class Backtester:
    def __init__(self, df: pd.DataFrame, signals: pd.DataFrame):
        self.df = df.copy()
        self.signals = signals.copy()
        self.trades: List[Trade] = []
        self.initial_balance = TRADING['initial_balance']
        self.open_positions: List[Trade] = []
        self.equity_curve = []
        self.results = {}
    
    def run(self) -> Dict:
        self.equity_curve = [self.initial_balance]
        for i in range(len(self.df)):
            current_price = self.df['Close'].iloc[i]
            current_time = self.df.index[i]
            self._check_exits(current_price, current_time, i)
            if self.signals['Sell_Signal'].iloc[i] == 1:
                self._open_position('SELL', current_price, current_time)
            elif self.signals['Buy_Signal'].iloc[i] == 1:
                self._open_position('BUY', current_price, current_time)
            self._update_equity(current_price)
        
        final_price = self.df['Close'].iloc[-1]
        final_time = self.df.index[-1]
        while self.open_positions:
            trade = self.open_positions.pop()
            trade.close(final_price, final_time)
            self.trades.append(trade)
        
        self._calculate_results()
        return self.results
    
    def _open_position(self, position_type: str, price: float, time: pd.Timestamp):
        if len(self.open_positions) >= TRADING['max_positions']:
            return
        position_size = self.initial_balance * TRADING['position_size']
        if position_size <= 0:
            return
        trade = Trade(price, time, position_type, position_size)
        self.open_positions.append(trade)
    
    def _check_exits(self, current_price: float, current_time: pd.Timestamp, index: int):
        positions_to_remove = []
        for i, trade in enumerate(self.open_positions):
            exit_trade = False
            if trade.position_type == 'BUY':
                stop_loss = trade.entry_price - (TRADING['stop_loss_pips'] / 10000)
                take_profit = trade.entry_price + (TRADING['take_profit_pips'] / 10000)
                if current_price <= stop_loss or current_price >= take_profit:
                    trade.close(current_price, current_time)
                    exit_trade = True
            else:
                stop_loss = trade.entry_price + (TRADING['stop_loss_pips'] / 10000)
                take_profit = trade.entry_price - (TRADING['take_profit_pips'] / 10000)
                if current_price >= stop_loss or current_price <= take_profit:
                    trade.close(current_price, current_time)
                    exit_trade = True
            if exit_trade:
                positions_to_remove.append(i)
                self.trades.append(trade)
        for i in reversed(positions_to_remove):
            self.open_positions.pop(i)
    
    def _update_equity(self, current_price: float):
        unrealized_pnl = sum([
            (current_price - trade.entry_price) * trade.size if trade.position_type == 'BUY'
            else (trade.entry_price - current_price) * trade.size
            for trade in self.open_positions
        ])
        realized_pnl = sum([trade.pnl for trade in self.trades])
        current_equity = self.initial_balance + realized_pnl + unrealized_pnl
        self.equity_curve.append(current_equity)
    
    def _calculate_results(self):
        if not self.trades:
            self.results = {'Total Trades': 0, 'Win Rate %': 0, 'Total Return %': 0}
            return
        total_trades = len(self.trades)
        winning_trades = len([t for t in self.trades if t.pnl > 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        total_pnl = sum([t.pnl for t in self.trades])
        total_return_pct = (total_pnl / self.initial_balance) * 100
        self.results = {
            'Total Trades': total_trades,
            'Winning Trades': winning_trades,
            'Win Rate %': win_rate,
            'Total Return %': total_return_pct,
            'Total P&L': total_pnl,
            'Final Balance': self.equity_curve[-1]
        }
    
    def get_trades_df(self) -> pd.DataFrame:
        if not self.trades:
            return pd.DataFrame()
        return pd.DataFrame([t.to_dict() for t in self.trades])
