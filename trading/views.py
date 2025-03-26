import yfinance as yf
from django.http import JsonResponse # type: ignore

# View to retrieve World Indices data
def get_world_indices(request):
    indices_symbols = {
        "S&P 500": "^GSPC",
        "Dow 30": "^DJI",
        "Nasdaq": "^IXIC",
        "Russell 2000": "^RUT",
        "FTSE 100": "^FTSE",
        "CAC 40": "^FCHI",
        "DAX": "^GDAXI",
        "Nikkei 225": "^N225",
        "Hang Seng": "^HSI",
        "S&P/ASX 200": "^AXJO",
    }
    data = {}
    for name, symbol in indices_symbols.items():
        stock = yf.Ticker(symbol)
        info = stock.history(period="1d")
        data[name] = {
            "value": round(info["Close"].iloc[-1], 2),
            "change": round(info["Close"].iloc[-1] - info["Open"].iloc[-1], 2),
            "change_percent": round(((info["Close"].iloc[-1] - info["Open"].iloc[-1]) / info["Open"].iloc[-1]) * 100, 2),
        }
    return JsonResponse(data)

# View to retrieve Commodities data
def get_commodities(request):
    commodities_symbols = {
        "Crude Oil": "CL=F",
        "Gold": "GC=F",
        "Silver": "SI=F",
    }
    data = {}
    for name, symbol in commodities_symbols.items():
        stock = yf.Ticker(symbol)
        info = stock.history(period="1d")
        data[name] = {
            "value": round(info["Close"].iloc[-1], 2),
            "change": round(info["Close"].iloc[-1] - info["Open"].iloc[-1], 2),
            "change_percent": round(((info["Close"].iloc[-1] - info["Open"].iloc[-1]) / info["Open"].iloc[-1]) * 100, 2),
        }
    return JsonResponse(data)

# View to retrieve Currencies data
def get_currencies(request):
    currencies_symbols = {
        "EUR/USD": "EURUSD=X",
        "USD/JPY": "JPY=X",
        "USD/GBP": "GBPUSD=X",
    }
    data = {}
    for name, symbol in currencies_symbols.items():
        stock = yf.Ticker(symbol)
        info = stock.history(period="1d")
        data[name] = {
            "value": round(info["Close"].iloc[-1], 6),
            "change": round(info["Close"].iloc[-1] - info["Open"].iloc[-1], 6),
            "change_percent": round(((info["Close"].iloc[-1] - info["Open"].iloc[-1]) / info["Open"].iloc[-1]) * 100, 2),
        }
    return JsonResponse(data)

# View to retrieve Cryptocurrencies data
def get_cryptocurrencies(request):
    crypto_symbols = {
        "BTC-USD": "BTC-USD",
        "ETH-USD": "ETH-USD",
        "XRP-USD": "XRP-USD",
    }
    data = {}
    for name, symbol in crypto_symbols.items():
        stock = yf.Ticker(symbol)
        info = stock.history(period="1d")
        data[name] = {
            "value": round(info["Close"].iloc[-1], 2),
            "change": round(info["Close"].iloc[-1] - info["Open"].iloc[-1], 2),
            "change_percent": round(((info["Close"].iloc[-1] - info["Open"].iloc[-1]) / info["Open"].iloc[-1]) * 100, 2),
        }
    return JsonResponse(data)
