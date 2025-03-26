# stock_simulator/urls.py

from django.contrib import admin
from django.urls import path, include  # include is used to add app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # Include accounts URLs
]
