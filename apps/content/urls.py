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

app_name = "content"

urlpatterns = [
    path('admin/', views.admin_content_list, name='admin_content_list'),
    path('admin/<objectid:content_id>/', views.admin_content_detail, name='admin_content_detail'),
    path('admin/<objectid:content_id>/delete/', views.admin_content_delete, name='admin_content_delete'),
    path('admin/<objectid:content_id>/flag/', views.admin_content_mark_flagged, name='admin_content_mark_flagged'),
    path('debug/', views.debug_content, name='debug_content'),
    
    # Add these regular user URLs
    path('create/', views.content_create, name='create'),
    path('<objectid:content_id>/', views.content_detail, name='detail'),
    path('<objectid:content_id>/edit/', views.content_edit, name='edit'),
    path('<objectid:content_id>/delete/', views.content_delete, name='delete'),
    path('<objectid:content_id>/comment/', views.add_comment, name='add_comment'),
]