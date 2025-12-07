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

app_name = "follow"

urlpatterns = [
    path('follow/<objectid:user_id>/', views.follow_user, name='follow'),
    path('unfollow/<objectid:user_id>/', views.unfollow_user, name='unfollow'),
    path('followers/', views.followers_list, name='followers'),
    path('following/', views.following_list, name='following'),
]