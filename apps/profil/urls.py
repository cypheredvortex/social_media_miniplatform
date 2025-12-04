from django.urls import path
from . import views


app_name="profil"

urlpatterns = [
    path('', views.admin_profile_list, name='admin_profile_list'),
    path('<str:profile_id>/', views.admin_profile_detail, name='admin_profile_detail'),
    path('<str:profile_id>/edit/', views.admin_profile_edit, name='admin_profile_edit'),
]
