from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def login(request):
    return render(request, 'auth/login.html')

def signup(request):
    return render(request, 'auth/signup.html')

def admin_panel(request):
    from apps.user.models import User
    from apps.post.models import Post
    from apps.comment.models import Comment
    from apps.report.models import Report
    
    users_count = User.objects.count()
    posts_count = Post.objects.count()
    comments_count = Comment.objects.count()
    reports_count = Report.objects.count()
    users = User.objects.all().order_by('-created_at')[:10]
    
    context = {
        'users_count': users_count,
        'posts_count': posts_count,
        'comments_count': comments_count,
        'reports_count': reports_count,
        'users': users,
    }
    return render(request, 'admin/admin_panel.html', context)

def user(request):
    return render(request, 'regularUser/user.html')

