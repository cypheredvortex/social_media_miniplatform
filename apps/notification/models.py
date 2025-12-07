from djongo import models

# Create your models here.
from apps.user.models import User
from apps.content.models import Content
from apps.enums.models import NotificationType

class Notification(models.Model):
    id = models.ObjectIdField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=NotificationType.choices)
    message = models.TextField()
    content = models.ForeignKey(Content, null=True, blank=True, on_delete=models.CASCADE, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Fixed typo here

    def mark_as_read(self):
        self.is_read = True
        self.save()
    
    class Meta:
        db_table = 'notifications'

    def __str__(self):
        return f"{self.type} notification for {self.user.username}"
