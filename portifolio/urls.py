from django.urls import path
from .views import portfolio_list, portfolio_detail, portfolio_create, portfolio_update, portfolio_delete

urlpatterns = [
    path('portfolios/', portfolio_list, name='portfolio_list'),
    path('portfolios/<int:id>/', portfolio_detail, name='portfolio_detail'),
    path('portfolios/create/', portfolio_create, name='portfolio_create'),
    path('portfolios/update/<int:id>/', portfolio_update, name='portfolio_update'),
    path('portfolios/delete/<int:id>/', portfolio_delete, name='portfolio_delete'),
]
