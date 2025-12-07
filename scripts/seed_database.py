#!/usr/bin/env python
import os
import sys
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_miniplatform.settings')
django.setup()

from apps.user.models import User
from apps.content.models import Content
from apps.profil.models import Profile
from apps.follow.models import Follow
from apps.like.models import Like
from apps.report.models import Report
from apps.notification.models import Notification
from apps.enums.models import (
    UserRole, UserStatus, ContentStatus, 
    VisibilityType, ReportTargetType, ReportStatus,
    NotificationType
)

# Sample data
SAMPLE_BIOS = [
    "Software developer passionate about AI and ML.",
    "Digital artist creating amazing visuals.",
    "Travel enthusiast exploring the world one country at a time.",
    "Foodie who loves trying new restaurants.",
    "Fitness coach helping people reach their goals.",
    "Photographer capturing life's beautiful moments.",
    "Book lover getting lost in fictional worlds.",
    "Music producer creating beats that move you.",
    "Entrepreneur building the next big thing.",
    "Environmental activist making the world greener.",
]

SAMPLE_LOCATIONS = [
    "New York, USA",
    "London, UK",
    "Tokyo, Japan",
    "Paris, France",
    "Sydney, Australia",
    "Toronto, Canada",
    "Berlin, Germany",
    "Singapore",
    "Dubai, UAE",
    "São Paulo, Brazil",
]

SAMPLE_POST_TEXTS = [
    "Just finished an amazing hike in the mountains! The view was breathtaking. #adventure",
    "Learning Django has been an incredible journey. The framework is so powerful!",
    "Today's sunset was absolutely stunning. Nature never ceases to amaze me.",
    "Just launched my new website! Check it out and let me know what you think.",
    "Reading an amazing book about machine learning. So many insights!",
    "Cooked an amazing Italian dinner tonight. Pasta from scratch is the best!",
    "Working on a new art project. Can't wait to share it with everyone.",
    "Just completed my first marathon! The feeling is indescribable.",
    "Thinking about starting a podcast. Any topic suggestions?",
    "The future of AI is both exciting and a bit scary. What are your thoughts?",
]

SAMPLE_COMMENT_TEXTS = [
    "Great post! Thanks for sharing.",
    "I completely agree with this.",
    "Interesting perspective, I never thought about it that way.",
    "This inspired me to try something new!",
    "Can you share more details about this?",
    "Well said! Keep up the good work.",
    "I have a different take on this topic...",
    "This made my day! Thank you.",
    "Looking forward to seeing more content like this.",
    "What resources would you recommend for learning more?",
]

SAMPLE_REPORT_REASONS = [
    "Inappropriate content that violates community guidelines.",
    "This user is harassing other members.",
    "Spam or promotional content without disclosure.",
    "Hate speech or discriminatory language.",
    "False information or misinformation.",
    "Copyright infringement or stolen content.",
    "Impersonation of another user or public figure.",
    "Explicit content not suitable for all audiences.",
    "Promotion of illegal activities.",
    "Threatening or violent language.",
]

AVATAR_URLS = [
    "https://api.dicebear.com/7.x/avataaars/svg?seed=john",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=alice",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=bob",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=eva",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=mike",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=sarah",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=david",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=lisa",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=kevin",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=emma",
]

# Clear existing data (with safe deletion for MongoDB)
def clear_data():
    print("Clearing existing data...")
    
    # Delete in reverse order to avoid foreign key constraints
    try:
        Notification.objects.all().delete()
    except Exception as e:
        print(f"Warning clearing notifications: {e}")
    
    try:
        Report.objects.all().delete()
    except Exception as e:
        print(f"Warning clearing reports: {e}")
    
    try:
        Like.objects.all().delete()
    except Exception as e:
        print(f"Warning clearing likes: {e}")
    
    try:
        Follow.objects.all().delete()
    except Exception as e:
        print(f"Warning clearing follows: {e}")
    
    try:
        # For MongoDB, we need to handle Content deletion carefully
        # Delete comments first (child records)
        Content.objects.filter(content_type='COMMENT').delete()
        # Then delete posts
        Content.objects.filter(content_type='POST').delete()
    except Exception as e:
        print(f"Warning clearing content: {e}")
    
    try:
        Profile.objects.all().delete()
    except Exception as e:
        print(f"Warning clearing profiles: {e}")
    
    try:
        User.objects.all().delete()
    except Exception as e:
        print(f"Warning clearing users: {e}")
    
    print("Data cleared successfully!")

def create_users():
    print("\nCreating users...")
    
    users = [
        {
            'username': 'admin',
            'email': 'admin@social.com',
            'password': 'admin123',
            'role': UserRole.ADMIN,
            'status': UserStatus.ACTIVE
        },
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'password123',
            'role': UserRole.REGULAR,
            'status': UserStatus.ACTIVE
        },
        {
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'password': 'password123',
            'role': UserRole.REGULAR,
            'status': UserStatus.ACTIVE
        },
        {
            'username': 'alex_wong',
            'email': 'alex@example.com',
            'password': 'password123',
            'role': UserRole.REGULAR,
            'status': UserStatus.SUSPENDED
        },
        {
            'username': 'sarah_lee',
            'email': 'sarah@example.com',
            'password': 'password123',
            'role': UserRole.REGULAR,
            'status': UserStatus.ACTIVE
        },
        {
            'username': 'mike_jones',
            'email': 'mike@example.com',
            'password': 'password123',
            'role': UserRole.REGULAR,
            'status': UserStatus.BANNED
        },
        {
            'username': 'emma_wilson',
            'email': 'emma@example.com',
            'password': 'password123',
            'role': UserRole.REGULAR,
            'status': UserStatus.ACTIVE
        },
        {
            'username': 'david_brown',
            'email': 'david@example.com',
            'password': 'password123',
            'role': UserRole.REGULAR,
            'status': UserStatus.ACTIVE
        },
        {
            'username': 'lisa_chen',
            'email': 'lisa@example.com',
            'password': 'password123',
            'role': UserRole.REGULAR,
            'status': UserStatus.ACTIVE
        },
        {
            'username': 'kevin_miller',
            'email': 'kevin@example.com',
            'password': 'password123',
            'role': UserRole.REGULAR,
            'status': UserStatus.ACTIVE
        }
    ]
    
    created_users = []
    for user_data in users:
        # Check if user exists first
        try:
            user = User.objects.get(username=user_data['username'])
            print(f"  User already exists: {user.username}")
        except User.DoesNotExist:
            user = User.objects.create(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=make_password(user_data['password']),
                role=user_data['role'],
                status=user_data['status'],
                last_login=timezone.now() - timedelta(days=random.randint(1, 30))
            )
            print(f"  Created user: {user.username} ({user.role})")
        
        created_users.append(user)
    
    return created_users

def create_profiles(users):
    print("\nCreating profiles...")
    
    for i, user in enumerate(users):
        try:
            profile = Profile.objects.get(user=user)
            print(f"  Profile already exists for: {user.username}")
        except Profile.DoesNotExist:
            profile = Profile.objects.create(
                user=user,
                bio=random.choice(SAMPLE_BIOS),
                location=random.choice(SAMPLE_LOCATIONS),
                avatar_url=AVATAR_URLS[i % len(AVATAR_URLS)],
                birthdate=timezone.now().date() - timedelta(days=random.randint(20*365, 40*365)),
                website=f"https://{user.username}.com" if random.random() > 0.5 else ""
            )
            print(f"  Created profile for: {user.username}")

def create_posts(users):
    print("\nCreating posts...")
    
    posts = []
    for i in range(10):  # Reduced to 10 posts for simplicity
        author = random.choice([u for u in users if u.role == UserRole.REGULAR and u.status == UserStatus.ACTIVE])
        
        # Create post with random date (within last 30 days)
        post_date = timezone.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        
        try:
            post = Content.objects.create(
                author=author,
                text=f"Post #{i+1}: {random.choice(SAMPLE_POST_TEXTS)}",
                content_type='POST',
                media_type='TEXT',
                media_url=f"https://picsum.photos/800/600?random={i}" if random.random() > 0.7 else "",
                status=ContentStatus.ACTIVE,
                visibility=random.choice([VisibilityType.PUBLIC, VisibilityType.FRIENDS_ONLY]),
                created_at=post_date,
                updated_at=post_date
            )
            posts.append(post)
            
            print(f"  Created post by {author.username}: {post.text[:50]}...")
        except Exception as e:
            print(f"  Error creating post: {e}")
    
    return posts

def create_comments(users, posts):
    print("\nCreating comments...")
    
    all_comments = []
    for post in posts:
        # Create 1-3 comments per post
        num_comments = random.randint(1, 3)
        for i in range(num_comments):
            commenter = random.choice([u for u in users if u.status == UserStatus.ACTIVE])
            comment_date = post.created_at + timedelta(hours=random.randint(1, 48))
            
            try:
                comment = Content.objects.create(
                    author=commenter,
                    text=random.choice(SAMPLE_COMMENT_TEXTS),
                    content_type='COMMENT',
                    parent_content=post,
                    media_type='TEXT',
                    status=ContentStatus.ACTIVE,
                    visibility=VisibilityType.PUBLIC,
                    created_at=comment_date,
                    updated_at=comment_date
                )
                all_comments.append(comment)
            except Exception as e:
                print(f"  Error creating comment: {e}")
    
    # Count comments
    comment_count = Content.objects.filter(content_type='COMMENT').count()
    print(f"  Created {comment_count} comments")
    return all_comments

def create_follows(users):
    print("\nCreating follow relationships...")
    
    follow_count = 0
    for follower in users:
        # Each user follows 2-3 other users
        num_to_follow = random.randint(2, 3)
        possible_follows = [u for u in users if u != follower and u.status == UserStatus.ACTIVE]
        
        if len(possible_follows) > 0:
            num_to_follow = min(num_to_follow, len(possible_follows))
            to_follow = random.sample(possible_follows, num_to_follow)
            
            for followed in to_follow:
                if not Follow.objects.filter(follower=follower, followed=followed).exists():
                    try:
                        Follow.objects.create(
                            follower=follower,
                            followed=followed,
                            created_at=timezone.now() - timedelta(days=random.randint(1, 90))
                        )
                        follow_count += 1
                    except Exception as e:
                        print(f"  Error creating follow: {e}")
    
    print(f"  Created {follow_count} follow relationships")

def create_likes(users, posts, all_comments):
    print("\nCreating likes...")
    
    like_count = 0
    
    # Create likes for posts
    for post in posts:
        if post.status != ContentStatus.ACTIVE:
            continue
            
        # Each post gets 2-5 likes
        num_likes = random.randint(2, 5)
        possible_likers = [u for u in users if u.status == UserStatus.ACTIVE]
        
        if len(possible_likers) > 0:
            num_likes = min(num_likes, len(possible_likers))
            likers = random.sample(possible_likers, num_likes)
            
            for liker in likers:
                if not Like.objects.filter(user=liker, content=post).exists():
                    try:
                        # Create the Like object properly
                        like = Like()
                        like.user = liker
                        like.content = post
                        like.created_at = post.created_at + timedelta(minutes=random.randint(5, 240))
                        like.save()
                        like_count += 1
                    except Exception as e:
                        print(f"  Error creating like: {e}")
    
    # Also like some comments
    active_comments = [c for c in all_comments if c.status == ContentStatus.ACTIVE]
    
    if len(active_comments) > 0:
        comments_to_like = random.sample(active_comments, min(5, len(active_comments)))
        
        for comment in comments_to_like:
            liker = random.choice([u for u in users if u.status == UserStatus.ACTIVE])
            if not Like.objects.filter(user=liker, content=comment).exists():
                try:
                    like = Like()
                    like.user = liker
                    like.content = comment
                    like.created_at = comment.created_at + timedelta(minutes=random.randint(5, 60))
                    like.save()
                    like_count += 1
                except Exception as e:
                    print(f"  Error creating comment like: {e}")
    
    print(f"  Created {like_count} likes")

def create_reports(users, posts, all_comments):
    print("\nCreating reports...")
    
    reports = []
    for i in range(5):  # Reduced to 5 reports
        reporter = random.choice([u for u in users if u.status == UserStatus.ACTIVE])
        
        # Decide target type
        target_type = random.choice([ReportTargetType.CONTENT, ReportTargetType.USER])
        
        if target_type == ReportTargetType.CONTENT:
            # Report a post or comment
            all_content = posts + all_comments
            if all_content:
                content = random.choice(all_content)
                target_content = content
                target_user = None
            else:
                continue
        else:
            # Report a user
            possible_targets = [u for u in users if u != reporter and u.status in [UserStatus.ACTIVE, UserStatus.SUSPENDED]]
            if not possible_targets:
                continue
            target_user = random.choice(possible_targets)
            target_content = None
        
        try:
            report = Report.objects.create(
                reporter=reporter,
                target_type=target_type,
                target_user=target_user,
                target_content=target_content,
                reason=random.choice(SAMPLE_REPORT_REASONS),
                status=ReportStatus.PENDING,
                created_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
            reports.append(report)
            
            target_desc = target_user.username if target_user else f"content by {target_content.author.username}"
            print(f"  Created report by {reporter.username} against {target_desc}")
        except Exception as e:
            print(f"  Error creating report: {e}")
    
    return reports

def create_notifications(users):
    print("\nCreating notifications...")
    
    notification_count = 0
    
    # Create some sample notifications
    for user in users[:5]:  # Create notifications for first 5 users
        if user.status == UserStatus.ACTIVE:
            try:
                Notification.objects.create(
                    user=user,
                    type=NotificationType.LIKE,
                    message=f"Someone liked your post",
                    created_at=timezone.now() - timedelta(hours=random.randint(1, 24)),
                    is_read=random.random() > 0.3
                )
                notification_count += 1
                
                Notification.objects.create(
                    user=user,
                    type=NotificationType.COMMENT,
                    message=f"Someone commented on your post",
                    created_at=timezone.now() - timedelta(hours=random.randint(1, 48)),
                    is_read=random.random() > 0.3
                )
                notification_count += 1
            except Exception as e:
                print(f"  Error creating notification: {e}")
    
    print(f"  Created {notification_count} notifications")

def print_summary():
    print("\n" + "="*50)
    print("SEEDING SUMMARY")
    print("="*50)
    
    print(f"Users: {User.objects.count()}")
    print(f"Profiles: {Profile.objects.count()}")
    print(f"Posts: {Content.objects.filter(content_type='POST').count()}")
    print(f"Comments: {Content.objects.filter(content_type='COMMENT').count()}")
    print(f"Follows: {Follow.objects.count()}")
    print(f"Likes: {Like.objects.count()}")
    print(f"Reports: {Report.objects.count()}")
    print(f"Notifications: {Notification.objects.count()}")
    
    print("\nUser Details (first 5):")
    for user in User.objects.all()[:5]:
        print(f"  {user.username}: {user.role}, {user.status}")
    
    print("\n" + "="*50)

def main():
    print("Starting data seeding for Social Media Platform...")
    
    # Ask user if they want to clear existing data
    clear_existing = input("\nClear existing data before seeding? (y/n): ").lower() == 'y'
    
    if clear_existing:
        try:
            clear_data()
        except Exception as e:
            print(f"Warning during clear: {e}")
            print("Continuing with seeding...")
    
    try:
        # Create data
        users = create_users()
        create_profiles(users)
        posts = create_posts(users)
        all_comments = create_comments(users, posts)
        create_follows(users)
        create_likes(users, posts, all_comments)
        create_reports(users, posts, all_comments)
        create_notifications(users)
        
        print_summary()
        
        print("\n" + "="*50)
        print("SEEDING COMPLETE!")
        print("="*50)
        
        # Print login credentials
        print("\nLOGIN CREDENTIALS:")
        print("Admin: username='admin', password='admin123'")
        print("Regular Users: username='john_doe', password='password123' (and similar for others)")
        
    except Exception as e:
        print(f"\nError during seeding: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()