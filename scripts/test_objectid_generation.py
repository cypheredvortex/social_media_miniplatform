import os
import sys
import django
from bson import ObjectId

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

from apps.user.models import User

print("="*60)
print("TESTING ObjectId GENERATION")
print("="*60)

# Test 1: Create user without ID (should auto-generate ObjectId)
print("\nTest 1: Create user without specifying ID")
user1 = User.objects.create(
    username='test1',
    email='test1@example.com',
    password_hash='test1'
)
print(f"  Username: {user1.username}")
print(f"  ID: {user1.id}")
print(f"  ID type: {type(user1.id)}")
print(f"  Is ObjectId: {isinstance(user1.id, ObjectId)}")

# Test 2: Create user with explicit ObjectId
print("\nTest 2: Create user with explicit ObjectId")
obj_id = ObjectId()
user2 = User.objects.create(
    id=obj_id,
    username='test2',
    email='test2@example.com',
    password_hash='test2'
)
print(f"  Username: {user2.username}")
print(f"  ID: {user2.id}")
print(f"  Expected ID: {obj_id}")
print(f"  IDs match: {user2.id == obj_id}")

# Test 3: Check if IDs are 24-character hex strings
print("\nTest 3: Verify ObjectId format")
print(f"  User1 ID string: {str(user1.id)}")
print(f"  Length: {len(str(user1.id))} characters")
print(f"  Is hex: {all(c in '0123456789abcdef' for c in str(user1.id))}")

# Clean up
user1.delete()
user2.delete()

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)