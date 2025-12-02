from django.db import models

# Create your models here.
from djongo import models
from apps.enums.models import UserRole, UserStatus

class User(models.Model):
    id = models.ObjectIdField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.REGULAR)
    status = models.CharField(max_length=20, choices=UserStatus.choices, default=UserStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def login(self, password):
        # implement password check
        pass

    def logout(self):
        pass

    def update_profile(self):
        pass

    def follow(self, user):
        pass

    def unfollow(self, user):
        pass
