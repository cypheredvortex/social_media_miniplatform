from djongo import models
from bson import ObjectId
from apps.enums.models import UserRole, UserStatus

def generate_object_id():
    """Generate a new ObjectId as string for the default value"""
    return str(ObjectId())

class User(models.Model):
    id = models.ObjectIdField(primary_key=True, default=ObjectId)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.REGULAR)
    status = models.CharField(max_length=20, choices=UserStatus.choices, default=UserStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    warning_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_username(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        if self.role == UserRole.ADMIN:
            return True
        return False
    
    def has_module_perms(self, app_label):
        if self.role == UserRole.ADMIN:
            return True
        return False
    
    @property
    def is_staff(self):
        return self.role == UserRole.ADMIN
    
    @property
    def is_active(self):
        return self.status == UserStatus.ACTIVE