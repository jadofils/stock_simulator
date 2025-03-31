from django.urls import path
from . import views

urlpatterns = [
    path('stocks/', views.get_all_stocks, name='get_all_stocks'),
    path('stocks/create/', views.create_stock, name='create_stock'),
    path('stocks/<int:stock_id>/', views.get_stock, name='get_stock'),
    path('stocks/<int:stock_id>/update/', views.update_stock, name='update_stock'),
    path('stocks/<int:stock_id>/delete/', views.delete_stock, name='delete_stock'),
]