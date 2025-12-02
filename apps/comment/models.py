from django.db import models

# Create your models here.
from djongo import models
from apps.content.models import Content
from apps.user.models import User
from apps.post.models import Post

class Comment(Content):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def reply(self, text, author):
        return Comment.objects.create(post=self.post, parent_comment=self, text=text, author=author)
