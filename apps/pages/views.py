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

# def admin_comment_list(request):
#     return render(request, 'admin/admin_comment_list.html')

# def admin_content_list(request):
#     return render(request, 'admin/admin_content_list.html')   

# def admin_post_list(request):
#     return render(request, 'admin/admin_post_list.html')

# def admin_profile_list(request):
#     return render(request, 'admin/admin_profile_list.html')

# def admin_report_list(request):
#     return render(request, 'admin/admin_report_list.html')

# def admin_user_list(request):
#     return render(request, 'admin/admin_user_list.html')

def user(request):
    return render(request, 'regularUser/user.html')

