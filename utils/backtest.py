"""
Backtesting utilities for Nifty 50 strategies

This module provides functions to backtest various trading strategies
on historical Nifty 50 data to evaluate their performance.
"""

import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
from data.nse_data import fetch_nifty50_symbols


class StrategyBacktester:
    """
    Backtest trading strategies on historical data
    """
    
    def __init__(self, start_date="2023-01-01", end_date=None, initial_capital=100000):
        self.start_date = start_date
        self.end_date = end_date or datetime.now().strftime('%Y-%m-%d')
        self.initial_capital = initial_capital
        self.symbols = fetch_nifty50_symbols()
    
    def fetch_historical_data(self, symbol, period="1y"):
        """Fetch historical data for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI for given prices"""
        delta = prices.diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_moving_averages(self, prices, short_period=20, long_period=50):
        """Calculate short and long moving averages"""
        ma_short = prices.rolling(window=short_period).mean()
        ma_long = prices.rolling(window=long_period).mean()
        return ma_short, ma_long
    
    def backtest_momentum_strategy(self, lookback_days=5):
        """
        Backtest momentum strategy:
        Buy top gainers from previous period, hold for specified days
        """
        results = []
        
        for symbol in self.symbols[:10]:  # Test on first 10 stocks
            data = self.fetch_historical_data(symbol)
            if data is None or len(data) < 60:
                continue
            
            # Calculate returns
            data['Returns'] = data['Close'].pct_change()
            data['Rolling_Return'] = data['Returns'].rolling(window=lookback_days).sum()
            
            # Generate signals
            data['Signal'] = 0
            data.loc[data['Rolling_Return'] > data['Rolling_Return'].quantile(0.8), 'Signal'] = 1
            data.loc[data['Rolling_Return'] < data['Rolling_Return'].quantile(0.2), 'Signal'] = -1
            
            # Calculate strategy returns
            data['Strategy_Returns'] = data['Signal'].shift(1) * data['Returns']
            
            # Calculate cumulative returns
            cumulative_returns = (1 + data['Strategy_Returns']).cumprod()
            
            total_return = cumulative_returns.iloc[-1] - 1
            volatility = data['Strategy_Returns'].std() * np.sqrt(252)
            sharpe_ratio = (data['Strategy_Returns'].mean() * 252) / (data['Strategy_Returns'].std() * np.sqrt(252))
            
            results.append({
                'symbol': symbol,
                'total_return': total_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': self.calculate_max_drawdown(cumulative_returns)
            })
        
        return results
    
    def backtest_rsi_strategy(self, rsi_period=14, oversold=30, overbought=70):
        """
        Backtest RSI mean reversion strategy:
        Buy when RSI < oversold, sell when RSI > overbought
        """
        results = []
        
        for symbol in self.symbols[:10]:
            data = self.fetch_historical_data(symbol)
            if data is None or len(data) < 60:
                continue
            
            # Calculate RSI
            data['RSI'] = self.calculate_rsi(data['Close'], rsi_period)
            data['Returns'] = data['Close'].pct_change()
            
            # Generate signals
            data['Signal'] = 0
            data.loc[data['RSI'] < oversold, 'Signal'] = 1  # Buy signal
            data.loc[data['RSI'] > overbought, 'Signal'] = -1  # Sell signal
            
            # Calculate strategy returns
            data['Strategy_Returns'] = data['Signal'].shift(1) * data['Returns']
            
            # Calculate performance metrics
            cumulative_returns = (1 + data['Strategy_Returns']).cumprod()
            
            total_return = cumulative_returns.iloc[-1] - 1
            volatility = data['Strategy_Returns'].std() * np.sqrt(252)
            sharpe_ratio = (data['Strategy_Returns'].mean() * 252) / (data['Strategy_Returns'].std() * np.sqrt(252))
            
            results.append({
                'symbol': symbol,
                'total_return': total_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': self.calculate_max_drawdown(cumulative_returns)
            })
        
        return results
    
    def backtest_ma_crossover_strategy(self, short_period=20, long_period=50):
        """
        Backtest moving average crossover strategy:
        Buy when short MA crosses above long MA, sell when it crosses below
        """
        results = []
        
        for symbol in self.symbols[:10]:
            data = self.fetch_historical_data(symbol)
            if data is None or len(data) < long_period + 10:
                continue
            
            # Calculate moving averages
            ma_short, ma_long = self.calculate_moving_averages(
                data['Close'], short_period, long_period
            )
            data['MA_Short'] = ma_short
            data['MA_Long'] = ma_long
            data['Returns'] = data['Close'].pct_change()
            
            # Generate signals
            data['Signal'] = 0
            data.loc[data['MA_Short'] > data['MA_Long'], 'Signal'] = 1
            data.loc[data['MA_Short'] < data['MA_Long'], 'Signal'] = -1
            
            # Calculate strategy returns
            data['Strategy_Returns'] = data['Signal'].shift(1) * data['Returns']
            
            # Calculate performance metrics
            cumulative_returns = (1 + data['Strategy_Returns']).cumprod()
            
            total_return = cumulative_returns.iloc[-1] - 1
            volatility = data['Strategy_Returns'].std() * np.sqrt(252)
            sharpe_ratio = (data['Strategy_Returns'].mean() * 252) / (data['Strategy_Returns'].std() * np.sqrt(252))
            
            results.append({
                'symbol': symbol,
                'total_return': total_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': self.calculate_max_drawdown(cumulative_returns)
            })
        
        return results
    
    def calculate_max_drawdown(self, cumulative_returns):
        """Calculate maximum drawdown"""
        peak = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - peak) / peak
        return drawdown.min()
    
    def compare_strategies(self):
        """Compare performance of different strategies"""
        print("Backtesting strategies...")
        
        momentum_results = self.backtest_momentum_strategy()
        rsi_results = self.backtest_rsi_strategy()
        ma_results = self.backtest_ma_crossover_strategy()
        
        # Calculate average performance
        strategies = {
            'Momentum': momentum_results,
            'RSI Mean Reversion': rsi_results,
            'MA Crossover': ma_results
        }
        
        print("\n" + "="*80)
        print("STRATEGY BACKTEST RESULTS")
        print("="*80)
        
        for strategy_name, results in strategies.items():
            if results:
                avg_return = np.mean([r['total_return'] for r in results])
                avg_sharpe = np.mean([r['sharpe_ratio'] for r in results if not np.isnan(r['sharpe_ratio'])])
                avg_volatility = np.mean([r['volatility'] for r in results])
                avg_max_dd = np.mean([r['max_drawdown'] for r in results])
                
                print(f"\n{strategy_name}:")
                print(f"  Average Return: {avg_return:.2%}")
                print(f"  Average Sharpe Ratio: {avg_sharpe:.2f}")
                print(f"  Average Volatility: {avg_volatility:.2%}")
                print(f"  Average Max Drawdown: {avg_max_dd:.2%}")
        
        return strategies


def run_backtest():
    """Run backtesting analysis"""
    backtester = StrategyBacktester()
    results = backtester.compare_strategies()
    return results


if __name__ == "__main__":
    run_backtest()
