#!/usr/bin/env python3
"""
Backtest Demo - Nifty 50 Strategies

This script demonstrates the backtesting functionality for various
Nifty 50 investment strategies.
"""

from rules import nifty50_strategy

def demo_backtesting():
    """Demonstrate all backtesting features"""
    
    print("🎯 NIFTY 50 STRATEGY BACKTESTING DEMO")
    print("=" * 60)
    
    print("\n1. Running Simplified Backtest...")
    print("-" * 40)
    try:
        simple_result = nifty50_strategy.run_simplified_backtest()
        print(f"✅ Simplified backtest completed successfully!")
        print(f"📊 Results: {simple_result}")
    except Exception as e:
        print(f"❌ Error in simplified backtest: {e}")
    
    print("\n" + "=" * 60)
    print("\n2. Running Detailed Strategy Analysis...")
    print("-" * 40)
    try:
        detailed_result = nifty50_strategy.backtest_strategies()
        print(f"✅ Detailed analysis completed successfully!")
        if detailed_result:
            print(f"🎯 Best Strategy: {detailed_result.get('best_strategy', 'N/A')}")
            print(f"📈 Market Sentiment: {detailed_result.get('market_sentiment', 'N/A')}")
            print(f"⚠️  Risk Level: {detailed_result.get('risk_level', 'N/A')}")
            print(f"📊 Total Stocks: {detailed_result.get('total_stocks', 'N/A')}")
    except Exception as e:
        print(f"❌ Error in detailed analysis: {e}")
    
    print("\n" + "=" * 60)
    print("\n3. Strategy Comparison Summary...")
    print("-" * 40)
    
    print("🔍 Available Backtesting Options:")
    print("  a) Quick Backtest - Fast overview of strategy performance")
    print("  b) Detailed Analysis - Comprehensive strategy comparison")
    print("  c) Full Historical Backtest - Deep historical analysis")
    
    print("\n📋 How to Use Backtesting:")
    print("  1. Run 'python main.py'")
    print("  2. Choose option 7 (Backtest Strategies)")
    print("  3. Select your preferred backtest type")
    print("  4. Review the results and recommendations")
    
    print("\n💡 Backtesting Benefits:")
    print("  • Compare strategy performance")
    print("  • Understand market conditions")
    print("  • Make informed investment decisions")
    print("  • Identify best-performing strategies")
    print("  • Assess risk levels")
    
    print("\n🎯 Next Steps:")
    print("  • Use the best-performing strategy for live trading")
    print("  • Diversify across multiple strategies")
    print("  • Monitor market conditions regularly")
    print("  • Adjust strategies based on risk tolerance")

if __name__ == "__main__":
    demo_backtesting()
