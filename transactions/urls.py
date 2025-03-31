from django.urls import path
from .views import transaction_list, transaction_detail, transaction_create, transaction_update, transaction_delete

urlpatterns = [
    path('transactions/', transaction_list, name='transaction_list'),
    path('transactions/<int:id>/', transaction_detail, name='transaction_detail'),
    path('transactions/create/', transaction_create, name='transaction_create'),
    path('transactions/update/<int:id>/', transaction_update, name='transaction_update'),
    path('transactions/delete/<int:id>/', transaction_delete, name='transaction_delete'),
]


