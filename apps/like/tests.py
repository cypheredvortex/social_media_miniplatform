from django.test import TestCase

# Create your tests here.
from django.urls import path
from . import views

urlpatterns = [
    path('like/', views.like_post, name='like_post'),
]
