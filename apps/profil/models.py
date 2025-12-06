from django.db import models

# Create your models here.
from djongo import models
from apps.user.models import User

class Profile(models.Model):
    id = models.ObjectIdField(primary_key=True)  # <-- Change from IntegerField
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar_url = models.URLField(blank=True)
    birthdate = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)

    def update_info(self, bio=None, location=None, avatar_url=None, birthdate=None, website=None):
        if bio: self.bio = bio
        if location: self.location = location
        if avatar_url: self.avatar_url = avatar_url
        if birthdate: self.birthdate = birthdate
        if website: self.website = website
        self.save()
