from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('stocks', views.stocks, name='stocks'),
    path('transactions', views.transactions, name='transactions'),
    path('history', views.history, name='history'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('settings', views.settings, name='settings'),
    path('markets', views.markets, name='markets'),

    #route for yahoo finance data api
    path('yfinance/investments', views.get_investments, name='get_investments'),\
    

    #route to render the investment template
    path('investments', views.investments, name='investment'),
  
]