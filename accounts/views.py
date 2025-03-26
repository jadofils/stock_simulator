from django.shortcuts import render

# Login view
def login(request):
    return render(request, 'accounts/login.html')

# Signup view
def signup(request):  # Corrected from 'sinup' to 'signup'
    return render(request, 'accounts/signup.html')
