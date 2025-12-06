# scripts/seed_database.py

import os
import django
import random
from datetime import datetime, timedelta
from bson import ObjectId
from faker import Faker
from django.utils import timezone
import sys

# --- Setup Django environment ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

# --- Imports ---
from apps.user.models import User
from apps.profil.models import Profile
from apps.post.models import Post
from apps.comment.models import Comment
from apps.content.models import Content
from apps.report.models import Report
from apps.enums.models import VisibilityType, ContentStatus, ReportStatus, ReportTargetType, UserRole, UserStatus

fake = Faker()

# --- Parameters ---
NUM_USERS = 10
NUM_POSTS = 20
NUM_COMMENTS = 50
NUM_REPORTS = 20

# --- Step 0: Clear existing data ---
print("Clearing existing data...")
Report.objects.all().delete()
Comment.objects.all().delete()
Post.objects.all().delete()
Profile.objects.all().delete()
User.objects.all().delete()
Content.objects.all().delete()
print("Existing data cleared.")

# --- Step 1: Create Users ---
print("Seeding users...")
users = []

for i in range(NUM_USERS):
    last_login = timezone.make_aware(fake.date_time_this_year())
    
    user = User.objects.create(
        id=ObjectId(),
        username=f"user{i+1}",
        email=f"user{i+1}@example.com",
        password_hash="hashed_password",
        role=random.choice([UserRole.REGULAR, UserRole.ADMIN]),
        status=UserStatus.ACTIVE,  # adapted to your choices
        last_login=last_login
    )
    
    users.append(user)

print(f"Created {len(users)} users.")


# --- Step 2: Create Profiles ---
fake = Faker()

users = list(User.objects.all())
profiles = []

for user in users:
    profile = Profile.objects.create(
        id=ObjectId(),
        user=user,
        bio=fake.paragraph(nb_sentences=2),
        location=fake.city(),
        avatar_url=fake.image_url(),
        birthdate=fake.date_of_birth(minimum_age=18, maximum_age=70),
        website=fake.url()
    )
    profiles.append(profile)

print(f"Created {len(profiles)} profiles.")


# --- Step 3: Create Posts + Content ---
print("Seeding posts and content...")
posts = []
post_contents = {}
for _ in range(NUM_POSTS):
    author = random.choice(users)
    text = fake.sentence(nb_words=10)
    status = random.choice([ContentStatus.ACTIVE, ContentStatus.DELETED, ContentStatus.FLAGGED])
    
    post = Post.objects.create(
        id=ObjectId(),
        text=text,
        author=author,
        image_url=f"https://picsum.photos/200/300?random={random.randint(1,1000)}",
        visibility=random.choice([VisibilityType.PUBLIC, VisibilityType.FRIENDS_ONLY, VisibilityType.PRIVATE]),
        status=status,
        is_edited=False
    )
    posts.append(post)

    # Content for reports
    content = Content.objects.create(
        id=ObjectId(),
        text=text,
        status=status
    )
    post_contents[post.id] = content
    print(f"Created Post {post.id} by {author.username} with Content {content.id}")

# --- Step 4: Create Comments + Content ---
print("Seeding comments and content...")
comments = []
comment_contents = {}
for _ in range(NUM_COMMENTS):
    author = random.choice(users)
    post = random.choice(posts)
    parent_comment = random.choice(comments) if comments and random.random() < 0.3 else None
    text = fake.sentence(nb_words=8)
    status = random.choice([ContentStatus.ACTIVE, ContentStatus.DELETED, ContentStatus.FLAGGED])
    
    comment = Comment.objects.create(
        id=ObjectId(),
        text=text,
        author=author,
        post=post,
        parent_comment=parent_comment,
        status=status,
        is_edited=False
    )
    comments.append(comment)

    # Content for reports
    content = Content.objects.create(
        id=ObjectId(),
        text=text,
        status=status
    )
    comment_contents[comment.id] = content
    print(f"Created Comment {comment.id} by {author.username} with Content {content.id}")

# --- Step 5: Create Reports ---
print("Seeding reports...")
for _ in range(NUM_REPORTS):
    reporter = random.choice(users)
    target_type = random.choice([ReportTargetType.USER, ReportTargetType.POST, ReportTargetType.COMMENT])
    status = random.choice([ReportStatus.PENDING, ReportStatus.RESOLVED, ReportStatus.REJECTED])
    reason = fake.sentence(nb_words=5)
    
    target_user = None
    target_content = None
    
    if target_type == ReportTargetType.USER:
        target_user = random.choice([u for u in users if u != reporter])
    elif target_type == ReportTargetType.POST:
        post = random.choice(posts)
        target_user = post.author
        target_content = post_contents.get(post.id)
    else:  # COMMENT
        comment = random.choice(comments)
        target_user = comment.author
        target_content = comment_contents.get(comment.id)
    
    report = Report.objects.create(
        id=ObjectId(),
        reporter=reporter,
        target_type=target_type,
        target_user=target_user,
        target_content=target_content,
        reason=reason,
        status=status
    )
    print(f"Created Report {report.id} for {target_type}")

print("Seeding completed successfully!")
