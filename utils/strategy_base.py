"""
Base strategy class to eliminate code duplication
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from utils.data_cache import data_cache


class BaseStrategy(ABC):
    """Base class for all investment strategies"""
    
    def __init__(self, symbols: List[str]):
        self.symbols = symbols
        self.recommendations = []
    
    @abstractmethod
    def generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate strategy-specific recommendations"""
        pass
    
    def safe_execute(self, func, *args, **kwargs):
        """Execute function with error handling"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            return None
    
    def get_cached_stock_data(self, symbol: str, full: bool = False):
        """Get stock data with caching"""
        return data_cache.get_stock_data(symbol, full)
    
    def create_recommendation(self, symbol: str, action: str, strategy: str, 
                            reason: str, current_price: float, confidence: float) -> Dict[str, Any]:
        """Create standardized recommendation format"""
        return {
            'symbol': symbol,
            'action': action,
            'strategy': strategy,
            'reason': reason,
            'current_price': current_price,
            'confidence': confidence
        }
    
    def filter_recommendations(self, recommendations: List[Dict[str, Any]], 
                             min_confidence: float = 50) -> List[Dict[str, Any]]:
        """Filter recommendations by confidence"""
        return [rec for rec in recommendations if rec['confidence'] >= min_confidence]
    
    def sort_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort recommendations by confidence"""
        return sorted(recommendations, key=lambda x: x['confidence'], reverse=True)


class StrategyRunner:
    """Unified strategy runner to eliminate duplicate functions"""
    
    def __init__(self):
        self.strategies = {}
    
    def register_strategy(self, name: str, strategy: BaseStrategy):
        """Register a strategy"""
        self.strategies[name] = strategy
    
    def run_strategy(self, strategy_name: str) -> List[Dict[str, Any]]:
        """Run a specific strategy"""
        if strategy_name not in self.strategies:
            print(f"Strategy '{strategy_name}' not found")
            return []
        
        strategy = self.strategies[strategy_name]
        recommendations = strategy.generate_recommendations()
        
        if recommendations:
            self.print_recommendations(recommendations, strategy_name)
        else:
            print(f"No recommendations found for {strategy_name}")
        
        return recommendations
    
    def run_multiple_strategies(self, strategy_names: List[str]) -> List[Dict[str, Any]]:
        """Run multiple strategies and combine results"""
        all_recommendations = []
        
        for strategy_name in strategy_names:
            print(f"Running {strategy_name}...")
            recommendations = self.run_strategy(strategy_name)
            all_recommendations.extend(recommendations)
        
        # Remove duplicates and sort
        unique_recommendations = self._remove_duplicates(all_recommendations)
        return sorted(unique_recommendations, key=lambda x: x['confidence'], reverse=True)
    
    def _remove_duplicates(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate recommendations based on symbol"""
        seen_symbols = set()
        unique_recs = []
        
        for rec in recommendations:
            if rec['symbol'] not in seen_symbols:
                seen_symbols.add(rec['symbol'])
                unique_recs.append(rec)
        
        return unique_recs
    
    def print_recommendations(self, recommendations: List[Dict[str, Any]], title: str = "Recommendations"):
        """Unified recommendation printing"""
        if not recommendations:
            print("No recommendations found.")
            return
        
        print(f"\n{'='*80}")
        print(f"{title.upper()}")
        print("="*80)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['symbol'].replace('.NS', '')}")
            print(f"   Action: {rec['action']}")
            print(f"   Strategy: {rec['strategy']}")
            print(f"   Reason: {rec['reason']}")
            print(f"   Current Price: ₹{rec['current_price']:.2f}")
            print(f"   Confidence: {rec['confidence']:.1f}%")
            print("-" * 60)
