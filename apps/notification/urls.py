from django.urls import path
from . import views

app_name = "notification"

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('<str:notification_id>/read/', views.mark_as_read, name='mark_read'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
]