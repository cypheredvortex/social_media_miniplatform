from django.db import models

# Create your models here.
from djongo import models
from apps.user.models import User
from apps.enums.models import NotificationType

class Notification(models.Model):
    id = models.ObjectIdField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=NotificationType.choices)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True
        self.save()
