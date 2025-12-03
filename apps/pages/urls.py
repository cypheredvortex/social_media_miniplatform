from django.urls import path
from apps.pages.views import signup, login, home, admin_panel, user

app_name = "pages"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("", home, name="home_page"),
    path("admin/", admin_panel, name="admin_panel"),
    path("user/", user, name="user"),
]
