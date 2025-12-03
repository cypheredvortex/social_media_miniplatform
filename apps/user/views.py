from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.user.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.db.models import Q
from apps.enums.models import UserRole

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip().lower()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validation
        if password != confirm_password:
            print(f"[debug] signup failed: passwords do not match for username={username}")
            messages.error(request, "Passwords do not match.")
            return render(request, "auth/signUp.html")
        
        if User.objects.filter(username=username).exists():
            print(f"[debug] signup failed: username exists: {username}")
            messages.error(request, "Username already exists.")
            return render(request, "auth/signUp.html")

        if User.objects.filter(email=email).exists():
            print(f"[debug] signup failed: email exists: {email}")
            messages.error(request, "Email already registered.")
            return render(request, "auth/signUp.html")

        # Create user
        hashed_password = make_password(password)
        user = User.objects.create(
            username=username,
            email=email,
            password_hash=hashed_password
        )
        print(f"[debug] signup succeeded: id={getattr(user, 'id', None)}, username={user.username}")
        messages.success(request, "Account created successfully! Please login.")
        return redirect("pages:login")

    # Render the signup template (the project stores auth templates under `templates/auth/`)
    return render(request, "auth/signUp.html")


def login_view(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username_or_email", "").strip()
        password = request.POST.get("password", "")

        # Validate inputs
        if not username_or_email or not password:
            messages.error(request, "Please enter both username/email and password.")
            return render(request, "user/login.html")

        # Try to fetch the user by username or email
        try:
            user = User.objects.get(
                Q(username=username_or_email) | Q(email=username_or_email)
            )
            # Debug: indicate user lookup succeeded (no sensitive data)
            print(f"[debug] user lookup succeeded: id={getattr(user, 'id', None)}")
        except User.DoesNotExist:
            # Debug: indicate lookup failed
            print(f"[debug] user lookup failed for: {username_or_email}")
            messages.error(request, "Invalid credentials.")
            return render(request, "auth/login.html")

        # Check password
        password_ok = check_password(password, user.password_hash)
        # Debug: show whether password matched (True/False)
        print(f"[debug] password check for user id={getattr(user, 'id', None)}: {password_ok}")
        if not password_ok:
            messages.error(request, "Invalid credentials.")
            return render(request, "auth/login.html")

        # Check account status
        if user.status != "ACTIVE":
            messages.error(request, f"Your account is {user.status}.")
            return render(request, "auth/login.html")

        # Login: store user ID in session
        request.session["user_id"] = user.id
        user.last_login = timezone.now()
        user.save()

        messages.success(request, f"Welcome back, {user.username}!")
        # Redirect based on user role
        try:
            if user.role == UserRole.ADMIN:
                return redirect("pages:admin_panel")
        except Exception:
            # If enums aren't available or value mismatches, fall back to admin check by string
            if getattr(user, 'role', '') == 'ADMIN':
                return redirect("pages:admin_panel")

        # Default: regular user page
        return redirect("pages:user")

    # GET request
    return render(request, "auth/login.html")


def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect("user:login")
