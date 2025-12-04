from django.db import models

# Create your models here.
from djongo import models
from apps.user.models import User
from apps.enums.models import VisibilityType


class Post(models.Model):
    id = models.ObjectIdField(primary_key=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('ACTIVE','Active'), ('DELETED','Deleted'), ('FLAGGED','Flagged')], default='ACTIVE')
    # Link to Content model will be added by migration as a nullable FK named `content`
    # content = models.ForeignKey('content.Content', null=True, blank=True, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    visibility = models.CharField(max_length=20, choices=VisibilityType.choices, default=VisibilityType.PUBLIC)

    def add_comment(self, comment_text):
        from comment.models import Comment
        comment = Comment.objects.create(post=self, text=comment_text, author=self.author)
        return comment
