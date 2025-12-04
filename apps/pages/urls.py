from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("", views.home, name="home_page"),
    path("admin/", views.admin_panel, name="admin_panel"),
    # path("content/", views.admin_content_list, name="content"),
    # path("post/", views.admin_post_list, name="post"),
    # path("comment/", views.admin_comment_list, name="comment"),
    # path("profile/", views.admin_profile_list, name="profile"),
    # path("report/", views.admin_report_list, name="report"),
    # path("admin/users/", views.admin_user_list, name="user_list"),
    # path("user/", views.user, name="user"),
]
