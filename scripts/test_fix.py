import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

from apps.content.models import Content
from apps.user.models import User

print("=== Testing Content Model ===")
print(f"Content model has author field: {hasattr(Content, 'author')}")
print(f"Total Content objects: {Content.objects.count()}")
print(f"Total User objects: {User.objects.count()}")

if Content.objects.count() > 0:
    content = Content.objects.first()
    print(f"\nFirst Content:")
    print(f"  ID: {content.id}")
    print(f"  Type: {content.content_type}")
    print(f"  Author ID: {content.author_id}")
    print(f"  Author object: {content.author}")
    if content.author:
        print(f"  Author username: {content.author.username}")
    else:
        print(f"  WARNING: No author associated!")
        
    # Check all fields
    print(f"\nContent fields:")
    for field in Content._meta.fields:
        print(f"  {field.name}: {getattr(content, field.name, 'N/A')}")