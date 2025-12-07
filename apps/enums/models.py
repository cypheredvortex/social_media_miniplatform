from django.db import models

# Create your models here.

class VisibilityType(models.TextChoices):
    PUBLIC = "PUBLIC"
    FRIENDS_ONLY = "FRIENDS_ONLY"
    PRIVATE = "PRIVATE"

class NotificationType(models.TextChoices):
    LIKE = "LIKE"
    COMMENT = "COMMENT"
    FOLLOW = "FOLLOW"
    REPLY = "REPLY"
    WARNING = "WARNING"

class ContentStatus(models.TextChoices):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    FLAGGED = "FLAGGED"

class UserRole(models.TextChoices):
    REGULAR = "REGULAR"
    ADMIN = "ADMIN"

class UserStatus(models.TextChoices):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    BANNED = "BANNED"

class ReportStatus(models.TextChoices):
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"

class ReportTargetType(models.TextChoices):
    CONTENT = "CONTENT"
    USER = "USER"