from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.user_profile_list, name='user_profile_list'),
    path('profiles/<int:id>/', views.user_profile_detail, name='user_profile_detail'),
    path('profiles/create/<int:user_id>/', views.user_profile_create, name='user_profile_create'), # Modified route
    path('profiles/update/<int:id>/', views.user_profile_update, name='user_profile_update'),
    path('profiles/delete/<int:id>/', views.user_profile_delete, name='user_profile_delete'),
]