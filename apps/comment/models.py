from djongo import models
from apps.user.models import User
from apps.post.models import Post
from apps.enums.models import ContentStatus


class Comment(models.Model):
    id = models.ObjectIdField(primary_key=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=ContentStatus.choices, default=ContentStatus.ACTIVE)

    def reply(self, text, author):
        return Comment.objects.create(post=self.post, parent_comment=self, text=text, author=author)
