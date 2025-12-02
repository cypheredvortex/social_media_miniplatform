from django.db import models

# Create your models here.
from djongo import models
from apps.user.models import User
from apps.content.models import Content
from apps.enums.models import ReportStatus, ReportTargetType

class Report(models.Model):
    id = models.ObjectIdField(primary_key=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    target_type = models.CharField(max_length=20, choices=ReportTargetType.choices)
    target_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='reports_received')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=ReportStatus.choices, default=ReportStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def resolve(self):
        self.status = ReportStatus.RESOLVED
        self.save()

    def reject(self):
        self.status = ReportStatus.REJECTED
        self.save()
