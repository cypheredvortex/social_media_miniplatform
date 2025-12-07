# apps/user/urls.py
from django.urls import path
from . import views
from django.urls import register_converter
from bson import ObjectId

class ObjectIdConverter:
    regex = '[0-9a-f]{24}'
    
    def to_python(self, value):
        return ObjectId(value)
    
    def to_url(self, value):
        return str(value)

register_converter(ObjectIdConverter, 'objectid')

app_name = "user"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    # Admin URLs - Use objectid converter
    path('admin/', views.admin_user_list, name='admin_user_list'),
    path('admin/<objectid:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('admin/<objectid:user_id>/activate/', views.admin_user_activate, name='admin_user_activate'),
    path('admin/<objectid:user_id>/suspend/', views.admin_user_suspend, name='admin_user_suspend'),
    path('admin/<objectid:user_id>/ban/', views.admin_user_ban, name='admin_user_ban'),
    path('admin/<objectid:user_id>/edit-role/', views.admin_user_edit_role, name='admin_user_edit_role'),
    path('admin/<objectid:user_id>/activity/', views.admin_user_activity, name='admin_user_activity'),
]