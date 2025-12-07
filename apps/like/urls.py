from django.urls import path
from .views import like_post
from django.urls import register_converter
from bson import ObjectId

class ObjectIdConverter:
    regex = '[0-9a-f]{24}'
    
    def to_python(self, value):
        return ObjectId(value)
    
    def to_url(self, value):
        return str(value)

register_converter(ObjectIdConverter, 'objectid')

urlpatterns = [
    path("content/<objectid:content_id>/", like_post, name="like_content"),
]