from djongo import models

# Create your models here.
from apps.user.models import User
from apps.content.models import Content

class Like(models.Model):
    id = models.ObjectIdField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, null=True, blank=True, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content')