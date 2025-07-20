"""
Investor Bot - Nifty 50 Strategy Runner

This script demonstrates various investment strategies for Nifty 50 stocks.
You can run different strategies individually or get comprehensive recommendations.
"""

from rules import nifty50_strategy

def main():
    print("🚀 Welcome to Nifty 50 Investment Strategy Bot!")
    print("=" * 60)
    
    while True:
        print("\nChoose a strategy to run:")
        print("1. Momentum Strategies (Top Gainers + MA Crossover)")
        print("2. Value Strategies (Low P/E + High Dividend)")
        print("3. Sentiment Strategies (Market Mood + Contrarian)")
        print("4. Mean Reversion Strategies (RSI + Support/Resistance)")
        print("5. Comprehensive Analysis (All Strategies)")
        print("6. Quick Market Overview")
        print("7. Backtest Strategies (Performance Analysis)")
        print("8. Latest Market News")
        print("9. Exit")

        choice = input("\nEnter your choice (1-9): ").strip()

        try:
            if choice == '1':
                nifty50_strategy.run_momentum_strategy()
            elif choice == '2':
                nifty50_strategy.run_value_strategy()
            elif choice == '3':
                nifty50_strategy.run_sentiment_strategy()
            elif choice == '4':
                strategy = nifty50_strategy.Nifty50Strategy()
                rsi_recs = strategy.rsi_oversold_strategy()
                support_recs = strategy.support_resistance_strategy()
                all_recs = rsi_recs + support_recs
                strategy.print_recommendations(all_recs)
            elif choice == '5':
                nifty50_strategy.run_comprehensive_analysis()
            elif choice == '6':
                print("\n📊 Quick Market Overview:")
                print("Current Market Mood:", nifty50_strategy.nse_data.fetch_market_mood())
                print("\nTop 5 Gainers:")
                gainers = nifty50_strategy.nse_data.fetch_gainers_or_losers(fetch_gainers=True)
                for stock in gainers:
                    print(f"  {stock['symbol'].replace('.NS', '')}: +{stock['change_pct']:.2f}%")
                print("\nTop 5 Losers:")
                losers = nifty50_strategy.nse_data.fetch_gainers_or_losers(fetch_gainers=False)
                for stock in losers:
                    print(f"  {stock['symbol'].replace('.NS', '')}: {stock['change_pct']:.2f}%")
            elif choice == '7':
                print("\n🔍 Backtesting Strategies...")
                print("Choose backtesting option:")
                print("  a) Quick Backtest (Simplified)")
                print("  b) Detailed Analysis") 
                print("  c) Full Historical Backtest")
                
                backtest_choice = input("Enter choice (a/b/c): ").strip().lower()
                
                if backtest_choice == 'a':
                    nifty50_strategy.run_simplified_backtest()
                elif backtest_choice == 'b':
                    nifty50_strategy.backtest_strategies()
                elif backtest_choice == 'c':
                    nifty50_strategy.run_backtest()
                else:
                    print("Invalid choice, running simplified backtest...")
                    nifty50_strategy.run_simplified_backtest()
            elif choice == '8':
                print("\n📰 Latest Market News:")
                print("Choose news option:")
                print("  a) Latest News Headlines")
                print("  b) News with Sentiment Analysis") 
                print("  c) Detailed News Analysis")
                
                news_choice = input("Enter choice (a/b/c): ").strip().lower()
                
                if news_choice == 'a':
                    print("\n📰 Latest Market News:")
                    print("=" * 60)
                    try:
                        news_items = nifty50_strategy.nse_data.fetch_news()
                        
                        if not news_items:
                            print("No news available at the moment.")
                        else:
                            print(f"Found {len(news_items)} news articles:\n")
                            
                            for i, news in enumerate(news_items[:10], 1):  # Show top 10 news items
                                print(f"{i}. {news.get('title', 'No Title')}")
                                
                                if news.get('provider'):
                                    print(f"   Source: {news['provider']}")
                                
                                if news.get('summary'):
                                    # Truncate summary if too long
                                    summary = news['summary']
                                    if len(summary) > 150:
                                        summary = summary[:147] + "..."
                                    print(f"   Summary: {summary}")
                                
                                if news.get('pub_date'):
                                    print(f"   Date: {news['pub_date']}")
                                
                                if news.get('url'):
                                    print(f"   URL: {news['url']}")
                                
                                print("-" * 60)
                    except Exception as e:
                        print(f"Error fetching news: {e}")
                
                elif news_choice == 'b':
                    nifty50_strategy.get_news_with_analysis()
                
                elif news_choice == 'c':
                    nifty50_strategy.analyze_news_sentiment()
                
                else:
                    print("Invalid choice, showing basic news...")
                    try:
                        news_items = nifty50_strategy.nse_data.fetch_news()
                        if news_items:
                            for i, news in enumerate(news_items[:5], 1):
                                print(f"{i}. {news.get('title', 'No Title')}")
                        else:
                            print("No news available.")
                    except Exception as e:
                        print(f"Error fetching news: {e}")
                
                # Option to get detailed news
                if news_choice == 'a':
                    try:
                        news_items = nifty50_strategy.nse_data.fetch_news()
                        if news_items:
                            detail_choice = input("\nWould you like to see detailed news? (y/n): ").strip().lower()
                            if detail_choice == 'y':
                                try:
                                    news_num = int(input(f"Enter news number (1-{min(len(news_items), 10)}): "))
                                    if 1 <= news_num <= min(len(news_items), 10):
                                        selected_news = news_items[news_num - 1]
                                        print(f"\n📰 Detailed News Article:")
                                        print("=" * 60)
                                        print(f"Title: {selected_news.get('title', 'No Title')}")
                                        print(f"Source: {selected_news.get('provider', 'Unknown')}")
                                        print(f"Date: {selected_news.get('pub_date', 'Unknown')}")
                                        print(f"Summary: {selected_news.get('summary', 'No summary available')}")
                                        if selected_news.get('url'):
                                            print(f"Full Article: {selected_news['url']}")
                                    else:
                                        print("Invalid news number.")
                                except ValueError:
                                    print("Please enter a valid number.")
                    except Exception as e:
                        print(f"Error in detailed news view: {e}")
            elif choice == '9':
                print("Thank you for using Nifty 50 Strategy Bot! 👋")
                break
            else:
                print("Invalid choice. Please try again.")
                
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()