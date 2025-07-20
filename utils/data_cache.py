"""
Data caching utility to avoid redundant API calls
"""
import time
from typing import Dict, Any, Optional
from data import nse_data


class DataCache:
    """Cache for stock data to reduce API calls"""
    
    def __init__(self, cache_duration=300):  # 5 minutes default
        self.cache = {}
        self.cache_duration = cache_duration
    
    def _is_cache_valid(self, timestamp: float) -> bool:
        """Check if cached data is still valid"""
        return time.time() - timestamp < self.cache_duration
    
    def get_stock_data(self, symbol: str, full: bool = False) -> Optional[Dict[str, Any]]:
        """Get cached stock data or fetch if not available"""
        cache_key = f"{symbol}_{full}"
        
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if self._is_cache_valid(timestamp):
                return data
        
        # Fetch fresh data
        try:
            data = nse_data.fetch_stock_data(symbol, full)
            self.cache[cache_key] = (data, time.time())
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
    
    def get_market_data(self) -> Optional[Dict[str, Any]]:
        """Get cached market data"""
        cache_key = "market_data"
        
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if self._is_cache_valid(timestamp):
                return data
        
        # Fetch fresh market data
        try:
            data = {
                'gainers': nse_data.fetch_gainers_or_losers(fetch_gainers=True, full_list=True),
                'mood': nse_data.fetch_market_mood(),
                'news': nse_data.fetch_news()
            }
            self.cache[cache_key] = (data, time.time())
            return data
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return None
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()


# Global cache instance
data_cache = DataCache()
