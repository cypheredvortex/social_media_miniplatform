# apps/report/urls.py
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

app_name="report"

urlpatterns = [
    path('admin/', views.admin_report_list, name='admin_report_list'),
    path('admin/<objectid:report_id>/', views.admin_report_detail, name='admin_report_detail'),
    path('admin/<objectid:report_id>/resolve/', views.admin_report_resolve, name='admin_report_resolve'),
    path('admin/<objectid:report_id>/reject/', views.admin_report_reject, name='admin_report_reject'),
    path('admin/<objectid:user_id>/warn/', views.admin_send_warning, name='admin_send_warning'),
]