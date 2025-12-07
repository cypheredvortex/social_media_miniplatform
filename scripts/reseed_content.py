#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_miniplatform.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from apps.user.models import User
from apps.enums.models import UserRole, UserStatus

def create_users():
    print("Creating users...")
    
    # Delete any existing users
    User.objects.all().delete()
    
    # Create admin
    admin = User(
        username='admin',
        email='admin@example.com',
        password_hash=make_password('admin123'),
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE
    )
    admin.save()
    print("✓ Admin user created:")
    print("  Username: admin")
    print("  Password: admin123")
    print(f"  ID: {admin.id}")
    
    # Create test user
    testuser = User(
        username='testuser',
        email='test@example.com',
        password_hash=make_password('test123'),
        role=UserRole.REGULAR,
        status=UserStatus.ACTIVE
    )
    testuser.save()
    print("\n✓ Test user created:")
    print("  Username: testuser")
    print("  Password: test123")
    print(f"  ID: {testuser.id}")
    
    # Create your user
    your_user = User(
        username='dell',
        email='dell@gmail.com',
        password_hash=make_password('1234'),
        role=UserRole.REGULAR,
        status=UserStatus.ACTIVE
    )
    your_user.save()
    print("\n✓ Your user created:")
    print("  Username: dell")
    print("  Password: 1234")
    print(f"  ID: {your_user.id}")

if __name__ == "__main__":
    create_users()