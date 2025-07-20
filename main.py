"""
Investor Bot - Nifty 50 Strategy Runner (Optimized)

This script demonstrates various investment strategies for Nifty 50 stocks.
You can run different strategies individually or get comprehensive recommendations.

OPTIMIZED VERSION: 
- Removed code duplication
- Uses centralized menu system
- Improved error handling
- Better separation of concerns
"""

from utils.menu_system import run_optimized_main

def main():
    """
    Main entry point - now uses optimized menu system
    This eliminates the 130+ lines of duplicate menu handling code
    """
    run_optimized_main()

if __name__ == "__main__":
    main()