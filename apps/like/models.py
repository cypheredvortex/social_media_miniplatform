from django.db import models

# Create your models here.
from djongo import models
from apps.user.models import User
from apps.post.models import Post
from apps.comment.models import Comment

class Like(models.Model):
    id = models.ObjectIdField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
