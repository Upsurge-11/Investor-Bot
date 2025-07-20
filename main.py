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
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
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