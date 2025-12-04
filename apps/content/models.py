from djongo import models
from apps.enums.models import ContentStatus


class Content(models.Model):
    id = models.ObjectIdField(primary_key=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=ContentStatus.choices, default=ContentStatus.ACTIVE)

    def edit(self, text):
        self.text = text
        self.is_edited = True
        self.save()

    def soft_delete(self):
        """Soft-delete by setting status to DELETED."""
        self.status = ContentStatus.DELETED
        self.save()
