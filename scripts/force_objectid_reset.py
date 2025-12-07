import os
import sys
import django
from pymongo import MongoClient
import subprocess

print("="*80)
print("FORCE ObjectIdField RESET")
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
print("\n2. Deleting all migration files...")
apps = ['user', 'content', 'profil', 'follow', 'like', 'notification', 'report', 'enums']

for app in apps:
    migrations_dir = os.path.join('apps', app, 'migrations')
    if os.path.exists(migrations_dir):
        for file in os.listdir(migrations_dir):
            file_path = os.path.join(migrations_dir, file)
            if file != '__init__.py':
                try:
                    os.remove(file_path)
                    print(f"   Removed: {file_path}")
                except:
                    pass
        print(f"   ✓ Cleared migrations for {app}")

# 3. Delete __pycache__ directories
print("\n3. Cleaning __pycache__ directories...")
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        cache_dir = os.path.join(root, '__pycache__')
        try:
            import shutil
            shutil.rmtree(cache_dir)
            print(f"   Removed: {cache_dir}")
        except:
            pass

# 4. Create fresh migrations with force
print("\n4. Creating fresh migrations...")
result = subprocess.run(['python', 'manage.py', 'makemigrations'], 
                       capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("Errors:", result.stderr)

# 5. Check migrations for ObjectIdField
print("\n5. Verifying migrations contain ObjectIdField...")
for app in apps:
    migration_file = os.path.join('apps', app, 'migrations', '0001_initial.py')
    if os.path.exists(migration_file):
        with open(migration_file, 'r') as f:
            content = f.read()
            if 'ObjectIdField' in content:
                print(f"   ✓ {app}: Contains ObjectIdField")
            else:
                print(f"   ✗ {app}: Missing ObjectIdField!")

# 6. Apply migrations
print("\n6. Applying migrations...")
result = subprocess.run(['python', 'manage.py', 'migrate'], 
                       capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("Errors:", result.stderr)

print("\n" + "="*80)
print("RESET COMPLETE!")
print("\nNow run: python scripts/test_objectid_generation.py")
print("="*80)