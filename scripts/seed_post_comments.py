import os
import django
import sys
import random
from datetime import datetime, timedelta
from bson import ObjectId

# --- Setup Django environment ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

from apps.user.models import User
from apps.post.models import Post
from apps.comment.models import Comment
from apps.enums.models import VisibilityType, ContentStatus

# --- Step 1: Clear existing posts and comments ---
print("Clearing existing Comment and Post entries...")
Comment.objects.all().delete()
Post.objects.all().delete()
print("Done.")

# --- Step 2: Sample data ---
sample_texts = [
    "Hello world! This is my first post.",
    "Exploring Django today!",
    "Just had the best coffee ever.",
    "My travel adventures begin here.",
    "Coding late into the night.",
    "Sharing some inspirational thoughts.",
    "Check out this amazing view!"
]

sample_images = [
    "https://picsum.photos/200/300?random=1",
    "https://picsum.photos/200/300?random=2",
    "https://picsum.photos/200/300?random=3",
    "",
    ""
]

visibility_options = [VisibilityType.PUBLIC, VisibilityType.FRIENDS_ONLY, VisibilityType.PRIVATE]

# --- Step 3: Create posts ---
users = list(User.objects.all())
if not users:
    raise Exception("No users found in the database. Create some users first!")

print("Seeding Post data...")
posts = []

for i in range(1, 21):  # create 20 posts
    author = random.choice(users)
    text = random.choice(sample_texts)
    image_url = random.choice(sample_images)
    visibility = random.choice(visibility_options)
    status = random.choice(['ACTIVE', 'DELETED', 'FLAGGED'])

    post = Post.objects.create(
        id=ObjectId(),
        author=author,
        text=text,
        image_url=image_url,
        visibility=visibility,
        status=status,
    )
    posts.append(post)
    print(f"Created Post: {post.id} by {post.author.username}")

# --- Step 4: Create comments ---
print("Seeding Comment data...")
sample_comments = [
    "Nice post!",
    "I totally agree.",
    "Can you explain more?",
    "Love this!",
    "Interesting perspective.",
    "Thanks for sharing!"
]

for post in posts:
    for _ in range(random.randint(1, 5)):  # 1-5 comments per post
        author = random.choice(users)
        text = random.choice(sample_comments)
        status = random.choice([ContentStatus.ACTIVE, ContentStatus.DELETED, ContentStatus.FLAGGED])

        comment = Comment.objects.create(
            id=ObjectId(),
            post=post,
            author=author,
            text=text,
            status=status
        )

        # optionally add a reply
        if random.random() < 0.3:  # 30% chance of a reply
            reply_author = random.choice(users)
            reply_text = random.choice(sample_comments)
            Comment.objects.create(
                id=ObjectId(),
                post=post,
                author=reply_author,
                text=reply_text,
                parent_comment=comment,
                status=status
            )

print("Seeding of posts and comments completed successfully!")
