# scripts/reseed_content.py

import os
import django
import sys
import random
from bson import ObjectId

# --- Setup Django environment ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

from apps.user.models import User
from apps.content.models import Content
from apps.report.models import Report
from apps.enums.models import ContentStatus, ReportStatus, ReportTargetType, UserRole

# --- Step 1: Clear existing data ---
print("Clearing existing Users, Content, and Report entries...")
Report.objects.all().delete()
Content.objects.all().delete()
User.objects.all().delete()
print("Done.")

# --- Step 2: Create sample Users ---
print("Creating sample users...")
usernames = ["alice", "bob", "charlie"]
users = []
for username in usernames:
    user = User.objects.create(
        id=ObjectId(),
        username=username,
        email=f"{username}@example.com",
        password_hash="hashed_password",  # replace with real hash if needed
        role=random.choice([UserRole.REGULAR, UserRole.ADMIN]),
    )
    users.append(user)
    print(f"Created User: {user.username} ({user.id})")

# --- Step 3: Create sample Content ---
print("Seeding Content...")
sample_texts = [
    "This is the first post.",
    "Hello world!",
    "Sample content for testing.",
    "Another interesting post.",
    "Lorem ipsum dolor sit amet.",
]

contents = []
for text in sample_texts:
    owner = random.choice(users)
    c = Content.objects.create(
        id=ObjectId(),
        text=text,
        status=random.choice([ContentStatus.ACTIVE, ContentStatus.DELETED, ContentStatus.FLAGGED]),
    )
    contents.append(c)
    print(f"Created Content: {c.id} -> {c.text[:30]}")

# --- Step 4: Create sample Reports ---
print("Seeding Reports...")
reasons = [
    "Spam content",
    "Offensive language",
    "Duplicate post",
    "Inappropriate content",
    "Other reason",
]

for content in contents:
    for _ in range(random.randint(1, 3)):  # 1-3 reports per content
        reporter = random.choice(users)
        report = Report.objects.create(
            id=ObjectId(),
            reporter=reporter,
            target_type=ReportTargetType.POST,
            target_user=None,  # optional
            target_content=content,
            reason=random.choice(reasons),
            status=ReportStatus.PENDING,
        )
        print(f"Created Report: {report.id} for Content {content.id}")

print("Reseeding completed successfully!")
