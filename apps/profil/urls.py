from django.urls import path, register_converter
from . import views
from bson import ObjectId

class ObjectIdConverter:
    regex = '[0-9a-f]{24}'
    
    def to_python(self, value):
        return ObjectId(value)
    
    def to_url(self, value):
        return str(value)

register_converter(ObjectIdConverter, 'objectid')

app_name="profil"

urlpatterns = [
    # Admin URLs
    path('admin/', views.admin_profile_list, name='admin_profile_list'),
    path('admin/<objectid:profile_id>/', views.admin_profile_detail, name='admin_profile_detail'),
    path('admin/<objectid:profile_id>/edit/', views.admin_profile_edit, name='admin_profile_edit'),
    
    # Regular user URLs
    path('', views.my_profile, name='my_profile'),
    path('edit/', views.edit_profile, name='edit'),
    path('user/<objectid:user_id>/', views.view_profile, name='view'),
]