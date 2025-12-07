from djongo import models
from apps.user.models import User
from apps.enums.models import ContentStatus, VisibilityType, ReportTargetType, ReportStatus, NotificationType

# ---------------------------
# Base Content Model
# ---------------------------
class Content(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('POST', 'Post'),
        ('COMMENT', 'Comment'),
    ]
    MEDIA_TYPE_CHOICES = [
        ('TEXT', 'Text'),
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
    ]

    id = models.ObjectIdField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contents')
    text = models.TextField(blank=True)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='TEXT')
    media_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=ContentStatus.choices, default=ContentStatus.ACTIVE)
    parent_content = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )  # For comments replying to posts or other comments
    visibility = models.CharField(max_length=20, choices=VisibilityType.choices, default=VisibilityType.PUBLIC)

    def edit(self, text=None, media_url=None):
        if text is not None:
            self.text = text
        if media_url is not None:
            self.media_url = media_url
        self.is_edited = True
        self.save()

    def soft_delete(self):
        self.status = ContentStatus.DELETED
        self.save()

    def add_reply(self, text, author, media_url=None):
        return Content.objects.create(
            author=author,
            text=text,
            content_type='COMMENT',
            parent_content=self,
            media_type='TEXT' if not media_url else 'IMAGE',
            media_url=media_url
        )


# ---------------------------
# Proxy Models for Convenience
# ---------------------------
class Post(Content):
    class Meta:
        proxy = True

    def add_comment(self, text, author, media_url=None):
        return Content.objects.create(
            author=author,
            text=text,
            content_type='COMMENT',
            parent_content=self,
            media_type='TEXT' if not media_url else 'IMAGE',
            media_url=media_url
        )


class Comment(Content):
    class Meta:
        proxy = True

    def reply(self, text, author, media_url=None):
        return Content.objects.create(
            author=author,
            text=text,
            content_type='COMMENT',
            parent_content=self,
            media_type='TEXT' if not media_url else 'IMAGE',
            media_url=media_url
        )