"""
Centralized news utilities to eliminate duplication
"""
from typing import List, Dict, Any, Optional
from data import nse_data


class NewsAnalyzer:
    """Centralized news analysis functionality"""
    
    POSITIVE_KEYWORDS = [
        'rise', 'gain', 'up', 'high', 'strong', 'bullish', 'positive', 
        'growth', 'increase', 'rally', 'surge', 'boom', 'profit', 'beat'
    ]
    
    NEGATIVE_KEYWORDS = [
        'fall', 'drop', 'down', 'low', 'weak', 'bearish', 'negative', 
        'decline', 'decrease', 'crash', 'plunge', 'slump', 'loss', 'miss'
    ]
    
    def __init__(self):
        self.news_items = []
        self.sentiment_scores = []
    
    def fetch_news(self) -> List[Dict[str, Any]]:
        """Fetch and cache news"""
        try:
            self.news_items = nse_data.fetch_news()
            return self.news_items
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of a single text"""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.POSITIVE_KEYWORDS if word in text_lower)
        negative_count = sum(1 for word in self.NEGATIVE_KEYWORDS if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = 'positive'
            score = positive_count - negative_count
            emoji = "📈"
        elif negative_count > positive_count:
            sentiment = 'negative'
            score = negative_count - positive_count
            emoji = "📉"
        else:
            sentiment = 'neutral'
            score = 0
            emoji = "➡️"
        
        return {
            'sentiment': sentiment,
            'score': score,
            'emoji': emoji,
            'positive_count': positive_count,
            'negative_count': negative_count
        }
    
    def analyze_all_news(self) -> Dict[str, Any]:
        """Analyze sentiment of all news"""
        if not self.news_items:
            self.fetch_news()
        
        self.sentiment_scores = []
        
        for news in self.news_items:
            title = news.get('title', '')
            summary = news.get('summary', '')
            text = f"{title} {summary}"
            
            sentiment_data = self.analyze_sentiment(text)
            
            self.sentiment_scores.append({
                'title': news.get('title', 'No Title'),
                'sentiment': sentiment_data['sentiment'],
                'score': sentiment_data['score'],
                'emoji': sentiment_data['emoji'],
                'provider': news.get('provider', 'Unknown'),
                'pub_date': news.get('pub_date', ''),
                'url': news.get('url', '')
            })
        
        return self._calculate_overall_sentiment()
    
    def _calculate_overall_sentiment(self) -> Dict[str, Any]:
        """Calculate overall market sentiment from news"""
        if not self.sentiment_scores:
            return {}
        
        positive_news = [s for s in self.sentiment_scores if s['sentiment'] == 'positive']
        negative_news = [s for s in self.sentiment_scores if s['sentiment'] == 'negative']
        neutral_news = [s for s in self.sentiment_scores if s['sentiment'] == 'neutral']
        
        total_news = len(self.sentiment_scores)
        positive_ratio = len(positive_news) / total_news
        negative_ratio = len(negative_news) / total_news
        
        if positive_ratio > negative_ratio:
            overall_sentiment = "BULLISH"
            confidence = positive_ratio * 100
        elif negative_ratio > positive_ratio:
            overall_sentiment = "BEARISH"
            confidence = negative_ratio * 100
        else:
            overall_sentiment = "NEUTRAL"
            confidence = 50
        
        return {
            'overall_sentiment': overall_sentiment,
            'confidence': confidence,
            'positive_count': len(positive_news),
            'negative_count': len(negative_news),
            'neutral_count': len(neutral_news),
            'total_news': total_news,
            'positive_ratio': positive_ratio,
            'negative_ratio': negative_ratio,
            'sentiment_scores': self.sentiment_scores
        }
    
    def display_news_with_sentiment(self, max_items: int = 8):
        """Display news with sentiment indicators"""
        print("\n📰 Latest Market News with Sentiment Analysis")
        print("=" * 60)
        
        if not self.sentiment_scores:
            self.analyze_all_news()
        
        if not self.sentiment_scores:
            print("No news available.")
            return
        
        print(f"📊 Found {len(self.sentiment_scores)} news articles:\n")
        
        for i, news in enumerate(self.sentiment_scores[:max_items], 1):
            print(f"{news['emoji']} {i}. {news['title']}")
            print(f"   Sentiment: {news['sentiment'].title()}")
            
            if news['provider']:
                print(f"   Source: {news['provider']}")
            
            print("-" * 60)
    
    def display_sentiment_summary(self):
        """Display sentiment analysis summary"""
        sentiment_data = self.analyze_all_news()
        
        if not sentiment_data:
            print("No sentiment data available.")
            return
        
        print(f"\n📊 Sentiment Breakdown:")
        print(f"  Positive News: {sentiment_data['positive_count']} ({sentiment_data['positive_ratio']*100:.1f}%)")
        print(f"  Negative News: {sentiment_data['negative_count']} ({sentiment_data['negative_ratio']*100:.1f}%)")
        print(f"  Neutral News: {sentiment_data['neutral_count']} ({(1-sentiment_data['positive_ratio']-sentiment_data['negative_ratio'])*100:.1f}%)")
        
        print(f"\n🎯 Overall News Sentiment: {sentiment_data['overall_sentiment']}")
        print(f"📈 Confidence Level: {sentiment_data['confidence']:.1f}%")
        
        # Trading recommendations
        self._display_trading_recommendations(sentiment_data)
    
    def _display_trading_recommendations(self, sentiment_data: Dict[str, Any]):
        """Display trading recommendations based on sentiment"""
        print(f"\n💡 News-Based Trading Recommendations:")
        
        overall_sentiment = sentiment_data['overall_sentiment']
        confidence = sentiment_data['confidence']
        
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
    
    def get_top_news_by_sentiment(self, sentiment_type: str, count: int = 3) -> List[Dict[str, Any]]:
        """Get top news by sentiment type"""
        if not self.sentiment_scores:
            self.analyze_all_news()
        
        filtered_news = [
            news for news in self.sentiment_scores 
            if news['sentiment'] == sentiment_type
        ]
        
        return sorted(filtered_news, key=lambda x: x['score'], reverse=True)[:count]


# Global news analyzer instance
news_analyzer = NewsAnalyzer()
