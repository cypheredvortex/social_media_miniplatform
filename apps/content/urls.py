from django.urls import path
from . import views

app_name = "content"

urlpatterns = [
    path('', views.admin_content_list, name='admin_content_list'),
    path('<str:content_id>/', views.admin_content_detail, name='admin_content_detail'),
    path('<str:content_id>/edit/', views.admin_content_edit, name='admin_content_edit'),
    path('<str:content_id>/delete/', views.admin_content_delete, name='admin_content_delete'),
    path('<str:content_id>/approve/', views.admin_content_approve, name='admin_content_approve'),
    path('<str:content_id>/reject/', views.admin_content_reject, name='admin_content_reject'),
]
