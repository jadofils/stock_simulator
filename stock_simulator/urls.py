from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # Include accounts app URLs
    path('api/v1/', include('accounts.urls')),  # API endpoints for accounts
]
