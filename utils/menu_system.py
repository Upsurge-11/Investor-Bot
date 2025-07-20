"""
Optimized menu system to eliminate code duplication in main.py
"""
from typing import Dict, Callable, Any
from rules import nifty50_strategy
from utils.news_utils import news_analyzer
from data import nse_data


class MenuSystem:
    """Centralized menu system with reusable components"""
    
    def __init__(self):
        self.menu_options = {
            '1': ('Momentum Strategies', self.run_momentum_strategies),
            '2': ('Value Strategies', self.run_value_strategies),
            '3': ('Sentiment Strategies', self.run_sentiment_strategies),
            '4': ('Mean Reversion Strategies', self.run_mean_reversion_strategies),
            '5': ('Comprehensive Analysis', self.run_comprehensive_analysis),
            '6': ('Quick Market Overview', self.show_market_overview),
            '7': ('Backtest Strategies', self.run_backtest_menu),
            '8': ('Latest Market News', self.run_news_menu),
            '9': ('Exit', self.exit_program)
        }
    
    def display_main_menu(self):
        """Display the main menu"""
        print("\\nChoose a strategy to run:")
        for key, (description, _) in self.menu_options.items():
            print(f"{key}. {description}")
    
    def handle_menu_choice(self, choice: str) -> bool:
        """Handle menu choice and return False if should exit"""
        choice = choice.strip()
        
        if choice in self.menu_options:
            description, handler = self.menu_options[choice]
            try:
                return handler()
            except Exception as e:
                print(f"An error occurred in {description}: {e}")
                print("Please try again.")
                return True
        else:
            print("Invalid choice. Please try again.")
            return True
    
    def run_momentum_strategies(self) -> bool:
        """Run momentum strategies"""
        nifty50_strategy.run_momentum_strategy()
        return True
    
    def run_value_strategies(self) -> bool:
        """Run value strategies"""
        nifty50_strategy.run_value_strategy()
        return True
    
    def run_sentiment_strategies(self) -> bool:
        """Run sentiment strategies"""
        nifty50_strategy.run_sentiment_strategy()
        return True
    
    def run_mean_reversion_strategies(self) -> bool:
        """Run mean reversion strategies"""
        strategy = nifty50_strategy.Nifty50Strategy()
        rsi_recs = strategy.rsi_oversold_strategy()
        support_recs = strategy.support_resistance_strategy()
        all_recs = rsi_recs + support_recs
        strategy.print_recommendations(all_recs)
        return True
    
    def run_comprehensive_analysis(self) -> bool:
        """Run comprehensive analysis"""
        nifty50_strategy.run_comprehensive_analysis()
        return True
    
    def show_market_overview(self) -> bool:
        """Show quick market overview"""
        print("\\n📊 Quick Market Overview:")
        print("Current Market Mood:", nse_data.fetch_market_mood())
        
        print("\\nTop 5 Gainers:")
        gainers = nse_data.fetch_gainers_or_losers(fetch_gainers=True)
        for stock in gainers:
            print(f"  {stock['symbol'].replace('.NS', '')}: +{stock['change_pct']:.2f}%")
        
        print("\\nTop 5 Losers:")
        losers = nse_data.fetch_gainers_or_losers(fetch_gainers=False)
        for stock in losers:
            print(f"  {stock['symbol'].replace('.NS', '')}: {stock['change_pct']:.2f}%")
        
        return True
    
    def run_backtest_menu(self) -> bool:
        """Handle backtest menu"""
        print("\\n🔍 Backtesting Strategies...")
        print("Choose backtesting option:")
        print("  a) Quick Backtest (Simplified)")
        print("  b) Detailed Analysis")
        print("  c) Full Historical Backtest")
        
        backtest_choice = input("Enter choice (a/b/c): ").strip().lower()
        
        backtest_options = {
            'a': nifty50_strategy.run_simplified_backtest,
            'b': nifty50_strategy.backtest_strategies,
            'c': nifty50_strategy.run_backtest
        }
        
        handler = backtest_options.get(backtest_choice, nifty50_strategy.run_simplified_backtest)
        handler()
        
        return True
    
    def run_news_menu(self) -> bool:
        """Handle news menu"""
        print("\\n📰 Latest Market News:")
        print("Choose news option:")
        print("  a) Latest News Headlines")
        print("  b) News with Sentiment Analysis")
        print("  c) Detailed News Analysis")
        
        news_choice = input("Enter choice (a/b/c): ").strip().lower()
        
        news_options = {
            'a': self.show_basic_news,
            'b': self.show_news_with_sentiment,
            'c': self.show_detailed_news_analysis
        }
        
        handler = news_options.get(news_choice, self.show_basic_news)
        handler()
        
        return True
    
    def show_basic_news(self):
        """Show basic news headlines"""
        print("\\n📰 Latest Market News:")
        print("=" * 60)
        
        try:
            news_items = nse_data.fetch_news()
            
            if not news_items:
                print("No news available at the moment.")
                return
            
            print(f"Found {len(news_items)} news articles:\\n")
            
            for i, news in enumerate(news_items[:10], 1):
                print(f"{i}. {news.get('title', 'No Title')}")
                
                if news.get('provider'):
                    print(f"   Source: {news['provider']}")
                
                if news.get('summary'):
                    summary = news['summary']
                    if len(summary) > 150:
                        summary = summary[:147] + "..."
                    print(f"   Summary: {summary}")
                
                if news.get('pub_date'):
                    print(f"   Date: {news['pub_date']}")
                
                print("-" * 60)
            
            # Option for detailed view
            self.offer_detailed_news_view(news_items)
            
        except Exception as e:
            print(f"Error fetching news: {e}")
    
    def show_news_with_sentiment(self):
        """Show news with sentiment analysis"""
        news_analyzer.display_news_with_sentiment()
    
    def show_detailed_news_analysis(self):
        """Show detailed news analysis"""
        news_analyzer.display_sentiment_summary()
    
    def offer_detailed_news_view(self, news_items):
        """Offer detailed news view option"""
        try:
            detail_choice = input("\\nWould you like to see detailed news? (y/n): ").strip().lower()
            if detail_choice == 'y':
                try:
                    news_num = int(input(f"Enter news number (1-{min(len(news_items), 10)}): "))
                    if 1 <= news_num <= min(len(news_items), 10):
                        selected_news = news_items[news_num - 1]
                        self.display_detailed_news(selected_news)
                    else:
                        print("Invalid news number.")
                except ValueError:
                    print("Please enter a valid number.")
        except Exception as e:
            print(f"Error in detailed news view: {e}")
    
    def display_detailed_news(self, news_item):
        """Display detailed news article"""
        print(f"\\n📰 Detailed News Article:")
        print("=" * 60)
        print(f"Title: {news_item.get('title', 'No Title')}")
        print(f"Source: {news_item.get('provider', 'Unknown')}")
        print(f"Date: {news_item.get('pub_date', 'Unknown')}")
        print(f"Summary: {news_item.get('summary', 'No summary available')}")
        if news_item.get('url'):
            print(f"Full Article: {news_item['url']}")
    
    def exit_program(self) -> bool:
        """Exit the program"""
        print("Thank you for using Nifty 50 Strategy Bot! 👋")
        return False


def run_optimized_main():
    """Optimized main function"""
    menu_system = MenuSystem()
    
    print("🚀 Welcome to Nifty 50 Investment Strategy Bot!")
    print("=" * 60)
    
    while True:
        menu_system.display_main_menu()
        choice = input("\\nEnter your choice (1-9): ")
        
        should_continue = menu_system.handle_menu_choice(choice)
        if not should_continue:
            break
        
        input("\\nPress Enter to continue...")


if __name__ == "__main__":
    run_optimized_main()
