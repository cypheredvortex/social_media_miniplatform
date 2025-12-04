import os
import django
from datetime import date
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

from apps.profil.models import Profile
from apps.user.models import User

# Fetch some existing users
users = list(User.objects.all()[:5])  # Get first 5 users, adjust if needed

# Prepare profile data
profiles_data = [
    {
        "id": 1,
        "bio": "Loves coding and coffee.",
        "location": "Casablanca, Morocco",
        "avatar_url": "https://example.com/avatar1.png",
        "birthdate": date(1995, 5, 21),
        "website": "https://user1.com"
    },
    {
        "id": 2,
        "bio": "Traveler and photographer.",
        "location": "Marrakech, Morocco",
        "avatar_url": "https://example.com/avatar2.png",
        "birthdate": date(1990, 11, 10),
        "website": "https://user2.com"
    },
    {
        "id": 3,
        "bio": "Foodie and chef.",
        "location": "Rabat, Morocco",
        "avatar_url": "https://example.com/avatar3.png",
        "birthdate": date(1988, 7, 3),
        "website": "https://user3.com"
    },
    {
        "id": 4,
        "bio": "Musician and writer.",
        "location": "Tangier, Morocco",
        "avatar_url": "https://example.com/avatar4.png",
        "birthdate": date(1992, 2, 14),
        "website": "https://user4.com"
    },
    {
        "id": 5,
        "bio": "Gamer and streamer.",
        "location": "Fes, Morocco",
        "avatar_url": "https://example.com/avatar5.png",
        "birthdate": date(1998, 9, 30),
        "website": "https://user5.com"
    }
]

# Insert profiles
for i, user in enumerate(users):
    profile_data = profiles_data[i]
    profile = Profile(
        id=profile_data["id"],
        user=user,
        bio=profile_data["bio"],
        location=profile_data["location"],
        avatar_url=profile_data["avatar_url"],
        birthdate=profile_data["birthdate"],
        website=profile_data["website"]
    )
    profile.save()
    print(f"Created profile for user {user.username}")

print("All profiles inserted successfully!")
