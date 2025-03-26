from django.shortcuts import render
#home page
def home(request):
    return render(request, 'accounts/home.html')
# Login view
def login(request):
    return render(request, 'accounts/login.html')

# Signup view
def signup(request):
    return render(request, 'accounts/signup.html')  # Render Sign Up page

# Forgot Password view
def forgot_password(request):
    return render(request, 'accounts/forgot_password.html')  # Render Forgot Password page
