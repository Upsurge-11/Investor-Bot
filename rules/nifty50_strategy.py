import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from data import nse_data


class Nifty50Strategy:
    """
    A comprehensive strategy class for Nifty 50 stock investments.
    Implements various trading strategies including momentum, mean reversion, 
    value investing, and sentiment-based approaches.
    """
    
    def __init__(self):
        self.symbols = nse_data.fetch_nifty50_symbols()
        self.recommendations = []
    
    # 1. MOMENTUM STRATEGIES
    
    def momentum_top_gainers_strategy(self, top_n=5):
        """
        Strategy: Buy top gaining stocks in Nifty 50
        Logic: Stocks with strong momentum tend to continue their trend
        """
        gainers = nse_data.fetch_gainers_or_losers(fetch_gainers=True, full_list=False)
        recommendations = []
        
        for stock in gainers[:top_n]:
            if stock['change_pct'] > 2:  # Only consider stocks with >2% gain
                recommendations.append({
                    'symbol': stock['symbol'],
                    'action': 'BUY',
                    'strategy': 'Momentum - Top Gainers',
                    'reason': f"Strong momentum with {stock['change_pct']:.2f}% gain",
                    'current_price': stock['lastPrice'],
                    'confidence': min(stock['change_pct'] * 10, 100)  # Higher gain = higher confidence
                })
        
        return recommendations
    
    def moving_average_crossover_strategy(self, short_period=20, long_period=50):
        """
        Strategy: Buy when short MA crosses above long MA (Golden Cross)
        Logic: Indicates bullish trend reversal
        """
        recommendations = []
        
        for symbol in self.symbols[:10]:  # Check first 10 stocks for demo
            try:
                # Fetch historical data
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="6mo")
                
                if len(hist) < long_period:
                    continue
                
                # Calculate moving averages
                hist['MA_short'] = hist['Close'].rolling(window=short_period).mean()
                hist['MA_long'] = hist['Close'].rolling(window=long_period).mean()
                
                # Check for golden cross (recent crossover)
                recent_data = hist.tail(5)
                if (recent_data['MA_short'].iloc[-1] > recent_data['MA_long'].iloc[-1] and
                    recent_data['MA_short'].iloc[-3] <= recent_data['MA_long'].iloc[-3]):
                    
                    recommendations.append({
                        'symbol': symbol,
                        'action': 'BUY',
                        'strategy': 'Momentum - MA Crossover',
                        'reason': f"Golden Cross: {short_period}MA crossed above {long_period}MA",
                        'current_price': hist['Close'].iloc[-1],
                        'confidence': 75
                    })
                    
            except Exception as e:
                continue
        
        return recommendations
    
    # 2. MEAN REVERSION STRATEGIES
    
    def rsi_oversold_strategy(self, period=14, oversold_threshold=30):
        """
        Strategy: Buy oversold stocks (RSI < 30)
        Logic: Oversold stocks tend to bounce back
        """
        recommendations = []
        
        for symbol in self.symbols[:15]:  # Check first 15 stocks for demo
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="3mo")
                
                if len(hist) < period + 1:
                    continue
                
                # Calculate RSI
                delta = hist['Close'].diff()
                gain = delta.where(delta > 0, 0).rolling(window=period).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                
                current_rsi = rsi.iloc[-1]
                
                if current_rsi < oversold_threshold:
                    recommendations.append({
                        'symbol': symbol,
                        'action': 'BUY',
                        'strategy': 'Mean Reversion - RSI Oversold',
                        'reason': f"RSI at {current_rsi:.2f}, indicating oversold condition",
                        'current_price': hist['Close'].iloc[-1],
                        'confidence': (oversold_threshold - current_rsi) * 2  # Lower RSI = higher confidence
                    })
                    
            except Exception as e:
                continue
        
        return recommendations
    
    def support_resistance_strategy(self):
        """
        Strategy: Buy near support levels, sell near resistance
        Logic: Stocks tend to bounce off support/resistance levels
        """
        recommendations = []
        
        for symbol in self.symbols[:10]:  # Check first 10 stocks for demo
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="6mo")
                
                if len(hist) < 50:
                    continue
                
                # Find support and resistance levels
                highs = hist['High'].rolling(window=20).max()
                lows = hist['Low'].rolling(window=20).min()
                
                current_price = hist['Close'].iloc[-1]
                recent_low = lows.iloc[-5:].min()
                recent_high = highs.iloc[-5:].max()
                
                # Buy if near support (within 2% of recent low)
                if current_price <= recent_low * 1.02:
                    recommendations.append({
                        'symbol': symbol,
                        'action': 'BUY',
                        'strategy': 'Mean Reversion - Support Level',
                        'reason': f"Price near support level at {recent_low:.2f}",
                        'current_price': current_price,
                        'confidence': 65
                    })
                
                # Sell if near resistance (within 2% of recent high)
                elif current_price >= recent_high * 0.98:
                    recommendations.append({
                        'symbol': symbol,
                        'action': 'SELL',
                        'strategy': 'Mean Reversion - Resistance Level',
                        'reason': f"Price near resistance level at {recent_high:.2f}",
                        'current_price': current_price,
                        'confidence': 65
                    })
                    
            except Exception as e:
                continue
        
        return recommendations
    
    # 3. VALUE-BASED STRATEGIES
    
    def low_pe_strategy(self, max_pe=15):
        """
        Strategy: Buy stocks with low P/E ratios
        Logic: Low P/E stocks are potentially undervalued
        """
        recommendations = []
        
        for symbol in self.symbols:
            try:
                stock_data = nse_data.fetch_stock_data(symbol, full=True)
                pe_ratio = stock_data.get('forwardPE') or stock_data.get('trailingPE')
                
                if pe_ratio and pe_ratio < max_pe and pe_ratio > 0:
                    recommendations.append({
                        'symbol': symbol,
                        'action': 'BUY',
                        'strategy': 'Value - Low P/E',
                        'reason': f"Low P/E ratio of {pe_ratio:.2f}",
                        'current_price': stock_data.get('currentPrice', 0),
                        'confidence': (max_pe - pe_ratio) * 5  # Lower P/E = higher confidence
                    })
                    
            except Exception as e:
                continue
        
        return sorted(recommendations, key=lambda x: x['confidence'], reverse=True)[:10]
    
    def high_dividend_strategy(self, min_yield=2.0):
        """
        Strategy: Buy high dividend yielding stocks
        Logic: High dividend stocks provide steady income
        """
        recommendations = []
        
        for symbol in self.symbols:
            try:
                stock_data = nse_data.fetch_stock_data(symbol, full=True)
                dividend_yield = stock_data.get('dividendYield')
                
                if dividend_yield and dividend_yield > min_yield:
                    recommendations.append({
                        'symbol': symbol,
                        'action': 'BUY',
                        'strategy': 'Value - High Dividend',
                        'reason': f"High dividend yield of {dividend_yield:.2f}%",
                        'current_price': stock_data.get('currentPrice', 0),
                        'confidence': min(dividend_yield * 15, 100)  # Higher yield = higher confidence
                    })
                    
            except Exception as e:
                continue
        
        return sorted(recommendations, key=lambda x: x['confidence'], reverse=True)[:10]
    
    # 4. SENTIMENT-BASED STRATEGIES
    
    def market_mood_strategy(self):
        """
        Strategy: Align with market sentiment
        Logic: Follow the overall market trend
        """
        mood_analysis = nse_data.fetch_market_mood()
        recommendations = []
        
        if "bullish" in mood_analysis.lower():
            # In bullish market, buy top gainers
            gainers = nse_data.fetch_gainers_or_losers(fetch_gainers=True, full_list=False)
            for stock in gainers[:3]:
                recommendations.append({
                    'symbol': stock['symbol'],
                    'action': 'BUY',
                    'strategy': 'Sentiment - Bullish Market',
                    'reason': f"Market bullish, riding momentum with {stock['change_pct']:.2f}% gainer",
                    'current_price': stock['lastPrice'],
                    'confidence': 70
                })
                
        elif "bearish" in mood_analysis.lower():
            # In bearish market, consider defensive stocks or wait
            recommendations.append({
                'symbol': 'CASH',
                'action': 'HOLD',
                'strategy': 'Sentiment - Bearish Market',
                'reason': "Market bearish, consider defensive positioning",
                'current_price': 0,
                'confidence': 80
            })
        
        return recommendations
    
    def contrarian_strategy(self):
        """
        Strategy: Go against market sentiment
        Logic: Buy when others are selling, sell when others are buying
        """
        recommendations = []
        
        # Buy biggest losers (contrarian approach)
        losers = nse_data.fetch_gainers_or_losers(fetch_gainers=False, full_list=False)
        
        for stock in losers[:3]:
            if stock['change_pct'] < -3:  # Only consider stocks down >3%
                recommendations.append({
                    'symbol': stock['symbol'],
                    'action': 'BUY',
                    'strategy': 'Sentiment - Contrarian',
                    'reason': f"Contrarian buy on {stock['change_pct']:.2f}% drop",
                    'current_price': stock['lastPrice'],
                    'confidence': min(abs(stock['change_pct']) * 8, 100)
                })
        
        return recommendations
    
    # 5. COMBINED STRATEGY METHODS
    
    def get_all_recommendations(self):
        """
        Get recommendations from all strategies
        """
        all_recommendations = []
        
        print("Analyzing Momentum strategies...")
        all_recommendations.extend(self.momentum_top_gainers_strategy())
        all_recommendations.extend(self.moving_average_crossover_strategy())
        
        print("Analyzing Mean Reversion strategies...")
        all_recommendations.extend(self.rsi_oversold_strategy())
        all_recommendations.extend(self.support_resistance_strategy())
        
        print("Analyzing Value strategies...")
        all_recommendations.extend(self.low_pe_strategy())
        all_recommendations.extend(self.high_dividend_strategy())
        
        print("Analyzing Sentiment strategies...")
        all_recommendations.extend(self.market_mood_strategy())
        all_recommendations.extend(self.contrarian_strategy())
        
        return all_recommendations
    
    def get_top_recommendations(self, top_n=10):
        """
        Get top N recommendations across all strategies
        """
        all_recs = self.get_all_recommendations()
        # Sort by confidence score
        sorted_recs = sorted(all_recs, key=lambda x: x['confidence'], reverse=True)
        return sorted_recs[:top_n]
    
    def print_recommendations(self, recommendations):
        """
        Pretty print recommendations
        """
        if not recommendations:
            print("No recommendations found.")
            return
        
        print("\n" + "="*80)
        print("NIFTY 50 INVESTMENT RECOMMENDATIONS")
        print("="*80)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['symbol'].replace('.NS', '')}")
            print(f"   Action: {rec['action']}")
            print(f"   Strategy: {rec['strategy']}")
            print(f"   Reason: {rec['reason']}")
            print(f"   Current Price: ₹{rec['current_price']:.2f}")
            print(f"   Confidence: {rec['confidence']:.1f}%")
            print("-" * 60)


# Strategy usage examples
def run_momentum_strategy():
    """Run momentum-based strategies"""
    strategy = Nifty50Strategy()
    print("Running Momentum Strategies...")
    
    gainers_recs = strategy.momentum_top_gainers_strategy()
    ma_recs = strategy.moving_average_crossover_strategy()
    
    all_momentum_recs = gainers_recs + ma_recs
    strategy.print_recommendations(all_momentum_recs)
    
    return all_momentum_recs

def run_value_strategy():
    """Run value-based strategies"""
    strategy = Nifty50Strategy()
    print("Running Value Strategies...")
    
    pe_recs = strategy.low_pe_strategy()
    dividend_recs = strategy.high_dividend_strategy()
    
    all_value_recs = pe_recs + dividend_recs
    strategy.print_recommendations(all_value_recs)
    
    return all_value_recs

def run_sentiment_strategy():
    """Run sentiment-based strategies"""
    strategy = Nifty50Strategy()
    print("Running Sentiment Strategies...")
    
    mood_recs = strategy.market_mood_strategy()
    contrarian_recs = strategy.contrarian_strategy()
    
    all_sentiment_recs = mood_recs + contrarian_recs
    strategy.print_recommendations(all_sentiment_recs)
    
    return all_sentiment_recs

def run_comprehensive_analysis():
    """Run all strategies and get best recommendations"""
    strategy = Nifty50Strategy()
    print("Running Comprehensive Analysis...")
    
    top_recs = strategy.get_top_recommendations(15)
    strategy.print_recommendations(top_recs)
    
    return top_recs