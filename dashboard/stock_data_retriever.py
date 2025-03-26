# yfinance/stock_data_retriever.py
import yfinance as yf # type: ignore
import pandas as pd # type: ignore

class StockDataRetriever:
    def __init__(self, tickers=None):
        if tickers is None:
            self.tickers = [
                'NVDA', 'TSLA', 'AAPL', 'MSFT', 'GOOGL',
                'AMZN', 'META', 'NFLX', 'INTC', 'AMD'
            ]
        else:
            self.tickers = tickers

    def get_live_stock_data(self):
        """
        Retrieve real-time stock data from Yahoo Finance
        """
        stock_data = []

        for ticker in self.tickers:
            try:
                # Fetch stock information
                stock = yf.Ticker(ticker)
                
                # Get current stock quote
                quote = stock.history(period='1d')
                
                if not quote.empty:
                    # Get most recent quote
                    current_quote = quote.iloc[-1]
                    
                    # Additional stock info
                    info = stock.info
                    
                    stock_info = {
                        'symbol': ticker,
                        'name': info.get('longName', ticker),
                        'current_price': current_quote['Close'],
                        'previous_close': current_quote['Close'],
                        'change': current_quote['Close'] - quote.iloc[0]['Open'],
                        'change_percent': ((current_quote['Close'] - quote.iloc[0]['Open']) / quote.iloc[0]['Open']) * 100,
                        'volume': current_quote['Volume'],
                        'market_cap': info.get('marketCap', 0),
                        '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                        '52_week_low': info.get('fiftyTwoWeekLow', 0)
                    }
                    
                    stock_data.append(stock_info)
                
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
        
        return stock_data

    def create_stock_dataframe(self):
        """
        Create a pandas DataFrame with stock data
        """
        stock_data = self.get_live_stock_data()
        return pd.DataFrame(stock_data)
