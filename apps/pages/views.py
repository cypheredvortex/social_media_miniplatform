from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def login(request):
    return render(request, 'auth/login.html')

def signup(request):
    return render(request, 'auth/signup.html')

def admin_panel(request):
    return render(request, 'admin/admin_panel.html')

def user(request):
    return render(request, 'regularUser/user.html')