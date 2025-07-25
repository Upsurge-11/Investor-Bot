"""
nse_data.py

Utility functions for fetching and analyzing Nifty 50 stock data using yfinance.

Functions:
  - fetch_nifty50_symbols():
      Returns a list of all 50 Nifty 50 stock symbols with the '.NS' suffix.

  - fetch_stock_data(symbol, full=False):
      Fetches stock data for a given symbol. Returns fast info or full info.

  - fetch_gainers_or_losers(fetch_gainers=True, full_list=False):
      Calculates daily percentage change for all Nifty 50 stocks and returns top gainers, losers, or the full sorted list.

  - fetch_market_mood():
      Analyzes Nifty 50 stock performance to determine if the market is bullish, bearish, or neutral.

  - fetch_news():
      Fetches the latest news for the Nifty 50 index, returning a list of news items with details.
"""
import yfinance as yf

"""
Fetches the list of Nifty 50 stock symbols.

Returns a hardcoded list of all 50 stock symbols that are part of the 
Nifty 50 index, formatted with the '.NS' suffix for NSE (National Stock Exchange).

Returns:
    list[str]: A list containing all 50 Nifty stock symbols with NSE suffix
"""
def fetch_nifty50_symbols() -> list[str]:
  return [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'BHARTIARTL.NS', 'ICICIBANK.NS',
    'INFY.NS', 'SBIN.NS', 'LICI.NS', 'ITC.NS', 'HINDUNILVR.NS',
    'LT.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS',
    'SUNPHARMA.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'BAJFINANCE.NS', 'NESTLEIND.NS',
    'ADANIENT.NS', 'HCLTECH.NS', 'WIPRO.NS', 'NTPC.NS', 'JSWSTEEL.NS',
    'POWERGRID.NS', 'TATAMOTORS.NS', 'COALINDIA.NS', 'M&M.NS', 'BAJAJFINSV.NS',
    'TATASTEEL.NS', 'TECHM.NS', 'GRASIM.NS', 'ADANIPORTS.NS', 'INDUSINDBK.NS',
    'CIPLA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'BRITANNIA.NS', 'APOLLOHOSP.NS',
    'BPCL.NS', 'DIVISLAB.NS', 'TRENT.NS', 'BAJAJ-AUTO.NS', 'ONGC.NS',
    'HEROMOTOCO.NS', 'SBILIFE.NS', 'HDFCLIFE.NS', 'SHRIRAMFIN.NS', 'LTIM.NS'
  ]

"""
Fetches stock data for a given symbol using yfinance.

Retrieves either full stock information or fast info based on the 'full' parameter.
Fast info includes basic metrics like current price, while full info includes
comprehensive company and financial data.

Args:
    symbol (str): The stock symbol to fetch data for (e.g., 'RELIANCE.NS')
    full (bool, optional):  If True, returns comprehensive stock info. 
                            If False, returns fast info only. Defaults to False.

Returns:
    dict: Stock data containing price information and other metrics
"""
def fetch_stock_data(symbol: str, full: bool = False) -> dict:
  ticker = yf.Ticker(symbol)
  if full:
    return ticker.info
  return dict(ticker.fast_info)

"""
Fetches top gaining or losing stocks from the Nifty 50 index.

Analyzes all Nifty 50 stocks to calculate their daily percentage change
(based on open vs last price) and returns either top gainers or losers.
Can return either top 5 or the complete sorted list.

Args:
    fetch_gainers (bool, optional): If True, returns top gainers. 
                                    If False, returns top losers. Defaults to True.
    full_list (bool, optional): If True, returns all stocks sorted by performance.
                                If False, returns only top 5. Defaults to False.

Returns:
    list[dict]: List of dictionaries containing stock symbol, open price, 
                last price, and percentage change for each stock
"""
def fetch_gainers_or_losers(fetch_gainers: bool = True, full_list: bool = False) -> list[dict]:
  symbols = fetch_nifty50_symbols()
  stock_performance_list = []

  for symbol in symbols:
    try:
      data = fetch_stock_data(symbol)
      open_price = data.get('open')
      last_price = data.get('lastPrice')
      if open_price and last_price:
        change_pct = ((last_price - open_price) / open_price) * 100
        stock_performance_list.append({
          'symbol': symbol,
          'open': open_price,
          'lastPrice': last_price,
          'change_pct': change_pct
        })
    except Exception:
      print(f"Error fetching data for {symbol}")
  if full_list:
    stock_performance_list = sorted(stock_performance_list, key=lambda x: x['change_pct'], reverse=True)
  elif fetch_gainers:
    stock_performance_list = sorted(stock_performance_list, key=lambda x: x['change_pct'], reverse=True)[:5]
  else:
    stock_performance_list = sorted(stock_performance_list, key=lambda x: x['change_pct'])[:5]
  return stock_performance_list

"""
Analyzes the overall market sentiment based on Nifty 50 stock performance.

Calculates the percentage of stocks that are gaining vs losing in the Nifty 50
index and determines if the market mood is bullish, bearish, or neutral.
Also provides average gain/loss percentages for context.

Returns:
    str:  A descriptive string indicating market mood (bullish/bearish/neutral)
          with supporting statistics including percentages of gainers/losers
          and average gain/loss percentages
"""
def fetch_market_mood() -> str:
  stock_performance_list = fetch_gainers_or_losers(full_list=True)
  if not stock_performance_list:
    return "No data available to determine market mood."
  bull = 0
  bear = 0
  avg_bull_change = []
  avg_bear_change = []
  for stock in stock_performance_list:
    if stock['change_pct'] > 0:
      bull += 1
      avg_bull_change.append(stock['change_pct'])
    else:
      bear += 1
      avg_bear_change.append(stock['change_pct'])
  if bull > bear:
    percentage = (bull / len(stock_performance_list)) * 100
    avg_bull_change_pct = sum(avg_bull_change) / len(avg_bull_change) if avg_bull_change else 0
    avg_bear_change_pct = sum(avg_bear_change) / len(avg_bear_change) if avg_bear_change else 0
    return f"Market is bullish with {percentage:.2f}% of stocks gaining and an average gain of {avg_bull_change_pct:.2f}%. Stocks losing on average {avg_bear_change_pct:.2f}%."
  
  elif bear > bull:
    percentage = (bear / len(stock_performance_list)) * 100
    avg_bear_change_pct = sum(avg_bear_change) / len(avg_bear_change) if avg_bear_change else 0
    avg_bull_change_pct = sum(avg_bull_change) / len(avg_bull_change) if avg_bull_change else 0
    return f"Market is bearish with {percentage:.2f}% of stocks losing and an average loss of {avg_bear_change_pct:.2f}%. Stocks gaining on average {avg_bull_change_pct:.2f}%."
  else:
    return "Market mood is neutral with equal gainers and losers."

"""
Fetches the latest news for the Nifty 50 index.

Uses yfinance to retrieve news articles related to the Nifty 50 index.
Extracts relevant information from the nested news structure including title,
summary, publication date, provider, and clickthrough URL.

Returns:
    list[dict]: A list of dictionaries containing news information with keys:
                - id: Unique identifier for the news item
                - title: News article title
                - summary: Brief summary of the article
                - pub_date: Publication date in ISO format
                - provider: News provider/source name
                - url: Clickthrough URL to the full article
"""
def fetch_news() -> list[dict]:
  ticker = yf.Ticker("^NSEI")
  news = ticker.news
  news_list = []
  
  for item in news:
    try:
      content = item.get('content', {})
      news_item = {
        "id": content.get('id'),
        "title": content.get('title'),
        "summary": content.get('summary'),
        "pub_date": content.get('pubDate'),
        "provider": content.get('provider', {}).get('displayName'),
        "url": content.get('clickThroughUrl', {}).get('url')
      }
      news_list.append(news_item)
    except Exception as e:
      print(f"Error processing news item: {e}")
      continue
  
  return news_list