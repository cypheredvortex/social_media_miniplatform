import os
import sys
import shutil
import subprocess
from pymongo import MongoClient

def run_command(cmd):
    """Run a shell command and print output"""
    print(f"\n>>> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"STDERR: {result.stderr}")
    return result.returncode

print("="*80)
print("OBJECTID FIELD COMPLETE FIX")
print("="*80)

# 1. Drop MongoDB database
print("\n1. Dropping MongoDB database...")
try:
    client = MongoClient("mongodb://localhost:27017/")
    client.drop_database('social_media_miniplatform_db')
    print("   ✓ Database dropped")
except Exception as e:
    print(f"   ✗ Error: {e}")

# 2. Delete ALL migration files
print("\n2. Deleting ALL migration files...")
migration_files = []
for root, dirs, files in os.walk('.'):
    if 'migrations' in root:
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                filepath = os.path.join(root, file)
                try:
                    os.remove(filepath)
                    migration_files.append(filepath)
                except:
                    pass

if migration_files:
    print(f"   ✓ Removed {len(migration_files)} migration files")
else:
    print("   No migration files found")

# 3. Delete ALL __pycache__ directories
print("\n3. Deleting ALL __pycache__ directories...")
cache_dirs = []
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        cache_dir = os.path.join(root, '__pycache__')
        try:
            shutil.rmtree(cache_dir)
            cache_dirs.append(cache_dir)
        except:
            pass

if cache_dirs:
    print(f"   ✓ Removed {len(cache_dirs)} __pycache__ directories")

# 4. Create fresh migrations
print("\n4. Creating fresh migrations...")
run_command("python manage.py makemigrations")

# 5. Check migrations for CustomObjectIdField
print("\n5. Verifying migrations contain CustomObjectIdField...")
apps = ['user', 'content', 'profil', 'follow', 'like', 'notification', 'report']
for app in apps:
    migration_file = f"apps/{app}/migrations/0001_initial.py"
    if os.path.exists(migration_file):
        with open(migration_file, 'r') as f:
            content = f.read()
            if 'CustomObjectIdField' in content:
                print(f"   ✓ {app}: Contains CustomObjectIdField")
            else:
                print(f"   ✗ {app}: Missing CustomObjectIdField!")

# 6. Apply migrations
print("\n6. Applying migrations...")
run_command("python manage.py migrate")

# 7. Create a test to verify ObjectId
print("\n7. Creating test to verify ObjectId generation...")
test_code = '''
import os
import sys
import django
from bson import ObjectId

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

from apps.user.models import User

print("\\n" + "="*60)
print("OBJECTID VERIFICATION TEST")
print("="*60)

# Test 1: Create user
print("\\nTest 1: Creating user...")
user = User.objects.create(
    username="objectid_test",
    email="test@objectid.com",
    password_hash="test123",
    role="REGULAR",
    status="ACTIVE"
)

print(f"  Username: {user.username}")
print(f"  ID: {user.id}")
print(f"  ID type: {type(user.id)}")
print(f"  Is ObjectId: {isinstance(user.id, ObjectId)}")

if isinstance(user.id, ObjectId):
    print("  ✓ SUCCESS: ID is ObjectId!")
    print(f"  ObjectId hex: {str(user.id)}")
    print(f"  Length: {len(str(user.id))} chars (should be 24)")
else:
    print(f"  ✗ FAILED: ID is {type(user.id)}, not ObjectId")

# Test 2: Retrieve user
print("\\nTest 2: Retrieving user...")
retrieved = User.objects.get(id=user.id)
print(f"  Retrieved username: {retrieved.username}")
print(f"  IDs match: {user.id == retrieved.id}")

# Test 3: Create another user
print("\\nTest 3: Creating another user...")
user2 = User.objects.create(
    username="objectid_test2",
    email="test2@objectid.com",
    password_hash="test456"
)
print(f"  User2 ID: {user2.id}")
print(f"  IDs are different: {user.id != user2.id}")

# Clean up
user.delete()
user2.delete()
print("\\n✓ Test users deleted")

print("\\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
'''

with open('test_objectid_verify.py', 'w') as f:
    f.write(test_code)

print("\n8. Running ObjectId verification test...")
run_command("python test_objectid_verify.py")

print("\n" + "="*80)
print("OBJECTID FIX COMPLETE!")
print("\nIf the test shows ObjectIds, run: python scripts/seed_database.py")
print("="*80)