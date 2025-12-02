from django.db import models

# Create your models here.
from django.db import models
from apps.user.models import User
from apps.content.models import Content
from apps.report.models import Report
from apps.enums.models import UserRole

class AdminActions(models.Model):
    class Meta:
        abstract = True

    def ban_user(self, user: User):
        user.status = "BANNED"
        user.save()

    def suspend_user(self, user: User):
        user.status = "SUSPENDED"
        user.save()

    def edit_user_role(self, user: User, role: UserRole):
        user.role = role
        user.save()

    def delete_content(self, content: Content):
        content.status = "DELETED"
        content.save()

    def edit_content(self, content: Content, text: str):
        content.edit(text)

    def approve_report(self, report: Report):
        report.resolve()

    def send_warning(self, user: User, message: str):
        from notification.models import Notification
        Notification.objects.create(user=user, type="WARNING", message=message)
