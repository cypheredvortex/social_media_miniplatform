from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.user.models import User
from apps.report.models import Report
from apps.content.models import Content
from apps.enums.models import UserRole

def home(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'role') and request.user.role == UserRole.ADMIN:
            return redirect('pages:admin_panel')
        
        # Get posts for regular users
        posts = Content.objects.filter(
            content_type='POST',
            status='ACTIVE'
        ).select_related('author').order_by('-created_at')[:20]
        
        return render(request, 'main/home.html', {'posts': posts})
    
    return render(request, 'main/home.html')

def login(request):
    return redirect('user:login')  # Redirect to our login view

def signup(request):
    return redirect('user:signup')  # Redirect to our signup view

@login_required
def admin_panel(request):
    if not hasattr(request.user, 'role') or request.user.role != UserRole.ADMIN:
        return redirect('pages:home_page')
    
    users_count = User.objects.count()
    reports_count = Report.objects.count()
    content_count = Content.objects.count()
    users = User.objects.all().order_by('-created_at')[:10]
    
    context = {
        'users_count': users_count,
        'reports_count': reports_count,
        'content_count': content_count,
        'users': users,
    }
    return render(request, 'admin/admin_panel.html', context)

@login_required
def user_dashboard(request):
    return render(request, 'regularUser/user.html')