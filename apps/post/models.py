from django.db import models

# Create your models here.
from djongo import models
from apps.content.models import Content
from apps.user.models import User
from apps.enums.models import VisibilityType

class Post(Content):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    visibility = models.CharField(max_length=20, choices=VisibilityType.choices, default=VisibilityType.PUBLIC)

    def add_comment(self, comment_text):
        from comment.models import Comment
        comment = Comment.objects.create(post=self, text=comment_text, author=self.author)
        return comment
