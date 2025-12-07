import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

from apps.user.models import User
from apps.content.models import Content
from apps.profil.models import Profile
from apps.report.models import Report

print("Checking model ID field types...")
print("="*60)

# Check User model
user_field = User._meta.get_field('id')
print(f"User.id field type: {user_field.__class__.__name__}")
print(f"User.id internal type: {user_field.get_internal_type()}")

# Create a test user to see ID format
if User.objects.count() == 0:
    test_user = User.objects.create(
        username='testuser',
        email='test@example.com',
        password_hash='test'
    )
    print(f"Test User ID: {test_user.id}")
    print(f"Test User ID type: {type(test_user.id)}")
    test_user.delete()
else:
    user = User.objects.first()
    print(f"First User ID: {user.id}")
    print(f"First User ID type: {type(user.id)}")

print("\n" + "="*60)
print("If IDs are integers, you need to switch to ObjectIdField")