from django.urls import path
from .views import portfolio_list, portfolio_detail, portfolio_create, portfolio_update, portfolio_delete

urlpatterns = [
    path('user/portfolios/', portfolio_list, name='portfolio_list'),
    path('user/portfolios/<int:id>/', portfolio_detail, name='portfolio_detail'),
    path('user/portfolios/create/', portfolio_create, name='portfolio_create'),
    path('user/portfolios/update/<int:id>/', portfolio_update, name='portfolio_update'),
    path('user/portfolios/delete/<int:id>/', portfolio_delete, name='portfolio_delete'),
]
