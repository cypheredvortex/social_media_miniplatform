from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("", views.home, name="home_page"),
    path("admin/", views.admin_panel, name="admin_panel"),
]
