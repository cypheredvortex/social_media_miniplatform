from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_post_list, name='admin_post_list'),
    path('<str:post_id>/', views.admin_post_detail, name='admin_post_detail'),
    path('<str:post_id>/delete/', views.admin_post_delete, name='admin_post_delete'),
]
