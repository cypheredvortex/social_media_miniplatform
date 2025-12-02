from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.user.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip().lower()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("user:signup")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("user:signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("user:signup")

        # Create user
        hashed_password = make_password(password)
        user = User.objects.create(
            username=username,
            email=email,
            password_hash=hashed_password
        )
        messages.success(request, "Account created successfully! Please login.")
        return redirect("user:login")

    return render(request, "user/signup.html")


def login_view(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username_or_email").strip()
        password = request.POST.get("password")

        try:
            user = User.objects.get(
                models.Q(username=username_or_email) | models.Q(email=username_or_email)
            )
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials.")
            return redirect("user:login")

        if not check_password(password, user.password_hash):
            messages.error(request, "Invalid credentials.")
            return redirect("user:login")

        if user.status != "ACTIVE":
            messages.error(request, f"Your account is {user.status}.")
            return redirect("user:login")

        # Set session manually (since you're not using Django auth user)
        request.session["user_id"] = str(user.id)
        user.last_login = timezone.now()
        user.save()
        messages.success(request, f"Welcome back, {user.username}!")
        return redirect("home")  # redirect to your main dashboard/home page

    return render(request, "user/login.html")


def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect("user:login")
