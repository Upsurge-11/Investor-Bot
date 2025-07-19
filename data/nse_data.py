"""
nse_data.py
This module provides utility functions to fetch and analyze stock data for the Nifty 50 index using the yfinance library.
It includes functions to retrieve the list of Nifty 50 stock symbols, fetch stock data for individual symbols, identify top gainers or losers, analyze the overall market sentiment based on daily price changes and fetch the latest news related to the Nifty 50 index.
Functions:
  fetch_nifty50_symbols() -> list[str]:
    Returns a hardcoded list of all 50 Nifty 50 stock symbols with the '.NS' suffix for NSE.
  fetch_stock_data(symbol: str, full: bool = False) -> dict:
    Fetches stock data for a given symbol using yfinance. Returns either fast info (basic metrics) or full info (comprehensive data).
  fetch_gainers_or_losers(fetch_gainers: bool = True, full_list: bool = False) -> list[dict]:
    Analyzes all Nifty 50 stocks to calculate daily percentage change and returns either top gainers or losers, or the complete sorted list.
  fetch_market_mood() -> str:
    Analyzes the overall market sentiment based on Nifty 50 stock performance, indicating if the market is bullish, bearish, or neutral.
  fetch_news() -> list[dict]:
    Fetches the latest news for the Nifty 50 index, returning a list of news items with titles, links, and publication dates.
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

"""Fetches the latest news for the Nifty 50 index.

Uses yfinance to retrieve news articles related to the Nifty 50 index.
Returns a list of news items containing titles, links, and publication dates.

Returns:
    list[dict]: A list of dictionaries containing news titles, links, and publication dates
"""
def fetch_news():
  ticker = yf.Ticker("^NSEI")  # Nifty 50 index
  news = ticker.news
  return news