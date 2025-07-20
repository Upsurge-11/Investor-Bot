# � Nifty 50 Investment Strategy Bot

A comprehensive Python-based investment bot that implements multiple trading strategies for Nifty 50 stocks using real-time market data and technical analysis.

## 📊 Available Strategies

### 1. **Momentum Strategies**

- **Top Gainers Strategy**: Identifies and recommends stocks with strong upward momentum
- **Moving Average Crossover**: Golden cross (20MA crossing above 50MA) signals
- **Breakout Strategy**: Stocks breaking through resistance levels

### 2. **Mean Reversion Strategies**

- **RSI Oversold/Overbought**: Buy oversold stocks (RSI < 30), sell overbought (RSI > 70)
- **Support/Resistance Levels**: Buy near support, sell near resistance
- **Bollinger Bands**: Mean reversion around price bands

### 3. **Value-Based Strategies**

- **Low P/E Ratio Strategy**: Identify undervalued stocks with low price-to-earnings ratios
- **High Dividend Yield**: Focus on stocks with attractive dividend yields
- **Book Value Analysis**: Stocks trading below their book value

### 4. **Sentiment-Based Strategies**

- **Market Mood Following**: Align with overall market sentiment (bullish/bearish)
- **Contrarian Strategy**: Go against prevailing market sentiment
- **News-Based Analysis**: React to market news and sentiment

### 5. **Sector Rotation**

- **Sector Leadership**: Focus on best-performing sectors within Nifty 50
- **Diversification**: Equal weight allocation across sectors

## 🛠️ Features

- **Real-time Data**: Uses yfinance for live NSE market data
- **Multiple Timeframes**: Support for different analysis periods (1mo, 3mo, 6mo, 1y)
- **Risk Management**: Confidence scoring and position sizing
- **Backtesting**: Historical performance analysis of strategies
- **Interactive CLI**: User-friendly command-line interface
- **Configurable**: YAML-based configuration for strategy parameters
- **Company Mapping**: Easy-to-use mapping between company names and stock ticker symbols
- **Configurable Analysis**: Customizable analysis parameters through YAML configuration files
- **Investment Strategies**: Built-in strategy modules for systematic investment approaches

## 📁 Project Structure

```
Investor-Bot/
├── cli/                    # Command line interface
│   └── main.py            # Main CLI application (Coming Soon)
├── configs/               # Configuration files
│   └── nifty50_config.yaml # Nifty 50 analysis configuration
├── data/                  # Data handling modules
│   ├── nse_data.py       # Core NSE data fetching functions
│   └── company_mapping.json # Company name to ticker mapping
├── portfolio/             # Portfolio management (Coming Soon)
├── rules/                 # Investment strategy rules
│   └── nifty50_strategy.py # Nifty 50 investment strategies
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Upsurge-11/Investor-Bot.git
   cd Investor-Bot
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv investor-bot-env
   source investor-bot-env/bin/activate  # On Windows: investor-bot-env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📊 Core Functions

### NSE Data Module (`data/nse_data.py`)

#### `fetch_nifty50_symbols()`

Returns a list of all 50 Nifty stock symbols with NSE suffix.

#### `fetch_stock_data(symbol, full=False)`

Fetches comprehensive stock data for a given symbol.

- `symbol`: Stock symbol (e.g., 'RELIANCE.NS')
- `full`: If True, returns detailed info; if False, returns basic metrics

#### `fetch_gainers_or_losers(fetch_gainers=True, full_list=False)`

Analyzes and returns top gaining or losing stocks.

- `fetch_gainers`: True for gainers, False for losers
- `full_list`: True for all stocks, False for top 5

#### `fetch_market_mood()`

Analyzes overall market sentiment and returns descriptive market mood.

#### `fetch_news()`

Fetches latest financial news related to Nifty 50 index.

## 🔧 Configuration

### Nifty 50 Configuration (`configs/nifty50_config.yaml`)

```yaml
# Enable/disable different analysis features
fetchAllStocksInIndex: true
fetchStockDetails:
  enabled: false
  stockSymbol: "RELIANCE"
fetchGainers: false
fetchLosers: false
fetchMarketMood: false
```

## 💼 Usage Examples

### Basic Stock Data Fetching

```python
from data.nse_data import fetch_stock_data, fetch_nifty50_symbols

# Get all Nifty 50 symbols
symbols = fetch_nifty50_symbols()
print(f"Total Nifty 50 stocks: {len(symbols)}")

# Fetch data for a specific stock
reliance_data = fetch_stock_data('RELIANCE.NS')
print(f"Reliance current price: ₹{reliance_data.get('lastPrice')}")
```

### Market Sentiment Analysis

```python
from data.nse_data import fetch_market_mood, fetch_gainers_or_losers

# Get overall market sentiment
mood = fetch_market_mood()
print(f"Market Mood: {mood}")

# Get top 5 gainers
top_gainers = fetch_gainers_or_losers(fetch_gainers=True, full_list=False)
for stock in top_gainers:
    print(f"{stock['symbol']}: +{stock['change_pct']:.2f}%")
```

### Company Name to Ticker Conversion

```python
import json

# Load company mapping
with open('data/company_mapping.json', 'r') as f:
    company_mapping = json.load(f)

# Get ticker for a company
ticker = company_mapping.get('Reliance-Industries')  # Returns 'RELIANCE.NS'
```

### Latest Market News

```python
from data.nse_data import fetch_news

# Get latest financial news
news_items = fetch_news()
for news in news_items[:3]:  # Show first 3 news items
    print(f"📰 {news['title']}")
    print(f"   Source: {news['provider']}")
    print(f"   Date: {news['pub_date']}")
    print()
```

## 🎯 Investment Strategies

The `rules/` directory contains strategy modules for systematic investment approaches:

- **Nifty 50 Strategy** (`nifty50_strategy.py`): Core strategies for Nifty 50 index investing
- **Portfolio Management**: Automated portfolio rebalancing and optimization (Coming Soon)
- **Risk Management**: Stop-loss and profit-taking rules (Coming Soon)

## 📈 Market Data Sources

- **Primary**: Yahoo Finance API via `yfinance` library
- **Coverage**: All Nifty 50 stocks listed on NSE (National Stock Exchange of India)
- **Data Types**: Real-time prices, historical data, company fundamentals, news

## 🔄 Planned Features

- [ ] **CLI Application**: Interactive command-line interface
- [ ] **Portfolio Tracking**: Personal portfolio management and tracking
- [ ] **Automated Trading**: Integration with broker APIs for automated trading
- [ ] **Technical Analysis**: Advanced charting and technical indicators
- [ ] **Alerts & Notifications**: Price alerts and market notifications
- [ ] **Backtesting**: Historical strategy performance testing
- [ ] **Web Dashboard**: Interactive web-based dashboard

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This tool is for educational and research purposes only. It should not be considered as financial advice. Always do your own research and consider consulting with a qualified financial advisor before making investment decisions. The authors are not responsible for any financial losses incurred from using this software.

## 🙋‍♂️ Support

If you have any questions or need help with the project, please open an issue on GitHub or contact the maintainers.

---

**Happy Investing! 📊💰**
