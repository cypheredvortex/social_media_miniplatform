from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from bson import ObjectId
from .models import User

class MongoDBAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        
        if check_password(password, user.password_hash):
            return user
        return None
    
    def get_user(self, user_id):
        try:
            # Convert string to ObjectId
            return User.objects.get(id=ObjectId(user_id))
        except (User.DoesNotExist, ValueError):
            return None