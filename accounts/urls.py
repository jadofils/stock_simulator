from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login', views.login, name='login'),  # Login page
    path('signup', views.signup, name='signup'),  # Sign Up page
    path('forgot_password', views.forgot_password, name='forgot_password'),  # Forgot Password page
]
