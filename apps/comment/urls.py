from django.urls import path
from . import views

app_name = "comment"

urlpatterns = [
    path('', views.admin_comment_list, name='admin_comment_list'),
    path('<str:comment_id>/', views.admin_comment_detail, name='admin_comment_detail'),
    path('<str:comment_id>/delete/', views.admin_comment_delete, name='admin_comment_delete'),
]
