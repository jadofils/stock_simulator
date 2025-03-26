from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('world-indices', views.get_world_indices, name='world_indices'),
    path('commodities', views.get_commodities, name='commodities'),
    path('currencies', views.get_currencies, name='currencies'),
    path('cryptocurrencies', views.get_cryptocurrencies, name='cryptocurrencies'),
]
