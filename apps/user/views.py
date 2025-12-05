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

# Admin views for user management
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import User
from apps.enums.models import UserStatus, UserRole

# List all users
def admin_user_list(request):
    users = User.objects.all().order_by('-created_at')
    return render(request, 'admin/admin_user_list.html', {'users': users})

# View user details
def admin_user_detail(request, user_id):
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return get_object_or_404(User, id=user_id)
    user = get_object_or_404(User, id=user_id)
    return render(request, 'admin/admin_user_detail.html', {'user': user})

def _redirect_back(request):
    """
    Determines whether to redirect to admin panel or user list
    depending on where the admin came from.
    """
    ref = request.META.get("HTTP_REFERER", "")

    if "admin_panel" in ref:
        return redirect("pages:admin_panel")

    # Default fallback
    return redirect("user:admin_user_list")


# Reactivate a suspended or banned user
def admin_user_activate(request, user_id):
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        pass

    user = get_object_or_404(User, id=user_id)

    # Set status back to ACTIVE
    user.status = UserStatus.ACTIVE
    user.save()

    messages.success(request, f'User {user.username} has been reactivated.')
    return _redirect_back(request)

# Suspend a user
def admin_user_suspend(request, user_id):
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        pass
    user = get_object_or_404(User, id=user_id)
    user.status = UserStatus.SUSPENDED
    user.save()
    messages.success(request, f'User {user.username} has been suspended.')
    return _redirect_back(request)


# Ban a user
def admin_user_ban(request, user_id):
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        pass
    user = get_object_or_404(User, id=user_id)
    user.status = UserStatus.BANNED
    user.save()
    messages.success(request, f'User {user.username} has been banned.')
    return _redirect_back(request)


# Edit user role
def admin_user_edit_role(request, user_id):
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        pass
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in [choice[0] for choice in UserRole.choices]:
            user.role = new_role
            user.save()
            messages.success(request, f'Role of {user.username} updated to {new_role}.')
            return redirect('user:admin_user_list')
        else:
            messages.error(request, 'Invalid role selected.')
    return render(request, 'admin/admin_user_edit_role.html', {'user': user, 'roles': UserRole.choices})


# View user activity (example: last login and status)
def admin_user_activity(request, user_id):
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        pass
    user = get_object_or_404(User, id=user_id)
    # You can expand this to include posts, comments, reports, etc.
    activity = {
        'last_login': user.last_login,
        'status': user.status,
        'role': user.role,
        'created_at': user.created_at,
    }
    return render(request, 'admin/user_activity.html', {'user': user, 'activity': activity})
