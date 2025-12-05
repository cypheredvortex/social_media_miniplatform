from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('', views.admin_user_list, name='admin_user_list'),
    path('<str:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('admin/users/<int:user_id>/activate/', views.admin_user_activate, name='admin_user_activate'),
    path('<str:user_id>/suspend/', views.admin_user_suspend, name='admin_user_suspend'),
    path('<str:user_id>/ban/', views.admin_user_ban, name='admin_user_ban'),
    path('<str:user_id>/edit-role/', views.admin_user_edit_role, name='admin_user_edit_role'),
    path('<str:user_id>/activity/', views.admin_user_activity, name='admin_user_activity'),
]
