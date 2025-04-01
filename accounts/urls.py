from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login-page', views.login, name='login-page'),  # Login page
    path('signup', views.signup, name='signup'),  # Sign Up page
    path('forgot_password', views.forgot_password, name='forgot_password'),  # Forgot Password page
]
