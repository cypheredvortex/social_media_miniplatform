from django.urls import path
from . import views

urlpatterns = [
    path('admin/reports/', views.admin_report_list, name='admin_report_list'),
    path('admin/reports/<str:report_id>/', views.admin_report_detail, name='admin_report_detail'),
    path('admin/reports/<str:report_id>/resolve/', views.admin_report_resolve, name='admin_report_resolve'),
    path('admin/reports/<str:report_id>/reject/', views.admin_report_reject, name='admin_report_reject'),
    path('admin/users/<str:user_id>/warn/', views.admin_send_warning, name='admin_send_warning'),
]
