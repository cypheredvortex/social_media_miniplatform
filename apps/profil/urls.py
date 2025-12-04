from django.urls import path
from . import views


app_name="profil"

urlpatterns = [
    path('admin/profiles/<str:profile_id>/', views.admin_profile_detail, name='admin_profile_detail'),
    path('admin/profiles/<str:profile_id>/edit/', views.admin_profile_edit, name='admin_profile_edit'),
]
