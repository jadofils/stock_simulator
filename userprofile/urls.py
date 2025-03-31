from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.user_profile_list, name='user_profile_list'),
    path('profile/<int:id>/', views.user_profile_detail, name='user_profile_detail'),
    path('profile/create/<int:user_id>/', views.user_profile_create, name='user_profile_create'), # Modified route
   path('profile/update/<int:id>/user/<int:user_id>/', views.user_profile_update, name='user_profile_update'),
    path('profile/delete/<int:id>/user/<int:user_id>/', views.user_profile_delete, name='user_profile_delete'),
]