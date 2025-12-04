from django.urls import path
from . import views

app_name="report"

urlpatterns = [
    path('', views.admin_report_list, name='admin_report_list'),
    path('<str:report_id>/', views.admin_report_detail, name='admin_report_detail'),
    path('<str:report_id>/resolve/', views.admin_report_resolve, name='admin_report_resolve'),
    path('<str:report_id>/reject/', views.admin_report_reject, name='admin_report_reject'),
    path('<str:user_id>/warn/', views.admin_send_warning, name='admin_send_warning'),
]
