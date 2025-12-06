# scripts/reseed_content.py

import os
import django
import sys
import random
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

from bson import ObjectId
from apps.content.models import Content

# Optional: delete all old content first
Content.objects.all().delete()

# Create new content with proper ObjectIds
sample_texts = [
    "This is post 0",
    "This is post 1",
    "This is post 2",
    "This is post 3",
    "This is post 4",
    "This is post 5",
    "This is post 6",
    "This is post 7",
    "This is post 8",
    "This is post 9",
]

for text in sample_texts:
    Content.objects.create(
        id=ObjectId(),  # generate a new ObjectId
        text=text
    )

print("Content reseeded successfully with ObjectIds!")
