import yfinance as yf

def fetch_stock_data(tickers):
    stock_data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5y")
        info = stock.info
        stock_data[ticker] = {
            'history': hist,
            'pe_ratio': info.get('forwardPE'),
            'dividend_yield': info.get('dividendYield'),
            'market_cap': info.get('marketCap')
        }
    return stock_data

if __name__ == "__main__":
    tickers = ['AAPL', 'GOOGL', 'MSFT']
    stock_data = fetch_stock_data(tickers)
    print(stock_data)
