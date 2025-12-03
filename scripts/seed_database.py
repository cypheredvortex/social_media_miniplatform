import os
import django
import sys
import random
from datetime import datetime

from bson import ObjectId  # Needed for Djongo ObjectId

# -------------------------------
# Setup Django environment
# -------------------------------
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

# -------------------------------
# Import models
# -------------------------------
from apps.user.models import User
from django.contrib.auth.hashers import make_password
from apps.post.models import Post
from apps.comment.models import Comment
from apps.like.models import Like
from apps.follow.models import Follow
from apps.report.models import Report
from apps.notification.models import Notification
from apps.profil.models import Profile
from apps.enums.models import VisibilityType, ReportTargetType, NotificationType

# -------------------------------
# Clear existing data
# -------------------------------
for model in [Notification, Report, Like, Comment, Post, Follow, Profile, User]:
    model.objects.all().delete()

# -------------------------------
# Seed Users
# -------------------------------
users = []
for i in range(5):
    # Give each seeded user a known password (password0, password1, ...)
    # and store it as a proper hash so authentication works.
    user = User.objects.create(
        username=f"user{i}",
        email=f"user{i}@example.com",
        password_hash=make_password(f"password{i}"),
        role="REGULAR",
        status="ACTIVE"
    )
    users.append(user)

# -------------------------------
# Seed Profiles
# -------------------------------
for user in users:
    Profile.objects.create(
        user=user,
        bio=f"Bio of {user.username}",
        location=f"City {random.randint(1, 100)}",
        avatar_url=f"https://picsum.photos/seed/{user.username}/200",
        birthdate=datetime(1990 + random.randint(0, 10), random.randint(1, 12), random.randint(1, 28)),
        website=f"https://example.com/{user.username}"
    )

# -------------------------------
# Seed Posts
# -------------------------------
posts = []
for i in range(5):
    post = Post.objects.create(
        author=random.choice(users),
        text=f"This is post {i}",
        image_url=f"https://picsum.photos/seed/post{i}/400",
        visibility=random.choice([v[0] for v in VisibilityType.choices])
    )
    posts.append(post)

# -------------------------------
# Seed Comments
# -------------------------------
comments = []
for i in range(5):
    comment = Comment.objects.create(
        author=random.choice(users),
        post=random.choice(posts),
        text=f"This is comment {i}"
    )
    comments.append(comment)

# -------------------------------
# Seed Likes
# -------------------------------
for i in range(5):
    Like.objects.create(
        user=random.choice(users),
        post=random.choice(posts),
        comment=random.choice(comments)
    )

# -------------------------------
# Seed Follows
# -------------------------------
for i in range(5):
    Follow.objects.create(
        follower=users[i],
        followed=users[(i + 1) % 5]
    )

# -------------------------------
# Seed Reports (users, posts, comments)
# -------------------------------
target_choices = ['USER', 'POST', 'COMMENT']
for i in range(5):
    target_type = random.choice(target_choices)
    report_data = {
        'reporter': random.choice(users),
        'target_type': target_type,
        'reason': f"This is report reason {i}"
    }
    if target_type == 'USER':
        report_data['target_user'] = random.choice(users)
    elif target_type == 'POST':
        report_data['target_user'] = None
    elif target_type == 'COMMENT':
        report_data['target_user'] = None

    Report.objects.create(**report_data)

# -------------------------------
# Seed Notifications
# -------------------------------
for i in range(5):
    Notification.objects.create(
        user=random.choice(users),
        type=random.choice([n[0] for n in NotificationType.choices]),
        message=f"This is notification {i}"
    )

print("✅ Database seeded successfully!")
