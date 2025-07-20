#!/usr/bin/env python3
"""
News Demo - Nifty 50 Investment Bot

This script demonstrates the news fetching and sentiment analysis functionality.
"""

from data import nse_data
from rules import nifty50_strategy

def demo_news_functionality():
    """Demonstrate all news features"""
    
    print("📰 NIFTY 50 NEWS FUNCTIONALITY DEMO")
    print("=" * 60)
    
    print("\n1. Basic News Fetching...")
    print("-" * 40)
    try:
        news_items = nse_data.fetch_news()
        print(f"✅ Successfully fetched {len(news_items)} news articles!")
        
        if news_items:
            print("\n📰 Latest Headlines:")
            for i, news in enumerate(news_items[:5], 1):
                title = news.get('title', 'No Title')
                source = news.get('provider', 'Unknown Source')
                print(f"  {i}. {title}")
                print(f"     Source: {source}")
                print()
        
    except Exception as e:
        print(f"❌ Error fetching news: {e}")
    
    print("\n" + "=" * 60)
    print("\n2. News with Sentiment Analysis...")
    print("-" * 40)
    try:
        nifty50_strategy.get_news_with_analysis()
    except Exception as e:
        print(f"❌ Error in sentiment analysis: {e}")
    
    print("\n" + "=" * 60)
    print("\n3. News Features Available:")
    print("-" * 40)
    print("📋 Available News Options:")
    print("  a) Latest News Headlines - Quick overview of current news")
    print("  b) News with Sentiment Analysis - Headlines with market sentiment")
    print("  c) Detailed News Analysis - Comprehensive sentiment breakdown")
    
    print("\n💡 How to Use News Features:")
    print("  1. Run 'python main.py'")
    print("  2. Choose option 8 (Latest Market News)")
    print("  3. Select your preferred news view")
    print("  4. Use sentiment insights for trading decisions")
    
    print("\n🎯 News Analysis Benefits:")
    print("  • Stay updated with market developments")
    print("  • Understand market sentiment")
    print("  • Make informed trading decisions")
    print("  • Identify market trends early")
    print("  • Get sentiment-based recommendations")
    
    print("\n📈 Trading Applications:")
    print("  • Bullish news → Consider momentum strategies")
    print("  • Bearish news → Look for value opportunities")
    print("  • Mixed sentiment → Use balanced approach")
    print("  • High volatility news → Adjust position sizes")

if __name__ == "__main__":
    demo_news_functionality()
