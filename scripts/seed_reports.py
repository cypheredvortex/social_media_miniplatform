# scripts/seed_data.py
import os
import django
import random
from datetime import datetime, timedelta
from bson import ObjectId
import sys

# --- Setup Django environment ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

from apps.user.models import User
from apps.profil.models import Profile
from apps.post.models import Post
from apps.comment.models import Comment
from apps.content.models import Content
from apps.enums.models import VisibilityType, ContentStatus, ReportStatus, ReportTargetType
from apps.report.models import Report

# --- Seed parameters ---
NUM_USERS = 20
NUM_PROFILES = NUM_USERS
NUM_POSTS = 50
NUM_COMMENTS = 100
NUM_REPORTS = 50

# --- Sample data ---
sample_usernames = [f'user{i}' for i in range(1, NUM_USERS+1)]
sample_bios = [
    "Loves coding", "Enjoys hiking", "Coffee enthusiast", "Tech blogger",
    "Traveler", "Music lover", "Foodie", "Gamer", "Photographer", "Writer"
]
sample_locations = ["New York", "Paris", "London", "Tokyo", "Berlin", "Sydney", "N/A"]
sample_post_texts = [
    "Hello world!", "My first post", "What a sunny day", "Feeling great today",
    "Check out this link", "Random thoughts", "I love coding", "Just chilling"
]
sample_comments = ["Nice!", "Agreed", "Well said", "I disagree", "Interesting...", "😂😂😂"]
sample_reasons = ["Spam", "Offensive content", "Harassment", "Fake news", "Other"]

# --- Step 0: Delete existing data safely ---
print("Deleting existing data...")

def safe_delete(model):
    for obj_id in model.objects.values_list('id', flat=True):
        model.objects.filter(id=obj_id).delete()

safe_delete(Report)
safe_delete(Comment)
safe_delete(Post)
safe_delete(Profile)
safe_delete(User)

print("Existing data deleted.")

# --- Step 1: Create users ---
print("Seeding users...")
users = []
for i in range(NUM_USERS):
    user = User.objects.create(
        id=ObjectId(),
        username=sample_usernames[i],
        email=f"{sample_usernames[i]}@example.com",
        password_hash="hashed_password",
        role="REGULAR",
        status="ACTIVE"
    )
    users.append(user)
print(f"Created {len(users)} users.")

# --- Step 2: Create profiles ---
print("Seeding profiles...")
profiles = []
for user in users:
    profile = Profile.objects.create(
        id=ObjectId(),
        user=user,
        bio=random.choice(sample_bios),
        location=random.choice(sample_locations),
        avatar_url=f"https://i.pravatar.cc/150?img={random.randint(1,70)}",
        birthdate=datetime.now().date() - timedelta(days=random.randint(5000, 15000)),
        website=f"https://www.{user.username}.com"
    )
    profiles.append(profile)
print(f"Created {len(profiles)} profiles.")

# --- Step 3: Create posts AND their content ---
print("Seeding posts and content...")
posts = []
for _ in range(NUM_POSTS):
    author = random.choice(users)
    post = Post.objects.create(
        id=ObjectId(),
        text=random.choice(sample_post_texts),
        author=author,
        image_url=f"https://picsum.photos/200/300?random={random.randint(1,1000)}",
        visibility=random.choice([VisibilityType.PUBLIC, VisibilityType.FRIENDS_ONLY, VisibilityType.PRIVATE]),
        status=random.choice([ContentStatus.ACTIVE, ContentStatus.DELETED, ContentStatus.FLAGGED])
    )
    # Create content immediately
    post_content = Content.objects.create(
        text=post.text,
        status=post.status
    )
    post.content = post_content
    post.save()
    posts.append(post)
print(f"Created {len(posts)} posts with content.")

# --- Step 4: Create comments AND their content ---
print("Seeding comments and content...")
comments = []
for _ in range(NUM_COMMENTS):
    author = random.choice(users)
    post = random.choice(posts)
    parent_comment = random.choice(comments) if comments and random.random() < 0.3 else None
    comment = Comment.objects.create(
        id=ObjectId(),
        text=random.choice(sample_comments),
        author=author,
        post=post,
        parent_comment=parent_comment,
        status=random.choice([ContentStatus.ACTIVE, ContentStatus.DELETED, ContentStatus.FLAGGED])
    )
    # Create content immediately
    comment_content = Content.objects.create(
        text=comment.text,
        status=comment.status
    )
    comment.content = comment_content
    comment.save()
    comments.append(comment)
print(f"Created {len(comments)} comments with content.")

# --- Step 5: Create reports ---
print("Seeding reports...")
reports = []
for _ in range(NUM_REPORTS):
    reporter = random.choice(users)
    target_type = random.choice([ReportTargetType.USER, ReportTargetType.POST, ReportTargetType.COMMENT])
    reason = random.choice(sample_reasons)
    status = random.choice([ReportStatus.PENDING, ReportStatus.RESOLVED, ReportStatus.REJECTED])

    target_user = None
    target_content = None

    if target_type == ReportTargetType.USER:
        target_user = random.choice([u for u in users if u != reporter])
    elif target_type == ReportTargetType.POST:
        post = random.choice(posts)
        target_user = post.author
        target_content = post.content  # Guaranteed to exist
    else:  # COMMENT
        comment = random.choice(comments)
        target_user = comment.author
        target_content = comment.content  # Guaranteed to exist

    report = Report.objects.create(
        id=ObjectId(),
        reporter=reporter,
        target_type=target_type,
        target_user=target_user,
        target_content=target_content,
        reason=reason,
        status=status
    )
    reports.append(report)
print(f"Created {len(reports)} reports.")
