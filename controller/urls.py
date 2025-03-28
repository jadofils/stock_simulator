# your_app/urls.py
from django.urls import path
from . import views  # This imports the views from the current directory
urlpatterns = [
    path('user/login/',views.login, name='login'),

    path('user/create/', views.create_user, name='create_user'),
    path('user/<int:user_id>/', views.get_user, name='get_user'),  # Ensure this is correctly imported
    path('user/<int:user_id>/update/', views.update_user, name='update_user'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('user/search/', views.search_users, name='search_users'),  # Ensure this is correctly imported
    path('user/sort/<str:sort_by>/<str:order>/', views.sort_users, name='sort_users'),
    path('users/', views.get_all_users, name='get_all_users'),

]
