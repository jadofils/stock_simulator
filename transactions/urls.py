from django.urls import path
from .views import transaction_list, transaction_detail, transaction_create, transaction_delete

urlpatterns = [
    path('user/transactions/', transaction_list, name='transaction_list'),
    path('user/transactions/<int:id>/', transaction_detail, name='transaction_detail'),
    path('user/transactions/create/', transaction_create, name='transaction_create'),
    # path('user/transactions/update/<int:id>/', transaction_update, name='transaction_update'),
    path('user/transactions/delete/<int:id>/', transaction_delete, name='transaction_delete'),
]


