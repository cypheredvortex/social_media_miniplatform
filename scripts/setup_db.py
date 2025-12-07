#!/usr/bin/env python
import os
import sys
import django
from bson import ObjectId

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

from django.contrib.auth.hashers import make_password
from apps.user.models import User
from apps.enums.models import UserRole, UserStatus

def setup_database():
    print("Setting up database...")
    
    # Drop and recreate collections if needed
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    db = client['social_media_miniplatform_db']
    
    # Drop all collections to start fresh
    collections = db.list_collection_names()
    for collection in collections:
        print(f"Dropping collection: {collection}")
        db[collection].drop()
    
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        admin = User(
            id=str(ObjectId()),
            username='admin',
            email='admin@example.com',
            password_hash=make_password('admin123'),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        admin.save()
        print("Admin user created: username=admin, password=admin123")
    
    # Create a test regular user
    if not User.objects.filter(username='testuser').exists():
        testuser = User(
            id=str(ObjectId()),
            username='testuser',
            email='test@example.com',
            password_hash=make_password('test123'),
            role=UserRole.REGULAR,
            status=UserStatus.ACTIVE
        )
        testuser.save()
        print("Test user created: username=testuser, password=test123")
    
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()