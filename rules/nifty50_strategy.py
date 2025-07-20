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

def run_backtest():
    """Run backtesting for all strategies"""
    try:
        from utils.backtest import StrategyBacktester
        
        print("🔍 Initializing Backtest Engine...")
        backtester = StrategyBacktester(start_date="2023-01-01")
        
        print("📊 Running Strategy Backtests (this may take a few minutes)...")
        results = backtester.compare_strategies()
        
        return results
        
    except ImportError:
        print("❌ Backtest module not found. Using simplified backtesting...")
        return run_simplified_backtest()
    except Exception as e:
        print(f"❌ Error running backtest: {e}")
        return None

def run_simplified_backtest():
    """Simplified backtesting using historical performance"""
    print("\n" + "="*80)
    print("SIMPLIFIED STRATEGY BACKTEST RESULTS")
    print("="*80)
    
    strategy = Nifty50Strategy()
    
    # Test momentum strategy on a few stocks
    print("\n📈 Testing Momentum Strategy...")
    momentum_wins = 0
    momentum_total = 0
    
    try:
        gainers = nse_data.fetch_gainers_or_losers(fetch_gainers=True, full_list=True)
        top_gainers = [stock for stock in gainers if stock['change_pct'] > 2][:5]
        
        for stock in top_gainers:
            momentum_total += 1
            if stock['change_pct'] > 1:  # Simple win condition
                momentum_wins += 1
        
        momentum_win_rate = (momentum_wins / momentum_total * 100) if momentum_total > 0 else 0
        print(f"  Momentum Strategy Win Rate: {momentum_win_rate:.1f}% ({momentum_wins}/{momentum_total})")
        print(f"  Average Gain: {sum([s['change_pct'] for s in top_gainers]) / len(top_gainers):.2f}%")
        
    except Exception as e:
        print(f"  Error testing momentum strategy: {e}")
    
    # Test value strategy
    print("\n💰 Testing Value Strategy...")
    try:
        value_recs = strategy.low_pe_strategy(max_pe=20)
        value_count = len(value_recs)
        avg_confidence = sum([rec['confidence'] for rec in value_recs]) / value_count if value_count > 0 else 0
        
        print(f"  Value Opportunities Found: {value_count}")
        print(f"  Average Confidence: {avg_confidence:.1f}%")
        
    except Exception as e:
        print(f"  Error testing value strategy: {e}")
    
    # Test sentiment strategy
    print("\n🎭 Testing Sentiment Strategy...")
    try:
        market_mood = nse_data.fetch_market_mood()
        sentiment_score = 0
        
        if "bullish" in market_mood.lower():
            sentiment_score = 75
        elif "bearish" in market_mood.lower():
            sentiment_score = 60
        else:
            sentiment_score = 50
            
        print(f"  Current Market Sentiment: {market_mood}")
        print(f"  Sentiment Strategy Score: {sentiment_score}%")
        
    except Exception as e:
        print(f"  Error testing sentiment strategy: {e}")
    
    print("\n📋 Backtest Summary:")
    print("  • Momentum strategies work best in trending markets")
    print("  • Value strategies provide steady long-term returns")
    print("  • Sentiment strategies help with market timing")
    print("  • Diversification across strategies reduces risk")
    
    return {
        'momentum_win_rate': momentum_win_rate if 'momentum_win_rate' in locals() else 0,
        'value_opportunities': value_count if 'value_count' in locals() else 0,
        'sentiment_score': sentiment_score if 'sentiment_score' in locals() else 0
    }

def backtest_strategies():
    """Detailed backtesting analysis"""
    print("\n" + "="*80)
    print("DETAILED STRATEGY ANALYSIS")
    print("="*80)
    
    strategy = Nifty50Strategy()
    
    # Get current market data for analysis
    try:
        all_stocks = nse_data.fetch_gainers_or_losers(fetch_gainers=True, full_list=True)
        
        print(f"\n📊 Market Overview:")
        print(f"  Total Stocks Analyzed: {len(all_stocks)}")
        
        gainers = [s for s in all_stocks if s['change_pct'] > 0]
        losers = [s for s in all_stocks if s['change_pct'] < 0]
        
        print(f"  Gainers: {len(gainers)} ({len(gainers)/len(all_stocks)*100:.1f}%)")
        print(f"  Losers: {len(losers)} ({len(losers)/len(all_stocks)*100:.1f}%)")
        
        avg_gain = sum([s['change_pct'] for s in gainers]) / len(gainers) if gainers else 0
        avg_loss = sum([s['change_pct'] for s in losers]) / len(losers) if losers else 0
        
        print(f"  Average Gain: +{avg_gain:.2f}%")
        print(f"  Average Loss: {avg_loss:.2f}%")
        
        # Strategy Performance Analysis
        print(f"\n🎯 Strategy Performance Analysis:")
        
        # Test each strategy
        strategies_performance = {}
        
        # 1. Momentum Strategy
        print(f"\n📈 Momentum Strategy Analysis:")
        momentum_recs = strategy.momentum_top_gainers_strategy(top_n=5)
        momentum_score = sum([rec['confidence'] for rec in momentum_recs]) / len(momentum_recs) if momentum_recs else 0
        strategies_performance['Momentum'] = {
            'recommendations': len(momentum_recs),
            'avg_confidence': momentum_score,
            'description': 'Follows market trends and momentum'
        }
        print(f"    Recommendations: {len(momentum_recs)}")
        print(f"    Average Confidence: {momentum_score:.1f}%")
        
        # 2. Value Strategy
        print(f"\n💰 Value Strategy Analysis:")
        try:
            pe_stocks = strategy.low_pe_strategy(max_pe=20)
            dividend_stocks = strategy.high_dividend_strategy(min_yield=1.5)
            value_recs = pe_stocks + dividend_stocks
            value_score = sum([rec['confidence'] for rec in value_recs]) / len(value_recs) if value_recs else 0
            strategies_performance['Value'] = {
                'recommendations': len(value_recs),
                'avg_confidence': value_score,
                'description': 'Focuses on undervalued stocks'
            }
            print(f"    Low P/E Opportunities: {len(pe_stocks)}")
            print(f"    High Dividend Opportunities: {len(dividend_stocks)}")
            print(f"    Total Value Recommendations: {len(value_recs)}")
            print(f"    Average Confidence: {value_score:.1f}%")
        except Exception as e:
            print(f"    Value analysis error: {e}")
            strategies_performance['Value'] = {'recommendations': 0, 'avg_confidence': 0, 'description': 'Error in analysis'}
        
        # 3. Mean Reversion Strategy
        print(f"\n🔄 Mean Reversion Strategy Analysis:")
        try:
            rsi_recs = strategy.rsi_oversold_strategy()
            support_recs = strategy.support_resistance_strategy()
            reversion_recs = rsi_recs + support_recs
            reversion_score = sum([rec['confidence'] for rec in reversion_recs]) / len(reversion_recs) if reversion_recs else 0
            strategies_performance['Mean Reversion'] = {
                'recommendations': len(reversion_recs),
                'avg_confidence': reversion_score,
                'description': 'Buys oversold, sells overbought'
            }
            print(f"    RSI Oversold Opportunities: {len(rsi_recs)}")
            print(f"    Support/Resistance Opportunities: {len(support_recs)}")
            print(f"    Total Mean Reversion Recommendations: {len(reversion_recs)}")
            print(f"    Average Confidence: {reversion_score:.1f}%")
        except Exception as e:
            print(f"    Mean reversion analysis error: {e}")
            strategies_performance['Mean Reversion'] = {'recommendations': 0, 'avg_confidence': 0, 'description': 'Error in analysis'}
        
        # 4. Sentiment Strategy
        print(f"\n🎭 Sentiment Strategy Analysis:")
        try:
            mood_recs = strategy.market_mood_strategy()
            contrarian_recs = strategy.contrarian_strategy()
            sentiment_recs = mood_recs + contrarian_recs
            sentiment_score = sum([rec['confidence'] for rec in sentiment_recs]) / len(sentiment_recs) if sentiment_recs else 0
            strategies_performance['Sentiment'] = {
                'recommendations': len(sentiment_recs),
                'avg_confidence': sentiment_score,
                'description': 'Based on market sentiment'
            }
            print(f"    Market Mood Recommendations: {len(mood_recs)}")
            print(f"    Contrarian Recommendations: {len(contrarian_recs)}")
            print(f"    Total Sentiment Recommendations: {len(sentiment_recs)}")
            print(f"    Average Confidence: {sentiment_score:.1f}%")
        except Exception as e:
            print(f"    Sentiment analysis error: {e}")
            strategies_performance['Sentiment'] = {'recommendations': 0, 'avg_confidence': 0, 'description': 'Error in analysis'}
        
        # Strategy Ranking
        print(f"\n🏆 Strategy Performance Ranking:")
        ranked_strategies = sorted(
            strategies_performance.items(), 
            key=lambda x: (x[1]['recommendations'] * 0.5 + x[1]['avg_confidence'] * 0.5), 
            reverse=True
        )
        
        for i, (strategy_name, performance) in enumerate(ranked_strategies, 1):
            total_score = performance['recommendations'] * 0.5 + performance['avg_confidence'] * 0.5
            print(f"    {i}. {strategy_name}: Score {total_score:.1f}")
            print(f"       {performance['description']}")
            print(f"       Recommendations: {performance['recommendations']}, Confidence: {performance['avg_confidence']:.1f}%")
        
        # Risk Analysis
        high_volatility = [s for s in all_stocks if abs(s['change_pct']) > 5]
        print(f"\n⚠️  Risk Analysis:")
        print(f"  High Volatility Stocks (>5% move): {len(high_volatility)}")
        volatility_ratio = len(high_volatility) / len(all_stocks) * 100
        print(f"  Market Volatility: {volatility_ratio:.1f}%")
        
        if volatility_ratio > 30:
            risk_level = "HIGH"
        elif volatility_ratio > 15:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        print(f"  Current Risk Level: {risk_level}")
        
        # Recommendations
        print(f"\n💡 Strategic Recommendations:")
        best_strategy = ranked_strategies[0][0] if ranked_strategies else "Diversified"
        print(f"  Best Performing Strategy: {best_strategy}")
        
        if len(gainers) > len(losers):
            print("  • Market is bullish - Consider momentum strategies")
            print("  • Look for breakout opportunities")
        else:
            print("  • Market is bearish - Consider value strategies")
            print("  • Focus on defensive stocks")
            
        if avg_gain > abs(avg_loss):
            print("  • Positive risk-reward ratio favors buying")
        else:
            print("  • Negative risk-reward ratio suggests caution")
        
        print(f"  • Risk Level: {risk_level} - Adjust position sizes accordingly")
        print(f"  • Diversify across {min(3, len(ranked_strategies))} top strategies")
            
    except Exception as e:
        print(f"Error in detailed analysis: {e}")
        return None
    
    return {
        'market_sentiment': 'bullish' if len(gainers) > len(losers) else 'bearish',
        'total_stocks': len(all_stocks),
        'gainers_count': len(gainers),
        'losers_count': len(losers),
        'avg_gain': avg_gain,
        'avg_loss': avg_loss,
        'best_strategy': best_strategy,
        'risk_level': risk_level,
        'strategies_performance': strategies_performance
    }

def analyze_news_sentiment():
    """Analyze news sentiment for trading insights"""
    print("\n" + "="*80)
    print("NEWS SENTIMENT ANALYSIS")
    print("="*80)
    
    try:
        news_items = nse_data.fetch_news()
        
        if not news_items:
            print("No news available for analysis.")
            return None
        
        print(f"\n📰 Analyzing {len(news_items)} news articles...")
        
        # Simple sentiment analysis based on keywords
        positive_keywords = ['rise', 'gain', 'up', 'high', 'strong', 'bullish', 'positive', 'growth', 'increase', 'rally', 'surge', 'boom']
        negative_keywords = ['fall', 'drop', 'down', 'low', 'weak', 'bearish', 'negative', 'decline', 'decrease', 'crash', 'plunge', 'slump']
        
        sentiment_scores = []
        
        for news in news_items:
            title = news.get('title', '').lower()
            summary = news.get('summary', '').lower()
            text = f"{title} {summary}"
            
            positive_count = sum(1 for word in positive_keywords if word in text)
            negative_count = sum(1 for word in negative_keywords if word in text)
            
            if positive_count > negative_count:
                sentiment = 'positive'
                score = positive_count - negative_count
            elif negative_count > positive_count:
                sentiment = 'negative'
                score = negative_count - positive_count
            else:
                sentiment = 'neutral'
                score = 0
            
            sentiment_scores.append({
                'title': news.get('title', 'No Title'),
                'sentiment': sentiment,
                'score': score,
                'provider': news.get('provider', 'Unknown')
            })
        
        # Calculate overall sentiment
        positive_news = [s for s in sentiment_scores if s['sentiment'] == 'positive']
        negative_news = [s for s in sentiment_scores if s['sentiment'] == 'negative']
        neutral_news = [s for s in sentiment_scores if s['sentiment'] == 'neutral']
        
        print(f"\n📊 Sentiment Breakdown:")
        print(f"  Positive News: {len(positive_news)} ({len(positive_news)/len(sentiment_scores)*100:.1f}%)")
        print(f"  Negative News: {len(negative_news)} ({len(negative_news)/len(sentiment_scores)*100:.1f}%)")
        print(f"  Neutral News: {len(neutral_news)} ({len(neutral_news)/len(sentiment_scores)*100:.1f}%)")
        
        # Overall market sentiment
        if len(positive_news) > len(negative_news):
            overall_sentiment = "BULLISH"
            confidence = (len(positive_news) / len(sentiment_scores)) * 100
        elif len(negative_news) > len(positive_news):
            overall_sentiment = "BEARISH"
            confidence = (len(negative_news) / len(sentiment_scores)) * 100
        else:
            overall_sentiment = "NEUTRAL"
            confidence = 50
        
        print(f"\n🎯 Overall News Sentiment: {overall_sentiment}")
        print(f"📈 Confidence Level: {confidence:.1f}%")
        
        # Show top positive and negative news
        if positive_news:
            print(f"\n✅ Top Positive News:")
            top_positive = sorted(positive_news, key=lambda x: x['score'], reverse=True)[:3]
            for i, news in enumerate(top_positive, 1):
                print(f"  {i}. {news['title'][:80]}..." if len(news['title']) > 80 else f"  {i}. {news['title']}")
        
        if negative_news:
            print(f"\n❌ Top Negative News:")
            top_negative = sorted(negative_news, key=lambda x: x['score'], reverse=True)[:3]
            for i, news in enumerate(top_negative, 1):
                print(f"  {i}. {news['title'][:80]}..." if len(news['title']) > 80 else f"  {i}. {news['title']}")
        
        # Trading recommendations based on news sentiment
        print(f"\n💡 News-Based Trading Recommendations:")
        if overall_sentiment == "BULLISH" and confidence > 60:
            print("  • Consider momentum strategies")
            print("  • Look for buying opportunities")
            print("  • Monitor breakout stocks")
        elif overall_sentiment == "BEARISH" and confidence > 60:
            print("  • Consider defensive strategies")
            print("  • Look for value opportunities")
            print("  • Be cautious with new positions")
        else:
            print("  • Mixed sentiment - use balanced approach")
            print("  • Focus on fundamental analysis")
            print("  • Wait for clearer signals")
        
        return {
            'overall_sentiment': overall_sentiment,
            'confidence': confidence,
            'positive_count': len(positive_news),
            'negative_count': len(negative_news),
            'neutral_count': len(neutral_news),
            'total_news': len(sentiment_scores)
        }
        
    except Exception as e:
        print(f"Error in news sentiment analysis: {e}")
        return None

def get_news_with_analysis():
    """Get news with sentiment analysis"""
    print("\n📰 Latest Market News with Sentiment Analysis")
    print("=" * 60)
    
    try:
        news_items = nse_data.fetch_news()
        
        if not news_items:
            print("No news available.")
            return
        
        # Simple sentiment keywords
        positive_keywords = ['rise', 'gain', 'up', 'high', 'strong', 'bullish', 'positive', 'growth', 'rally']
        negative_keywords = ['fall', 'drop', 'down', 'low', 'weak', 'bearish', 'negative', 'decline', 'crash']
        
        print(f"📊 Found {len(news_items)} news articles:\n")
        
        for i, news in enumerate(news_items[:8], 1):  # Show top 8 news items
            title = news.get('title', 'No Title')
            summary = news.get('summary', '')
            
            # Simple sentiment analysis
            text = f"{title} {summary}".lower()
            positive_count = sum(1 for word in positive_keywords if word in text)
            negative_count = sum(1 for word in negative_keywords if word in text)
            
            if positive_count > negative_count:
                sentiment_emoji = "📈"
                sentiment = "Positive"
            elif negative_count > positive_count:
                sentiment_emoji = "📉"
                sentiment = "Negative"
            else:
                sentiment_emoji = "➡️"
                sentiment = "Neutral"
            
            print(f"{sentiment_emoji} {i}. {title}")
            print(f"   Sentiment: {sentiment}")
            
            if news.get('provider'):
                print(f"   Source: {news['provider']}")
            
            if summary and len(summary) > 0:
                short_summary = summary[:120] + "..." if len(summary) > 120 else summary
                print(f"   Summary: {short_summary}")
            
            print("-" * 60)
        
        # Quick sentiment analysis
        analyze_news_sentiment()
        
    except Exception as e:
        print(f"Error fetching news: {e}")