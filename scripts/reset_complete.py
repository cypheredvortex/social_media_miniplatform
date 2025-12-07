#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

def reset_project():
    print("Resetting project...")
    
    # 1. Delete all migration files
    base_dir = Path(__file__).parent
    migration_files = list(base_dir.rglob("*/migrations/*.py"))
    migration_files = [f for f in migration_files if f.name != "__init__.py"]
    
    for file in migration_files:
        print(f"Deleting: {file}")
        file.unlink()
    
    # 2. Delete all .pyc files
    pyc_files = list(base_dir.rglob("*/migrations/*.pyc"))
    for file in pyc_files:
        print(f"Deleting: {file}")
        try:
            file.unlink()
        except:
            pass
    
    # 3. Delete SQLite database if exists
    db_file = base_dir / "db.sqlite3"
    if db_file.exists():
        print(f"Deleting: {db_file}")
        db_file.unlink()
    
    # 4. Create __init__.py in migrations directories
    apps = [
        'user', 'content', 'like', 'follow', 'report', 
        'notification', 'profil', 'enums', 'pages'
    ]
    
    for app in apps:
        migrations_dir = base_dir / "apps" / app / "migrations"
        migrations_dir.mkdir(parents=True, exist_ok=True)
        init_file = migrations_dir / "__init__.py"
        if not init_file.exists():
            init_file.touch()
            print(f"Created: {init_file}")
    
    print("\nProject reset complete!")
    print("\nNext steps:")
    print("1. Drop MongoDB database: mongosh -> use social_media_miniplatform_db -> db.dropDatabase()")
    print("2. Run: python manage.py makemigrations")
    print("3. Run: python manage.py migrate")
    print("4. Create admin: python create_admin.py")

if __name__ == "__main__":
    reset_project()