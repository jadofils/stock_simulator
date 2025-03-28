from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # Include accounts app URLs
    path('api/v1/auth/', include('accounts.urls')),  # API endpoints for accounts
    path('api/v1/', include('dashboard.urls')),  # Include dashboard app URLs
    path('api/v1/trading/', include('trading.urls')),  # Include trading app URLs

    path('api/', include('controller.urls')),  # Make sure this line is present to include your app's URLs

]
