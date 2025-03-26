from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .stock_data_retriever import StockDataRetriever # type: ignore

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def portfolio(request):
    return render(request, 'dashboard/portfolio.html')

def stocks(request):
    return render(request, 'dashboard/stocks.html')

def transactions(request):
    return render(request, 'dashboard/transactions.html')

def history(request):
    return render(request, 'dashboard/history.html')
def watchlist(request):
    return render(request, 'dashboard/watchlist.html')

def markets(request):
    return render(request, 'dashboard/markets.html')

def settings(request):
    return render(request, 'dashboard/settings.html')
def investments(request):
    return render(request, 'dashboard/investments.html')

@csrf_exempt
def get_investments(request):
    """
    View to return live stock data
    """
    retriever = StockDataRetriever()
    stock_df = retriever.create_stock_dataframe()
    
    # Convert the DataFrame to a dictionary and return as JSON response
    stock_data = stock_df.to_dict(orient='records')
    
    return JsonResponse(stock_data, safe=False)