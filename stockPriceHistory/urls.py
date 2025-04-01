from django.urls import path
from .views import stock_price_list, stock_price_detail, stock_price_create, stock_price_update, stock_price_delete

urlpatterns = [
    path('user/stock_prices/', stock_price_list, name='stock_price_list'),
    path('user/stock_prices/<int:id>/', stock_price_detail, name='stock_price_detail'),
    path('user/stock_prices/create/', stock_price_create, name='stock_price_create'),
    path('user/stock_prices/update/<int:id>/', stock_price_update, name='stock_price_update'),
    path('user/stock_prices/delete/<int:id>/', stock_price_delete, name='stock_price_delete'),
]
