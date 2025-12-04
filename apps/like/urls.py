from django.urls import path
from .views import like_post

urlpatterns = [
    path("post/<str:post_id>", like_post, name="like_post"),
]
