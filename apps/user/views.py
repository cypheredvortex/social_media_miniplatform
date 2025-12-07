from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.db.models import Q
from bson import ObjectId
from django.http import Http404

from apps.user.models import User
from apps.enums.models import UserRole, UserStatus

# ---------------------------
# Authentication Views
# ---------------------------

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "auth/signUp.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "auth/signUp.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "auth/signUp.html")

        # Create user - ObjectId will be generated automatically
        user = User(
            username=username,
            email=email,
            password_hash=make_password(password),
            role=UserRole.REGULAR,
            status=UserStatus.ACTIVE
        )
        user.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect("user:login")

    return render(request, "auth/signUp.html")

def login_view(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username_or_email", "").strip()
        password = request.POST.get("password", "")

        if not username_or_email or not password:
            messages.error(request, "Please enter both username/email and password.")
            return render(request, "auth/login.html")

        try:
            user = User.objects.get(
                Q(username=username_or_email) | Q(email=username_or_email)
            )
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials.")
            return render(request, "auth/login.html")

        if not check_password(password, user.password_hash):
            messages.error(request, "Invalid credentials.")
            return render(request, "auth/login.html")

        if user.status != UserStatus.ACTIVE:
            messages.error(request, f"Your account is {user.status}.")
            return render(request, "auth/login.html")

        # Set session with string representation of ObjectId
        request.session["user_id"] = str(user.id)
        request.session["username"] = user.username
        request.session["role"] = user.role
        
        # Update last login - don't use update_fields, just save
        user.last_login = timezone.now()
        user.save()  # Changed from user.save(update_fields=['last_login'])

        if user.role == UserRole.ADMIN:
            return redirect("pages:admin_panel")

        return redirect("pages:home_page")

    return render(request, "auth/login.html")

def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect("user:login")


# ---------------------------
# Admin User Management Views
# ---------------------------

def admin_user_list(request):
    # Check if user is admin
    if not hasattr(request.user, 'role') or request.user.role != UserRole.ADMIN:
        messages.error(request, "Access denied. Admin only.")
        return redirect("pages:home_page")
    
    users = User.objects.all().order_by('-created_at')
    return render(request, 'admin/admin_user_list.html', {'users': users})


def admin_user_detail(request, user_id):
    # Check if user is admin
    if not hasattr(request.user, 'role') or request.user.role != UserRole.ADMIN:
        messages.error(request, "Access denied. Admin only.")
        return redirect("pages:home_page")
    
    try:
        user = User.objects.get(id=user_id)
    except (User.DoesNotExist, Exception):
        raise Http404("User not found")
    
    return render(request, 'admin/admin_user_detail.html', {'user': user})


def _redirect_back(request):
    next_url = request.GET.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("user:admin_user_list")


def admin_user_activate(request, user_id):
    # Check if user is admin
    if not hasattr(request.user, 'role') or request.user.role != UserRole.ADMIN:
        messages.error(request, "Access denied. Admin only.")
        return redirect("pages:home_page")
    
    user = get_object_or_404(User, id=user_id)
    user.status = UserStatus.ACTIVE
    user.save()
    messages.success(request, f'User {user.username} has been reactivated.')
    return _redirect_back(request)


def admin_user_suspend(request, user_id):
    # Check if user is admin
    if not hasattr(request.user, 'role') or request.user.role != UserRole.ADMIN:
        messages.error(request, "Access denied. Admin only.")
        return redirect("pages:home_page")
    
    user = get_object_or_404(User, id=user_id)
    user.status = UserStatus.SUSPENDED
    user.save()
    messages.success(request, f'User {user.username} has been suspended.')
    return _redirect_back(request)


def admin_user_ban(request, user_id):
    # Check if user is admin
    if not hasattr(request.user, 'role') or request.user.role != UserRole.ADMIN:
        messages.error(request, "Access denied. Admin only.")
        return redirect("pages:home_page")
    
    user = get_object_or_404(User, id=user_id)
    user.status = UserStatus.BANNED
    user.save()
    messages.success(request, f'User {user.username} has been banned.')
    return _redirect_back(request)


def admin_user_edit_role(request, user_id):
    # Check if user is admin
    if not hasattr(request.user, 'role') or request.user.role != UserRole.ADMIN:
        messages.error(request, "Access denied. Admin only.")
        return redirect("pages:home_page")
    
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


def admin_user_activity(request, user_id):
    # Check if user is admin
    if not hasattr(request.user, 'role') or request.user.role != UserRole.ADMIN:
        messages.error(request, "Access denied. Admin only.")
        return redirect("pages:home_page")
    
    user = get_object_or_404(User, id=user_id)
    activity = {
        'last_login': user.last_login,
        'status': user.status,
        'role': user.role,
        'created_at': user.created_at,
    }
    return render(request, 'admin/user_activity.html', {'user': user, 'activity': activity})