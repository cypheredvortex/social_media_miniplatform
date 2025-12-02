from django.urls import path
from apps.pages.views import signup, login, home

app_name = "user"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("", home, name="home_page"),
]
